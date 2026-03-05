"""
Medium Components - 中型组件库（区块级）
=========================================

包含 12 个区块级组件模板，每个都是可独立使用的功能模块。

组件列表:
    1. MetricCard - 指标卡片
    2. ChartPanel - 图表面板
    3. FilterBar - 筛选栏
    4. DataList - 数据列表
    5. NavSidebar - 导航侧边栏
    6. HeaderBar - 顶部导航栏
    7. FooterBar - 页脚
    8. AlertPanel - 通知面板
    9. UploadZone - 上传区域
    10. CommentSection - 评论区块
    11. TimelineBlock - 时间线
    12. PricingTable - 价格表
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# 组件分类枚举
# ============================================================================

class MediumComponentCategory(Enum):
    """中型组件分类"""
    DATA_DISPLAY = "data_display"     # 数据展示
    INPUT = "input"                   # 输入
    NAVIGATION = "navigation"         # 导航
    LAYOUT = "layout"                 # 布局
    FEEDBACK = "feedback"             # 反馈
    MEDIA = "media"                   # 媒体
    CONTENT = "content"               # 内容
    COMMERCE = "commerce"             # 商务


# ============================================================================
# 组件属性定义（复用大型组件结构）
# ============================================================================

@dataclass
class ComponentProp:
    """组件属性定义"""
    name: str
    type: str
    default: Any = None
    required: bool = False
    description: str = ""
    options: Optional[List[Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.type,
            "default": self.default,
            "required": self.required,
            "description": self.description,
            "options": self.options,
        }


# ============================================================================
# 中型组件定义
# ============================================================================

@dataclass
class MediumComponent:
    """
    中型组件定义

    Attributes:
        id: 组件唯一标识符
        name: 组件名称
        category: 组件分类
        description: 组件描述
        preview: ASCII 预览图
        features: 特性列表
        code_skeleton: Streamlit 代码骨架
        props: 可配置属性列表
        tags: 标签列表
        dependencies: 依赖项
        industry_compatibility: 适用行业
        composable: 是否可组合（用于构建大型组件）
    """
    id: str
    name: str
    category: MediumComponentCategory
    description: str
    preview: str
    features: List[str]
    code_skeleton: str
    props: List[ComponentProp] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    industry_compatibility: List[str] = field(default_factory=lambda: ["general"])
    composable: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "preview": self.preview,
            "features": self.features,
            "props": [p.to_dict() for p in self.props],
            "tags": self.tags,
            "dependencies": self.dependencies,
            "industry_compatibility": self.industry_compatibility,
            "composable": self.composable,
        }

    def get_code(self, **kwargs) -> str:
        """
        获取带参数的代码

        Args:
            **kwargs: 组件属性值

        Returns:
            格式化后的代码字符串
        """
        code = self.code_skeleton
        for key, value in kwargs.items():
            placeholder = f"{{{{{key}}}}}"
            code = code.replace(placeholder, str(value))
        return code


# ============================================================================
# 1. MetricCard - 指标卡片
# ============================================================================

METRIC_CARD = MediumComponent(
    id="metric_card",
    name="指标卡片",
    category=MediumComponentCategory.DATA_DISPLAY,
    description="""
    数据指标展示卡片，用于显示关键KPI及其趋势变化。
    适用于仪表盘、统计页面、数据概览等场景。
    """,
    preview="""
    ┌─────────────────────┐
    │  💰 总销售额        │
    │                     │
    │    ¥128,500         │
    │    ↗ 15.2%         │
    │                     │
    │  较上月 +¥16,800    │
    └─────────────────────┘
    """,
    features=[
        "📊 数值展示 - 大字号显示核心指标",
        "📈 趋势指示 - 上升/下降/持平箭头",
        "📉 变化率 - 百分比或绝对值变化",
        "🎨 颜色编码 - 红绿配色表示正负向",
        "🏷️ 图标支持 - 自定义图标或 emoji",
        "⏱️ 时间范围 - 显示对比时间区间",
        "📊 迷你图表 - 嵌入迷你折线图",
        "🔗 点击交互 - 可跳转详情页",
    ],
    code_skeleton="""
import streamlit as st

# ==================== 配置区 ====================
TITLE = "{{title}}"  # 标题
VALUE = "{{value}}"  # 主数值
DELTA = "{{delta}}"  # 变化值
ICON = "{{icon}}"  # 图标
SHOW_DELTA = {{show_delta}}  # 显示变化
COLOR = "{{color}}"  # 颜色主题

# ==================== 主卡片 ====================
# 颜色映射
color_map = {
    "green": {"bg": "#d4edda", "text": "#155724", "icon": "📈"},
    "red": {"bg": "#f8d7da", "text": "#721c24", "icon": "📉"},
    "blue": {"bg": "#d1ecf1", "text": "#0c5460", "icon": "💙"},
    "yellow": {"bg": "#fff3cd", "text": "#856404", "icon": "💛"},
}
colors = color_map.get(COLOR, color_map["blue"])

