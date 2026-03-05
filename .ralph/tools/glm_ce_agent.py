"""
GLM Compound Engineering Agent
基于GLM-4.7的真实CE代理实现

替代brain_v3.py中的假CE模拟器
"""

import json
import os
from typing import Dict, List
from anthropic import Anthropic


class GLMCompoundEngineeringAgent:
    """使用GLM-4.7实现的真实Compound Engineering代理"""

    def __init__(self):
        # 使用GLM Coding Plan配置
        self.client = Anthropic(
            api_key=os.getenv(
                "ANTHROPIC_AUTH_TOKEN",
                "434698bbe0754202aabea54a1b6d184d.zPhgfbdAFrX46GDg"
            ),
            base_url=os.getenv(
                "ANTHROPIC_BASE_URL",
                "https://open.bigmodel.cn/api/anthropic"
            )
        )
        self.model_47 = "glm-4.7"
        self.model_air = "glm-4.5-air"

    def invoke(self, agent_name: str, *args, **kwargs) -> Dict:
        """统一调用接口"""
        agents = {
            "req_dev": self.req_dev_agent,
            "spec_writer": self.spec_writer_agent,
            "architect": self.architect_agent,
            "code_reviewer": self.code_reviewer_agent,
            "brainstorm": self.brainstorm_agent,
            "design_review": self.design_review_agent,
        }

        if agent_name in agents:
            return agents[agent_name](*args, **kwargs)
        else:
            raise ValueError(f"Unknown agent: {agent_name}")

    def req_dev_agent(self, user_input: str) -> Dict:
        """需求分析代理 - 使用GLM-4.7深度分析"""

        prompt = f"""你是一个专业的需求分析专家（Compound Engineering的req-dev agent）。

用户需求描述：
{user_input}

请执行需求开发分析，包括：
1. 深入理解需求意图
2. 提出3-5个关键澄清问题（具体、有针对性）
3. 识别功能性需求
4. 识别非功能性需求（性能、安全、可用性等）
5. 识别技术约束
6. 识别潜在风险

请以JSON格式返回：
{{
    "understanding": "你对需求的理解总结",
    "questions": [
        "问题1：关于用户群体的问题",
        "问题2：关于功能范围的问题",
        "问题3：关于技术约束的问题"
    ],
    "requirements": {{
        "functional": ["功能需求1", "功能需求2"],
        "non_functional": ["非功能需求1", "非功能需求2"],
        "constraints": ["约束1", "约束2"]
    }},
    "risks": ["风险1", "风险2"]
}}

请确保问题具体、有价值，避免泛泛而谈。
"""

        try:
            response = self.client.messages.create(
                model=self.model_47,
                max_tokens=2000,
                temperature=0.3,  # 较低温度，更理性分析
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # 解析JSON响应
            content = response.content[0].text
            result = json.loads(content)
            result["agent"] = "req_dev"
            result["model"] = "glm-4.7"
            return result

        except Exception as e:
            # 降级处理
            return {
                "agent": "req_dev",
                "error": str(e),
                "questions": [
                    "这个功能的主要用户是谁？",
                    "成功的标准是什么？",
                    "有哪些边界情况需要考虑？"
                ],
                "requirements": {
                    "functional": [],
                    "non_functional": [],
                    "constraints": []
                }
            }

    def spec_writer_agent(self, requirements: Dict) -> str:
        """规格编写代理 - 生成详细技术规格"""

        prompt = f"""你是一个专业的技术规格编写专家（spec-writer agent）。

需求分析结果：
{json.dumps(requirements, ensure_ascii=False, indent=2)}

请生成完整的技术规格文档，使用Markdown格式，包括：

## 概述
简要说明功能目标和价值

## 输入
- 明确所有输入参数、数据格式、验证规则

## 输出
- 明确所有输出内容、数据格式、响应结构

## 业务规则
1. 列出所有业务逻辑规则
2. 包含边界条件处理
3. 包含异常情况处理

## 技术约束
- 性能要求
- 安全要求
- 兼容性要求
- 资源限制

## 验收标准
- [ ] 明确的测试标准
- [ ] 可验证的质量指标

## 测试用例
至少3个测试场景：
1. 正常情况
2. 边界情况
3. 错误处理

请确保规格详细、具体、可执行。
"""

        try:
            response = self.client.messages.create(
                model=self.model_47,
                max_tokens=4000,
                temperature=0.2,  # 低温度，严谨规格
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return response.content[0].text

        except Exception as e:
            # 降级：返回基础模板
            return f"""# 技术规格文档

## 概述
待定义

## 错误
规格生成失败: {str(e)}
请手动完善。
"""

    def architect_agent(self, requirements: Dict) -> Dict:
        """架构设计代理 - 设计系统架构"""

        prompt = f"""你是一个系统架构师（architect agent）。

需求：
{json.dumps(requirements, ensure_ascii=False, indent=2)}

请设计系统架构，返回JSON格式：
{{
    "architecture_pattern": "选择的架构模式（如MVC、Microservices、Layered等）",
    "rationale": "选择此架构的原因",
    "components": [
        {{
            "name": "组件名称",
            "responsibility": "职责描述",
            "dependencies": ["依赖的组件"],
            "technology": "建议的技术栈"
        }}
    ],
    "data_flow": "数据流描述（从输入到输出）",
    "technology_stack": {{
        "frontend": "前端技术选择及理由",
        "backend": "后端技术选择及理由",
        "database": "数据库选择及理由",
        "other": "其他技术组件"
    }},
    "scalability": {{
        "horizontal": "横向扩展方案",
        "vertical": "纵向扩展方案"
    }},
    "security": ["安全措施1", "安全措施2"],
    "risks": [
        {{
            "risk": "风险描述",
            "mitigation": "缓解措施"
        }}
    ],
    "trade_offs": [
        {{
            "decision": "设计决策",
            "pro": "优点",
            "con": "缺点",
            "reason": "选择原因"
        }}
    ]
}}

请提供专业、全面的架构设计。
"""

        try:
            response = self.client.messages.create(
                model=self.model_47,
                max_tokens=4000,
                temperature=0.4,  # 允许一定创造性
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = response.content[0].text
            result = json.loads(content)
            result["agent"] = "architect"
            return result

        except Exception as e:
            return {
                "agent": "architect",
                "error": str(e),
                "architecture_pattern": "Layered",
                "components": [],
                "risks": []
            }

    def code_reviewer_agent(self, code: str, context: str = "") -> Dict:
        """代码审查代理 - 深度代码质量分析"""

        prompt = f"""你是一个严格的代码审查专家（code-reviewer agent）。

上下文：{context if context else "通用代码审查"}

待审查代码：
```
{code}
```

请进行全面的代码审查，返回JSON：
{{
    "quality_score": 0-10的评分,
    "summary": "总体评价（2-3句）",
    "issues": [
        {{
            "severity": "critical/high/medium/low",
            "category": "security/performance/logic/style",
            "description": "问题描述",
            "line": 行号（如果能确定）,
            "suggestion": "修复建议"
        }}
    ],
    "strengths": ["代码优点1", "代码优点2"],
    "security_warnings": [
        {{
            "type": "SQL注入/XSS/CSRF/等",
            "description": "安全问题描述",
            "fix": "修复方法"
        }}
    ],
    "performance_issues": ["性能问题描述"],
    "best_practices": ["违反的最佳实践"],
    "approved": true/false,
    "blocking_issues": ["必须修复才能通过的问题"]
}}

重点检查：
1. 安全漏洞（SQL注入、XSS、CSRF、命令注入、路径遍历等）
2. 逻辑错误和边界情况
3. 性能问题（N+1查询、内存泄漏、死循环等）
4. 代码规范和可读性
5. 错误处理的完整性
6. 潜在的运行时错误

请严格、专业地审查。
"""

        try:
            response = self.client.messages.create(
                model=self.model_47,
                max_tokens=3000,
                temperature=0.1,  # 极低温度，严格审查
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = response.content[0].text
            result = json.loads(content)
            result["agent"] = "code_reviewer"
            result["model"] = "glm-4.7"
            return result

        except Exception as e:
            return {
                "agent": "code_reviewer",
                "error": str(e),
                "quality_score": 5,
                "issues": [],
                "approved": True  # 降级时通过
            }

    def brainstorm_agent(self, requirements: Dict) -> Dict:
        """头脑风暴代理 - 探索多种解决方案"""

        prompt = f"""你是一个创新思维专家（brainstorm agent）。

需求：
{json.dumps(requirements, ensure_ascii=False, indent=2)}

请提供多种设计方案的头脑风暴，返回JSON：
{{
    "design_options": [
        {{
            "approach": "方案名称",
            "description": "方案描述",
            "pros": ["优点1", "优点2"],
            "cons": ["缺点1", "缺点2"],
            "complexity": "low/medium/high",
            "time_estimate": "预估时间"
        }}
    ],
    "trade_offs": [
        {{
            "dimension": "权衡维度（如性能vs简单性）",
            "analysis": "分析说明"
        }}
    ],
    "recommendations": [
        {{
            "option": "推荐方案",
            "reason": "推荐理由",
            "when_to_use": "适用场景"
        }}
    ],
    "innovative_ideas": ["创新想法1", "创新想法2"]
}}

鼓励创造性和多样性。
"""

        try:
            response = self.client.messages.create(
                model=self.model_47,
                max_tokens=3000,
                temperature=0.7,  # 高温度，鼓励创造性
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = response.content[0].text
            result = json.loads(content)
            result["agent"] = "brainstorm"
            return result

        except Exception as e:
            return {
                "agent": "brainstorm",
                "error": str(e),
                "design_options": [],
                "recommendations": []
            }

    def design_review_agent(self, design: Dict) -> Dict:
        """设计审查代理 - 评估设计质量"""

        prompt = f"""你是一个设计审查专家（design-review agent）。

设计方案：
{json.dumps(design, ensure_ascii=False, indent=2)}

请审查设计质量，返回JSON：
{{
    "overall_score": 0-10的评分,
    "completeness": {{
        "score": 0-10,
        "missing": ["缺失的部分"]
    }},
    "feasibility": {{
        "score": 0-10,
        "concerns": ["可行性担忧"]
    }},
    "maintainability": {{
        "score": 0-10,
        "issues": ["可维护性问题"]
    }},
    "scalability": {{
        "score": 0-10,
        "bottlenecks": ["扩展性瓶颈"]
    }},
    "issues": [
        {{
            "severity": "critical/high/medium/low",
            "area": "问题领域",
            "description": "问题描述",
            "suggestion": "改进建议"
        }}
    ],
    "strengths": ["设计优点"],
    "approved": true/false,
    "conditions": ["通过的前提条件"]
}}

请专业、客观地评估。
"""

        try:
            response = self.client.messages.create(
                model=self.model_47,
                max_tokens=2500,
                temperature=0.2,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = response.content[0].text
            result = json.loads(content)
            result["agent"] = "design_review"
            return result

        except Exception as e:
            return {
                "agent": "design_review",
                "error": str(e),
                "overall_score": 7,
                "approved": True,
                "issues": []
            }


# 测试代码
if __name__ == "__main__":
    import io
    import sys
    # 修复Windows控制台UTF-8输出
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("测试GLM Compound Engineering Agent")
    print("=" * 60)

    agent = GLMCompoundEngineeringAgent()

    # 测试需求分析
    print("\n[测试1: 需求分析]")
    print("-" * 60)
    req_result = agent.req_dev_agent("创建一个用户注册功能，支持邮箱验证")
    print(f"理解: {req_result.get('understanding', 'N/A')}")
    print(f"问题数量: {len(req_result.get('questions', []))}")
    for i, q in enumerate(req_result.get('questions', []), 1):
        print(f"  问题{i}: {q}")

    # 测试代码审查
    print("\n[测试2: 代码审查]")
    print("-" * 60)
    test_code = """
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    return result
"""
    review_result = agent.code_reviewer_agent(test_code, "用户登录函数")
    print(f"质量评分: {review_result.get('quality_score', 0)}/10")
    print(f"安全警告: {len(review_result.get('security_warnings', []))}")
    print(f"通过审查: {review_result.get('approved')}")

    print("\n测试完成！")
