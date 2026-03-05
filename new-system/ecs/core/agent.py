"""
ECS - Agent核心实现
支持SPAR循环、Theory of Mind、迹发沟通
"""

import asyncio
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import anthropic
from anthropic import APIError, APITimeoutError, RateLimitError
from datetime import datetime
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)


# ============================================================
# 数据结构
# ============================================================

class Personality:
    """大五人格模型 - 性格特质"""

    def __init__(
        self,
        openness: float = 0.5,        # 开放性：创造力、好奇心
        conscientiousness: float = 0.5, # 尽责性：自律、组织能力
        extraversion: float = 0.5,     # 外向性：社交活跃度
        agreeableness: float = 0.5,    # 宜人性：合作倾向
        neuroticism: float = 0.5       # 神经质：情绪稳定性
    ):
        self.openness = max(0.0, min(1.0, openness))
        self.conscientiousness = max(0.0, min(1.0, conscientiousness))
        self.extraversion = max(0.0, min(1.0, extraversion))
        self.agreeableness = max(0.0, min(1.0, agreeableness))
        self.neuroticism = max(0.0, min(1.0, neuroticism))

    def to_dict(self) -> Dict[str, float]:
        return {
            "openness": self.openness,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "agreeableness": self.agreeableness,
            "neuroticism": self.neuroticism
        }


class TheoryOfMind:
    """心智模型 - Agent对其他Agent的理解"""

    def __init__(self):
        # beliefs[agent_id] = 该Agent当前观点的摘要
        self.beliefs: Dict[str, str] = {}

        # confidence[agent_id] = 对该Agent观点的置信度
        self.confidence: Dict[str, float] = {}

        # personality_models[agent_id] = 对该Agent性格的建模
        self.personality_models: Dict[str, Personality] = {}

    def update_belief(self, agent_id: str, belief: str, confidence: float = 0.5):
        """更新对某个Agent的信念"""
        self.beliefs[agent_id] = belief
        self.confidence[agent_id] = max(0.0, min(1.0, confidence))

    def get_belief(self, agent_id: str) -> Optional[str]:
        """获取对某个Agent的信念"""
        return self.beliefs.get(agent_id)

    def get_confidence(self, agent_id: str) -> float:
        """获取对某个Agent的置信度"""
        return self.confidence.get(agent_id, 0.5)

    def should_respond(self, agent_id: str, threshold: float = 0.7) -> bool:
        """判断是否应该回应某个Agent的观点"""
        confidence = self.get_confidence(agent_id)
        # 如果置信度低，表示有异议，应该回应
        return confidence < threshold


