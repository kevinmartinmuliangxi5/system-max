#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
会话捕获Hook系统

实现5个生命周期Hook:
1. session-start: 会话开始
2. user-prompt-submit: 用户提交提示
3. tool-call: 工具调用
4. assistant-response: 助手响应
5. session-end: 会话结束
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from enum import Enum


class HookType(Enum):
    """Hook类型枚举"""
    SESSION_START = "session_start"
    USER_PROMPT_SUBMIT = "user_prompt_submit"
    TOOL_CALL = "tool_call"
    ASSISTANT_RESPONSE = "assistant_response"
    SESSION_END = "session_end"


class SessionCapture:
    """会话捕获系统"""

    def __init__(self, storage_dir: str = ".ralph/memories/captures"):
        """
        初始化会话捕获

        Args:
            storage_dir: 存储目录
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # 当前会话
        self.current_session_id: Optional[str] = None
        self.current_session: Dict = {}

        # Hook回调
        self.hooks: Dict[HookType, List[Callable]] = {
            hook_type: [] for hook_type in HookType
        }

    def start_session(self, metadata: Optional[Dict] = None) -> str:
        """
        开始新会话

        Args:
            metadata: 会话元数据

        Returns:
            会话ID
        """
        # 如果有未结束的会话，先结束它
        if self.current_session_id:
            self.end_session()

        # 生成新会话ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_session_id = f"capture_{timestamp}"

        # 初始化会话数据
        self.current_session = {
            "id": self.current_session_id,
            "start_time": datetime.now().isoformat(),
            "metadata": metadata or {},
            "interactions": [],
            "tool_calls": [],
            "decisions": [],
            "learnings": [],
            "errors": [],
            "end_time": None
        }

        # 触发session-start hook
        self._trigger_hook(HookType.SESSION_START, {
            "session_id": self.current_session_id,
            "metadata": metadata
        })

        print(f"✓ 会话已启动: {self.current_session_id}")
        return self.current_session_id

    def capture_user_prompt(self, prompt: str, context: Optional[Dict] = None):
        """
        捕获用户提示

        Args:
            prompt: 用户输入的提示
            context: 上下文信息
        """
        if not self.current_session_id:
            self.start_session()

        interaction = {
            "type": "user_prompt",
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "context": context or {}
        }

        self.current_session["interactions"].append(interaction)

        # 触发hook
        self._trigger_hook(HookType.USER_PROMPT_SUBMIT, interaction)

    def capture_tool_call(
        self,
        tool_name: str,
        parameters: Dict,
        result: Optional[Any] = None
    ):
        """
        捕获工具调用

        Args:
            tool_name: 工具名称
            parameters: 调用参数
            result: 调用结果
        """
        if not self.current_session_id:
            return

        tool_call = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "parameters": parameters,
            "result": str(result)[:200] if result else None  # 限制长度
        }

        self.current_session["tool_calls"].append(tool_call)

        # 触发hook
        self._trigger_hook(HookType.TOOL_CALL, tool_call)

    def capture_assistant_response(
        self,
        response: str,
        metadata: Optional[Dict] = None
    ):
        """
        捕获助手响应

        Args:
            response: 助手响应内容
            metadata: 元数据
        """
        if not self.current_session_id:
            return

        interaction = {
            "type": "assistant_response",
            "timestamp": datetime.now().isoformat(),
            "response": response,
            "metadata": metadata or {}
        }

        self.current_session["interactions"].append(interaction)

        # 触发hook
        self._trigger_hook(HookType.ASSISTANT_RESPONSE, interaction)

    def capture_decision(self, decision: Dict):
        """
        捕获决策信息

        Args:
            decision: 决策信息
        """
        if not self.current_session_id:
            return

        decision_record = {
            "timestamp": datetime.now().isoformat(),
            **decision
        }

        self.current_session["decisions"].append(decision_record)

    def capture_learning(self, learning: Dict):
        """
        捕获学习经验

        Args:
            learning: 学习信息
        """
        if not self.current_session_id:
            return

        learning_record = {
            "timestamp": datetime.now().isoformat(),
            **learning
        }

        self.current_session["learnings"].append(learning_record)

    def capture_error(self, error: Dict):
        """
        捕获错误信息

        Args:
            error: 错误信息
        """
        if not self.current_session_id:
            return

        error_record = {
            "timestamp": datetime.now().isoformat(),
            **error
        }

        self.current_session["errors"].append(error_record)

    def end_session(self, summary: Optional[str] = None) -> Optional[Dict]:
        """
        结束会话

        Args:
            summary: 会话摘要

        Returns:
            完整的会话数据
        """
        if not self.current_session_id:
            return None

        # 更新结束时间
        self.current_session["end_time"] = datetime.now().isoformat()
        if summary:
            self.current_session["summary"] = summary

        # 保存会话数据
        session_file = self.storage_dir / f"{self.current_session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_session, f, indent=2, ensure_ascii=False)

        # 触发hook
        self._trigger_hook(HookType.SESSION_END, {
            "session_id": self.current_session_id,
            "session_data": self.current_session
        })

        print(f"✓ 会话已结束并保存: {self.current_session_id}")

        # 返回会话数据
        session_data = self.current_session.copy()

        # 重置当前会话
        self.current_session_id = None
        self.current_session = {}

        return session_data

    def register_hook(self, hook_type: HookType, callback: Callable):
        """
        注册Hook回调

        Args:
            hook_type: Hook类型
            callback: 回调函数
        """
        if hook_type not in self.hooks:
            self.hooks[hook_type] = []

        self.hooks[hook_type].append(callback)
        print(f"✓ 已注册 {hook_type.value} hook")

    def _trigger_hook(self, hook_type: HookType, data: Dict):
        """
        触发Hook

        Args:
            hook_type: Hook类型
            data: 传递给回调的数据
        """
        callbacks = self.hooks.get(hook_type, [])
        for callback in callbacks:
            try:
                callback(data)
            except Exception as e:
                print(f"警告: Hook回调失败 ({hook_type.value}): {e}")

    def get_current_session(self) -> Optional[Dict]:
        """
        获取当前会话数据

        Returns:
            当前会话数据
        """
        if not self.current_session_id:
            return None
        return self.current_session.copy()

    def load_session(self, session_id: str) -> Optional[Dict]:
        """
        加载历史会话

        Args:
            session_id: 会话ID

        Returns:
            会话数据
        """
        session_file = self.storage_dir / f"{session_id}.json"
        if not session_file.exists():
            return None

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None


class SessionHookManager:
    """会话Hook管理器 - 集成claude-mem"""

    def __init__(self, capture: SessionCapture):
        """
        初始化Hook管理器

        Args:
            capture: SessionCapture实例
        """
        self.capture = capture
        self._register_default_hooks()

    def _register_default_hooks(self):
        """注册默认的Hook"""

        # session-end时自动保存到claude-mem
        def save_to_claude_mem(data: Dict):
            """保存会话到claude-mem"""
            try:
                from claude_mem_enhanced import get_claude_mem

                session_data = data.get("session_data", {})

                # 转换为claude-mem格式
                claude_mem_data = {
                    "task": {
                        "id": session_data.get("id", ""),
                        "name": session_data.get("metadata", {}).get("task_name", "未命名任务"),
                        "description": session_data.get("summary", ""),
                        "status": "completed"
                    },
                    "decisions": session_data.get("decisions", []),
                    "learnings": session_data.get("learnings", []),
                    "errors": session_data.get("errors", [])
                }

                # 存储到claude-mem
                cm = get_claude_mem()
                cm.store_session(claude_mem_data, auto_compress=True)

                print("✓ 会话已自动保存到claude-mem")

            except Exception as e:
                print(f"警告: 保存到claude-mem失败: {e}")

        self.capture.register_hook(HookType.SESSION_END, save_to_claude_mem)

        # user-prompt-submit时记录日志
        def log_user_prompt(data: Dict):
            """记录用户提示"""
            prompt = data.get("prompt", "")
            print(f"📝 用户提示已捕获: {prompt[:50]}..." if len(prompt) > 50 else f"📝 用户提示已捕获: {prompt}")

        self.capture.register_hook(HookType.USER_PROMPT_SUBMIT, log_user_prompt)

        # tool-call时记录
        def log_tool_call(data: Dict):
            """记录工具调用"""
            tool = data.get("tool", "")
            print(f"🔧 工具调用已捕获: {tool}")

        self.capture.register_hook(HookType.TOOL_CALL, log_tool_call)


# 全局实例
_session_capture = None


def get_session_capture() -> SessionCapture:
    """获取全局SessionCapture实例"""
    global _session_capture
    if _session_capture is None:
        _session_capture = SessionCapture()
        # 自动启动Hook管理器
        SessionHookManager(_session_capture)
    return _session_capture


if __name__ == "__main__":
    # 测试
    print("=== 会话捕获Hook系统测试 ===\n")

    capture = SessionCapture()
    hook_manager = SessionHookManager(capture)

    # 测试完整会话流程
    print("1. 开始会话:")
    capture.start_session({"task_name": "测试用户登录功能"})

    print("\n2. 捕获用户提示:")
    capture.capture_user_prompt("请实现JWT用户登录")

    print("\n3. 捕获工具调用:")
    capture.capture_tool_call("code_generator", {"language": "python"}, "生成的代码...")

    print("\n4. 捕获助手响应:")
    capture.capture_assistant_response("已生成登录代码")

    print("\n5. 捕获决策:")
    capture.capture_decision({
        "description": "选择JWT认证",
        "alternatives": ["JWT", "Session"],
        "rationale": "无状态更适合分布式"
    })

    print("\n6. 捕获学习:")
    capture.capture_learning({
        "observation": "JWT过期时间24小时最佳",
        "situation": "用户登录",
        "outcome": "用户体验良好"
    })

    print("\n7. 捕获错误:")
    capture.capture_error({
        "error": "Token验证失败",
        "solution": "检查密钥配置",
        "type": "authentication"
    })

    print("\n8. 结束会话:")
    session_data = capture.end_session("完成JWT用户登录功能实现")

    print("\n9. 会话统计:")
    print(f"  交互数: {len(session_data['interactions'])}")
    print(f"  工具调用: {len(session_data['tool_calls'])}")
    print(f"  决策数: {len(session_data['decisions'])}")
    print(f"  学习数: {len(session_data['learnings'])}")
    print(f"  错误数: {len(session_data['errors'])}")

    print("\n✓ 测试完成")
