"""
Recommendation Rules - 推荐规则矩阵
====================================

定义推荐系统使用的规则矩阵和评分标准：

规则类别:
    - 行业-组件兼容性矩阵
    - 用例-布局映射规则
    - 氛围-主题关联规则
    - 复杂度-组件映射规则
    - 无障碍访问-组件筛选规则
    - 框架-组件兼容性规则

数据结构:
    - 矩阵使用字典嵌套结构
    - 分值范围 0.0-1.0
    - 支持动态权重调整
"""

from typing import Dict, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass


# ============================================================================
# 规则类型枚举
# ============================================================================

class RuleType(Enum):
    """规则类型"""
    INDUSTRY_COMPONENT = "industry_component"  # 行业-组件兼容性
    USE_CASE_LAYOUT = "use_case_layout"        # 用例-布局映射
    MOOD_THEME = "mood_theme"                  # 氛围-主题关联
    COMPLEXITY_COMPONENT = "complexity_component"  # 复杂度-组件
    ACCESSIBILITY_FILTER = "accessibility_filter"  # 无障碍筛选
    FRAMEWORK_COMPATIBILITY = "framework_compatibility"  # 框架兼容性


class Mood(Enum):
    """氛围/情绪"""
    PROFESSIONAL = "professional"  # 专业
    FRIENDLY = "friendly"          # 友好
    CREATIVE = "creative"          # 创意
    CALM = "calm"                  # 平静
    ENERGETIC = "energetic"        # 活力
    TRUSTWORTHY = "trustworthy"    # 可信
    MODERN = "modern"              # 现代
    CLASSIC = "classic"            # 经典


class Complexity(Enum):
    """复杂度"""
    MINIMAL = "minimal"    # 极简
    SIMPLE = "simple"      # 简单
    MODERATE = "moderate"  # 中等
    COMPLEX = "complex"    # 复杂
    ADVANCED = "advanced"  # 高级


class UserLevel(Enum):
    """用户水平"""
    BEGINNER = "beginner"      # 初学者
    INTERMEDIATE = "intermediate"  # 中级
    EXPERT = "expert"          # 专家


# ============================================================================
# 规则权重配置
# ============================================================================

@dataclass
class RuleWeights:
    """规则权重配置"""
    industry_match: float = 0.35       # 行业匹配权重
    use_case_fit: float = 0.25         # 用例适应权重
    complexity_match: float = 0.20     # 复杂度匹配权重
    accessibility: float = 0.15        # 无障碍权重
    framework_compatibility: float = 0.05  # 框架兼容权重

    def adjust_based_on_feedback(self, rule_type: RuleType, delta: float):
        """基于用户反馈调整权重"""
        weight_map = {
            RuleType.INDUSTRY_COMPONENT: self.industry_match,
            RuleType.USE_CASE_LAYOUT: self.use_case_fit,
            RuleType.COMPLEXITY_COMPONENT: self.complexity_match,
            RuleType.ACCESSIBILITY_FILTER: self.accessibility,
            RuleType.FRAMEWORK_COMPATIBILITY: self.framework_compatibility,
        }

        if rule_type in weight_map:
            current = weight_map[rule_type]
            new_value = max(0.0, min(1.0, current + delta))

            # 重新归一化所有权重
            if rule_type == RuleType.INDUSTRY_COMPONENT:
                self.industry_match = new_value
            elif rule_type == RuleType.USE_CASE_LAYOUT:
                self.use_case_fit = new_value
            elif rule_type == RuleType.COMPLEXITY_COMPONENT:
                self.complexity_match = new_value
            elif rule_type == RuleType.ACCESSIBILITY_FILTER:
                self.accessibility = new_value
            elif rule_type == RuleType.FRAMEWORK_COMPATIBILITY:
                self.framework_compatibility = new_value


# ============================================================================
# 行业-组件兼容性矩阵
# ============================================================================

