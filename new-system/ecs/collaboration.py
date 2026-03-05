"""
ECS - 协作引擎
实现SPAR循环（感知-讨论-行动-反思）
"""

import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import logging

from .core.agent import ECSAgent, EnvironmentContext
from .core.viewpoint import Viewpoint, ViewpointSpace, DiscussionHistory, Message, MessageType, create_viewpoint, create_message
from .emergence import EmergenceDetector, EmergenceReport
from .roles import recommend_roles_for_task


# ============================================================
# 配置数据类
# ============================================================

@dataclass
class CollaborationConfig:
    """协作配置"""
    # Agent配置
    agent_count: int = 5
    agent_selection_strategy: str = "auto"  # auto/diverse/random/custom
    custom_roles: Optional[List[str]] = None

    # SPAR循环配置
    enable_sense_phase: bool = True
    enable_discuss_phase: bool = True
    enable_act_phase: bool = True
    enable_reflect_phase: bool = True

    # 感知阶段配置
    sense_tools: List[Dict] = field(default_factory=list)

    # 讨论阶段配置
    max_rounds: int = 3
    consensus_threshold: float = 0.7
    early_stop: bool = True
    discussion_mode: str = "broadcast"  # broadcast/p2p/hybrid
    temperature_discuss: float = 0.8

    # 行动阶段配置
    temperature_act: float = 0.2
    output_format: str = "structured"  # structured/narrative/both

    # 反思阶段配置
    enable_reflection: bool = True

    # 涌现检测配置
    emergence_threshold: float = 0.7

    # 迹发沟通配置
    stigmergy_enabled: bool = True
    environment_context_size: int = 100  # 环境上下文保留条目数

    # 温度动态调整
    temperature_dynamic: bool = True

    # 安全配置
    max_iterations: int = 30
    max_cost: float = 5.0


@dataclass
class CollaborationResult:
    """协作结果"""
    task: str
    solution: str
    emergence_report: EmergenceReport
    discussion_history: DiscussionHistory
    environment_context: EnvironmentContext
    rounds_completed: int
    total_time: float
    agent_outputs: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "task": self.task,
            "solution": self.solution,
            "emergence_report": self.emergence_report.to_dict(),
            "discussion_history": self.discussion_history.to_dict(),
            "environment_context": self.environment_context.to_dict(),
            "rounds_completed": self.rounds_completed,
            "total_time": self.total_time,
            "agent_outputs": self.agent_outputs,
            "metadata": self.metadata
        }


# ============================================================
# 协作引擎
# ============================================================

