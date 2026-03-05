"""
Component Composition System - 组件组合系统
===========================================

实现组件间的组合逻辑，包括规则定义、布局生成、页面组合和验证功能。

核心功能:
    1. CompositionRule - 组件组合规则（嵌套、互斥、推荐搭配）
    2. LayoutGenerator - 自动生成布局代码
    3. compose_page() - 组合多个组件成完整页面
    4. validate_composition() - 验证组件组合合理性
    5. 10 种预定义组合模式

使用方式:
    from ui_library.patterns import (
        CompositionRule,
        LayoutGenerator,
        compose_page,
        validate_composition,
        PREDEFINED_PATTERNS,
    )
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json


# ============================================================================
# 导入组件和主题定义
# ============================================================================

# 导入大型组件
try:
    from ..components.large import (
        LargeComponent,
        LargeComponentCategory,
        LARGE_COMPONENTS,
    )
except ImportError:
    # 用于独立运行时的回退
    LargeComponent = None
    LargeComponentCategory = None
    LARGE_COMPONENTS = []

# 导入中型组件
try:
    from ..components.medium import (
        MediumComponent,
        MediumComponentCategory,
        MEDIUM_COMPONENTS,
    )
except ImportError:
    MediumComponent = None
    MediumComponentCategory = None
    MEDIUM_COMPONENTS = []

# 导入主题定义
try:
    from ..themes.definitions import (
        Theme,
        ThemeMode,
        ThemeCategory,
        get_theme,
        DEFAULT_LIGHT,
        DEFAULT_DARK,
    )
except ImportError:
    Theme = None
    ThemeMode = None
    ThemeCategory = None
    get_theme = None
    DEFAULT_LIGHT = None
    DEFAULT_DARK = None


# ============================================================================
# 枚举定义
# ============================================================================

class ComponentSize(Enum):
    """组件尺寸"""
    SMALL = "small"       # 小（1/4 宽度）
    MEDIUM = "medium"     # 中（1/2 宽度）
    LARGE = "large"       # 大（3/4 宽度）
    FULL = "full"         # 全宽


class LayoutType(Enum):
    """布局类型"""
    SIDEBAR_LEFT = "sidebar_left"       # 左侧边栏
    SIDEBAR_RIGHT = "sidebar_right"     # 右侧边栏
    TOP_NAV = "top_nav"                 # 顶部导航
    SINGLE_COLUMN = "single_column"     # 单栏
    TWO_COLUMN = "two_column"           # 双栏
    THREE_COLUMN = "three_column"       # 三栏
    GRID = "grid"                       # 网格
    MASONRY = "masonry"                 # 瀑布流
    TABS = "tabs"                       # 标签页


class CompositionConstraint(Enum):
    """组合约束类型"""
    NESTING = "nesting"         # 可嵌套
    EXCLUSIVE = "exclusive"     # 互斥
    RECOMMENDED = "recommended" # 推荐搭配
    REQUIRED = "required"       # 必需包含
    PARENT = "parent"           # 父容器要求
    CHILD = "child"             # 子容器要求


class ValidationResult(Enum):
    """验证结果"""
    VALID = "valid"             # 有效
    WARNING = "warning"         # 警告
    ERROR = "error"             # 错误


# ============================================================================
# 组合规则类
# ============================================================================

@dataclass
class ComponentConstraint:
    """
    组件约束定义

    Attributes:
        component_id: 组件ID
        constraint_type: 约束类型
        target_component: 目标组件ID（互斥/搭配时使用）
        reason: 约束原因
        severity: 严重程度 (info, warning, error)
    """
    component_id: str
    constraint_type: CompositionConstraint
    target_component: Optional[str] = None
    reason: str = ""
    severity: str = "info"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component_id": self.component_id,
            "constraint_type": self.constraint_type.value,
            "target_component": self.target_component,
            "reason": self.reason,
            "severity": self.severity,
        }


class CompositionRule:
    """
    组件组合规则类

    定义组件间的组合关系，包括嵌套规则、互斥关系和推荐搭配
    """

    # 组件嵌套规则（哪些组件可以作为父容器）
    NESTING_RULES: Dict[str, List[str]] = {
        "dashboard": ["metric_card", "chart_panel", "filter_bar", "data_table", "alert_panel"],
        "settings": ["nav_sidebar", "header_bar", "filter_bar"],
        "form_wizard": ["upload_zone", "alert_panel"],
        "data_table": ["filter_bar", "alert_panel", "pagination"],
        "landing": ["pricing_table", "header_bar", "footer_bar"],
    }

    # 组件互斥规则（不能同时出现）
    EXCLUSIVE_RULES: Dict[str, List[str]] = {
        "nav_sidebar": ["top_nav"],  # 侧边栏和顶部导航通常二选一
        "single_column": ["two_column", "three_column", "grid"],
        "modal": ["toast"],  # 弹窗和提示不推荐同时出现
    }

    # 组件推荐搭配
    RECOMMENDED_PAIRS: List[Tuple[str, str]] = [
        ("filter_bar", "data_table"),
        ("filter_bar", "chart_panel"),
        ("header_bar", "nav_sidebar"),
        ("metric_card", "chart_panel"),
        ("upload_zone", "alert_panel"),
        ("pricing_table", "landing"),
        ("comment_section", "data_list"),
        ("timeline_block", "data_list"),
        ("dashboard", "metric_card"),
        ("dashboard", "chart_panel"),
    ]

    # 必需组件（某个组件需要其他组件配合）
    REQUIRED_COMPONENTS: Dict[str, List[str]] = {
        "data_table": ["pagination"],
        "filter_bar": ["alert_panel"],
        "form_wizard": ["alert_panel"],
    }

    # 父容器要求
    PARENT_REQUIREMENTS: Dict[str, str] = {
        "metric_card": "dashboard",
        "chart_panel": "dashboard",
        "filter_bar": "data_table",
    }

    def __init__(self):
        """初始化组合规则"""
        self._custom_constraints: List[ComponentConstraint] = []

    def can_nest(self, parent_id: str, child_id: str) -> bool:
        """
        检查是否可以嵌套

        Args:
            parent_id: 父组件ID
            child_id: 子组件ID

        Returns:
            是否可以嵌套
        """
        if parent_id in self.NESTING_RULES:
            return child_id in self.NESTING_RULES[parent_id]
        return False

    def is_exclusive(self, component1: str, component2: str) -> bool:
        """
        检查两个组件是否互斥

        Args:
            component1: 组件1 ID
            component2: 组件2 ID

        Returns:
            是否互斥
        """
        # 双向检查
        if component1 in self.EXCLUSIVE_RULES:
            if component2 in self.EXCLUSIVE_RULES[component1]:
                return True
        if component2 in self.EXCLUSIVE_RULES:
            if component1 in self.EXCLUSIVE_RULES[component2]:
                return True
        return False

    def get_recommendations(self, component_id: str) -> List[str]:
        """
        获取与组件推荐搭配的其他组件

        Args:
            component_id: 组件ID

        Returns:
            推荐组件ID列表
        """
        recommendations = []
        for pair in self.RECOMMENDED_PAIRS:
            if pair[0] == component_id:
                recommendations.append(pair[1])
            elif pair[1] == component_id:
                recommendations.append(pair[0])
        return recommendations

    def get_required_components(self, component_id: str) -> List[str]:
        """
        获取组件需要的必需组件

        Args:
            component_id: 组件ID

        Returns:
            必需组件ID列表
        """
        return self.REQUIRED_COMPONENTS.get(component_id, [])

    def get_parent_requirement(self, component_id: str) -> Optional[str]:
        """
        获取组件的父容器要求

        Args:
            component_id: 组件ID

        Returns:
            父组件ID，如果没有要求则返回 None
        """
        return self.PARENT_REQUIREMENTS.get(component_id)

    def add_custom_constraint(self, constraint: ComponentConstraint):
        """添加自定义约束"""
        self._custom_constraints.append(constraint)

    def get_all_constraints(self, component_id: str) -> List[ComponentConstraint]:
        """获取组件的所有约束"""
        constraints = []

        # 嵌套规则
        for parent, children in self.NESTING_RULES.items():
            if component_id in children:
                constraints.append(ComponentConstraint(
                    component_id=component_id,
                    constraint_type=CompositionConstraint.NESTING,
                    target_component=parent,
                    reason=f"可嵌套在 {parent} 中",
                    severity="info"
                ))

        # 互斥规则
        if component_id in self.EXCLUSIVE_RULES:
            for exclusive in self.EXCLUSIVE_RULES[component_id]:
                constraints.append(ComponentConstraint(
                    component_id=component_id,
                    constraint_type=CompositionConstraint.EXCLUSIVE,
                    target_component=exclusive,
                    reason=f"与 {exclusive} 互斥",
                    severity="warning"
                ))

        # 推荐搭配
        for rec in self.get_recommendations(component_id):
            constraints.append(ComponentConstraint(
                component_id=component_id,
                constraint_type=CompositionConstraint.RECOMMENDED,
                target_component=rec,
                reason=f"推荐与 {rec} 搭配使用",
                severity="info"
            ))

        # 必需组件
        for req in self.get_required_components(component_id):
            constraints.append(ComponentConstraint(
                component_id=component_id,
                constraint_type=CompositionConstraint.REQUIRED,
                target_component=req,
                reason=f"需要 {req} 配合使用",
                severity="error"
            ))

        # 自定义约束
        for c in self._custom_constraints:
            if c.component_id == component_id:
                constraints.append(c)

        return constraints


# ============================================================================
# 布局生成器类
# ============================================================================

@dataclass
class LayoutConfig:
    """
    布局配置

    Attributes:
        layout_type: 布局类型
        component_sizes: 组件尺寸映射 {component_id: size}
        component_order: 组件顺序
        gap: 间距
        padding: 内边距
        responsive: 是否响应式
    """
    layout_type: LayoutType
    component_sizes: Dict[str, ComponentSize] = field(default_factory=dict)
    component_order: List[str] = field(default_factory=list)
    gap: int = 16
    padding: int = 24
    responsive: bool = True


class LayoutGenerator:
    """
    布局生成器

    根据选定组件自动生成布局代码
    """

    def __init__(self, framework: str = "streamlit"):
        """
        初始化布局生成器

        Args:
            framework: 目标框架 (streamlit, react, vue)
        """
        self.framework = framework
        self.rule = CompositionRule()

    def generate_layout(
        self,
        components: List[str],
        layout_type: LayoutType = LayoutType.SIDEBAR_LEFT,
        config: Optional[LayoutConfig] = None
    ) -> str:
        """
        生成布局代码

        Args:
            components: 组件ID列表
            layout_type: 布局类型
            config: 布局配置

        Returns:
            生成的代码字符串
        """
        if config is None:
            config = self._infer_config(components, layout_type)

        if self.framework == "streamlit":
            return self._generate_streamlit_layout(components, layout_type, config)
        elif self.framework == "react":
            return self._generate_react_layout(components, layout_type, config)
        elif self.framework == "vue":
            return self._generate_vue_layout(components, layout_type, config)
        else:
            return f"// {self.framework} 框架暂不支持"

    def _infer_config(self, components: List[str], layout_type: LayoutType) -> LayoutConfig:
        """推断布局配置"""
        config = LayoutConfig(layout_type=layout_type)

        # 根据组件类型推断尺寸
        for comp in components:
            if "metric" in comp or "card" in comp:
                config.component_sizes[comp] = ComponentSize.MEDIUM
            elif "chart" in comp or "table" in comp:
                config.component_sizes[comp] = ComponentSize.FULL
            elif "nav" in comp or "header" in comp:
                config.component_sizes[comp] = ComponentSize.FULL
            else:
                config.component_sizes[comp] = ComponentSize.LARGE

        config.component_order = components
        return config

    def _generate_streamlit_layout(
        self,
        components: List[str],
        layout_type: LayoutType,
        config: LayoutConfig
    ) -> str:
        """生成 Streamlit 布局代码"""
        code_lines = ['"""', f"Generated {layout_type.value} layout", '"""', ""]
        code_lines.append("import streamlit as st")
        code_lines.append("")

        # 添加主题支持
        code_lines.append("# 配置页面")
        code_lines.append("st.set_page_config(")
        code_lines.append('    page_title="组合页面",')
        code_lines.append('    page_icon="🎨",')
        code_lines.append('    layout="wide",')
        code_lines.append(")")
        code_lines.append("")

        # 根据布局类型生成代码
        if layout_type == LayoutType.SIDEBAR_LEFT:
            code_lines.extend(self._streamlit_sidebar_layout(components, config))
        elif layout_type == LayoutType.SIDEBAR_RIGHT:
            code_lines.extend(self._streamlit_sidebar_right_layout(components, config))
        elif layout_type == LayoutType.TOP_NAV:
            code_lines.extend(self._streamlit_top_nav_layout(components, config))
        elif layout_type == LayoutType.TWO_COLUMN:
            code_lines.extend(self._streamlit_two_column_layout(components, config))
        elif layout_type == LayoutType.THREE_COLUMN:
            code_lines.extend(self._streamlit_three_column_layout(components, config))
        elif layout_type == LayoutType.GRID:
            code_lines.extend(self._streamlit_grid_layout(components, config))
        elif layout_type == LayoutType.TABS:
            code_lines.extend(self._streamlit_tabs_layout(components, config))
        else:
            code_lines.extend(self._streamlit_single_column_layout(components, config))

        return "\n".join(code_lines)

    def _streamlit_sidebar_layout(self, components: List[str], config: LayoutConfig) -> List[str]:
        """生成左侧边栏布局"""
        lines = []

        # 侧边栏
        lines.append("# 侧边栏")
        lines.append("with st.sidebar:")
        lines.append('    st.title("导航")')
        lines.append('    st.page_link("app.py", label="首页", icon="🏠")')
        lines.append('    st.page_link("pages/page1.py", label="页面1", icon="📄")')
        lines.append('    st.page_link("pages/page2.py", label="页面2", icon="📄")')
        lines.append("")
        lines.append("    st.divider()")
        lines.append("")
        lines.append('    st.markdown("### 设置")')
        lines.append('    theme = st.selectbox("主题", ["浅色", "深色"])')
        lines.append("")
        lines.append("# 主内容区")
        lines.append("st.title('📊 主内容区域')")
        lines.append("")
        lines.append("# 组件区域")
        lines.append(self._generate_components_placeholder(components))
        lines.append("")
        lines.append("# 组件占位符 - 请根据需要替换为实际组件代码")
        lines.append("# for component in " + str(components) + ":")
        lines.append("#     render_component(component)")

        return lines

    def _streamlit_top_nav_layout(self, components: List[str], config: LayoutConfig) -> List[str]:
        """生成顶部导航布局"""
        lines = []

        lines.append("# 顶部导航")
        lines.append("st.title('🎯 应用标题')")
        lines.append("")
        lines.append("col1, col2, col3, col4, col5 = st.columns(5)")
        lines.append("")
        lines.append("with col1:")
        lines.append('    st.page_link("app.py", label="首页", icon="🏠")')
        lines.append("")
        lines.append("with col2:")
        lines.append('    st.page_link("pages/page1.py", label="页面1", icon="📄")')
        lines.append("")
        lines.append("with col3:")
        lines.append('    st.page_link("pages/page2.py", label="页面2", icon="📄")')
        lines.append("")
        lines.append("with col4:")
        lines.append("    pass  # 占位")
        lines.append("")
        lines.append("with col5:")
        lines.append('    st.selectbox("主题", ["浅色", "深色"], label_visibility="collapsed")')
        lines.append("")
        lines.append("st.divider()")
        lines.append("")
        lines.append("# 主内容区")
        lines.append("st.header('主内容')")
        lines.append("")
        lines.append(self._generate_components_placeholder(components))

        return lines

    def _streamlit_two_column_layout(self, components: List[str], config: LayoutConfig) -> List[str]:
        """生成双栏布局"""
        lines = []

        lines.append("# 双栏布局")
        lines.append("")
        lines.append(f"# 共 {len(components)} 个组件")
        lines.append("col1, col2 = st.columns(2)")
        lines.append("")
        lines.append("with col1:")
        lines.append(f'    st.info("左栏 ({len(components) // 2 + len(components) % 2} 个组件)")')
        lines.append("    " + self._generate_components_placeholder(components[:len(components)//2 + len(components)%2]))
        lines.append("")
        lines.append("with col2:")
        lines.append(f'    st.info("右栏 ({len(components) // 2} 个组件)")')
        lines.append("    " + self._generate_components_placeholder(components[len(components)//2 + len(components)%2:]))

        return lines

    def _streamlit_three_column_layout(self, components: List[str], config: LayoutConfig) -> List[str]:
        """生成三栏布局"""
        lines = []

        lines.append("# 三栏布局")
        lines.append("")
        lines.append("col1, col2, col3 = st.columns(3)")
        lines.append("")
        lines.append("# 分配组件到三栏")
        lines.append(f"components = {components}")
        lines.append(f"col1_components = components[0:{(len(components) + 2) // 3}]")
        lines.append(f"col2_components = components[{(len(components) + 2) // 3}:{2 * (len(components) + 2) // 3}]")
        lines.append(f"col3_components = components[{2 * (len(components) + 2) // 3}:]")
        lines.append("")
        lines.append("with col1:")
        lines.append(f"    st.write('栏目 1')")
")
        lines.append("with col2:")
        lines.append(f"    st.write('栏目 2')")
        lines.append("")
        lines.append("with col3:")
        lines.append(f"    st.write('栏目 3')")

        return lines

    def _streamlit_grid_layout(self, components: List[str], config: LayoutConfig) -> List[str]:
        """生成网格布局"""
        lines = []

        lines.append("# 网格布局")
        lines.append("")
        lines.append(f"# {len(components)} 个组件，按 3 列网格排列")
        lines.append("cols = st.columns(min(len(components), 3))")
        lines.append("")
        lines.append("for i, component in enumerate(components):")
        lines.append("    with cols[i % 3]:")
        lines.append("        st.container(height=200)")
        lines.append("        st.caption(component)")
        lines.append("        # 在这里渲染组件")

        return lines

    def _streamlit_tabs_layout(self, components: List[str], config: LayoutConfig) -> List[str]:
        """生成标签页布局"""
        lines = []

        # 为每个组件创建标签页
        tab_names = [f"标签 {i+1}" for i in range(len(components))]

        lines.append("# 标签页布局")
        lines.append("")
        lines.append(f"tabs = st.tabs({tab_names})")
        lines.append("")
        lines.append("for tab, component in zip(tabs, components):")
        lines.append("    with tab:")
        lines.append("        st.subheader(component)")
        lines.append("        # 在这里渲染组件")

        return lines

    def _streamlit_single_column_layout(self, components: List[str], config: LayoutConfig) -> List[str]:
        """生成单栏布局"""
        lines = []

        lines.append("# 单栏布局")
        lines.append("")
        lines.append(f"# 共 {len(components)} 个组件垂直排列")
        lines.append("")
        lines.append("for i, component in enumerate(components):")
        lines.append("    st.container()")
        lines.append("    st.subheader(f'组件 {i+1}: {component}')")
        lines.append("    st.divider()")

        return lines

    def _streamlit_sidebar_right_layout(self, components: List[str], config: LayoutConfig) -> List[str]:
        """生成右侧边栏布局"""
        # Streamlit 原生只支持左侧边栏
        # 这里使用列模拟右侧边栏
        lines = []

        lines.append("# 右侧边栏布局（使用列模拟）")
        lines.append("")
        lines.append("main_col, sidebar_col = st.columns([3, 1])")
        lines.append("")
        lines.append("# 主内容区")
        lines.append("with main_col:")
        lines.append("    st.title('主内容')")
        lines.append("    " + self._generate_components_placeholder(components))
        lines.append("")
        lines.append("# 右侧边栏")
        lines.append("with sidebar_col:")
        lines.append('    st.markdown("### 侧边栏")')
        lines.append('    st.info("这里放置侧边栏内容")')

        return lines

    def _generate_components_placeholder(self, components: List[str]) -> str:
        """生成组件占位符代码"""
        return f"# 组件: {', '.join(components)}"

    def _generate_react_layout(
        self,
        components: List[str],
        layout_type: LayoutType,
        config: LayoutConfig
    ) -> str:
        """生成 React 布局代码"""
        lines = [
            '"""',
            f"Generated {layout_type.value} layout for React",
            '"""',
            "",
            "import React from 'react';",
            "import {{ Layout, Menu, Card }} from 'antd';",
            "",
            "export default function GeneratedPage() {{",
            "  return (",
            "    <Layout>",
            "      {/* 组件将在这里渲染 */}",
            "      {components.map((comp, i) => (",
            "        <Card key={{i}} title={{comp}}>",
            "          {/* {comp} 组件内容 */}",
            "        </Card>",
            "      ))}",
            "    </Layout>",
            "  );",
            "}",
        ]

        return "\n".join(lines)

    def _generate_vue_layout(
        self,
        components: List[str],
        layout_type: LayoutType,
        config: LayoutConfig
    ) -> str:
        """生成 Vue 布局代码"""
        lines = [
            '"""',
            f"Generated {layout_type.value} layout for Vue",
            '"""',
            "",
            "<template>",
            "  <div class='layout'>",
            "    <h1>Generated Page</h1>",
            "    <div v-for='(comp, i) in components' :key='i' class='component'>",
            "      <div class='component-title'>{{ comp }}</div>",
            "      <!-- {{ comp }} 组件内容 -->",
            "    </div>",
            "  </div>",
            "</template>",
            "",
            "<script setup>",
            "const components = " + str(components),
            "</script>",
            "",
            "<style scoped>",
            ".layout {",
            "  padding: 24px;",
            "}",
            ".component {",
            "  margin-bottom: 16px;",
            "}",
            "</style>",
        ]

        return "\n".join(lines)