INDUSTRY_COMPONENT_MATRIX: Dict[str, Dict[str, float]] = {
    "government": {
        # 政府行业偏好稳定、安全、表单密集型组件
        "form_wizard": 0.95,      # 表单向导
        "data_table": 0.90,       # 数据表格
        "alert_panel": 0.85,      # 警告面板
        "dashboard": 0.80,        # 仪表板
        "settings": 0.85,         # 设置页
        "chatbot": 0.60,          # 聊天机器人
        "landing": 0.50,          # 落地页
        "kanban": 0.40,           # 看板
    },
    "finance": {
        # 金融行业偏好数据密集、安全、专业组件
        "data_table": 0.95,       # 数据表格
        "dashboard": 0.90,        # 仪表板
        "chart_panel": 0.90,      # 图表面板
        "form_wizard": 0.80,      # 表单向导
        "alert_panel": 0.85,      # 警告面板
        "metric_card": 0.85,      # 指标卡片
        "chatbot": 0.50,          # 聊天机器人
        "landing": 0.45,          # 落地页
    },
    "healthcare": {
        # 医疗行业偏好表单、时间线、数据展示组件
        "form_wizard": 0.90,      # 表单向导
        "timeline_block": 0.90,   # 时间线
        "data_table": 0.85,       # 数据表格
        "alert_panel": 0.90,      # 警告面板
        "dashboard": 0.75,        # 仪表板
        "chatbot": 0.70,          # 聊天机器人
        "kanban": 0.50,           # 看板
        "landing": 0.40,          # 落地页
    },
    "ecommerce": {
        # 电商行业偏好展示、营销、交互组件
        "landing": 0.95,          # 落地页
        "pricing_table": 0.90,    # 定价表
        "data_list": 0.85,        # 数据列表
        "chart_panel": 0.75,      # 图表面板
        "dashboard": 0.70,        # 仪表板
        "form_wizard": 0.80,      # 表单向导（结账流程）
        "comment_section": 0.80,  # 评论区域
        "chatbot": 0.85,          # 聊天机器人
    },
    "education": {
        # 教育行业偏好内容展示、互动、导航组件
        "dashboard": 0.85,        # 仪表板
        "timeline_block": 0.85,   # 时间线
        "data_table": 0.75,       # 数据表格
        "chatbot": 0.75,          # 聊天机器人
        "form_wizard": 0.70,      # 表单向导
        "landing": 0.80,          # 落地页
        "comment_section": 0.70,  # 评论区域
        "nav_sidebar": 0.85,      # 导航侧边栏
    },
    "technology": {
        # 科技行业偏好现代、数据、协作组件
        "dashboard": 0.90,        # 仪表板
        "kanban": 0.90,           # 看板
        "data_table": 0.85,       # 数据表格
        "chart_panel": 0.85,      # 图表面板
        "chatbot": 0.80,          # 聊天机器人
        "settings": 0.80,         # 设置页
        "form_wizard": 0.65,      # 表单向导
        "landing": 0.70,          # 落地页
    },
}


# ============================================================================
# 用例-布局映射规则
# ============================================================================

USE_CASE_LAYOUT_RULES: Dict[str, List[Tuple[str, float]]] = {
    "data_visualization": [
        # 数据可视化用例
        ("dashboard_grid", 0.95),   # 仪表板网格
        ("analytics_center", 0.90), # 分析中心
        ("report_layout", 0.85),    # 报告布局
    ],
    "user_management": [
        # 用户管理用例
        ("master_detail", 0.90),    # 主从布局
        ("data_table_center", 0.95), # 表格中心
        ("form_split", 0.80),       # 表单分栏
    ],
    "content_consumption": [
        # 内容消费用例
        ("article_focus", 0.90),    # 文章聚焦
        ("card_grid", 0.85),        # 卡片网格
        ("timeline_vertical", 0.80), # 垂直时间线
    ],
    "task_management": [
        # 任务管理用例
        ("kanban_board", 0.95),     # 看板布局
        ("list_split", 0.85),       # 列表分栏
        ("workspace", 0.80),        # 工作空间
    ],
    "e_commerce": [
        # 电商用例
        ("product_catalog", 0.95),  # 商品目录
        ("checkout_flow", 0.90),    # 结账流程
        ("landing_hero", 0.85),     # 落地页焦点
    ],
    "social_interaction": [
        # 社交交互用例
        ("feed_center", 0.95),      # 信息流中心
        ("profile_card", 0.85),     # 个人资料卡
        ("chat_layout", 0.90),      # 聊天布局
    ],
    "form_entry": [
        # 表单录入用例
        ("form_wizard", 0.95),      # 表单向导
        ("split_form", 0.85),       # 分栏表单
        ("modal_focus", 0.75),      # 模态聚焦
    ],
    "settings_config": [
        # 设置配置用例
        ("settings_nav", 0.95),     # 设置导航
        ("tabbed_settings", 0.90),  # 标签设置
        ("toggle_split", 0.80),     # 切换分栏
    ],
}


