"""
React Adapter - Streamlit 到 React 代码生成器
===============================================

将 Streamlit 组件语法转换为 React JSX 代码，支持 Tailwind CSS 样式输出。

核心类:
    - ComponentMapping: Streamlit → React 组件映射表
    - PropMapping: Streamlit → React 属性映射表
    - StyleMapping: Streamlit → Tailwind CSS 样式映射
    - ReactAdapter: 主适配器类

主要函数:
    - generate_react_component(component_def, theme): 生成单个 React 组件
    - generate_react_page(page_def, theme): 生成完整 React 页面
    - streamlit_to_react(code): 直接转换 Streamlit 代码到 React
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import re
import json


# ============================================================================
# 枚举定义
# ============================================================================

class ReactLibrary(Enum):
    """React UI 库选项"""
    CUSTOM = "custom"           # 自定义组件
    MUI = "mui"                 # Material-UI
    ANTD = "antd"               # Ant Design
    CHAKRA = "akra"             # Chakra UI
    TAILWIND = "tailwind"       # Tailwind UI
    SHADCN = "shadcn"           # shadcn/ui


class OutputFormat(Enum):
    """输出格式"""
    JSX = "jsx"                 # JSX 格式
    TSX = "tsx"                 # TypeScript TSX 格式
    FUNCTIONAL = "functional"   # 函数式组件
    CLASS = "class"             # 类组件


# ============================================================================
# 数据类定义
# ============================================================================

@dataclass
class ComponentMapping:
    """组件映射配置"""
    streamlit_component: str        # Streamlit 组件名
    react_component: str            # React 组件名
    library: ReactLibrary           # 使用的 UI 库
    import_path: str                # 导入路径
    prop_mappings: Dict[str, str]   # 属性映射
    needs_wrapper: bool = False     # 是否需要包装组件
    wrapper_component: str = ""     # 包装组件名


@dataclass
class PropMapping:
    """属性映射配置"""
    streamlit_prop: str
    react_prop: str
    transform_func: Optional[str] = None  # 转换函数名
    default_value: Any = None


@dataclass
class StyleMapping:
    """样式映射配置"""
    streamlit_prop: str
    tailwind_classes: str
    css_properties: Dict[str, str] = field(default_factory=dict)


@dataclass
class ReactComponentDef:
    """React 组件定义"""
    name: str
    imports: List[str]
    props: Dict[str, Any]
    state_vars: List[Dict[str, str]]
    effects: List[str]
    jsx_content: str
    styles: Dict[str, str] = field(default_factory=dict)
    is_typescript: bool = False


@dataclass
class ReactPageDef:
    """React 页面定义"""
    name: str
    components: List[ReactComponentDef]
    layout: str
    theme: Dict[str, str]
    imports: List[str]
    routing: Optional[Dict[str, str]] = None


# ============================================================================
# 组件映射表
# ============================================================================

COMPONENT_MAPPINGS: Dict[str, ComponentMapping] = {
    # 基础组件映射
    "st.button": ComponentMapping(
        streamlit_component="st.button",
        react_component="Button",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/button",
        prop_mappings={
            "label": "children",
            "on_click": "onClick",
            "disabled": "disabled",
            "type": "type",
            "key": "key",
        }
    ),
    "st.text_input": ComponentMapping(
        streamlit_component="st.text_input",
        react_component="Input",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/input",
        prop_mappings={
            "label": "placeholder",
            "value": "value",
            "on_change": "onChange",
            "max_chars": "maxLength",
            "disabled": "disabled",
            "type": "type",
        }
    ),
    "st.number_input": ComponentMapping(
        streamlit_component="st.number_input",
        react_component="Input",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/input",
        prop_mappings={
            "label": "placeholder",
            "value": "value",
            "on_change": "onChange",
            "min_value": "min",
            "max_value": "max",
            "step": "step",
            "disabled": "disabled",
        }
    ),
    "st.text_area": ComponentMapping(
        streamlit_component="st.text_area",
        react_component="Textarea",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/textarea",
        prop_mappings={
            "label": "placeholder",
            "value": "value",
            "on_change": "onChange",
            "height": "rows",
            "max_chars": "maxLength",
            "disabled": "disabled",
        }
    ),
    "st.selectbox": ComponentMapping(
        streamlit_component="st.selectbox",
        react_component="Select",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/select",
        prop_mappings={
            "label": "placeholder",
            "options": "options",
            "index": "defaultValue",
            "on_change": "onValueChange",
        }
    ),
    "st.multiselect": ComponentMapping(
        streamlit_component="st.multiselect",
        react_component="MultiSelect",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/multi-select",
        prop_mappings={
            "label": "placeholder",
            "options": "options",
            "default": "defaultValue",
            "on_change": "onChange",
        }
    ),
    "st.checkbox": ComponentMapping(
        streamlit_component="st.checkbox",
        react_component="Checkbox",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/checkbox",
        prop_mappings={
            "label": "label",
            "value": "checked",
            "on_change": "onCheckedChange",
        }
    ),
    "st.slider": ComponentMapping(
        streamlit_component="st.slider",
        react_component="Slider",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/slider",
        prop_mappings={
            "value": "value",
            "min_value": "min",
            "max_value": "max",
            "step": "step",
            "on_change": "onValueChange",
        }
    ),
    "st.date_input": ComponentMapping(
        streamlit_component="st.date_input",
        react_component="DatePicker",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/date-picker",
        prop_mappings={
            "value": "date",
            "on_change": "onDateChange",
            "min_value": "minDate",
            "max_value": "maxDate",
        }
    ),
    "st.time_input": ComponentMapping(
        streamlit_component="st.time_input",
        react_component="TimePicker",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/time-picker",
        prop_mappings={
            "value": "time",
            "on_change": "onTimeChange",
        }
    ),
    "st.file_uploader": ComponentMapping(
        streamlit_component="st.file_uploader",
        react_component="FileUpload",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/file-upload",
        prop_mappings={
            "label": "label",
            "type": "accept",
            "on_change": "onFileChange",
            "multiple": "multiple",
        }
    ),
    "st.download_button": ComponentMapping(
        streamlit_component="st.download_button",
        react_component="DownloadButton",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/download-button",
        prop_mappings={
            "label": "children",
            "data": "data",
            "file_name": "fileName",
            "mime": "mimeType",
        }
    ),

    # 布局组件映射
    "st.columns": ComponentMapping(
        streamlit_component="st.columns",
        react_component="div",
        library=ReactLibrary.TAILWIND,
        import_path="",
        prop_mappings={},
        needs_wrapper=True,
        wrapper_component="Flex"
    ),
    "st.container": ComponentMapping(
        streamlit_component="st.container",
        react_component="div",
        library=ReactLibrary.TAILWIND,
        import_path="",
        prop_mappings={},
        needs_wrapper=True,
        wrapper_component="Container"
    ),
    "st.sidebar": ComponentMapping(
        streamlit_component="st.sidebar",
        react_component="Sidebar",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/layout/sidebar",
        prop_mappings={},
        needs_wrapper=True,
        wrapper_component="SidebarLayout"
    ),
    "st.tabs": ComponentMapping(
        streamlit_component="st.tabs",
        react_component="Tabs",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/tabs",
        prop_mappings={
            "tabs": "tabs",
        }
    ),
    "st.expander": ComponentMapping(
        streamlit_component="st.expander",
        react_component="Collapsible",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/collapsible",
        prop_mappings={
            "label": "title",
            "expanded": "open",
        }
    ),
    "st.empty": ComponentMapping(
        streamlit_component="st.empty",
        react_component="Fragment",
        library=ReactLibrary.CUSTOM,
        import_path="react",
        prop_mappings={},
    ),

    # 数据展示组件映射
    "st.dataframe": ComponentMapping(
        streamlit_component="st.dataframe",
        react_component="DataTable",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/data-table",
        prop_mappings={
            "data": "data",
            "height": "height",
            "width": "width",
            "use_container_width": "responsive",
        }
    ),
    "st.table": ComponentMapping(
        streamlit_component="st.table",
        react_component="Table",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/table",
        prop_mappings={
            "data": "data",
        }
    ),
    "st.json": ComponentMapping(
        streamlit_component="st.json",
        react_component="JsonViewer",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/json-viewer",
        prop_mappings={
            "data": "data",
            "expanded": "defaultExpanded",
        }
    ),
    "st.metric": ComponentMapping(
        streamlit_component="st.metric",
        react_component="MetricCard",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/metric-card",
        prop_mappings={
            "label": "title",
            "value": "value",
            "delta": "change",
            "help": "description",
        }
    ),
    "st.progress": ComponentMapping(
        streamlit_component="st.progress",
        react_component="Progress",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/progress",
        prop_mappings={
            "value": "value",
        }
    ),
    "st.spinner": ComponentMapping(
        streamlit_component="st.spinner",
        react_component="Spinner",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/spinner",
        prop_mappings={
            "text": "label",
        }
    ),
    "st.status": ComponentMapping(
        streamlit_component="st.status",
        react_component="StatusIndicator",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/status-indicator",
        prop_mappings={
            "label": "label",
            "state": "state",
        }
    ),

    # 媒体组件映射
    "st.image": ComponentMapping(
        streamlit_component="st.image",
        react_component="Image",
        library=ReactLibrary.CUSTOM,
        import_path="next/image",
        prop_mappings={
            "image": "src",
            "caption": "alt",
            "width": "width",
            "use_column_width": "responsive",
        }
    ),
    "st.audio": ComponentMapping(
        streamlit_component="st.audio",
        react_component="AudioPlayer",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/audio-player",
        prop_mappings={
            "data": "src",
            "format": "format",
        }
    ),
    "st.video": ComponentMapping(
        streamlit_component="st.video",
        react_component="VideoPlayer",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/video-player",
        prop_mappings={
            "data": "src",
            "format": "format",
        }
    ),

    # 反馈组件映射
    "st.success": ComponentMapping(
        streamlit_component="st.success",
        react_component="Alert",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/alert",
        prop_mappings={
            "message": "children",
        }
    ),
    "st.error": ComponentMapping(
        streamlit_component="st.error",
        react_component="Alert",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/alert",
        prop_mappings={
            "message": "children",
        }
    ),
    "st.warning": ComponentMapping(
        streamlit_component="st.warning",
        react_component="Alert",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/alert",
        prop_mappings={
            "message": "children",
        }
    ),
    "st.info": ComponentMapping(
        streamlit_component="st.info",
        react_component="Alert",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/alert",
        prop_mappings={
            "message": "children",
        }
    ),
    "st.exception": ComponentMapping(
        streamlit_component="st.exception",
        react_component="ExceptionDisplay",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/exception-display",
        prop_mappings={
            "element": "error",
        }
    ),
    "st.toast": ComponentMapping(
        streamlit_component="st.toast",
        react_component="Toast",
        library=ReactLibrary.SHADCN,
        import_path="@/components/ui/toast",
        prop_mappings={
            "message": "title",
            "icon": "icon",
        }
    ),

    # 图表组件映射
    "st.line_chart": ComponentMapping(
        streamlit_component="st.line_chart",
        react_component="LineChart",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/charts/line-chart",
        prop_mappings={
            "data": "data",
            "width": "width",
            "height": "height",
            "use_container_width": "responsive",
        }
    ),
    "st.bar_chart": ComponentMapping(
        streamlit_component="st.bar_chart",
        react_component="BarChart",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/charts/bar-chart",
        prop_mappings={
            "data": "data",
            "width": "width",
            "height": "height",
            "use_container_width": "responsive",
        }
    ),
    "st.area_chart": ComponentMapping(
        streamlit_component="st.area_chart",
        react_component="AreaChart",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/charts/area-chart",
        prop_mappings={
            "data": "data",
            "width": "width",
            "height": "height",
            "use_container_width": "responsive",
        }
    ),
    "st.plotly_chart": ComponentMapping(
        streamlit_component="st.plotly_chart",
        react_component="PlotlyChart",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/charts/plotly-chart",
        prop_mappings={
            "figure_or_data": "figure",
            "use_container_width": "responsive",
        }
    ),

    # 导航组件映射
    "st.page_link": ComponentMapping(
        streamlit_component="st.page_link",
        react_component="Link",
        library=ReactLibrary.CUSTOM,
        import_path="next/link",
        prop_mappings={
            "page": "href",
            "label": "children",
        }
    ),
    "st.navigation": ComponentMapping(
        streamlit_component="st.navigation",
        react_component="Navigation",
        library=ReactLibrary.CUSTOM,
        import_path="@/components/navigation",
        prop_mappings={
            "pages": "items",
        }
    ),

    # 状态控制组件映射
    "st.session_state": ComponentMapping(
        streamlit_component="st.session_state",
        react_component="useState",
        library=ReactLibrary.CUSTOM,
        import_path="react",
        prop_mappings={},
    ),
    "st.rerun": ComponentMapping(
        streamlit_component="st.rerun",
        react_component="forceUpdate",
        library=ReactLibrary.CUSTOM,
        import_path="",
        prop_mappings={},
    ),
}


# ============================================================================
# 样式映射表 (Tailwind CSS)
# ============================================================================

STYLE_MAPPINGS: Dict[str, List[StyleMapping]] = {
    "spacing": [
        StyleMapping("padding", "p-4", {"padding": "1rem"}),
        StyleMapping("margin", "m-4", {"margin": "1rem"}),
        StyleMapping("gap", "gap-4", {"gap": "1rem"}),
    ],
    "sizing": [
        StyleMapping("width", "w-full", {"width": "100%"}),
        StyleMapping("height", "h-full", {"height": "100%"}),
        StyleMapping("min_width", "min-w-fit", {"min-width": "fit-content"}),
        StyleMapping("max_width", "max-w-7xl", {"max-width": "80rem"}),
    ],
    "typography": [
        StyleMapping("font_size", "text-base", {"font-size": "1rem"}),
        StyleMapping("font_weight", "font-semibold", {"font-weight": "600"}),
        StyleMapping("text_align", "text-center", {"text-align": "center"}),
        StyleMapping("line_height", "leading-relaxed", {"line-height": "1.625"}),
    ],
    "colors": [
        StyleMapping("color", "text-primary", {"color": "var(--primary)"}),
        StyleMapping("background_color", "bg-primary", {"background-color": "var(--primary)"}),
        StyleMapping("border_color", "border-primary", {"border-color": "var(--primary)"}),
    ],
    "borders": [
        StyleMapping("border", "border rounded", {"border": "1px solid", "border-radius": "0.375rem"}),
        StyleMapping("border_width", "border-2", {"border-width": "2px"}),
        StyleMapping("border_radius", "rounded-lg", {"border-radius": "0.5rem"}),
    ],
    "flexbox": [
        StyleMapping("display_flex", "flex", {"display": "flex"}),
        StyleMapping("flex_direction", "flex-row", {"flex-direction": "row"}),
        StyleMapping("justify_content", "justify-center", {"justify-content": "center"}),
        StyleMapping("align_items", "items-center", {"align-items": "center"}),
        StyleMapping("flex_wrap", "flex-wrap", {"flex-wrap": "wrap"}),
    ],
    "grid": [
        StyleMapping("display_grid", "grid", {"display": "grid"}),
        StyleMapping("grid_columns", "grid-cols-3", {"grid-template-columns": "repeat(3, minmax(0, 1fr))"}),
        StyleMapping("grid_gap", "gap-4", {"gap": "1rem"}),
    ],
    "position": [
        StyleMapping("position", "relative", {"position": "relative"}),
        StyleMapping("top", "top-0", {"top": "0"}),
        StyleMapping("left", "left-0", {"left": "0"}),
        StyleMapping("z_index", "z-10", {"z-index": "10"}),
    ],
    "effects": [
        StyleMapping("shadow", "shadow-lg", {"box-shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)"}),
        StyleMapping("opacity", "opacity-50", {"opacity": "0.5"}),
        StyleMapping("transition", "transition-all", {"transition": "all 150ms ease-in-out"}),
    ],
}


# ============================================================================
# React Adapter 主类
# ============================================================================

class ReactAdapter:
    """
    React 框架适配器

    将 Streamlit 组件定义转换为 React JSX 代码。

    主要方法:
        - convert_component(component_def): 转换单个组件
        - convert_page(page_def, theme): 转换完整页面
        - apply_theme(theme): 应用主题样式
        - generate_imports(components): 生成导入语句
    """

    def __init__(
        self,
        output_format: OutputFormat = OutputFormat.TSX,
        ui_library: ReactLibrary = ReactLibrary.SHADCN,
        use_tailwind: bool = True,
        use_typescript: bool = True
    ):
        """
        初始化 React 适配器

        Args:
            output_format: 输出格式 (JSX/TSX)
            ui_library: 使用的 UI 库
            use_tailwind: 是否使用 Tailwind CSS
            use_typescript: 是否使用 TypeScript
        """
        self.output_format = output_format
        self.ui_library = ui_library
        self.use_tailwind = use_tailwind
        self.use_typescript = use_typescript
        self.imports: set = set()
        self.state_vars: List[Dict[str, str]] = []
        self.effects: List[str] = []

    def convert_component(
        self,
        component_def: Dict[str, Any],
        theme: Optional[Dict[str, str]] = None
    ) -> ReactComponentDef:
        """
        转换单个组件定义

        Args:
            component_def: 组件定义字典
            theme: 主题配置

        Returns:
            ReactComponentDef: React 组件定义
        """
        component_id = component_def.get("id", "Component")
        component_name = self._to_pascal_case(component_id)

        # 收集导入
        self._collect_imports(component_def)

        # 转换属性
        props = self._convert_props(component_def.get("props", {}))

        # 生成状态变量
        self._generate_state_vars(component_def)

        # 生成 JSX 内容
        jsx_content = self._generate_jsx(component_def, theme)

        # 应用主题样式
        styles = self._apply_theme_styles(theme) if theme else {}

        return ReactComponentDef(
            name=component_name,
            imports=list(self.imports),
            props=props,
            state_vars=self.state_vars,
            effects=self.effects,
            jsx_content=jsx_content,
            styles=styles,
            is_typescript=self.use_typescript
        )

    def convert_page(
        self,
        page_def: Dict[str, Any],
        theme: Dict[str, str]
    ) -> ReactPageDef:
        """
        转换完整页面定义

        Args:
            page_def: 页面定义字典
            theme: 主题配置

        Returns:
            ReactPageDef: React 页面定义
        """
        page_name = page_def.get("name", "Page")
        components = page_def.get("components", [])
        layout = page_def.get("layout", "default")

        # 转换所有组件
        react_components = []
        for comp in components:
            react_comp = self.convert_component(comp, theme)
            react_components.append(react_comp)

        return ReactPageDef(
            name=page_name,
            components=react_components,
            layout=layout,
            theme=theme,
            imports=list(self.imports)
        )

    def generate_code(
        self,
        component_def: ReactComponentDef
    ) -> str:
        """
        生成完整的 React 组件代码

        Args:
            component_def: React 组件定义

        Returns:
            str: 完整的 React 组件代码
        """
        # 生成导入语句
        imports = self._generate_imports_statement(component_def.imports)

        # 生成接口定义 (TypeScript)
        interface_def = self._generate_interface(component_def) if self.use_typescript else ""

        # 生成组件签名
        component_signature = self._generate_component_signature(component_def)

        # 生成状态声明
        state_declarations = self._generate_state_declarations(component_def)

        # 生成副作用
        effects = self._generate_effects(component_def)

        # 生成 JSX 返回
        return_statement = self._generate_return(component_def)

        # 组合完整代码
        code = f"""{imports}

