"""
记忆系统基础接口
定义所有记忆类型的抽象基类、数据结构和配置
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from datetime import datetime
from enum import Enum


class MemoryType(Enum):
    """记忆类型枚举"""
    WORKING = "working"      # 工作记忆
    EPISODIC = "episodic"    # 情景记忆
    SEMANTIC = "semantic"    # 语义记忆


@dataclass
class MemoryEntry:
    """
    记忆条目 - 通用数据结构

    所有记忆类型使用统一的数据格式，确保跨层记忆流动时的一致性。
    包含时间戳、类型、内容和元数据。
    """
    id: str
    timestamp: str
    content: Dict[str, Any]
    memory_type: MemoryType
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None  # 向量嵌入（阶段三启用）

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "metadata": self.metadata,
            "embedding": self.embedding
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntry":
        """从字典创建实例"""
        return cls(
            id=data["id"],
            timestamp=data["timestamp"],
            content=data["content"],
            memory_type=MemoryType(data.get("memory_type", "working")),
            metadata=data.get("metadata", {}),
            embedding=data.get("embedding")
        )


@dataclass
class MemoryQuery:
    """
    记忆查询 - 统一查询接口

    支持多种查询模式：
    - by_id: 按ID查询
    - by_type: 按类型查询
    - by_content: 按内容关键词查询
    - by_time_range: 按时间范围查询
    - by_similarity: 按相似度查询（阶段三启用向量检索）
    """
    query_type: str  # 查询类型
    filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 10
    offset: int = 0
    sort_by: Optional[str] = None  # 排序字段: "timestamp", "relevance"
    sort_desc: bool = True


@dataclass
class MemoryConfig:
    """
    记忆系统配置

    集中管理所有记忆层的配置参数。
    支持JSON序列化，便于配置持久化。
    """
    # 工作记忆配置
    working_max_items: int = 100
    working_session_ttl: int = 3600  # 会话过期时间（秒）

    # 情景记忆配置
    episodic_storage_path: str = "./data/episodic"
    episodic_max_episodes: int = 1000
    episodic_retention_days: int = 30  # 保留天数

    # 语义记忆配置
    semantic_storage_path: str = "./data/semantic"
    semantic_min_usage_count: int = 3  # 最小使用次数才保留模式

    # 记忆流动配置
    consolidation_threshold: float = 0.7  # 工作记忆→情景记忆阈值（涌现分数）
    abstraction_threshold: float = 0.8    # 情景记忆→语义记忆阈值（涌现分数）
    consolidation_interval: int = 300     # 巩固间隔（秒）

    # 向量数据库配置（阶段三启用）
    use_vector_db: bool = False
    vector_db_path: str = "./data/vectors"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dim: int = 384

    def get_episodic_path(self) -> Path:
        """获取情景记忆存储路径"""
        path = Path(self.episodic_storage_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_semantic_path(self) -> Path:
        """获取语义记忆存储路径"""
        path = Path(self.semantic_storage_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_vector_db_path(self) -> Path:
        """获取向量数据库路径"""
        path = Path(self.vector_db_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（支持JSON序列化）"""
        return {
            "working_max_items": self.working_max_items,
            "working_session_ttl": self.working_session_ttl,
            "episodic_storage_path": self.episodic_storage_path,
            "episodic_max_episodes": self.episodic_max_episodes,
            "episodic_retention_days": self.episodic_retention_days,
            "semantic_storage_path": self.semantic_storage_path,
            "semantic_min_usage_count": self.semantic_min_usage_count,
            "consolidation_threshold": self.consolidation_threshold,
            "abstraction_threshold": self.abstraction_threshold,
            "consolidation_interval": self.consolidation_interval,
            "use_vector_db": self.use_vector_db,
            "vector_db_path": self.vector_db_path,
            "embedding_model": self.embedding_model,
            "embedding_dim": self.embedding_dim,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryConfig":
        """从字典创建实例"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class BaseMemory(ABC):
    """
    记忆基类 - 所有记忆类型的抽象接口

    定义统一的数据操作接口，确保所有记忆层实现一致的行为。
    子类必须实现所有抽象方法。
    """

    def __init__(self, config: Optional[MemoryConfig] = None, memory_type: MemoryType = MemoryType.WORKING):
        """
        初始化记忆基类

        Args:
            config: 记忆配置
            memory_type: 记忆类型
        """
        self.config = config or MemoryConfig()
        self.memory_type = memory_type
        self._created_at = datetime.now().isoformat()

    @abstractmethod
    def save(self, data: Union[Dict[str, Any], MemoryEntry]) -> bool:
        """
        保存数据到记忆

        Args:
            data: 要保存的数据，可以是字典或MemoryEntry实例

        Returns:
            bool: 保存是否成功
        """
        pass

    @abstractmethod
    def load(self, query: Union[Dict[str, Any], MemoryQuery]) -> List[Dict[str, Any]]:
        """
        从记忆加载数据

        Args:
            query: 查询条件，可以是字典或MemoryQuery实例

        Returns:
            List[Dict]: 查询结果列表
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """清空记忆"""
        pass

    @abstractmethod
    def count(self) -> int:
        """
        返回记忆项数量

        Returns:
            int: 记忆项总数
        """
        pass

    # ==================== 辅助方法 ====================

    def _generate_id(self) -> str:
        """生成唯一ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        memory_prefix = self.memory_type.value[0]  # w/e/s
        return f"{memory_prefix}_{timestamp}"

    def _now(self) -> str:
        """获取当前时间戳"""
        return datetime.now().isoformat()

    def _to_entry(self, data: Dict[str, Any]) -> MemoryEntry:
        """将字典转换为MemoryEntry"""
        if isinstance(data, MemoryEntry):
            return data

        return MemoryEntry(
            id=data.get("id", self._generate_id()),
            timestamp=data.get("timestamp", self._now()),
            content=data.get("content", data),
            memory_type=self.memory_type,
            metadata=data.get("metadata", {}),
            embedding=data.get("embedding")
        )
