"""
Theme Engine - 主题引擎
====================

实现主题应用、切换、CSS 生成、Streamlit 配置等功能。

核心功能:
    - apply_theme(): 应用主题到指定上下文
    - switch_theme(): 切换当前主题
    - get_css_variables(): 生成 CSS 变量
    - get_streamlit_config(): 生成 Streamlit 配置
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from pathlib import Path

# 导入主题定义
from .definitions import (
    Theme,
    ThemeMode,
    ThemeCategory,
    THEME_REGISTRY,
    get_theme,
    list_themes,
    get_light_themes,
    get_dark_themes,
)


# ============================================================================
# 主题引擎类
# ============================================================================

class ThemeEngine:
    """
    主题引擎

    负责主题的应用、切换、配置生成等核心功能
    """

    def __init__(self):
        """初始化主题引擎"""
        self._current_theme: Optional[Theme] = None
        self._theme_history: List[str] = []
        self._custom_overrides: Dict[str, Any] = {}

    def apply_theme(
        self,
        theme: Theme,
        context: str = "global",
        overrides: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        应用主题到指定上下文

        Args:
            theme: 主题实例
            context: 应用上下文 ("global", "page", "component")
            overrides: 自定义覆盖配置

        Returns:
            是否应用成功
        """
        try:
            # 保存当前主题
            if self._current_theme and self._current_theme.id != theme.id:
                self._theme_history.append(self._current_theme.id)

            # 应用主题
            self._current_theme = theme

            # 应用自定义覆盖
            if overrides:
                self._custom_overrides.update(overrides)

            return True

        except Exception as e:
            print(f"应用主题失败: {e}")
            return False

    def switch_theme(self, theme_id: str) -> bool:
        """
        切换当前主题

        Args:
            theme_id: 主题ID

        Returns:
            是否切换成功
        """
        if theme_id not in THEME_REGISTRY:
            print(f"主题不存在: {theme_id}")
            return False

        theme = THEME_REGISTRY[theme_id]
        return self.apply_theme(theme)

    def get_current_theme(self) -> Optional[Theme]:
        """
        获取当前主题

        Returns:
            当前主题实例
        """
        return self._current_theme

    def get_theme_history(self) -> List[str]:
        """
        获取主题历史记录

        Returns:
            主题ID列表
        """
        return self._theme_history.copy()

    def undo_theme(self) -> bool:
        """
        撤销上次主题切换

        Returns:
            是否撤销成功
        """
        if not self._theme_history:
            print("没有历史记录")
            return False

        prev_theme_id = self._theme_history.pop()
        theme = THEME_REGISTRY.get(prev_theme_id)

        if theme:
            self._current_theme = theme
            return True

        return False

    def get_css_variables(
        self,
        theme: Optional[Theme] = None,
        include_custom: bool = True
    ) -> str:
        """
        生成 CSS 变量

        Args:
            theme: 主题实例，None 表示使用当前主题
            include_custom: 是否包含自定义变量

        Returns:
            CSS 变量字符串
        """
        theme = theme or self._current_theme

        if not theme:
            theme = get_theme("default_light")

        # 获取基础 CSS
        css = theme.get_full_css()

        # 添加自定义覆盖
        if include_custom and self._custom_overrides:
            css += "\n/* 自定义覆盖 */\n"
            css += ":root {\n"
            for key, value in self._custom_overrides.items():
                css += f"  --{key}: {value};\n"
            css += "}\n"

        return css

    def get_streamlit_config(self, theme: Optional[Theme] = None) -> Dict[str, Any]:
        """
        生成 Streamlit 配置

        Args:
            theme: 主题实例，None 表示使用当前主题

        Returns:
            Streamlit 配置字典
        """
        theme = theme or self._current_theme

        if not theme:
            theme = get_theme("default_light")

        is_dark = theme.mode == ThemeMode.DARK

        config = {
            "primaryColor": theme.colors.primary,
            "backgroundColor": theme.colors.background,
            "secondaryBackgroundColor": theme.colors.surface,
            "textColor": theme.colors.text,
            "font": theme.typography.font_family,
        }

        # 深色模式配置
        if is_dark:
            config.update({
                "base": "dark",
                "backgroundColor": theme.colors.background,
                "secondaryBackgroundColor": theme.colors.surface,
                "textColor": theme.colors.text,
            })

        return config

    def export_theme(self, theme: Optional[Theme] = None, format: str = "json") -> str:
        """
        导出主题配置

        Args:
            theme: 主题实例
            format: 导出格式 ("json", "css", "yaml")

        Returns:
            导出的配置字符串
        """
        theme = theme or self._current_theme

        if not theme:
            theme = get_theme("default_light")

        if format == "json":
            import json
            return json.dumps(theme.to_dict(), indent=2, ensure_ascii=False)

        elif format == "css":
            return self.get_css_variables(theme)

        elif format == "yaml":
            try:
                import yaml
                return yaml.dump(theme.to_dict(), allow_unicode=True)
            except ImportError:
                return "Error: PyYAML not installed"

        else:
            raise ValueError(f"不支持的格式: {format}")

    def create_custom_theme(
        self,
        base_theme_id: str,
        overrides: Dict[str, Any],
        name: Optional[str] = None
    ) -> Theme:
        """
        基于现有主题创建自定义主题

        Args:
            base_theme_id: 基础主题ID
            overrides: 覆盖配置
            name: 自定义主题名称

        Returns:
            新主题实例
        """
        base_theme = get_theme(base_theme_id)

        if not base_theme:
            raise ValueError(f"基础主题不存在: {base_theme_id}")

        # 深拷贝基础主题
        import copy
        new_theme = copy.deepcopy(base_theme)

        # 更新 ID 和名称
        new_theme.id = f"{base_theme_id}_custom"
        new_theme.name = name or f"自定义 {base_theme.name}"
        new_theme.category = ThemeCategory.CUSTOM

        # 应用颜色覆盖
        if "colors" in overrides:
            color_dict = overrides["colors"]
            for key, value in color_dict.items():
                if hasattr(new_theme.colors, key):
                    setattr(new_theme.colors, key, value)

        # 应用自定义变量
        if "custom_vars" in overrides:
            new_theme.custom_vars.update(overrides["custom_vars"])

        return new_theme

    def compare_themes(self, theme_ids: List[str]) -> Dict[str, Any]:
        """
        对比多个主题

        Args:
            theme_ids: 主题ID列表

        Returns:
            对比结果字典
        """
        themes = [get_theme(tid) for tid in theme_ids]
        themes = [t for t in themes if t is not None]

        comparison = {
            "themes": [t.to_dict() for t in themes],
            "differences": self._find_differences(themes)
        }

        return comparison

    def _find_differences(self, themes: List[Theme]) -> List[Dict[str, Any]]:
        """找出主题间的差异"""
        differences = []

        if len(themes) < 2:
            return differences

        # 对比所有主题的配置
        base_theme = themes[0]

        for i, theme in enumerate(themes[1:], 1):
            diff = {
                "theme_index": i,
                "theme_name": theme.name,
                "differences": []
            }

            # 对比颜色
            if theme.colors.primary != base_theme.colors.primary:
                diff["differences"].append({"field": "primary", "value": theme.colors.primary})

            if theme.colors.background != base_theme.colors.background:
                diff["differences"].append({"field": "background", "value": theme.colors.background})

            # 对比字体
            if theme.typography.font_family != base_theme.typography.font_family:
                diff["differences"].append({"field": "font_family", "value": theme.typography.font_family})

            if diff["differences"]:
                differences.append(diff)

        return differences


