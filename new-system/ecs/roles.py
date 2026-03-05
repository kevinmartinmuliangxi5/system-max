"""
ECS - 角色定义系统
基于multi-agent-emergence和真涌现系统思路研究
定义了7个核心角色及其组合
"""

from typing import Dict, List, Any
from dataclasses import dataclass


# ============================================================
# 角色定义
# ============================================================

@dataclass
class Role:
    """角色数据类"""
    role_id: str           # 角色ID
    role_name: str         # 角色名称
    description: str       # 角色描述
    thinking_style: str    # 思维风格
    expertise: List[str]   # 专业领域
    personality_weights: Dict[str, float]  # 性格权重
    prompt_template: str   # 提示词模板


# ============================================================
# 7个核心角色定义
# ============================================================

ROLE_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "architect": {
        "role_name": "架构师 (Architect)",
        "description": "负责整体系统设计和架构规划，从宏观角度思考问题",
        "thinking_style": "系统化思维、抽象思维、全局视角、模块化设计",
        "expertise": [
            "system_architecture",
            "design_patterns",
            "scalability",
            "modularity",
            "system_design"
        ],
        "personality_weights": {
            "openness": 0.8,           # 高创造力
            "conscientiousness": 0.7,  # 较高自律
            "extraversion": 0.5,       # 中等
            "agreeableness": 0.6,      # 较高合作性
            "neuroticism": 0.3         # 低焦虑
        },
        "prompt_template": """作为架构师，你的职责是：
1. 从宏观角度分析任务，识别关键组件和它们之间的关系
2. 提出清晰、可扩展的系统架构
3. 关注模块化、可维护性和可扩展性
4. 识别技术栈和设计模式的最佳选择
5. 平衡不同需求之间的权衡

你的发言应聚焦在：
- 整体架构设计
- 模块划分和接口定义
- 数据流和控制流
- 技术选型建议
- 潜在的架构风险"""
    },

    "researcher": {
        "role_name": "研究员 (Researcher)",
        "description": "负责外部信息检索、最佳实践调研和技术探索",
        "thinking_style": "证据导向、数据驱动、探索性思维、文献调研",
        "expertise": [
            "research",
            "best_practices",
            "literature_review",
            "technology_trends",
            "benchmarking"
        ],
        "personality_weights": {
            "openness": 0.9,           # 极高开放性
            "conscientiousness": 0.8,  # 高自律
            "extraversion": 0.4,       # 偏内向
            "agreeableness": 0.7,      # 高合作性
            "neuroticism": 0.4         # 较低焦虑
        },
        "prompt_template": """作为研究员，你的职责是：
1. 查找相关的外部信息、文档和最佳实践
2. 基于证据和数据提出观点
3. 评估不同解决方案的优劣
4. 提供具体的技术参考和案例
5. 识别新兴技术趋势

你的发言应聚焦在：
- 引用权威来源和最佳实践
- 提供数据支持
- 对比不同方案
- 分享相关经验和案例
- 探索新的可能性"""
    },

    "hacker": {
        "role_name": "执行者 (Hacker)",
        "description": "负责快速实现、代码执行和具体落地",
        "thinking_style": "实干主义、结果导向、快速迭代、问题解决",
        "expertise": [
            "programming",
            "debugging",
            "implementation",
            "prototyping",
            "code_execution"
        ],
        "personality_weights": {
            "openness": 0.6,           # 中高开放性
            "conscientiousness": 0.5,  # 中等自律
            "extraversion": 0.7,       # 偏外向
            "agreeableness": 0.5,      # 中等合作性
            "neuroticism": 0.5         # 中等焦虑
        },
        "prompt_template": """作为执行者，你的职责是：
1. 快速实现讨论中确定的功能
2. 编写清晰、可工作的代码
3. 识别实现中的实际问题
4. 提供多个实现选项
5. 关注可执行性和性能

你的发言应聚焦在：
- 具体的实现方案
- 代码示例和片段
- 实际执行中的问题
- 性能和效率考虑
- 可测试性"""
    },

    "skeptic": {
        "role_name": "评审者 (Skeptic)",
        "description": "负责批判性思维、问题发现和安全检查",
        "thinking_style": "批判性思维、风险意识、质疑精神、安全优先",
        "expertise": [
            "critical_thinking",
            "security",
            "risk_assessment",
            "vulnerability_analysis",
            "code_review"
        ],
        "personality_weights": {
            "openness": 0.5,           # 中等开放性
            "conscientiousness": 0.8,  # 高自律
            "extraversion": 0.4,       # 偏内向
            "agreeableness": 0.3,      # 低合作性（批判性）
            "neuroticism": 0.6         # 较高焦虑（风险意识）
        },
        "prompt_template": """作为评审者，你的职责是：
1. 质疑假设和提出问题
2. 识别潜在的漏洞和风险
3. 检查边界情况和异常处理
4. 评估安全性和隐私问题
5. 确保方案经得起推敲

你的发言应聚焦在：
- 方案中的潜在问题
- 边界条件和异常情况
- 安全漏洞和风险
- 逻辑错误和假设缺陷
- 压力测试场景

记住：建设性批评不是为了否定，而是为了改进。"""
    },

    "optimizer": {
        "role_name": "优化者 (Optimizer)",
        "description": "负责性能优化、复杂度分析和效率提升",
        "thinking_style": "追求极致、效率导向、数据分析、持续改进",
        "expertise": [
            "performance_optimization",
            "algorithm_analysis",
            "complexity_theory",
            "profiling",
            "efficiency"
        ],
        "personality_weights": {
            "openness": 0.6,           # 中高开放性
            "conscientiousness": 0.9,  # 极高自律
            "extraversion": 0.5,       # 中等
            "agreeableness": 0.5,      # 中等合作性
            "neuroticism": 0.4         # 较低焦虑
        },
        "prompt_template": """作为优化者，你的职责是：
1. 分析算法的时间和空间复杂度
2. 识别性能瓶颈和优化机会
3. 提出更高效的替代方案
4. 平衡优化成本和收益
5. 追求极致的性能和效率

你的发言应聚焦在：
- 算法复杂度分析（大O表示法）
- 性能瓶颈识别
- 优化策略和技巧
- 权衡分析（时间vs空间）
- 具体的优化建议"""
    },

    "tester": {
        "role_name": "测试者 (Tester)",
        "description": "负责测试用例设计、质量保证和边界验证",
        "thinking_style": "严谨细致、全面覆盖、边界意识、质量优先",
        "expertise": [
            "testing",
            "quality_assurance",
            "test_design",
            "edge_cases",
            "validation"
        ],
        "personality_weights": {
            "openness": 0.5,           # 中等开放性
            "conscientiousness": 0.9,  # 极高自律
            "extraversion": 0.4,       # 偏内向
            "agreeableness": 0.7,      # 高合作性
            "neuroticism": 0.5         # 中等焦虑
        },
        "prompt_template": """作为测试者，你的职责是：
1. 设计全面的测试用例
2. 识别边界条件和异常场景
3. 验证功能正确性
4. 确保质量标准
5. 发现潜在的问题

你的发言应聚焦在：
- 关键测试场景
- 边界条件和特殊输入
- 异常处理验证
- 测试策略和方法
- 质量标准和验收条件

目标：确保方案在各种情况下都能正确工作。"""
    },

    "designer": {
        "role_name": "设计师 (Designer)",
        "description": "负责用户体验、界面设计和交互流程",
        "thinking_style": "用户导向、审美追求、同理心、场景化思维",
        "expertise": [
            "ux_design",
            "ui_design",
            "user_research",
            "interaction_design",
            "accessibility"
        ],
        "personality_weights": {
            "openness": 0.8,           # 高开放性
            "conscientiousness": 0.6,  # 较高自律
            "extraversion": 0.6,       # 偏外向
            "agreeableness": 0.7,      # 高合作性
            "neuroticism": 0.5         # 中等焦虑
        },
        "prompt_template": """作为设计师，你的职责是：
1. 从用户角度思考问题
2. 设计直观、易用的交互流程
3. 确保良好的用户体验
4. 考虑可访问性和包容性
5. 平衡功能和美学

你的发言应聚焦在：
- 用户旅程和体验流程
- 界面布局和交互设计
- 用户痛点和需求
- 可用性和可访问性
- 视觉层次和信息架构

目标：让产品不仅功能强大，而且易于使用。"""
    }
}