{interface_def}
export function {component_signature}{{
{state_declarations}
{effects}

  return (
{return_statement}
  );
}}

export default {component_def.name};
"""

        return code

    # ========================================================================
    # 私有辅助方法
    # ========================================================================

    def _to_pascal_case(self, text: str) -> str:
        """转换为 PascalCase"""
        # 移除特殊字符和数字
        text = re.sub(r'[^a-zA-Z0-9]+', ' ', text)
        # 转换为每个单词首字母大写
        words = text.split()
        return ''.join(word.capitalize() for word in words)

    def _to_camel_case(self, text: str) -> str:
        """转换为 camelCase"""
        pascal = self._to_pascal_case(text)
        return pascal[0].lower() + pascal[1:] if pascal else ""

    def _collect_imports(self, component_def: Dict[str, Any]) -> None:
        """收集所需的导入"""
        features = component_def.get("features", [])
        code_skeleton = component_def.get("code_skeleton", "")

        # 分析代码骨架中的 Streamlit 调用
        st_calls = re.findall(r'st\.\w+', code_skeleton)
        for call in st_calls:
            if call in COMPONENT_MAPPINGS:
                mapping = COMPONENT_MAPPINGS[call]
                if mapping.import_path:
                    self.imports.add(mapping.import_path)

        # 添加 React 核心
        self.imports.add("react")

        # 添加 Tailwind (如果使用)
        if self.use_tailwind:
            self.imports.add("@/styles/globals.css")

    def _convert_props(self, props: Dict[str, Any]) -> Dict[str, Any]:
        """转换属性"""
        converted = {}
        for key, value in props.items():
            # 转换为 camelCase
            react_key = self._to_camel_case(key)
            converted[react_key] = value
        return converted

    def _generate_state_vars(self, component_def: Dict[str, Any]) -> None:
        """生成状态变量"""
        features = component_def.get("features", [])

        # 根据特性生成状态
        if "状态管理" in features or "数据绑定" in features:
            self.state_vars.append({
                "name": "value",
                "type": "string",
                "initial": '""'
            })

        if "加载状态" in features or "异步操作" in features:
            self.state_vars.append({
                "name": "loading",
                "type": "boolean",
                "initial": "false"
            })

        if "错误处理" in features:
            self.state_vars.append({
                "name": "error",
                "type": "string | null",
                "initial": "null"
            })

    def _generate_jsx(
        self,
        component_def: Dict[str, Any],
        theme: Optional[Dict[str, str]] = None
    ) -> str:
        """生成 JSX 内容"""
        code_skeleton = component_def.get("code_skeleton", "")

        # 转换 Streamlit 代码到 JSX
        jsx = self._convert_streamlit_to_jsx(code_skeleton, theme)

        return jsx

    def _convert_streamlit_to_jsx(
        self,
        code: str,
        theme: Optional[Dict[str, str]] = None
    ) -> str:
        """将 Streamlit 代码转换为 JSX"""
        # 替换 st.button
        code = re.sub(
            r'st\.button\("([^"]+)"',
            r'<Button>\1</Button>',
            code
        )

        # 替换 st.text_input
        code = re.sub(
            r'st\.text_input\("([^"]+)", key="(\w+)"',
            r'<Input placeholder="\1" id="\2" />',
            code
        )

        # 替换 st.columns
        code = re.sub(
            r'st\.columns\((\d+)\)',
            r'<div className="grid grid-cols-\1 gap-4">',
            code
        )

        # 替换 st.sidebar
        code = re.sub(
            r'with st\.sidebar:',
            r'<Sidebar>',
            code
        )

        # 替换 st.write
        code = re.sub(
            r'st\.write\(([^)]+)\)',
            r'<p>{\1}</p>',
            code
        )

        # 替换 st.markdown
        code = re.sub(
            r'st\.markdown\("([^"]+)"\)',
            r'<div className="prose">\1</div>',
            code
        )

        # 替换 st.metric
        code = re.sub(
            r'st\.metric\("([^"]+)",\s*"([^"]+)"',
            r'<MetricCard title="\1" value="\2" />',
            code
        )

        # 替换 st.progress
        code = re.sub(
            r'st\.progress\(([\d.]+)\)',
            r'<Progress value={\1 * 100} />',
            code
        )

        # 应用主题样式
        if theme:
            code = self._apply_theme_to_jsx(code, theme)

        return code

    def _apply_theme_to_jsx(self, jsx: str, theme: Dict[str, str]) -> str:
        """将主题样式应用到 JSX"""
        # 这里可以根据主题配置添加 className
        if theme.get("mode") == "dark":
            # 添加深色模式类
            jsx = re.sub(
                r'className="([^"]*)"',
                r'className="\1 dark"',
                jsx
            )
        return jsx

    def _apply_theme_styles(self, theme: Dict[str, str]) -> Dict[str, str]:
        """应用主题样式"""
        styles = {}

        # 主题颜色映射
        color_vars = {
            "primary": "--primary",
            "secondary": "--secondary",
            "background": "--background",
            "surface": "--surface",
            "text": "--text",
            "accent": "--accent",
        }

        for key, var in color_vars.items():
            if key in theme:
                styles[var] = theme[key]

        return styles

    def _generate_imports_statement(self, imports: List[str]) -> str:
        """生成导入语句"""
        statements = []

        # React 核心
        if "react" in imports:
            ts_import = "import React, { " if self.use_typescript else "import { "
            statements.append(f'{ts_import}useState, useEffect }} from "react";')

        # 其他导入
        for imp in imports:
            if imp not in ["react", "@/styles/globals.css"]:
                statements.append(f'import {{ }} from "{imp}";')

        # 样式
        if "@/styles/globals.css" in imports:
            statements.append('import "@/styles/globals.css";')

        return "\n".join(statements)

    def _generate_interface(self, component_def: ReactComponentDef) -> str:
        """生成 TypeScript 接口"""
        if not self.use_typescript:
            return ""

        interface_name = f"{component_def.name}Props"

        props_def = []
        for prop, value in component_def.props.items():
            prop_type = "string"
            if isinstance(value, bool):
                prop_type = "boolean"
            elif isinstance(value, int):
                prop_type = "number"
            elif isinstance(value, list):
                prop_type = "any[]"

            props_def.append(f"  {prop}?: {prop_type};")

        if not props_def:
            return ""

        interface = f"interface {interface_name} {{\n{chr(10).join(props_def)}\n}}\n"
        return interface

    def _generate_component_signature(self, component_def: ReactComponentDef) -> str:
        """生成组件签名"""
        interface_name = f"{component_def.name}Props"

        if self.use_typescript:
            return f"{component_def.name}: {{ }} : {interface_name} "
        else:
            return f"{component_def.name}() "

    def _generate_state_declarations(self, component_def: ReactComponentDef) -> str:
        """生成状态声明"""
        declarations = []

        for state_var in component_def.state_vars:
            name = state_var["name"]
            type_annotation = f": {state_var['type']}" if self.use_typescript else ""
            initial = state_var["initial"]
            declarations.append(f"  const [{name}, set{name.capitalize()}] = useState{type_annotation}({initial});")

        return "\n".join(declarations) if declarations else "  // State declarations"

    def _generate_effects(self, component_def: ReactComponentDef) -> str:
        """生成副作用钩子"""
        if not component_def.effects:
            return "  // Effects"

        effects = []
        for effect in component_def.effects:
            effects.append(f"  {effect}")

        return "\n".join(effects)

    def _generate_return(self, component_def: ReactComponentDef) -> str:
        """生成返回语句"""
        jsx = component_def.jsx_content

        # 缩进 JSX
        lines = jsx.split("\n")
        indented = ["    " + line for line in lines]

        return "\n".join(indented)


# ============================================================================
# 便捷函数
# ============================================================================

def generate_react_component(
    component_def: Dict[str, Any],
    theme: Optional[Dict[str, str]] = None,
    **kwargs
) -> str:
    """
    生成 React 组件代码

    Args:
        component_def: 组件定义字典
        theme: 主题配置
        **kwargs: 其他配置参数
            - output_format: 输出格式 (默认 "tsx")
            - ui_library: UI 库 (默认 "shadcn")
            - use_tailwind: 是否使用 Tailwind (默认 True)
            - use_typescript: 是否使用 TypeScript (默认 True)

    Returns:
        str: 完整的 React 组件代码
    """
    output_format = OutputFormat(kwargs.get("output_format", "tsx"))
    ui_library = ReactLibrary(kwargs.get("ui_library", "shadcn"))
    use_tailwind = kwargs.get("use_tailwind", True)
    use_typescript = kwargs.get("use_typescript", True)

    adapter = ReactAdapter(
        output_format=output_format,
        ui_library=ui_library,
        use_tailwind=use_tailwind,
        use_typescript=use_typescript
    )

    react_component = adapter.convert_component(component_def, theme)
    return adapter.generate_code(react_component)


def generate_react_page(
    page_def: Dict[str, Any],
    theme: Dict[str, str],
    **kwargs
) -> str:
    """
    生成完整 React 页面代码

    Args:
        page_def: 页面定义字典
        theme: 主题配置
        **kwargs: 其他配置参数

    Returns:
        str: 完整的 React 页面代码
    """
    output_format = OutputFormat(kwargs.get("output_format", "tsx"))
    ui_library = ReactLibrary(kwargs.get("ui_library", "shadcn"))
    use_tailwind = kwargs.get("use_tailwind", True)
    use_typescript = kwargs.get("use_typescript", True)

    adapter = ReactAdapter(
        output_format=output_format,
        ui_library=ui_library,
        use_tailwind=use_tailwind,
        use_typescript=use_typescript
    )

    react_page = adapter.convert_page(page_def, theme)

    # 生成页面级代码
    components_code = []
    for comp in react_page.components:
        comp_code = adapter.generate_code(comp)
        components_code.append(comp_code)

    # 组合完整页面
    page_code = f"""
{''.join(components_code)}

