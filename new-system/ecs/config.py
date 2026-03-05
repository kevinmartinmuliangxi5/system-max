"""
ECS - 配置管理系统
支持YAML/JSON配置文件
"""

import os
import yaml
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
from pathlib import Path


# ============================================================
# LLM配置
# ============================================================

@dataclass
class LLMConfig:
    """LLM配置"""
    provider: str = "anthropic"  # anthropic 或 openai
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.7
    max_tokens: int = 2000
    api_key: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LLMConfig':
        """从字典创建"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


# ============================================================
# 涌现检测配置
# ============================================================

@dataclass
class EmergenceConfig:
    """涌现检测配置"""
    diversity_threshold: float = 0.5
    consensus_threshold: float = 0.7
    novelty_threshold: float = 0.6
    emergence_threshold: float = 0.7
    diversity_weight: float = 0.3
    consensus_weight: float = 0.3
    novelty_weight: float = 0.4
    enable_phase_detection: bool = True
    enable_network_analysis: bool = True
    enable_synergy_detection: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmergenceConfig':
        """从字典创建"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


# ============================================================
# Agent配置
# ============================================================

@dataclass
class AgentConfig:
    """Agent配置"""
    count: int = 5
    selection_strategy: str = "auto"  # auto/diverse/random/custom
    enable_personality: bool = True
    enable_theory_of_mind: bool = True
    enable_learning: bool = False
    custom_roles: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfig':
        """从字典创建"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


# ============================================================
# 协作配置
# ============================================================

@dataclass
class CollaborationConfig:
    """协作配置"""
    max_rounds: int = 3
    consensus_threshold: float = 0.7
    early_stop: bool = True
    timeout_per_round: int = 300
    discussion_mode: str = "broadcast"  # broadcast/p2p/hybrid
    enable_parallel: bool = True
    batch_size: int = 3

    # SPAR循环配置
    enable_sense_phase: bool = True
    enable_discuss_phase: bool = True
    enable_act_phase: bool = True
    enable_reflect_phase: bool = True

    # 迹发沟通
    stigmergy_enabled: bool = True
    environment_context_size: int = 100

    # 温度配置
    temperature_dynamic: bool = True
    temperature_discuss: float = 0.8
    temperature_act: float = 0.2

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CollaborationConfig':
        """从字典创建"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


# ============================================================
# 输出配置
# ============================================================

@dataclass
class OutputConfig:
    """输出配置"""
    format: str = "structured"  # structured/narrative/both
    include_process: bool = True
    include_metrics: bool = True
    include_agent_details: bool = False
    export_format: str = "json"  # json/markdown/html
    output_dir: str = "output"
    auto_save: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OutputConfig':
        """从字典创建"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


# ============================================================
# 日志配置
# ============================================================

@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    file: str = "ecs.log"
    console: bool = True
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LoggingConfig':
        """从字典创建"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


# ============================================================
# 主配置
# ============================================================

