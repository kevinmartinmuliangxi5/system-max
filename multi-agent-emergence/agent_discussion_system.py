"""
多Agent协作讨论系统 - 真涌现实现

基于不同角色的LLM agents通过讨论协作完成任务
实现语义层面的真涌现
"""

import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from openai import OpenAI
import os
from datetime import datetime


@dataclass
class Message:
    """讨论消息"""
    speaker: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"[{self.speaker}]: {self.content}"


@dataclass
class Agent:
    """Agent角色"""
    name: str
    role: str
    personality: str
    system_prompt: str

    def __str__(self):
        return f"{self.name} ({self.role})"


class DiscussionFacilitator:
    """讨论主持人"""

    def __init__(self, api_key: str, base_url: str = "https://open.bigmodel.cn/api/coding/paas/v4"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = "GLM-4.7"

        # 定义Agent角色
        self.agents = self._create_agents()

        # 讨论历史
        self.discussion: List[Message] = []

        # 涌现时刻
        self.emergence_moments = []

    def _create_agents(self) -> Dict[str, Agent]:
        """创建不同角色的Agent"""
        return {
            "Architect": Agent(
                name="Architect",
                role="架构师",
                personality="系统化思维，关注整体设计",
                system_prompt="""你是一位资深架构师。
你的职责：
1. 分析问题的本质和核心需求
2. 提出高层解决思路和架构设计
3. 从系统角度思考，不纠结细节
4. 用简洁语言表达思路（不超过150字）

风格：理性、全局观、概括性强"""
            ),

            "Coder": Agent(
                name="Coder",
                role="编码者",
                personality="实干主义，快速实现",
                system_prompt="""你是一位实用主义程序员。
你的职责：
1. 根据架构思路编写代码
2. 代码简洁清晰，可读性高
3. 优先完成功能，不过度优化
4. 用Python实现

风格：务实、高效、追求简单"""
            ),

            "Critic": Agent(
                name="Critic",
                role="评审者",
                personality="批判性思维，挑刺专家",
                system_prompt="""你是一位严格的代码评审专家。
你的职责：
1. 找出方案或代码的潜在问题
2. 指出边界情况和漏洞
3. 质疑不合理的设计
4. 批评要建设性（不超过100字）

风格：犀利、严谨、追求完美"""
            ),

            "Optimizer": Agent(
                name="Optimizer",
                role="优化者",
                personality="追求极致性能",
                system_prompt="""你是一位性能优化专家。
你的职责：
1. 分析算法时间/空间复杂度
2. 提出优化建议
3. 权衡可读性和性能
4. 只在必要时优化（不超过100字）

风格：精益求精、注重效率"""
            ),

            "Tester": Agent(
                name="Tester",
                role="测试者",
                personality="细致严谨，考虑全面",
                system_prompt="""你是一位资深测试工程师。
你的职责：
1. 设计关键测试用例
2. 考虑边界条件和异常情况
3. 验证方案的正确性
4. 简明列出测试点（不超过100字）

风格：谨慎、全面、追求质量"""
            )
        }

    async def agent_speak(self, agent: Agent, context: str) -> str:
        """Agent发言"""
        # 构建上下文（最近5轮讨论）
        recent_discussion = "\n".join([
            str(msg) for msg in self.discussion[-5:]
        ])

        prompt = f"""当前任务：{context}

最近讨论：
{recent_discussion if recent_discussion else "(首轮发言)"}

现在轮到你发言。请从你的角色出发，给出简洁的观点。"""

        # 调用LLM
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": agent.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # 增加多样性
                max_tokens=300
            )

            content = response.choices[0].message.content.strip()

            # 记录到讨论历史
            msg = Message(speaker=agent.name, content=content)
            self.discussion.append(msg)

            return content

        except Exception as e:
            return f"[{agent.name} 发言失败: {e}]"

    async def facilitate_discussion(self, task: str, rounds: int = 3) -> Dict:
        """主持讨论"""
        print("=" * 60)
        print(f"🎯 任务：{task}")
        print("=" * 60)
        print()

        # 讨论顺序
        order = ["Architect", "Coder", "Critic", "Optimizer", "Tester"]

        for round_num in range(1, rounds + 1):
            print(f"\n{'='*60}")
            print(f"📢 第 {round_num} 轮讨论")
            print(f"{'='*60}\n")

            for agent_name in order:
                agent = self.agents[agent_name]

                print(f"💬 {agent.role} ({agent.name}) 发言中...")

                response = await self.agent_speak(agent, task)

                print(f"[{agent.name}]:")
                print(f"{response}\n")

                # 检测涌现
                if self._detect_emergence_moment(response):
                    self.emergence_moments.append({
                        "round": round_num,
                        "speaker": agent_name,
                        "content": response
                    })
                    print("✨ [涌现时刻] 检测到新想法或突破性观点！\n")

                # 短暂停顿（模拟思考）
                await asyncio.sleep(0.5)

        # 总结
        summary = await self._generate_summary(task)

        return {
            "task": task,
            "discussion": self.discussion,
            "emergence_moments": self.emergence_moments,
            "summary": summary,
            "total_rounds": rounds
        }

    def _detect_emergence_moment(self, content: str) -> bool:
        """简单的涌现检测（基于关键词）"""
        emergence_keywords = [
            "新想法", "突然想到", "更好的方案", "结合",
            "创新", "改进", "优化", "综合", "突破",
            "换个角度", "重新考虑", "发现", "启发"
        ]

        return any(keyword in content for keyword in emergence_keywords)

    async def _generate_summary(self, task: str) -> str:
        """生成讨论总结"""
        discussion_text = "\n\n".join([str(msg) for msg in self.discussion])

        prompt = f"""请总结以下多角色讨论，提炼出：
1. 最终达成的方案
2. 关键的突破性想法
3. 协作产生的价值（1+1>2的地方）

任务：{task}

讨论记录：
{discussion_text}

请用150字内总结。"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是讨论总结专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )

            return response.choices[0].message.content.strip()
        except:
            return "总结生成失败"

    def print_report(self, result: Dict):
        """打印报告"""
        print("\n" + "=" * 60)
        print("📊 讨论报告")
        print("=" * 60)

        print(f"\n🎯 任务：{result['task']}")
        print(f"📝 轮次：{result['total_rounds']}")
        print(f"💬 发言：{len(result['discussion'])} 条")
        print(f"✨ 涌现时刻：{len(result['emergence_moments'])} 次")

        if result['emergence_moments']:
            print("\n🌟 涌现时刻详情：")
            for i, moment in enumerate(result['emergence_moments'], 1):
                print(f"{i}. 第{moment['round']}轮 - {moment['speaker']}:")
                print(f"   {moment['content'][:80]}...")

        print(f"\n📋 总结：")
        print(result['summary'])
        print()


async def main():
    """主函数"""
    # 配置
    API_KEY = os.getenv("ZHIPUAI_API_KEY", "your_api_key_here")

    if API_KEY == "your_api_key_here":
        print("❌ 请先配置 ZHIPUAI_API_KEY 环境变量")
        return

    # 创建主持人
    facilitator = DiscussionFacilitator(api_key=API_KEY)

    # 测试任务
    task = "设计一个疯狂动物城主题的星球大战游戏，要求疯狂动物城元素明显"

    # 开始讨论
    result = await facilitator.facilitate_discussion(task, rounds=3)

    # 打印报告
    facilitator.print_report(result)


if __name__ == "__main__":
    # 运行示例
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       多Agent协作讨论系统 - 真涌现演示                    ║
║                                                           ║
║   通过不同角色的LLM agents讨论协作，                      ║
║   实现语义层面的智能涌现！                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")

    asyncio.run(main())
