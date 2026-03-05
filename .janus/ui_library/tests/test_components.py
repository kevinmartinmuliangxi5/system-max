"""
Component Tests - 组件测试
===========================

测试组件库的完整功能。

测试内容:
    - 组件加载
    - 组件属性
    - 组件功能
    - 边界条件
"""

import pytest
from ui_library import get_component, list_components


class TestComponents:
    """组件测试类"""

    def test_get_dashboard_component(self):
        """测试获取 Dashboard 组件"""
        component = get_component("DashboardPage")
        assert component is not None
        assert component["id"] == "DashboardPage"
        assert component["name"] == "DashboardPage"
        assert "仪表盘" in component["description"]

    def test_get_metric_card_component(self):
        """测试获取 MetricCard 组件"""
        component = get_component("MetricCard")
        assert component is not None
        assert component["id"] == "MetricCard"
        assert component["size"] == "medium"

    def test_get_nonexistent_component(self):
        """测试获取不存在的组件"""
        component = get_component("NonExistentComponent")
        assert component is None

    def test_list_all_components(self):
        """测试列出所有组件"""
        components = list_components()
        assert len(components) > 0
        assert len(components) >= 20  # 8 large + 12 medium

    def test_list_large_components(self):
        """测试列出大型组件"""
        components = list_components(size="large")
        assert len(components) == 8
        for comp in components:
            assert comp["size"] == "large"

    def test_list_medium_components(self):
        """测试列出中型组件"""
        components = list_components(size="medium")
        assert len(components) == 12
        for comp in components:
            assert comp["size"] == "medium"

    def test_component_has_required_fields(self):
        """测试组件包含必需字段"""
        component = get_component("DashboardPage")
        required_fields = ["id", "name", "description", "category", "size", "features", "code_skeleton"]
        for field in required_fields:
            assert field in component

    def test_component_features_list(self):
        """测试组件特性列表"""
        component = get_component("DashboardPage")
        assert isinstance(component["features"], list)
        assert len(component["features"]) > 0

    def test_component_code_skeleton(self):
        """测试组件代码骨架"""
        component = get_component("DashboardPage")
        assert "code_skeleton" in component
        assert len(component["code_skeleton"]) > 0
        assert "streamlit" in component["code_skeleton"].lower() or "st." in component["code_skeleton"]

    def test_all_large_components_accessible(self):
        """测试所有大型组件可访问"""
        large_component_ids = [
            "DashboardPage", "ChatbotPage", "FormWizardPage",
            "DataTablePage", "SettingsPage", "LandingPage",
            "KanbanPage", "ProfilePage"
        ]
        for comp_id in large_component_ids:
            component = get_component(comp_id)
            assert component is not None, f"Component {comp_id} should exist"

    def test_all_medium_components_accessible(self):
        """测试所有中型组件可访问"""
        medium_component_ids = [
            "MetricCard", "ChartPanel", "FilterBar", "DataList",
            "NavSidebar", "HeaderBar", "FooterBar", "AlertPanel",
            "UploadZone", "CommentSection", "TimelineBlock", "PricingTable"
        ]
        for comp_id in medium_component_ids:
            component = get_component(comp_id)
            assert component is not None, f"Component {comp_id} should exist"

    def test_component_category(self):
        """测试组件类别"""
        component = get_component("DashboardPage")
        assert "category" in component
        assert isinstance(component["category"], str)

    def test_component_preview(self):
        """测试组件预览"""
        component = get_component("DashboardPage")
        assert "preview" in component

    def test_component_props(self):
        """测试组件属性"""
        component = get_component("DashboardPage")
        assert "props" in component
        assert isinstance(component["props"], dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