# ============================================================================
# 组合验证
# ============================================================================

@dataclass
class CompositionIssue:
    """
    组合问题定义

    Attributes:
        issue_type: 问题类型
        severity: 严重程度 (error, warning, info)
        message: 问题描述
        affected_components: 受影响的组件
        suggestion: 修复建议
    """
    issue_type: str
    severity: str
    message: str
    affected_components: List[str]
    suggestion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_type": self.issue_type,
            "severity": self.severity,
            "message": self.message,
            "affected_components": self.affected_components,
            "suggestion": self.suggestion,
        }


@dataclass
class CompositionValidationResult:
    """
    组合验证结果

    Attributes:
        is_valid: 是否有效
        issues: 问题列表
        warnings: 警告数量
        errors: 错误数量
        score: 合规分数 (0-100)
    """
    is_valid: bool
    issues: List[CompositionIssue]
    warnings: int = 0
    errors: int = 0
    score: int = 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "issues": [i.to_dict() for i in self.issues],
            "warnings": self.warnings,
            "errors": self.errors,
            "score": self.score,
        }


def validate_composition(
    components: List[str],
    rules: Optional[CompositionRule] = None
) -> CompositionValidationResult:
    """
    验证组件组合是否合理

    Args:
        components: 组件ID列表
        rules: 组合规则（可选）

    Returns:
        验证结果
    """
    if rules is None:
        rules = CompositionRule()

    issues = []
    score = 100
    component_set = set(components)

    # 检查互斥关系
    for i, comp1 in enumerate(components):
        for comp2 in components[i+1:]:
            if rules.is_exclusive(comp1, comp2):
                issues.append(CompositionIssue(
                    issue_type="exclusive",
                    severity="warning",
                    message=f"{comp1} 和 {comp2} 互斥",
                    affected_components=[comp1, comp2],
                    suggestion=f"建议只使用其中之一"
                ))
                score -= 20

    # 检查必需组件
    for comp in components:
        required = rules.get_required_components(comp)
        for req in required:
            if req not in component_set:
                issues.append(CompositionIssue(
                    issue_type="missing_required",
                    severity="error",
                    message=f"{comp} 需要 {req} 配合使用",
                    affected_components=[comp],
                    suggestion=f"添加 {req} 组件"
                ))
                score -= 30

    # 检查推荐搭配
    for comp in components:
        recommended = rules.get_recommendations(comp)
        for rec in recommended:
            if rec not in component_set:
                issues.append(CompositionIssue(
                    issue_type="missing_recommended",
                    severity="info",
                    message=f"{comp} 推荐与 {rec} 搭配使用",
                    affected_components=[comp],
                    suggestion=f"考虑添加 {rec} 以获得更好体验"
                ))
                score -= 5

    # 检查组件数量
    if len(components) > 15:
        issues.append(CompositionIssue(
            issue_type="too_many_components",
            severity="warning",
            message=f"组件数量过多 ({len(components)} 个)",
            affected_components=components,
            suggestion="考虑拆分为多个页面"
        ))
        score -= 10
    elif len(components) == 0:
        issues.append(CompositionIssue(
            issue_type="no_components",
            severity="error",
            message="没有选择任何组件",
            affected_components=[],
            suggestion="请至少选择一个组件"
        ))
        score = 0

    # 检查父容器要求
    for comp in components:
        parent_req = rules.get_parent_requirement(comp)
        if parent_req and parent_req not in component_set:
            issues.append(CompositionIssue(
                issue_type="missing_parent",
                severity="warning",
                message=f"{comp} 建议放在 {parent_req} 容器中",
                affected_components=[comp],
                suggestion=f"添加 {parent_req} 或调整布局"
            ))
            score -= 15

    # 统计错误和警告
    errors = sum(1 for i in issues if i.severity == "error")
    warnings = sum(1 for i in issues if i.severity == "warning")

    # 确保分数在 0-100 范围内
    score = max(0, min(100, score))

    return CompositionValidationResult(
        is_valid=errors == 0,
        issues=issues,
        warnings=warnings,
        errors=errors,
        score=score
    )


