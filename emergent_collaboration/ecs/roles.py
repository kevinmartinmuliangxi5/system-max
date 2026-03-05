"""
ECS - 预定义角色模块

提供常用的Agent角色定义
"""

from .agent import AgentRole, Expertise, ThinkingStyle


# 预定义的专业领域
EXPERTISE_DOMAINS = {
    # 技术类
    "software_architecture": Expertise(
        domain="软件架构",
        skills=["系统设计", "技术选型", "可扩展性", "性能优化"],
        experience_level=0.8
    ),
    "frontend_development": Expertise(
        domain="前端开发",
        skills=["React", "Vue", "CSS", "用户体验", "响应式设计"],
        experience_level=0.7
    ),
    "backend_development": Expertise(
        domain="后端开发",
        skills=["API设计", "数据库", "服务器架构", "安全性"],
        experience_level=0.7
    ),
    "devops": Expertise(
        domain="运维工程",
        skills=["CI/CD", "容器化", "云服务", "监控"],
        experience_level=0.7
    ),
    "data_science": Expertise(
        domain="数据科学",
        skills=["机器学习", "统计分析", "数据可视化", "预测建模"],
        experience_level=0.8
    ),
    "security": Expertise(
        domain="信息安全",
        skills=["渗透测试", "加密", "安全审计", "合规"],
        experience_level=0.8
    ),

    # 产品类
    "product_management": Expertise(
        domain="产品管理",
        skills=["需求分析", "优先级管理", "MVP规划", "用户调研"],
        experience_level=0.8
    ),
    "ux_design": Expertise(
        domain="用户体验设计",
        skills=["用户研究", "交互设计", "原型设计", "可用性测试"],
        experience_level=0.8
    ),
    "ui_design": Expertise(
        domain="用户界面设计",
        skills=["视觉设计", "设计系统", "品牌", "动效"],
        experience_level=0.7
    ),
    "content_strategy": Expertise(
        domain="内容策略",
        skills=["内容规划", "文案写作", "品牌传播", "SEO"],
        experience_level=0.6
    ),

    # 商业类
    "business_strategy": Expertise(
        domain="商业策略",
        skills=["市场分析", "竞争策略", "商业模式", "财务规划"],
        experience_level=0.8
    ),
    "marketing": Expertise(
        domain="市场营销",
        skills=["品牌营销", "数字营销", "增长策略", "用户获取"],
        experience_level=0.7
    ),
    "sales": Expertise(
        domain="销售",
        skills=["客户关系", "谈判", "渠道管理", "成交技巧"],
        experience_level=0.7
    ),

    # 运营类
    "operations": Expertise(
        domain="运营管理",
        skills=["流程优化", "效率提升", "资源管理", "质量控制"],
        experience_level=0.7
    ),
    "customer_success": Expertise(
        domain="客户成功",
        skills=["客户支持", "用户留存", "成功案例", "满意度管理"],
        experience_level=0.7
    ),
    "community_management": Expertise(
        domain="社区管理",
        skills=["社群运营", "用户增长", "活动策划", "危机公关"],
        experience_level=0.6
    ),

    # 创意类
    "creative_direction": Expertise(
        domain="创意总监",
        skills=["创意概念", "品牌故事", "视觉策略", "创新思维"],
        experience_level=0.9
    ),
    "copywriting": Expertise(
        domain="文案创作",
        skills=["品牌文案", "广告语", "内容创作", "故事叙述"],
        experience_level=0.7
    ),

    # 研究类
    "user_research": Expertise(
        domain="用户研究",
        skills=["用户访谈", "问卷调查", "行为分析", "洞察提取"],
        experience_level=0.8
    ),
    "market_research": Expertise(
        domain="市场研究",
        skills=["市场分析", "竞品分析", "趋势预测", "数据解读"],
        experience_level=0.8
    ),
    "competitive_intelligence": Expertise(
        domain="竞争情报",
        skills=["竞品分析", "情报收集", "策略预警", "SWOT分析"],
        experience_level=0.7
    ),

    # 质量类
    "quality_assurance": Expertise(
        domain="质量保证",
        skills=["测试策略", "自动化测试", "性能测试", "bug追踪"],
        experience_level=0.7
    ),
    "code_review": Expertise(
        domain="代码审查",
        skills=["代码质量", "最佳实践", "重构", "技术债管理"],
        experience_level=0.8
    ),
}