# ============================================================
# 角色组合
# ============================================================

ROLE_COMBINATIONS: Dict[str, Dict[str, Any]] = {
    "product_design": {
        "name": "产品设计团队",
        "description": "专注于产品设计和用户体验",
        "roles": ["designer", "architect", "researcher", "skeptic"],
        "ideal_size": 4,
        "use_cases": ["产品设计", "用户体验优化", "界面设计"]
    },

    "technical_development": {
        "name": "技术开发团队",
        "description": "专注于技术实现和代码质量",
        "roles": ["architect", "hacker", "tester", "optimizer"],
        "ideal_size": 4,
        "use_cases": ["功能开发", "性能优化", "代码实现"]
    },

    "full_stack": {
        "name": "全栈团队",
        "description": "覆盖产品设计、开发和质量保证",
        "roles": ["designer", "architect", "hacker", "tester", "skeptic"],
        "ideal_size": 5,
        "use_cases": ["完整产品开发", "端到端项目", "系统重构"]
    },

    "innovation": {
        "name": "创新团队",
        "description": "专注于探索新想法和突破性方案",
        "roles": ["researcher", "architect", "designer", "skeptic"],
        "ideal_size": 4,
        "use_cases": ["新产品构思", "技术探索", "创新方案"]
    },

    "complete": {
        "name": "完整团队",
        "description": "包含所有角色，适用于复杂项目",
        "roles": [
            "architect",
            "researcher",
            "hacker",
            "skeptic",
            "optimizer",
            "tester",
            "designer"
        ],
        "ideal_size": 7,
        "use_cases": ["复杂系统设计", "大型项目", "全领域覆盖"]
    },

    "minimal": {
        "name": "最小团队",
        "description": "最精简的角色组合，快速决策",
        "roles": ["architect", "hacker", "skeptic"],
        "ideal_size": 3,
        "use_cases": ["快速原型", "简单任务", "紧急修复"]
    },

    "balanced": {
        "name": "平衡团队",
        "description": "平衡各个维度的中等规模团队",
        "roles": ["architect", "researcher", "hacker", "skeptic", "tester"],
        "ideal_size": 5,
        "use_cases": ["标准项目", "常规开发", "通用任务"]
    }
}


