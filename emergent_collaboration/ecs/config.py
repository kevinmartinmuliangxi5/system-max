"""
ECS - 配置模块

系统配置管理
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path
import yaml
import json


@dataclass
class LLMConfig:
    """LLM配置"""
    provider: str = "anthropic"        # anthropic, openai
    model: str = "claude-sonnet-4-20250514"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000

    # Anthropic特定配置
    anthropic_api_key: Optional[str] = None
    anthropic_version: str = "2023-06-01"

    # OpenAI特定配置
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None

    def __post_init__(self):
        """从环境变量加载API密钥"""
        if not self.anthropic_api_key:
            self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # 根据provider设置默认值
        if self.provider == "anthropic" and not self.api_key:
            self.api_key = self.anthropic_api_key
        elif self.provider == "openai" and not self.api_key:
            self.api_key = self.openai_api_key

    def validate(self) -> bool:
        """验证配置"""
        if self.provider == "anthropic":
            return bool(self.api_key or self.anthropic_api_key)
        elif self.provider == "openai":
            return bool(self.api_key or self.openai_api_key)
        return False

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'provider': self.provider,
            'model': self.model,
            'api_key': self.api_key,  # 不输出敏感信息
            'base_url': self.base_url,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }


@dataclass
class EmergenceConfig:
    """涌现检测配置"""
    # 阈值
    diversity_threshold: float = 0.5        # 多样性阈值
    consensus_threshold: float = 0.7       # 共识阈值
    novelty_threshold: float = 0.6         # 新颖度阈值
    emergence_threshold: float = 0.7       # 涌现阈值

    # 权重
    diversity_weight: float = 0.3          # 多样性权重
    consensus_weight: float = 0.3          # 共识权重
    novelty_weight: float = 0.4            # 新颖度权重

    # 高级选项
    enable_phase_detection: bool = True    # 启用阶段检测
    enable_network_analysis: bool = True   # 启用网络分析
    enable_synergy_detection: bool = True  # 启用协同检测

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'diversity_threshold': self.diversity_threshold,
            'consensus_threshold': self.consensus_threshold,
            'novelty_threshold': self.novelty_threshold,
            'emergence_threshold': self.emergence_threshold,
            'diversity_weight': self.diversity_weight,
            'consensus_weight': self.consensus_weight,
            'novelty_weight': self.novelty_weight,
            'enable_phase_detection': self.enable_phase_detection,
            'enable_network_analysis': self.enable_network_analysis,
            'enable_synergy_detection': self.enable_synergy_detection
        }


@dataclass
class AgentConfig:
    """Agent配置"""
    count: int = 5                        # Agent数量
    selection_strategy: str = "auto"      # auto, diverse, random, custom

    # 自定义Agent列表（当selection_strategy=custom时使用）
    custom_roles: List[str] = field(default_factory=list)
    custom_agents: List[Dict] = field(default_factory=list)

    # Agent属性
    enable_personality: bool = True       # 启用性格差异
    enable_theory_of_mind: bool = True     # 启用心智建模
    enable_learning: bool = False          # 启用学习能力

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'count': self.count,
            'selection_strategy': self.selection_strategy,
            'custom_roles': self.custom_roles,
            'custom_agents': self.custom_agents,
            'enable_personality': self.enable_personality,
            'enable_theory_of_mind': self.enable_theory_of_mind,
            'enable_learning': self.enable_learning
        }


@dataclass
class CollaborationConfig:
    """协作流程配置"""
    max_rounds: int = 3                    # 最大轮数
    convergence_threshold: float = 0.7     # 收敛阈值
    early_stop: bool = True                # 启用早停
    timeout_per_round: int = 300           # 每轮超时（秒）

    # 讨论模式
    discussion_mode: str = "broadcast"     # broadcast, p2p, hybrid
    enable_parallel: bool = True           # 启用并行处理
    batch_size: int = 3                    # 批处理大小

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'max_rounds': self.max_rounds,
            'convergence_threshold': self.convergence_threshold,
            'early_stop': self.early_stop,
            'timeout_per_round': self.timeout_per_round,
            'discussion_mode': self.discussion_mode,
            'enable_parallel': self.enable_parallel,
            'batch_size': self.batch_size
        }


@dataclass
class OutputConfig:
    """输出配置"""
    format: str = "structured"             # structured, narrative, both
    include_process: bool = True          # 包含过程记录
    include_metrics: bool = True          # 包含指标数据
    include_agent_details: bool = False   # 包含Agent详情

    # 导出选项
    export_format: str = "json"            # json, markdown, html
    output_dir: str = "output"             # 输出目录
    auto_save: bool = True                 # 自动保存

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'format': self.format,
            'include_process': self.include_process,
            'include_metrics': self.include_metrics,
            'include_agent_details': self.include_agent_details,
            'export_format': self.export_format,
            'output_dir': self.output_dir,
            'auto_save': self.auto_save
        }


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"                    # DEBUG, INFO, WARNING, ERROR
    file: str = "ecs.log"                 # 日志文件
    console: bool = True                   # 控制台输出
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'level': self.level,
            'file': self.file,
            'console': self.console,
            'format': self.format
        }


@dataclass
class ECSConfig:
    """ECS完整配置"""
    # 子配置
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

    def __post_init__(self):
        """确保工作目录存在"""
        self.workspace = str(Path(self.workspace).resolve())

    def validate(self) -> tuple[bool, List[str]]:
        """
        验证配置

        Returns:
            (是否有效, 错误列表)
        """
        errors = []

        # 验证LLM配置
        if not self.llm.validate():
            errors.append("LLM配置无效：缺少API密钥")

        # 验证Agent数量
        if self.agents.count < 2:
            errors.append("Agent数量必须大于等于2")
        elif self.agents.count > 20:
            errors.append("Agent数量建议不超过20")

        # 验证阈值
        if not (0 <= self.emergence.emergence_threshold <= 1):
            errors.append("涌现阈值必须在0-1之间")
        if not (0 <= self.collaboration.convergence_threshold <= 1):
            errors.append("收敛阈值必须在0-1之间")

        return len(errors) == 0, errors

    @classmethod
    def from_file(cls, config_path: str) -> 'ECSConfig':
        """
        从文件加载配置

        Args:
            config_path: 配置文件路径

        Returns:
            ECSConfig对象
        """
        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        # 根据文件类型解析
        if config_file.suffix in ['.yaml', '.yml']:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        elif config_file.suffix == '.json':
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise ValueError(f"不支持的配置文件格式: {config_file.suffix}")

        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ECSConfig':
        """
        从字典创建配置

        Args:
            data: 配置字典

        Returns:
            ECSConfig对象
        """
        # 解析嵌套配置
        llm_data = data.get('llm', {})
        emergence_data = data.get('emergence', {})
        agents_data = data.get('agents', {})
        collaboration_data = data.get('collaboration', {})
        output_data = data.get('output', {})
        logging_data = data.get('logging', {})

        return cls(
            llm=LLMConfig(**llm_data),
            emergence=EmergenceConfig(**emergence_data),
            agents=AgentConfig(**agents_data),
            collaboration=CollaborationConfig(**collaboration_data),
            output=OutputConfig(**output_data),
            logging=LoggingConfig(**logging_data),
            verbose=data.get('verbose', False),
            debug=data.get('debug', False),
            workspace=data.get('workspace', 'workspace')
        )

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

    def save(self, path: str):
        """
        保存配置到文件

        Args:
            path: 保存路径
        """
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = self.to_dict()

        if output_path.suffix in ['.yaml', '.yml']:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        elif output_path.suffix == '.json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            # 默认使用JSON
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)


def load_config(config_path: Optional[str] = None) -> ECSConfig:
    """
    加载配置

    Args:
        config_path: 配置文件路径（可选）

    Returns:
        ECSConfig对象
    """
    if config_path is None:
        # 尝试查找默认配置文件
        for filename in ['config.yaml', 'config.yml', 'config.json', '.ecs.yaml']:
            config_file = Path(filename)
            if config_file.exists():
                config_path = str(config_file)
                break

    if config_path:
        return ECSConfig.from_file(config_path)
    else:
        # 返回默认配置
        return ECSConfig()


def create_default_config(output_path: str = "config.yaml"):
    """
    创建默认配置文件

    Args:
        output_path: 输出路径
    """
    default_config = ECSConfig()
    default_config.save(output_path)


__all__ = [
    'LLMConfig',
    'EmergenceConfig',
    'AgentConfig',
    'CollaborationConfig',
    'OutputConfig',
    'LoggingConfig',
    'ECSConfig',
    'load_config',
    'create_default_config',
]
