"""
ECS - 包初始化模块
"""

__version__ = "1.0.0"

from .ecs import (
    ECSCoordinator,
    easy_collaborate,
    quick,
    ECSConfig,
    load_config
)

__all__ = [
    'ECSCoordinator',
    'easy_collaborate',
    'quick',
    'ECSConfig',
    'load_config',
    '__version__'
]