class EnvironmentContext:
    """环境上下文 - 迹发沟通的核心"""

    def __init__(self):
        # 共享的观察信息
        self.observations: List[Dict] = []

        # 发现的问题/bug
        self.issues: List[Dict] = []

        # 想法/建议
        self.ideas: List[Dict] = []

        # 外部信息/证据
        self.evidences: List[Dict] = []

        # 代码/实现片段
        self.snippets: List[Dict] = []

        # 测试用例
        self.test_cases: List[Dict] = []

        # 元数据
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "version": "2.0"
        }

    def add_observation(self, agent_id: str, content: str, tags: List[str] = None):
        """添加观察信息"""
        self.observations.append({
            "agent_id": agent_id,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or []
        })

    def add_issue(self, agent_id: str, issue: str, severity: str = "medium", location: str = ""):
        """添加问题/bug"""
        self.issues.append({
            "agent_id": agent_id,
            "issue": issue,
            "severity": severity,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "resolved": False
        })

    def add_idea(self, agent_id: str, idea: str, category: str = "general"):
        """添加想法/建议"""
        self.ideas.append({
            "agent_id": agent_id,
            "idea": idea,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })

    def add_evidence(self, agent_id: str, evidence: str, source: str = ""):
        """添加外部证据"""
        self.evidences.append({
            "agent_id": agent_id,
            "evidence": evidence,
            "source": source,
            "timestamp": datetime.now().isoformat()
        })

    def add_snippet(self, agent_id: str, code: str, language: str = "python", description: str = ""):
        """添加代码片段"""
        self.snippets.append({
            "agent_id": agent_id,
            "code": code,
            "language": language,
            "description": description,
            "timestamp": datetime.now().isoformat()
        })

    def add_test_case(self, agent_id: str, test_case: str, expected: str = ""):
        """添加测试用例"""
        self.test_cases.append({
            "agent_id": agent_id,
            "test_case": test_case,
            "expected": expected,
            "timestamp": datetime.now().isoformat()
        })

    def get_recent(self, category: str, limit: int = 5) -> List[Dict]:
        """获取最近的信息（迹发沟通的核心）"""
        mapping = {
            "observations": self.observations,
            "issues": self.issues,
            "ideas": self.ideas,
            "evidences": self.evidences,
            "snippets": self.snippets,
            "test_cases": self.test_cases
        }
        items = mapping.get(category, [])
        return items[-limit:] if items else []

    def get_summary(self) -> str:
        """获取环境上下文摘要（供Agent感知）"""
        parts = []

        if self.observations:
            parts.append(f"## 观察信息\n{self._format_items(self.observations)}")

        if self.issues:
            parts.append(f"## 发现的问题\n{self._format_items(self.issues)}")

        if self.ideas:
            parts.append(f"## 想法与建议\n{self._format_items(self.ideas)}")

        if self.evidences:
            parts.append(f"## 外部证据\n{self._format_items(self.evidences)}")

        if self.snippets:
            parts.append(f"## 代码片段\n{self._format_items(self.snippets)}")

        if self.test_cases:
            parts.append(f"## 测试用例\n{self._format_items(self.test_cases)}")

        return "\n\n".join(parts) if parts else "（环境为空）"

    def _format_items(self, items: List[Dict]) -> str:
        """格式化项目列表"""
        formatted = []
        for item in items[-5:]:  # 最多显示5个
            if "content" in item:
                formatted.append(f"- [{item['agent_id']}] {item['content']}")
            elif "issue" in item:
                formatted.append(f"- [{item['agent_id']}] {item['issue']} [{item['severity']}]")
            elif "idea" in item:
                formatted.append(f"- [{item['agent_id']}] {item['idea']}")
            elif "evidence" in item:
                formatted.append(f"- [{item['agent_id']}] {item['evidence']} (来源: {item['source']})")
            elif "code" in item:
                formatted.append(f"- [{item['agent_id']}] {item.get('description', '代码')}")
            elif "test_case" in item:
                formatted.append(f"- [{item['agent_id']}] {item['test_case']}")
        return "\n".join(formatted) if formatted else "无"

    def to_dict(self) -> Dict:
        """转换为字典（用于序列化）"""
        return {
            "observations": self.observations,
            "issues": self.issues,
            "ideas": self.ideas,
            "evidences": self.evidences,
            "snippets": self.snippets,
            "test_cases": self.test_cases,
            "metadata": self.metadata
        }


# ============================================================
# Agent实现
# ============================================================

