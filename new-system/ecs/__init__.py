"""
ECS - EmergentCollaboration System
多Agent无领导小组讨论真涌现系统

版本: 2.0 Enhanced
作者: ECS Team
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from .config import ECSConfig, load_config, get_api_key
from .collaboration import CollaborationEngine, CollaborationConfig, CollaborationResult
from .roles import (
    ROLE_DEFINITIONS,
    ROLE_COMBINATIONS,
    get_all_roles,
    get_role_definition,
    recommend_roles_for_task,
    list_role_combinations
)
from .core.viewpoint import EmergenceType, SystemPhase


# ============================================================
# 设置日志
# ============================================================

def setup_logging(config: ECSConfig):
    """设置日志"""
    logging.basicConfig(
        level=getattr(logging, config.logging.level),
        format=config.logging.format,
        filename=config.logging.file if config.logging.file else None,
        force=True
    )


# ============================================================
# ECSCoordinator - 主协调器
# ============================================================

class ECSCoordinator:
    """
    ECS主协调器

    管理整个多Agent协作过程的高级接口
    """

    def __init__(self, config: Optional[ECSConfig] = None):
        """
        初始化协调器

        Args:
            config: ECS配置（可选）
        """
        self.config = config or load_config()
        setup_logging(self.config)
        self.logger = logging.getLogger(__name__)

        # 获取API密钥
        try:
            self.api_key = get_api_key(self.config)
        except ValueError as e:
            self.logger.warning(str(e))
            self.api_key = None

        # 验证配置
        errors = self.config.validate()
        if errors:
            self.logger.warning(f"配置验证警告: {'; '.join(errors)}")

    # ========================================================
    # 主要协作方法
    # ========================================================

    def collaborate(
        self,
        task: str,
        agent_count: Optional[int] = None,
        max_rounds: Optional[int] = None,
        emergence_threshold: Optional[float] = None,
        roles: Optional[List[str]] = None,
        verbose: Optional[bool] = None
    ) -> CollaborationResult:
        """
        执行协作

        Args:
            task: 任务描述
            agent_count: Agent数量（覆盖配置）
            max_rounds: 最大讨论轮次（覆盖配置）
            emergence_threshold: 涌现阈值（覆盖配置）
            roles: 角色列表（可选）
            verbose: 详细输出（覆盖配置）

        Returns:
            协作结果
        """
        if not self.api_key:
            raise ValueError("未设置API密钥，无法执行协作")

        # 应用覆盖参数
        if agent_count is not None:
            self.config.agents.count = agent_count
        if max_rounds is not None:
            self.config.collaboration.max_rounds = max_rounds
        if emergence_threshold is not None:
            self.config.emergence.emergence_threshold = emergence_threshold
        if verbose is not None:
            self.config.verbose = verbose

        # 创建协作配置
        collab_config = CollaborationConfig(
            agent_count=self.config.agents.count,
            custom_roles=roles,
            max_rounds=self.config.collaboration.max_rounds,
            consensus_threshold=self.config.collaboration.consensus_threshold,
            emergence_threshold=self.config.emergence.emergence_threshold,
            stigmergy_enabled=self.config.collaboration.stigmergy_enabled,
            temperature_dynamic=self.config.collaboration.temperature_dynamic,
            temperature_discuss=self.config.collaboration.temperature_discuss,
            temperature_act=self.config.collaboration.temperature_act
        )

        # 创建协作引擎
        engine = CollaborationEngine(
            config=collab_config,
            api_key=self.api_key,
            llm_provider=self.config.llm.provider,
            model=self.config.llm.model
        )

        # 执行协作
        if self.config.verbose:
            self.logger.info(f"开始协作: {task}")

        result = asyncio.run(engine.collaborate(task, roles))

        if self.config.verbose:
            self.logger.info(f"协作完成，涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")

        # 自动保存
        if self.config.output.auto_save:
            self.export_result(result)

        return result

    async def collaborate_async(
        self,
        task: str,
        **kwargs
    ) -> CollaborationResult:
        """异步版本的协作方法"""
        # 同步版本的异步包装
        return self.collaborate(task, **kwargs)

    # ========================================================
    # 角色管理
    # ========================================================

    def get_available_roles(self) -> Dict[str, str]:
        """获取所有可用角色"""
        return get_all_roles()

    def get_role_details(self, role_id: str) -> Dict[str, Any]:
        """获取角色详情"""
        return get_role_definition(role_id)

    def recommend_roles_for_task(self, task: str, num_agents: int = 5) -> List[str]:
        """为任务推荐角色"""
        return recommend_roles_for_task(task, num_agents)

    def list_role_combinations(self) -> Dict[str, str]:
        """列出所有角色组合"""
        return list_role_combinations()

    # ========================================================
    # 导出方法
    # ========================================================

    def export_result(
        self,
        result: CollaborationResult,
        output_file: Optional[str] = None,
        format: Optional[str] = None
    ):
        """
        导出结果

        Args:
            result: 协作结果
            output_file: 输出文件路径（可选）
            format: 输出格式（json/markdown，默认为配置中的格式）
        """
        if format is None:
            format = self.config.output.export_format

        if output_file is None:
            timestamp = result.metadata.get('timestamp', 'unknown')
            output_file = f"{self.config.output.output_dir}/result_{timestamp}.{format}"

        # 确保输出目录存在
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        elif format == "markdown":
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(self._format_result_as_markdown(result))
        else:
            raise ValueError(f"不支持的输出格式: {format}")

        self.logger.info(f"结果已保存到: {output_file}")

    def _format_result_as_markdown(self, result: CollaborationResult) -> str:
        """将结果格式化为Markdown"""
        lines = [
            "# 多Agent协作结果",
            "",
            f"## 任务",
            result.task,
            "",
            f"## 涌现分析",
            f"- **涌现类型**: {result.emergence_report.emergence_type.value}",
            f"- **系统阶段**: {result.emergence_report.system_phase.value}",
            f"- **涌现强度**: {result.emergence_report.metrics.emergence_score:.2f}",
            f"- **多样性**: {result.emergence_report.metrics.diversity:.2f}",
            f"- **共识度**: {result.emergence_report.metrics.consensus:.2f}",
            f"- **新颖度**: {result.emergence_report.metrics.novelty:.2f}",
            f"- **协同度**: {result.emergence_report.metrics.synergy:.2f}",
            "",
            "## 解决方案",
            "",
            result.solution,
            "",
            "## 涌现洞察"
        ]

        for insight in result.emergence_report.insights:
            lines.append(f"- {insight}")

        if result.emergence_report.recommendations:
            lines.append("")
            lines.append("## 建议")
            for rec in result.emergence_report.recommendations:
                lines.append(f"- {rec}")

        lines.extend([
            "",
            "## 协作统计",
            f"- **完成轮次**: {result.rounds_completed}",
            f"- **耗时**: {result.total_time:.1f}秒",
            f"- **参与Agent**: {', '.join(result.metadata.get('agents', []))}"
        ])

        return "\n".join(lines)


# ============================================================
# ECSQueryBuilder - 查询构建器
# ============================================================

class ECSQueryBuilder:
    """
    流式API构建协作查询

    示例:
        result = (ECSQueryBuilder()
            .with_task("设计一个系统")
            .with_agents(5)
            .with_rounds(3)
            .execute())
    """

    def __init__(self):
        self._task: Optional[str] = None
        self._agent_count: Optional[int] = None
        self._selection_strategy: str = "auto"
        self._roles: Optional[List[str]] = None
        self._max_rounds: int = 3
        self._threshold: float = 0.7
        self._output: Optional[str] = None
        self._verbose: bool = False
        self._config: Optional[ECSConfig] = None

    def with_task(self, task: str) -> 'ECSQueryBuilder':
        """设置任务"""
        self._task = task
        return self

    def with_agents(
        self,
        count: int,
        strategy: str = "auto"
    ) -> 'ECSQueryBuilder':
        """设置Agent数量和选择策略"""
        self._agent_count = count
        self._selection_strategy = strategy
        return self

    def with_roles(self, roles: List[str]) -> 'ECSQueryBuilder':
        """设置角色列表"""
        self._roles = roles
        return self

    def with_rounds(self, rounds: int) -> 'ECSQueryBuilder':
        """设置讨论轮次"""
        self._max_rounds = rounds
        return self

    def with_threshold(self, threshold: float) -> 'ECSQueryBuilder':
        """设置涌现阈值"""
        self._threshold = threshold
        return self

    def with_output(self, output: str) -> 'ECSQueryBuilder':
        """设置输出文件"""
        self._output = output
        return self

    def verbose(self, verbose: bool = True) -> 'ECSQueryBuilder':
        """设置详细输出"""
        self._verbose = verbose
        return self

    def with_config(self, config: ECSConfig) -> 'ECSQueryBuilder':
        """设置配置"""
        self._config = config
        return self

    def with_llm(
        self,
        provider: str = "anthropic",
        model: str = "claude-sonnet-4-20250514"
    ) -> 'ECSQueryBuilder':
        """设置LLM配置"""
        if self._config is None:
            self._config = ECSConfig()
        self._config.llm.provider = provider
        self._config.llm.model = model
        return self

    def execute(self) -> CollaborationResult:
        """执行协作"""
        if not self._task:
            raise ValueError("必须设置任务（使用with_task方法）")

        # 创建或复用配置
        config = self._config or ECSConfig()
        config.verbose = self._verbose

        # 创建协调器
        coordinator = ECSCoordinator(config)

        # 执行协作
        result = coordinator.collaborate(
            task=self._task,
            agent_count=self._agent_count,
            max_rounds=self._max_rounds,
            emergence_threshold=self._threshold,
            roles=self._roles
        )

        # 保存到指定文件
        if self._output:
            coordinator.export_result(result, self._output)

        return result


# ============================================================
# 便捷函数
# ============================================================

def easy_collaborate(
    task: str,
    agents: int = 5,
    rounds: int = 3,
    threshold: float = 0.7,
    output: Optional[str] = None,
    verbose: bool = True
) -> CollaborationResult:
    """
    最简单的协作函数

    Args:
        task: 任务描述
        agents: Agent数量
        rounds: 讨论轮次
        threshold: 涌现阈值
        output: 输出文件（可选）
        verbose: 详细输出

    Returns:
        协作结果

    示例:
        result = easy_collaborate(
            task="设计一个可持续的城市自行车共享系统",
            agents=5,
            rounds=3
        )
    """
    config = ECSConfig()
    config.verbose = verbose

    coordinator = ECSCoordinator(config)
    result = coordinator.collaborate(
        task=task,
        agent_count=agents,
        max_rounds=rounds,
        emergence_threshold=threshold
    )

    if output:
        coordinator.export_result(result, output)

    return result


# 便捷别名
quick = easy_collaborate


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 主类
    "ECSCoordinator",
    "ECSQueryBuilder",

    # 配置
    "ECSConfig",
    "load_config",

    # 协作相关
    "CollaborationResult",
    "CollaborationConfig",

    # 角色相关
    "ROLE_DEFINITIONS",
    "ROLE_COMBINATIONS",

    # 涌现相关
    "EmergenceType",
    "SystemPhase",

    # 便捷函数
    "easy_collaborate",
    "quick",

    # 版本信息
    "__version__"
]

__version__ = "2.0.0"
