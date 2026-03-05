"""
Composition Tests - 组合系统测试
=================================

测试组件组合系统的完整功能。

测试内容:
    - 组件组合
    - 布局生成
    - 验证规则
    - 预定义模式
"""

import pytest
from ui_library import compose


class TestComposition:
    """组合系统测试类"""

    def test_compose_dashboard(self):
        """测试组合仪表盘"""
        page_code = compose(
            components=["HeaderBar", "MetricCard", "ChartPanel"],
            layout_type="dashboard",
            framework="streamlit"
        )
        assert page_code is not None
        assert isinstance(page_code, str)
        assert len(page_code) > 0

    def test_compose_form(self):
        """测试组合表单"""
        page_code = compose(
            components=["HeaderBar", "FilterBar"],
            layout_type="form",
            framework="streamlit"
        )
        assert page_code is not None

    def test_compose_with_theme(self):
        """测试带主题的组合"""
        page_code = compose(
            components=["MetricCard"],
            layout_type="dashboard",
            theme="tech_neon",
            framework="streamlit"
        )
        assert page_code is not None

    def test_compose_invalid_component(self):
        """测试组合无效组件"""
        # 无效组件应该被忽略，不会导致错误
        page_code = compose(
            components=["InvalidComponent", "MetricCard"],
            layout_type="dashboard",
            framework="streamlit"
        )
        assert page_code is not None

    def test_compose_empty_components(self):
        """测试空组件列表"""
        page_code = compose(
            components=[],
            layout_type="dashboard",
            framework="streamlit"
        )
        # 空组件列表应该返回空或占位内容
        assert page_code is not None

    def test_compose_react_framework(self):
        """测试 React 框架组合"""
        page_code = compose(
            components=["MetricCard"],
            layout_type="dashboard",
            framework="react"
        )
        assert page_code is not None

    def test_compose_multiple_components(self):
        """测试多组件组合"""
        page_code = compose(
            components=["HeaderBar", "MetricCard", "ChartPanel", "FilterBar", "DataList"],
            layout_type="dashboard",
            framework="streamlit"
        )
        assert page_code is not None
        # 多组件应该生成更长的代码
        assert len(page_code) > 100

    def test_compose_analytics_layout(self):
        """测试分析布局"""
        page_code = compose(
            components=["ChartPanel", "MetricCard"],
            layout_type="analytics",
            framework="streamlit"
        )
        assert page_code is not None

    def test_compose_content_layout(self):
        """测试内容布局"""
        page_code = compose(
            components=["HeaderBar", "CommentSection"],
            layout_type="content",
            framework="streamlit"
        )
        assert page_code is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
