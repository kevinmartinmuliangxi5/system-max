"""
工作记忆 - 存储当前会话的临时信息

类似人类的工作记忆，容量有限，会话结束即清空。
特点：
- 快速访问：使用deque和dict实现O(1)访问
- 容量限制：自动淘汰最旧的数据
- 会话隔离：会话结束后完全清空
- 多类型存储：支持消息、上下文、状态等
"""

from typing import List, Dict, Any, Optional, Deque, Union
from collections import deque, OrderedDict
from threading import Lock
from .base import BaseMemory, MemoryConfig, MemoryType, MemoryEntry, MemoryQuery


class WorkingMemory(BaseMemory):
    """
    工作记忆 - 存储当前会话的临时信息

    工作记忆是系统的短期缓存，用于：
    - 存储当前会话的对话消息
    - 维护会话上下文（如当前任务、用户偏好）
    - 跟踪临时状态（如进度标记、中间结果）

    特性：
    - 自动容量管理：使用deque的maxlen自动淘汰
    - 线程安全：使用Lock保护并发访问
    - 快速检索：O(1)的上下文查找
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        super().__init__(config, MemoryType.WORKING)
        self.max_items = self.config.working_max_items
        self._lock = Lock()

        # 消息队列 - 自动淘汰最旧消息
        self.messages: Deque[Dict[str, Any]] = deque(maxlen=self.max_items)

        # 上下文字典 - 会话状态
        self.context: Dict[str, Any] = {}

        # 状态字典 - 临时状态跟踪
        self.state: Dict[str, Any] = {}

    def save(self, data: Union[Dict[str, Any], MemoryEntry]) -> bool:
        """
        保存数据到工作记忆

        Args:
            data: 要保存的数据，支持格式：
                - {'type': 'message', 'content': {...}}
                - {'type': 'context', 'key': str, 'value': any}
                - {'type': 'state', 'key': str, 'value': any}
                - MemoryEntry实例

        Returns:
            bool: 保存是否成功
        """
        try:
            with self._lock:
                if isinstance(data, MemoryEntry):
                    self.messages.append(data.to_dict())
                    return True

                data_type = data.get('type', 'message')

                if data_type == 'message':
                    content = data.get('content', data)
                    self.messages.append({
                        "timestamp": self._now(),
                        "content": content
                    })
                elif data_type == 'context':
                    key = data.get('key')
                    value = data.get('value')
                    if key:
                        self.context[key] = {
                            "value": value,
                            "timestamp": self._now()
                        }
                elif data_type == 'state':
                    key = data.get('key')
                    value = data.get('value')
                    if key:
                        self.state[key] = {
                            "value": value,
                            "timestamp": self._now()
                        }
                else:
                    # 默认作为消息处理
                    self.messages.append({
                        "timestamp": self._now(),
                        "content": data
                    })

                return True
        except Exception:
            # 静默失败，工作记忆是临时的，不应影响主流程
            return False

    def load(self, query: Union[Dict[str, Any], MemoryQuery]) -> List[Dict[str, Any]]:
        """
        从工作记忆加载数据

        Args:
            query: 查询条件，支持：
                - {'type': 'messages', 'n': int} - 获取最近n条消息
                - {'type': 'context', 'key': str} - 获取上下文
                - {'type': 'state', 'key': str} - 获取状态
                - {'type': 'all'} - 获取所有数据

        Returns:
            List[Dict]: 查询结果
        """
        with self._lock:
            query_type = query.get('type', 'all') if isinstance(query, dict) else query.query_type

            if query_type == 'messages' or query_type == 'message':
                n = query.get('n', query.get('limit', 10)) if isinstance(query, dict) else query.limit
                recent = self.get_recent(n)
                return [{"message": msg} for msg in recent]

            elif query_type == 'context':
                key = query.get('key') if isinstance(query, dict) else query.filters.get('key')
                if key:
                    entry = self.context.get(key)
                    if entry:
                        return [{"key": key, **entry}]
                    return []
                return [{"key": k, **v} for k, v in self.context.items()]

            elif query_type == 'state':
                key = query.get('key') if isinstance(query, dict) else query.filters.get('key')
                if key:
                    entry = self.state.get(key)
                    if entry:
                        return [{"key": key, **entry}]
                    return []
                return [{"key": k, **v} for k, v in self.state.items()]

            else:
                # 返回所有消息
                return [{"message": msg} for msg in self.messages]

    def clear(self) -> None:
        """清空工作记忆"""
        with self._lock:
            self.messages.clear()
            self.context.clear()
            self.state.clear()

    def count(self) -> int:
        """
        返回记忆项数量

        Returns:
            int: 消息数 + 上下文数 + 状态数
        """
        with self._lock:
            return len(self.messages) + len(self.context) + len(self.state)

    # ==================== 便捷方法 ====================

    def add_message(self, message: Dict[str, Any]) -> None:
        """
        添加消息到工作记忆

        Args:
            message: 消息内容
        """
        self.save({"type": "message", "content": message})

    def get_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        获取最近n条消息

        Args:
            n: 返回消息数量

        Returns:
            List[Dict]: 最近的消息列表
        """
        with self._lock:
            return list(self.messages)[-n:]

    def set_context(self, key: str, value: Any) -> None:
        """
        设置上下文

        Args:
            key: 上下文键
            value: 上下文值
        """
        self.save({"type": "context", "key": key, "value": value})

    def get_context(self, key: str, default: Any = None) -> Any:
        """
        获取上下文值

        Args:
            key: 上下文键
            default: 默认值

        Returns:
            Any: 上下文值或默认值
        """
        with self._lock:
            entry = self.context.get(key)
            return entry["value"] if entry else default

    def get_all_context(self) -> Dict[str, Any]:
        """
        获取所有上下文

        Returns:
            Dict[str, Any]: 所有上下文的浅拷贝
        """
        with self._lock:
            return {k: v["value"] for k, v in self.context.items()}

    def set_state(self, key: str, value: Any) -> None:
        """
        设置临时状态

        Args:
            key: 状态键
            value: 状态值
        """
        self.save({"type": "state", "key": key, "value": value})

    def get_state(self, key: str, default: Any = None) -> Any:
        """
        获取状态值

        Args:
            key: 状态键
            default: 默认值

        Returns:
            Any: 状态值或默认值
        """
        with self._lock:
            entry = self.state.get(key)
            return entry["value"] if entry else default

    def peek_messages(self) -> List[Dict[str, Any]]:
        """
        查看所有消息（不弹出）

        Returns:
            List[Dict]: 所有消息的副本
        """
        with self._lock:
            return list(self.messages)
