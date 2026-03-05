"""
Documentation Generator - 文档生成器
====================================

自动生成 UI 组件库的完整文档，包括组件手册、主题预览和行业指南。

核心类:
    - ComponentDoc: 组件文档数据类
    - ThemeDoc: 主题文档数据类
    - IndustryDoc: 行业文档数据类
    - DocGenerator: 主文档生成器

主要函数:
    - generate_component_doc(component): 生成单个组件文档
    - generate_theme_preview(theme): 生成主题预览文档
    - generate_industry_guide(industry): 生成行业使用指南
    - generate_all_docs(): 生成所有文档
    - export_to_markdown(docs, output_path): 导出到 Markdown
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
import json
from datetime import datetime


# ============================================================================
# 枚举定义
# ============================================================================

class DocFormat(Enum):
    """文档格式"""
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"


class DocSection(Enum):
    """文档章节"""
    OVERVIEW = "overview"
    INSTALLATION = "installation"
    QUICK_START = "quick_start"
    COMPONENTS = "components"
    THEMES = "themes"
    PATTERNS = "patterns"
    INDUSTRIES = "industries"
    API_REFERENCE = "api_reference"
    EXAMPLES = "examples"
    FAQ = "faq"


# ============================================================================
# 数据类定义
# ============================================================================

@dataclass
class ComponentDoc:
    """组件文档"""
    component_id: str
    name: str
    description: str
    category: str
    size: str  # large, medium
    features: List[str]
    props: List[Dict[str, Any]]
    methods: List[Dict[str, str]]
    examples: List[str]
    preview_ascii: str
    streamlit_code: str
    react_code: Optional[str] = None
    related_components: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"


@dataclass
class ThemeDoc:
    """主题文档"""
    theme_id: str
    name: str
    description: str
    mode: str  # light, dark, auto
    colors: Dict[str, str]
    typography: Dict[str, str]
    spacing: Dict[str, str]
    border_radius: Dict[str, str]
    shadows: List[str]
    preview_url: Optional[str] = None
    palette_chart: str = ""
    usage_examples: List[str] = field(default_factory=list)
    recommended_for: List[str] = field(default_factory=list)


@dataclass
class IndustryDoc:
    """行业文档"""
    industry_id: str
    name: str
    description: str
    templates: List[str]
    recommended_themes: List[str]
    common_components: List[str]
    use_cases: List[Dict[str, str]]
    best_practices: List[str]
    code_examples: List[Dict[str, str]]
    integration_guide: str = ""


@dataclass
class APIDoc:
    """API 文档"""
    function_name: str
    module: str
    description: str
    parameters: List[Dict[str, Any]]
    returns: Dict[str, str]
    raises: List[str]
    example: str
    see_also: List[str] = field(default_factory=list)


@dataclass
class CompleteDocumentation:
    """完整文档集"""
    readme: str
    components: str
    themes: str
    industries: str
    patterns: str
    api_reference: str
    examples: str
    faq: str
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================================
# 文档生成器主类
# ============================================================================

class DocGenerator:
    """
    文档生成器

    自动生成 UI 组件库的完整文档。

    主要方法:
        - generate_component_doc(component): 生成组件文档
        - generate_theme_doc(theme): 生成主题文档
        - generate_industry_doc(industry): 生成行业文档
        - generate_readme(): 生成 README
        - generate_all(): 生成所有文档
    """

    def __init__(
        self,
        base_path: str,
        output_format: DocFormat = DocFormat.MARKDOWN,
        include_code_examples: bool = True,
        include_previews: bool = True
    ):
        """
        初始化文档生成器

        Args:
            base_path: UI 库基础路径
            output_format: 输出格式
            include_code_examples: 是否包含代码示例
            include_previews: 是否包含预览图
        """
        self.base_path = base_path
        self.output_format = output_format
        self.include_code_examples = include_code_examples
        self.include_previews = include_previews

        # 导入组件库
        try:
            from ui_library import components, themes, patterns, industries
            self.components_module = components
            self.themes_module = themes
            self.patterns_module = patterns
            self.industries_module = industries
        except ImportError:
            self.components_module = None
            self.themes_module = None
            self.patterns_module = None
            self.industries_module = None

    def generate_component_doc(self, component: Any) -> ComponentDoc:
        """
        生成组件文档

        Args:
            component: 组件定义对象

        Returns:
            ComponentDoc: 组件文档
        """
        component_id = getattr(component, "id", component.__class__.__name__)
        name = getattr(component, "name", component_id)
        description = getattr(component, "description", "")
        category = getattr(component, "category", "general")
        size = getattr(component, "size", "medium")
        features = getattr(component, "features", [])
        preview = getattr(component, "preview", "")
        code_skeleton = getattr(component, "code_skeleton", "")
        props = getattr(component, "props", {})

        # 生成属性文档
        props_doc = []
        for prop_name, prop_value in props.items():
            props_doc.append({
                "name": prop_name,
                "type": self._infer_type(prop_value),
                "default": str(prop_value) if prop_value else "",
                "description": f"The {prop_name} property"
            })

        # 生成方法文档
        methods_doc = []
        if hasattr(component, "render_streamlit"):
            methods_doc.append({
                "name": "render_streamlit",
                "description": "Render the component in Streamlit",
                "returns": "str: Streamlit code"
            })

        # 生成代码示例
        examples = []
        if code_skeleton and self.include_code_examples:
            examples.append("### Streamlit Example\n```python\n" + code_skeleton + "\n```")

        # React 代码示例（如果存在）
        react_code = None
        if hasattr(component, "react_skeleton") and self.include_code_examples:
            react_code = component.react_skeleton
            examples.append("### React Example\n```tsx\n" + react_code + "\n```")

        return ComponentDoc(
            component_id=component_id,
            name=name,
            description=description,
            category=category,
            size=size,
            features=features,
            props=props_doc,
            methods=methods_doc,
            examples=examples,
            preview_ascii=preview,
            streamlit_code=code_skeleton,
            react_code=react_code,
            tags=self._extract_tags(component)
        )

    def generate_theme_doc(self, theme: Dict[str, Any]) -> ThemeDoc:
        """
        生成主题文档

        Args:
            theme: 主题定义字典

        Returns:
            ThemeDoc: 主题文档
        """
        theme_id = theme.get("id", "unknown")
        name = theme.get("name", theme_id)
        description = theme.get("description", "")
        mode = theme.get("mode", "light")

        colors = theme.get("colors", {})
        typography = theme.get("typography", {})
        spacing = theme.get("spacing", {})
        border_radius = theme.get("border_radius", {})
        shadows = theme.get("shadows", [])

        # 生成调色板图表
        palette_chart = self._generate_palette_chart(colors)

        # 生成使用示例
        usage_examples = []
        if self.include_code_examples:
            usage_examples.append(f"```python\nimport streamlit as st\nfrom ui_library.themes import apply_theme\n\napply_theme('{theme_id}')\n```")

        return ThemeDoc(
            theme_id=theme_id,
            name=name,
            description=description,
            mode=mode,
            colors=colors,
            typography=typography,
            spacing=spacing,
            border_radius=border_radius,
            shadows=shadows,
            palette_chart=palette_chart,
            usage_examples=usage_examples,
            recommended_for=theme.get("recommended_for", [])
        )

    def generate_industry_doc(self, industry_id: str) -> IndustryDoc:
        """
        生成行业使用指南

        Args:
            industry_id: 行业 ID

        Returns:
            IndustryDoc: 行业文档
        """
        if not self.industries_module:
            return IndustryDoc(
                industry_id=industry_id,
                name=industry_id,
                description="Industry module not available",
                templates=[],
                recommended_themes=[],
                common_components=[],
                use_cases=[],
                best_practices=[],
                code_examples=[]
            )

        # 获取行业模块
        industry_module = getattr(self.industries_module, industry_id, None)
        if not industry_module:
            return IndustryDoc(
                industry_id=industry_id,
                name=industry_id,
                description="Industry not found",
                templates=[],
                recommended_themes=[],
                common_components=[],
                use_cases=[],
                best_practices=[],
                code_examples=[]
            )

        # 提取模板信息
        templates = getattr(industry_module, "__all__", [])

        # 获取推荐主题
        recommended_themes = getattr(industry_module, "RECOMMENDED_THEMES", [])

        # 获取常用组件
        common_components = getattr(industry_module, "COMMON_COMPONENTS", [])

        # 生成用例
        use_cases = self._generate_industry_use_cases(industry_id)

        # 生成最佳实践
        best_practices = self._generate_best_practices(industry_id)

        # 生成代码示例
        code_examples = self._generate_industry_code_examples(industry_module)

        # 生成集成指南
        integration_guide = self._generate_integration_guide(industry_id)

        return IndustryDoc(
            industry_id=industry_id,
            name=industry_id.replace("_", " ").title(),
            description=f"Templates and components for {industry_id} industry",
            templates=templates,
            recommended_themes=recommended_themes,
            common_components=common_components,
            use_cases=use_cases,
            best_practices=best_practices,
            code_examples=code_examples,
            integration_guide=integration_guide
        )

    def generate_readme(self) -> str:
        """
        生成 README.md

        Returns:
            str: README 内容
        """
        return """# UI Template Library Pro

