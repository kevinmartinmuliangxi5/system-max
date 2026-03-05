"""
Components - UI组件库模块
========================

包含所有UI组件的定义和实现。

组件分类:
    - layout/: 布局组件（容器、栅格、分割面板等）
    - form/: 表单组件（输入框、选择器、表单容器等）
    - data/: 数据展示组件（表格、图表、卡片等）
    - navigation/: 导航组件（菜单、面包屑、标签页等）
    - feedback/: 反馈组件（提示、弹窗、加载状态等）
    - media/: 媒体组件（图片、视频、文件上传等）

组件规模:
    - Large (大型): 复杂功能模块，>500行代码
    - Medium (中型): 单一功能组件，100-500行代码
    - Small (小型): 基础UI元素，<100行代码
"""

from .registry import ComponentRegistry, ComponentMetadata
from .base import BaseComponent, ComponentProps

__all__ = [
    "ComponentRegistry",
    "ComponentMetadata",
    "BaseComponent",
    "ComponentProps",
]


# ============================================================================
# 组件导入（延迟加载）
# ============================================================================

def _load_layout_components():
    """加载布局组件"""
    from . import layout
    return layout.__all__


def _load_form_components():
    """加载表单组件"""
    from . import form
    return form.__all__


def _load_data_components():
    """加载数据展示组件"""
    from . import data
    return data.__all__


def _load_navigation_components():
    """加载导航组件"""
    from . import navigation
    return navigation.__all__


def _load_feedback_components():
    """加载反馈组件"""
    from . import feedback
    return feedback.__all__


def _load_media_components():
    """加载媒体组件"""
    from . import media
    return media.__all__


# ============================================================================
# 组件分类映射
# ============================================================================

CATEGORY_MODULES = {
    "layout": _load_layout_components,
    "form": _load_form_components,
    "data": _load_data_components,
    "navigation": _load_navigation_components,
    "feedback": _load_feedback_components,
    "media": _load_media_components,
}


def get_components_by_category(category: str):
    """
    按分类获取组件列表

    Args:
        category: 组件分类名称

    Returns:
        该分类下的所有组件
    """
    loader = CATEGORY_MODULES.get(category)
    if loader:
        try:
            return loader()
        except ImportError:
            return []
    return []


def list_all_categories():
    """返回所有组件分类"""
    return list(CATEGORY_MODULES.keys())


def get_component_count(category: str = None) -> int:
    """
    获取组件数量

    Args:
        category: 指定分类，None 表示总数

    Returns:
        组件数量
    """
    if category:
        components = get_components_by_category(category)
        return len(components) if components else 0

    total = 0
    for cat in CATEGORY_MODULES:
        total += get_component_count(cat)
    return total