# 显示卡片
st.markdown(f\"\"\"
<div style='background: {colors['bg']}; padding: 1.5rem; border-radius: 8px; border-left: 4px solid {colors['text']};'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <div style='color: {colors['text']}; font-size: 0.9rem; margin-bottom: 0.5rem;'>
                {ICON} {TITLE}
            </div>
            <div style='font-size: 2rem; font-weight: bold; color: {colors['text']};'>
                {VALUE}
            </div>
        </div>
    </div>
\"\"\", unsafe_allow_html=True)

# 显示变化
if SHOW_DELTA and DELTA:
    delta_color = "green" if DELTA.startswith("+") or DELTA.startswith("↗") else "red"
    st.markdown(f\"\"\"
<div style='color: {delta_color}; font-size: 0.9rem; margin-top: 0.5rem;'>
    {DELTA} 较上月
</div>
\"\"\", unsafe_allow_html=True)

# ==================== 使用 Streamlit Metric（备选） ====================
# st.metric(
#     label=f\"{ICON} {TITLE}\",
#     value=VALUE,
#     delta=DELTA if SHOW_DELTA else None
# )
""",
    props=[
        ComponentProp("title", "str", "总销售额", True, "卡片标题"),
        ComponentProp("value", "str", "¥128,500", True, "主显示数值"),
        ComponentProp("delta", "str", "+15.2%", False, "变化值"),
        ComponentProp("icon", "str", "💰", False, "图标 emoji"),
        ComponentProp("show_delta", "bool", True, False, "显示变化率"),
        ComponentProp("color", "str", "blue", False, "颜色主题"),
    ],
    tags=["卡片", "指标", "KPI", "数据展示"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "finance", "ecommerce", "healthcare"],
)


# ============================================================================
# 2. ChartPanel - 图表面板
# ============================================================================

CHART_PANEL = MediumComponent(
    id="chart_panel",
    name="图表面板",
    category=MediumComponentCategory.DATA_DISPLAY,
    description="""
    可配置的图表面板，支持多种图表类型和交互功能。
    适用于数据分析、趋势展示、对比图表等场景。
    """,
    preview="""
    ┌─────────────────────────────────────┐
    │  📈 销售趋势         [折线] [柱状] │
    ├─────────────────────────────────────┤
    │                                     │
    │     100 ┤          ╱╲               │
    │      80 ┤        ╱  ╲╱╲             │
    │      60 ┤   ╱╲╱╱      ╲            │
    │      40 ┤ ╱╱            ╲          │
    │      20 ┤╱╱               ╲╱       │
    │       0 └──────────────────────   │
    │         1月 2月 3月 4月 5月 6月   │
    │                                     │
    │  [📥导出] [🔍放大] [⚙️设置]      │
    └─────────────────────────────────────┘
    """,
    features=[
        "📊 多种图表 - 折线、柱状、面积、饼图",
        "🎨 自定义样式 - 颜色、字体、边框",
        "📱 响应式 - 自适应容器大小",
        "🔍 缩放功能 - 放大查看细节",
        "📥 数据导出 - 导出图表数据",
        "🔄 动态更新 - 实时数据刷新",
        "📊 多轴支持 - 双Y轴对比",
        "🏷️ 图例控制 - 显示/隐藏图例",
        "📊 堆叠模式 - 多系列堆叠显示",
        "🎯 数据点提示 - 悬停显示数值",
    ],
    code_skeleton="""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ==================== 配置区 ====================
TITLE = "{{title}}"  # 图表标题
CHART_TYPE = "{{chart_type}}"  # 图表类型
SHOW_EXPORT = {{show_export}}  # 显示导出按钮
SHOW_ZOOM = {{show_zoom}}  # 显示缩放按钮

# ==================== 模拟数据 ====================
dates = pd.date_range(\"2024-01-01\", periods=6, freq=\"MS\")
values = [65, 78, 52, 88, 95, 72]

# ==================== 图表类型选择 ====================
chart_type = st.selectbox(
    \"图表类型\",
    [\"折线图\", \"柱状图\", \"面积图\", \"饼图\"],
    index=[\"line\", \"bar\", \"area\", \"pie\"].index(CHART_TYPE)
)

# ==================== 创建图表 ====================
fig = go.Figure()

if chart_type == \"折线图\":
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode=\"lines+markers\",
        name=\"销售额\",
        line=dict(color=\"#007bff\", width=3),
        marker=dict(size=8)
    ))

elif chart_type == \"柱状图\":
    fig.add_trace(go.Bar(
        x=dates,
        y=values,
        name=\"销售额\",
        marker_color=\"#007bff\"
    ))

elif chart_type == \"面积图\":
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        fill=\"tozeroy\",
        mode=\"lines\",
        name=\"销售额\",
        line=dict(color=\"#007bff\", width=2)
    ))

elif chart_type == \"饼图\":
    fig.add_trace(go.Pie(
        labels=[\"1月\", \"2月\", \"3月\", \"4月\", \"5月\", \"6月\"],
        values=values,
        hole=0.3
    ))

# ==================== 图表布局 ====================
fig.update_layout(
    title=dict(text=f\"📈 {TITLE}\", x=0.5, xanchor=\"center\"),
    xaxis_title=\"日期\",
    yaxis_title=\"金额\",
    hovermode=\"x unified\",
    height=400,
    margin=dict(l=20, r=20, t=40, b=20),
)

# ==================== 显示图表 ====================
st.plotly_chart(fig, use_container_width=True)

# ==================== 操作按钮 ====================
col1, col2, col3 = st.columns(3)

with col1:
    if SHOW_EXPORT and st.button(\"📥 导出数据\"):
        csv = pd.DataFrame({\"日期\": dates, \"数值\": values}).to_csv(index=False)
        st.download_button(\"下载 CSV\", csv, \"data.csv\", \"text/csv\")

with col2:
    if SHOW_ZOOM and st.button(\"🔍 放大查看\"):
        st.info(\"全屏查看功能\")

with col3:
    if st.button(\"⚙️ 设置\"):
        with st.expander(\"图表设置\", expanded=True):
            color = st.color_picker(\"主颜色\", \"#007bff\")
            show_grid = st.checkbox(\"显示网格线\", value=True)
            show_legend = st.checkbox(\"显示图例\", value=True)

# ==================== 使用 Streamlit 原生图表（备选） ====================
# st.line_chart(pd.DataFrame({\"日期\": dates, \"数值\": values}).set_index(\"日期\"))
# st.bar_chart(pd.DataFrame({\"日期\": dates, \"数值\": values}).set_index(\"日期\"))
# st.area_chart(pd.DataFrame({\"日期\": dates, \"数值\": values}).set_index(\"日期\"))
""",
    props=[
        ComponentProp("title", "str", "销售趋势", True, "图表标题"),
        ComponentProp("chart_type", "str", "line", False, "默认图表类型"),
        ComponentProp("show_export", "bool", True, False, "显示导出按钮"),
        ComponentProp("show_zoom", "bool", True, False, "显示缩放按钮"),
        ComponentProp("height", "int", 400, False, "图表高度"),
    ],
    tags=["图表", "数据可视化", "分析", "趋势"],
    dependencies=["streamlit", "plotly", "pandas"],
    industry_compatibility=["general", "finance", "healthcare", "ecommerce", "manufacturing"],
)


# ============================================================================
# 3. FilterBar - 筛选栏
# ============================================================================

FILTER_BAR = MediumComponent(
    id="filter_bar",
    name="筛选栏",
    category=MediumComponentCategory.INPUT,
    description="""
    多条件筛选组件，支持日期范围、下拉选择、关键词搜索。
    适用于数据列表、表格筛选、搜索功能等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────┐
    │  🔍 搜索框__________  [▼状态]  [📅日期]   │
    │                                              │
    │  已选: [状态:激活 ×] [日期:1月 ×]          │
    │                                              │
    │  [应用筛选]  [清除全部]    共: 1,234 条    │
    └─────────────────────────────────────────────┘
    """,
    features=[
        "🔍 关键词搜索 - 实时搜索过滤",
        "📅 日期范围 - 快捷日期选择",
        "▼ 下拉筛选 - 单选/多选下拉框",
        "🏷️ 标签筛选 - 可移除的筛选标签",
        "✅ 复选框 - 多选项同时筛选",
        "📊 数值范围 - 滑块范围选择",
        "💾 保存筛选 - 保存常用筛选条件",
        "🔄 快捷预设 - 一日/一周/一月快捷",
    ],
    code_skeleton="""
import streamlit as st
from datetime import datetime, timedelta

# ==================== 配置区 ====================
SHOW_SEARCH = {{show_search}}  # 显示搜索框
SHOW_DATE_RANGE = {{show_date_range}}  # 显示日期范围
SHOW_STATUS_FILTER = {{show_status_filter}}  # 显示状态筛选
PRESET_PERIODS = {{preset_periods}}  # 预设时间段

# ==================== 筛选容器 ====================
with st.container():
    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])

    # 搜索框
    if SHOW_SEARCH:
        with col1:
            search_keyword = st.text_input(
                \"🔍 搜索\",
                placeholder=\"输入关键词...\",
                label_visibility=\"collapsed\"
            )

    # 日期范围
    if SHOW_DATE_RANGE:
        with col2:
            date_range = st.selectbox(
                \"时间范围\",
                [\"今日\", \"昨日\", \"最近7天\", \"最近30天\", \"自定义\"],
                label_visibility=\"collapsed\"
            )

        if date_range == \"自定义\":
            with col3:
                col_start, col_end = st.columns(2)
                with col_start:
                    start_date = st.date_input(\"开始\", datetime.now() - timedelta(days=30))
                with col_end:
                    end_date = st.date_input(\"结束\", datetime.now())

    # 状态筛选
    if SHOW_STATUS_FILTER:
        with col4:
            status_filter = st.multiselect(
                \"状态\",
                [\"激活\", \"禁用\", \"待审核\"],
                default=[],
                label_visibility=\"collapsed\"
            )

    # 分类筛选
    with col5:
        category_filter = st.selectbox(
            \"分类\",
            [\"全部\", \"类别A\", \"类别B\", \"类别C\"],
            label_visibility=\"collapsed\"
        )

# ==================== 已选筛选标签 ====================
st.divider()

# 初始化筛选状态
if \"active_filters\" not in st.session_state:
    st.session_state.active_filters = {}

# 显示已选筛选
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    if st.session_state.active_filters:
        st.write(\"**已选筛选:**\")
        tags_html = \" \".join([
            f\"<span style='background: #e9ecef; padding: 0.3rem 0.6rem; border-radius: 20px; margin-right: 0.5rem;'>{k}: {v} ×</span>\"
            for k, v in st.session_state.active_filters.items()
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
    else:
        st.caption(\"暂无筛选条件\")

with col2:
    if st.button(\"🔄 重置\", use_container_width=True):
        st.session_state.active_filters = {}
        st.rerun()

with col3:
    result_count = 1234
    st.metric(\"结果\", result_count)

# ==================== 高级筛选（展开式） ====================
with st.expander(\"⚙️ 高级筛选\", expanded=False):
    col1, col2, col3 = st.columns(3)

    with col1:
        min_value = st.number_input(\"最小值\", value=0)
        max_value = st.number_input(\"最大值\", value=1000)

    with col2:
        sort_by = st.selectbox(\"排序\", [\"时间\", \"相关性\", \"热度\"])
        sort_order = st.radio(\"顺序\", [\"升序\", \"降序\"], horizontal=True)

    with col3:
        include_archived = st.checkbox(\"包含已归档\")
        only_favorites = st.checkbox(\"仅收藏\")

# ==================== 应用筛选按钮 ====================
col1, col2 = st.columns([4, 1])

with col1:
    st.write(\"\")  # 占位

with col2:
    apply_button = st.button(\"✅ 应用筛选\", use_container_width=True, type=\"primary\")

if apply_button:
    # 保存筛选条件
    if search_keyword:
        st.session_state.active_filters[\"搜索\"] = search_keyword
    if status_filter:
        st.session_state.active_filters[\"状态\"] = \", \".join(status_filter)
    if category_filter != \"全部\":
        st.session_state.active_filters[\"分类\"] = category_filter

    st.success(f\"✅ 筛选已应用，找到 {result_count} 条结果\")
    st.rerun()
""",
    props=[
        ComponentProp("show_search", "bool", True, False, "显示搜索框"),
        ComponentProp("show_date_range", "bool", True, False, "显示日期范围"),
        ComponentProp("show_status_filter", "bool", True, False, "显示状态筛选"),
        ComponentProp("preset_periods", "list", ["今日", "昨日", "最近7天"], False, "预设时间段"),
        ComponentProp("enable_advanced", "bool", True, False, "启用高级筛选"),
    ],
    tags=["筛选", "搜索", "过滤器", "表单"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "ecommerce", "finance", "healthcare"],
)


# ============================================================================
# 4. DataList - 数据列表
# ============================================================================

DATA_LIST = MediumComponent(
    id="data_list",
    name="数据列表",
    category=MediumComponentCategory.DATA_DISPLAY,
    description="""
    结构化数据列表，支持行操作、批量选择、分页。
    适用于用户列表、文件列表、任务列表等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────┐
    │  □  张三     zhang@qq.com     [编辑][删除]  │
    │  □  李四     li@qq.com        [编辑][删除]  │
    │  □  王五     wang@qq.com      [编辑][删除]  │
    │  □  赵六     zhao@qq.com      [编辑][删除]  │
    │                                              │
    │  已选: 2     [批量删除]     [◀ 1 2 3 ▶]    │
    └─────────────────────────────────────────────┘
    """,
    features=[
        "📋 列表展示 - 清晰的行布局",
        "✅ 多选模式 - 复选框批量选择",
        "⚙️ 行操作 - 编辑/删除/复制",
        "🔍 行内搜索 - 高亮匹配内容",
        "📄 分页导航 - 自定义每页条数",
        "🔄 排序功能 - 点击列头排序",
        "🎨 行样式 - 斑马纹、悬停高亮",
        "📊 空状态 - 无数据提示",
        "⏳ 加载状态 -骨架屏加载",
        "🗑️ 批量操作 - 批量删除/导出",
    ],
    code_skeleton="""
import streamlit as st
import pandas as pd
from typing import List, Dict

# ==================== 配置区 ====================
TITLE = \"{{title}}\"  # 列表标题
SHOW_CHECKBOX = {{show_checkbox}}  # 显示复选框
SHOW_ACTIONS = {{show_actions}}  # 显示操作按钮
PAGE_SIZE = {{page_size}}  # 每页条数

# ==================== 模拟数据 ====================
data = [
    {\"name\": \"张三\", \"email\": \"zhang@qq.com\", \"status\": \"激活\", \"role\": \"管理员\"},
    {\"name\": \"李四\", \"email\": \"li@qq.com\", \"status\": \"激活\", \"role\": \"用户\"},
    {\"name\": \"王五\", \"email\": \"wang@qq.com\", \"status\": \"禁用\", \"role\": \"用户\"},
    {\"name\": \"赵六\", \"email\": \"zhao@qq.com\", \"status\": \"激活\", \"role\": \"编辑\"},
    {\"name\": \"钱七\", \"email\": \"qian@qq.com\", \"status\": \"激活\", \"role\": \"用户\"},
]

# ==================== 顶部操作栏 ====================
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.subheader(f\"📋 {TITLE}\")

with col2:
    if st.button(\"+ 新建\", use_container_width=True):
        st.info(\"打开新建表单\")

with col3:
    if st.button(\"🔄 刷新\", use_container_width=True):
        st.rerun()

# ==================== 筛选栏 ====================
with st.expander(\"🔍 筛选\", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input(\"搜索\", placeholder=\"搜索姓名或邮箱\")
    with col2:
        status_filter = st.multiselect(\"状态\", [\"激活\", \"禁用\"], default=[])

# ==================== 数据列表 ====================
st.divider()

# 初始化选择状态
if \"selected_items\" not in st.session_state:
    st.session_state.selected_items = []

# 分页
total_items = len(data)
total_pages = (total_items - 1) // PAGE_SIZE + 1

col1, col2, col3 = st.columns(3)
with col1:
    current_page = st.number_input(\"页码\", 1, total_pages, 1)
with col2:
    page_size = st.selectbox(\"每页\", [5, 10, 20, 50], index=0)
with col3:
    st.write(f\"共 {total_items} 条\")

# 数据切片
start_idx = (current_page - 1) * page_size
end_idx = start_idx + page_size
page_data = data[start_idx:end_idx]

# 显示列表
for i, item in enumerate(page_data):
    col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])

    with col1:
        if SHOW_CHECKBOX:
            checked = st.checkbox(\"\", key=f\"check_{i}\")
            if checked and item not in st.session_state.selected_items:
                st.session_state.selected_items.append(item)

    with col2:
        st.write(f\"**{item['name']}**\")

    with col3:
        st.caption(item[\"email\"])

    with col4:
        status_color = \"🟢\" if item[\"status\"] == \"激活\" else \"🔴\"
        st.write(f\"{status_color} {item['status']}\")

    with col5:
        if SHOW_ACTIONS:
            action_col1, action_col2 = st.columns(2)
            with action_col1:
                if st.button(\"✏️\", key=f\"edit_{i}\"):
                    st.info(f\"编辑 {item['name']}\")
            with action_col2:
                if st.button(\"🗑️\", key=f\"delete_{i}\"):
                    st.warning(f\"删除 {item['name']}\")

    st.divider()

# ==================== 批量操作 ====================
if st.session_state.selected_items:
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.write(f\"✅ 已选择 {len(st.session_state.selected_items)} 项\")

    with col2:
        if st.button(\"🗑️ 批量删除\", use_container_width=True):
            st.warning(\"确认删除选中项？\")

    with col3:
        if st.button(\"❌ 取消选择\", use_container_width=True):
            st.session_state.selected_items = []
            st.rerun()

# ==================== 分页导航 ====================
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])

with col1:
    if st.button(\"◀ 上一页\") and current_page > 1:
        st.session_state.current_page = current_page - 1
        st.rerun()

with col5:
    if st.button(\"下一页 ▶\") and current_page < total_pages:
        st.session_state.current_page = current_page + 1
        st.rerun()

# ==================== 使用 Streamlit DataFrame（备选） ====================
# df = pd.DataFrame(data)
# st.dataframe(
#     df,
#     column_config={
#         \"name\": \"姓名\",
#         \"email\": \"邮箱\",
#         \"status\": st.column_config.SelectboxColumn(\"状态\", options=[\"激活\", \"禁用\"]),
#         \"role\": \"角色\"
#     },
#     hide_index=True,
#     use_container_width=True,
#     on_select=\"rerun\",
#     selection_mode=\"multi-row\"
# )
""",
    props=[
        ComponentProp("title", "str", "用户列表", True, "列表标题"),
        ComponentProp("show_checkbox", "bool", True, False, "显示复选框"),
        ComponentProp("show_actions", "bool", True, False, "显示操作按钮"),
        ComponentProp("page_size", "int", 10, False, "每页条数"),
        ComponentProp("enable_sort", "bool", True, False, "启用排序"),
    ],
    tags=["列表", "数据", "表格", "展示"],
    dependencies=["streamlit", "pandas"],
    industry_compatibility=["general", "ecommerce", "finance", "healthcare"],
)


# ============================================================================
# 5. NavSidebar - 导航侧边栏
# ============================================================================

NAV_SIDEBAR = MediumComponent(
    id="nav_sidebar",
    name="导航侧边栏",
    category=MediumComponentCategory.NAVIGATION,
    description="""
    可折叠的导航侧边栏，支持多级菜单和图标。
    适用于后台管理、控制面板、应用主界面等场景。
    """,
    preview="""
    ┌───────────────────┐
    │  🏠 首页          │
    │  ─────────────────│
    │  📊 数据中心       │
    │    ├─ 📈 概览      │
    │    ├─ 📋 报告      │
    │    └─ ⚙️ 设置      │
    │  ─────────────────│
    │  👥 用户管理       │
    │  ─────────────────│
    │  💬 消息中心  (3)  │
    │  ─────────────────│
    │  ⚙️ 系统设置       │
    │  ─────────────────│
    │  [◀ 折叠]         │
    └───────────────────┘
    """,
    features=[
        "📁 多级菜单 - 支持无限层级嵌套",
        "🎯 激活状态 - 高亮当前页面",
        "🔢 徽章计数 - 未读消息数量",
        "📱 响应式 - 自适应移动端",
        "🔍 搜索菜单 - 快速查找菜单项",
        "⭐ 收藏夹 - 常用菜单收藏",
        "🏷️ 标签页 - 最近访问记录",
        "🎨 主题切换 - 明暗模式切换",
        "🔒 权限控制 - 根据角色显示",
        "◀️▶️ 折叠展开 - 节省屏幕空间",
    ],
    code_skeleton="""
import streamlit as st

# ==================== 配置区 ====================
LOGO = \"{{logo}}\"  # Logo 文字或图标
SHOW_COLLAPSE = {{show_collapse}}  # 显示折叠按钮
DEFAULT_EXPANDED = {{default_expanded}}  # 默认展开

# ==================== 菜单定义 ====================
MENU_ITEMS = [
    {
        \"id\": \"home\",
        \"icon\": \"🏠\",
        \"label\": \"首页\",
        \"page\": \"home\"
    },
    {
        \"id\": \"data\",
        \"icon\": \"📊\",
        \"label\": \"数据中心\",
        \"children\": [
            {\"id\": \"overview\", \"icon\": \"📈\", \"label\": \"概览\", \"page\": \"overview\"},
            {\"id\": \"reports\", \"icon\": \"📋\", \"label\": \"报告\", \"page\": \"reports\"},
            {\"id\": \"settings\", \"icon\": \"⚙️\", \"label\": \"设置\", \"page\": \"data_settings\"}
        ]
    },
    {
        \"id\": \"users\",
        \"icon\": \"👥\",
        \"label\": \"用户管理\",
        \"page\": \"users\"
    },
    {
        \"id\": \"messages\",
        \"icon\": \"💬\",
        \"label\": \"消息中心\",
        \"badge\": \"3\",
        \"page\": \"messages\"
    },
    {
        \"id\": \"settings\",
        \"icon\": \"⚙️\",
        \"label\": \"系统设置\",
        \"children\": [
            {\"id\": \"profile\", \"icon\": \"👤\", \"label\": \"个人资料\", \"page\": \"profile\"},
            {\"id\": \"security\", \"icon\": \"🔒\", \"label\": \"安全设置\", \"page\": \"security\"},
            {\"id\": \"notifications\", \"icon\": \"🔔\", \"label\": \"通知设置\", \"page\": \"notifications\"}
        ]
    }
]

# ==================== 初始化状态 ====================
if \"sidebar_expanded\" not in st.session_state:
    st.session_state.sidebar_expanded = DEFAULT_EXPANDED

if \"current_page\" not in st.session_state:
    st.session_state.current_page = \"home\"

# ==================== Logo 区域 ====================
st.markdown(f\"\"\"
<div style='text-align: center; padding: 1.5rem 0; border-bottom: 1px solid #e9ecef;'>
    <h2 style='margin: 0; color: #007bff;'>{LOGO}</h2>
</div>
\"\"\", unsafe_allow_html=True)

st.divider()

# ==================== 渲染菜单 ====================
def render_menu_item(item, level=0):
    \"\"\"渲染菜单项\"\"\"
    indent = \"&nbsp;\" * (level * 4)

    # 有子菜单
    if \"children\" in item:
        with st.expander(f\"{indent}{item['icon']} {item['label']}\", expanded=False):
            for child in item['children']:
                render_menu_item(child, level + 1)
    # 普通菜单项
    else:
        label = item['label']
        if item.get('badge'):
            label += f\" <span style='background: #dc3545; color: white; padding: 0.1rem 0.4rem; border-radius: 10px; font-size: 0.8rem;'>{item['badge']}</span>\"

        is_active = st.session_state.current_page == item.get('page')
        active_style = \"background: #007bff; color: white;\" if is_active else \"\"

        st.markdown(f\"\"\"
<div style='padding: 0.5rem 1rem; border-radius: 4px; {active_style} cursor: pointer; margin-bottom: 0.25rem;'>
    {indent}{item['icon']} {label}
</div>
\"\"\", unsafe_allow_html=True)

        if st.button(f\"{label}\", key=f\"nav_{item['id']}\"):
            st.session_state.current_page = item.get('page', item['id'])
            st.rerun()

# 渲染所有菜单
for item in MENU_ITEMS:
    render_menu_item(item)
    st.divider()

# ==================== 底部操作 ====================
st.divider()

col1, col2 = st.columns(2)

with col1:
    if SHOW_COLLAPSE:
        if st.button(\"◀️ 折叠\", use_container_width=True):
            st.session_state.sidebar_expanded = False
            st.rerun()

with col2:
    if st.button(\"🌙 主题\", use_container_width=True):
        st.info(\"切换主题\")

# ==================== 用户信息 ====================
st.divider()

with st.container():
    st.markdown(\"\"\"
<div style='display: flex; align-items: center; padding: 0.5rem; background: #f8f9fa; border-radius: 8px;'>
    <div style='font-size: 2rem; margin-right: 0.5rem;'>👤</div>
    <div>
        <div style='font-weight: bold;'>张三</div>
        <div style='font-size: 0.8rem; color: #666;'>管理员</div>
    </div>
</div>
\"\"\", unsafe_allow_html=True)

# ==================== 使用 Streamlit 原生侧边栏 ====================
# with st.sidebar:
#     st.title(LOGO)
#     st.divider()
#     for item in MENU_ITEMS:
#         if \"children\" in item:
#             with st.expander(item['icon'] + \" \" + item['label']):
#                 for child in item['children']:
#                     st.page_link(child['page'], label=child['icon'] + \" \" + child['label'])
#         else:
#             st.page_link(item['page'], label=item['icon'] + \" \" + item['label'])
""",
    props=[
        ComponentProp("logo", "str", "🏢 系统", False, "Logo 文字"),
        ComponentProp("show_collapse", "bool", True, False, "显示折叠按钮"),
        ComponentProp("default_expanded", "bool", True, False, "默认展开"),
        ComponentProp("enable_search", "bool", True, False, "启用菜单搜索"),
        ComponentProp("show_user", "bool", True, False, "显示用户信息"),
    ],
    tags=["导航", "侧边栏", "菜单", "布局"],
    dependencies=["streamlit"],
    industry_compatibility=["general"],
)


# ============================================================================
# 6. HeaderBar - 顶部导航栏
# ============================================================================

HEADER_BAR = MediumComponent(
    id="header_bar",
    name="顶部导航栏",
    category=MediumComponentCategory.NAVIGATION,
    description="""
    固定顶部导航栏，包含 Logo、主菜单、用户信息。
    适用于网站、应用、管理系统等场景。
    """,
    preview="""
    ┌───────────────────────────────────────────────────────┐
    │  🏢 品牌    首页  产品  关于  联系     [搜索🔍] [🔔]│
    │                          [👤张三 ▼]  [菜单≡]         │
    └───────────────────────────────────────────────────────┘
    """,
    features=[
        "🏢 Logo 展示 - 品牌 Logo 和名称",
        "📍 主导航 - 一级水平菜单",
        "🔍 搜索框 - 全站搜索功能",
        "🔔 通知铃铛 - 消息提醒",
        "👤 用户菜单 - 下拉用户菜单",
        "🌙 主题切换 - 明暗模式切换",
        "📱 移动端菜单 - 汉堡菜单",
        "🎨 固定顶部 - 滚动时固定",
        "🔗 面包屑 - 当前位置导航",
        "🌐 多语言 - 语言切换器",
    ],
    code_skeleton="""
import streamlit as st

# ==================== 配置区 ====================
BRAND_NAME = \"{{brand_name}}\"  # 品牌名称
LOGO_ICON = \"{{logo_icon}}\"  # Logo 图标
SHOW_SEARCH = {{show_search}}  # 显示搜索框
SHOW_NOTIFICATIONS = {{show_notifications}}  # 显示通知
FIXED_TOP = {{fixed_top}}  # 固定顶部

# ==================== 导航菜单 ====================
NAV_ITEMS = [
    {\"label\": \"首页\", \"page\": \"home\", \"icon\": \"🏠\"},
    {\"label\": \"产品\", \"page\": \"products\", \"icon\": \"📦\"},
    {\"label\": \"关于\", \"page\": \"about\", \"icon\": \"ℹ️\"},
    {\"label\": \"联系\", \"page\": \"contact\", \"icon\": \"📧\"},
]

# ==================== 渲染导航栏 ====================
st.markdown(f\"\"\"
<style>
    .header-fixed {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
</style>

<div style='display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: #f8f9fa; border-bottom: 1px solid #dee2e6;'>
    <!-- Logo -->
    <div style='font-size: 1.5rem; font-weight: bold; color: #007bff;'>
        {LOGO_ICON} {BRAND_NAME}
    </div>

    <!-- 主导航 -->
    <div style='display: flex; gap: 2rem;'>
        {\"\".join([f\"<a href='#{item['page']}' style='text-decoration: none; color: #333; font-weight: 500;'>{item['label']}</a>\" for item in NAV_ITEMS])}
    </div>

    <!-- 右侧操作 -->
    <div style='display: flex; gap: 1rem; align-items: center;'>
\"\"\", unsafe_allow_html=True)

# ==================== 右侧组件 ====================
col1, col2, col3, col4 = st.columns(4)

# 搜索框
if SHOW_SEARCH:
    with col1:
        search = st.text_input(\"🔍\", placeholder=\"搜索...\", label_visibility=\"collapsed\")
        if search:
            st.info(f\"搜索: {search}\")

# 通知铃铛
if SHOW_NOTIFICATIONS:
    with col2:
        if st.button(\"🔔\"):
            with st.expander(\"通知\", expanded=True):
                st.info(\"📬 您有 3 条新消息\")
                st.success(\"✅ 任务已完成\")
                st.warning(\"⚠️ 系统将于今晚维护\")

# 用户菜单
with col3:
    user_menu = st.selectbox(
        \"👤\",
        [\"张三\", \"个人资料\", \"设置\", \"退出\"],
        label_visibility=\"collapsed\"
    )

# 移动端菜单
with col4:
    if st.button(\"≡ 菜单\"):
        with st.sidebar:
            st.write(\"**移动端菜单**\")
            for item in NAV_ITEMS:
                st.button(f\"{item['icon']} {item['label']}\")

st.markdown(\"</div></div>\", unsafe_allow_html=True)

# ==================== 面包屑导航（可选） ====================
st.divider()

breadcrumb_items = [\"首页\", \"产品\", \"详情\"]
breadcrumb_html = \" | \".join(breadcrumb_items)

st.markdown(f\"\"\"
<div style='padding: 0.5rem 0; color: #666; font-size: 0.9rem;'>
    📍 {breadcrumb_html}
</div>
\"\"\", unsafe_allow_html=True)

# ==================== 使用 Streamlit 原生导航 ====================
# st.title(f\"{LOGO_ICON} {BRAND_NAME}\")
# st.tabs([item['label'] for item in NAV_ITEMS])

# ==================== 多语言切换（可选） ====================
col1, col2, col3 = st.columns(3)

with col3:
    language = st.selectbox(
        \"🌐\",
        [\"简体中文\", \"English\", \"日本語\"],
        label_visibility=\"collapsed\"
    )
""",
    props=[
        ComponentProp("brand_name", "str", "我的应用", True, "品牌名称"),
        ComponentProp("logo_icon", "str", "🏢", False, "Logo 图标"),
        ComponentProp("show_search", "bool", True, False, "显示搜索框"),
        ComponentProp("show_notifications", "bool", True, False, "显示通知铃铛"),
        ComponentProp("fixed_top", "bool", True, False, "固定在顶部"),
        ComponentProp("show_breadcrumb", "bool", True, False, "显示面包屑"),
    ],
    tags=["导航", "头部", "菜单", "布局"],
    dependencies=["streamlit"],
    industry_compatibility=["general"],
)


# ============================================================================
# 7. FooterBar - 页脚
# ============================================================================

FOOTER_BAR = MediumComponent(
    id="footer_bar",
    name="页脚",
    category=MediumComponentCategory.LAYOUT,
    description="""
    页面底部页脚，包含链接、版权、社交媒体。
    适用于网站、应用、文档等场景。
    """,
    preview="""
    ┌───────────────────────────────────────────────────────┐
    │  [关于] [产品] [服务] [博客] [联系我们]              │
    │                                                       │
    │  ┌─────────┬─────────┬─────────┬─────────┐           │
    │  │ 产品    │ 公司    │ 支持    │ 法律    │           │
    │  │ 功能A   │ 关于我们│ 帮助中心│ 隐私政策│           │
    │  │ 功能B   │ 团队    │ FAQ     │ 服务条款│           │
    │  │ 功能C   │ 招聘    │ 联系我们│ Cookie  │           │
    │  └─────────┴─────────┴─────────┴─────────┘           │
    │                                                       │
    │  🐦  📘  📸  💼  📺                                   │
    │                                                       │
    │  © 2024 公司名. 保留所有权利。                         │
    └───────────────────────────────────────────────────────┘
    """,
    features=[
        "🔗 快速链接 - 主要页面链接",
        "📂 分栏链接 - 分类链接组",
        "📧 联系信息 - 邮箱、电话、地址",
        "🐦 社交媒体 - 社交平台图标链接",
        "©️ 版权信息 - 公司名称和年份",
        "🌐 多语言 - 语言切换器",
        "🎨 品牌元素 - Logo 和标语",
        "📱 订阅功能 - 邮件订阅表单",
        "🔐 安全标识 - SSL、认证等",
        "📍 地址信息 - 公司地址",
    ],
    code_skeleton="""
import streamlit as st

# ==================== 配置区 ====================
COMPANY_NAME = \"{{company_name}}\"  # 公司名称
YEAR = {{year}}  # 版权年份
SHOW_SOCIAL = {{show_social}}  # 显示社交媒体
SHOW_NEWSLETTER = {{show_newsletter}}  # 显示邮件订阅
LINK_COLUMNS = {{link_columns}}  # 链接列配置

# ==================== 链接配置 ====================
FOOTER_LINKS = {
    \"产品\": [
        {\"label\": \"功能A\", \"url\": \"#product-a\"},
        {\"label\": \"功能B\", \"url\": \"#product-b\"},
        {\"label\": \"功能C\", \"url\": \"#product-c\"},
    ],
    \"公司\": [
        {\"label\": \"关于我们\", \"url\": \"#about\"},
        {\"label\": \"团队\", \"url\": \"#team\"},
        {\"label\": \"招聘\", \"url\": \"#careers\"},
    ],
    \"支持\": [
        {\"label\": \"帮助中心\", \"url\": \"#help\"},
        {\"label\": \"FAQ\", \"url\": \"#faq\"},
        {\"label\": \"联系我们\", \"url\": \"#contact\"},
    ],
    \"法律\": [
        {\"label\": \"隐私政策\", \"url\": \"#privacy\"},
        {\"label\": \"服务条款\", \"url\": \"#terms\"},
        {\"label\": \"Cookie\", \"url\": \"#cookies\"},
    ]
}

# ==================== 主链接 ====================
st.divider()

col1, col2, col3, col4, col5 = st.columns(5)

quick_links = [\"首页\", \"产品\", \"服务\", \"博客\", \"联系我们\"]

with col1:
    for link in quick_links:
        st.markdown(f\"[**{link}**](#{link.lower().replace(' ', '-')})\")

with col2:
    st.write(\"\")

# ==================== 分栏链接 ====================
st.divider()

# 计算列数
num_columns = len(FOOTER_LINKS)
cols = st.columns(num_columns)

for col, (category, links) in zip(cols, FOOTER_LINKS.items()):
    with col:
        st.markdown(f\"**{category}**\")
        for link in links:
            st.markdown(f\"[{link['label']}]({link['url']})\")

# ==================== 社交媒体 ====================
st.divider()

if SHOW_SOCIAL:
    st.markdown(\"**关注我们**\")

    social_links = [
        (\"🐦\", \"Twitter\", \"https://twitter.com\"),
        (\"📘\", \"Facebook\", \"https://facebook.com\"),
        (\"📸\", \"Instagram\", \"https://instagram.com\"),
        (\"💼\", \"LinkedIn\", \"https://linkedin.com\"),
        (\"📺\", \"YouTube\", \"https://youtube.com\"),
    ]

    cols = st.columns(len(social_links))
    for col, (icon, name, url) in zip(cols, social_links):
        with col:
            st.markdown(f\"[{icon}]({url})\")

# ==================== 邮件订阅 ====================
st.divider()

if SHOW_NEWSLETTER:
    col1, col2, col3 = st.columns([3, 2, 1])

    with col1:
        email = st.text_input(\"订阅我们的新闻\", placeholder=\"输入您的邮箱\")

    with col2:
        if st.button(\"订阅\", use_container_width=True):
            if email:
                st.success(f\"✅ 已发送确认邮件到 {email}\")

    with col3:
        st.write(\"\")

# ==================== 版权信息 ====================
st.divider()

st.markdown(f\"\"\"
<div style='text-align: center; color: #666; padding: 1rem 0;'>
    <p style='margin: 0;'>© {YEAR} {COMPANY_NAME}. 保留所有权利。</p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
        Made with ❤️ using Streamlit
    </p>
</div>
\"\"\", unsafe_allow_html=True)

# ==================== 备案信息（可选） ====================
st.caption(\"\"\" 京ICP备12345678号-1 | 京公网安备 11010802012345号 \"\"\")

# ==================== 安全标识 ====================
col1, col2, col3 = st.columns(3)

with col1:
    st.caption(\"🔒 SSL 安全连接\")

with col2:
    st.caption(\"✓ 已通过安全认证\")

with col3:
    st.caption(\"🛡️ 隐私保护\")
""",
    props=[
        ComponentProp("company_name", "str", "公司名称", True, "公司名称"),
        ComponentProp("year", "int", 2024, False, "版权年份"),
        ComponentProp("show_social", "bool", True, False, "显示社交媒体"),
        ComponentProp("show_newsletter", "bool", True, False, "显示邮件订阅"),
        ComponentProp("link_columns", "dict", None, False, "链接列配置"),
        ComponentProp("show_icp", "bool", True, False, "显示备案信息"),
    ],
    tags=["页脚", "底部", "布局", "版权"],
    dependencies=["streamlit"],
    industry_compatibility=["general"],
)


# ============================================================================
# 8. AlertPanel - 通知面板
# ============================================================================

ALERT_PANEL = MediumComponent(
    id="alert_panel",
    name="通知面板",
    category=MediumComponentCategory.FEEDBACK,
    description="""
    多状态通知面板，支持成功、警告、错误、信息提示。
    适用于系统通知、操作反馈、状态提示等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────┐
    │  ✅ 成功！操作已完成。                  [×] │
    ├─────────────────────────────────────────────┤
    │  ⚠️ 警告：请注意检查输入内容。          [×] │
    ├─────────────────────────────────────────────┤
    │  ❌ 错误：操作失败，请重试。            [×] │
    ├─────────────────────────────────────────────┤
    │  ℹ️ 信息：系统将于今晚进行维护。        [×] │
    └─────────────────────────────────────────────┘
    """,
    features=[
        "✅ 成功提示 - 绿色成功消息",
        "⚠️ 警告提示 - 黄色警告消息",
        "❌ 错误提示 - 红色错误消息",
        "ℹ️ 信息提示 - 蓝色信息消息",
        "❌ 关闭按钮 - 可关闭通知",
        "⏱️ 自动关闭 - 定时自动消失",
        "🔔 声音提示 - 通知声音",
        "📍 固定位置 - 顶部/底部/角落",
        "🎨 图标支持 - 自定义图标",
        "📊 进度条 - 操作进度显示",
    ],
    code_skeleton="""
import streamlit as st
import time

# ==================== 配置区 ====================
AUTO_CLOSE = {{auto_close}}  # 自动关闭
CLOSE_TIMEOUT = {{close_timeout}}  # 关闭超时（秒）
SHOW_ICON = {{show_icon}}  # 显示图标

# ==================== 通知状态枚举 ====================
class AlertType:
    SUCCESS = \"success\"
    WARNING = \"warning\"
    ERROR = \"error\"
    INFO = \"info\"

# ==================== 样式配置 ====================
ALERT_STYLES = {
    AlertType.SUCCESS: {
        \"icon\": \"✅\",
        \"color\": \"#155724\",
        \"bg\": \"#d4edda\",
        \"border\": \"#c3e6cb\"
    },
    AlertType.WARNING: {
        \"icon\": \"⚠️\",
        \"color\": \"#856404\",
        \"bg\": \"#fff3cd\",
        \"border\": \"#ffeeba\"
    },
    AlertType.ERROR: {
        \"icon\": \"❌\",
        \"color\": \"#721c24\",
        \"bg\": \"#f8d7da\",
        \"border\": \"#f5c6cb\"
    },
    AlertType.INFO: {
        \"icon\": \"ℹ️\",
        \"color\": \"#0c5460\",
        \"bg\": \"#d1ecf1\",
        \"border\": \"#bee5eb\"
    }
}

# ==================== 通知函数 ====================
def show_alert(message: str, alert_type: str = AlertType.INFO, show_close: bool = True):
    \"\"\"显示通知消息\"\"\"
    style = ALERT_STYLES.get(alert_type, ALERT_STYLES[AlertType.INFO])

    icon_html = style['icon'] if SHOW_ICON else \"\"
    close_html = \" [×]\" if show_close else \"\"

    st.markdown(f\"\"\"
<div style='background: {style['bg']}; color: {style['color']}; padding: 1rem; border-radius: 4px; border-left: 4px solid {style['border']}; margin-bottom: 1rem;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div style='display: flex; align-items: center; gap: 0.5rem;'>
            <span style='font-size: 1.2rem;'>{icon_html}</span>
            <span>{message}</span>
        </div>
        <span style='cursor: pointer; opacity: 0.7;'>{close_html}</span>
    </div>
</div>
\"\"\", unsafe_allow_html=True)

# ==================== 演示各种通知 ====================
st.subheader(\"📢 通知面板示例\")

# 成功通知
col1, col2 = st.columns(2)
with col1:
    if st.button(\"✅ 显示成功\", use_container_width=True):
        show_alert(\"操作已成功完成！\", AlertType.SUCCESS)

# 警告通知
with col2:
    if st.button(\"⚠️ 显示警告\", use_container_width=True):
        show_alert(\"请注意检查输入内容！\", AlertType.WARNING)

# 错误通知
col1, col2 = st.columns(2)
with col1:
    if st.button(\"❌ 显示错误\", use_container_width=True):
        show_alert(\"操作失败，请稍后重试！\", AlertType.ERROR)

# 信息通知
with col2:
    if st.button(\"ℹ️ 显示信息\", use_container_width=True):
        show_alert(\"系统将于今晚 22:00 进行维护！\", AlertType.INFO)

# ==================== 带操作按钮的通知 ====================
st.divider()

with st.success(\"✅ 数据已成功保存！\"):
    st.write(\"您的更改已生效。\")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(\"查看详情\", use_container_width=True):
            st.info(\"跳转到详情页\")
    with col2:
        if st.button(\"撤销\", use_container_width=True):
            st.warning(\"已撤销操作\")

# ==================== 自动关闭演示 ====================
st.divider()

if AUTO_CLOSE:
    placeholder = st.empty()

    with placeholder.container():
        show_alert(\"此消息将在 3 秒后自动消失...\", AlertType.INFO, show_close=False)

    time.sleep(CLOSE_TIMEOUT)
    placeholder.empty()

# ==================== 使用 Streamlit 原生通知 ====================
# st.success(\"✅ 这是成功消息\")
# st.warning(\"⚠️ 这是警告消息\")
# st.error(\"❌ 这是错误消息\")
# st.info(\"ℹ️ 这是信息消息\")

# ==================== 进度通知 ====================
st.divider()

with st.container():
    st.balloons()
    st.success(\"🎉 恭喜！任务已全部完成！\")

    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)

    st.success(\"✅ 进度条加载完成！\")
""",
    props=[
        ComponentProp("auto_close", "bool", True, False, "自动关闭"),
        ComponentProp("close_timeout", "int", 5, False, "关闭超时（秒）"),
        ComponentProp("show_icon", "bool", True, False, "显示图标"),
        ComponentProp("position", "str", "top", False, "显示位置"),
        ComponentProp("stackable", "bool", True, False, "可堆叠"),
    ],
    tags=["通知", "提示", "反馈", "消息"],
    dependencies=["streamlit"],
    industry_compatibility=["general"],
)


# ============================================================================
# 9. UploadZone - 上传区域
# ============================================================================

UPLOAD_ZONE = MediumComponent(
    id="upload_zone",
    name="上传区域",
    category=MediumComponentCategory.INPUT,
    description="""
    拖拽式文件上传组件，支持预览和进度显示。
    适用于头像上传、文件导入、图片管理等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────┐
    │  📁 文件上传区                              │
    │                                             │
    │          ┌─────────────────┐               │
    │          │                 │               │
    │          │  📎 拖拽文件到   │               │
    │          │     此区域      │               │
    │          │                 │               │
    │          │   或点击选择    │               │
    │          │                 │               │
    │          └─────────────────┘               │
    │                                             │
    │  支持格式: JPG, PNG, PDF  最大: 10MB      │
    └─────────────────────────────────────────────┘
    """,
    features=[
        "📎 拖拽上传 - 拖拽文件到区域",
        "👆 点击上传 - 点击选择文件",
        "👀 预览功能 - 图片/文件预览",
        "📊 进度条 - 上传进度显示",
        "📋 文件列表 - 已上传文件列表",
        "❌ 删除功能 - 删除已上传文件",
        "📏 大小限制 - 文件大小限制",
        "🎨 格式限制 - 允许的文件格式",
        "📷 裁剪功能 - 图片裁剪编辑",
        "☁️ 云存储 - 直接上传到云",
    ],
    code_skeleton="""
import streamlit as st
from typing import List

# ==================== 配置区 ====================
ALLOWED_TYPES = {{allowed_types}}  # 允许的文件类型
MAX_SIZE_MB = {{max_size_mb}}  # 最大文件大小（MB）
MULTIPLE = {{multiple}}  # 允许多文件
SHOW_PREVIEW = {{show_preview}}  # 显示预览

# ==================== 初始化状态 ====================
if \"uploaded_files\" not in st.session_state:
    st.session_state.uploaded_files = []

# ==================== 上传区域 ====================
st.subheader(\"📁 文件上传\")

# 上传配置
upload_config = {
    \"jpg\": \"图片\",
    \"jpeg\": \"图片\",
    \"png\": \"图片\",
    \"gif\": \"图片\",
    \"pdf\": \"文档\",
    \"doc\": \"文档\",
    \"docx\": \"文档\",
    \"txt\": \"文本\",
    \"csv\": \"数据\",
    \"xlsx\": \"数据\"
}

allowed_types_str = \", \".join([f\".{ext}\" for ext in ALLOWED_TYPES]) if ALLOWED_TYPES else \"所有格式\"

# 拖拽区域样式
st.markdown(f\"\"\"
<style>
    .upload-zone {{
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 3rem 1rem;
        text-align: center;
        background: #f8f9fa;
        transition: all 0.3s;
    }}
    .upload-zone:hover {{
        border-color: #007bff;
        background: #e9ecef;
    }}
</style>

<div class='upload-zone'>
    <div style='font-size: 3rem; margin-bottom: 1rem;'>📎</div>
    <div style='font-size: 1.1rem; margin-bottom: 0.5rem;'><strong>拖拽文件到此处</strong></div>
    <div style='color: #666; margin-bottom: 1rem;'>或点击下方按钮选择</div>
    <div style='font-size: 0.9rem; color: #999;'>
        支持格式: {allowed_types_str}<br>
        最大大小: {MAX_SIZE_MB} MB
    </div>
</div>
\"\"\", unsafe_allow_html=True)

# ==================== 文件上传 ====================
uploaded_files = st.file_uploader(
    \"选择文件\",
    type=ALLOWED_TYPES if ALLOWED_TYPES else None,
    accept_multiple_files=MULTIPLE,
    help=f\"支持 {allowed_types_str} 格式，最大 {MAX_SIZE_MB} MB\"
)

# ==================== 文件预览 ====================
if uploaded_files:
    st.divider()
    st.subheader(\"✅ 已选择的文件\")

    for i, file in enumerate(uploaded_files):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            # 显示文件信息
            file_size_mb = len(file.getvalue()) / (1024 * 1024)
            file_info = f\"📄 {file.name} ({file_size_mb:.2f} MB)\"

            # 图片预览
            if SHOW_PREVIEW and file.type in [\"image/jpeg\", \"image/png\", \"image/gif\"]:
                st.image(file, width=200)
                st.write(file_info)
            else:
                st.write(file_info)

        with col2:
            # 文件大小检查
            if file_size_mb > MAX_SIZE_MB:
                st.error(f\"超过 {MAX_SIZE_MB} MB\")
            else:
                st.success(\"✓ 符合要求\")
        with col3:
            # 删除按钮
            if st.button(\"🗑️ 删除\", key=f\"delete_{i}\"):
                st.session_state.uploaded_files.pop(i)
                st.rerun()

    st.divider()

    # 上传按钮
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button(\"☁️ 开始上传\", type=\"primary\", use_container_width=True):
            # 显示进度
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f\"上传中... {i + 1}%\")

            status_text.empty()
            progress_bar.empty()

            st.success(f\"✅ 成功上传 {len(uploaded_files)} 个文件！\")

            # 保存到会话状态
            for file in uploaded_files:
                st.session_state.uploaded_files.append({
                    \"name\": file.name,
                    \"size\": len(file.getvalue()),
                    \"type\": file.type
                })

    with col2:
        if st.button(\"❌ 清空全部\", use_container_width=True):
            st.session_state.uploaded_files = []
            st.rerun()

    with col3:
        st.write(\"\")

# ==================== 已上传文件列表 ====================
if st.session_state.uploaded_files:
    st.divider()
    st.write(\"**已上传的文件:**\")

    for file in st.session_state.uploaded_files:
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f\"📄 {file['name']}\")

        with col2:
            size_mb = file['size'] / (1024 * 1024)
            st.caption(f\"{size_mb:.2f} MB\")

        with col3:
            if st.button(\"🗑️\", key=f\"remove_{file['name']}\"):
                st.session_state.uploaded_files.remove(file)
                st.rerun()

# ==================== 使用 Streamlit 原生上传（备选） ====================
# st.file_uploader(\"上传文件\", type=['png', 'jpg'])
# st.camera_input(\"拍照上传\")
# st.audio_uploader(\"上传音频\")
""",
    props=[
        ComponentProp("allowed_types", "list", ["jpg", "png", "pdf"], False, "允许的文件类型"),
        ComponentProp("max_size_mb", "int", 10, False, "最大文件大小（MB）"),
        ComponentProp("multiple", "bool", True, False, "允许多文件上传"),
        ComponentProp("show_preview", "bool", True, False, "显示文件预览"),
        ComponentProp("enable_crop", "bool", False, False, "启用图片裁剪"),
    ],
    tags=["上传", "文件", "图片", "输入"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "ecommerce", "healthcare", "education"],
)


# ============================================================================
# 10. CommentSection - 评论区块
# ============================================================================

COMMENT_SECTION = MediumComponent(
    id="comment_section",
    name="评论区块",
    category=MediumComponentCategory.CONTENT,
    description="""
    嵌套评论组件，支持回复、点赞、排序。
    适用于文章评论、产品评价、讨论区等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────┐
    │  💬 评论 (12)                               │
    ├─────────────────────────────────────────────┤
    │  👤 张三        2024-01-15 14:30  [👍 5]    │
    │  这是一篇很好的文章，学到了很多！          │
    │                                             │
    │    💬 回复 (2)                               │
    │    ┌──────────────────────────────────────┐ │
    │    │ 👤 李四    2024-01-15 15:00  [👍 2]  │ │
    │    │ 同意！总结得很到位。                 │ │
    │    └──────────────────────────────────────┘ │
    │                                             │
    │    [回复...]                                │
    ├─────────────────────────────────────────────┤
    │  👤 王五        2024-01-15 16:00  [👍 3]    │
    │  能否详细解释一下第二点？                  │
    ├─────────────────────────────────────────────┤
    │  ┌─────────────────────────────────────────┐│
    │  │ ✍️ 添加评论...                         ││
    │  └─────────────────────────────────────────┘│
    │                                             │
    │  [📝 发表评论]        [最新 ▼]            │
    └─────────────────────────────────────────────┘
    """,
    features=[
        "💬 多级嵌套 - 支持多级回复",
        "👍 点赞功能 - 评论点赞/踩",
        "📅 时间显示 - 相对时间/绝对时间",
        "🔍 搜索评论 - 关键词搜索",
        "📊 排序方式 - 最新/热门/最早",
        "✏️ 编辑评论 - 编辑/删除自己的评论",
        "👤 用户头像 - 显示用户信息",
        "📊 分页加载 - 懒加载评论",
        "🔔 回复通知 - 回复时通知",
        "🎯 表情支持 - 评论表情包",
    ],
    code_skeleton="""
import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict

# ==================== 配置区 ====================
SHOW_AVATAR = {{show_avatar}}  # 显示头像
ENABLE_NESTING = {{enable_nesting}}  # 启用嵌套
MAX_NESTING = {{max_nesting}}  # 最大嵌套层级
ALLOW_EDIT = {{allow_edit}}  # 允许编辑

# ==================== 模拟评论数据 ====================
COMMENTS = [
    {
        \"id\": 1,
        \"user\": \"张三\",
        \"avatar\": \"👨‍💼\",
        \"content\": \"这是一篇很好的文章，学到了很多！\",
        \"time\": datetime.now() - timedelta(hours=2),
        \"likes\": 5,
        \"replies\": [
            {
                \"id\": 11,
                \"user\": \"李四\",
                \"avatar\": \"👩‍💻\",
                \"content\": \"同意！总结得很到位。\",
                \"time\": datetime.now() - timedelta(hours=1),
                \"likes\": 2
            },
            {
                \"id\": 12,
                \"user\": \"王五\",
                \"avatar\": \"👨‍🎓\",
                \"content\": \"确实很有帮助！\",
                \"time\": datetime.now() - timedelta(minutes=30),
                \"likes\": 1
            }
        ]
    },
    {
        \"id\": 2,
        \"user\": \"赵六\",
        \"avatar\": \"👩‍🔬\",
        \"content\": \"能否详细解释一下第二点？\",
        \"time\": datetime.now() - timedelta(hours=3),
        \"likes\": 3,
        \"replies\": []
    }
]

# ==================== 辅助函数 ====================
def format_time(dt: datetime) -> str:
    \"\"\"格式化时间\"\"\"
    now = datetime.now()
    diff = now - dt

    if diff < timedelta(minutes=1):
        return \"刚刚\"
    elif diff < timedelta(hours=1):
        return f\"{diff.seconds // 60}分钟前\"
    elif diff < timedelta(days=1):
        return f\"{diff.seconds // 3600}小时前\"
    elif diff < timedelta(days=7):
        return f\"{diff.days}天前\"
    else:
        return dt.strftime(\"%Y-%m-%d\")

def render_comment(comment: Dict, level: int = 0):
    \"\"\"渲染单条评论\"\"\"
    indent = \"&nbsp;\" * (level * 4)

    # 评论内容
    with st.container():
        avatar_html = comment['avatar'] if SHOW_AVATAR else \"\"
        time_str = format_time(comment['time'])

        st.markdown(f\"\"\"
<div style='padding: 1rem; border-left: 3px solid #dee2e6; margin-bottom: 0.5rem; background: #f8f9fa; border-radius: 4px;'>
    <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
        <span style='font-size: 1.5rem;'>{avatar_html}</span>
        <span style='font-weight: bold;'>{comment['user']}</span>
        <span style='color: #999; font-size: 0.85rem;'>{time_str}</span>
        <span style='margin-left: auto;'>👍 {comment['likes']}</span>
    </div>
    <div style='margin-left: 2rem;'>{comment['content']}</div>
</div>
\"\"\", unsafe_allow_html=True)

        # 操作按钮
        col1, col2, col3, col4 = st.columns([1, 1, 1, 4])

        with col1:
            if st.button(\"👍 赞\", key=f\"like_{comment['id']}\"):
                st.success(f\"已点赞！\")

        with col2:
            if ENABLE_NESTING and level < MAX_NESTING:
                if st.button(\"💬 回复\", key=f\"reply_{comment['id']}\"):
                    st.session_state[f\"replying_{comment['id']}\"] = True

        with col3:
            if ALLOW_EDIT and comment['user'] == \"当前用户\":
                if st.button(\"✏️ 编辑\", key=f\"edit_{comment['id']}\"):
                    st.info(\"编辑评论\")

        # 回复框
        if ENABLE_NESTING and st.session_state.get(f\"replying_{comment['id']}\"):
            with st.container():
                reply_text = st.text_area(
                    f\"回复 {comment['user']}:\",
                    key=f\"reply_input_{comment['id']}\",
                    placeholder=\"输入回复内容...\",
                    height=80
                )
                if st.button(\"发送回复\", key=f\"send_reply_{comment['id']}\"):
                    if reply_text:
                        st.success(f\"✅ 回复已发送！\")
                        st.session_state[f\"replying_{comment['id']}\"] = False
                        st.rerun()
                if st.button(\"取消\", key=f\"cancel_reply_{comment['id']}\"):
                    st.session_state[f\"replying_{comment['id']}\"] = False
                    st.rerun()

        # 渲染子评论
        if ENABLE_NESTING and comment.get('replies'):
            for reply in comment['replies']:
                render_comment(reply, level + 1)

# ==================== 主评论区块 ====================
st.subheader(\"💬 评论\")

# 排序方式
col1, col2 = st.columns([4, 1])

with col1:
    sort_by = st.selectbox(
        \"排序方式\",
        [\"最新\", \"热门\", \"最早\"],
        label_visibility=\"collapsed\"
    )

with col2:
    total_comments = sum(1 + len(c.get('replies', [])) for c in COMMENTS)
    st.metric(\"总数\", total_comments)

st.divider()

# 渲染评论
for comment in COMMENTS:
    render_comment(comment)

# ==================== 添加评论表单 ====================
st.divider()

with st.expander(\"✍️ 添加评论\", expanded=False):
    col1, col2 = st.columns([3, 1])

    with col1:
        new_comment = st.text_area(
            \"评论内容\",
            placeholder=\"分享你的想法...\",
            height=100
        )

    with col2:
        st.write(\"\")
        st.write(\"\")
        if st.button(\"📝 发表评论\", use_container_width=True, type=\"primary\"):
            if new_comment:
                st.success(\"✅ 评论已发表！\")
            else:
                st.warning(\"请输入评论内容\")

# ==================== 评论统计 ====================
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(\"总评论数\", total_comments, \"+5\")

with col2:
    total_likes = sum(c['likes'] for c in COMMENTS)
    st.metric(\"总点赞数\", total_likes)

with col3:
    avg_rating = 4.5
    st.metric(\"平均评分\", f\"{avg_rating} ⭐\")
""",
    props=[
        ComponentProp("show_avatar", "bool", True, False, "显示用户头像"),
        ComponentProp("enable_nesting", "bool", True, False, "启用嵌套回复"),
        ComponentProp("max_nesting", "int", 3, False, "最大嵌套层级"),
        ComponentProp("allow_edit", "bool", True, False, "允许编辑评论"),
        ComponentProp("enable_emoji", "bool", True, False, "启用表情回复"),
    ],
    tags=["评论", "讨论", "社交", "内容"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "ecommerce", "education", "media"],
)


# ============================================================================
# 11. TimelineBlock - 时间线
# ============================================================================

TIMELINE_BLOCK = MediumComponent(
    id="timeline_block",
    name="时间线",
    category=MediumComponentCategory.CONTENT,
    description="""
    垂直时间线组件，展示步骤进度或历史事件。
    适用于项目进度、历史记录、路线图等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────┐
    │  📅 项目时间线                             │
    ├─────────────────────────────────────────────┤
    │  ●─────────────────────────────────────    │
    │  │  2024-01-15                             │
    │  │  ✅ 项目启动                            │
    │  │  完成需求分析和团队组建                 │
    │  │                                         │
    │  ●─────────────────────────────────────    │
    │  │  2024-02-01                             │
    │  │  🚀 开发阶段                            │
    │  │  完成核心功能开发                       │
    │  │                                         │
    │  ●─────────────────────────────────────    │
    │  │  2024-03-15                             │
    │  │  📦 测试部署                            │
    │  │  进行系统测试和上线                     │
    │  │                                         │
    │  ●─────────────────────────────────────    │
    │  │  2024-04-01                             │
    │  │  🎉 正式发布                            │
    │  │                                         │
    └─────────────────────────────────────────────┘
    """,
    features=[
        "📍 垂直布局 - 时间从上到下",
        "🔵 节点标记 - 完成进行未完成状态",
        "📅 日期显示 - 事件发生时间",
        "📝 详细描述 - 事件详情说明",
        "🎨 颜色编码 - 状态颜色区分",
        "🔗 连接线 - 垂直连接线",
        "📊 进度百分比 - 完成度显示",
        "↔️ 水平模式 - 水平时间线备选",
        "🏷️ 标签系统 - 事件标签",
        "🔍 搜索过滤 - 按时间/类型筛选",
    ],
    code_skeleton="""
import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict

# ==================== 配置区 ====================
ORIENTATION = \"{{orientation}}\"  # 时间线方向
SHOW_DATE = {{show_date}}  # 显示日期
SHOW_DESCRIPTION = {{show_description}}  # 显示描述
SHOW_PROGRESS = {{show_progress}}  # 显示进度

# ==================== 模拟时间线数据 ====================
TIMELINE_EVENTS = [
    {
        \"date\": \"2024-01-15\",
        \"title\": \"✅ 项目启动\",
        \"description\": \"完成需求分析和团队组建\",
        \"status\": \"completed\",
        \"icon\": \"🚀\"
    },
    {
        \"date\": \"2024-02-01\",
        \"title\": \"🔨 开发阶段\",
        \"description\": \"完成核心功能开发和单元测试\",
        \"status\": \"in_progress\",
        \"icon\": \"💻\"
    },
    {
        \"date\": \"2024-03-15\",
        \"title\": \"📋 测试部署\",
        \"description\": \"进行系统集成测试和部署上线\",
        \"status\": \"pending\",
        \"icon\": \"🧪\"
    },
    {
        \"date\": \"2024-04-01\",
        \"title\": \"🎉 正式发布\",
        \"description\": \"产品正式发布并开始运营\",
        \"status\": \"pending\",
        \"icon\": \"🎊\"
    }
]

# ==================== 状态配置 ====================
STATUS_STYLES = {
    \"completed\": {\"color\": \"#28a745\", \"icon\": \"✅\"},
    \"in_progress\": {\"color\": \"#007bff\", \"icon\": \"🔄\"},
    \"pending\": {\"color\": \"#6c757d\", \"icon\": \"⏳\"},
    \"cancelled\": {\"color\": \"#dc3545\", \"icon\": \"❌\"}
}

# ==================== 时间线渲染 ====================
st.subheader(\"📅 项目时间线\")

# 进度条
if SHOW_PROGRESS:
    completed_count = sum(1 for e in TIMELINE_EVENTS if e['status'] == 'completed')
    progress = completed_count / len(TIMELINE_EVENTS)
    st.progress(progress)
    st.caption(f\"完成度: {progress*100:.0f}%\")

st.divider()

# 垂直时间线
for i, event in enumerate(TIMELINE_EVENTS):
    status_style = STATUS_STYLES.get(event['status'], STATUS_STYLES[\"pending\"])

    # 左侧日期和右侧内容
    col1, col2 = st.columns([1, 5])

    with col1:
        if SHOW_DATE:
            st.markdown(f\"<div style='color: #999; font-size: 0.9rem;'>{event['date']}</div>\", unsafe_allow_html=True)

    with col2:
        # 时间线节点
        st.markdown(f\"\"\"
<div style='position: relative; padding-left: 2rem; border-left: 2px solid {status_style['color']}; margin-bottom: 1.5rem;'>
    <div style='position: absolute; left: -0.6rem; top: 0; width: 1.2rem; height: 1.2rem; background: {status_style['color']}; border-radius: 50%; text-align: center; line-height: 1.2rem; color: white; font-size: 0.8rem;'>
        {status_style['icon']}
    </div>
    <div style='margin-bottom: 0.5rem;'>
        <strong style='font-size: 1.1rem;'>{event['title']}</strong>
    </div>
\"\"\", unsafe_allow_html=True)

        if SHOW_DESCRIPTION:
            st.markdown(f\"<div style='color: #666;'>{event['description']}</div>\", unsafe_allow_html=True)

        # 操作按钮（模拟）
        if event['status'] == 'pending':
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f\"开始任务\", key=f\"start_{i}\"):
                    st.info(f\"开始 {event['title']}\")
        elif event['status'] == 'completed':
            st.caption(f\"✅ 已完成\")

        st.markdown(\"</div>\", unsafe_allow_html=True)

# ==================== 水平时间线（备选） ====================
st.divider()
st.write(\"**水平视图（备选）:**\")

cols = st.columns(len(TIMELINE_EVENTS))
for col, event in zip(cols, TIMELINE_EVENTS):
    with col:
        status_style = STATUS_STYLES.get(event['status'], STATUS_STYLES[\"pending\"])

        st.markdown(f\"\"\"
<div style='text-align: center; padding: 1rem; border-top: 3px solid {status_style['color']};'>
    <div style='font-size: 1.5rem;'>{status_style['icon']}</div>
    <div style='font-weight: bold; margin: 0.5rem 0;'>{event['title']}</div>
    <div style='font-size: 0.85rem; color: #999;'>{event['date']}</div>
</div>
\"\"\", unsafe_allow_html=True)

# ==================== 使用 Streamlit Steps（备选） ====================
# st.steps([
#     \"项目启动\",
#     \"开发阶段\",
#     \"测试部署\",
#     \"正式发布\"
# ])

# ==================== 里程碑统计 ====================
st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    completed = sum(1 for e in TIMELINE_EVENTS if e['status'] == 'completed')
    st.metric(\"已完成\", completed)

with col2:
    in_progress = sum(1 for e in TIMELINE_EVENTS if e['status'] == 'in_progress')
    st.metric(\"进行中\", in_progress)

with col3:
    pending = sum(1 for e in TIMELINE_EVENTS if e['status'] == 'pending')
    st.metric(\"待开始\", pending)

with col4:
    if TIMELINE_EVENTS:
        start_date = datetime.strptime(TIMELINE_EVENTS[0]['date'], '%Y-%m-%d')
        end_date = datetime.strptime(TIMELINE_EVENTS[-1]['date'], '%Y-%m-%d')
        total_days = (end_date - start_date).days
        st.metric(\"总天数\", f\"{total_days} 天\")
""",
    props=[
        ComponentProp("orientation", "str", "vertical", False, "时间线方向"),
        ComponentProp("show_date", "bool", True, False, "显示日期"),
        ComponentProp("show_description", "bool", True, False, "显示描述"),
        ComponentProp("show_progress", "bool", True, False, "显示进度条"),
        ComponentProp("status_colors", "dict", None, False, "状态颜色配置"),
    ],
    tags=["时间线", "进度", "历史", "里程碑"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "project_management", "education", "healthcare"],
)


# ============================================================================
# 12. PricingTable - 价格表
# ============================================================================

PRICING_TABLE = MediumComponent(
    id="pricing_table",
    name="价格表",
    category=MediumComponentCategory.COMMERCE,
    description="""
    多方案价格对比表，支持特性列表和推荐标记。
    适用于产品定价、服务套餐、会员等级等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────┐
    │  💰 选择适合您的方案                               │
    ├─────────────────────────────────────────────────────┤
    │  ┌─────────┬─────────┬─────────┬─────────┐        │
    │  │  基础版  │  专业版 │  企业版 │  定制版  │        │
    │  ├─────────┼─────────┼─────────┼─────────┤        │
    │  │  免费   │  ¥99/月 │ ¥299/月 │ 联系销售 │        │
    │  ├─────────┼─────────┼─────────┼─────────┤        │
    │  │ ✓ 功能1 │ ✓ 功能1 │ ✓ 功能1 │ ✓ 全部  │        │
    │  │ ✗ 功能2 │ ✓ 功能2 │ ✓ 功能2 │ ✓ 全部  │        │
    │  │ ✗ 功能3 │ ✗ 功能3 │ ✓ 功能3 │ ✓ 全部  │        │
    │  │ ✗ 功能4 │ ✗ 功能4 │ ✓ 功能4 │ ✓ 全部  │        │
    │  ├─────────┼─────────┼─────────┼─────────┤        │
    │  │[开始使用]│[开始使用]│[开始使用]│[联系我们]│        │
    │  │         │⭐ 推荐  │         │         │        │
    │  └─────────┴─────────┴─────────┴─────────┘        │
    └─────────────────────────────────────────────────────┘
    """,
    features=[
        "💰 价格展示 - 清晰的价格对比",
        "📋 特性列表 - 功能特性清单",
        "⭐ 推荐标记 - 推荐方案高亮",
        "✅❌ 图标 - 功能有无标识",
        "🔄 切换周期 - 月付/年付切换",
        "🎁 优惠标签 - 折扣/优惠信息",
        "📊 差异高亮 - 方案间差异对比",
        "🔗 CTA 按钮 - 转化引导按钮",
        "💬 定制选项 - 联系销售选项",
        "📱 响应式 - 移动端适配",
    ],
    code_skeleton="""
import streamlit as st

# ==================== 配置区 ====================
BILLING_PERIOD = \"{{billing_period}}\"  # 计费周期
RECOMMENDED_PLAN = \"{{recommended_plan}}\"  # 推荐方案
SHOW_TOGGLE = {{show_toggle}}  # 显示周期切换

# ==================== 价格方案配置 ====================
PRICING_PLANS = [
    {
        \"name\": \"基础版\",
        \"price\": 0,
        \"period\": \"免费\",
        \"description\": \"适合个人和小团队\",
        \"features\": [
            {\"name\": \"最多 5 个用户\", \"included\": True},
            {\"name\": \"10 GB 存储空间\", \"included\": True},
            {\"name\": \"基础报表\", \"included\": True},
            {\"name\": \"邮件支持\", \"included\": True},
            {\"name\": \"API 访问\", \"included\": False},
            {\"name\": \"自定义域名\", \"included\": False},
        ],
        \"cta_text\": \"开始使用\",
        \"recommended\": False
    },
    {
        \"name\": \"专业版\",
        \"price\": 99,
        \"period\": \"月\",
        \"description\": \"适合成长型企业\",
        \"features\": [
            {\"name\": \"最多 20 个用户\", \"included\": True},
            {\"name\": \"100 GB 存储空间\", \"included\": True},
            {\"name\": \"高级报表\", \"included\": True},
            {\"name\": \"优先支持\", \"included\": True},
            {\"name\": \"API 访问\", \"included\": True},
            {\"name\": \"自定义域名\", \"included\": False},
        ],
        \"cta_text\": \"开始使用\",
        \"recommended\": True
    },
    {
        \"name\": \"企业版\",
        \"price\": 299,
        \"period\": \"月\",
        \"description\": \"适合大规模部署\",
        \"features\": [
            {\"name\": \"无限用户\", \"included\": True},
            {\"name\": \"1 TB 存储空间\", \"included\": True},
            {\"name\": \"定制报表\", \"included\": True},
            {\"name\": \"24/7 专属支持\", \"included\": True},
            {\"name\": \"API 访问\", \"included\": True},
            {\"name\": \"自定义域名\", \"included\": True},
        ],
        \"cta_text\": \"开始使用\",
        \"recommended\": False
    },
    {
        \"name\": \"定制版\",
        \"price\": None,
        \"period\": \"联系销售\",
        \"description\": \"按需定制解决方案\",
        \"features\": [
            {\"name\": \"一切企业版功能\", \"included\": True},
            {\"name\": \"专属部署\", \"included\": True},
            {\"name\": \"SLA 保证\", \"included\": True},
            {\"name\": \"专属客户经理\", \"included\": True},
            {\"name\": \"定制开发\", \"included\": True},
            {\"name\": \"现场培训\", \"included\": True},
        ],
        \"cta_text\": \"联系我们\",
        \"recommended\": False
    }
]

# ==================== 计费周期切换 ====================
st.subheader(\"💰 选择适合您的方案\")

if SHOW_TOGGLE:
    period_toggle = st.toggle(\"📅 年付优惠 (省 20%)\", value=False)
    billing_period = \"年\" if period_toggle else \"月\"

    if period_toggle:
        st.info(\"🎁 年付可享受 20% 优惠！\")
else:
    billing_period = BILLING_PERIOD

# ==================== 价格表 ====================
cols = st.columns(len(PRICING_PLANS))

for col, plan in zip(cols, PRICING_PLANS):
    with col:
        # 推荐标记
        if plan[\"recommended\"]:
            st.markdown(f\"\"\"
<div style='background: #ffc107; color: white; text-align: center; padding: 0.3rem; border-radius: 4px 4px 0 0; font-weight: bold;'>
    ⭐ 推荐
</div>
\"\"\", unsafe_allow_html=True)

        # 方案卡片
        bg_color = \"\"\" if not plan[\"recommended\"] else \"background: #fff9e6;\"

        st.markdown(f\"\"\"
<div style='{bg_color} padding: 1.5rem; border: 2px solid #dee2e6; border-radius: 8px; text-align: center;'>
    <h3 style='margin: 0.5rem 0;'>{plan['name']}</h3>
    <p style='color: #666; font-size: 0.9rem;'>{plan['description']}</p>
\"\"\", unsafe_allow_html=True)

        # 价格
        if plan['price'] is not None:
            if billing_period == \"年\" and plan['period'] == \"月\":
                yearly_price = int(plan['price'] * 12 * 0.8)
                st.markdown(f\"\"\"
<div style='font-size: 2rem; font-weight: bold; color: #007bff;'>¥{yearly_price}<span style='font-size: 1rem; color: #666;'>/年</span></div>
<div style='color: #999; font-size: 0.85rem; text-decoration: line-through;'>¥{plan['price'] * 12}/年</div>
\"\"\", unsafe_allow_html=True)
            else:
                price_display = f\"¥{plan['price']}\" if plan['price'] > 0 else \"免费\"
                st.markdown(f\"\"\"
<div style='font-size: 2rem; font-weight: bold; color: #007bff;'>{price_display}<span style='font-size: 1rem; color: #666;'>/{plan['period']}</span></div>
\"\"\", unsafe_allow_html=True)
        else:
            st.markdown(f\"\"\"
<div style='font-size: 1.5rem; font-weight: bold; color: #007bff;'>联系销售</div>
\"\"\", unsafe_allow_html=True)

        st.divider()

        # 功能列表
        for feature in plan['features']:
            icon = \"✅\" if feature['included'] else \"❌\"
            color = \"#28a745\" if feature['included'] else \"#dc3545\"
            st.markdown(f\"\"\"
<div style='display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0; font-size: 0.9rem;'>
    <span style='color: {color};'>{icon}</span>
    <span style='{\"color: #999;\" if not feature[\"included\"] else \"\"}'>{feature['name']}</span>
</div>
\"\"\", unsafe_allow_html=True)

        # CTA 按钮
        button_type = \"primary\" if plan[\"recommended\"] else \"secondary\"
        if st.button(plan['cta_text'], key=f\"cta_{plan['name']}\", use_container_width=True, type=button_type):
            if plan['price'] is None:
                st.info(\"📞 联系销售获取定制方案\")
            else:
                st.success(f\"已选择 {plan['name']}！\")

        st.markdown(\"</div>\", unsafe_allow_html=True)

# ==================== 对比表格（备选视图） ====================
st.divider()

with st.expander(\"📊 详细对比表\", expanded=False):
    # 创建对比数据
    comparison_data = {
        \"功能\": [f['name'] for f in PRICING_PLANS[0]['features']],
        **{plan['name']: [\"✅\" if f['included'] else \"❌\" for f in plan['features']] for plan in PRICING_PLANS}
    }

    import pandas as pd
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

# ==================== 常见问题 ====================
st.divider()

st.subheader(\"❓ 常见问题\")

faq = [
    {\"q\": \"可以随时取消订阅吗？\", \"a\": \"可以，随时取消，不收取额外费用。\"},
    {\"q\": \"支持哪些支付方式？\", \"a\": \"支持微信、支付宝、银行转账等多种方式。\"},
    {\"q\": \"如何升级或降级？\", \"a\": \"在设置中可以随时更改您的订阅计划。\"},
]

for i, item in enumerate(faq):
    with st.expander(f\"**Q: {item['q']}**\", expanded=i == 0):
        st.write(f\"A: {item['a']}\")

# ==================== 联系方式 ====================
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(\"**💬 销售咨询**\")
    st.write(\"📞 400-123-4567\")
    st.write(\"📧 sales@example.com\")

with col2:
    st.markdown(\"**🤝 技术支持**\")
    st.write(\"📞 400-765-4321\")
    st.write(\"📧 support@example.com\")

with col3:
    st.markdown(\"**🏢 企业合作**\")
    st.write(\"📞 400-111-2222\")
    st.write(\"📧 business@example.com\")
""",
    props=[
        ComponentProp("billing_period", "str", "月", False, "默认计费周期"),
        ComponentProp("recommended_plan", "str", "professional", False, "推荐方案"),
        ComponentProp("show_toggle", "bool", True, False, "显示月付/年付切换"),
        ComponentProp("show_faq", "bool", True, False, "显示常见问题"),
        ComponentProp("show_contact", "bool", True, False, "显示联系方式"),
    ],
    tags=["价格", "定价", "套餐", "商务"],
    dependencies=["streamlit", "pandas"],
    industry_compatibility=["general", "ecommerce", "saas", "education"],
)


# ============================================================================
# 组件注册表
# ============================================================================

MEDIUM_COMPONENTS = {
    "metric_card": METRIC_CARD,
    "chart_panel": CHART_PANEL,
    "filter_bar": FILTER_BAR,
    "data_list": DATA_LIST,
    "nav_sidebar": NAV_SIDEBAR,
    "header_bar": HEADER_BAR,
    "footer_bar": FOOTER_BAR,
    "alert_panel": ALERT_PANEL,
    "upload_zone": UPLOAD_ZONE,
    "comment_section": COMMENT_SECTION,
    "timeline_block": TIMELINE_BLOCK,
    "pricing_table": PRICING_TABLE,
}


# ============================================================================
# 便捷函数
# ============================================================================

def get_medium_component(component_id: str) -> Optional[MediumComponent]:
    """
    获取中型组件

    Args:
        component_id: 组件ID

    Returns:
        中型组件实例，不存在则返回 None
    """
    return MEDIUM_COMPONENTS.get(component_id)


def list_medium_components(
    category: Optional[MediumComponentCategory] = None
) -> List[MediumComponent]:
    """
    列出中型组件

    Args:
        category: 指定分类，None 表示全部

    Returns:
        中型组件列表
    """
    if category:
        return [c for c in MEDIUM_COMPONENTS.values() if c.category == category]
    return list(MEDIUM_COMPONENTS.values())


def get_components_by_industry(industry: str) -> List[MediumComponent]:
    """
    按行业获取推荐组件

    Args:
        industry: 行业名称

    Returns:
        适用于该行业的中型组件列表
    """
    return [
        c for c in MEDIUM_COMPONENTS.values()
        if industry in c.industry_compatibility or "general" in c.industry_compatibility
    ]


def search_medium_components(keyword: str) -> List[MediumComponent]:
    """
    搜索中型组件

    Args:
        keyword: 搜索关键词

    Returns:
        匹配的中型组件列表
    """
    keyword_lower = keyword.lower()
    results = []
    for component in MEDIUM_COMPONENTS.values():
        if (keyword_lower in component.name.lower() or
            keyword_lower in component.description.lower() or
            any(keyword_lower in tag.lower() for tag in component.tags)):
            results.append(component)
    return results


def get_composable_components() -> List[MediumComponent]:
    """
    获取可组合的组件（用于构建大型组件）

    Returns:
        可组合的中型组件列表
    """
    return [c for c in MEDIUM_COMPONENTS.values() if c.composable]


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "MediumComponentCategory",
    # 数据类
    "ComponentProp",
    "MediumComponent",
    # 组件定义
    "METRIC_CARD",
    "CHART_PANEL",
    "FILTER_BAR",
    "DATA_LIST",
    "NAV_SIDEBAR",
    "HEADER_BAR",
    "FOOTER_BAR",
    "ALERT_PANEL",
    "UPLOAD_ZONE",
    "COMMENT_SECTION",
    "TIMELINE_BLOCK",
    "PRICING_TABLE",
    # 注册表
    "MEDIUM_COMPONENTS",
    # 便捷函数
    "get_medium_component",
    "list_medium_components",
    "get_components_by_industry",
    "search_medium_components",
    "get_composable_components",
]