# ============================================================================
# 全局主题引擎实例
# ============================================================================

_global_engine: Optional[ThemeEngine] = None


def get_theme_engine() -> ThemeEngine:
    """
    获取全局主题引擎（单例模式）

    Returns:
        ThemeEngine 实例
    """
    global _global_engine
    if _global_engine is None:
        _global_engine = ThemeEngine()
    return _global_engine


# ============================================================================
# Streamlit 集成函数
# ============================================================================

def render_theme_switcher(
    key: str = "theme_selector",
    show_preview: bool = True,
    show_search: bool = True
) -> Optional[str]:
    """
    渲染主题切换器组件

    Args:
        key: 组件唯一标识
        show_preview: 显示预览
        show_search: 显示搜索功能

    Returns:
        选中的主题ID
    """
    engine = get_theme_engine()

    st.subheader("🎨 主题选择")

    # 搜索框
    selected_theme_id = None

    if show_search:
        search_keyword = st.text_input("🔍 搜索主题", key=f"{key}_search")

        if search_keyword:
            matching_themes = search_themes(search_keyword)
            theme_options = {t.id: f"{t.name} ({t.id})" for t in matching_themes}
        else:
            theme_options = {}
    else:
        # 所有主题
        theme_options = {t.id: f"{t.name} ({t.id})" for t in THEME_REGISTRY.values()}

    # 分类筛选
    col1, col2, col3 = st.columns(3)

    with col1:
        category_filter = st.selectbox(
            "分类",
            ["全部", "默认", "自然", "专业", "活力", "季节", "自定义"],
            key=f"{key}_category"
        )

    with col2:
        mode_filter = st.selectbox(
            "模式",
            ["全部", "浅色", "深色"],
            key=f"{key}_mode"
        )

    with col3:
        if st.button("🔄 重置", key=f"{key}_reset"):
            engine.switch_theme("default_light")
            st.rerun()

    # 应用筛选
    if category_filter != "全部" or mode_filter != "全部":
        themes = list_themes()

        if category_filter != "全部":
            category_map = {
                "默认": ThemeCategory.DEFAULT,
                "自然": ThemeCategory.NATURE,
                "专业": ThemeCategory.PROFESSIONAL,
                "活力": ThemeCategory.VIBRANT,
                "季节": ThemeCategory.SEASONAL,
                "自定义": ThemeCategory.CUSTOM
            }
            themes = [t for t in themes if t.category == category_map.get(category_filter)]

        if mode_filter != "全部":
            mode_map = {"浅色": ThemeMode.LIGHT, "深色": ThemeMode.DARK}
            themes = [t for t in themes if t.mode == mode_map.get(mode_filter)]

        theme_options = {t.id: f"{t.name} ({t.id})" for t in themes}

    # 主题选择
    current_theme = engine.get_current_theme()
    default_index = list(theme_options.keys()).index(current_theme.id) if current_theme else 0

    selected_id = st.selectbox(
        "选择主题",
        options=list(theme_options.keys()),
        format_func=lambda x: theme_options[x],
        index=default_index,
        key=f"{key}_selector"
    )

    # 应用主题
    if selected_id and selected_id != (current_theme.id if current_theme else ""):
        engine.switch_theme(selected_id)
        st.success(f"✅ 已切换到 {theme_options[selected_id]}")
        st.rerun()

    # 显示预览
    if show_preview and selected_id:
        theme = get_theme(selected_id)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**主色调**")
            st.markdown(f"""
<div style='background: {theme.colors.primary}; color: white; padding: 1rem; border-radius: 8px; text-align: center;'>
                Primary
            </div>
""", unsafe_allow_html=True)

        with col2:
            st.markdown("**表面色**")
            st.markdown(f"""
<div style='background: {theme.colors.surface}; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid {theme.colors.border};'>
                Surface
            </div>
""", unsafe_allow_html=True)

        with col3:
            st.markdown("**文本色**")
            st.markdown(f"""
<div style='background: {theme.colors.background}; color: {theme.colors.text}; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid {theme.colors.border};'>
                Text
            </div>
""", unsafe_allow_html=True)

    return selected_id