# ============================================================================
# 页面组合
# ============================================================================

@dataclass
class ComponentInstance:
    """
    组件实例定义

    Attributes:
        component_id: 组件ID
        props: 组件属性
        size: 组件尺寸
        order: 渲染顺序
    """
    component_id: str
    props: Dict[str, Any] = field(default_factory=dict)
    size: ComponentSize = ComponentSize.FULL
    order: int = 0


@dataclass
class PageComposition:
    """
    页面组合定义

    Attributes:
        name: 页面名称
        description: 页面描述
        layout_type: 布局类型
        components: 组件实例列表
        theme: 主题ID
        code: 生成的代码
    """
    name: str
    description: str
    layout_type: LayoutType
    components: List[ComponentInstance]
    theme: Optional[str] = None
    code: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "layout_type": self.layout_type.value,
            "components": [
                {
                    "component_id": c.component_id,
                    "props": c.props,
                    "size": c.size.value,
                    "order": c.order,
                }
                for c in self.components
            ],
            "theme": self.theme,
            "code": self.code,
        }


def compose_page(
    components: Union[List[str], List[ComponentInstance]],
    layout_type: LayoutType = LayoutType.SIDEBAR_LEFT,
    theme: Optional[str] = None,
    framework: str = "streamlit"
) -> PageComposition:
    """
    将多个组件组合成完整页面

    Args:
        components: 组件ID列表或组件实例列表
        layout_type: 布局类型
        theme: 主题ID
        framework: 目标框架

    Returns:
        页面组合定义
    """
    # 转换组件ID为组件实例
    if components and isinstance(components[0], str):
        component_instances = [
            ComponentInstance(component_id=str(c), order=i)
            for i, c in enumerate(components)
        ]
    else:
        component_instances = components

    # 生成代码
    generator = LayoutGenerator(framework=framework)
    component_ids = [c.component_id for c in component_instances]
    code = generator.generate_layout(component_ids, layout_type)

    # 确定页面名称
    if "dashboard" in component_ids:
        name = "数据仪表盘"
        description = "综合数据展示和管理页面"
    elif "form" in component_ids:
        name = "表单页面"
        description = "数据输入和收集页面"
    elif "data" in component_ids or "table" in component_ids:
        name = "数据管理"
        description = "数据浏览和管理页面"
    else:
        name = "组合页面"
        description = f"包含 {len(components)} 个组件的自定义页面"

    return PageComposition(
        name=name,
        description=description,
        layout_type=layout_type,
        components=component_instances,
        theme=theme,
        code=code
    )


