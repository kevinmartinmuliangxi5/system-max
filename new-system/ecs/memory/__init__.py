"""
ECS 记忆系统 - 三层认知架构

This module implements a hierarchical memory system inspired by human cognition:
- Working Memory: Temporary session storage (short-term, fast access)
- Episodic Memory: Historical collaboration records (mid-term, temporal)
- Semantic Memory: Abstracted success patterns (long-term, knowledge)

Architecture:
    Working Memory (Session)
         ↓ (consolidation)
    Episodic Memory (History)
         ↓ (abstraction)
    Semantic Memory (Patterns)
"""

from .base import BaseMemory, MemoryEntry, MemoryQuery, MemoryConfig
from .working import WorkingMemory
from .episodic import EpisodicMemory
from .semantic import SemanticMemory
from .manager import MemoryManager, MemoryFlow

__all__ = [
    # 基础接口
    "BaseMemory",
    "MemoryEntry",
    "MemoryQuery",
    "MemoryConfig",

    # 三层记忆
    "WorkingMemory",
    "EpisodicMemory",
    "SemanticMemory",

    # 管理器
    "MemoryManager",
    "MemoryFlow",
]