# ============================================================================
# 氛围-主题关联规则
# ============================================================================

MOOD_THEME_MAPPING: Dict[Mood, List[Tuple[str, float]]] = {
    Mood.PROFESSIONAL: [
        # 专业氛围
        ("default_dark", 0.95),     # 默认深色
        ("corporate_gray", 0.95),   # 企业灰
        ("midnight_blue", 0.90),    # 午夜蓝
        ("default_light", 0.85),    # 默认浅色
        ("ocean_blue", 0.80),       # 海洋蓝
    ],
    Mood.FRIENDLY: [
        # 友好氛围
        ("spring_blossom", 0.95),   # 春日花开
        ("warm_earth", 0.90),       # 温暖大地
        ("berry_purple", 0.85),     # 浆果紫
        ("rose_gold", 0.85),        # 玫瑰金
        ("sunset_orange", 0.80),    # 日落橙
    ],
    Mood.CREATIVE: [
        # 创意氛围
        ("tech_neon", 0.95),        # 科技霓虹
        ("berry_purple", 0.90),     # 浆果紫
        ("sunset_orange", 0.85),    # 日落橙
        ("ocean_blue", 0.80),       # 海洋蓝
        ("rose_gold", 0.75),        # 玫瑰金
    ],
    Mood.CALM: [
        # 平静氛围
        ("cool_mint", 0.95),        # 清新薄荷
        ("ocean_blue", 0.90),       # 海洋蓝
        ("arctic_frost", 0.90),     # 北极霜
        ("forest_green", 0.85),     # 森林绿
        ("default_light", 0.80),    # 默认浅色
    ],
    Mood.ENERGETIC: [
        # 活力氛围
        ("tech_neon", 0.95),        # 科技霓虹
        ("sunset_orange", 0.90),    # 日落橙
        ("berry_purple", 0.85),     # 浆果紫
        ("ocean_blue", 0.75),       # 海洋蓝
    ],
    Mood.TRUSTWORTHY: [
        # 可信氛围
        ("corporate_gray", 0.95),   # 企业灰
        ("midnight_blue", 0.95),    # 午夜蓝
        ("ocean_blue", 0.90),       # 海洋蓝
        ("forest_green", 0.85),     # 森林绿
        ("default_dark", 0.80),     # 默认深色
    ],
    Mood.MODERN: [
        # 现代氛围
        ("tech_neon", 0.95),        # 科技霓虹
        ("ocean_blue", 0.90),       # 海洋蓝
        ("default_dark", 0.85),     # 默认深色
        ("rose_gold", 0.80),        # 玫瑰金
    ],
    Mood.CLASSIC: [
        # 经典氛围
        ("default_light", 0.95),    # 默认浅色
        ("corporate_gray", 0.90),   # 企业灰
        ("forest_green", 0.85),     # 森林绿
        ("warm_earth", 0.80),       # 温暖大地
    ],
}


# ============================================================================
# 复杂度-组件映射规则
# ============================================================================

COMPLEXITY_COMPONENT_RULES: Dict[Complexity, Tuple[float, float]] = {
    # (最小组件数, 最大组件数)
    Complexity.MINIMAL: (1, 2),       # 极简：1-2个组件
    Complexity.SIMPLE: (2, 4),        # 简单：2-4个组件
    Complexity.MODERATE: (4, 7),      # 中等：4-7个组件
    Complexity.COMPLEX: (7, 12),      # 复杂：7-12个组件
    Complexity.ADVANCED: (12, 20),    # 高级：12-20个组件
}

# 复杂度与组件类型的偏好
COMPLEXITY_COMPONENT_PREFERENCE: Dict[Complexity, Dict[str, float]] = {
    Complexity.MINIMAL: {
        "metric_card": 0.95,
        "alert_panel": 0.90,
    },
    Complexity.SIMPLE: {
        "metric_card": 0.90,
        "chart_panel": 0.85,
        "data_list": 0.85,
        "alert_panel": 0.80,
    },
    Complexity.MODERATE: {
        "dashboard": 0.90,
        "data_table": 0.85,
        "chart_panel": 0.85,
        "filter_bar": 0.80,
        "nav_sidebar": 0.75,
    },
    Complexity.COMPLEX: {
        "dashboard": 0.95,
        "data_table": 0.90,
        "form_wizard": 0.85,
        "chart_panel": 0.85,
        "filter_bar": 0.85,
        "kanban": 0.80,
    },
    Complexity.ADVANCED: {
        "dashboard": 0.95,
        "kanban": 0.90,
        "form_wizard": 0.90,
        "data_table": 0.90,
        "chart_panel": 0.90,
        "filter_bar": 0.85,
        "settings": 0.85,
        "timeline_block": 0.80,
    },
}


