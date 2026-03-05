"""
Theme Definitions - 主题定义系统
==============================

定义 15 个主题配色方案和样式变量。

主题列表:
    1. default_light - 默认浅色
    2. default_dark - 默认深色
    3. ocean_blue - 海洋蓝
    4. forest_green - 森林绿
    5. sunset_orange - 日落橙
    6. berry_purple - 浆果紫
    7. corporate_gray - 商务灰
    8. tech_neon - 科技霓虹
    9. warm_earth - 暖土色
    10. cool_mint - 清凉薄荷
    11. rose_gold - 玫瑰金
    12. midnight_blue - 午夜蓝
    13. autumn_maple - 秋枫红
    14. spring_blossom - 春樱粉
    15. arctic_frost - 极地霜
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# 主题模式枚举
# ============================================================================

class ThemeMode(Enum):
    """主题模式"""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


class ThemeCategory(Enum):
    """主题分类"""
    DEFAULT = "default"           # 默认主题
    NATURE = "nature"             # 自然风格
    PROFESSIONAL = "professional" # 专业风格
    VIBRANT = "vibrant"           # 活力风格
    SEASONAL = "seasonal"         # 季节主题
    CUSTOM = "custom"             # 自定义主题


# ============================================================================
# 颜色定义
# ============================================================================

@dataclass
class ColorPalette:
    """
    颜色调色板

    Attributes:
        primary: 主色调
        secondary: 次要色调
        background: 背景色
        surface: 表面色（卡片、面板）
        text: 主文本色
        text_secondary: 次要文本色
        accent: 强调色
        success: 成功色
        warning: 警告色
        error: 错误色
        info: 信息色
        border: 边框色
        divider: 分割线色
    """
    primary: str
    secondary: str
    background: str
    surface: str
    text: str
    text_secondary: str
    accent: str
    success: str
    warning: str
    error: str
    info: str
    border: str
    divider: str

    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "background": self.background,
            "surface": self.surface,
            "text": self.text,
            "text_secondary": self.text_secondary,
            "accent": self.accent,
            "success": self.success,
            "warning": self.warning,
            "error": self.error,
            "info": self.info,
            "border": self.border,
            "divider": self.divider,
        }

    def get_css_variables(self) -> str:
        """生成 CSS 变量"""
        return f"""
