"""
ECS - Agent模块

定义Agent的核心数据结构和行为
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import asyncio
import anthropic
import os


class ThinkingStyle(Enum):
    """思维风格"""
    ANALYTICAL = "analytical"      # 分析型
    CREATIVE = "creative"          # 创造型
    PRACTICAL = "practical"        # 务实型
    CRITICAL = "critical"          # 批判型
    INTEGRATIVE = "integrative"    # 综合型
    EMPATHETIC = "empathetic"      # 共情型


@dataclass
class Personality:
    """性格特征（大五人格）"""
    openness: float = 0.5          # 开放性：创造力、好奇心
    conscientiousness: float = 0.5  # 尽责性：自律、可靠
    extraversion: float = 0.5       # 外向性：社交、活力
    agreeableness: float = 0.5      # 宜人性：合作、友善
    neuroticism: float = 0.5        # 神经质：情绪稳定性

    def __post_init__(self):
        """确保值在0-1范围内"""
        for attr in ['openness', 'conscientiousness', 'extraversion',
                     'agreeableness', 'neuroticism']:
            value = getattr(self, attr)
            setattr(self, attr, max(0.0, min(1.0, value)))

    def to_prompt_suffix(self) -> str:
        """转换为提示词后缀"""
        traits = []
        if self.openness > 0.7:
            traits.append("思维开放，乐于接受新想法")
        if self.conscientiousness > 0.7:
            traits.append("认真细致，注重细节")
        if self.extraversion > 0.7:
            traits.append("积极主动，善于沟通")
        if self.agreeableness > 0.7:
            traits.append("合作友善，寻求共识")
        if self.neuroticism < 0.3:
            traits.append("情绪稳定，抗压能力强")

        if traits:
            return "你的性格特点：" + "、".join(traits) + "。"
        return ""

    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {
            'openness': self.openness,
            'conscientiousness': self.conscientiousness,
            'extraversion': self.extraversion,
            'agreeableness': self.agreeableness,
            'neuroticism': self.neuroticism
        }


@dataclass
class Expertise:
    """专业领域"""
    domain: str                   # 领域名称
    skills: List[str] = field(default_factory=list)  # 技能列表
    experience_level: float = 0.5  # 经验水平（0-1）

    def to_description(self) -> str:
        """生成描述"""
        level_str = "初级" if self.experience_level < 0.33 else \
                    "中级" if self.experience_level < 0.67 else "高级"
        return f"{self.domain}（{level_str}，擅长{'、'.join(self.skills[:3])}）"


@dataclass
class AgentRole:
    """Agent角色定义"""
    id: str
    name: str
    description: str
    thinking_style: ThinkingStyle
    expertise: List[Expertise]
    system_prompt_template: str
    focus_areas: List[str] = field(default_factory=list)

    def get_system_prompt(self, personality: Optional[Personality] = None) -> str:
        """生成完整的系统提示"""
        prompt = f"""你是{self.name}。

{self.description}

你的思维风格：{self.thinking_style.value}
你的专业领域：
"""
        for exp in self.expertise:
            prompt += f"- {exp.to_description()}\n"

        if self.focus_areas:
            prompt += f"\n你的关注重点：{'、'.join(self.focus_areas)}\n"

        if personality:
            prompt += f"\n{personality.to_prompt_suffix()}\n"

        prompt += """