# ============================================================================
# 无障碍访问-组件筛选规则
# ============================================================================

# 每个组件的无障碍得分（0.0-1.0）
ACCESSIBILITY_SCORES: Dict[str, float] = {
    # 高无障碍性组件
    "data_table": 0.95,         # 表格有良好的ARIA支持
    "form_wizard": 0.90,        # 表单可进行键盘导航
    "alert_panel": 0.95,        # 警告有角色标识
    "metric_card": 0.85,        # 卡片较简单
    "settings": 0.90,           # 设置页面通常重视无障碍
    "nav_sidebar": 0.85,        # 导航支持键盘
    "header_bar": 0.90,         # 标题栏有语义化标记
    "footer_bar": 0.90,

    # 中等无障碍性组件
    "chart_panel": 0.70,        # 图表需要额外处理
    "dashboard": 0.75,          # 仪表板复杂度较高
    "data_list": 0.80,
    "filter_bar": 0.75,
    "comment_section": 0.75,
    "upload_zone": 0.70,
    "timeline_block": 0.75,
    "pricing_table": 0.80,

    # 较低无障碍性组件（需要增强）
    "kanban": 0.60,             # 看板拖拽交互复杂
    "chatbot": 0.65,            # 聊天界面需要优化
    "landing": 0.70,            # 落地页视觉性强
}

# 无障碍级别阈值
ACCESSIBILITY_THRESHOLDS = {
    "strict": 0.85,     # 严格模式：只推荐高分组件
    "moderate": 0.70,   # 中等模式：允许中等组件
    "basic": 0.50,      # 基础模式：允许低分组件
}


# ============================================================================
# 框架-组件兼容性规则
# ============================================================================

FRAMEWORK_COMPATIBILITY: Dict[str, Dict[str, float]] = {
    "react": {
        # React 原生支持的组件
        "dashboard": 1.0,
        "data_table": 1.0,
        "form_wizard": 1.0,
        "chart_panel": 0.95,      # 需要图表库
        "kanban": 0.95,           # 需要拖拽库
        "chatbot": 0.95,
        "landing": 1.0,
        "settings": 1.0,
    },
    "vue": {
        # Vue 原生支持的组件
        "dashboard": 1.0,
        "data_table": 1.0,
        "form_wizard": 1.0,
        "chart_panel": 0.95,      # 需要图表库
        "kanban": 0.95,           # 需要拖拽库
        "chatbot": 0.95,
        "landing": 1.0,
        "settings": 1.0,
    },
    "streamlit": {
        # Streamlit 原生支持的组件
        "dashboard": 1.0,
        "data_table": 1.0,
        "form_wizard": 0.90,      # 需要st.form
        "chart_panel": 1.0,       # st.pyplot等
        "metric_card": 1.0,       # st.metric
        "alert_panel": 0.95,      # st.warning/error等
        "filter_bar": 0.85,
        "nav_sidebar": 0.75,      # Streamlit已有侧边栏
        "kanban": 0.60,           # 不原生支持
        "chatbot": 0.85,          # st.chat_message
        "landing": 0.80,
        "settings": 0.90,
    },
}


# ============================================================================
# 用户水平-布局复杂度映射
# ============================================================================

USER_LEVEL_LAYOUT_COMPLEXITY: Dict[UserLevel, List[Complexity]] = {
    UserLevel.BEGINNER: [
        Complexity.MINIMAL,
        Complexity.SIMPLE,
    ],
    UserLevel.INTERMEDIATE: [
        Complexity.SIMPLE,
        Complexity.MODERATE,
        Complexity.COMPLEX,
    ],
    UserLevel.EXPERT: [
        Complexity.MODERATE,
        Complexity.COMPLEX,
        Complexity.ADVANCED,
    ],
}


# ============================================================================
# 组件组合规则（用于推荐多组件协同）
# ============================================================================

