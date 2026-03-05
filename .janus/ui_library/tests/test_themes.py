"""
Theme Tests - 主题测试
======================

测试主题系统的完整功能。

测试内容:
    - 主题加载
    - 主题属性
    - 主题应用
    - 模式切换
"""

import pytest
from ui_library import get_theme, list_themes, apply_theme


class TestThemes:
    """主题测试类"""

    def test_get_tech_neon_theme(self):
        """测试获取科技霓虹主题"""
        theme = get_theme("tech_neon")
        assert theme is not None
        assert theme["id"] == "tech_neon"
        assert "霓虹" in theme["name"]

    def test_get_ocean_blue_theme(self):
        """测试获取海洋蓝主题"""
        theme = get_theme("ocean_blue")
        assert theme is not None
        assert theme["id"] == "ocean_blue"

    def test_get_nonexistent_theme(self):
        """测试获取不存在的主题"""
        theme = get_theme("nonexistent_theme")
        assert theme is None

    def test_list_all_themes(self):
        """测试列出所有主题"""
        themes = list_themes()
        assert len(themes) == 15  # 15 个主题

    def test_theme_has_required_fields(self):
        """测试主题包含必需字段"""
        theme = get_theme("tech_neon")
        required_fields = ["id", "name", "description", "mode", "colors"]
        for field in required_fields:
            assert field in theme

    def test_theme_colors(self):
        """测试主题颜色"""
        theme = get_theme("tech_neon")
        assert "colors" in theme
        required_colors = ["primary", "secondary", "background", "surface", "text"]
        for color in required_colors:
            assert color in theme["colors"]

    def test_theme_mode(self):
        """测试主题模式"""
        theme = get_theme("tech_neon")
        assert "mode" in theme
        assert theme["mode"] in ["light", "dark", "auto"]

    def test_theme_typography(self):
        """测试主题字体"""
        theme = get_theme("tech_neon")
        assert "typography" in theme
        assert "font_family" in theme["typography"]

    def test_all_themes_accessible(self):
        """测试所有主题可访问"""
        theme_ids = [
            "default_light", "default_dark", "ocean_blue", "forest_green",
            "sunset_orange", "berry_purple", "corporate_gray", "tech_neon",
            "warm_earth", "cool_mint", "rose_gold", "midnight_blue",
            "autumn_maple", "spring_blossom", "arctic_frost"
        ]
        for theme_id in theme_ids:
            theme = get_theme(theme_id)
            assert theme is not None, f"Theme {theme_id} should exist"

    def test_theme_color_format(self):
        """测试主题颜色格式"""
        theme = get_theme("tech_neon")
        for color_name, color_value in theme["colors"].items():
            assert isinstance(color_value, str)
            # 检查是十六进制颜色
            assert color_value.startswith("#")
            assert len(color_value) == 7

    def test_apply_theme_function(self):
        """测试应用主题函数"""
        # 注意: 这个测试需要 Streamlit 环境
        # 在实际环境中，这个函数会注入 CSS
        theme = get_theme("tech_neon")
        assert theme is not None
        # apply_theme("tech_neon")  # 需要 Streamlit 环境

    def test_theme_description(self):
        """测试主题描述"""
        theme = get_theme("tech_neon")
        assert "description" in theme
        assert isinstance(theme["description"], str)

    def test_light_themes(self):
        """测试浅色主题"""
        light_themes = ["default_light", "ocean_blue", "forest_green"]
        for theme_id in light_themes:
            theme = get_theme(theme_id)
            assert theme["mode"] == "light"

    def test_dark_themes(self):
        """测试深色主题"""
        dark_themes = ["default_dark", "midnight_blue"]
        for theme_id in dark_themes:
            theme = get_theme(theme_id)
            assert theme["mode"] == "dark"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
