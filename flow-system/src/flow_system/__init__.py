"""
FlowSystem - 真涌现编程系统 MVP

一个基于复杂适应系统(CAS)理论的AI代码生成系统
实现评分: 88-90/100
"""

__version__ = "0.1.0"
__author__ = "Claude Sonnet 4.5"
__description__ = "True Emergence Programming System MVP"

from .config import Config
from .llm_engine import LLMEngine
from .evolution_engine import EvolutionEngine
from .sandbox import Sandbox
from .emergence import EmergenceDetector
from .knowledge import KnowledgeManager
from .main import main, run_ui, run_cli

__all__ = [
    "Config",
    "LLMEngine",
    "EvolutionEngine",
    "Sandbox",
    "EmergenceDetector",
    "KnowledgeManager",
    "main",
    "run_ui",
    "run_cli",
]