COMPONENT_COMBINATIONS: Dict[str, List[List[str]]] = {
    "government": [
        ["data_table", "filter_bar", "alert_panel"],
        ["form_wizard", "alert_panel", "header_bar"],
        ["dashboard", "metric_card", "chart_panel"],
    ],
    "finance": [
        ["dashboard", "metric_card", "chart_panel", "data_table"],
        ["data_table", "filter_bar", "chart_panel"],
        ["form_wizard", "alert_panel"],
    ],
    "healthcare": [
        ["form_wizard", "timeline_block", "alert_panel"],
        ["data_table", "filter_bar"],
        ["dashboard", "metric_card"],
    ],
    "ecommerce": [
        ["landing", "pricing_table"],
        ["data_list", "filter_bar", "comment_section"],
        ["chart_panel", "metric_card"],
    ],
    "education": [
        ["dashboard", "timeline_block"],
        ["data_table", "nav_sidebar"],
        ["chatbot", "comment_section"],
    ],
    "technology": [
        ["dashboard", "chart_panel", "data_table", "kanban"],
        ["settings", "nav_sidebar"],
        ["kanban", "filter_bar", "alert_panel"],
    ],
}


# ============================================================================
# 主题切换规则（基于时间/情境）
# ============================================================================

class TimeContext(Enum):
    """时间情境"""
    MORNING = "morning"      # 早晨 (6-12)
    AFTERNOON = "afternoon"  # 下午 (12-18)
    EVENING = "evening"      # 晚上 (18-22)
    NIGHT = "night"          # 深夜 (22-6)

TIME_THEME_MAPPING: Dict[TimeContext, List[str]] = {
    TimeContext.MORNING: ["default_light", "spring_blossom", "cool_mint"],
    TimeContext.AFTERNOON: ["ocean_blue", "forest_green", "default_light"],
    TimeContext.EVENING: ["sunset_orange", "warm_earth", "default_light"],
    TimeContext.NIGHT: ["default_dark", "midnight_blue", "arctic_frost"],
}


# ============================================================================
# 推荐规则引擎类
# ============================================================================

