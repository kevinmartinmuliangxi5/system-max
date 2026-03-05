"""
UI Library Adapters - 框架适配器模块
=======================================

提供多框架代码生成能力，将组件定义转换为不同前端框架的实现代码。

当前支持的框架:
    - React + JSX + Tailwind CSS
    - （未来可扩展: Vue, Svelte, Angular 等）

模块结构:
    - react_adapter: Streamlit → React 转换器
    - vue_adapter: Streamlit → Vue 转换器（待实现）
    - svelte_adapter: Streamlit → Svelte 转换器（待实现）

使用示例:
    from ui_library.adapters import ReactAdapter

    adapter = ReactAdapter()
    react_code = adapter.generate_component(component_def, theme)

导出内容:
    - ReactAdapter: React 框架适配器类
    - ComponentMapping: 组件映射表
"""

from .react_adapter import (
    ReactAdapter,
    ComponentMapping,
    PropMapping,
    StyleMapping,
    generate_react_component,
    generate_react_page,
    streamlit_to_react,
)

__all__ = [
    "ReactAdapter",
    "ComponentMapping",
    "PropMapping",
    "StyleMapping",
    "generate_react_component",
    "generate_react_page",
    "streamlit_to_react",
]