def render_theme_preview(theme: Theme, show_details: bool = True):
    """
    渲染主题预览卡片

    Args:
        theme: 主题实例
        show_details: 显示详细信息
    """
    engine = get_theme_engine()

    st.markdown(f"""
<div style='background: {theme.colors.background}; padding: 1.5rem; border-radius: 8px; border: 1px solid {theme.colors.border};'>
    <h3 style='color: {theme.colors.text}; margin: 0 0 1rem 0;'>{theme.name}</h3>
    <p style='color: {theme.colors.text_secondary}; margin-bottom: 1rem;'>{theme.description}</p>

    <div style='display: flex; gap: 0.5rem; margin-bottom: 1rem;'>
        <span style='background: {theme.colors.primary}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>Primary</span>
        <span style='background: {theme.colors.secondary}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>Secondary</span>
        <span style='background: {theme.colors.success}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>Success</span>
        <span style='background: {theme.colors.warning}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>Warning</span>
        <span style='background: {theme.colors.error}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>Error</span>
    </div>

    <div style='color: {theme.colors.text}; font-size: 0.9rem;'>
        <strong>模式:</strong> {theme.mode.value}<br>
        <strong>分类:</strong> {theme.category.value}
    </div>
</div>
""", unsafe_allow_html=True)

    if show_details:
        with st.expander("📊 详细信息"):
            st.json(theme.to_dict())