<div align="center">

**双脑协同 UI 设计系统**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-red.svg)](https://streamlit.io/)
[![React](https://img.shields.io/badge/React-18+-cyan.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

智能、高效、生产就绪的 UI 组件库系统

[快速开始](#快速开始) • [组件手册](#组件手册) • [主题指南](#主题指南) • [行业模板](#行业模板)

</div>

---

## 📖 简介

UI Template Library Pro 是一个专为 AI 辅助开发设计的 UI 组件库系统，提供了：

- **20+ 预制组件** - 从页面级到区块级的完整组件库
- **15+ 主题方案** - 覆盖各种场景的配色方案
- **10+ 交互模式** - 常见的用户交互模式实现
- **4+ 行业模板** - 数据分析、教育、CMS、AI 应用等
- **多框架支持** - Streamlit、React、Vue（规划中）
- **智能推荐** - 基于场景的组件和主题推荐

## ✨ 特性

### 🎨 组件丰富

- **页面级组件**: Dashboard、Chatbot、FormWizard、DataTable、Settings、Landing、Kanban、Profile
- **区块级组件**: MetricCard、ChartPanel、FilterBar、DataList、NavSidebar、HeaderBar 等
- **交互模式**: 表单、搜索、分页、弹窗、提示、加载、拖拽、滚动、切换、折叠

### 🎭 主题系统

- 15 种精心设计的配色方案
- 支持浅色/深色模式
- 可自定义的样式变量
- Tailwind CSS 集成

### 🏭 行业模板

- **数据分析/BI**: 仪表盘、报表生成器、数据探索器、告警监控、ETL 流程
- **教育培训**: 课程目录、课程播放器、测验系统、进度跟踪、讨论区
- **CMS**: 文章编辑器、媒体库、内容列表、分类管理、SEO 面板
- **AI 应用**: 对话助手、图像生成、模型试验场、数据标注、流水线构建

### 🔄 框架适配

- **Streamlit**: 原生支持，开箱即用
- **React**: 自动代码生成，TypeScript 支持
- **Vue**: 即将推出

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-repo/ui-library-pro.git
cd ui-library-pro

# 安装依赖
pip install -e .
```

### 基础使用

#### Streamlit

```python
import streamlit as st
from ui_library import get_component, get_theme, apply_theme

# 应用主题
apply_theme("tech_neon")

# 获取并渲染组件
dashboard = get_component("DashboardPage")
st.write(dashboard["code_skeleton"])
```

#### React

```python
from ui_library.adapters import generate_react_component

# 生成 React 组件
react_code = generate_react_component(
    component_def=dashboard,
    theme=get_theme("tech_neon")
)

# 保存到文件
with open("Dashboard.tsx", "w") as f:
    f.write(react_code)
```

### 智能推荐

```python
from ui_library import recommend

# 获取推荐
recommendations = recommend(
    industry="data_analytics",
    use_case="dashboard",
    complexity="medium"
)

# 应用推荐
for component in recommendations["components"]:
    st.write(component["code_skeleton"])
```

## 📚 文档

### [组件手册](COMPONENTS.md)

完整的组件 API 文档，包括：
- 组件列表
- 属性说明
- 方法签名
- 代码示例
- 最佳实践

### [主题指南](THEMES.md)

主题系统完整文档：
- 主题列表
- 配色方案
- 自定义方法
- 切换模式

### [行业模板](INDUSTRIES.md)

行业专用模板文档：
- 模板介绍
- 使用场景
- 推荐配置
- 集成指南

### [API 参考](API_REFERENCE.md)

完整的 API 文档：
- 模块函数
- 类定义
- 参数说明
- 返回值

## 🎯 使用场景

### 快速原型

```python
from ui_library import compose, get_theme

# 快速组合页面
page = compose(
    components=["HeaderBar", "MetricCard", "ChartPanel"],
    layout="dashboard",
    theme="ocean_blue"
)
```

### 行业应用

```python
from ui_library.industries import data_analytics

# 使用行业模板
dashboard = data_analytics.BIDashboard()
st.write(dashboard.render_streamlit())
```

### 代码生成

```python
from ui_library.adapters import generate_react_page

# 生成 React 页面
page_code = generate_react_page(
    page_def=page_definition,
    theme=theme_config
)
```

## 🛠️ 开发

### 项目结构

```
ui_library/
├── __init__.py           # 模块入口
├── config.py             # 全局配置
├── components/           # 组件库
│   ├── large.py         # 大型组件
│   └── medium.py        # 中型组件
├── themes/              # 主题系统
│   ├── definitions.py   # 主题定义
│   └── engine.py        # 主题引擎
├── patterns/            # 交互模式
│   ├── interactions.py  # 交互模式
│   └── composition.py   # 组合系统
├── industries/          # 行业模板
│   ├── data_analytics.py
│   ├── education.py
│   ├── cms.py
│   └── ai_apps.py
├── adapters/            # 框架适配
│   └── react_adapter.py
└── recommender/         # 推荐引擎
    ├── engine.py
    └── rules.py
```

### 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - Python Web 框架
- [React](https://reactjs.org/) - JavaScript 库
- [Tailwind CSS](https://tailwindcss.com/) - CSS 框架
- [shadcn/ui](https://ui.shadcn.com/) - React 组件库灵感

---

<div align="center">

**Made with ❤️ by the UI Library Pro Team**

[官网](https://ui-library.pro) • [文档](https://docs.ui-library.pro) • [示例](https://examples.ui-library.pro)

</div>
"""

    def generate_components_doc(self) -> str:
        """生成组件手册"""
        doc = "# 组件手册 (Components)\n\n"
        doc += "完整的组件 API 文档和使用指南。\n\n"

        doc += "## 目录\n\n"
        doc += "- [页面级组件](#页面级组件)\n"
        doc += "- [区块级组件](#区块级组件)\n"
        doc += "- [交互模式](#交互模式)\n\n"

        # 页面级组件
        doc += "## 页面级组件\n\n"
        large_components = ["DashboardPage", "ChatbotPage", "FormWizardPage",
                           "DataTablePage", "SettingsPage", "LandingPage", "KanbanPage", "ProfilePage"]
        for comp in large_components:
            doc += f"### {comp}\n\n"
            doc += f"**类型**: 页面级组件\n\n"
            doc += f"**描述**: {comp} 页面组件模板\n\n"
            doc += f"**特性**:\n"
            doc += f"- 响应式布局\n"
            doc += f"- 状态管理\n"
            doc += f"- 事件处理\n\n"
            doc += f"**使用示例**:\n"
            doc += "```python\n"
            doc += f"from ui_library.components import get_component\n\n"
            doc += f"component = get_component('{comp}')\n"
            doc += f"st.write(component['code_skeleton'])\n"
            doc += "```\n\n"

        # 区块级组件
        doc += "## 区块级组件\n\n"
        medium_components = ["MetricCard", "ChartPanel", "FilterBar", "DataList",
                            "NavSidebar", "HeaderBar", "FooterBar", "AlertPanel",
                            "UploadZone", "CommentSection", "TimelineBlock", "PricingTable"]
        for comp in medium_components:
            doc += f"### {comp}\n\n"
            doc += f"**类型**: 区块级组件\n\n"
            doc += f"**描述**: {comp} 区块组件\n\n"
            doc += f"**Props**:\n"
            doc += f"- `title`: 标题\n"
            doc += f"- `value`: 值/内容\n"
            doc += f"- `options`: 配置选项\n\n"
            doc += f"**使用示例**:\n"
            doc += "```python\n"
            doc += f"from ui_library.components import get_component\n\n"
            doc += f"component = get_component('{comp}')\n"
            doc += f"st.write(component['code_skeleton'])\n"
            doc += "```\n\n"

        # 交互模式
        doc += "## 交互模式\n\n"
        patterns = ["FormPattern", "SearchPattern", "PaginationPattern", "ModalPattern",
                   "ToastPattern", "LoadingPattern", "DragDropPattern", "InfiniteScrollPattern",
                   "TabSwitchPattern", "CollapsiblePattern"]
        for pattern in patterns:
            doc += f"### {pattern}\n\n"
            doc += f"**类型**: 交互模式\n\n"
            doc += f"**描述**: {pattern} 交互模式实现\n\n"
            doc += f"**触发条件**: 用户操作触发\n"
            doc += f"**状态管理**: 多状态支持\n"
            doc += f"**反馈机制**: 即时反馈\n\n"

        return doc

    def generate_themes_doc(self) -> str:
        """生成主题手册"""
        doc = "# 主题指南 (Themes)\n\n"
        doc += "完整的主题系统文档。\n\n"

        doc += "## 目录\n\n"
        doc += "- [主题列表](#主题列表)\n"
        doc += "- [配色方案](#配色方案)\n"
        doc += "- [自定义主题](#自定义主题)\n"
        doc += "- [模式切换](#模式切换)\n\n"

        doc += "## 主题列表\n\n"

        themes = [
            ("default_light", "默认浅色", "经典的浅色主题"),
            ("default_dark", "默认深色", "经典的深色主题"),
            ("ocean_blue", "海洋蓝", "清新的海洋风格"),
            ("forest_green", "森林绿", "自然的森林风格"),
            ("sunset_orange", "日落橙", "温暖的日落风格"),
            ("berry_purple", "浆果紫", "优雅的紫色主题"),
            ("corporate_gray", "商务灰", "专业的商务风格"),
            ("tech_neon", "科技霓虹", "未来感的霓虹风格"),
            ("warm_earth", "暖土色", "温馨的土色主题"),
            ("cool_mint", "清凉薄荷", "清新的薄荷风格"),
            ("rose_gold", "玫瑰金", "优雅的玫瑰金"),
            ("midnight_blue", "午夜蓝", "深邃的午夜蓝"),
            ("autumn_maple", "秋枫红", "浓郁的秋枫风格"),
            ("spring_blossom", "春樱粉", "柔和的樱花风格"),
            ("arctic_frost", "极地霜", "纯净的极地风格"),
        ]

        for theme_id, name, description in themes:
            doc += f"### {name} (`{theme_id}`)\n\n"
            doc += f"{description}\n\n"
            doc += f"**配色**:\n"
            doc += f"- Primary: `var(--{theme_id}-primary)`\n"
            doc += f"- Secondary: `var(--{theme_id}-secondary)`\n"
            doc += f"- Background: `var(--{theme_id}-background)`\n\n"
            doc += f"**使用**:\n"
            doc += "```python\n"
            doc += f"from ui_library.themes import apply_theme\n\n"
            doc += f"apply_theme('{theme_id}')\n"
            doc += "```\n\n"

        doc += "## 配色方案\n\n"
        doc += "每个主题包含以下颜色变量：\n\n"
        doc += "| 变量名 | 描述 | 示例 |\n"
        doc += "|--------|------|------|\n"
        doc += "| `--primary` | 主色调 | #3B82F6 |\n"
        doc += "| `--secondary` | 次要色 | #6366F1 |\n"
        doc += "| `--background` | 背景色 | #FFFFFF |\n"
        doc += "| `--surface` | 表面色 | #F9FAFB |\n"
        doc += "| `--text` | 文本色 | #111827 |\n"
        doc += "| `--accent` | 强调色 | #F59E0B |\n"
        doc += "| `--success` | 成功色 | #10B981 |\n"
        doc += "| `--warning` | 警告色 | #F59E0B |\n"
        doc += "| `--error` | 错误色 | #EF4444 |\n"
        doc += "| `--border` | 边框色 | #E5E7EB |\n\n"

        doc += "## 自定义主题\n\n"
        doc += "```python\n"
        doc += "from ui_library.themes import ThemeEngine\n\n"
        doc += "# 创建自定义主题\n"
        doc += "custom_theme = {\n"
        doc += "    'id': 'my_theme',\n"
        doc += "    'name': 'My Custom Theme',\n"
        doc += "    'mode': 'light',\n"
        doc += "    'colors': {\n"
        doc += "        'primary': '#3B82F6',\n"
        doc += "        'secondary': '#6366F1',\n"
        doc += "        # ... 更多颜色\n"
        doc += "    }\n"
        doc += "}\n\n"
        doc += "# 应用自定义主题\n"
        doc += "engine = ThemeEngine()\n"
        doc += "engine.apply_theme(custom_theme)\n"
        doc += "```\n\n"

        doc += "## 模式切换\n\n"
        doc += "支持浅色/深色模式切换：\n\n"
        doc += "```python\n"
        doc += "import streamlit as st\n\n"
        doc += "mode = st.sidebar.selectbox('主题模式', ['light', 'dark', 'auto'])\n"
        doc += "apply_theme('ocean_blue', mode=mode)\n"
        doc += "```\n\n"

        return doc

    def generate_industries_doc(self) -> str:
        """生成行业指南"""
        doc = "# 行业模板 (Industries)\n\n"
        doc += "行业专用模板和使用指南。\n\n"

        industries = [
            {
                "id": "data_analytics",
                "name": "数据分析/BI",
                "description": "数据分析行业的专用模板",
                "templates": ["BIDashboard", "ReportBuilder", "DataExplorer", "AlertMonitor", "ETLPipeline"],
                "themes": ["corporate_gray", "tech_neon", "midnight_blue"]
            },
            {
                "id": "education",
                "name": "教育培训",
                "description": "教育培训行业的专用模板",
                "templates": ["CourseCatalog", "LessonPlayer", "QuizSystem", "ProgressTracker", "DiscussionForum"],
                "themes": ["ocean_blue", "spring_blossom", "forest_green"]
            },
            {
                "id": "cms",
                "name": "内容管理",
                "description": "CMS 系统的专用模板",
                "templates": ["ArticleEditor", "MediaLibrary", "ContentList", "CategoryManager", "SEOPanel"],
                "themes": ["default_light", "midnight_blue", "corporate_gray"]
            },
            {
                "id": "ai_apps",
                "name": "AI 应用",
                "description": "AI 应用的专用模板",
                "templates": ["ChatAssistant", "ImageGenerator", "ModelPlayground", "DataAnnotation", "PipelineBuilder"],
                "themes": ["tech_neon", "cool_mint", "midnight_blue"]
            },
        ]

        for industry in industries:
            doc += f"## {industry['name']}\n\n"
            doc += f"{industry['description']}\n\n"
            doc += f"**推荐主题**: {', '.join(f'`{t}`' for t in industry['themes'])}\n\n"
            doc += f"**可用模板**:\n\n"

            for template in industry['templates']:
                doc += f"### {template}\n\n"
                doc += f"**使用示例**:\n"
                doc += "```python\n"
                doc += f"from ui_library.industries import {industry['id']}\n\n"
                doc += f"template = {industry['id']}.{template}()\n"
                doc += f"st.write(template.render_streamlit())\n"
                doc += "```\n\n"

        doc += "## 使用指南\n\n"
        doc += "### 1. 导入行业模块\n\n"
        doc += "```python\n"
        doc += "from ui_library.industries import data_analytics\n"
        doc += "```\n\n"

        doc += "### 2. 选择模板\n\n"
        doc += "```python\n"
        doc += "# 创建仪表盘\n"
        doc += "dashboard = data_analytics.BIDashboard()\n"
        doc += "\n"
        doc += "# 渲染模板\n"
        doc += "st.write(dashboard.render_streamlit())\n"
        doc += "```\n\n"

        doc += "### 3. 应用主题\n\n"
        doc += "```python\n"
        doc += "from ui_library.themes import apply_theme\n\n"
        doc += "apply_theme('tech_neon')\n"
        doc += "```\n\n"

        return doc

    def generate_api_reference_doc(self) -> str:
        """生成 API 参考文档"""
        doc = "# API 参考 (API Reference)\n\n"
        doc += "完整的 API 文档。\n\n"

        doc += "## 组件 API\n\n"
        doc += "### get_component(id)\n\n"
        doc += "获取组件定义。\n\n"
        doc += "**参数**:\n"
        doc += "- `id` (str): 组件 ID\n\n"
        doc += "**返回**: Dict[str, Any]\n\n"
        doc += "**示例**:\n"
        doc += "```python\n"
        doc += "component = get_component('DashboardPage')\n"
        doc += "```\n\n"

        doc += "### list_components(size=None, category=None)\n\n"
        doc += "列出所有组件。\n\n"
        doc += "**参数**:\n"
        doc += "- `size` (str, optional): 组件大小 ('large', 'medium')\n"
        doc += "- `category` (str, optional): 组件类别\n\n"
        doc += "**返回**: List[Dict[str, Any]]\n\n"

        doc += "## 主题 API\n\n"
        doc += "### get_theme(id)\n\n"
        doc += "获取主题定义。\n\n"
        doc += "**参数**:\n"
        doc += "- `id` (str): 主题 ID\n\n"
        doc += "**返回**: Dict[str, Any]\n\n"

        doc += "### apply_theme(id, mode='light')\n\n"
        doc += "应用主题到页面。\n\n"
        doc += "**参数**:\n"
        doc += "- `id` (str): 主题 ID\n"
        doc += "- `mode` (str): 主题模式 ('light', 'dark', 'auto')\n\n"

        doc += "## 推荐引擎 API\n\n"
        doc += "### recommend(industry, use_case, complexity='medium')\n\n"
        doc += "获取智能推荐。\n\n"
        doc += "**参数**:\n"
        doc += "- `industry` (str): 行业 ID\n"
        doc += "- `use_case` (str): 使用场景\n"
        doc += "- `complexity` (str): 复杂度 ('simple', 'medium', 'complex')\n\n"
        doc += "**返回**: Dict[str, Any]\n\n"

        doc += "## 组合 API\n\n"
        doc += "### compose(components, layout_type, theme)\n\n"
        doc += "组合多个组件生成页面。\n\n"
        doc += "**参数**:\n"
        doc += "- `components` (List[str]): 组件 ID 列表\n"
        doc += "- `layout_type` (str): 布局类型\n"
        doc += "- `theme` (str): 主题 ID\n\n"
        doc += "**返回**: str\n\n"

        doc += "## 适配器 API\n\n"
        doc += "### generate_react_component(component_def, theme)\n\n"
        doc += "生成 React 组件代码。\n\n"
        doc += "**参数**:\n"
        doc += "- `component_def` (Dict): 组件定义\n"
        doc += "- `theme` (Dict): 主题配置\n\n"
        doc += "**返回**: str\n\n"

        doc += "### generate_react_page(page_def, theme)\n\n"
        doc += "生成 React 页面代码。\n\n"
        doc += "**参数**:\n"
        doc += "- `page_def` (Dict): 页面定义\n"
        doc += "- `theme` (Dict): 主题配置\n\n"
        doc += "**返回**: str\n\n"

        return doc

    def generate_examples_doc(self) -> str:
        """生成示例文档"""
        doc = "# 示例 (Examples)\n\n"
        doc += "常见使用示例。\n\n"

        doc += "## 示例 1: 创建仪表盘\n\n"
        doc += "```python\n"
        doc += "import streamlit as st\n"
        doc += "from ui_library import get_component, get_theme, apply_theme\n"
        doc += "from ui_library.industries import data_analytics\n\n"
        doc += "# 应用主题\n"
        doc += "apply_theme('tech_neon')\n\n"
        doc += "# 创建 BI 仪表盘\n"
        doc += "dashboard = data_analytics.BIDashboard()\n"
        doc += "st.write(dashboard.render_streamlit())\n"
        doc += "```\n\n"

        doc += "## 示例 2: 智能推荐\n\n"
        doc += "```python\n"
        doc += "from ui_library import recommend\n\n"
        doc += "# 获取推荐\n"
        doc += "recommendations = recommend(\n"
        doc += "    industry='education',\n"
        doc += "    use_case='course_catalog',\n"
        doc += "    complexity='medium'\n"
        doc += ")\n\n"
        doc += "# 应用推荐\n"
        doc += "for component in recommendations['components']:\n"
        doc += "    st.write(component['code_skeleton'])\n"
        doc += "```\n\n"

        doc += "## 示例 3: 自定义组合\n\n"
        doc += "```python\n"
        doc += "from ui_library.patterns import compose_page\n\n"
        doc += "# 组合页面\n"
        doc += "page = compose_page(\n"
        doc += "    components=['HeaderBar', 'MetricCard', 'ChartPanel'],\n"
        doc += "    layout_type='dashboard',\n"
        doc += "    theme='ocean_blue'\n"
        doc += ")\n\n"
        doc += "st.write(page)\n"
        doc += "```\n\n"

        doc += "## 示例 4: React 代码生成\n\n"
        doc += "```python\n"
        doc += "from ui_library.adapters import generate_react_component\n\n"
        doc += "# 获取组件\n"
        doc += "component = get_component('DashboardPage')\n\n"
        doc += "# 生成 React 代码\n"
        doc += "react_code = generate_react_component(\n"
        doc += "    component_def=component,\n"
        doc += "    theme=get_theme('tech_neon')\n"
        doc += ")\n\n"
        doc += "# 保存文件\n"
        doc += "with open('Dashboard.tsx', 'w') as f:\n"
        doc += "    f.write(react_code)\n"
        doc += "```\n\n"

        doc += "## 示例 5: 交互模式\n\n"
        doc += "```python\n"
        doc += "from ui_library.patterns import FormPattern\n\n"
        doc += "# 使用表单模式\n"
        doc += "form = FormPattern()\n"
        doc += "st.write(form.render_streamlit())\n"
        doc += "```\n\n"

        return doc

    def generate_faq_doc(self) -> str:
        """生成 FAQ 文档"""
        doc = "# 常见问题 (FAQ)\n\n"

        faqs = [
            {
                "q": "如何安装 UI Library Pro?",
                "a": "使用 pip 安装: `pip install ui-library-pro`"
            },
            {
                "q": "支持哪些框架?",
                "a": "目前支持 Streamlit 和 React，Vue 支持正在开发中。"
            },
            {
                "q": "如何自定义主题?",
                "a": "可以创建自定义主题配置并使用 apply_theme() 应用。"
            },
            {
                "q": "如何贡献代码?",
                "a": "欢迎提交 Pull Request 或 Issue 到 GitHub 仓库。"
            },
            {
                "q": "是否支持 TypeScript?",
                "a": "React 代码生成器支持 TypeScript (TSX) 输出。"
            },
            {
                "q": "如何切换深色模式?",
                "a": "使用 apply_theme(id, mode='dark') 切换到深色模式。"
            },
        ]

        for faq in faqs:
            doc += f"### {faq['q']}\n\n"
            doc += f"{faq['a']}\n\n"

        return doc

    def generate_all(self) -> CompleteDocumentation:
        """
        生成所有文档

        Returns:
            CompleteDocumentation: 完整文档集
        """
        return CompleteDocumentation(
            readme=self.generate_readme(),
            components=self.generate_components_doc(),
            themes=self.generate_themes_doc(),
            industries=self.generate_industries_doc(),
            patterns="# 交互模式\n\n详见 patterns/interactions.py",
            api_reference=self.generate_api_reference_doc(),
            examples=self.generate_examples_doc(),
            faq=self.generate_faq_doc()
        )

    # ========================================================================
    # 私有辅助方法
    # ========================================================================

    def _infer_type(self, value: Any) -> str:
        """推断值的类型"""
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "number"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "any"

    def _extract_tags(self, component: Any) -> List[str]:
        """提取组件标签"""
        tags = []
        category = getattr(component, "category", "")
        if category:
            tags.append(category)
        size = getattr(component, "size", "")
        if size:
            tags.append(size)
        return tags

    def _generate_palette_chart(self, colors: Dict[str, str]) -> str:
        """生成调色板图表"""
        chart = "| 颜色 | 值 | 预览 |\n|------|-----|------|\n"
        for name, value in colors.items():
            chart += f"| {name} | `{value}` | <span style='background-color:{value};padding:8px 16px;'>&nbsp;</span> |\n"
        return chart

    def _generate_industry_use_cases(self, industry_id: str) -> List[Dict[str, str]]:
        """生成行业用例"""
        use_cases = [
            {
                "title": "基础应用",
                "description": f"使用 {industry_id} 模板构建基础应用",
                "complexity": "简单"
            },
            {
                "title": "高级应用",
                "description": f"结合多个 {industry_id} 模板构建复杂应用",
                "complexity": "中等"
            },
            {
                "title": "企业应用",
                "description": f"自定义和扩展 {industry_id} 模板",
                "complexity": "复杂"
            },
        ]
        return use_cases

    def _generate_best_practices(self, industry_id: str) -> List[str]:
        """生成最佳实践"""
        return [
            f"使用推荐的 {industry_id} 主题",
            "遵循组件组合规则",
            "保持代码模块化",
            "添加适当的错误处理",
            "优化性能和用户体验"
        ]

    def _generate_industry_code_examples(self, industry_module: Any) -> List[Dict[str, str]]:
        """生产行业代码示例"""
        examples = []
        templates = getattr(industry_module, "__all__", [])
        for template in templates[:3]:  # 只取前3个
            template_class = getattr(industry_module, template, None)
            if template_class:
                examples.append({
                    "title": f"{template} 示例",
                    "code": f"from ui_library.industries import {industry_module.__name__}\n\n"
                           f"template = {industry_module.__name__}.{template}()\n"
                           f"st.write(template.render_streamlit())"
                })
        return examples

    def _generate_integration_guide(self, industry_id: str) -> str:
        """生成集成指南"""
        return f"""
### 集成 {industry_id} 模板

1. **导入模块**
   ```python
   from ui_library.industries import {industry_id}
   ```

2. **选择模板**
   ```python
   template = {industry_id}.TemplateName()
   ```

3. **渲染内容**
   ```python
   st.write(template.render_streamlit())
   ```

4. **应用主题**
   ```python
   from ui_library.themes import apply_theme
   apply_theme('recommended_theme')
   ```

5. **自定义配置**
   ```python
   template.config.update({{ 'key': 'value' }})
   ```
"""


# ============================================================================
# 便捷函数
# ============================================================================

def generate_component_doc(component: Any) -> ComponentDoc:
    """
    生成组件文档

    Args:
        component: 组件定义对象

    Returns:
        ComponentDoc: 组件文档
    """
    base_path = os.path.dirname(os.path.dirname(__file__))
    generator = DocGenerator(base_path)
    return generator.generate_component_doc(component)


def generate_theme_preview(theme: Dict[str, Any]) -> ThemeDoc:
    """
    生成主题预览

    Args:
        theme: 主题定义字典

    Returns:
        ThemeDoc: 主题文档
    """
    base_path = os.path.dirname(os.path.dirname(__file__))
    generator = DocGenerator(base_path)
    return generator.generate_theme_doc(theme)


def generate_industry_guide(industry_id: str) -> IndustryDoc:
    """
    生成行业使用指南

    Args:
        industry_id: 行业 ID

    Returns:
        IndustryDoc: 行业文档
    """
    base_path = os.path.dirname(os.path.dirname(__file__))
    generator = DocGenerator(base_path)
    return generator.generate_industry_doc(industry_id)


def generate_all_docs() -> CompleteDocumentation:
    """
    生成所有文档

    Returns:
        CompleteDocumentation: 完整文档集
    """
    base_path = os.path.dirname(os.path.dirname(__file__))
    generator = DocGenerator(base_path)
    return generator.generate_all()


def export_to_markdown(docs: CompleteDocumentation, output_path: str) -> None:
    """
    导出文档到 Markdown 文件

    Args:
        docs: 完整文档集
        output_path: 输出目录路径
    """
    os.makedirs(output_path, exist_ok=True)

    # 导出 README
    with open(os.path.join(output_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(docs.readme)

    # 导出组件手册
    with open(os.path.join(output_path, "COMPONENTS.md"), "w", encoding="utf-8") as f:
        f.write(docs.components)

    # 导出主题指南
    with open(os.path.join(output_path, "THEMES.md"), "w", encoding="utf-8") as f:
        f.write(docs.themes)

    # 导出行业指南
    with open(os.path.join(output_path, "INDUSTRIES.md"), "w", encoding="utf-8") as f:
        f.write(docs.industries)

    # 导出交互模式
    with open(os.path.join(output_path, "PATTERNS.md"), "w", encoding="utf-8") as f:
        f.write(docs.patterns)

    # 导出 API 参考
    with open(os.path.join(output_path, "API_REFERENCE.md"), "w", encoding="utf-8") as f:
        f.write(docs.api_reference)

    # 导出示例
    with open(os.path.join(output_path, "EXAMPLES.md"), "w", encoding="utf-8") as f:
        f.write(docs.examples)

    # 导出 FAQ
    with open(os.path.join(output_path, "FAQ.md"), "w", encoding="utf-8") as f:
        f.write(docs.faq)

    print(f"Documentation exported to {output_path}")


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 枚举
    "DocFormat",
    "DocSection",
    # 数据类
    "ComponentDoc",
    "ThemeDoc",
    "IndustryDoc",
    "APIDoc",
    "CompleteDocumentation",
    # 主类
    "DocGenerator",
    # 便捷函数
    "generate_component_doc",
    "generate_theme_preview",
    "generate_industry_guide",
    "generate_all_docs",
    "export_to_markdown",
]