class ECSAgent:
    """
    ECS智能体核心实现

    特性：
    - 支持SPAR循环（感知-讨论-行动-反思）
    - Theory of Mind（心智建模）
    - 迹发沟通（通过环境传递信息）
    - 动态温度调整
    """

    # 角色定义（加载自roles.py）
    ROLE_DEFINITIONS = None

    def __init__(
        self,
        agent_id: str,
        role: str,
        api_key: str,
        llm_provider: str = "anthropic",
        model: str = "claude-sonnet-4-20250514",
        personality: Optional[Personality] = None,
        enable_tom: bool = True,
        enable_stigmergy: bool = True
    ):
        self.agent_id = agent_id
        self.role = role
        self.llm_provider = llm_provider
        self.model = model
        self.enable_tom = enable_tom
        self.enable_stigmergy = enable_stigmergy

        # 性格特质
        self.personality = personality or Personality()

        # 心智模型
        self.theory_of_mind = TheoryOfMind() if enable_tom else None

        # API客户端
        self.client = anthropic.Anthropic(api_key=api_key)

        # 角色信息（延迟加载）
        self._role_info = None

        # 历史记录
        self.message_history: List[Dict] = []

    @property
    def role_info(self) -> Dict:
        """获取角色信息"""
        if self._role_info is None:
            from ..roles import ROLE_DEFINITIONS
            self._role_info = ROLE_DEFINITIONS.get(self.role, {
                "role_name": "Unknown",
                "description": "未知角色",
                "thinking_style": "通用",
                "expertise": [],
                "personality_weights": {}
            })
        return self._role_info

    # ========================================================
    # SPAR循环 - Sense阶段
    # ========================================================

    async def sense(
        self,
        task: str,
        env_context: EnvironmentContext,
        available_tools: List[Dict] = None
    ) -> Dict:
        """
        感知阶段：获取任务相关信息

        Args:
            task: 任务描述
            env_context: 环境上下文（迹发沟通的载体）
            available_tools: 可用的感知工具列表

        Returns:
            感知结果字典
        """
        role_info = self.role_info

        # 构建感知提示词
        prompt = self._build_sense_prompt(task, env_context, available_tools)

        # 调用LLM
        response = await self._call_llm(
            prompt=prompt,
            temperature=0.5,  # 感知阶段使用中等温度
            max_tokens=1500
        )

        # 解析响应
        result = self._parse_sense_response(response)

        # 更新环境上下文（迹发沟通）
        if self.enable_stigmergy:
            for observation in result.get("observations", []):
                env_context.add_observation(
                    agent_id=self.agent_id,
                    content=observation,
                    tags=result.get("tags", [])
                )

            for issue in result.get("issues", []):
                env_context.add_issue(
                    agent_id=self.agent_id,
                    issue=issue["description"],
                    severity=issue.get("severity", "medium"),
                    location=issue.get("location", "")
                )

        return result

    def _build_sense_prompt(
        self,
        task: str,
        env_context: EnvironmentContext,
        available_tools: List[Dict]
    ) -> str:
        """构建感知提示词"""
        role_info = self.role_info

        prompt = f"""你是{role_info['role_name']}，负责{role_info['description']}。

你的思维风格是：{role_info['thinking_style']}

当前任务：{task}

## 环境上下文（其他Agent的感知成果）

{env_context.get_summary()}

## 你的感知任务

请从你角色的专业角度，对任务进行感知和分析：

1. **观察**：你注意到了什么？有什么关键信息？
2. **问题识别**：你发现了哪些潜在问题、风险或漏洞？
3. **信息需求**：你需要哪些额外信息？（如果有可用的工具，请说明）
4. **初步想法**：你有什么初步的想法或建议？

请以结构化的方式输出：
- 观察列表（每个观察一句话）
- 问题列表（如有，标注严重程度：low/medium/high/critical）
- 信息需求列表
- 初步想法列表
- 相关标签（用于分类，如：architecture、security、performance等）
"""

        return prompt

    def _parse_sense_response(self, response: str) -> Dict:
        """解析感知响应"""
        # 简单的解析实现
        result = {
            "observations": [],
            "issues": [],
            "information_needs": [],
            "initial_ideas": [],
            "tags": []
        }

        lines = response.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if '观察' in line and ('列表' in line or ':' in line):
                current_section = "observations"
            elif '问题' in line and ('列表' in line or ':' in line):
                current_section = "issues"
            elif '信息' in line and '需求' in line:
                current_section = "information_needs"
            elif '想法' in line and ('列表' in line or ':' in line):
                current_section = "initial_ideas"
            elif '标签' in line:
                current_section = "tags"
            elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                content = line.lstrip('-•*').strip()
                if content and current_section:
                    if current_section == "issues":
                        result[current_section].append({"description": content})
                    else:
                        result[current_section].append(content)

        return result

    # ========================================================
    # SPAR循环 - Discuss阶段
    # ========================================================

    async def discuss(
        self,
        task: str,
        env_context: EnvironmentContext,
        peer_messages: List[Dict],
        round_num: int,
        temperature: float = 0.8
    ) -> str:
        """
        讨论阶段：参与无领导小组讨论

        Args:
            task: 任务描述
            env_context: 环境上下文
            peer_messages: 其他Agent的发言历史
            round_num: 当前轮次
            temperature: 温度参数

        Returns:
            发言内容
        """
        role_info = self.role_info

        # 构建讨论提示词
        prompt = self._build_discuss_prompt(
            task, env_context, peer_messages, round_num
        )

        # 调用LLM
        response = await self._call_llm(
            prompt=prompt,
            temperature=temperature,  # 讨论阶段使用较高温度
            max_tokens=2000
        )

        # 更新心智模型
        if self.theory_of_mind:
            for msg in peer_messages:
                peer_id = msg.get("agent_id", "unknown")
                # 根据发言内容更新对peer的理解
                self.theory_of_mind.update_belief(
                    agent_id=peer_id,
                    belief=msg.get("content", "")[:200],  # 摘要
                    confidence=self._estimate_agreement(response, msg.get("content", ""))
                )

        # 更新环境上下文
        if self.enable_stigmergy:
            # 提取发言中的想法并添加到环境
            env_context.add_idea(
                agent_id=self.agent_id,
                idea=response[:500],  # 摘要
                category="discussion"
            )

        return response

    def _build_discuss_prompt(
        self,
        task: str,
        env_context: EnvironmentContext,
        peer_messages: List[Dict],
        round_num: int
    ) -> str:
        """构建讨论提示词"""
        role_info = self.role_info

        # 构建讨论历史
        discussion_history = ""
        if peer_messages:
            discussion_history = "## 之前的讨论\n\n"
            for msg in peer_messages[-5:]:  # 最近5条
                agent_id = msg.get("agent_id", "Unknown")
                content = msg.get("content", "")
                discussion_history += f"**{agent_id}**: {content}\n\n"

        # 环境上下文（迹发沟通）
        env_summary = env_context.get_summary()

        prompt = f"""你是{role_info['role_name']}，负责{role_info['description']}。

你的思维风格是：{role_info['thinking_style']}

## 当前任务

{task}

## 环境上下文

{env_summary}

{discussion_history}

## 你的发言任务（第{round_num}轮讨论）

请基于你的角色专业角度，参与讨论：

### 发言原则
1. **坚持你的视角**：基于你的专业背景提出观点
2. **基于证据**：引用环境上下文中的观察、证据或代码片段
3. **建设性批判**：如果不同意，请提出具体的改进建议
4. **推动共识**：在适当的时候寻求共识或妥协
5. **涌现意识**：如果发现了新的洞察或突破，请明确指出

### 发言结构
1. 你的核心观点（一句话）
2. 你的理由（引用证据）
3. 你对其他观点的回应（同意/反对/补充）
4. 你的建议或下一步

请直接输出你的发言内容，不要包含格式标记。
"""

        return prompt

    def _estimate_agreement(self, my_response: str, peer_content: str) -> float:
        """估算与peer观点的一致性（简化版）"""
        # 实际实现应使用语义相似度
        # 这里使用简单的关键词重叠
        my_words = set(my_response.lower().split())
        peer_words = set(peer_content.lower().split())
        overlap = len(my_words & peer_words)
        total = len(my_words | peer_words)
        return overlap / total if total > 0 else 0.5

    # ========================================================
    # SPAR循环 - Act阶段
    # ========================================================

    async def act(
        self,
        task: str,
        env_context: EnvironmentContext,
        consensus_summary: str,
        temperature: float = 0.2
    ) -> Dict:
        """
        行动阶段：将共识转化为具体输出

        Args:
            task: 任务描述
            env_context: 环境上下文
            consensus_summary: 共识摘要
            temperature: 温度参数（行动阶段使用低温）

        Returns:
            行动结果（包含具体输出：代码、设计文档、解决方案等）
        """
        role_info = self.role_info

        # 构建行动提示词
        prompt = self._build_act_prompt(task, env_context, consensus_summary)

        # 调用LLM
        response = await self._call_llm(
            prompt=prompt,
            temperature=temperature,  # 行动阶段使用低温度
            max_tokens=4000
        )

        # 解析行动结果
        result = self._parse_act_response(response)

        return result

    def _build_act_prompt(
        self,
        task: str,
        env_context: EnvironmentContext,
        consensus_summary: str
    ) -> str:
        """构建行动提示词"""
        role_info = self.role_info

        prompt = f"""你是{role_info['role_name']}，负责{role_info['description']}。

## 原始任务

{task}

## 团队共识

{consensus_summary}

## 环境上下文（所有观察、问题、证据、代码片段）

{env_context.get_summary()}

## 你的行动任务

基于团队共识，从你的角色角度产出具体成果：

### 输出要求
1. **精确性**：基于共识，不要添加未经讨论的内容
2. **完整性**：覆盖共识中的所有要点
3. **质量**：产出专业、可直接使用的内容

### 输出格式（根据你的角色）
- **Architect**: 架构图、系统设计文档、模块划分
- **Hacker**: 可执行代码、实现细节、注释
- **Researcher**: 技术调研报告、最佳实践、参考资料
- **Skeptic**: 风险评估、安全检查清单、测试要点
- **Optimizer**: 性能分析、优化建议、复杂度评估
- **Tester**: 测试计划、测试用例、验收标准
- **Designer**: 用户流程、界面原型、交互说明

请输出你的工作成果，使用适当的格式（代码块、Markdown、列表等）。
"""

        return prompt

    def _parse_act_response(self, response: str) -> Dict:
        """解析行动响应"""
        result = {
            "content": response,
            "type": "text",
            "agent_id": self.agent_id,
            "role": self.role,
            "timestamp": datetime.now().isoformat()
        }

        # 检测是否包含代码
        if "```" in response:
            result["type"] = "code"
            # 提取代码块
            import re
            code_blocks = re.findall(r'```(\w+)?\n(.*?)```', response, re.DOTALL)
            if code_blocks:
                result["code_blocks"] = [
                    {"language": lang or "text", "code": code.strip()}
                    for lang, code in code_blocks
                ]

        return result

    # ========================================================
    # SPAR循环 - Reflect阶段
    # ========================================================

    async def reflect(
        self,
        task: str,
        discussion_history: List[Dict],
        final_output: str,
        emergence_metrics: Dict
    ) -> str:
        """
        反思阶段：对整个协作过程进行反思

        Args:
            task: 原始任务
            discussion_history: 讨论历史
            final_output: 最终输出
            emergence_metrics: 涌现指标

        Returns:
            反思报告
        """
        prompt = self._build_reflect_prompt(
            task, discussion_history, final_output, emergence_metrics
        )

        response = await self._call_llm(
            prompt=prompt,
            temperature=0.6,
            max_tokens=2000
        )

        return response

    def _build_reflect_prompt(
        self,
        task: str,
        discussion_history: List[Dict],
        final_output: str,
        emergence_metrics: Dict
    ) -> str:
        """构建反思提示词"""
        # 构建简化的讨论历史
        history_summary = ""
        if discussion_history:
            for msg in discussion_history[-10:]:
                history_summary += f"{msg.get('agent_id')}: {msg.get('content', '')[:100]}...\n"

        prompt = f"""你是{self.role_info['role_name']}，现在需要对整个协作过程进行反思。

## 原始任务

{task}

## 讨论过程摘要

{history_summary}

## 最终输出

{final_output[:1000]}...

## 涌现指标

- 多样性: {emergence_metrics.get('diversity', 0):.2f}
- 共识度: {emergence_metrics.get('consensus', 0):.2f}
- 新颖度: {emergence_metrics.get('novelty', 0):.2f}
- 整合度: {emergence_metrics.get('integration', 0):.2f}
- 涌现强度: {emergence_metrics.get('emergence_score', 0):.2f}

## 反思任务

请从你的角色角度，对这次协作进行反思：

1. **协作质量**：讨论是否充分？是否有重要观点被遗漏？
2. **输出质量**：最终成果是否满足任务要求？有哪些不足？
3. **涌现评估**：是否实现了真涌现？涌现的强度和类型？
4. **改进建议**：如果再次进行类似的任务，有哪些改进空间？

请输出你的反思报告。
"""

        return prompt

    # ========================================================
    # 通用方法
    # ========================================================

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=4,
            max=10
        ),
        retry=retry_if_exception_type((
            APIError,
            APITimeoutError,
            RateLimitError
        )),
        reraise=True
    )
    async def _call_llm(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """带重试的LLM调用"""
        system_prompt = self._get_system_prompt()

        # Anthropic SDK 的 messages.create 是同步的，需要在异步上下文中运行
        loop = asyncio.get_event_loop()
        message = await loop.run_in_executor(
            None,
            lambda: self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
        )
        return message.content[0].text

    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        role_info = self.role_info

        prompt = f"""你是{role_info['role_name']}，在多Agent协作系统中工作。

## 你的角色

{role_info['description']}

## 你的思维风格

{role_info['thinking_style']}

## 你的专业领域

{', '.join(role_info.get('expertise', []))}

## 协作原则

1. **无领导协作**：没有固定的领导者，基于贡献影响力
2. **坚持你的视角**：基于你的专业背景提出观点
3. **基于证据**：引用观察、证据或代码片段支持你的观点
4. **建设性批判**：如果不同意，请提出具体的改进建议
5. **推动共识**：在适当的时候寻求共识或妥协
6. **迹发沟通**：通过环境上下文传递信息，减少重复
7. **涌现意识**：当发现新的洞察或突破时，请明确指出

## 性格特质

你的性格特质会影响你的发言风格：
- 开放性: {self.personality.openness:.2f} (影响创造力)
- 尽责性: {self.personality.conscientiousness:.2f} (影响详细程度)
- 外向性: {self.personality.extraversion:.2f} (影响发言频率)
- 宜人性: {self.personality.agreeableness:.2f} (影响合作倾向)
- 神经质: {self.personality.neuroticism:.2f} (影响风险感知)

请始终保持你的角色定位，以专业、建设性的方式参与协作。
"""
        return prompt

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "personality": self.personality.to_dict(),
            "enable_tom": self.enable_tom,
            "enable_stigmergy": self.enable_stigmergy,
            "theory_of_mind": {
                "beliefs": self.theory_of_mind.beliefs if self.theory_of_mind else {},
                "confidence": self.theory_of_mind.confidence if self.theory_of_mind else {}
            }
        }


# ============================================================
# 工厂函数
# ============================================================

def create_agent(
    agent_id: str,
    role: str,
    api_key: str,
    **kwargs
) -> ECSAgent:
    """创建Agent实例"""
    return ECSAgent(
        agent_id=agent_id,
        role=role,
        api_key=api_key,
        **kwargs
    )


def create_agent_group(
    roles: List[str],
    api_key: str,
    llm_provider: str = "anthropic",
    model: str = "claude-sonnet-4-20250514"
) -> List[ECSAgent]:
    """创建一组Agent"""
    agents = []
    for i, role in enumerate(roles):
        agent_id = f"{role}_{i+1}"
        agent = create_agent(
            agent_id=agent_id,
            role=role,
            api_key=api_key,
            llm_provider=llm_provider,
            model=model
        )
        agents.append(agent)
    return agents
