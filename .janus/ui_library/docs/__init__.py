"""
UI Library Documentation Generator - 文档生成模块
==================================================

自动生成组件库文档，包括组件手册、主题预览、行业指南等。

主要功能:
    - generate_component_doc(): 生成组件文档
    - generate_theme_preview(): 生成主题预览
    - generate_industry_guide(): 生成行业使用指南
    - export_to_markdown(): 导出 Markdown 文档
    - generate_all_docs(): 生成所有文档

使用示例:
    from ui_library.docs import generate_all_docs, export_to_markdown

    # 生成所有文档
    docs = generate_all_docs()

    # 导出到文件
    export_to_markdown(docs, "./docs/")

导出内容:
    - DocGenerator: 文档生成器主类
    - generate_all_docs: 生成所有文档的便捷函数
    - export_to_markdown: 导出 Markdown 文档
"""

from .generator import (
    DocGenerator,
    ComponentDoc,
    ThemeDoc,
    IndustryDoc,
    generate_component_doc,
    generate_theme_preview,
    generate_industry_guide,
    generate_all_docs,
    export_to_markdown,
)

__all__ = [
    "DocGenerator",
    "ComponentDoc",
    "ThemeDoc",
    "IndustryDoc",
    "generate_component_doc",
    "generate_theme_preview",
    "generate_industry_guide",
    "generate_all_docs",
    "export_to_markdown",
]