// Main Page Layout
export default function {react_page.name}() {{
  return (
    <div className="{_get_theme_classes(theme)}">
      {/* Page content here */}
    </div>
  );
}}
"""

    return page_code


def streamlit_to_react(
    code: str,
    theme: Optional[Dict[str, str]] = None
) -> str:
    """
    直接转换 Streamlit 代码到 React JSX

    Args:
        code: Streamlit Python 代码
        theme: 主题配置

    Returns:
        str: React JSX 代码
    """
    adapter = ReactAdapter()
    return adapter._convert_streamlit_to_jsx(code, theme)


def _get_theme_classes(theme: Dict[str, str]) -> str:
    """获取主题 CSS 类"""
    classes = ["min-h-screen"]

    mode = theme.get("mode", "light")
    if mode == "dark":
        classes.append("dark")

    return " ".join(classes)


# ============================================================================
# 代码模板生成器
# ============================================================================

class ReactCodeTemplates:
    """React 代码模板生成器"""

    @staticmethod
    def button_component() -> str:
        """生成按钮组件模板"""
        return '''
import React from 'react';
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'ghost';
  size?: 'default' | 'sm' | 'lg';
}

export function Button({
  className,
  variant = 'default',
  size = 'default',
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-md font-medium transition-colors",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
        "disabled:pointer-events-none disabled:opacity-50",
        {
          'bg-primary text-primary-foreground hover:bg-primary/90': variant === 'default',
          'bg-destructive text-destructive-foreground hover:bg-destructive/90': variant === 'destructive',
          'border border-input bg-background hover:bg-accent hover:text-accent-foreground': variant === 'outline',
          'hover:bg-accent hover:text-accent-foreground': variant === 'ghost',
        },
        {
          'h-10 px-4 py-2': size === 'default',
          'h-9 px-3': size === 'sm',
          'h-11 px-8': size === 'lg',
        },
        className
      )}
      {...props}
    />
  );
}
'''

    @staticmethod
    def input_component() -> str:
        """生成输入框组件模板"""
        return '''
import React from 'react';
import { cn } from "@/lib/utils";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export function Input({ className, type, ...props }: InputProps) {
  return (
    <input
      type={type}
      className={cn(
        "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2",
        "text-sm ring-offset-background file:border-0 file:bg-transparent",
        "file:text-sm file:font-medium placeholder:text-muted-foreground",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
        "disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  );
}
'''

    @staticmethod
    def card_component() -> str:
        """生成卡片组件模板"""
        return '''
import React from 'react';
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-lg border bg-card text-card-foreground shadow-sm",
        className
      )}
      {...props}
    />
  );
}

export function CardHeader({ className, ...props }: CardProps) {
  return (
    <div
      className={cn("flex flex-col space-y-1.5 p-6", className)}
      {...props}
    />
  );
}

export function CardTitle({ className, ...props }: CardProps) {
  return (
    <h3
      className={cn(
        "text-2xl font-semibold leading-none tracking-tight",
        className
      )}
      {...props}
    />
  );
}

export function CardContent({ className, ...props }: CardProps) {
  return (
    <div className={cn("p-6 pt-0", className)} {...props} />
  );
}
'''

    @staticmethod
    def metric_card_component() -> str:
        """生成指标卡片组件模板"""
        return '''
import React from 'react';
import { Card, CardHeader, CardContent } from './card';
import { cn } from '@/lib/utils';

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeType?: 'increase' | 'decrease' | 'neutral';
  icon?: React.ReactNode;
  className?: string;
}

export function MetricCard({
  title,
  value,
  change,
  changeType = 'neutral',
  icon,
  className,
}: MetricCardProps) {
  return (
    <Card className={className}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <div className="text-sm font-medium text-muted-foreground">
          {title}
        </div>
        {icon && (
          <div className="text-muted-foreground">
            {icon}
          </div>
        )}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {change !== undefined && (
          <p
            className={cn(
              'text-xs',
              changeType === 'increase' && 'text-green-600',
              changeType === 'decrease' && 'text-red-600',
              changeType === 'neutral' && 'text-muted-foreground'
            )}
          >
            {changeType === 'increase' && '+'}
            {change}% from last month
          </p>
        )}
      </CardContent>
    </Card>
  );
}
'''

    @staticmethod
    def sidebar_component() -> str:
        """生成侧边栏组件模板"""
        return '''
import React from 'react';
import { cn } from '@/lib/utils';
import Link from 'next/link';

interface SidebarItem {
  title: string;
  href: string;
  icon?: React.ReactNode;
}

interface SidebarProps {
  items: SidebarItem[];
  className?: string;
}

export function Sidebar({ items, className }: SidebarProps) {
  return (
    <aside
      className={cn(
        'w-64 border-r bg-background',
        className
      )}
    >
      <div className="flex h-full flex-col">
        <div className="h-16 border-b flex items-center px-6">
          <span className="font-semibold text-lg">Logo</span>
        </div>
        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-3">
            {items.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2',
                    'text-sm font-medium text-muted-foreground',
                    'hover:bg-accent hover:text-accent-foreground',
                    'transition-colors'
                  )}
                >
                  {item.icon}
                  {item.title}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </aside>
  );
}
'''


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 枚举
    "ReactLibrary",
    "OutputFormat",
    # 数据类
    "ComponentMapping",
    "PropMapping",
    "StyleMapping",
    "ReactComponentDef",
    "ReactPageDef",
    # 主类
    "ReactAdapter",
    # 便捷函数
    "generate_react_component",
    "generate_react_page",
    "streamlit_to_react",
    # 模板
    "ReactCodeTemplates",
]
