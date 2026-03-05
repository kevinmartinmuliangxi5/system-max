"""
UI Template Library Pro - 双脑协同 UI 设计系统
================================================

一个支持多框架、多行业的 UI 组件库管理系统。
提供组件推荐、主题定制、行业模板、代码生成等功能。

模块结构:
    - components: 大型/中型组件库
    - themes: 主题定义系统 (15+ 主题)
    - patterns: 交互模式库 (10+ 模式)
    - industries: 行业专用模板 (4+ 行业)
    - recommender: 智能推荐引擎
    - adapters: 框架适配器 (React, Vue)
    - docs: 文档生成器

快速开始:
    >>> from ui_library import get_component, apply_theme, recommend
    >>>
    >>> # 获取组件
    >>> dashboard = get_component("DashboardPage")
    >>> print(dashboard["name"])
    >>>
    >>> # 应用主题
    >>> apply_theme("tech_neon")
    >>>
    >>> # 智能推荐
    >>> recommendations = recommend(industry="data_analytics", use_case="dashboard")
    >>> print(recommendations["components"])

版本: 1.0.0
作者: Commander System
"""

__version__ = "1.0.0"
__author__ = "Commander System"

# ============================================================================
# 核心 API 导出
# ============================================================================

# 组件相关
from .components import large as large_components
from .components import medium as medium_components

# 主题相关
from .themes import definitions as theme_definitions
from .themes import engine as theme_engine

# 模式相关
from .patterns import interactions
from .patterns import composition

# 行业模板
from .industries import data_analytics
from .industries import education
from .industries import cms
from .industries import ai_apps

# 推荐引擎
from .recommender import engine as recommender_engine
from .recommender import rules as recommender_rules

# 适配器
from .adapters import ReactAdapter
from .adapters import generate_react_component
from .adapters import generate_react_page

# 文档生成器
from .docs import DocGenerator
from .docs import generate_all_docs
from .docs import export_to_markdown

# ============================================================================
# 用户友好的 API 函数
# ============================================================================

def get_component(component_id: str):
    """
    获取组件定义

    Args:
        component_id: 组件 ID (如 "DashboardPage", "MetricCard")

    Returns:
        组件定义字典，包含:
            - id: 组件 ID
            - name: 组件名称
            - description: 描述
            - category: 类别
            - size: 大小 (large/medium)
            - features: 特性列表
            - preview: ASCII 预览
            - code_skeleton: Streamlit 代码骨架
            - props: 属性字典

    Example:
        >>> component = get_component("DashboardPage")
        >>> print(component["name"])
        DashboardPage
        >>> print(component["description"])
        数据仪表盘（指标卡片+图表+筛选器）
    """
    # 先在大型组件中查找
    for comp in _get_large_components():
        if getattr(comp, "id", comp.__class__.__name__) == component_id:
            return _component_to_dict(comp)

    # 再在中型组件中查找
    for comp in _get_medium_components():
        if getattr(comp, "id", comp.__class__.__name__) == component_id:
            return _component_to_dict(comp)

    return None


def list_components(size: str = None, category: str = None) -> list:
    """
    列出所有组件

    Args:
        size: 组件大小过滤 ("large", "medium", None 表示全部)
        category: 类别过滤

    Returns:
        组件列表

    Example:
        >>> # 列出所有大型组件
        >>> large_comps = list_components(size="large")
        >>>
        >>> # 列出所有组件
        >>> all_comps = list_components()
    """
    components = []

    if size is None or size == "large":
        for comp in _get_large_components():
            comp_dict = _component_to_dict(comp)
            if category is None or comp_dict.get("category") == category:
                components.append(comp_dict)

    if size is None or size == "medium":
        for comp in _get_medium_components():
            comp_dict = _component_to_dict(comp)
            if category is None or comp_dict.get("category") == category:
                components.append(comp_dict)

    return components


def get_theme(theme_id: str):
    """
    获取主题定义

    Args:
        theme_id: 主题 ID (如 "tech_neon", "ocean_blue")

    Returns:
        主题定义字典，包含:
            - id: 主题 ID
            - name: 主题名称
            - description: 描述
            - mode: 模式 (light/dark/auto)
            - colors: 颜色配置
            - typography: 字体配置
            - spacing: 间距配置
            - border_radius: 圆角配置
            - shadows: 阴影配置

    Example:
        >>> theme = get_theme("tech_neon")
        >>> print(theme["name"])
        科技霓虹
        >>> print(theme["colors"]["primary"])
        #3B82F6
    """
    themes = theme_definitions.THEMES
    return themes.get(theme_id)


def list_themes() -> list:
    """
    列出所有主题

    Returns:
        主题列表

    Example:
        >>> themes = list_themes()
        >>> for theme in themes:
        ...     print(theme["name"])
    """
    themes = theme_definitions.THEMES
    return [
        {
            "id": theme_id,
            "name": theme.get("name", theme_id),
            "description": theme.get("description", ""),
            "mode": theme.get("mode", "light"),
        }
        for theme_id, theme in themes.items()
    ]


def apply_theme(theme_id: str, mode: str = None):
    """
    应用主题到页面 (仅适用于 Streamlit)

    Args:
        theme_id: 主题 ID
        mode: 主题模式 ("light", "dark", "auto")，None 则使用主题默认

    Example:
        >>> import streamlit as st
        >>> from ui_library import apply_theme
        >>>
        >>> apply_theme("tech_neon")
        >>>
        >>> # 强制深色模式
        >>> apply_theme("ocean_blue", mode="dark")
    """
    theme = get_theme(theme_id)
    if not theme:
        raise ValueError(f"Theme '{theme_id}' not found")

    theme_mode = mode or theme.get("mode", "light")

    # 使用主题引擎应用
    engine = theme_engine.ThemeEngine()
    engine.apply_theme(theme_id, mode=theme_mode)