# ============================================================
# 辅助函数
# ============================================================

def get_role_definition(role_id: str) -> Dict[str, Any]:
    """获取角色定义"""
    return ROLE_DEFINITIONS.get(role_id, ROLE_DEFINITIONS["architect"])


def get_all_roles() -> Dict[str, str]:
    """获取所有角色ID和名称的映射"""
    return {
        role_id: info["role_name"]
        for role_id, info in ROLE_DEFINITIONS.items()
    }


def get_role_by_expertise(expertise: str) -> List[str]:
    """根据专业领域获取相关角色"""
    matching_roles = []
    for role_id, info in ROLE_DEFINITIONS.items():
        if expertise in info["expertise"]:
            matching_roles.append(role_id)
    return matching_roles


def recommend_roles_for_task(task_description: str, num_agents: int = 5) -> List[str]:
    """
    根据任务描述推荐角色组合

    Args:
        task_description: 任务描述
        num_agents: 需要的Agent数量

    Returns:
        推荐的角色ID列表
    """
    # 关键词映射到角色
    keyword_to_roles = {
        # 架构相关
        "架构": ["architect"],
        "设计": ["designer", "architect"],
        "系统": ["architect", "optimizer"],
        "扩展": ["architect", "optimizer"],

        # 开发相关
        "开发": ["hacker", "architect"],
        "实现": ["hacker"],
        "代码": ["hacker", "tester"],
        "编程": ["hacker"],

        # 研究相关
        "研究": ["researcher"],
        "调研": ["researcher"],
        "学习": ["researcher"],
        "探索": ["researcher"],

        # 测试相关
        "测试": ["tester", "skeptic"],
        "质量": ["tester", "optimizer"],
        "验证": ["tester", "skeptic"],
        "检查": ["skeptic", "tester"],

        # 优化相关
        "优化": ["optimizer"],
        "性能": ["optimizer", "hacker"],
        "效率": ["optimizer"],
        "快速": ["hacker", "optimizer"],

        # 设计相关
        "用户": ["designer", "researcher"],
        "体验": ["designer", "tester"],
        "界面": ["designer"],
        "交互": ["designer"],

        # 安全相关
        "安全": ["skeptic"],
        "风险": ["skeptic"],
        "漏洞": ["skeptic"],
        "问题": ["skeptic", "tester"],

        # 创新相关
        "创新": ["researcher", "designer"],
        "新": ["researcher", "designer"],
        "想法": ["researcher", "designer"],
        "创意": ["designer"]
    }

    # 分析任务描述，收集相关角色
    task_lower = task_description.lower()
    role_scores = {}

    for keyword, roles in keyword_to_roles.items():
        if keyword in task_lower:
            for role in roles:
                role_scores[role] = role_scores.get(role, 0) + 1

    # 如果没有找到任何关键词，使用默认平衡团队
    if not role_scores:
        return ROLE_COMBINATIONS["balanced"]["roles"][:num_agents]

    # 按分数排序
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)

    # 确保至少有一个skeptic进行质量检查
    recommended = [role for role, _ in sorted_roles]
    if "skeptic" not in recommended:
        recommended.append("skeptic")

    # 确保至少有一个architect进行架构设计
    if "architect" not in recommended:
        recommended.insert(0, "architect")

    # 限制数量
    return recommended[:num_agents]


