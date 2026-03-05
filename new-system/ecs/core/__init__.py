"""
ECS Core Module
"""

from .agent import ECSAgent, Personality, TheoryOfMind, EnvironmentContext
from .viewpoint import (
    Viewpoint,
    Message,
    ViewpointSpace,
    DiscussionHistory,
    EmergenceType,
    SystemPhase,
    MessageType,
    create_viewpoint,
    create_message,
    calculate_text_similarity
)

__all__ = [
    "ECSAgent",
    "Personality",
    "TheoryOfMind",
    "EnvironmentContext",
    "Viewpoint",
    "Message",
    "ViewpointSpace",
    "DiscussionHistory",
    "EmergenceType",
    "SystemPhase",
    "MessageType",
    "create_viewpoint",
    "create_message",
    "calculate_text_similarity"
]