def apply_theme_to_page(theme: Theme):
    """
    将主题应用到 Streamlit 页面

    Args:
        theme: 主题实例
    """
    engine = get_theme_engine()
    engine.apply_theme(theme)

    # 应用 CSS 样式
    css_variables = engine.get_css_variables(theme)

    st.markdown(f"<style>{css_variables}</style>", unsafe_allow_html=True)

    # 应用 Streamlit 配置
    config = engine.get_streamlit_config(theme)

    # 更新页面样式
    st.markdown(f"""
<style>
    .stApp {{
        background-color: {config.get('backgroundColor', '#ffffff')};
    }}

    .stMarkdown {{
        color: {config.get('textColor', '#212529')};
    }}

    /* 自定义滚动条 */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {theme.colors.surface};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {theme.colors.border};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {theme.colors.text_secondary};
    }}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# 便捷函数
# ============================================================================

def switch_theme(theme_id: str) -> bool:
    """
    切换主题的便捷函数

    Args:
        theme_id: 主题ID

    Returns:
        是否切换成功
    """
    engine = get_theme_engine()
    return engine.switch_theme(theme_id)


def get_current_theme_id() -> Optional[str]:
    """
    获取当前主题ID

    Returns:
        当前主题ID
    """
    engine = get_theme_engine()
    theme = engine.get_current_theme()
    return theme.id if theme else None


def get_theme_css(theme_id: Optional[str] = None) -> str:
    """
    获取主题 CSS 的便捷函数

    Args:
        theme_id: 主题ID，None 表示当前主题

    Returns:
        CSS 变量字符串
    """
    engine = get_theme_engine()

    if theme_id:
        theme = get_theme(theme_id)
    else:
        theme = engine.get_current_theme()

    return engine.get_css_variables(theme) if theme else ""


def export_current_theme(format: str = "json") -> str:
    """
    导出当前主题

    Args:
        format: 导出格式

    Returns:
        导出的配置字符串
    """
    engine = get_theme_engine()
    return engine.export_theme(format=format)


def create_theme_presets() -> Dict[str, str]:
    """
    创建主题预设快捷方式

    Returns:
        预设主题字典
    """
    return {
        "light": "default_light",
        "dark": "default_dark",
        "ocean": "ocean_blue",
        "forest": "forest_green",
        "sunset": "sunset_orange",
        "berry": "berry_purple",
        "corporate": "corporate_gray",
        "neon": "tech_neon",
        "earth": "warm_earth",
        "mint": "cool_mint",
        "rose": "rose_gold",
        "midnight": "midnight_blue",
        "autumn": "autumn_maple",
        "spring": "spring_blossom",
        "arctic": "arctic_frost",
    }


# ============================================================================
# Streamlit 页面组件
# ============================================================================

def theme_settings_page():
    """主题设置页面"""
    st.set_page_config(
        page_title="主题设置",
        page_icon="🎨",
        layout="wide"
    )

    st.title("🎨 主题系统")

    engine = get_theme_engine()

    # 主题切换器
    selected_theme = render_theme_switcher()

    # 当前主题信息
    current_theme = engine.get_current_theme()
    if current_theme:
        st.divider()
        st.subheader("当前主题")
        render_theme_preview(current_theme)

    # 所有主题展示
    st.divider()
    st.subheader("所有主题")

    # 按分类展示
    categories = {
        "默认": [DEFAULT_LIGHT, DEFAULT_DARK],
        "自然": [OCEAN_BLUE, FOREST_GREEN, WARM_EARTH, COOL_MINT],
        "活力": [SUNSET_ORANGE, BERRY_PURPLE, ROSE_GOLD, TECH_NEON],
        "专业": [CORPORATE_GRAY, MIDNIGHT_BLUE],
        "季节": [AUTUMN_MAPLE, SPRING_BLOSSOM, ARCTIC_FROST],
    }

    tabs = st.tabs(list(categories.keys()))

    for tab, (category_name, themes) in zip(tabs, categories.items()):
        with tab:
            cols = st.columns(len(themes))

            for col, theme in zip(cols, themes):
                with col:
                    render_theme_preview(theme, show_details=False)

                    if st.button(f"使用 {theme.name}", key=f"use_{theme.id}"):
                        switch_theme(theme.id)
                        st.rerun()

    # 导出功能
    st.divider()
    st.subheader("📥 导出主题")

    col1, col2, col3 = st.columns(3)

    with col1:
        export_format = st.selectbox("格式", ["json", "css", "yaml"])

    with col2:
        if st.button("导出当前主题", use_container_width=True):
            exported = export_current_theme(export_format)

            st.download_button(
                label=f"下载 {export_format.upper()}",
                data=exported,
                file_name=f"theme_{export_format}.{export_format}",
                mime="application/json" if export_format == "json" else "text/css"
            )

    with col3:
        st.write(\"\")
        st.write(f\"**{export_format.upper()}** 格式\")


# ============================================================================
# 自动主题切换（基于系统偏好）
# ============================================================================

def auto_detect_theme_mode() -> ThemeMode:
    """
    自动检测系统主题偏好

    Returns:
        检测到的主题模式
    """
    # 在实际应用中，这里可以调用系统 API
    # 目前返回默认浅色模式
    return ThemeMode.LIGHT


def apply_auto_theme():
    """应用自动检测的主题"""
    detected_mode = auto_detect_theme_mode()

    # 根据检测到的模式选择主题
    if detected_mode == ThemeMode.DARK:
        switch_theme("default_dark")
    else:
        switch_theme("default_light")


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 引擎类
    "ThemeEngine",
    # 全局实例
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
    "auto_detect_theme_mode",
    "apply_auto_theme",
    # 页面组件
    "theme_settings_page",
]
