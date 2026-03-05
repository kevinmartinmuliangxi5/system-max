"""
ECS - 协作引擎模块

实现多Agent无领导小组讨论的核心协作流程
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, field
import uuid
import json
from pathlib import Path

from .agent import ECSAgent, Personality, create_agent_from_config
from .roles import get_role, get_roles_by_ids, recommend_roles
from .viewpoint import Viewpoint, ViewpointSpace, Message, MessageType, Solution, DiscussionRound
from .emergence import EmergenceDetector, EmergenceReport, EmergenceType, SystemPhase


@dataclass
class CollaborationConfig:
    """协作配置"""
    max_rounds: int = 3                  # 最大讨论轮数
    convergence_threshold: float = 0.7   # 收敛阈值
    emergence_threshold: float = 0.7     # 涌现阈值
    timeout_per_round: int = 300         # 每轮超时（秒）

    # Agent配置
    agent_count: int = 5
    role_selection: str = "auto"         # auto/diverse/random

    # LLM配置
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000

    # 输出配置
    verbose: bool = False
    save_intermediate: bool = True


@dataclass
class CollaborationResult:
    """协作结果"""
    success: bool
    solution: str                    # 最终方案
    emergence_report: EmergenceReport  # 涌现报告

    # 过程记录
    initial_viewpoints: Dict[str, str] = field(default_factory=dict)
    discussion_rounds: List[Dict] = field(default_factory=list)
    synthesis_history: List[str] = field(default_factory=list)

    # 元数据
    total_time: float = 0.0
    rounds_completed: int = 0
    total_messages: int = 0

    # 追踪信息
    agent_contributions: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'success': self.success,
            'solution': self.solution,
            'emergence_report': self.emergence_report.to_dict(),
            'initial_viewpoints': self.initial_viewpoints,
            'discussion_rounds': self.discussion_rounds,
            'synthesis_history': self.synthesis_history,
            'total_time': self.total_time,
            'rounds_completed': self.rounds_completed,
            'total_messages': self.total_messages,
            'agent_contributions': self.agent_contributions
        }


class CollaborationEngine:
    """
    协作引擎

    实现无领导小组讨论的四阶段流程：
    1. 观点发散 (Divergence)
    2. 观点碰撞 (Collision)
    3. 观点收敛 (Convergence)
    4. 迭代优化 (Refinement)
    """

    def __init__(self, config: CollaborationConfig):
        """
        初始化协作引擎

        Args:
            config: 协作配置
        """
        self.config = config

        # 初始化组件
        self.agents: Dict[str, ECSAgent] = {}
        self.viewpoint_space = ViewpointSpace()
        self.emergence_detector = EmergenceDetector(
            consensus_threshold=config.convergence_threshold,
            novelty_threshold=0.6
        )

        # 状态追踪
        self.current_round = 0
        self.is_running = False
        self.start_time = None

        # 回调函数
        self.on_round_complete: Optional[Callable] = None
        self.on_emergence_detected: Optional[Callable] = None

    def initialize_agents(self, task: str):
        """
        初始化Agent

        Args:
            task: 任务描述（用于推荐角色）
        """
        # 选择角色
        if self.config.role_selection == "auto":
            role_ids = recommend_roles(task, self.config.agent_count)
        elif self.config.role_selection == "diverse":
            # 选择多样性最大的角色组合
            role_ids = list([
                "technical_architect", "product_manager", "ux_designer",
                "creative_director", "qa_engineer", "user_researcher"
            ])[:self.config.agent_count]
        else:
            # 随机选择
            all_roles = [
                "technical_architect", "product_manager", "ux_designer",
                "ui_designer", "software_engineer", "qa_engineer",
                "data_analyst", "creative_director", "user_researcher"
            ]
            import random
            role_ids = random.sample(all_roles, self.config.agent_count)

        # 创建Agent
        for i, role_id in enumerate(role_ids):
            role = get_role(role_id)
            agent = ECSAgent(
                agent_id=f"{role_id}_{i}",
                role=role,
                personality=Personality(
                    openness=0.7 + (i % 3) * 0.1,      # 0.7-0.9
                    conscientiousness=0.6 + (i % 2) * 0.2,
                    extraversion=0.4 + (i % 4) * 0.15,
                    agreeableness=0.5 + (i % 3) * 0.15,
                    neuroticism=0.3 + (i % 5) * 0.1
                )
            )
            self.agents[agent.agent_id] = agent

        if self.config.verbose:
            print(f"初始化了 {len(self.agents)} 个Agent:")
            for agent_id, agent in self.agents.items():
                print(f"  - {agent_id}: {agent.role.name}")

    async def collaborate(self, task: str) -> CollaborationResult:
        """
        执行完整的协作流程

        Args:
            task: 任务描述

        Returns:
            协作结果
        """
        self.start_time = datetime.now()
        self.is_running = True

        try:
            # === 阶段1: 观点发散 ===
            if self.config.verbose:
                print("\n=== 阶段1: 观点发散 ===")

            initial_viewpoints = await self._stage1_divergence(task)

            # === 阶段2: 观点碰撞 ===
            if self.config.verbose:
                print("\n=== 阶段2: 观点碰撞 ===")

            discussion_rounds = await self._stage2_collision(task, initial_viewpoints)

            # === 阶段3: 观点收敛 ===
            if self.config.verbose:
                print("\n=== 阶段3: 观点收敛 ===")

            synthesis = await self._stage3_convergence(initial_viewpoints, discussion_rounds)

            # === 阶段4: 迭代优化 ===
            if self.config.verbose:
                print("\n=== 阶段4: 迭代优化 ===")

            final_solution, emergence_report = await self._stage4_refinement(
                task, synthesis, discussion_rounds
            )

            # 创建结果
            total_time = (datetime.now() - self.start_time).total_seconds()

            result = CollaborationResult(
                success=True,
                solution=final_solution,
                emergence_report=emergence_report,
                initial_viewpoints={aid: vp.content for aid, vp in initial_viewpoints.items()},
                discussion_rounds=discussion_rounds,
                synthesis_history=synthesis,
                total_time=total_time,
                rounds_completed=self.current_round,
                total_messages=len(self.viewpoint_space.message_history),
                agent_contributions=self._get_agent_contributions()
            )

            return result

        except Exception as e:
            if self.config.verbose:
                print(f"\n❌ 协作过程出错: {e}")

            # 返回失败结果
            return CollaborationResult(
                success=False,
                solution="",
                emergence_report=self.emergence_detector.history[-1] if self.emergence_detector.history else None,
                total_time=(datetime.now() - self.start_time).total_seconds()
            )

        finally:
            self.is_running = False

    async def _stage1_divergence(self, task: str) -> Dict[str, Viewpoint]:
        """
        阶段1: 观点发散

        所有Agent独立分析任务，生成初始观点
        """
        # 并发调用所有Agent
        tasks = [
            agent.analyze(task)
            for agent in self.agents.values()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 创建观点对象
        viewpoints = {}
        for (agent_id, agent), result in zip(self.agents.items(), results):
            if isinstance(result, Exception):
                if self.config.verbose:
                    print(f"  ⚠️ {agent_id} 分析失败: {result}")
                continue

            viewpoint = Viewpoint(
                agent_id=agent_id,
                content=result,
                confidence=0.7 + (hash(agent_id) % 10) / 30  # 0.7-1.0
            )
            viewpoints[agent_id] = viewpoint
            self.viewpoint_space.add_viewpoint(viewpoint)

            if self.config.verbose:
                print(f"  ✓ {agent_id}: {result[:100]}...")

        # 检测初始涌现
        initial_report = self.emergence_detector.detect(self.viewpoint_space, 0)
        if self.config.verbose:
            print(f"\n  初始涌现类型: {initial_report.emergence_type.value}")
            print(f"  初始多样性: {initial_report.metrics.diversity:.2f}")
            print(f"  初始共识度: {initial_report.metrics.consensus:.2f}")

        return viewpoints

    async def _stage2_collision(self,
                               task: str,
                               initial_viewpoints: Dict[str, Viewpoint]) -> List[Dict]:
        """
        阶段2: 观点碰撞

        Agent之间进行多轮讨论，观点碰撞
        """
        discussion_rounds = []
        max_rounds = min(self.config.max_rounds, 5)  # 最多5轮讨论

        for round_num in range(1, max_rounds + 1):
            self.current_round = round_num

            if self.config.verbose:
                print(f"\n  第 {round_num} 轮讨论:")

            # 开始新一轮讨论
            round_obj = self.viewpoint_space.start_discussion_round(round_num)

            # 生成讨论对（相邻Agent配对）
            agent_ids = list(self.agents.keys())
            discussion_pairs = []
            for i in range(len(agent_ids)):
                j = (i + 1) % len(agent_ids)
                discussion_pairs.append((agent_ids[i], agent_ids[j]))

            # 并发执行讨论
            tasks = []
            for agent1_id, agent2_id in discussion_pairs:
                # 获取之前的消息作为上下文
                peer_messages = [
                    {
                        'agent_id': msg.agent_id,
                        'content': msg.content[:200]
                    }
                    for msg in self.viewpoint_space.message_history[-5:]  # 最近5条
                ]

                task_coroutine = self.agents[agent1_id].discuss(
                    topic=task,
                    peer_messages=peer_messages,
                    round_num=round_num
                )
                tasks.append(task_coroutine)

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # 处理结果
            for (agent1_id, _), result in zip(discussion_pairs, results):
                if isinstance(result, Exception):
                    continue

                # 创建消息对象
                message = Message(
                    message_id=str(uuid.uuid4()),
                    agent_id=agent1_id,
                    content=result,
                    message_type=MessageType.DISCUSSION,
                    round_num=round_num
                )
                self.viewpoint_space.add_message(message)
                round_obj.add_message(message)

                if self.config.verbose:
                    print(f"    [{agent1_id}]: {result[:150]}...")

            # 结束本轮
            self.viewpoint_space.finish_discussion_round(round_num)
            discussion_rounds.append(round_obj.to_dict())

            # 检测收敛
            report = self.emergence_detector.detect(self.viewpoint_space, round_num)
            if self.config.verbose:
                print(f"    共识度: {report.metrics.consensus:.2f}")
                print(f"    系统阶段: {report.system_phase.value}")

            # 如果共识很高，提前结束
            if report.metrics.consensus > self.config.convergence_threshold:
                if self.config.verbose:
                    print(f"\n  ✓ 达到共识阈值，提前结束讨论")
                break

            # 触发回调
            if self.on_round_complete:
                await self.on_round_complete(round_num, report)

        return discussion_rounds

    async def _stage3_convergence(self,
                                initial_viewpoints: Dict[str, Viewpoint],
                                discussion_rounds: List[Dict]) -> List[str]:
        """
        阶段3: 观点收敛

        综合所有观点和讨论，形成初步方案
        """
        synthesis_history = []

        # 准备上下文
        all_viewpoints = [
            {
                'agent_id': agent_id,
                'content': vp.content
            }
            for agent_id, vp in initial_viewpoints.items()
        ]

        # 并发综合
        tasks = []
        for agent in self.agents.values():
            task_coroutine = agent.synthesize(all_viewpoints, discussion_rounds)
            tasks.append(task_coroutine)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理结果
        for agent, result in zip(self.agents.values(), results):
            if isinstance(result, Exception):
                continue

            synthesis_history.append(result)

            if self.config.verbose:
                print(f"\n  [{agent.agent_id}] 的综合方案:")
                print(f"  {result[:200]}...")

        return synthesis_history

    async def _stage4_refinement(self,
                                 task: str,
                                 synthesis: List[str],
                                 discussion_rounds: List[Dict]) -> tuple:
        """
        阶段4: 迭代优化

        基于反馈迭代优化方案，直到达到涌现阈值
        """
        # 选择最佳初始方案（选择最长的，通常更完整）
        best_synthesis = max(synthesis, key=len) if synthesis else "未生成方案"

        current_solution = best_synthesis
        refinement_history = [current_solution]

        # 迭代优化
        for iteration in range(1, self.config.max_rounds + 1):
            if self.config.verbose:
                print(f"\n  第 {iteration} 轮优化:")

            # 收集反馈
            feedback_list = []
            for agent in self.agents.values():
                try:
                    evaluation = await agent.evaluate(current_solution)

                    # 构建反馈
                    feedback = {
                        'agent_id': agent.agent_id,
                        'content': f"评分: {evaluation.get('overall_score', 0)}/10\n"
                                   f"理由: {evaluation.get('reasoning', '')[:200]}",
                        'quality_score': evaluation.get('overall_score', 0) / 10,
                    }
                    feedback_list.append(feedback)

                    if self.config.verbose:
                        print(f"    [{agent.agent_id}]: {evaluation.get('overall_score', 0)}/10")

                except Exception as e:
                    if self.config.verbose:
                        print(f"    ⚠️ [{agent.agent_id}] 评估失败: {e}")
                    continue

            # 如果所有评分都很高，停止迭代
            avg_score = np.mean([f['quality_score'] for f in feedback_list])
            if avg_score > 0.85:
                if self.config.verbose:
                    print(f"\n  ✓ 平均评分 {avg_score:.2f} > 0.85，结束优化")
                break

            # 选择一个Agent进行优化（选择评分最低的建议最多的）
            best_agent_id = min(feedback_list, key=lambda f: f['quality_score'])['agent_id']

            try:
                refined = await self.agents[best_agent_id].refine(
                    current_solution,
                    feedback_list,
                    iteration
                )

                current_solution = refined
                refinement_history.append(refined)

                if self.config.verbose:
                    print(f"    → 由 {best_agent_id} 优化")

            except Exception as e:
                if self.config.verbose:
                    print(f"    ⚠️ 优化失败: {e}")
                break

        # 最终涌现检测
        final_report = self.emergence_detector.detect(self.viewpoint_space, 99)

        if self.config.verbose:
            print(f"\n=== 涌现检测 ===")
            print(f"涌现类型: {final_report.emergence_type.value}")
            print(f"涌现强度: {final_report.metrics.emergence_score:.2f}")
            print(f"系统阶段: {final_report.system_phase.value}")
            print(f"\n建议:")
            for rec in final_report.recommendations:
                print(f"  {rec}")

        return current_solution, final_report

    def _get_agent_contributions(self) -> Dict[str, int]:
        """获取Agent贡献统计"""
        return self.viewpoint_space.get_statistics()['agent_participation']

    def export_session(self, result: CollaborationResult, output_path: str):
        """
        导出会话记录

        Args:
            result: 协作结果
            output_path: 输出文件路径
        """
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        session_data = {
            'timestamp': datetime.now().isoformat(),
            'config': {
                'max_rounds': self.config.max_rounds,
                'agent_count': self.config.agent_count,
                'convergence_threshold': self.config.convergence_threshold,
            },
            'result': result.to_dict(),
            'viewpoint_space': self.viewpoint_space.to_dict(),
            'agents': {
                agent_id: agent.to_dict()
                for agent_id, agent in self.agents.items()
            }
        }

        # 根据文件格式导出
        if output.suffix == '.json':
            output.write_text(json.dumps(session_data, ensure_ascii=False, indent=2))
        elif output.suffix == '.md':
            self._export_markdown(session_data, output)
        else:
            output.write_text(json.dumps(session_data, ensure_ascii=False, indent=2))

    def _export_markdown(self, session_data: Dict, output_path: Path):
        """导出为Markdown格式"""
        lines = [
            "# 多Agent协作会话报告",
            "",
            f"**时间**: {session_data['timestamp']}",
            f"**总耗时**: {session_data['result']['total_time']:.1f}秒",
            f"**轮次**: {session_data['result']['rounds_completed']}",
            f"**消息数**: {session_data['result']['total_messages']}",
            "",
            "## 涌现分析",
            "",
            f"- **涌现类型**: {session_data['result']['emergence_report']['emergence_type']}",
            f"- **系统阶段**: {session_data['result']['emergence_report']['system_phase']}",
            f"- **涌现强度**: {session_data['result']['emergence_report']['metrics']['emergence_score']:.2f}",
            "",
            "### 详细指标",
            "",
            f"- 多样性: {session_data['result']['emergence_report']['metrics']['diversity']:.2f}",
            f"- 共识度: {session_data['result']['emergence_report']['metrics']['consensus']:.2f}",
            f"- 新颖度: {session_data['result']['emergence_report']['metrics']['novelty']:.2f}",
            f"- 整合度: {session_data['result']['emergence_report']['metrics']['integration']:.2f}",
            "",
            "## 初始观点",
            "",
        ]

        for agent_id, content in session_data['result']['initial_viewpoints'].items():
            lines.extend([
                f"### {agent_id}",
                "",
                content,
                ""
            ])

        lines.extend([
            "## 讨论过程",
            "",
        ])

        for round_data in session_data['result']['discussion_rounds']:
            lines.extend([
                f"### 第 {round_data['round_num']} 轮",
                "",
            ])
            for msg in round_data['messages']:
                lines.extend([
                    f"**{msg['agent_id']}** ({msg['message_type']}):",
                    "",
                    msg['content'],
                    ""
                ])

        lines.extend([
            "## 最终方案",
            "",
            session_data['result']['solution'],
            "",
            "## 建议",
            "",
        ])

        for rec in session_data['result']['emergence_report']['recommendations']:
            lines.append(f"- {rec}")

        output_path.write_text("\n".join(lines), encoding='utf-8')


# 工厂函数
def create_collaboration_engine(config: CollaborationConfig = None) -> CollaborationEngine:
    """
    创建协作引擎

    Args:
        config: 协作配置（可选）

    Returns:
        CollaborationEngine实例
    """
    if config is None:
        config = CollaborationConfig()

    return CollaborationEngine(config)


def create_engine_from_config(config_dict: Dict[str, Any]) -> CollaborationEngine:
    """
    从配置字典创建协作引擎

    Args:
        config_dict: 配置字典

    Returns:
        CollaborationEngine实例
    """
    config = CollaborationConfig(
        max_rounds=config_dict.get('max_rounds', 3),
        convergence_threshold=config_dict.get('convergence_threshold', 0.7),
        emergence_threshold=config_dict.get('emergence_threshold', 0.7),
        timeout_per_round=config_dict.get('timeout_per_round', 300),
        agent_count=config_dict.get('agent_count', 5),
        role_selection=config_dict.get('role_selection', 'auto'),
        llm_temperature=config_dict.get('llm_temperature', 0.7),
        llm_max_tokens=config_dict.get('llm_max_tokens', 2000),
        verbose=config_dict.get('verbose', False),
        save_intermediate=config_dict.get('save_intermediate', True)
    )

    return CollaborationEngine(config)


__all__ = [
    'CollaborationConfig',
    'CollaborationResult',
    'CollaborationEngine',
    'create_collaboration_engine',
    'create_engine_from_config',
]