# ============================================================================
# 预定义组合模式
# ============================================================================

@dataclass
class PredefinedPattern:
    """
    预定义组合模式

    Attributes:
        id: 模式ID
        name: 模式名称
        description: 模式描述
        components: 包含的组件列表
        layout_type: 推荐布局类型
        recommended_theme: 推荐主题
        use_cases: 适用场景
    """
    id: str
    name: str
    description: str
    components: List[str]
    layout_type: LayoutType
    recommended_theme: str
    use_cases: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "components": self.components,
            "layout_type": self.layout_type.value,
            "recommended_theme": self.recommended_theme,
            "use_cases": self.use_cases,
        }


# 10种预定义组合模式
PREDEFINED_PATTERNS: Dict[str, PredefinedPattern] = {
    "dashboard": PredefinedPattern(
        id="dashboard",
        name="数据仪表盘",
        description="经典的数据仪表盘布局，包含导航、指标卡片、图表和数据表格",
        components=[
            "nav_sidebar",
            "header_bar",
            "metric_card",
            "metric_card",
            "chart_panel",
            "data_table",
            "filter_bar",
        ],
        layout_type=LayoutType.SIDEBAR_LEFT,
        recommended_theme="default_light",
        use_cases=["数据分析", "运营监控", "业务报表"]
    ),

    "data_management": PredefinedPattern(
        id="data_management",
        name="数据管理",
        description="数据管理页面，包含筛选、列表和操作功能",
        components=[
            "header_bar",
            "filter_bar",
            "data_table",
            "alert_panel",
        ],
        layout_type=LayoutType.TOP_NAV,
        recommended_theme="corporate_gray",
        use_cases=["数据录入", "记录管理", "清单查看"]
    ),

    "form_center": PredefinedPattern(
        id="form_center",
        name="表单中心",
        description="表单录入页面，包含分步表单和验证反馈",
        components=[
            "header_bar",
            "form_wizard",
            "alert_panel",
            "upload_zone",
        ],
        layout_type=LayoutType.SINGLE_COLUMN,
        recommended_theme="ocean_blue",
        use_cases=["用户注册", "信息采集", "问卷调查"]
    ),

    "analytics": PredefinedPattern(
        id="analytics",
        name="分析中心",
        description="数据分析和可视化页面，多图表展示",
        components=[
            "nav_sidebar",
            "filter_bar",
            "chart_panel",
            "chart_panel",
            "chart_panel",
            "metric_card",
        ],
        layout_type=LayoutType.SIDEBAR_LEFT,
        recommended_theme="tech_neon",
        use_cases=["数据挖掘", "趋势分析", "统计报告"]
    ),

    "content_feed": PredefinedPattern(
        id="content_feed",
        name="内容流",
        description="信息流和内容展示页面",
        components=[
            "header_bar",
            "data_list",
            "comment_section",
            "alert_panel",
        ],
        layout_type=LayoutType.SINGLE_COLUMN,
        recommended_theme="forest_green",
        use_cases=["新闻资讯", "社交动态", "博客文章"]
    ),

    "ecommerce": PredefinedPattern(
        id="ecommerce",
        name="电商页面",
        description="电商展示和交易页面",
        components=[
            "header_bar",
            "pricing_table",
            "data_list",
            "footer_bar",
        ],
        layout_type=LayoutType.TOP_NAV,
        recommended_theme="sunset_orange",
        use_cases=["商品展示", "价格对比", "在线购买"]
    ),

    "task_board": PredefinedPattern(
        id="task_board",
        name="任务看板",
        description="看板式任务管理页面",
        components=[
            "header_bar",
            "filter_bar",
            "data_table",  # 看板列
            "alert_panel",
        ],
        layout_type=LayoutType.TWO_COLUMN,
        recommended_theme="cool_mint",
        use_cases=["项目管理", "任务追踪", "工作流"]
    ),

    "settings": PredefinedPattern(
        id="settings",
        name="设置中心",
        description="系统设置和配置页面",
        components=[
            "nav_sidebar",
            "header_bar",
            "data_list",
            "form_wizard",
        ],
        layout_type=LayoutType.SIDEBAR_LEFT,
        recommended_theme="midnight_blue",
        use_cases=["系统配置", "用户设置", "偏好管理"]
    ),

    "portal": PredefinedPattern(
        id="portal",
        name="门户首页",
        description="门户首页，多内容区块展示",
        components=[
            "header_bar",
            "metric_card",
            "metric_card",
            "metric_card",
            "data_list",
            "footer_bar",
        ],
        layout_type=LayoutType.GRID,
        recommended_theme="rose_gold",
        use_cases=["企业门户", "个人主页", "导航中心"]
    ),

    "documentation": PredefinedPattern(
        id="documentation",
        name="文档中心",
        description="文档浏览和搜索页面",
        components=[
            "header_bar",
            "filter_bar",
            "data_list",
            "timeline_block",
        ],
        layout_type=LayoutType.SIDEBAR_LEFT,
        recommended_theme="warm_earth",
        use_cases=["API文档", "知识库", "帮助中心"]
    ),
}


