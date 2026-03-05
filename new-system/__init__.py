"""
ECS - EmergentCollaboration System
多Agent无领导小组讨论真涌现系统

版本: 2.0 Enhanced
"""

from ecs import (
    # 主类
    ECSCoordinator,
    ECSQueryBuilder,

    # 配置
    ECSConfig,
    load_config,

    # 协作相关
    CollaborationResult,
    CollaborationConfig,

    # 角色相关
    ROLE_DEFINITIONS,
    ROLE_COMBINATIONS,

    # 涌现相关
    EmergenceType,
    SystemPhase,

    # 便捷函数
    easy_collaborate,
    quick,

    # 版本信息
    __version__
)

__all__ = [
    "ECSCoordinator",
    "ECSQueryBuilder",
    "ECSConfig",
    "load_config",
    "CollaborationResult",
    "CollaborationConfig",
    "ROLE_DEFINITIONS",
    "ROLE_COMBINATIONS",
    "EmergenceType",
    "SystemPhase",
    "easy_collaborate",
    "quick",
    "__version__"
]