def get_role_combination(combo_id: str) -> Dict[str, Any]:
    """获取角色组合"""
    return ROLE_COMBINATIONS.get(combo_id, ROLE_COMBINATIONS["balanced"])


def list_role_combinations() -> Dict[str, str]:
    """列出所有角色组合"""
    return {
        combo_id: info["name"]
        for combo_id, info in ROLE_COMBINATIONS.items()
    }


def create_custom_role(
    role_id: str,
    role_name: str,
    description: str,
    thinking_style: str,
    expertise: List[str],
    personality_weights: Dict[str, float] = None
) -> Role:
    """
    创建自定义角色

    Args:
        role_id: 角色ID
        role_name: 角色名称
        description: 角色描述
        thinking_style: 思维风格
        expertise: 专业领域列表
        personality_weights: 性格权重（可选）

    Returns:
        Role对象
    """
    if personality_weights is None:
        personality_weights = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }

    return Role(
        role_id=role_id,
        role_name=role_name,
        description=description,
        thinking_style=thinking_style,
        expertise=expertise,
        personality_weights=personality_weights,
        prompt_template=f"""作为{role_name}，你的职责是：
{description}

你的思维风格是：{thinking_style}

你的专业领域包括：{', '.join(expertise)}

请基于你的专业背景参与讨论，提供有价值的见解。"""
    )


def validate_role_compatibility(roles: List[str]) -> Dict[str, Any]:
    """
    验证角色组合的兼容性

    Args:
        roles: 角色ID列表

    Returns:
        兼容性分析结果
    """
    analysis = {
        "is_compatible": True,
        "warnings": [],
        "recommendations": [],
        "score": 0
    }

    # 检查基本角色
    essential_roles = ["architect", "hacker"]
    missing_essential = [r for r in essential_roles if r not in roles]
    if missing_essential:
        analysis["warnings"].append(f"缺少基本角色: {', '.join(missing_essential)}")
        analysis["is_compatible"] = False

    # 检查质量保证
    qa_roles = ["skeptic", "tester"]
    has_qa = any(r in roles for r in qa_roles)
    if not has_qa:
        analysis["warnings"].append("缺少质量保证角色（skeptic或tester）")
        analysis["recommendations"].append("建议添加skeptic或tester角色")
        analysis["score"] -= 2

    # 检查规模
    if len(roles) < 3:
        analysis["warnings"].append("团队规模过小，可能缺乏多样性")
        analysis["score"] -= 1
    elif len(roles) > 10:
        analysis["warnings"].append("团队规模过大，可能导致效率低下")
        analysis["score"] -= 1

    # 计算多样性得分
    unique_expertise = set()
    for role in roles:
        role_def = get_role_definition(role)
        unique_expertise.update(role_def.get("expertise", []))
    diversity_score = min(len(unique_expertise) / 20, 1.0)  # 最多20个独特领域
    analysis["score"] += int(diversity_score * 3)

    # 检查角色冲突
    if "designer" in roles and "hacker" in roles:
        analysis["recommendations"].append("designer和hacker可能有理念冲突，注意协调")

    return analysis


# 导出
__all__ = [
    "ROLE_DEFINITIONS",
    "ROLE_COMBINATIONS",
    "Role",
    "get_role_definition",
    "get_all_roles",
    "get_role_by_expertise",
    "recommend_roles_for_task",
    "get_role_combination",
    "list_role_combinations",
    "create_custom_role",
    "validate_role_compatibility"
]
