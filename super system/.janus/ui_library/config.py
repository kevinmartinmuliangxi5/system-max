"""
UI Library Configuration - 全局配置模块
========================================

定义UI组件库的全局配置，包括：
- 支持的前端框架
- 支持的行业类型
- 主题元数据和默认配置
- 组件分类体系
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json


# ============================================================================
# 前端框架配置
# ============================================================================

SUPPORTED_FRAMEWORKS = {
    "react": {
        "name": "React",
        "version": "18.x",
        "file_extension": ".jsx",
        "style_extension": ".css",
        "component_pattern": "functional",
        "hooks": True,
        "tsx_support": True,
        "description": "使用 React Hooks 的函数式组件",
    },
    "vue": {
        "name": "Vue.js",
        "version": "3.x",
        "file_extension": ".vue",
        "style_extension": ".scss",
        "component_pattern": "composition",
        "hooks": True,
        "tsx_support": True,
        "description": "Vue 3 Composition API",
    },
    "vanilla": {
        "name": "Vanilla JS",
        "version": "ES6+",
        "file_extension": ".js",
        "style_extension": ".css",
        "component_pattern": "class",
        "hooks": False,
        "tsx_support": False,
        "description": "原生 JavaScript，无框架依赖",
    },
}


# ============================================================================
# 行业类型配置
# ============================================================================

SUPPORTED_INDUSTRIES = {
    "general": {
        "name": "通用",
        "description": "适用于大多数场景的通用组件",
        "color_scheme": ["#007bff", "#6c757d", "#28a745"],
        "typography": {"font_family": "system-ui, sans-serif"},
    },
    "healthcare": {
        "name": "医疗健康",
        "description": "医疗行业专用组件，强调清晰度和专业性",
        "color_scheme": ["#17a2b8", "#138496", "#0d6efd"],
        "typography": {"font_family": "Helvetica Neue, Arial, sans-serif"},
        "specific_components": ["patient_form", "medical_chart", "appointment_scheduler"],
    },
    "finance": {
        "name": "金融服务",
        "description": "金融行业组件，强调数据可视化和安全性",
        "color_scheme": ["#28a745", "#20c997", "#007bff"],
        "typography": {"font_family": "Roboto, sans-serif"},
        "specific_components": ["account_summary", "transaction_table", "risk_indicator"],
    },
    "ecommerce": {
        "name": "电子商务",
        "description": "电商行业组件，强调转化率和用户体验",
        "color_scheme": ["#fd7e14", "#dc3545", "#ffc107"],
        "typography": {"font_family": "Inter, sans-serif"},
        "specific_components": ["product_card", "shopping_cart", "checkout_flow"],
    },
    "education": {
        "name": "教育培训",
        "description": "教育行业组件，强调互动性和易用性",
        "color_scheme": ["#6610f2", "#6f42c1", "#e83e8c"],
        "typography": {"font_family": "Nunito, sans-serif"},
        "specific_components": ["course_card", "quiz_interface", "progress_tracker"],
    },
    "manufacturing": {
        "name": "制造业",
        "description": "制造业组件，强调生产流程和数据监控",
        "color_scheme": ["#343a40", "#495057", "#6c757d"],
        "typography": {"font_family": "Segoe UI, sans-serif"},
        "specific_components": ["production_dashboard", "quality_control", "inventory_table"],
    },
}


# ============================================================================
# 组件分类体系
# ============================================================================

COMPONENT_CATEGORIES = {
    "layout": {
        "name": "布局组件",
        "description": "页面结构和布局相关组件",
        "icon": "layout",
    },
    "form": {
        "name": "表单组件",
        "description": "数据输入和表单相关组件",
        "icon": "edit",
    },
    "data": {
        "name": "数据展示",
        "description": "数据可视化和表格相关组件",
        "icon": "table",
    },
    "navigation": {
        "name": "导航组件",
        "description": "页面导航和路由相关组件",
        "icon": "compass",
    },
    "feedback": {
        "name": "反馈组件",
        "description": "用户反馈和状态提示组件",
        "icon": "bell",
    },
    "media": {
        "name": "媒体组件",
        "description": "图片、视频等媒体相关组件",
        "icon": "image",
    },
}


COMPONENT_SIZE = {
    "large": {
        "name": "大型组件",
        "description": "复杂的功能模块，包含多个子组件",
        "lines_of_code": "> 500",
        "examples": ["Dashboard", "DataGrid", "FormBuilder"],
    },
    "medium": {
        "name": "中型组件",
        "description": "单一功能组件，可独立使用",
        "lines_of_code": "100 - 500",
        "examples": ["Button", "Input", "Modal", "Dropdown"],
    },
    "small": {
        "name": "小型组件",
        "description": "基础UI元素，通常组合使用",
        "lines_of_code": "< 100",
        "examples": ["Icon", "Badge", "Spinner", "Divider"],
    },
}


# ============================================================================
# 主题元数据配置
# ============================================================================

THEME_METADATA = {
    "color": {
        "primary": "主题主色，用于主要操作和强调",
        "secondary": "主题次要色，用于辅助操作",
        "success": "成功状态色",
        "warning": "警告状态色",
        "danger": "危险状态色",
        "info": "信息状态色",
        "light": "浅色背景",
        "dark": "深色背景",
    },
    "typography": {
        "font_family": "主字体族",
        "font_size_base": "基础字号",
        "line_height": "行高",
        "font_weight": "字重",
    },
    "spacing": {
        "unit": "间距单位基数",
        "scale": "间距缩放比例",
    },
    "border": {
        "radius": "圆角大小",
        "width": "边框宽度",
    },
    "shadow": {
        "level": "阴影级别 (0-5)",
    },
}


# ============================================================================
# 默认主题定义
# ============================================================================

DEFAULT_THEMES = {
    "light": {
        "name": "明亮主题",
        "colors": {
            "primary": "#007bff",
            "secondary": "#6c757d",
            "success": "#28a745",
            "warning": "#ffc107",
            "danger": "#dc3545",
            "info": "#17a2b8",
            "light": "#f8f9fa",
            "dark": "#343a40",
        },
        "typography": {
            "font_family": "system-ui, -apple-system, sans-serif",
            "font_size_base": "16px",
            "line_height": 1.5,
        },
    },
    "dark": {
        "name": "暗黑主题",
        "colors": {
            "primary": "#0d6efd",
            "secondary": "#6c757d",
            "success": "#198754",
            "warning": "#ffc107",
            "danger": "#dc3545",
            "info": "#0dcaf0",
            "light": "#212529",
            "dark": "#f8f9fa",
        },
        "typography": {
            "font_family": "system-ui, -apple-system, sans-serif",
            "font_size_base": "16px",
            "line_height": 1.5,
        },
    },
}


# ============================================================================
# 推荐引擎配置
# ============================================================================

RECOMMENDATION_CONFIG = {
    "weights": {
        "industry_match": 0.4,      # 行业匹配权重
        "framework_compatibility": 0.3,  # 框架兼容性权重
        "usage_frequency": 0.2,     # 使用频率权重
        "user_rating": 0.1,         # 用户评分权重
    },
    "threshold": 0.5,              # 推荐阈值
    "max_results": 10,             # 最大推荐结果数
}


# ============================================================================
# 配置类
# ============================================================================

@dataclass
class Config:
    """
    UI库全局配置类

    Attributes:
        default_framework: 默认前端框架
        default_industry: 默认行业类型
        default_theme: 默认主题
        component_cache_enabled: 是否启用组件缓存
        recommendation_enabled: 是否启用智能推荐
    """
    default_framework: str = "react"
    default_industry: str = "general"
    default_theme: str = "light"
    component_cache_enabled: bool = True
    recommendation_enabled: bool = True

    # 路径配置
    base_dir: Path = field(default_factory=lambda: Path(__file__).parent)
    components_dir: Path = field(init=False)
    themes_dir: Path = field(init=False)
    patterns_dir: Path = field(init=False)
    industries_dir: Path = field(init=False)
    docs_dir: Path = field(init=False)

    # 自定义扩展
    custom_frameworks: Dict[str, Any] = field(default_factory=dict)
    custom_industries: Dict[str, Any] = field(default_factory=dict)
    custom_themes: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """初始化路径配置"""
        self.components_dir = self.base_dir / "components"
        self.themes_dir = self.base_dir / "themes"
        self.patterns_dir = self.base_dir / "patterns"
        self.industries_dir = self.base_dir / "industries"
        self.docs_dir = self.base_dir / "docs"

    def validate(self) -> bool:
        """
        验证配置是否有效

        Returns:
            配置是否有效
        """
        if self.default_framework not in SUPPORTED_FRAMEWORKS:
            raise ValueError(f"不支持的框架: {self.default_framework}")

        if self.default_industry not in SUPPORTED_INDUSTRIES:
            raise ValueError(f"不支持的行业: {self.default_industry}")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """将配置转换为字典"""
        return {
            "default_framework": self.default_framework,
            "default_industry": self.default_industry,
            "default_theme": self.default_theme,
            "component_cache_enabled": self.component_cache_enabled,
            "recommendation_enabled": self.recommendation_enabled,
        }

    @classmethod
    def from_file(cls, config_path: Path) -> "Config":
        """
        从JSON文件加载配置

        Args:
            config_path: 配置文件路径

        Returns:
            Config 实例
        """
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    def save_to_file(self, config_path: Path):
        """
        保存配置到JSON文件

        Args:
            config_path: 配置文件路径
        """
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


# ============================================================================
# 全局配置实例
# ============================================================================

_global_config: Optional[Config] = None


def get_config() -> Config:
    """
    获取全局配置实例（单例模式）

    Returns:
        Config 实例
    """
    global _global_config
    if _global_config is None:
        _global_config = Config()
        _global_config.validate()
    return _global_config


def set_config(config: Config):
    """
    设置全局配置

    Args:
        config: 新的配置实例
    """
    global _global_config
    config.validate()
    _global_config = config


def reset_config():
    """重置为默认配置"""
    global _global_config
    _global_config = Config()
    _global_config.validate()


# ============================================================================
# 辅助函数
# ============================================================================

def get_framework_info(framework: str) -> Optional[Dict[str, Any]]:
    """
    获取框架信息

    Args:
        framework: 框架名称

    Returns:
        框架信息字典，如果框架不存在则返回 None
    """
    return SUPPORTED_FRAMEWORKS.get(framework)


def get_industry_info(industry: str) -> Optional[Dict[str, Any]]:
    """
    获取行业信息

    Args:
        industry: 行业名称

    Returns:
        行业信息字典，如果行业不存在则返回 None
    """
    return SUPPORTED_INDUSTRIES.get(industry)


def get_theme_colors(theme_name: str) -> Optional[Dict[str, str]]:
    """
    获取主题颜色配置

    Args:
        theme_name: 主题名称

    Returns:
        颜色配置字典
    """
    theme = DEFAULT_THEMES.get(theme_name)
    return theme["colors"] if theme else None


def list_available_themes() -> List[str]:
    """返回所有可用主题名称"""
    return list(DEFAULT_THEMES.keys())


def list_available_categories() -> List[str]:
    """返回所有组件分类"""
    return list(COMPONENT_CATEGORIES.keys())


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 配置常量
    "SUPPORTED_FRAMEWORKS",
    "SUPPORTED_INDUSTRIES",
    "COMPONENT_CATEGORIES",
    "COMPONENT_SIZE",
    "THEME_METADATA",
    "DEFAULT_THEMES",
    "RECOMMENDATION_CONFIG",
    # 配置类
    "Config",
    "get_config",
    "set_config",
    "reset_config",
    # 辅助函数
    "get_framework_info",
    "get_industry_info",
    "get_theme_colors",
    "list_available_themes",
    "list_available_categories",
]