def recommend(industry: str, use_case: str, complexity: str = "medium"):
    """
    智能推荐组件和主题

    Args:
        industry: 行业 ID (如 "data_analytics", "education", "cms", "ai_apps")
        use_case: 使用场景 (如 "dashboard", "form", "report")
        complexity: 复杂度 ("simple", "medium", "complex")

    Returns:
        推荐结果字典，包含:
            - components: 推荐组件列表
            - themes: 推荐主题列表 (Top 3)
            - layout: 推荐布局模式
            - pattern: 推荐组合模式

    Example:
        >>> recommendations = recommend(
        ...     industry="data_analytics",
        ...     use_case="dashboard",
        ...     complexity="medium"
        ... )
        >>>
        >>> for component in recommendations["components"]:
        ...     print(component["name"])
    """
    engine = recommender_engine.RecommenderEngine()
    return engine.recommend(
        industry=industry,
        use_case=use_case,
        complexity=complexity
    )


def compose(components: list, layout_type: str = "default", theme: str = None, framework: str = "streamlit"):
    """
    组合多个组件生成完整页面代码

    Args:
        components: 组件 ID 列表 (如 ["HeaderBar", "MetricCard", "ChartPanel"])
        layout_type: 布局类型 ("dashboard", "form", "analytics", "content", "default")
        theme: 主题 ID (如 "tech_neon")
        framework: 框架类型 ("streamlit", "react")

    Returns:
        生成的页面代码字符串

    Example:
        >>> page_code = compose(
        ...     components=["HeaderBar", "MetricCard", "ChartPanel"],
        ...     layout_type="dashboard",
        ...     theme="ocean_blue",
        ...     framework="streamlit"
        ... )
        >>>
        >>> import streamlit as st
        >>> st.write(page_code)
    """
    # 使用组合系统
    generator = composition.LayoutGenerator(framework=framework)

    # 获取组件定义
    component_defs = []
    for comp_id in components:
        comp = get_component(comp_id)
        if comp:
            component_defs.append(comp)

    # 生成布局
    page_code = generator.generate_layout(
        components=component_defs,
        layout_type=layout_type,
        theme=theme
    )

    return page_code


def export_docs(output_path: str = "./docs"):
    """
    导出所有文档到 Markdown 文件

    Args:
        output_path: 输出目录路径

    Example:
        >>> from ui_library import export_docs
        >>>
        >>> export_docs("./my_docs")
        Documentation exported to ./my_docs
    """
    docs = generate_all_docs()
    export_to_markdown(docs, output_path)


def generate_react(component_id: str, theme_id: str = None):
    """
    生成 React 组件代码

    Args:
        component_id: 组件 ID
        theme_id: 主题 ID (可选)

    Returns:
        React (TSX) 代码字符串

    Example:
        >>> react_code = generate_react("DashboardPage", "tech_neon")
        >>> with open("Dashboard.tsx", "w") as f:
        ...     f.write(react_code)
    """
    component = get_component(component_id)
    if not component:
        raise ValueError(f"Component '{component_id}' not found")

    theme = None
    if theme_id:
        theme = get_theme(theme_id)

    return generate_react_component(component_def=component, theme=theme)


# ============================================================================
# 内部辅助函数
# ============================================================================

def _get_large_components():
    """获取所有大型组件"""
    return [
        large_components.DashboardPage,
        large_components.ChatbotPage,
        large_components.FormWizardPage,
        large_components.DataTablePage,
        large_components.SettingsPage,
        large_components.LandingPage,
        large_components.KanbanPage,
        large_components.ProfilePage,
    ]


def _get_medium_components():
    """获取所有中型组件"""
    return [
        medium_components.MetricCard,
        medium_components.ChartPanel,
        medium_components.FilterBar,
        medium_components.DataList,
        medium_components.NavSidebar,
        medium_components.HeaderBar,
        medium_components.FooterBar,
        medium_components.AlertPanel,
        medium_components.UploadZone,
        medium_components.CommentSection,
        medium_components.TimelineBlock,
        medium_components.PricingTable,
    ]


def _component_to_dict(comp):
    """将组件类转换为字典"""
    # 如果是类，先实例化
    if isinstance(comp, type):
        comp = comp()

    return {
        "id": getattr(comp, "id", comp.__class__.__name__),
        "name": getattr(comp, "name", comp.__class__.__name__),
        "description": getattr(comp, "description", ""),
        "category": getattr(comp, "category", "general"),
        "size": getattr(comp, "size", "medium"),
        "features": getattr(comp, "features", []),
        "preview": getattr(comp, "preview", ""),
        "code_skeleton": getattr(comp, "code_skeleton", ""),
        "props": getattr(comp, "props", {}),
    }


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 核心组件
    "get_component",
    "list_components",
    "get_theme",
    "list_themes",
    "apply_theme",
    "recommend",
    "compose",
    "export_docs",
    "generate_react",
    # 版本信息
    "__version__",
    "__author__",
]


# ============================================================================
# 便捷别名
# ============================================================================

# 为了向后兼容，添加一些别名
get_template = get_component
get_all_templates = list_components
get_template_summary = lambda: {
    "total_components": len(list_components()),
    "large_components": len(list_components(size="large")),
    "medium_components": len(list_components(size="medium")),
    "total_themes": len(list_themes()),
}