def get_pattern(pattern_id: str) -> Optional[PredefinedPattern]:
    """获取预定义模式"""
    return PREDEFINED_PATTERNS.get(pattern_id)


def list_patterns() -> List[PredefinedPattern]:
    """列出所有预定义模式"""
    return list(PREDEFINED_PATTERNS.values())


def list_patterns_by_use_case(use_case: str) -> List[PredefinedPattern]:
    """根据用例列出模式"""
    return [
        p for p in PREDEFINED_PATTERNS.values()
        if use_case in p.use_cases
    ]


def compose_from_pattern(
    pattern_id: str,
    framework: str = "streamlit",
    custom_theme: Optional[str] = None
) -> PageComposition:
    """
    根据预定义模式组合页面

    Args:
        pattern_id: 模式ID
        framework: 目标框架
        custom_theme: 自定义主题（覆盖默认主题）

    Returns:
        页面组合定义
    """
    pattern = get_pattern(pattern_id)
    if not pattern:
        raise ValueError(f"未找到模式: {pattern_id}")

    theme = custom_theme or pattern.recommended_theme

    return compose_page(
        components=pattern.components,
        layout_type=pattern.layout_type,
        theme=theme,
        framework=framework
    )


# ============================================================================
# 工厂函数
# ============================================================================

