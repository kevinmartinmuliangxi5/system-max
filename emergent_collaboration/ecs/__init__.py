"""
ECS - EmergentCollaboration System

多Agent无领导小组讨论真涌现系统
"""

__version__ = "1.0.0"
__author__ = "ECS Team"

from . import (
    ECSCoordinator,
    ECSQueryBuilder,
    easy_collaborate,
    quick,
    collaborate_with_custom_agents
)

from .config import (
    ECSConfig,
    LLMConfig,
    EmergenceConfig,
    AgentConfig,
    load_config
)

from .agent import (
    ECSAgent,
    AgentRole,
    Personality,
    Expertise,
    ThinkingStyle,
    create_agent_from_config
)

from .emergence import (
    EmergenceDetector,
    EmergenceReport,
    EmergenceMetrics,
    EmergenceType,
    SystemPhase
)

from .collaboration import (
    CollaborationEngine,
    CollaborationConfig,
    CollaborationResult,
    create_collaboration_engine
)

from .roles import (
    get_role,
    list_roles,
    get_roles_by_ids,
    recommend_roles,
    ROLE_COMBINATIONS,
    PREDEFINED_ROLES
)

from .viewpoint import (
    Viewpoint,
    ViewpointSpace,
    Message,
    Feedback,
    Solution,
    DiscussionRound
)

__all__ = [
    # 主接口
    'ECSCoordinator',
    'ECSQueryBuilder',
    'easy_collaborate',
    'quick',
    'collaborate_with_custom_agents',

    # 配置
    'ECSConfig',
    'LLMConfig',
    'EmergenceConfig',
    'AgentConfig',
    'load_config',

    # Agent
    'ECSAgent',
    'AgentRole',
    'Personality',
    'Expertise',
    'ThinkingStyle',
    'create_agent_from_config',

    # 涌现检测
    'EmergenceDetector',
    'EmergenceReport',
    'EmergenceMetrics',
    'EmergenceType',
    'SystemPhase',

    # 协作引擎
    'CollaborationEngine',
    'CollaborationConfig',
    'CollaborationResult',
    'create_collaboration_engine',

    # 角色
    'get_role',
    'list_roles',
    'get_roles_by_ids',
    'recommend_roles',
    'ROLE_COMBINATIONS',
    'PREDEFINED_ROLES',

    # 数据结构
    'Viewpoint',
    'ViewpointSpace',
    'Message',
    'Feedback',
    'Solution',
    'DiscussionRound',
]