# 预定义的角色模板
PREDEFINED_ROLES = {
    "technical_architect": AgentRole(
        id="technical_architect",
        name="技术架构师",
        description="专注于系统架构设计和技术决策，关注可行性、性能、可扩展性和安全性。",
        thinking_style=ThinkingStyle.ANALYTICAL,
        expertise=[EXPERTISE_DOMAINS["software_architecture"],
                   EXPERTISE_DOMAINS["backend_development"]],
        system_prompt_template="",
        focus_areas=["技术可行性", "系统架构", "技术选型", "性能优化", "安全考虑"]
    ),

    "product_manager": AgentRole(
        id="product_manager",
        name="产品经理",
        description="关注用户价值、产品定位和市场需求，确保产品解决真实问题。",
        thinking_style=ThinkingStyle.INTEGRATIVE,
        expertise=[EXPERTISE_DOMAINS["product_management"],
                   EXPERTISE_DOMAINS["user_research"]],
        system_prompt_template="",
        focus_areas=["用户需求", "产品定位", "功能优先级", "用户体验", "商业价值"]
    ),

    "ux_designer": AgentRole(
        id="ux_designer",
        name="UX设计师",
        description="专注于用户体验和交互设计，确保产品易用、流畅、令人愉悦。",
        thinking_style=ThinkingStyle.EMPATHETIC,
        expertise=[EXPERTISE_DOMAINS["ux_design"],
                   EXPERTISE_DOMAINS["user_research"]],
        system_prompt_template="",
        focus_areas=["用户体验", "交互流程", "可用性", "情感化设计", "无障碍设计"]
    ),

    "ui_designer": AgentRole(
        id="ui_designer",
        name="UI设计师",
        description="专注于视觉设计和界面美学，创造美观、一致的视觉体验。",
        thinking_style=ThinkingStyle.CREATIVE,
        expertise=[EXPERTISE_DOMAINS["ui_design"]],
        system_prompt_template="",
        focus_areas=["视觉风格", "设计系统", "品牌一致性", "细节打磨", "动效设计"]
    ),

    "software_engineer": AgentRole(
        id="software_engineer",
        name="软件工程师",
        description="专注于代码实现和技术落地，关注代码质量、可维护性和开发效率。",
        thinking_style=ThinkingStyle.PRACTICAL,
        expertise=[EXPERTISE_DOMAINS["backend_development"],
                   EXPERTISE_DOMAINS["frontend_development"]],
        system_prompt_template="",
        focus_areas=["代码实现", "技术实现", "开发效率", "代码质量", "测试"]
    ),

    "qa_engineer": AgentRole(
        id="qa_engineer",
        name="QA工程师",
        description="专注于质量保证和测试，从用户角度发现问题和潜在风险。",
        thinking_style=ThinkingStyle.CRITICAL,
        expertise=[EXPERTISE_DOMAINS["quality_assurance"],
                   EXPERTISE_DOMAINS["code_review"]],
        system_prompt_template="",
        focus_areas=["测试策略", "边界情况", "用户体验bug", "性能瓶颈", "安全漏洞"]
    ),

    "data_analyst": AgentRole(
        id="data_analyst",
        name="数据分析师",
        description="基于数据进行决策分析，关注量化指标、效果评估和数据驱动优化。",
        thinking_style=ThinkingStyle.ANALYTICAL,
        expertise=[EXPERTISE_DOMAINS["data_science"],
                   EXPERTISE_DOMAINS["market_research"]],
        system_prompt_template="",
        focus_areas=["数据指标", "A/B测试", "用户行为分析", "效果评估", "预测模型"]
    ),

    "creative_director": AgentRole(
        id="creative_director",
        name="创意总监",
        description="提供突破性的创意想法，寻找与众不同的解决方案。",
        thinking_style=ThinkingStyle.CREATIVE,
        expertise=[EXPERTISE_DOMAINS["creative_direction"],
                   EXPERTISE_DOMAINS["content_strategy"]],
        system_prompt_template="",
        focus_areas=["创意概念", "品牌故事", "情感共鸣", "创新突破", "文化洞察"]
    ),

    "business_strategist": AgentRole(
        id="business_strategist",
        name="商业策略师",
        description="关注商业模式、市场竞争和盈利策略，确保产品具有商业价值。",
        thinking_style=ThinkingStyle.ANALYTICAL,
        expertise=[EXPERTISE_DOMAINS["business_strategy"],
                   EXPERTISE_DOMAINS["competitive_intelligence"]],
        system_prompt_template="",
        focus_areas=["商业模式", "市场定位", "竞争优势", "盈利策略", "增长策略"]
    ),

    "user_researcher": AgentRole(
        id="user_researcher",
        name="用户研究员",
        description="深入理解用户需求和行为模式，发现用户的显性和隐性需求。",
        thinking_style=ThinkingStyle.EMPATHETIC,
        expertise=[EXPERTISE_DOMAINS["user_research"],
                   EXPERTISE_DOMAINS["market_research"]],
        system_prompt_template="",
        focus_areas=["用户画像", "使用场景", "痛点分析", "需求挖掘", "行为观察"]
    ),

    "operations_manager": AgentRole(
        id="operations_manager",
        name="运营经理",
        description="关注资源效率、流程优化和执行可行性，确保方案可以落地。",
        thinking_style=ThinkingStyle.PRACTICAL,
        expertise=[EXPERTISE_DOMAINS["operations"],
                   EXPERTISE_DOMAINS["project_management"]],
        system_prompt_template="",
        focus_areas=["资源评估", "成本控制", "时间规划", "执行计划", "风险管理"]
    ),

    "security_expert": AgentRole(
        id="security_expert",
        name="安全专家",
        description="识别潜在的安全风险和合规问题，确保系统安全可靠。",
        thinking_style=ThinkingStyle.CRITICAL,
        expertise=[EXPERTISE_DOMAINS["security"]],
        system_prompt_template="",
        focus_areas=["安全风险", "数据保护", "合规要求", "漏洞分析", "安全策略"]
    ),
}