class RuleEngine:
    """
    推荐规则引擎

    负责应用各种规则矩阵进行评分和筛选
    """

    def __init__(self, weights: Optional[RuleWeights] = None):
        """
        初始化规则引擎

        Args:
            weights: 规则权重配置
        """
        self.weights = weights or RuleWeights()
        self._accessibility_level = "moderate"

    def get_industry_score(self, industry: str, component_id: str) -> float:
        """
        获取行业-组件兼容性得分

        Args:
            industry: 行业ID
            component_id: 组件ID

        Returns:
            兼容性得分 (0.0-1.0)
        """
        if industry not in INDUSTRY_COMPONENT_MATRIX:
            return 0.5  # 默认中等得分

        industry_rules = INDUSTRY_COMPONENT_MATRIX[industry]
        return industry_rules.get(component_id, 0.5)

    def get_mood_theme_scores(self, mood: Mood) -> List[Tuple[str, float]]:
        """
        获取氛围-主题得分列表

        Args:
            mood: 氛围枚举

        Returns:
            (主题ID, 得分) 列表，按得分降序
        """
        if mood not in MOOD_THEME_MAPPING:
            return []

        return sorted(
            MOOD_THEME_MAPPING[mood],
            key=lambda x: x[1],
            reverse=True
        )

    def get_use_case_layouts(self, use_case: str) -> List[Tuple[str, float]]:
        """
        获取用例-布局映射列表

        Args:
            use_case: 用例ID

        Returns:
            (布局ID, 得分) 列表，按得分降序
        """
        if use_case not in USE_CASE_LAYOUT_RULES:
            return []

        return sorted(
            USE_CASE_LAYOUT_RULES[use_case],
            key=lambda x: x[1],
            reverse=True
        )

    def get_complexity_range(self, complexity: Complexity) -> Tuple[int, int]:
        """
        获取复杂度对应的组件数量范围

        Args:
            complexity: 复杂度枚举

        Returns:
            (最小数量, 最大数量)
        """
        return COMPLEXITY_COMPONENT_RULES.get(complexity, (1, 3))

    def get_accessibility_score(self, component_id: str) -> float:
        """
        获取组件无障碍得分

        Args:
            component_id: 组件ID

        Returns:
            无障碍得分 (0.0-1.0)
        """
        return ACCESSIBILITY_SCORES.get(component_id, 0.5)

    def filter_by_accessibility(
        self,
        components: List[str],
        level: str = "moderate"
    ) -> List[str]:
        """
        按无障碍级别筛选组件

        Args:
            components: 组件ID列表
            level: 无障碍级别 ("strict", "moderate", "basic")

        Returns:
            筛选后的组件列表
        """
        threshold = ACCESSIBILITY_THRESHOLDS.get(level, 0.70)
        return [
            c for c in components
            if self.get_accessibility_score(c) >= threshold
        ]

    def get_framework_score(self, framework: str, component_id: str) -> float:
        """
        获取框架-组件兼容性得分

        Args:
            framework: 框架ID
            component_id: 组件ID

        Returns:
            兼容性得分 (0.0-1.0)
        """
        if framework not in FRAMEWORK_COMPATIBILITY:
            return 0.5

        return FRAMEWORK_COMPATIBILITY[framework].get(component_id, 0.5)

    def get_component_combinations(self, industry: str) -> List[List[str]]:
        """
        获取行业的推荐组件组合

        Args:
            industry: 行业ID

        Returns:
            组件组合列表
        """
        return COMPONENT_COMBINATIONS.get(industry, [])

    def get_time_based_themes(self, time_context: TimeContext) -> List[str]:
        """
        基于时间情境推荐主题

        Args:
            time_context: 时间情境

        Returns:
            推荐主题ID列表
        """
        return TIME_THEME_MAPPING.get(time_context, [])

    def calculate_component_score(
        self,
        component_id: str,
        industry: str,
        framework: str,
        complexity: Optional[Complexity] = None,
        require_accessibility: bool = False
    ) -> float:
        """
        计算组件综合得分

        Args:
            component_id: 组件ID
            industry: 行业ID
            framework: 框架ID
            complexity: 复杂度
            require_accessibility: 是否要求高无障碍性

        Returns:
            综合得分 (0.0-1.0)
        """
        scores = []

        # 行业匹配得分
        industry_score = self.get_industry_score(industry, component_id)
        scores.append(("industry", industry_score, self.weights.industry_match))

        # 框架兼容性得分
        framework_score = self.get_framework_score(framework, component_id)
        scores.append(("framework", framework_score, self.weights.framework_compatibility))

        # 复杂度偏好得分
        if complexity:
            pref = COMPLEXITY_COMPONENT_PREFERENCE.get(complexity, {})
            complexity_score = pref.get(component_id, 0.5)
            scores.append(("complexity", complexity_score, self.weights.complexity_match))

        # 无障碍得分
        if require_accessibility:
            a11y_score = self.get_accessibility_score(component_id)
            scores.append(("accessibility", a11y_score, self.weights.accessibility))

        # 加权计算总分
        total_score = sum(score * weight for _, score, weight in scores)
        total_weight = sum(weight for _, _, weight in scores)

        return total_score / total_weight if total_weight > 0 else 0.0

    def adjust_weights(self, rule_type: RuleType, delta: float):
        """
        调整规则权重

        Args:
            rule_type: 规则类型
            delta: 调整增量 (-0.1 到 +0.1)
        """
        self.weights.adjust_based_on_feedback(rule_type, delta)

    def set_accessibility_level(self, level: str):
        """
        设置无障碍级别

        Args:
            level: 级别 ("strict", "moderate", "basic")
        """
        if level in ACCESSIBILITY_THRESHOLDS:
            self._accessibility_level = level


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "RuleType",
    "Mood",
    "Complexity",
    "UserLevel",
    "TimeContext",
    # 权重配置
    "RuleWeights",
    # 规则矩阵
    "INDUSTRY_COMPONENT_MATRIX",
    "USE_CASE_LAYOUT_RULES",
    "MOOD_THEME_MAPPING",
    "COMPLEXITY_COMPONENT_RULES",
    "COMPLEXITY_COMPONENT_PREFERENCE",
    "ACCESSIBILITY_SCORES",
    "ACCESSIBILITY_THRESHOLDS",
    "FRAMEWORK_COMPATIBILITY",
    "USER_LEVEL_LAYOUT_COMPLEXITY",
    "COMPONENT_COMBINATIONS",
    "TIME_THEME_MAPPING",
    # 规则引擎
    "RuleEngine",
]
