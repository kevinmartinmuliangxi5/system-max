"""
Patterns - 交互模式库
====================

定义和管理UI组件的交互模式和最佳实践。

交互模式分类:
    - navigation/: 导航模式（面包屑、标签页、分步导航等）
    - feedback/: 反馈模式（加载状态、错误处理、空状态等）
    - input/: 输入模式（表单验证、自动完成、多选等）
    - display/: 展示模式（懒加载、虚拟滚动、分页等）
    - layout/: 布局模式（响应式、栅格系统、分割面板等）
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# 交互模式类型枚举
# ============================================================================

class PatternCategory(Enum):
    """交互模式分类"""
    NAVIGATION = "navigation"
    FEEDBACK = "feedback"
    INPUT = "input"
    DISPLAY = "display"
    LAYOUT = "layout"
    AUTHENTICATION = "authentication"
    DATA_MANAGEMENT = "data_management"


# ============================================================================
# 交互模式数据类
# ============================================================================

@dataclass
class InteractionPattern:
    """
    交互模式定义

    Attributes:
        id: 模式唯一标识符
        name: 模式名称
        category: 模式分类
        description: 模式描述
        use_case: 适用场景
        components: 涉及的组件列表
        implementation: 实现说明
        best_practices: 最佳实践列表
        alternatives: 替代方案
        examples: 示例代码
        accessibility: 可访问性说明
    """
    id: str
    name: str
    category: PatternCategory
    description: str
    use_case: str
    components: List[str] = field(default_factory=list)
    implementation: str = ""
    best_practices: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)
    examples: Dict[str, str] = field(default_factory=dict)
    accessibility: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "use_case": self.use_case,
            "components": self.components,
            "implementation": self.implementation,
            "best_practices": self.best_practices,
            "alternatives": self.alternatives,
            "examples": self.examples,
            "accessibility": self.accessibility,
        }


# ============================================================================
# 交互模式注册表
# ============================================================================

class PatternRegistry:
    """交互模式注册表"""

    def __init__(self):
        self._patterns: Dict[str, InteractionPattern] = {}
        self._register_default_patterns()

    def _register_default_patterns(self):
        """注册默认交互模式"""

        # === Navigation Patterns ===

        breadcrumbs = InteractionPattern(
            id="breadcrumbs",
            name="面包屑导航",
            category=PatternCategory.NAVIGATION,
            description="显示用户在网站层次结构中的当前位置",
            use_case="深层次网站结构，帮助用户理解当前位置和返回上级",
            components=["Breadcrumb", "Link"],
            best_practices=[
                "不要在首页显示面包屑",
                "使用分隔符（如 / 或 >）区分层级",
                "保持路径简短，最多显示3-4个层级",
                "当前页面不可点击",
            ],
            alternatives=["顶部标签页", "返回按钮"],
            accessibility="使用 nav 标签和 aria-label='breadcrumb'",
        )
        self.register(breadcrumbs)

        tabs = InteractionPattern(
            id="tabs",
            name="标签页切换",
            category=PatternCategory.NAVIGATION,
            description="在相同上下文中切换不同内容视图",
            use_case="内容分类展示，节省页面空间",
            components=["Tab", "TabPanel", "TabList"],
            best_practices=[
                "标签文本简短明确",
                "当前标签清晰高亮",
                "支持键盘导航",
                "保持标签页状态（切换后不重置）",
            ],
            alternatives=["下拉菜单", "侧边栏"],
            accessibility="使用 role='tablist' 和 aria-selected",
        )
        self.register(tabs)

        stepper = InteractionPattern(
            id="stepper",
            name="分步导航",
            category=PatternCategory.NAVIGATION,
            description="将复杂流程分解为多个步骤",
            use_case="多步骤表单、向导、配置流程",
            components=["Stepper", "Step", "Button"],
            best_practices=[
                "显示总步骤数和当前位置",
                "明确标记完成的步骤",
                "允许返回修改之前的步骤",
                "提供进度指示",
            ],
            alternatives=["长表单", "向导对话框"],
            accessibility="使用 aria-current='step'",
        )
        self.register(stepper)

        # === Feedback Patterns ===

        loading = InteractionPattern(
            id="loading_skeleton",
            name="骨架屏加载",
            category=PatternCategory.FEEDBACK,
            description="在内容加载时显示占位符",
            use_case="改善加载体验，减少感知等待时间",
            components=["Skeleton", "Spinner"],
            best_practices=[
                "骨架屏应与实际内容结构相似",
                "添加微妙的动画效果",
                "加载时间<100ms时无需显示",
            ],
            alternatives=["传统加载动画", "进度条"],
            accessibility="使用 aria-busy='true' 和 aria-live='polite'",
        )
        self.register(loading)

        empty_state = InteractionPattern(
            id="empty_state",
            name="空状态",
            category=PatternCategory.FEEDBACK,
            description="当没有数据或内容时显示的友好提示",
            use_case="列表为空、搜索无结果、未添加项目",
            components=["EmptyState", "Icon", "Button"],
            best_practices=[
                "提供清晰的说明文字",
                "添加插图或图标增强视觉效果",
                "提供行动按钮（如'添加项目'）",
                "保持友好和鼓励的语气",
            ],
            alternatives=["空白页面", "默认提示"],
            accessibility="使用 role='status'",
        )
        self.register(empty_state)

        error_handling = InteractionPattern(
            id="inline_validation",
            name="内联表单验证",
            category=PatternCategory.FEEDBACK,
            description="实时显示表单字段的验证结果",
            use_case="表单输入、数据校验",
            components=["Input", "ErrorMessage", "HelperText"],
            best_practices=[
                "在用户离开字段（onBlur）时验证",
                "错误信息清晰具体",
                "使用颜色和图标增强识别",
                "不要过早显示错误（输入中）",
            ],
            alternatives=["提交后验证", "对话框错误"],
            accessibility="使用 aria-invalid 和 aria-describedby",
        )
        self.register(error_handling)

        # === Input Patterns ===

        autocomplete = InteractionPattern(
            id="autocomplete",
            name="自动完成",
            category=PatternCategory.INPUT,
            description="根据用户输入提供匹配建议",
            use_case="搜索框、地址输入、标签选择",
            components=["Autocomplete", "Input", "Dropdown"],
            best_practices=[
                "最少输入2-3个字符后显示建议",
                "高亮匹配部分",
                "支持键盘导航",
                "显示匹配原因（如分类）",
            ],
            alternatives=["下拉选择", "自由输入"],
            accessibility="使用 role='combobox' 和 aria-autocomplete",
        )
        self.register(autocomplete)

        multi_select = InteractionPattern(
            id="multi_select",
            name="多选选择器",
            category=PatternCategory.INPUT,
            description="允许用户选择多个选项",
            use_case="标签选择、权限分配、筛选器",
            components=["MultiSelect", "Checkbox", "Tag"],
            best_practices=[
                "清晰显示已选项数量",
                "支持删除已选项",
                "提供全选功能",
                "考虑搜索/筛选选项",
            ],
            alternatives=["复选框组", "下拉多选"],
            accessibility="使用 aria-multiselectable='true'",
        )
        self.register(multi_select)

        # === Display Patterns ===

        lazy_load = InteractionPattern(
            id="lazy_loading",
            name="懒加载",
            category=PatternCategory.DISPLAY,
            description="延迟加载内容，直到用户需要时",
            use_case="图片列表、长页面、无限滚动",
            components=["LazyLoad", "Spinner"],
            best_practices=[
                "使用占位符或加载指示器",
                "预加载临近内容",
                "考虑用户带宽和设备",
                "提供加载状态反馈",
            ],
            alternatives=["分页", "全量加载"],
            accessibility="使用 aria-busy",
        )
        self.register(lazy_load)

        virtual_scroll = InteractionPattern(
            id="virtual_scrolling",
            name="虚拟滚动",
            category=PatternCategory.DISPLAY,
            description="只渲染可见区域的项目",
            use_case="大数据列表（1000+项）",
            components=["VirtualList", "ScrollContainer"],
            best_practices=[
                "保持滚动位置",
                "处理动态高度项目",
                "提供缓冲区渲染",
                "优化滚动性能",
            ],
            alternatives=["分页", "限制显示数量"],
            accessibility="确保键盘导航正常工作",
        )
        self.register(virtual_scroll)

        # === Layout Patterns ===

        responsive_grid = InteractionPattern(
            id="responsive_grid",
            name="响应式栅格",
            category=PatternCategory.LAYOUT,
            description="根据屏幕尺寸自动调整布局",
            use_case="卡片列表、仪表盘、图库",
            components=["Grid", "Container"],
            best_practices=[
                "移动优先设计",
                "使用断点（sm/md/lg/xl）",
                "保持间距一致",
                "测试各种屏幕尺寸",
            ],
            alternatives=["固定宽度", "流式布局"],
            accessibility="确保阅读顺序合理",
        )
        self.register(responsive_grid)

        split_view = InteractionPattern(
            id="split_pane",
            name="分割面板",
            category=PatternCategory.LAYOUT,
            description="将区域分为可调整大小的两部分",
            use_case="代码编辑器、文件浏览器、对比视图",
            components=["SplitPane", "Resizer"],
            best_practices=[
                "设置最小宽度防止内容被挤压",
                "提供拖动手柄",
                "记住用户调整的大小",
                "支持折叠面板",
            ],
            alternatives=["标签页", "模态对话框"],
            accessibility="使用 role='separator' 和 aria-valuenow",
        )
        self.register(split_view)

    def register(self, pattern: InteractionPattern):
        """
        注册交互模式

        Args:
            pattern: 交互模式实例
        """
        self._patterns[pattern.id] = pattern

    def get(self, pattern_id: str) -> Optional[InteractionPattern]:
        """
        获取交互模式

        Args:
            pattern_id: 模式ID

        Returns:
            交互模式实例，不存在则返回 None
        """
        return self._patterns.get(pattern_id)

    def list_by_category(self, category: PatternCategory) -> List[InteractionPattern]:
        """
        按分类列出交互模式

        Args:
            category: 模式分类

        Returns:
            该分类下的所有交互模式
        """
        return [p for p in self._patterns.values() if p.category == category]

    def list_all(self) -> List[InteractionPattern]:
        """列出所有交互模式"""
        return list(self._patterns.values())

    def search(self, keyword: str) -> List[InteractionPattern]:
        """
        搜索交互模式

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的交互模式列表
        """
        keyword_lower = keyword.lower()
        results = []
        for pattern in self._patterns.values():
            if (keyword_lower in pattern.name.lower() or
                keyword_lower in pattern.description.lower() or
                keyword_lower in pattern.use_case.lower()):
                results.append(pattern)
        return results


# ============================================================================
# 全局注册表实例
# ============================================================================

_default_registry: Optional[PatternRegistry] = None


def get_pattern_registry() -> PatternRegistry:
    """
    获取全局交互模式注册表（单例模式）

    Returns:
        PatternRegistry 实例
    """
    global _default_registry
    if _default_registry is None:
        _default_registry = PatternRegistry()
    return _default_registry


# ============================================================================
# 便捷函数
# ============================================================================

def get_pattern(pattern_id: str) -> Optional[InteractionPattern]:
    """获取交互模式"""
    return get_pattern_registry().get(pattern_id)


def list_patterns(category: PatternCategory = None) -> List[InteractionPattern]:
    """
    列出交互模式

    Args:
        category: 指定分类，None 表示全部

    Returns:
        交互模式列表
    """
    if category:
        return get_pattern_registry().list_by_category(category)
    return get_pattern_registry().list_all()


def search_patterns(keyword: str) -> List[InteractionPattern]:
    """搜索交互模式"""
    return get_pattern_registry().search(keyword)


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "PatternCategory",
    # 数据类
    "InteractionPattern",
    # 管理器
    "PatternRegistry",
    "get_pattern_registry",
    # 便捷函数
    "get_pattern",
    "list_patterns",
    "search_patterns",
]