--color-primary: {self.primary};
--color-secondary: {self.secondary};
--color-background: {self.background};
--color-surface: {self.surface};
--color-text: {self.text};
--color-text-secondary: {self.text_secondary};
--color-accent: {self.accent};
--color-success: {self.success};
--color-warning: {self.warning};
--color-error: {self.error};
--color-info: {self.info};
--color-border: {self.border};
--color-divider: {self.divider};
"""


# ============================================================================
# 灰度色阶
# ============================================================================

@dataclass
class GrayScale:
    """
    灰度色阶

    Attributes:
        gray_50 to gray_900: 从浅到深的灰色
    """
    gray_50: str = "#fafafa"
    gray_100: str = "#f5f5f5"
    gray_200: str = "#eeeeee"
    gray_300: str = "#e0e0e0"
    gray_400: str = "#bdbdbd"
    gray_500: str = "#9e9e9e"
    gray_600: str = "#757575"
    gray_700: str = "#616161"
    gray_800: str = "#424242"
    gray_900: str = "#212121"

    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {
            "gray_50": self.gray_50,
            "gray_100": self.gray_100,
            "gray_200": self.gray_200,
            "gray_300": self.gray_300,
            "gray_400": self.gray_400,
            "gray_500": self.gray_500,
            "gray_600": self.gray_600,
            "gray_700": self.gray_700,
            "gray_800": self.gray_800,
            "gray_900": self.gray_900,
        }


# ============================================================================
# 排版配置
# ============================================================================

@dataclass
class Typography:
    """
    排版配置

    Attributes:
        font_family: 主字体
        font_family_code: 代码字体
        font_size_base: 基础字号
        line_height: 行高
        letter_spacing: 字间距
        font_weights: 字重配置
    """
    font_family: str
    font_family_code: str
    font_size_base: int
    line_height: float
    letter_spacing: float
    font_weights: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "font_family": self.font_family,
            "font_family_code": self.font_family_code,
            "font_size_base": self.font_size_base,
            "line_height": self.line_height,
            "letter_spacing": self.letter_spacing,
            "font_weights": self.font_weights,
        }


# ============================================================================
# 间距和尺寸
# ============================================================================

@dataclass
class Spacing:
    """
    间距配置

    Attributes:
        unit: 基础间距单位（像素）
        scale: 间距缩放比例
    """
    unit: int = 8
    scale: float = 1.5

    def get_spacing(self, level: int) -> int:
        """
        获取指定级别的间距

        Args:
            level: 级别 (0-10)

        Returns:
            间距像素值
        """
        return int(self.unit * (self.scale ** level))

    def to_dict(self) -> Dict[str, int]:
        """返回常用间距字典"""
        return {
            f"spacing_{i}": self.get_spacing(i)
            for i in range(11)
        }


# ============================================================================
# 边框和阴影
# ============================================================================

@dataclass
class Border:
    """
    边框配置

    Attributes:
        radius: 圆角配置
        width: 边框宽度
    """
    radius_sm: int = 4
    radius_md: int = 8
    radius_lg: int = 12
    radius_xl: int = 16
    radius_full: int = 9999
    width_thin: int = 1
    width_normal: int = 2
    width_thick: int = 4

    def to_dict(self) -> Dict[str, int]:
        """转换为字典"""
        return {
            "radius_sm": self.radius_sm,
            "radius_md": self.radius_md,
            "radius_lg": self.radius_lg,
            "radius_xl": self.radius_xl,
            "radius_full": self.radius_full,
            "width_thin": self.width_thin,
            "width_normal": self.width_normal,
            "width_thick": self.width_thick,
        }


@dataclass
class Shadow:
    """
    阴影配置

    Attributes:
        levels: 阴影级别定义
    """
    none: str = "none"
    sm: str = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: str = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    lg: str = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
    xl: str = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
    xxl: str = "0 25px 50px -12px rgba(0, 0, 0, 0.25)"

    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {
            "none": self.none,
            "sm": self.sm,
            "md": self.md,
            "lg": self.lg,
            "xl": self.xl,
            "xxl": self.xxl,
        }


# ============================================================================
# 完整主题定义
# ============================================================================

@dataclass
class Theme:
    """
    完整主题定义

    Attributes:
        id: 主题唯一标识符
        name: 主题名称
        description: 主题描述
        mode: 主题模式
        category: 主题分类
        colors: 颜色调色板
        grays: 灰度色阶
        typography: 排版配置
        spacing: 间距配置
        border: 边框配置
        shadow: 阴影配置
        custom_vars: 自定义变量
    """
    id: str
    name: str
    description: str
    mode: ThemeMode
    category: ThemeCategory
    colors: ColorPalette
    grays: GrayScale = field(default_factory=GrayScale)
    typography: Typography = field(default_factory=lambda: Typography(
        font_family="system-ui, -apple-system, sans-serif",
        font_family_code="Monaco, Consolas, monospace",
        font_size_base=16,
        line_height=1.5,
        letter_spacing=0.0
    ))
    spacing: Spacing = field(default_factory=Spacing)
    border: Border = field(default_factory=Border)
    shadow: Shadow = field(default_factory=Shadow)
    custom_vars: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为完整字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "mode": self.mode.value,
            "category": self.category.value,
            "colors": self.colors.to_dict(),
            "grays": self.grays.to_dict(),
            "typography": self.typography.to_dict(),
            "spacing": self.spacing.to_dict(),
            "border": self.border.to_dict(),
            "shadow": self.shadow.to_dict(),
            "custom_vars": self.custom_vars,
        }

    def get_full_css(self) -> str:
        """
        获取完整的 CSS 变量定义

        Returns:
            CSS 变量字符串
        """
        lines = [":root {"]
        lines.append("/* 颜色 */")
        lines.append(self.colors.get_css_variables())

        lines.append("/* 灰度 */")
        for i in range(50, 1000, 50):
            attr = f"gray_{i}"
            value = getattr(self.grays, f"gray_{i}", "")
            lines.append(f"--color-gray-{i}: {value};")

        lines.append("/* 排版 */")
        lines.append(f"--font-family: {self.typography.font_family};")
        lines.append(f"--font-family-code: {self.typography.font_family_code};")
        lines.append(f"--font-size-base: {self.typography.font_size_base}px;")
        lines.append(f"--line-height: {self.typography.line_height};")

        lines.append("/* 间距 */")
        for i in range(11):
            lines.append(f"--spacing-{i}: {self.spacing.get_spacing(i)}px;")

        lines.append("/* 边框 */")
        lines.append(f"--border-radius-sm: {self.border.radius_sm}px;")
        lines.append(f"--border-radius-md: {self.border.radius_md}px;")
        lines.append(f"--border-radius-lg: {self.border.radius_lg}px;")

        lines.append("/* 阴影 */")
        lines.append(f"--shadow-sm: {self.shadow.sm};")
        lines.append(f"--shadow-md: {self.shadow.md};")
        lines.append(f"--shadow-lg: {self.shadow.lg};")

        # 自定义变量
        if self.custom_vars:
            lines.append("/* 自定义 */")
            for key, value in self.custom_vars.items():
                lines.append(f"--{key}: {value};")

        lines.append("}")
        return "\n".join(lines)


# ============================================================================
# 1. 默认浅色主题
# ============================================================================

DEFAULT_LIGHT = Theme(
    id="default_light",
    name="默认浅色",
    description="简洁明快的浅色主题，适合日常使用",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.DEFAULT,
    colors=ColorPalette(
        primary="#007bff",
        secondary="#6c757d",
        background="#ffffff",
        surface="#f8f9fa",
        text="#212529",
        text_secondary="#6c757d",
        accent="#0d6efd",
        success="#28a745",
        warning="#ffc107",
        error="#dc3545",
        info="#17a2b8",
        border="#dee2e6",
        divider="#e9ecef"
    ),
    custom_vars={
        "brand-color": "#007bff",
        "link-color": "#007bff",
        "hover-bg": "#f8f9fa"
    }
)


# ============================================================================
# 2. 默认深色主题
# ============================================================================

DEFAULT_DARK = Theme(
    id="default_dark",
    name="默认深色",
    description="护眼舒适的深色主题，适合夜间使用",
    mode=ThemeMode.DARK,
    category=ThemeCategory.DEFAULT,
    colors=ColorPalette(
        primary="#0d6efd",
        secondary="#6c757d",
        background="#1e1e1e",
        surface="#2d2d2d",
        text="#e9ecef",
        text_secondary="#adb5bd",
        accent="#3d8bfd",
        success="#198754",
        warning="#ffc107",
        error="#dc3545",
        info="#0dcaf0",
        border="#495057",
        divider="#343a40"
    ),
    grays=GrayScale(
        gray_50="#212529",
        gray_100="#343a40",
        gray_200="#495057",
        gray_300="#adb5bd",
        gray_400="#ced4da",
        gray_500="#dee2e6",
        gray_600="#e9ecef",
        gray_700="#f8f9fa",
        gray_800="#ffffff",
        gray_900="#ffffff"
    )
)


# ============================================================================
# 3. 海洋蓝主题
# ============================================================================

OCEAN_BLUE = Theme(
    id="ocean_blue",
    name="海洋蓝",
    description="清新海洋风格，如沐海风",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.NATURE,
    colors=ColorPalette(
        primary="#0ea5e9",
        secondary="#0dcaf0",
        background="#f0f8ff",
        surface="#e7f3ff",
        text="#0c4a6e",
        text_secondary="#0369a1",
        accent="#0096c7",
        success="#20c997",
        warning="#fd7e14",
        error="#ef4444",
        info="#0dcaf0",
        border="#bae6fd",
        divider="#e0f2fe"
    ),
    custom_vars={
        "water-deep": "#00509d",
        "water-light": "#66d4ff"
    }
)


# ============================================================================
# 4. 森林绿主题
# ============================================================================

FOREST_GREEN = Theme(
    id="forest_green",
    name="森林绿",
    description="自然森林风格，清新护眼",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.NATURE,
    colors=ColorPalette(
        primary="#198754",
        secondary="#20c997",
        background="#f0fff4",
        surface="#e6ffea",
        text="#14532d",
        text_secondary="#166534",
        accent="#059669",
        success="#22c55e",
        warning="#eab308",
        error="#ef4444",
        info="#06b6d4",
        border="#bbf7d0",
        divider="#dcfce7"
    ),
    custom_vars={
        "leaf-dark": "#14532d",
        "leaf-light": "#86efac"
    }
)


# ============================================================================
# 5. 日落橙主题
# ============================================================================

SUNSET_ORANGE = Theme(
    id="sunset_orange",
    name="日落橙",
    description="温暖日落风格，活力满满",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.SEASONAL,
    colors=ColorPalette(
        primary="#ea580c",
        secondary="#f97316",
        background="#fff7ed",
        surface="#ffedd5",
        text="#7c2d12",
        text_secondary="#9a3412",
        accent="#c2410c",
        success="#16a34a",
        warning="#ca8a04",
        error="#dc2626",
        info="#0891b2",
        border="#fed7aa",
        divider="#ffedd5"
    ),
    custom_vars={
        "sun-core": "#fb923c",
        "sun-glow": "#fdba74"
    }
)


# ============================================================================
# 6. 浆果紫主题
# ============================================================================

BERRY_PURPLE = Theme(
    id="berry_purple",
    name="浆果紫",
    description="甜美浆果风格，优雅高贵",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.VIBRANT,
    colors=ColorPalette(
        primary="#9333ea",
        secondary="#a855f7",
        background="#faf5ff",
        surface="#f3e8ff",
        text="#581c87",
        text_secondary="#6b21a8",
        accent="#7e22ce",
        success="#16a34a",
        warning="#ca8a04",
        error="#dc2626",
        info="#0891b2",
        border="#e9d5ff",
        divider="#f3e8ff"
    ),
    custom_vars={
        "berry-dark": "#581c87",
        "berry-light": "#d8b4fe"
    }
)


# ============================================================================
# 7. 商务灰主题
# ============================================================================

CORPORATE_GRAY = Theme(
    id="corporate_gray",
    name="商务灰",
    description="专业商务风格，稳重可靠",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.PROFESSIONAL,
    colors=ColorPalette(
        primary="#475569",
        secondary="#64748b",
        background="#f8fafc",
        surface="#f1f5f9",
        text="#0f172a",
        text_secondary="#334155",
        accent="#334155",
        success="#16a34a",
        warning="#ca8a04",
        error="#dc2626",
        info="#0284c7",
        border="#e2e8f0",
        divider="#f1f5f9"
    ),
    typography=Typography(
        font_family="Inter, -apple-system, sans-serif",
        font_family_code="JetBrains Mono, monospace",
        font_size_base=14,
        line_height=1.6,
        letter_spacing=0.0
    ),
    custom_vars={
        "corporate-blue": "#1e40af",
        "corporate-navy": "#1e3a8a"
    }
)


# ============================================================================
# 8. 科技霓虹主题
# ============================================================================

TECH_NEON = Theme(
    id="tech_neon",
    name="科技霓虹",
    description="赛博朋克风格，炫酷科技",
    mode=ThemeMode.DARK,
    category=ThemeCategory.VIBRANT,
    colors=ColorPalette(
        primary="#00ff88",
        secondary="#00d9ff",
        background="#0a0e27",
        surface="#1a1f3a",
        text="#e0e7ff",
        text_secondary="#a5b4fc",
        accent="#ff00ff",
        success="#00ff88",
        warning="#ffcc00",
        error="#ff0055",
        info="#00d9ff",
        border="#312e81",
        divider="#1e1b4b"
    ),
    grays=GrayScale(
        gray_50="#1a1f3a",
        gray_100="#2d2d54",
        gray_200="#3d3d6d",
        gray_300="#52528a",
        gray_400="#6b6ba3",
        gray_500="#8585c1",
        gray_600="#9f9eda",
        gray_700="#babce8",
        gray_800="#d4d6f3",
        gray_900="#e0e7ff"
    ),
    custom_vars={
        "neon-pink": "#ff00ff",
        "neon-blue": "#00d9ff",
        "neon-green": "#00ff88"
    },
    shadow=Shadow(
        sm="0 0 5px rgba(0, 255, 136, 0.5)",
        md="0 0 10px rgba(0, 217, 255, 0.5)",
        lg="0 0 20px rgba(255, 0, 255, 0.3)",
        xl="0 0 30px rgba(0, 255, 136, 0.4)",
        xxl="0 0 40px rgba(0, 217, 255, 0.5)"
    )
)


# ============================================================================
# 9. 暖土色主题
# ============================================================================

WARM_EARTH = Theme(
    id="warm_earth",
    name="暖土色",
    description="温暖大地风格，自然舒适",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.NATURE,
    colors=ColorPalette(
        primary="#b45309",
        secondary="#d97706",
        background="#fffbeb",
        surface="#fef3c7",
        text="#78350f",
        text_secondary="#92400e",
        accent="#c2410c",
        success="#16a34a",
        warning="#ca8a04",
        error="#dc2626",
        info="#075985",
        border="#fde68a",
        divider="#fef3c7"
    ),
    custom_vars={
        "earth-brown": "#78350f",
        "earth-tan": "#d97706"
    }
)


# ============================================================================
# 10. 清凉薄荷主题
# ============================================================================

COOL_MINT = Theme(
    id="cool_mint",
    name="清凉薄荷",
    description="清新薄荷风格，凉爽怡人",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.NATURE,
    colors=ColorPalette(
        primary="#059669",
        secondary="#10b981",
        background="#f0fdf4",
        surface="#dcfce7",
        text="#14532d",
        text_secondary="#166534",
        accent="#047857",
        success="#22c55e",
        warning="#eab308",
        error="#ef4444",
        info="#06b6d4",
        border="#bbf7d0",
        divider="#dcfce7"
    ),
    custom_vars={
        "mint-dark": "#064e3b",
        "mint-light": "#6ee7b7"
    }
)


# ============================================================================
# 11. 玫瑰金主题
# ============================================================================

ROSE_GOLD = Theme(
    id="rose_gold",
    name="玫瑰金",
    description="优雅玫瑰风格，精致奢华",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.VIBRANT,
    colors=ColorPalette(
        primary="#e11d48",
        secondary="#f43f5e",
        background="#fff1f2",
        surface="#ffe4e6",
        text="#881337",
        text_secondary="#9f1239",
        accent="#be123c",
        success="#16a34a",
        warning="#ca8a04",
        error="#dc2626",
        info="#0891b2",
        border="#fecdd3",
        divider="#ffe4e6"
    ),
    border=Border(
        radius_sm=8,
        radius_md=16,
        radius_lg=20,
        radius_xl=24,
        radius_full=9999
    ),
    custom_vars={
        "rose-petals": "#fda4af",
        "gold-accent": "#fbbf24"
    }
)


# ============================================================================
# 12. 午夜蓝主题
# ============================================================================

MIDNIGHT_BLUE = Theme(
    id="midnight_blue",
    name="午夜蓝",
    description="深邃午夜风格，静谧优雅",
    mode=ThemeMode.DARK,
    category=ThemeCategory.PROFESSIONAL,
    colors=ColorPalette(
        primary="#3b82f6",
        secondary="#60a5fa",
        background="#0f172a",
        surface="#1e293b",
        text="#f1f5f9",
        text_secondary="#cbd5e1",
        accent="#2563eb",
        success="#10b981",
        warning="#f59e0b",
        error="#ef4444",
        info="#06b6d4",
        border="#334155",
        divider="#1e293b"
    ),
    grays=GrayScale(
        gray_50="#1e293b",
        gray_100="#334155",
        gray_200="#475569",
        gray_300="#64748b",
        gray_400="#94a3b8",
        gray_500="#cbd5e1",
        gray_600="#e2e8f0",
        gray_700="#f1f5f9",
        gray_800="#f8fafc",
        gray_900="#ffffff"
    ),
    custom_vars={
        "midnight-deep": "#020617",
        "midnight-light": "#475569"
    }
)


# ============================================================================
# 13. 秋枫红主题
# ============================================================================

AUTUMN_MAPLE = Theme(
    id="autumn_maple",
    name="秋枫红",
    description="金秋枫叶风格，温暖诗意",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.SEASONAL,
    colors=ColorPalette(
        primary="#dc2626",
        secondary="#ef4444",
        background="#fef2f2",
        surface="#fee2e2",
        text="#7f1d1d",
        text_secondary="#991b1b",
        accent="#b91c1c",
        success="#16a34a",
        warning="#ca8a04",
        error="#dc2626",
        info="#0891b2",
        border="#fecaca",
        divider="#fee2e2"
    ),
    custom_vars={
        "maple-red": "#b91c1c",
        "maple-orange": "#f97316",
        "autumn-gold": "#f59e0b"
    }
)


# ============================================================================
# 14. 春樱粉主题
# ============================================================================

SPRING_BLOSSOM = Theme(
    id="spring_blossom",
    name="春樱粉",
    description="浪漫春樱风格，柔美温馨",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.SEASONAL,
    colors=ColorPalette(
        primary="#db2777",
        secondary="#ec4899",
        background="#fdf2f8",
        surface="#fce7f3",
        text="#831843",
        text_secondary="#9d174d",
        accent="#be185d",
        success="#16a34a",
        warning="#ca8a04",
        error="#dc2626",
        info="#0891b2",
        border="#fbcfe8",
        divider="#fce7f3"
    ),
    border=Border(
        radius_sm=12,
        radius_md=16,
        radius_lg=20,
        radius_xl=24,
        radius_full=9999
    ),
    custom_vars={
        "sakura-pink": "#f472b6",
        "sakura-light": "#fbcfe8"
    }
)


# ============================================================================
# 15. 极地霜主题
# ============================================================================

ARCTIC_FROST = Theme(
    id="arctic_frost",
    name="极地霜",
    description="冰雪极地风格，清爽纯净",
    mode=ThemeMode.LIGHT,
    category=ThemeCategory.SEASONAL,
    colors=ColorPalette(
        primary="#0284c7",
        secondary="#0369a1",
        background="#f0f9ff",
        surface="#e0f2fe",
        text="#0c4a6e",
        text_secondary="#075985",
        accent="#0284c7",
        success="#16a34a",
        warning="#eab308",
        error="#dc2626",
        info="#0891b2",
        border="#bae6fd",
        divider="#e0f2fe"
    ),
    custom_vars={
        "frost-white": "#e0f2fe",
        "ice-blue": "#7dd3fc",
        "arctic-deep": "#075985"
    }
)


# ============================================================================
# 主题注册表
# ============================================================================

THEME_REGISTRY = {
    "default_light": DEFAULT_LIGHT,
    "default_dark": DEFAULT_DARK,
    "ocean_blue": OCEAN_BLUE,
    "forest_green": FOREST_GREEN,
    "sunset_orange": SUNSET_ORANGE,
    "berry_purple": BERRY_PURPLE,
    "corporate_gray": CORPORATE_GRAY,
    "tech_neon": TECH_NEON,
    "warm_earth": WARM_EARTH,
    "cool_mint": COOL_MINT,
    "rose_gold": ROSE_GOLD,
    "midnight_blue": MIDNIGHT_BLUE,
    "autumn_maple": AUTUMN_MAPLE,
    "spring_blossom": SPRING_BLOSSOM,
    "arctic_frost": ARCTIC_FROST,
}


# ============================================================================
# 便捷函数
# ============================================================================

def get_theme(theme_id: str) -> Theme:
    """
    获取主题

    Args:
        theme_id: 主题ID

    Returns:
        主题实例，不存在则返回默认浅色主题
    """
    return THEME_REGISTRY.get(theme_id, DEFAULT_LIGHT)


def list_themes(
    category: Optional[ThemeCategory] = None,
    mode: Optional[ThemeMode] = None
) -> List[Theme]:
    """
    列出主题

    Args:
        category: 按分类筛选
        mode: 按模式筛选

    Returns:
        主题列表
    """
    themes = list(THEME_REGISTRY.values())

    if category:
        themes = [t for t in themes if t.category == category]

    if mode:
        themes = [t for t in themes if t.mode == mode]

    return themes


def get_light_themes() -> List[Theme]:
    """获取所有浅色主题"""
    return [t for t in THEME_REGISTRY.values() if t.mode == ThemeMode.LIGHT]


def get_dark_themes() -> List[Theme]:
    """获取所有深色主题"""
    return [t for t in THEME_REGISTRY.values() if t.mode == ThemeMode.DARK]


def search_themes(keyword: str) -> List[Theme]:
    """
    搜索主题

    Args:
        keyword: 搜索关键词

    Returns:
        匹配的主题列表
    """
    keyword_lower = keyword.lower()
    return [
        t for t in THEME_REGISTRY.values()
        if (keyword_lower in t.name.lower() or
            keyword_lower in t.description.lower() or
            keyword_lower in t.id.lower())
    ]


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "ThemeMode",
    "ThemeCategory",
    # 数据类
    "ColorPalette",
    "GrayScale",
    "Typography",
    "Spacing",
    "Border",
    "Shadow",
    "Theme",
    # 主题定义
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
    # 注册表
    "THEME_REGISTRY",
    # 便捷函数
    "get_theme",
    "list_themes",
    "get_light_themes",
    "get_dark_themes",
    "search_themes",
]