def get_role(role_id: str) -> AgentRole:
    """
    获取预定义角色

    Args:
        role_id: 角色ID

    Returns:
        AgentRole对象

    Raises:
        ValueError: 如果角色不存在
    """
    if role_id not in PREDEFINED_ROLES:
        available = ", ".join(PREDEFINED_ROLES.keys())
        raise ValueError(f"角色'{role_id}'不存在。可用角色：{available}")
    return PREDEFINED_ROLES[role_id]


def list_roles() -> list:
    """列出所有可用角色"""
    return list(PREDEFINED_ROLES.keys())


def get_roles_by_ids(role_ids: list) -> list:
    """
    根据ID列表获取角色

    Args:
        role_ids: 角色ID列表

    Returns:
        AgentRole对象列表
    """
    return [get_role(rid) for rid in role_ids]


# 角色组合推荐
ROLE_COMBINATIONS = {
    "product_design": {
        "name": "产品设计组",
        "roles": ["product_manager", "ux_designer", "ui_designer",
                "user_researcher", "creative_director"],
        "description": "适合产品设计和用户体验任务"
    },

    "technical_development": {
        "name": "技术开发组",
        "roles": ["technical_architect", "software_engineer", "qa_engineer",
                "security_expert", "data_analyst"],
        "description": "适合技术架构和开发任务"
    },

    "business_strategy": {
        "name": "商业策略组",
        "roles": ["business_strategist", "product_manager", "data_analyst",
                "user_researcher", "operations_manager"],
        "description": "适合商业策略和产品规划任务"
    },

    "full_stack": {
        "name": "全栈团队",
        "roles": ["technical_architect", "product_manager", "ux_designer",
                "software_engineer", "qa_engineer", "user_researcher"],
        "description": "适合端到端的完整项目"
    },

    "innovation": {
        "name": "创新小组",
        "roles": ["creative_director", "user_researcher", "data_analyst",
                "product_manager", "technical_architect"],
        "description": "适合需要突破性创新的复杂任务"
    },
}


def get_role_combination(combination_id: str) -> list:
    """
    获取角色组合

    Args:
        combination_id: 组合ID

    Returns:
        角色ID列表
    """
    if combination_id not in ROLE_COMBINATIONS:
        available = ", ".join(ROLE_COMBINATIONS.keys())
        raise ValueError(f"组合'{combination_id}'不存在。可用组合：{available}")

    return ROLE_COMBINATIONS[combination_id]["roles"]


def recommend_roles(task: str, num_agents: int = 5) -> list:
    """
    根据任务推荐角色

    Args:
        task: 任务描述
        num_agents: 需要的Agent数量

    Returns:
        推荐的角色ID列表
    """
    # 简单的关键词匹配
    task_lower = task.lower()

    # 关键词到角色的映射
    role_keywords = {
        "technical_architect": ["架构", "技术", "系统", "scalability", "性能"],
        "product_manager": ["产品", "用户", "需求", "功能", "mvp"],
        "ux_designer": ["体验", "交互", "用户", "ux", "易用"],
        "ui_designer": ["设计", "视觉", "界面", "美观", "ui"],
        "software_engineer": ["开发", "代码", "实现", "编程", "技术"],
        "qa_engineer": ["测试", "质量", "bug", "验证"],
        "data_analyst": ["数据", "分析", "指标", "统计"],
        "creative_director": ["创意", "创新", "突破", "想法"],
        "business_strategist": ["商业", "盈利", "市场", "竞争"],
        "user_researcher": ["用户", "研究", "调研", "洞察"],
        "operations_manager": ["运营", "资源", "成本", "效率"],
        "security_expert": ["安全", "风险", "合规", "保护"],
    }

    # 计算每个角色的匹配分数
    role_scores = {}
    for role_id, keywords in role_keywords.items():
        score = sum(1 for kw in keywords if kw in task_lower)
        if score > 0:
            role_scores[role_id] = score

    # 按分数排序
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)

    # 返回top N
    return [role_id for role_id, _ in sorted_roles[:num_agents]]


# 导出
__all__ = [
    'get_role',
    'list_roles',
    'get_roles_by_ids',
    'get_role_combination',
    'recommend_roles',
    'ROLE_COMBINATIONS',
    'PREDEFINED_ROLES',
]