@dataclass
class ECSConfig:
    """ECS主配置"""
    llm: LLMConfig = field(default_factory=LLMConfig)
    emergence: EmergenceConfig = field(default_factory=EmergenceConfig)
    agents: AgentConfig = field(default_factory=AgentConfig)
    collaboration: CollaborationConfig = field(default_factory=CollaborationConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    # 全局设置
    verbose: bool = False
    debug: bool = False
    workspace: str = "workspace"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ECSConfig':
        """从字典创建"""
        config = cls()

        if 'llm' in data:
            config.llm = LLMConfig.from_dict(data['llm'])
        if 'emergence' in data:
            config.emergence = EmergenceConfig.from_dict(data['emergence'])
        if 'agents' in data:
            config.agents = AgentConfig.from_dict(data['agents'])
        if 'collaboration' in data:
            config.collaboration = CollaborationConfig.from_dict(data['collaboration'])
        if 'output' in data:
            config.output = OutputConfig.from_dict(data['output'])
        if 'logging' in data:
            config.logging = LoggingConfig.from_dict(data['logging'])

        # 全局设置
        for key in ['verbose', 'debug', 'workspace']:
            if key in data:
                setattr(config, key, data[key])

        return config

    @classmethod
    def from_yaml(cls, file_path: str) -> 'ECSConfig':
        """从YAML文件加载"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    @classmethod
    def from_json(cls, file_path: str) -> 'ECSConfig':
        """从JSON文件加载"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'llm': self.llm.to_dict(),
            'emergence': self.emergence.to_dict(),
            'agents': self.agents.to_dict(),
            'collaboration': self.collaboration.to_dict(),
            'output': self.output.to_dict(),
            'logging': self.logging.to_dict(),
            'verbose': self.verbose,
            'debug': self.debug,
            'workspace': self.workspace
        }

    def to_yaml(self, file_path: str):
        """保存为YAML文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, allow_unicode=True, default_flow_style=False)

    def to_json(self, file_path: str):
        """保存为JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def validate(self) -> List[str]:
        """验证配置，返回错误列表"""
        errors = []

        # 验证LLM配置
        if not self.llm.api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
            if not api_key:
                errors.append("未设置API密钥，请设置ANTHROPIC_API_KEY或OPENAI_API_KEY环境变量")

        # 验证Agent配置
        if self.agents.count < 2:
            errors.append("Agent数量至少为2")
        if self.agents.count > 15:
            errors.append("Agent数量建议不超过15")

        # 验证协作配置
        if self.collaboration.max_rounds < 1:
            errors.append("讨论轮次至少为1")
        if self.collaboration.max_rounds > 10:
            errors.append("讨论轮次建议不超过10")

        # 验证阈值
        if not (0 <= self.emergence.emergence_threshold <= 1):
            errors.append("涌现阈值必须在0-1之间")
        if not (0 <= self.collaboration.consensus_threshold <= 1):
            errors.append("共识阈值必须在0-1之间")

        return errors


# ============================================================
# 配置加载函数
# ============================================================

def load_config(config_path: Optional[str] = None) -> ECSConfig:
    """
    加载配置

    Args:
        config_path: 配置文件路径（可选）

    Returns:
        ECSConfig实例
    """
    # 如果指定了配置文件
    if config_path:
        path = Path(config_path)
        if path.exists():
            if path.suffix in ['.yaml', '.yml']:
                return ECSConfig.from_yaml(str(path))
            elif path.suffix == '.json':
                return ECSConfig.from_json(str(path))

    # 尝试默认配置文件
    default_paths = ['config.yaml', 'config.yml', 'config.json', '.ecs/config.yaml']
    for default_path in default_paths:
        path = Path(default_path)
        if path.exists():
            if path.suffix in ['.yaml', '.yml']:
                return ECSConfig.from_yaml(str(path))
            elif path.suffix == '.json':
                return ECSConfig.from_json(str(path))

    # 返回默认配置
    return ECSConfig()


def get_api_key(config: ECSConfig) -> str:
    """
    获取API密钥

    Args:
        config: ECS配置

    Returns:
        API密钥字符串
    """
    # 优先使用配置中的密钥
    if config.llm.api_key:
        return config.llm.api_key

    # 从环境变量获取
    if config.llm.provider == "anthropic":
        key = os.getenv("ANTHROPIC_API_KEY")
    elif config.llm.provider == "openai":
        key = os.getenv("OPENAI_API_KEY")
    else:
        key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")

    if not key:
        raise ValueError(
            "未找到API密钥。请设置以下环境变量之一：\n"
            "- ANTHROPIC_API_KEY (用于Claude)\n"
            "- OPENAI_API_KEY (用于GPT)\n"
            "或在配置文件中指定api_key"
        )

    return key


# 导出
__all__ = [
    "LLMConfig",
    "EmergenceConfig",
    "AgentConfig",
    "CollaborationConfig",
    "OutputConfig",
    "LoggingConfig",
    "ECSConfig",
    "load_config",
    "get_api_key"
]