在讨论中，请：
1. 基于你的专业视角提出观点
2. 尊重其他角色的不同意见
3. 寻求共识而非固执己见
4. 建设性地提出挑战和补充
"""
        return prompt


class ECSAgent:
    """ECS Agent基类"""

    def __init__(self,
                 agent_id: str,
                 role: AgentRole,
                 personality: Personality,
                 llm_client: Optional[Any] = None):
        """
        初始化Agent

        Args:
            agent_id: Agent唯一标识
            role: 角色定义
            personality: 性格特征
            llm_client: LLM客户端（可选）
        """
        self.agent_id = agent_id
        self.role = role
        self.personality = personality
        self.llm_client = llm_client or self._create_default_client()

        # 状态追踪
        self.message_count = 0
        self.last_activity = None
        self.theory_of_mind_model = {}  # 对其他Agent的心智模型

        # 观点历史
        self.viewpoint_history = []

    def _create_default_client(self) -> anthropic.Anthropic:
        """创建默认的Anthropic客户端"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("需要设置ANTHROPIC_API_KEY环境变量")
        return anthropic.Anthropic(api_key=api_key)

    def get_system_prompt(self) -> str:
        """获取系统提示"""
        return self.role.get_system_prompt(self.personality)

    async def analyze(self, task: str, context: Dict[str, Any] = None) -> str:
        """
        独立分析任务（阶段1：观点发散）

        Args:
            task: 任务描述
            context: 额外上下文

        Returns:
            分析结果（观点文本）
        """
        prompt = f"""请对以下任务进行分析：

任务：{task}

请基于你的角色和专业视角，提供你的分析和观点。包括：
1. 你认为的核心问题是什么？
2. 有哪些关键的考虑因素？
3. 你的初步建议或想法是什么？
4. 有哪些潜在的风险或挑战？

请保持简洁，重点突出你的专业视角。
"""
        response = await self._call_llm(prompt)
        self.viewpoint_history.append({
            'stage': 'analyze',
            'content': response
        })
        return response

    async def discuss(self,
                     topic: str,
                     peer_messages: List[Dict[str, str]],
                     round_num: int) -> str:
        """
        参与讨论（阶段2：观点碰撞）

        Args:
            topic: 讨论主题
            peer_messages: 其他Agent的消息列表
            round_num: 当前轮次

        Returns:
            讨论发言
        """
        # 构建peer消息摘要
        peer_summary = self._summarize_peer_messages(peer_messages)

        prompt = f"""现在是讨论阶段。

讨论主题：{topic}

其他角色的观点摘要：
{peer_summary}

请你：
1. 基于你的专业视角回应这些观点
2. 提出你的补充、挑战或建议
3. 寻求与其他观点的连接或整合
4. 保持开放和建设性的态度

请简洁发言（200字以内）。
"""
        response = await self._call_llm(prompt)
        self.message_count += 1
        self.last_activity = 'discuss'
        return response

    async def synthesize(self,
                        all_viewpoints: List[Dict[str, str]],
                        discussions: List[Dict]) -> str:
        """
        综合观点（阶段3：观点收敛）

        Args:
            all_viewpoints: 所有Agent的初始观点
            discussions: 讨论记录

        Returns:
            综合方案
        """
        viewpoints_summary = self._format_viewpoints_summary(all_viewpoints)
        discussions_summary = self._format_discussions_summary(discussions)

        prompt = f"""请综合所有观点，形成一个整合方案。

所有初始观点：
{viewpoints_summary}

讨论过程：
{discussions_summary}

请基于你的角色，提供一个综合方案，要求：
1. 整合不同视角的关键洞察
2. 平衡不同观点的关切
3. 提出具体可行的建议
4. 说明为什么这个方案是最佳平衡

请结构化地呈现方案。
"""
        response = await self._call_llm(prompt)
        self.viewpoint_history.append({
            'stage': 'synthesize',
            'content': response
        })
        return response

    async def refine(self,
                    current_solution: str,
                    feedback_list: List[Dict[str, str]],
                    iteration: int) -> str:
        """
        优化方案（阶段4：迭代优化）

        Args:
            current_solution: 当前方案
            feedback_list: 其他Agent的反馈
            iteration: 当前迭代次数

        Returns:
            优化后的方案
        """
        feedback_summary = self._format_feedback_summary(feedback_list)

        prompt = f"""请基于反馈优化方案。

当前方案：
{current_solution}

其他角色的反馈：
{feedback_summary}

请：
1. 认真考虑这些反馈
2. 在保持核心价值的同时进行调整
3. 说明你做了哪些改进以及原因
4. 如果有无法采纳的反馈，说明原因

请提供优化后的完整方案。
"""
        response = await self._call_llm(prompt)
        self.viewpoint_history.append({
            'stage': 'refine',
            'content': response
        })
        return response

    async def evaluate(self, solution: str, criteria: List[str] = None) -> Dict[str, Any]:
        """
        评估方案质量

        Args:
            solution: 待评估方案
            criteria: 评估标准列表

        Returns:
            评估结果字典
        """
        if criteria is None:
            criteria = ["可行性", "完整性", "创新性", "实用性"]

        prompt = f"""请从你的专业视角评估以下方案：

方案：
{solution}

评估标准：{'、'.join(criteria)}

请对每个标准打分（0-10分）并简要说明理由。

以JSON格式返回：
{{
  "scores": {{
    "标准1": 分数,
    "标准2": 分数,
    ...
  }},
  "overall_score": 总分,
  "reasoning": "总体评价理由"
}}
"""
        response = await self._call_llm(prompt, use_json=True)

        # 解析JSON响应
        import json
        try:
            return json.loads(response)
        except:
            # 如果JSON解析失败，返回默认评分
            return {
                "scores": {c: 7.0 for c in criteria},
                "overall_score": 7.0,
                "reasoning": response
            }

    def _summarize_peer_messages(self, messages: List[Dict[str, str]]) -> str:
        """总结其他Agent的消息"""
        if not messages:
            return "暂无其他观点"

        summary_parts = []
        for msg in messages[:5]:  # 最多显示5条
            agent_id = msg.get('agent_id', 'Unknown')
            content = msg.get('content', '')[:150]
            summary_parts.append(f"- [{agent_id}]: {content}...")

        return "\n".join(summary_parts)

    def _format_viewpoints_summary(self, viewpoints: List[Dict[str, str]]) -> str:
        """格式化观点摘要"""
        if not viewpoints:
            return "无观点"

        parts = []
        for i, vp in enumerate(viewpoints, 1):
            agent_id = vp.get('agent_id', f'Agent{i}')
            content = vp.get('content', '')[:300]
            parts.append(f"\n{i}. [{agent_id}]:\n{content}")

        return "\n".join(parts)

    def _format_discussions_summary(self, discussions: List[Dict]) -> str:
        """格式化讨论摘要"""
        if not discussions:
            return "无讨论记录"

        parts = []
        for discussion in discussions[:3]:  # 最多显示3轮讨论
            round_num = discussion.get('round', '?')
            parts.append(f"\n=== 第{round_num}轮讨论 ===")
            for msg in discussion.get('messages', [])[:3]:
                agent_id = msg.get('agent_id', '?')
                content = msg.get('content', '')[:100]
                parts.append(f"  [{agent_id}]: {content}")

        return "\n".join(parts)

    def _format_feedback_summary(self, feedback_list: List[Dict[str, str]]) -> str:
        """格式化反馈摘要"""
        if not feedback_list:
            return "无反馈"

        parts = []
        for i, feedback in enumerate(feedback_list, 1):
            agent_id = feedback.get('agent_id', f'Agent{i}')
            content = feedback.get('content', '')[:200]
            parts.append(f"{i}. [{agent_id}]: {content}")

        return "\n".join(parts)

    async def _call_llm(self,
                        prompt: str,
                        use_json: bool = False,
                        max_tokens: int = 2000) -> str:
        """
        调用LLM

        Args:
            prompt: 提示词
            use_json: 是否要求JSON输出
            max_tokens: 最大token数

        Returns:
            LLM响应
        """
        system_prompt = self.get_system_prompt()

        try:
            message = self.llm_client.messages.create(
                model="claude-sonnet-4-20250514",  # 或使用环境变量配置
                max_tokens=max_tokens,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            # 错误处理
            return f"LLM调用失败：{str(e)}"

    def update_theory_of_mind(self, other_agent_id: str, observation: Dict):
        """更新对其他Agent的心智模型"""
        if other_agent_id not in self.theory_of_mind_model:
            self.theory_of_mind_model[other_agent_id] = {
                'reliability': 0.5,
                'expertise_areas': [],
                'communication_style': 'unknown',
                'interaction_count': 0
            }

        model = self.theory_of_mind_model[other_agent_id]
        model['interaction_count'] += 1

        # 更新可靠性评分（指数移动平均）
        current_reliability = observation.get('reliability', 0.5)
        model['reliability'] = 0.7 * model['reliability'] + 0.3 * current_reliability

        # 记录专业领域
        expertise = observation.get('expertise')
        if expertise and expertise not in model['expertise_areas']:
            model['expertise_areas'].append(expertise)

    def get_theory_of_mind(self, other_agent_id: str) -> Optional[Dict]:
        """获取对其他Agent的心智模型"""
        return self.theory_of_mind_model.get(other_agent_id)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于序列化）"""
        return {
            'agent_id': self.agent_id,
            'role': {
                'id': self.role.id,
                'name': self.role.name,
                'description': self.role.description,
                'thinking_style': self.role.thinking_style.value
            },
            'personality': self.personality.to_dict(),
            'message_count': self.message_count,
            'last_activity': self.last_activity
        }


def create_agent_from_config(config: Dict[str, Any]) -> ECSAgent:
    """
    从配置字典创建Agent

    Args:
        config: 配置字典，包含role, personality等

    Returns:
        ECSAgent实例
    """
    role_config = config.get('role', {})
    personality_config = config.get('personality', {})

    role = AgentRole(
        id=role_config.get('id', 'custom'),
        name=role_config.get('name', 'Custom Role'),
        description=role_config.get('description', ''),
        thinking_style=ThinkingStyle(role_config.get('thinking_style', 'analytical')),
        expertise=[
            Expertise(
                domain=exp.get('domain', ''),
                skills=exp.get('skills', []),
                experience_level=exp.get('experience_level', 0.5)
            )
            for exp in role_config.get('expertise', [])
        ],
        system_prompt_template=role_config.get('system_prompt_template', ''),
        focus_areas=role_config.get('focus_areas', [])
    )

    personality = Personality(**personality_config)

    return ECSAgent(
        agent_id=config.get('agent_id', 'agent_0'),
        role=role,
        personality=personality
    )
