"""
记忆管理器 - 统一管理三层记忆系统

协调工作记忆、情景记忆和语义记忆之间的交互。
实现记忆流动：工作记忆→情景记忆→语义记忆
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum
from threading import Lock

from .base import MemoryConfig, MemoryEntry, MemoryType
from .working import WorkingMemory
from .episodic import EpisodicMemory
from .semantic import SemanticMemory


class MemoryFlow(Enum):
    """
    记忆流动方向

    定义记忆在不同层级之间的流动方向：
    - CONSOLIDATE: 工作记忆 → 情景记忆（巩固）
    - ABSTRACT: 情景记忆 → 语义记忆（抽象化）
    - FULL_CYCLE: 完整周期（工作→情景→语义）
    - RETRIEVE: 从长期记忆检索到工作记忆
    """
    CONSOLIDATE = "consolidate"  # 巩固：工作→情景
    ABSTRACT = "abstract"        # 抽象：情景→语义
    FULL_CYCLE = "full_cycle"    # 完整周期：工作→情景→语义
    RETRIEVE = "retrieve"        # 检索：长期→工作


class MemoryManager:
    """
    记忆管理器 - 统一管理三层记忆

    三层记忆架构：
    1. 工作记忆 (Working Memory) - 当前会话临时信息，会话结束清空
    2. 情景记忆 (Episodic Memory) - 历史协作记录，可检索相似任务
    3. 语义记忆 (Semantic Memory) - 成功模式、最佳实践等抽象知识

    记忆流动：
        Working Memory (Session)
             ↓ consolidation
        Episodic Memory (History)
             ↓ abstraction
        Semantic Memory (Patterns)

    使用示例：
        ```python
        manager = MemoryManager()

        # 添加工作记忆
        manager.add_message({"role": "user", "content": "Hello"})

        # 保存协作经验（自动触发记忆流动）
        manager.save_collaboration_experience(
            task="Implement feature X",
            config={...},
            result={...},
            emergence_score=0.85
        )

        # 检索相似经验
        similar = manager.get_similar_experiences("Implement feature Y")

        # 获取推荐配置
        config = manager.recommend_config("Implement feature Z")
        ```
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        """
        初始化记忆管理器

        Args:
            config: 记忆系统配置
        """
        self.config = config or MemoryConfig()
        self._lock = Lock()

        # 初始化三层记忆
        self.working = WorkingMemory(self.config)
        self.episodic = EpisodicMemory(self.config)
        self.semantic = SemanticMemory(self.config)

        # 统计信息
        self._stats = {
            'total_consolidations': 0,
            'total_abstractions': 0,
            'last_consolidation': None,
            'last_abstraction': None,
        }

    # ==================== 协作经验管理 ====================

    def save_collaboration_experience(
        self,
        task: str,
        config: Dict[str, Any],
        result: Dict[str, Any],
        emergence_score: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        保存协作经验到长期记忆（自动触发记忆流动）

        根据涌现分数自动决定记忆流动：
        - emergence_score >= consolidation_threshold: 工作记忆 → 情景记忆
        - emergence_score >= abstraction_threshold: 进一步抽象到语义记忆

        Args:
            task: 任务描述
            config: 协作配置
            result: 协作结果
            emergence_score: 涌现分数 (0.0 - 1.0)
            metadata: 额外元数据

        Returns:
            Dict[str, Any]: 保存结果，包含流动信息
        """
        metadata = metadata or {}
        flow_info = {
            'consolidated': False,
            'abstracted': False,
            'timestamp': self._now()
        }

        episode_data = {
            'task': task,
            'config': config,
            'result': result,
            'emergence_score': emergence_score,
            'metadata': metadata
        }

        # 第一层：保存到情景记忆（巩固）
        if emergence_score >= self.config.consolidation_threshold:
            self.episodic.save(episode_data)
            flow_info['consolidated'] = True
            self._stats['total_consolidations'] += 1
            self._stats['last_consolidation'] = self._now()

        # 第二层：抽象到语义记忆
        if emergence_score >= self.config.abstraction_threshold:
            pattern_name = self.semantic.save_success_pattern(
                task=task,
                config=config,
                emergence_score=emergence_score
            )
            flow_info['abstracted'] = True
            flow_info['pattern_name'] = pattern_name
            self._stats['total_abstractions'] += 1
            self._stats['last_abstraction'] = self._now()

        return flow_info

    def recommend_config(self, task: str) -> Optional[Dict[str, Any]]:
        """
        基于历史推荐配置

        从情景记忆中检索相似任务的最佳配置。

        Args:
            task: 当前任务描述

        Returns:
            Optional[Dict]: 推荐的配置，没有相似历史时返回None
        """
        best_configs = self.episodic.load({
            'type': 'best_configs',
            'task': task
        })

        if best_configs:
            return best_configs[0].get('config')
        return None

    def get_similar_experiences(
        self,
        task: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        获取相似的历史经验

        Args:
            task: 当前任务描述
            top_k: 返回前k个最相似的经验

        Returns:
            List[Dict]: 相似的历史情景列表
        """
        return self.episodic.load({
            'type': 'similar',
            'task': task,
            'top_k': top_k
        })

    # ==================== 工作记忆管理 ====================

    def add_message(self, message: Dict[str, Any]) -> None:
        """
        添加消息到工作记忆

        Args:
            message: 消息内容
        """
        self.working.add_message(message)

    def get_recent_messages(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        获取最近的消息

        Args:
            n: 返回消息数量

        Returns:
            List[Dict]: 最近的消息列表
        """
        return self.working.get_recent(n)

    def set_context(self, key: str, value: Any) -> None:
        """
        设置工作记忆上下文

        Args:
            key: 上下文键
            value: 上下文值
        """
        self.working.set_context(key, value)

    def get_context(self, key: str, default: Any = None) -> Any:
        """
        获取工作记忆上下文

        Args:
            key: 上下文键
            default: 默认值

        Returns:
            Any: 上下文值或默认值
        """
        return self.working.get_context(key, default)

    def set_state(self, key: str, value: Any) -> None:
        """
        设置临时状态

        Args:
            key: 状态键
            value: 状态值
        """
        self.working.set_state(key, value)

    def get_state(self, key: str, default: Any = None) -> Any:
        """
        获取临时状态

        Args:
            key: 状态键
            default: 默认值

        Returns:
            Any: 状态值或默认值
        """
        return self.working.get_state(key, default)

    # ==================== 语义记忆管理 ====================

    def get_success_patterns(self) -> List[Dict[str, Any]]:
        """
        获取所有成功模式

        Returns:
            List[Dict]: 成功模式列表
        """
        return self.semantic.get_success_patterns()

    def get_pattern(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """
        获取指定模式

        Args:
            pattern_name: 模式名称

        Returns:
            Optional[Dict]: 模式数据
        """
        return self.semantic.get_pattern(pattern_name)

    def save_pattern(
        self,
        pattern_name: str,
        pattern_data: Dict[str, Any]
    ) -> bool:
        """
        保存模式到语义记忆

        Args:
            pattern_name: 模式名称
            pattern_data: 模式数据

        Returns:
            bool: 是否保存成功
        """
        return self.semantic.save_pattern(pattern_name, pattern_data)

    # ==================== 记忆流动控制 ====================

    def consolidate_working_memory(self, threshold: Optional[float] = None) -> int:
        """
        手动触发工作记忆巩固

        将工作记忆中的重要内容转移到情景记忆。
        通常在会话结束时调用。

        Args:
            threshold: 巩固阈值，默认使用配置值

        Returns:
            int: 巩固的记忆项数量
        """
        threshold = threshold or self.config.consolidation_threshold
        count = 0

        # 获取工作记忆中的所有消息
        messages = self.working.load({'type': 'all'})

        for msg in messages:
            # 假设所有工作记忆都值得保存（可根据实际策略调整）
            self.episodic.save({
                'task': str(msg.get('content', {})),
                'config': {},
                'result': {},
                'emergence_score': threshold,
                'metadata': {'source': 'working_memory'}
            })
            count += 1

        if count > 0:
            self._stats['total_consolidations'] += count
            self._stats['last_consolidation'] = self._now()

        return count

    def abstract_episodic_to_semantic(self, threshold: Optional[float] = None) -> int:
        """
        手动触发情景记忆抽象

        将情景记忆中高涌现分数的经验抽象为语义模式。

        Args:
            threshold: 抽象阈值，默认使用配置值

        Returns:
            int: 抽象的模式数量
        """
        threshold = threshold or self.config.abstraction_threshold
        count = 0

        # 获取所有情景
        episodes = self.episodic.load({'type': 'all'})

        for ep in episodes:
            score = ep.get('emergence_score', 0)
            if score >= threshold:
                self.semantic.save_success_pattern(
                    task=ep.get('task', ''),
                    config=ep.get('config', {}),
                    emergence_score=score
                )
                count += 1

        if count > 0:
            self._stats['total_abstractions'] += count
            self._stats['last_abstraction'] = self._now()

        return count

    # ==================== 会话管理 ====================

    def cleanup_session(self) -> None:
        """
        清理会话（保留长期记忆）

        在会话结束时调用，清空工作记忆但保留情景和语义记忆。
        """
        self.working.clear()

    def get_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息

        Returns:
            Dict[str, Any]: 包含各层记忆数量和流动统计
        """
        return {
            'working_memory_count': self.working.count(),
            'episodic_memory_count': self.episodic.count(),
            'semantic_memory_count': self.semantic.count(),
            'total_experiences': self.episodic.count(),
            'total_patterns': self.semantic.count(),
            'flow_stats': self._stats.copy()
        }

    # ==================== 批量操作 ====================

    def export_all_memories(self) -> Dict[str, Any]:
        """
        导出所有记忆数据

        Returns:
            Dict[str, Any]: 包含所有层级的记忆数据
        """
        return {
            'working': {
                'messages': list(self.working.messages),
                'context': self.working.get_all_context(),
            },
            'episodic': self.episodic.load({'type': 'all'}),
            'semantic': self.semantic.load({'type': 'all'}),
            'stats': self.get_stats(),
            'export_timestamp': self._now()
        }

    # ==================== 内部方法 ====================

    def _now(self) -> str:
        """获取当前时间戳"""
        return datetime.now().isoformat()