class CollaborationEngine:
    """
    协作引擎

    实现SPAR循环：
    - Sense（感知）：获取任务信息，更新环境上下文
    - Discuss（讨论）：多轮无领导小组讨论
    - Act（行动）：基于共识产生具体输出
    - Reflect（反思）：评估协作过程和结果
    """

    def __init__(
        self,
        config: CollaborationConfig,
        api_key: str,
        llm_provider: str = "anthropic",
        model: str = "claude-sonnet-4-20250514"
    ):
        self.config = config
        self.api_key = api_key
        self.llm_provider = llm_provider
        self.model = model

        # 创建Agent
        self.agents: List[ECSAgent] = []

        # 协作状态
        self.environment_context = EnvironmentContext()
        self.discussion_history = DiscussionHistory()
        self.viewpoint_space = ViewpointSpace()

        # 涌现检测器
        self.emergence_detector = EmergenceDetector(
            emergence_threshold=config.emergence_threshold
        )

        # 日志
        self.logger = logging.getLogger(__name__)

    # ========================================================
    # 主协作流程
    # ========================================================

    async def collaborate(self, task: str, roles: List[str] = None) -> CollaborationResult:
        """
        执行协作

        Args:
            task: 任务描述
            roles: 角色列表（可选，如果不提供则自动推荐）

        Returns:
            协作结果
        """
        start_time = datetime.now()

        # 1. 初始化Agent
        if roles is None:
            roles = recommend_roles_for_task(
                task,
                num_agents=self.config.agent_count
            )
        self._initialize_agents(roles)

        self.logger.info(f"开始协作任务: {task}")
        self.logger.info(f"Agent角色: {roles}")

        # 记录初始观点（用于计算新颖度）
        initial_viewpoints = []

        # ====================================================
        # SPAR循环 - Sense阶段
        # ====================================================
        if self.config.enable_sense_phase:
            self.logger.info("=== Sense阶段 ===")
            await self._sense_phase(task)
            initial_viewpoints = [vp.content for vp in self.viewpoint_space.get_all_viewpoints()]

        # ====================================================
        # SPAR循环 - Discuss阶段
        # ====================================================
        if self.config.enable_discuss_phase:
            self.logger.info("=== Discuss阶段 ===")
            await self._discuss_phase(task)

        # ====================================================
        # 涌现检测
        # ====================================================
        emergence_report = self.emergence_detector.detect(
            self.viewpoint_space,
            initial_viewpoints=initial_viewpoints
        )

        self.logger.info(f"涌现强度: {emergence_report.metrics.emergence_score:.2f}")
        self.logger.info(f"涌现类型: {emergence_report.emergence_type.value}")

        # ====================================================
        # SPAR循环 - Act阶段
        # ====================================================
        if self.config.enable_act_phase:
            self.logger.info("=== Act阶段 ===")
            solution = await self._act_phase(task, emergence_report)
        else:
            solution = self._generate_solution_from_discussion(task)

        # ====================================================
        # SPAR循环 - Reflect阶段
        # ====================================================
        if self.config.enable_reflect_phase:
            self.logger.info("=== Reflect阶段 ===")
            await self._reflect_phase(task, solution, emergence_report)

        # ====================================================
        # 生成结果
        # ====================================================
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        result = CollaborationResult(
            task=task,
            solution=solution,
            emergence_report=emergence_report,
            discussion_history=self.discussion_history,
            environment_context=self.environment_context,
            rounds_completed=self.config.max_rounds,
            total_time=total_time,
            metadata={
                "agents": [agent.agent_id for agent in self.agents],
                "roles": roles,
                "config": {
                    "max_rounds": self.config.max_rounds,
                    "consensus_threshold": self.config.consensus_threshold,
                    "emergence_threshold": self.config.emergence_threshold
                }
            }
        )

        self.logger.info(f"协作完成，耗时: {total_time:.1f}秒")

        return result

    # ========================================================
    # Agent初始化
    # ========================================================

    def _initialize_agents(self, roles: List[str]):
        """初始化Agent"""
        self.agents = []
        for i, role in enumerate(roles):
            agent_id = f"{role}_{i+1}"
            agent = ECSAgent(
                agent_id=agent_id,
                role=role,
                api_key=self.api_key,
                llm_provider=self.llm_provider,
                model=self.model,
                enable_tom=True,
                enable_stigmergy=self.config.stigmergy_enabled
            )
            self.agents.append(agent)

    # ========================================================
    # SPAR循环 - Sense阶段实现
    # ========================================================

    async def _sense_phase(self, task: str):
        """Sense阶段：所有Agent感知任务（并行执行）"""
        # ========== 创建所有Agent的sense任务 ==========
        tasks = [
            agent.sense(
                task=task,
                env_context=self.environment_context,
                available_tools=self.config.sense_tools
            )
            for agent in self.agents
        ]

        # ========== 使用asyncio.gather并行执行 ==========
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # ========== 处理所有响应 ==========
        sense_results = []
        for agent, response in zip(self.agents, responses):
            # 检查是否有异常
            if isinstance(response, Exception):
                self.logger.error(f"Agent {agent.agent_id} 感知失败: {response}")
                # 创建失败记录
                error_message = create_message(
                    agent_id=agent.agent_id,
                    content=f"[感知失败] {str(response)}",
                    message_type=MessageType.SENSE,
                    round_num=0
                )
                self.discussion_history.add_message(error_message)
                continue

            # 正常响应处理
            try:
                # 创建观点
                initial_idea = response.get("initial_ideas", ["无初步想法"])
                content = initial_idea[0] if initial_idea else "无初步想法"

                viewpoint = create_viewpoint(
                    agent_id=agent.agent_id,
                    content=content,
                    confidence=0.5,
                    phase="sense"
                )
                self.viewpoint_space.add_viewpoint(viewpoint)

                # 创建消息
                message = create_message(
                    agent_id=agent.agent_id,
                    content=f"感知结果：{response}",
                    message_type=MessageType.SENSE,
                    round_num=0
                )
                self.discussion_history.add_message(message)

                sense_results.append(response)

                self.logger.debug(f"Agent {agent.agent_id} Sense阶段完成")

            except Exception as e:
                self.logger.error(f"处理Agent {agent.agent_id}感知结果时出错: {e}")

    # ========================================================
    # SPAR循环 - Discuss阶段实现
    # ========================================================

    async def _discuss_phase(self, task: str):
        """Discuss阶段：多轮讨论（并行执行）"""
        for round_num in range(1, self.config.max_rounds + 1):
            self.logger.info(f"--- 第{round_num}轮讨论 ---")

            # 获取之前的消息
            previous_messages = self.discussion_history.get_recent(limit=20)

            # 动态温度调整
            temperature = self._get_discuss_temperature(round_num)

            # ========== 并行执行所有Agent ==========
            # 创建所有Agent的讨论任务
            tasks = [
                agent.discuss(
                    task=task,
                    env_context=self.environment_context,
                    peer_messages=previous_messages,
                    round_num=round_num,
                    temperature=temperature
                )
                for agent in self.agents
            ]

            # 使用asyncio.gather并行执行
            # return_exceptions=True 确保单个Agent失败不影响其他Agent
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            # ========== 处理所有响应 ==========
            for agent, response in zip(self.agents, responses):
                # 检查是否有异常
                if isinstance(response, Exception):
                    self.logger.error(f"Agent {agent.agent_id} 发言失败: {response}")
                    # 创建失败记录
                    error_message = create_message(
                        agent_id=agent.agent_id,
                        content=f"[执行失败] {str(response)}",
                        message_type=MessageType.DISCUSS,
                        round_num=round_num
                    )
                    self.discussion_history.add_message(error_message)
                    continue

                # 正常响应处理
                try:
                    # 创建观点
                    viewpoint = create_viewpoint(
                        agent_id=agent.agent_id,
                        content=response,
                        confidence=0.6,
                        phase=f"discuss_r{round_num}"
                    )
                    self.viewpoint_space.add_viewpoint(viewpoint)

                    # 创建消息
                    message = create_message(
                        agent_id=agent.agent_id,
                        content=response,
                        message_type=MessageType.DISCUSS,
                        round_num=round_num
                    )
                    self.discussion_history.add_message(message)

                    self.logger.debug(f"Agent {agent.agent_id} 第{round_num}轮发言完成")

                except Exception as e:
                    self.logger.error(f"处理Agent {agent.agent_id}响应时出错: {e}")

            # ========== 检查共识 ==========
            if self.config.early_stop:
                consensus = self.viewpoint_space.get_consensus()
                self.logger.info(f"当前共识度: {consensus:.2f}")

                if consensus >= self.config.consensus_threshold:
                    self.logger.info(f"达成共识({consensus:.2f} >= {self.config.consensus_threshold})，提前结束讨论")
                    break

    def _get_discuss_temperature(self, round_num: int) -> float:
        """获取讨论阶段的温度（动态调整）"""
        if not self.config.temperature_dynamic:
            return self.config.temperature_discuss

        # 第一轮：高温激发创意
        if round_num == 1:
            return 0.9
        # 后续轮次：逐渐降温，收敛观点
        else:
            decay = 0.1 * (round_num - 1)
            return max(0.5, self.config.temperature_discuss - decay)

    # ========================================================
    # SPAR循环 - Act阶段实现
    # ========================================================

    async def _act_phase(self, task: str, emergence_report: EmergenceReport) -> str:
        """Act阶段：产生具体输出"""
        # 生成共识摘要
        consensus_summary = self._generate_consensus_summary(emergence_report)

        # 每个Agent产出成果
        agent_outputs = {}
        all_outputs = []

        for agent in self.agents:
            try:
                result = await agent.act(
                    task=task,
                    env_context=self.environment_context,
                    consensus_summary=consensus_summary,
                    temperature=self.config.temperature_act
                )

                agent_outputs[agent.agent_id] = result
                all_outputs.append(f"## {agent.role_info['role_name']}\n\n{result.get('content', result)}")

            except Exception as e:
                self.logger.error(f"Agent {agent.agent_id} 行动失败: {e}")

        # 整合所有输出
        solution = self._format_solution(task, all_outputs, emergence_report)

        return solution

    def _generate_consensus_summary(self, emergence_report: EmergenceReport) -> str:
        """生成共识摘要"""
        viewpoints = self.viewpoint_space.get_all_viewpoints()

        summary_parts = [
            "# 团队共识摘要",
            "",
            f"## 涌现分析",
            f"- 涌现类型: {emergence_report.emergence_type.value}",
            f"- 系统阶段: {emergence_report.system_phase.value}",
            f"- 涌现强度: {emergence_report.metrics.emergence_score:.2f}",
            "",
            "## 核心观点"
        ]

        for vp in viewpoints[-5:]:  # 最近5个观点
            summary_parts.append(f"- **{vp.agent_id}**: {vp.content[:200]}...")

        if emergence_report.insights:
            summary_parts.append("")
            summary_parts.append("## 关键洞察")
            for insight in emergence_report.insights:
                summary_parts.append(f"- {insight}")

        return "\n".join(summary_parts)

    def _format_solution(self, task: str, outputs: List[str], emergence_report: EmergenceReport) -> str:
        """格式化最终解决方案"""
        parts = [
            "# 多Agent协作解决方案",
            "",
            f"## 任务",
            task,
            "",
            f"## 协作概况",
            f"- 涌现强度: {emergence_report.metrics.emergence_score:.2f}",
            f"- 涌现类型: {emergence_report.emergence_type.value}",
            f"- 系统阶段: {emergence_report.system_phase.value}",
            "",
            "## 团队输出",
            "",
            "\n\n".join(outputs),
            "",
            "## 涌现洞察"
        ]

        for insight in emergence_report.insights:
            parts.append(f"- {insight}")

        if emergence_report.recommendations:
            parts.append("")
            parts.append("## 建议")
            for rec in emergence_report.recommendations:
                parts.append(f"- {rec}")

        return "\n".join(parts)

    def _generate_solution_from_discussion(self, task: str) -> str:
        """从讨论历史生成解决方案（不执行Act阶段时）"""
        messages = self.discussion_history.get_recent(limit=20)

        parts = [
            "# 多Agent协作讨论结果",
            "",
            f"## 任务",
            task,
            "",
            "## 讨论摘要",
            ""
        ]

        for msg in messages:
            if msg.message_type in [MessageType.SENSE, MessageType.DISCUSS]:
                parts.append(f"### {msg.agent_id}")
                parts.append(msg.content)
                parts.append("")

        return "\n".join(parts)

    # ========================================================
    # SPAR循环 - Reflect阶段实现
    # ========================================================

    async def _reflect_phase(
        self,
        task: str,
        solution: str,
        emergence_report: EmergenceReport
    ):
        """Reflect阶段：反思和评估"""
        # 选择一个Agent进行反思（通常是Skeptic或Tester）
        reflect_agent = next(
            (a for a in self.agents if a.role in ["skeptic", "tester", "architect"]),
            self.agents[0]
        )

        try:
            reflection = await reflect_agent.reflect(
                task=task,
                discussion_history=[m.to_dict() for m in self.discussion_history.messages],
                final_output=solution,
                emergence_metrics=emergence_report.metrics.to_dict()
            )

            # 创建反思消息
            message = create_message(
                agent_id=reflect_agent.agent_id,
                content=reflection,
                message_type=MessageType.REFLECT,
                round_num=0
            )
            self.discussion_history.add_message(message)

            self.logger.info(f"反思完成: {reflection[:200]}...")

        except Exception as e:
            self.logger.error(f"反思失败: {e}")


# ============================================================
# 工厂函数
# ============================================================

def create_collaboration_engine(
    config: CollaborationConfig,
    api_key: str,
    llm_provider: str = "anthropic",
    model: str = "claude-sonnet-4-20250514"
) -> CollaborationEngine:
    """创建协作引擎"""
    return CollaborationEngine(
        config=config,
        api_key=api_key,
        llm_provider=llm_provider,
        model=model
    )


# 导出
__all__ = [
    "CollaborationConfig",
    "CollaborationResult",
    "CollaborationEngine",
    "create_collaboration_engine"
]
