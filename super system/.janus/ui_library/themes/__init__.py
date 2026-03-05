"""
Themes - 主题系统模块
====================

管理UI组件库的主题配置，支持：
- 颜色方案定制
- 字体排版配置
- 间距和尺寸系统
- 动态主题切换

主题结构:
    - 颜色变量 (primary, secondary, success, warning, danger, etc.)
    - 排版变量 (font_family, font_size, line_height, etc.)
    - 间距变量 (spacing scale)
    - 效果变量 (shadow, border, transition)

子模块:
    - definitions: 15个主题定义
    - engine: 主题引擎和应用函数
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field


# ============================================================================
# 主题数据类
# ============================================================================

@dataclass
class ColorScheme:
    """颜色方案配置"""
    primary: str = "#007bff"
    secondary: str = "#6c757d"
    success: str = "#28a745"
    warning: str = "#ffc107"
    danger: str = "#dc3545"
    info: str = "#17a2b8"
    light: str = "#f8f9fa"
    dark: str = "#343a40"
    white: str = "#ffffff"
    black: str = "#000000"
    gray: Dict[str, str] = field(default_factory=lambda: {
        "100": "#f8f9fa",
        "200": "#e9ecef",
        "300": "#dee2e6",
        "400": "#ced4da",
        "500": "#adb5bd",
        "600": "#6c757d",
        "700": "#495057",
        "800": "#343a40",
        "900": "#212529",
    })

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "success": self.success,
            "warning": self.warning,
            "danger": self.danger,
            "info": self.info,
            "light": self.light,
            "dark": self.dark,
            "white": self.white,
            "black": self.black,
            "gray": self.gray,
        }


@dataclass
class Typography:
    """排版配置"""
    font_family: str = "system-ui, -apple-system, sans-serif"
    font_size_base: str = "16px"
    font_size_scale: float = 1.125  # Major third (type) scale
    line_height: float = 1.5
    font_weight: Dict[str, int] = field(default_factory=lambda: {
        "light": 300,
        "normal": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700,
    })

    def get_font_size(self, level: int) -> str:
        """
        获取指定级别的字号

        Args:
            level: 级别 (0-6)

        Returns:
            字号字符串
        """
        base_size = float(self.font_size_base.replace("px", ""))
        size = base_size * (self.font_size_scale ** level)
        return f"{size:.2f}px"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "font_family": self.font_family,
            "font_size_base": self.font_size_base,
            "font_size_scale": self.font_size_scale,
            "line_height": self.line_height,
            "font_weight": self.font_weight,
        }


@dataclass
class Spacing:
    """间距配置"""
    unit: str = "8px"  # 基础间距单位
    scale: float = 1.5  # 间距缩放比例

    def get_spacing(self, level: int) -> str:
        """
        获取指定级别的间距

        Args:
            level: 级别 (0-10)

        Returns:
            间距字符串
        """
        base_size = float(self.unit.replace("px", ""))
        size = base_size * (self.scale ** level)
        return f"{size:.2f}px"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "unit": self.unit,
            "scale": self.scale,
        }


@dataclass
class Border:
    """边框配置"""
    radius: Dict[str, str] = field(default_factory=lambda: {
        "none": "0",
        "sm": "2px",
        "md": "4px",
        "lg": "8px",
        "xl": "12px",
        "full": "9999px",
    })
    width: Dict[str, str] = field(default_factory=lambda: {
        "thin": "1px",
        "normal": "2px",
        "thick": "4px",
    })

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "radius": self.radius,
            "width": self.width,
        }


@dataclass
class Shadow:
    """阴影配置"""
    levels: Dict[str, str] = field(default_factory=lambda: {
        "none": "none",
        "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
        "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
        "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
    })

    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {"levels": self.levels}


# ============================================================================
# 简化的主题类（保留向后兼容）
# ============================================================================

@dataclass
class Theme:
    """
    主题配置类（简化版，用于向后兼容）

    完整的主题定义请使用 definitions.py 中的 Theme 类
    """
    name: str
    description: str = ""
    mode: str = "light"
    colors: ColorScheme = field(default_factory=ColorScheme)
    typography: Typography = field(default_factory=Typography)
    spacing: Spacing = field(default_factory=Spacing)
    border: Border = field(default_factory=Border)
    shadow: Shadow = field(default_factory=Shadow)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "mode": self.mode,
            "colors": self.colors.to_dict(),
            "typography": self.typography.to_dict(),
            "spacing": self.spacing.to_dict(),
            "border": self.border.to_dict(),
            "shadow": self.shadow.to_dict(),
        }

    def to_css_variables(self) -> str:
        """
        生成CSS变量定义

        Returns:
            CSS变量字符串
        """
        lines = [f":root {{{self.name}-theme} {{"]
        lines.append("  /* Colors */")

        # 颜色变量
        colors = self.colors
        lines.append(f"  --color-primary: {colors.primary};")
        lines.append(f"  --color-secondary: {colors.secondary};")
        lines.append(f"  --color-success: {colors.success};")
        lines.append(f"  --color-warning: {colors.warning};")
        lines.append(f"  --color-danger: {colors.danger};")
        lines.append(f"  --color-info: {colors.info};")

        # 灰度
        for shade, value in colors.gray.items():
            lines.append(f"  --color-gray-{shade}: {value};")

        # 排版变量
        lines.append("\n  /* Typography */")
        lines.append(f"  --font-family: {self.typography.font_family};")
        lines.append(f"  --font-size-base: {self.typography.font_size_base};")
        lines.append(f"  --line-height: {self.typography.line_height};")

        for i in range(7):
            lines.append(f"  --font-size-{i}: {self.typography.get_font_size(i)};")

        # 间距变量
        lines.append("\n  /* Spacing */")
        for i in range(11):
            lines.append(f"  --spacing-{i}: {self.spacing.get_spacing(i)};")

        # 边框变量
        lines.append("\n  /* Border */")
        for name, value in self.border.radius.items():
            lines.append(f"  --border-radius-{name}: {value};")

        # 阴影变量
        lines.append("\n  /* Shadow */")
        for name, value in self.shadow.levels.items():
            lines.append(f"  --shadow-{name}: {value};")

        lines.append("}")
        return "\n".join(lines)


# ============================================================================
# 主题管理器
# ============================================================================

class ThemeManager:
    """主题管理器"""

    def __init__(self):
        self._themes: Dict[str, Theme] = {}
        self._current_theme: Optional[str] = None
        self._register_default_themes()

    def _register_default_themes(self):
        """注册默认主题"""
        # Light theme
        light = Theme(
            name="light",
            description="明亮主题，适合日间使用",
            mode="light",
            colors=ColorScheme(
                primary="#007bff",
                secondary="#6c757d",
                success="#28a745",
                warning="#ffc107",
                danger="#dc3545",
                info="#17a2b8",
                light="#f8f9fa",
                dark="#343a40",
            ),
        )
        self.register(light)

        # Dark theme
        dark = Theme(
            name="dark",
            description="暗黑主题，适合夜间使用",
            mode="dark",
            colors=ColorScheme(
                primary="#0d6efd",
                secondary="#6c757d",
                success="#198754",
                warning="#ffc107",
                danger="#dc3545",
                info="#0dcaf0",
                light="#212529",
                dark="#f8f9fa",
            ),
        )
        self.register(dark)

        # Set default
        self.set_current("light")

    def register(self, theme: Theme):
        """
        注册主题

        Args:
            theme: 主题实例
        """
        self._themes[theme.name] = theme

    def get(self, name: str) -> Optional[Theme]:
        """
        获取主题

        Args:
            name: 主题名称

        Returns:
            主题实例，不存在则返回 None
        """
        return self._themes.get(name)

    def set_current(self, name: str):
        """
        设置当前主题

        Args:
            name: 主题名称
        """
        if name not in self._themes:
            raise ValueError(f"主题不存在: {name}")
        self._current_theme = name

    def get_current(self) -> Optional[Theme]:
        """
        获取当前主题

        Returns:
            当前主题实例
        """
        if self._current_theme:
            return self._themes.get(self._current_theme)
        return None

    def list_themes(self) -> list[str]:
        """返回所有已注册的主题名称"""
        return list(self._themes.keys())


# ============================================================================
# 全局主题管理器实例
# ============================================================================

_default_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """
    获取全局主题管理器（单例模式）

    Returns:
        ThemeManager 实例
    """
    global _default_manager
    if _default_manager is None:
        _default_manager = ThemeManager()
    return _default_manager


def get_current_theme() -> Optional[Theme]:
    """获取当前主题"""
    return get_theme_manager().get_current()


def set_theme(name: str):
    """设置当前主题"""
    get_theme_manager().set_current(name)


# ============================================================================
# 导入新模块
# ============================================================================

# 导入主题定义
from .definitions import (
    # 枚举
    ThemeMode,
    ThemeCategory,
    # 15个主题定义
    DEFAULT_LIGHT,
    DEFAULT_DARK,
    OCEAN_BLUE,
    FOREST_GREEN,
    SUNSET_ORANGE,
    BERRY_PURPLE,
    CORPORATE_GRAY,
    TECH_NEON,
    WARM_EARTH,
    COOL_MINT,
    ROSE_GOLD,
    MIDNIGHT_BLUE,
    AUTUMN_MAPLE,
    SPRING_BLOSSOM,
    ARCTIC_FROST,
    # 主题注册表和便捷函数
    THEME_REGISTRY,
    get_theme,
    list_themes,
    get_light_themes,
    get_dark_themes,
    search_themes,
)

# 导入主题引擎
from .engine import (
    # 引擎类
    ThemeEngine,
    # 全局实例
    get_theme_engine,
    # Streamlit 集成
    render_theme_switcher,
    render_theme_preview,
    apply_theme_to_page,
    # 便捷函数
    switch_theme,
    get_current_theme_id,
    get_theme_css,
    export_current_theme,
    create_theme_presets,
    # 页面组件
    theme_settings_page,
)


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 原有数据类（向后兼容）
    "ColorScheme",
    "Typography",
    "Spacing",
    "Border",
    "Shadow",
    "Theme",
    # 原有管理器（向后兼容）
    "ThemeManager",
    "get_theme_manager",
    "get_current_theme",
    "set_theme",
    # ===== 新增：主题定义 =====
    # 枚举
    "ThemeMode",
    "ThemeCategory",
    # 15个主题
    "DEFAULT_LIGHT",
    "DEFAULT_DARK",
    "OCEAN_BLUE",
    "FOREST_GREEN",
    "SUNSET_ORANGE",
    "BERRY_PURPLE",
    "CORPORATE_GRAY",
    "TECH_NEON",
    "WARM_EARTH",
    "COOL_MINT",
    "ROSE_GOLD",
    "MIDNIGHT_BLUE",
    "AUTUMN_MAPLE",
    "SPRING_BLOSSOM",
    "ARCTIC_FROST",
    # 注册表和函数
    "THEME_REGISTRY",
    "get_theme",
    "list_themes",
    "get_light_themes",
    "get_dark_themes",
    "search_themes",
    # ===== 新增：主题引擎 =====
    # 引擎类
    "ThemeEngine",
    "get_theme_engine",
    # Streamlit 集成
    "render_theme_switcher",
    "render_theme_preview",
    "apply_theme_to_page",
    # 便捷函数
    "switch_theme",
    "get_current_theme_id",
    "get_theme_css",
    "export_current_theme",
    "create_theme_presets",
    # 页面组件
    "theme_settings_page",
]