class CompositionFactory:
    """
    组件组合工厂

    提供便捷的组件组合和页面生成功能
    """

    def __init__(self, framework: str = "streamlit"):
        """
        初始化工厂

        Args:
            framework: 目标框架
        """
        self.framework = framework
        self.rules = CompositionRule()
        self.generator = LayoutGenerator(framework)

    def create_dashboard(
        self,
        metrics: int = 4,
        charts: int = 2,
        with_sidebar: bool = True
    ) -> PageComposition:
        """
        创建仪表盘页面

        Args:
            metrics: 指标卡片数量
            charts: 图表数量
            with_sidebar: 是否包含侧边栏

        Returns:
            页面组合定义
        """
        components = []

        if with_sidebar:
            components.append("nav_sidebar")

        components.append("header_bar")

        for i in range(metrics):
            components.append("metric_card")

        for i in range(charts):
            components.append("chart_panel")

        components.append("data_table")
        components.append("filter_bar")

        return compose_page(
            components=components,
            layout_type=LayoutType.SIDEBAR_LEFT if with_sidebar else LayoutType.TOP_NAV,
            theme="default_light",
            framework=self.framework
        )

    def create_form_page(
        self,
        steps: int = 3,
        with_upload: bool = False
    ) -> PageComposition:
        """
        创建表单页面

        Args:
            steps: 表单步数
            with_upload: 是否包含上传区域

        Returns:
            页面组合定义
        """
        components = ["header_bar", "form_wizard", "alert_panel"]

        if with_upload:
            components.append("upload_zone")

        return compose_page(
            components=components,
            layout_type=LayoutType.SINGLE_COLUMN,
            theme="ocean_blue",
            framework=self.framework
        )

    def create_data_grid(
        self,
        columns: int = 2
    ) -> PageComposition:
        """
        创建数据网格页面

        Args:
            columns: 列数

        Returns:
            页面组合定义
        """
        layout_map = {
            1: LayoutType.SINGLE_COLUMN,
            2: LayoutType.TWO_COLUMN,
            3: LayoutType.THREE_COLUMN,
        }

        components = ["header_bar", "filter_bar"]
        for i in range(columns * 2):
            components.append("data_table")
        components.append("alert_panel")

        return compose_page(
            components=components,
            layout_type=layout_map.get(columns, LayoutType.GRID),
            theme="corporate_gray",
            framework=self.framework
        )

    def get_suggestions(self, components: List[str]) -> List[str]:
        """
        获取组件组合建议

        Args:
            components: 已选组件列表

        Returns:
            建议添加的组件列表
        """
        suggestions = set()

        for comp in components:
            # 添加推荐搭配
            suggestions.update(self.rules.get_recommendations(comp))

            # 添加必需组件
            suggestions.update(self.rules.get_required_components(comp))

        # 移除已存在的组件
        return list(suggestions - set(components))


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "ComponentSize",
    "LayoutType",
    "CompositionConstraint",
    "ValidationResult",
    # 组合规则
    "CompositionRule",
    "ComponentConstraint",
    # 布局生成
    "LayoutGenerator",
    "LayoutConfig",
    # 验证
    "CompositionIssue",
    "CompositionValidationResult",
    "validate_composition",
    # 页面组合
    "ComponentInstance",
    "PageComposition",
    "compose_page",
    # 预定义模式
    "PredefinedPattern",
    "PREDEFINED_PATTERNS",
    "get_pattern",
    "list_patterns",
    "list_patterns_by_use_case",
    "compose_from_pattern",
    # 工厂
    "CompositionFactory",
]
