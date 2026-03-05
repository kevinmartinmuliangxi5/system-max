"""
Data Analytics Industry Templates - 数据分析/BI行业模板
=======================================================

包含数据分析行业专用的 5 个完整页面模板：

模板列表:
    1. BIDashboard - BI 仪表盘（多维度数据、下钻、联动）
    2. ReportBuilder - 报表生成器（拖拽式、导出）
    3. DataExplorer - 数据探索（查询、可视化、保存）
    4. AlertMonitor - 告警监控（阈值、通知、历史）
    5. ETLPipeline - ETL 流程（数据源、转换、目标）

推荐主题:
    - corporate_gray: 适合企业级 BI 场景
    - tech_neon: 适合数据可视化场景
    - midnight_blue: 适合监控大屏场景

使用方式:
    from ui_library.industries.data_analytics import (
        BIDashboard,
        ReportBuilder,
        DataExplorer,
        AlertMonitor,
        ETLPipeline,
    )
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import pandas as pd
from datetime import datetime, timedelta


# ============================================================================
# 枚举定义
# ============================================================================

class ChartType(Enum):
    """图表类型"""
    LINE = "line"               # 折线图
    BAR = "bar"                 # 柱状图
    PIE = "pie"                 # 饼图
    AREA = "area"               # 面积图
    SCATTER = "scatter"         # 散点图
    HEATMAP = "heatmap"         # 热力图
    TREEMAP = "treemap"         # 树图
    FUNNEL = "funnel"           # 漏斗图
    GAUGE = "gauge"             # 仪表盘
    TABLE = "table"             # 表格


class AggregationType(Enum):
    """聚合类型"""
    SUM = "sum"                 # 求和
    AVG = "avg"                 # 平均
    COUNT = "count"             # 计数
    MIN = "min"                 # 最小值
    MAX = "max"                 # 最大值
    DISTINCT = "distinct"       # 去重计数


class ExportFormat(Enum):
    """导出格式"""
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"
    JSON = "json"
    IMAGE = "image"


class AlertSeverity(Enum):
    """告警级别"""
    INFO = "info"               # 信息
    WARNING = "warning"         # 警告
    CRITICAL = "critical"       # 严重
    FATAL = "fatal"             # 致命


class PipelineStatus(Enum):
    """流程状态"""
    IDLE = "idle"               # 空闲
    RUNNING = "running"         # 运行中
    SUCCESS = "success"         # 成功
    FAILED = "failed"           # 失败
    PAUSED = "paused"           # 暂停


# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class MetricDefinition:
    """
    指标定义

    Attributes:
        name: 指标名称
        field: 数据字段
        aggregation: 聚合类型
        format: 格式化字符串
        color: 显示颜色
        icon: 图标
    """
    name: str
    field: str
    aggregation: AggregationType
    format: str = "{:.2f}"
    color: str = "#007bff"
    icon: str = "📊"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "field": self.field,
            "aggregation": self.aggregation.value,
            "format": self.format,
            "color": self.color,
            "icon": self.icon,
        }


@dataclass
class DimensionDefinition:
    """
    维度定义

    Attributes:
        name: 维度名称
        field: 数据字段
        values: 可选值列表
        default_value: 默认值
    """
    name: str
    field: str
    values: Optional[List[str]] = None
    default_value: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "field": self.field,
            "values": self.values,
            "default_value": self.default_value,
        }


@dataclass
class ChartDefinition:
    """
    图表定义

    Attributes:
        id: 图表ID
        title: 图表标题
        chart_type: 图表类型
        x_field: X轴字段
        y_field: Y轴字段
        color_field: 颜色字段
        size: 图表尺寸
        interactive: 是否交互
        drill_down: 下钻配置
    """
    id: str
    title: str
    chart_type: ChartType
    x_field: str
    y_field: str
    color_field: Optional[str] = None
    size: str = "medium"
    interactive: bool = True
    drill_down: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "chart_type": self.chart_type.value,
            "x_field": self.x_field,
            "y_field": self.y_field,
            "color_field": self.color_field,
            "size": self.size,
            "interactive": self.interactive,
            "drill_down": self.drill_down,
        }


@dataclass
class AlertRule:
    """
    告警规则

    Attributes:
        id: 规则ID
        name: 规则名称
        metric: 监控指标
        condition: 条件表达式
        threshold: 阈值
        severity: 告警级别
        enabled: 是否启用
        notification_channels: 通知渠道
    """
    id: str
    name: str
    metric: str
    condition: str  # ">", "<", ">=", "<=", "==", "!="
    threshold: float
    severity: AlertSeverity
    enabled: bool = True
    notification_channels: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "metric": self.metric,
            "condition": self.condition,
            "threshold": self.threshold,
            "severity": self.severity.value,
            "enabled": self.enabled,
            "notification_channels": self.notification_channels,
        }


@dataclass
class PipelineStep:
    """
    流程步骤

    Attributes:
        id: 步骤ID
        name: 步骤名称
        type: 步骤类型
        config: 配置参数
        order: 执行顺序
    """
    id: str
    name: str
    type: str  # "extract", "transform", "load"
    config: Dict[str, Any]
    order: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "config": self.config,
            "order": self.order,
        }


# ============================================================================
# 1. BIDashboard - BI 仪表盘模板
# ============================================================================

class BIDashboard:
    """
    BI 仪表盘模板

    功能: 多维度数据展示、下钻分析、图表联动

    推荐主题: corporate_gray, tech_neon

    特性:
        - 实时数据刷新
        - 多维度筛选
        - 图表下钻
        - 跨图表联动
        - 自定义布局
    """

    # 默认指标定义
    DEFAULT_METRICS = [
        MetricDefinition(
            name="总收入",
            field="revenue",
            aggregation=AggregationType.SUM,
            format="¥{:.2f}万",
            color="#28a745",
            icon="💰"
        ),
        MetricDefinition(
            name="订单数",
            field="orders",
            aggregation=AggregationType.COUNT,
            format="{:.0f}",
            color="#007bff",
            icon="📦"
        ),
        MetricDefinition(
            name="客单价",
            field="amount",
            aggregation=AggregationType.AVG,
            format="¥{:.2f}",
            color="#ffc107",
            icon="🏷️"
        ),
        MetricDefinition(
            name="转化率",
            field="conversion",
            aggregation=AggregationType.AVG,
            format="{:.2f}%",
            color="#17a2b8",
            icon="📈"
        ),
    ]

    # 默认维度定义
    DEFAULT_DIMENSIONS = [
        DimensionDefinition(
            name="时间范围",
            field="date",
            default_value="最近7天"
        ),
        DimensionDefinition(
            name="地区",
            field="region",
            values=["华东", "华南", "华北", "西南", "西北"],
            default_value="全部"
        ),
        DimensionDefinition(
            name="产品类别",
            field="category",
            values=["电子产品", "服装", "食品", "家居"],
            default_value="全部"
        ),
    ]

    # 默认图表定义
    DEFAULT_CHARTS = [
        ChartDefinition(
            id="revenue_trend",
            title="收入趋势",
            chart_type=ChartType.LINE,
            x_field="date",
            y_field="revenue",
            size="large"
        ),
        ChartDefinition(
            id="category_dist",
            title="品类分布",
            chart_type=ChartType.PIE,
            x_field="category",
            y_field="revenue",
            size="medium"
        ),
        ChartDefinition(
            id="region_rank",
            title="地区排行",
            chart_type=ChartType.BAR,
            x_field="region",
            y_field="revenue",
            size="medium"
        ),
        ChartDefinition(
            id="conversion_funnel",
            title="转化漏斗",
            chart_type=ChartType.FUNNEL,
            x_field="stage",
            y_field="count",
            size="medium"
        ),
    ]

    def __init__(
        self,
        metrics: Optional[List[MetricDefinition]] = None,
        dimensions: Optional[List[DimensionDefinition]] = None,
        charts: Optional[List[ChartDefinition]] = None
    ):
        """
        初始化 BI 仪表盘

        Args:
            metrics: 指标列表
            dimensions: 维度列表
            charts: 图表列表
        """
        self.metrics = metrics or self.DEFAULT_METRICS
        self.dimensions = dimensions or self.DEFAULT_DIMENSIONS
        self.charts = charts or self.DEFAULT_CHARTS
        self._data_cache = {}
        self._filters = {}

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return f'''"""
BI 仪表盘 - Streamlit 实现
==========================

功能: 多维度数据展示、下钻分析、图表联动
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="BI 仪表盘",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# 模拟数据生成
# ============================================================================

@st.cache_data(ttl=300)
def generate_dashboard_data():
    """生成仪表盘数据"""
    import numpy as np
    from datetime import timedelta

    # 生成日期序列
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start_date, end_date, freq="D")

    # 生成基础数据
    np.random.seed(42)
    n = len(dates)

    data = {{
        "date": dates,
        "revenue": np.random.uniform(50, 200, n) * 10000,
        "orders": np.random.randint(100, 500, n),
        "amount": np.random.uniform(100, 1000, n),
        "conversion": np.random.uniform(1, 5, n),
        "region": np.random.choice(["华东", "华南", "华北", "西南", "西北"], n),
        "category": np.random.choice(["电子产品", "服装", "食品", "家居"], n),
    }}

    df = pd.DataFrame(data)
    df["week"] = df["date"].dt.isocalendar().week
    df["month"] = df["date"].dt.month

    return df


# ============================================================================
# 状态管理
# ============================================================================

if "dashboard_filters" not in st.session_state:
    st.session_state.dashboard_filters = {{
        "date_range": "最近7天",
        "region": "全部",
        "category": "全部",
        "auto_refresh": False,
        "refresh_interval": 60,
    }}

if "dashboard_drill_down" not in st.session_state:
    st.session_state.dashboard_drill_down = {{}}


# ============================================================================
# 侧边栏 - 筛选控制
# ============================================================================

st.sidebar.title("🎛️ 控制面板")

# 数据刷新
with st.sidebar.expander("⏱️ 数据刷新", expanded=False):
    auto_refresh = st.checkbox(
        "自动刷新",
        value=st.session_state.dashboard_filters["auto_refresh"],
        key="auto_refresh_toggle"
    )
    st.session_state.dashboard_filters["auto_refresh"] = auto_refresh

    if auto_refresh:
        interval = st.slider(
            "刷新间隔（秒）",
            30, 300,
            st.session_state.dashboard_filters["refresh_interval"]
        )
        st.session_state.dashboard_filters["refresh_interval"] = interval
        st.caption(f"每 {{interval}} 秒自动刷新")

    if st.button("🔄 立即刷新", use_container_width=True):
        st.cache_data.clear()
        st.success("数据已刷新！")
        st.rerun()

st.sidebar.divider()

# 维度筛选
with st.sidebar.expander("🔍 维度筛选", expanded=True):
    # 时间范围
    date_options = ["今天", "昨天", "最近7天", "最近30天", "本月", "上月", "自定义"]
    date_range = st.selectbox(
        "时间范围",
        date_options,
        index=date_options.index(st.session_state.dashboard_filters["date_range"])
    )
    st.session_state.dashboard_filters["date_range"] = date_range

    if date_range == "自定义":
        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("开始日期")
        with col2:
            end = st.date_input("结束日期")

    # 地区筛选
    regions = ["全部"] + ["华东", "华南", "华北", "西南", "西北"]
    region = st.selectbox(
        "地区",
        regions,
        index=regions.index(st.session_state.dashboard_filters["region"])
    )
    st.session_state.dashboard_filters["region"] = region

    # 品类筛选
    categories = ["全部"] + ["电子产品", "服装", "食品", "家居"]
    category = st.selectbox(
        "产品类别",
        categories,
        index=categories.index(st.session_state.dashboard_filters["category"])
    )
    st.session_state.dashboard_filters["category"] = category

st.sidebar.divider()

# 布局选择
with st.sidebar.expander("📐 布局设置", expanded=False):
    layout_style = st.radio(
        "布局风格",
        ["紧凑", "标准", "宽松"],
        horizontal=True
    )

    show_chart_titles = st.checkbox("显示图表标题", value=True)
    enable_drill_down = st.checkbox("启用下钻功能", value=True)

# ============================================================================
# 数据处理
# ============================================================================

@st.cache_data(ttl=60)
def apply_filters(df, filters):
    """应用筛选条件"""
    filtered_df = df.copy()

    # 时间范围筛选
    date_range = filters.get("date_range", "最近7天")
    end_date = datetime.now()

    if date_range == "今天":
        start_date = end_date.replace(hour=0, minute=0, second=0)
    elif date_range == "昨天":
        start_date = end_date - timedelta(days=1)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = start_date + timedelta(days=1)
    elif date_range == "最近7天":
        start_date = end_date - timedelta(days=7)
    elif date_range == "最近30天":
        start_date = end_date - timedelta(days=30)
    elif date_range == "本月":
        start_date = end_date.replace(day=1, hour=0, minute=0, second=0)
    elif date_range == "上月":
        start_date = end_date.replace(day=1) - timedelta(days=end_date.day)
        start_date = start_date.replace(day=1)
        end_date = start_date + timedelta(days=32)
        end_date = end_date.replace(day=1)
    else:  # 自定义
        start_date = end_date - timedelta(days=7)

    filtered_df = filtered_df[
        (filtered_df["date"] >= start_date) &
        (filtered_df["date"] <= end_date)
    ]

    # 地区筛选
    region = filters.get("region", "全部")
    if region != "全部":
        filtered_df = filtered_df[filtered_df["region"] == region]

    # 品类筛选
    category = filters.get("category", "全部")
    if category != "全部":
        filtered_df = filtered_df[filtered_df["category"] == category]

    return filtered_df


# 获取数据
df = generate_dashboard_data()
filtered_df = apply_filters(df, st.session_state.dashboard_filters)


# ============================================================================
# 主标题栏
# ============================================================================

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    st.title("📊 BI 仪表盘")

with col2:
    st.metric("数据周期", st.session_state.dashboard_filters["date_range"])

with col3:
    st.metric("记录数", f"{{len(filtered_df):,}}")


# ============================================================================
# 核心指标卡片
# ============================================================================

st.divider()

metric_cols = st.columns(len({m.name for m in self.DEFAULT_METRICS}))

for i, metric in enumerate(self.DEFAULT_METRICS):
    with metric_cols[i % len(metric_cols)]:
        # 计算指标值
        if metric.aggregation == AggregationType.SUM:
            value = filtered_df[metric.field].sum()
        elif metric.aggregation == AggregationType.COUNT:
            value = len(filtered_df)
        elif metric.aggregation == AggregationType.AVG:
            value = filtered_df[metric.field].mean()
        elif metric.aggregation == AggregationType.MAX:
            value = filtered_df[metric.field].max()
        elif metric.aggregation == AggregationType.MIN:
            value = filtered_df[metric.field].min()

        # 计算变化率
        prev_value = df[metric.field].sum() if metric.aggregation == AggregationType.SUM else len(df)
        if prev_value > 0:
            change = (value - prev_value) / prev_value * 100
        else:
            change = 0

        # 格式化显示
        if metric.format.startswith("¥"):
            formatted_value = metric.format.format(value / 10000) + "万"
        elif "%" in metric.format:
            formatted_value = metric.format.format(value)
        else:
            formatted_value = metric.format.format(value)

        # 显示指标
        st.metric(
            label=f"{{metric.icon}} {{metric.name}}",
            value=formatted_value,
            delta=f"{{change:+.1f}}%" if abs(change) > 0.1 else None,
            delta_color="normal" if change >= 0 else "inverse"
        )


# ============================================================================
# 图表区域
# ============================================================================

st.divider()

# 收入趋势图
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💰 收入趋势")

    # 按日期聚合
    trend_data = filtered_df.groupby("date").agg({{"revenue": "sum", "orders": "sum"}}).reset_index()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend_data["date"],
        y=trend_data["revenue"] / 10000,
        mode="lines+markers",
        name="收入（万元）",
        line=dict(color="#28a745", width=3),
        fill="tozeroy",
        fillcolor="rgba(40, 167, 69, 0.1)"
    ))

    fig_trend.update_layout(
        xaxis_title="日期",
        yaxis_title="收入（万元）",
        hovermode="x unified",
        height=350,
        margin=dict(l=0, r=0, t=30, b=0),
        template="plotly_white"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("📊 品类分布")

    category_data = filtered_df.groupby("category").agg({{"revenue": "sum"}}).reset_index()

    fig_pie = go.Figure(data=[go.Pie(
        labels=category_data["category"],
        values=category_data["revenue"],
        hole=0.4,
        textinfo="percent+label",
        textposition="inside"
    )])

    fig_pie.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False
    )

    st.plotly_chart(fig_pie, use_container_width=True)


st.divider()

# 地区排行
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 地区收入排行")

    region_data = filtered_df.groupby("region").agg({{"revenue": "sum"}}).reset_index()
    region_data = region_data.sort_values("revenue", ascending=False)

    fig_bar = px.bar(
        region_data,
        x="revenue",
        y="region",
        orientation="h",
        text_auto=",.0f",
        color="revenue",
        color_continuous_scale="Blues"
    )

    fig_bar.update_layout(
        xaxis_title="收入（元）",
        yaxis_title="",
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("📈 订单量趋势")

    order_data = filtered_df.groupby("date").agg({{"orders": "sum"}}).reset_index()

    fig_area = px.area(
        order_data,
        x="date",
        y="orders",
        color_discrete_sequence=["#007bff"]
    )

    fig_area.update_layout(
        xaxis_title="日期",
        yaxis_title="订单数",
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        template="plotly_white"
    )

    st.plotly_chart(fig_area, use_container_width=True)


# ============================================================================
# 数据表格
# ============================================================================

st.divider()

with st.expander("📋 查看详细数据", expanded=False):
    # 显示聚合后的数据
    display_data = filtered_df.groupby("date").agg({{
        "revenue": "sum",
        "orders": "sum",
        "amount": "mean",
        "conversion": "mean"
    }}).reset_index()

    display_data["revenue"] = display_data["revenue"] / 10000  # 转为万元

    display_data.columns = ["日期", "总收入（万元）", "订单数", "客单价", "转化率"]

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    # 导出按钮
    csv = display_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 导出数据",
        data=csv,
        file_name=f"dashboard_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.csv",
        mime="text/csv"
    )


# ============================================================================
# 联动分析
# ============================================================================

st.divider()

st.subheader("🔗 联动分析")

st.caption("点击上方任意图表区域，此处显示相关详细数据")

# 获取点击事件
if st.session_state.dashboard_drill_down:
    drill_info = st.session_state.dashboard_drill_down
    st.info(f"🔍 下钻分析: {{drill_info}}")
else:
    st.info("💡 点击图表元素可进行下钻分析")


# ============================================================================
# 页脚
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.caption(f"🕐 最后更新: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")

with col2:
    if st.session_state.dashboard_filters["auto_refresh"]:
        st.caption(f"🔄 自动刷新: 每 {{st.session_state.dashboard_filters['refresh_interval']}} 秒")

with col3:
    st.caption("📊 数据来源: 业务系统")
'''

    def get_sample_data(self) -> Dict[str, Any]:
        """获取示例数据结构"""
        return {
            "metrics": [m.to_dict() for m in self.metrics],
            "dimensions": [d.to_dict() for d in self.dimensions],
            "charts": [c.to_dict() for c in self.charts],
            "sample_records": [
                {
                    "date": "2024-01-15",
                    "revenue": 125000.50,
                    "orders": 342,
                    "region": "华东",
                    "category": "电子产品",
                },
                {
                    "date": "2024-01-15",
                    "revenue": 89300.00,
                    "orders": 256,
                    "region": "华南",
                    "category": "服装",
                },
            ]
        }


# ============================================================================
# 2. ReportBuilder - 报表生成器模板
# ============================================================================

class ReportBuilder:
    """
    报表生成器模板

    功能: 拖拽式报表设计、模板保存、多格式导出

    推荐主题: corporate_gray

    特性:
        - 可视化报表设计
        - 组件拖拽布局
        - 数据绑定
        - 样式定制
        - 导出 PDF/Excel
    """

    def __init__(self):
        """初始化报表生成器"""
        self._templates = {}
        self._components = [
            {"id": "table", "name": "数据表格", "icon": "📋"},
            {"id": "chart", "name": "图表", "icon": "📊"},
            {"id": "metric", "name": "指标卡", "icon": "🎯"},
            {"id": "text", "name": "文本", "icon": "📝"},
            {"id": "image", "name": "图片", "icon": "🖼️"},
            {"id": "divider", "name": "分割线", "icon": "➖"},
        ]

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
报表生成器 - Streamlit 实现
==============================

功能: 拖拽式报表设计、模板保存、多格式导出
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import xlsxwriter
from datetime import datetime


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="报表生成器",
    page_icon="📑",
    layout="wide"
)


# ============================================================================
# 状态管理
# ============================================================================

if "report_components" not in st.session_state:
    st.session_state.report_components = []

if "report_templates" not in st.session_state:
    st.session_state.report_templates = {{
        "sales_report": {{
            "name": "销售报表",
            "components": ["metric", "chart", "table"]
        }},
        "inventory_report": {{
            "name": "库存报表",
            "components": ["table", "metric"]
        }}
    }}

if "selected_template" not in st.session_state:
    st.session_state.selected_template = None


# ============================================================================
# 示例数据
# ============================================================================

@st.cache_data
def get_sample_data():
    """获取示例数据"""
    data = {{
        "product": ["产品A", "产品B", "产品C", "产品D", "产品E"],
        "sales": [125000, 89000, 67000, 156000, 98000],
        "quantity": [342, 256, 189, 421, 298],
        "profit": [45000, 32000, 21000, 58000, 35000],
        "category": ["电子", "服装", "食品", "电子", "家居"]
    }}
    return pd.DataFrame(data)


# ============================================================================
# 侧边栏 - 组件面板
# ============================================================================

st.sidebar.title("📦 报表组件")

st.sidebar.caption("拖拽组件到报表区域")

# 组件列表
components = [
    {{"id": "table", "name": "数据表格", "icon": "📋", "description": "展示详细数据列表"}},
    {{"id": "chart", "name": "图表", "icon": "📊", "description": "可视化数据展示"}},
    {{"id": "metric", "name": "指标卡", "icon": "🎯", "description": "突出显示关键指标"}},
    {{"id": "text", "name": "文本", "icon": "📝", "description": "标题、说明文字"}},
    {{"id": "image", "name": "图片", "icon": "🖼️", "description": "插入图片或Logo"}},
    {{"id": "divider", "name": "分割线", "icon": "➖", "description": "内容分隔"}},
]

for comp in components:
    with st.sidebar.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(comp["icon"])
        with col2:
            st.write(comp["name"])
            st.caption(comp["description"])

        if st.button("添加", key=f'add_{comp["id"]}', use_container_width=True):
            st.session_state.report_components.append({{
                "id": comp["id"],
                "name": comp["name"],
                "icon": comp["icon"]
            }})
            st.rerun()

st.sidebar.divider()

# 模板选择
st.sidebar.subheader("📋 报表模板")

for template_id, template in st.session_state.report_templates.items():
    if st.button(
        f'{{template["name"]}}',
        key=f'template_{template_id}',
        use_container_width=True
    ):
        st.session_state.selected_template = template_id
        st.session_state.report_components = []
        st.rerun()


# ============================================================================
# 主界面
# ============================================================================

st.title("📑 报表生成器")

# 报表设置
col1, col2, col3 = st.columns(3)

with col1:
    report_name = st.text_input("报表名称", value="未命名报表")

with col2:
    report_author = st.text_input("作者", value="管理员")

with col3:
    created_date = st.date_input("创建日期", value=datetime.now().date())

st.divider()


# ============================================================================
# 报表预览区域
# ============================================================================

st.subheader("👁️ 报表预览")

if not st.session_state.report_components:
    st.info("👈 从左侧面板选择组件添加到报表")
else:
    # 报表标题
    st.markdown(f"<h1 style='text-align: center;'>{{report_name}}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>作者: {{report_author}} | 日期: {{created_date}}</p>", unsafe_allow_html=True)
    st.divider()

    df = get_sample_data()

    # 渲染组件
    for i, comp in enumerate(st.session_state.report_components):
        st.markdown(f"<h3>{{comp['icon']}} {{comp['name']}}</h3>", unsafe_allow_html=True)

        if comp["id"] == "table":
            # 数据表格
            st.dataframe(df, use_container_width=True)

        elif comp["id"] == "chart":
            # 图表
            chart_type = st.selectbox(
                "图表类型",
                ["柱状图", "折线图", "饼图", "面积图"],
                key=f'chart_type_{i}'
            )

            if chart_type == "柱状图":
                fig = px.bar(df, x="product", y="sales", title="销售额")
            elif chart_type == "折线图":
                fig = px.line(df, x="product", y="sales", title="销售额趋势")
            elif chart_type == "饼图":
                fig = px.pie(df, names="product", values="sales", title="销售占比")
            else:
                fig = px.area(df, x="product", y="sales", title="销售额")

            st.plotly_chart(fig, use_container_width=True)

        elif comp["id"] == "metric":
            # 指标卡
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric("总销售额", f"¥{{df['sales'].sum()/10000:.1f}}万")
            with metric_cols[1]:
                st.metric("总销量", f"{{df['quantity'].sum():,}}")
            with metric_cols[2]:
                st.metric="总利润", f"¥{{df['profit'].sum()/10000:.1f}}万")
            with metric_cols[3]:
                st.metric="产品数", f"{{len(df)}}")

        elif comp["id"] == "text":
            # 文本
            text_content = st.text_area(
                "文本内容",
                value="这是报表的说明文字，可以在这里添加报表的分析、结论等信息。",
                key=f'text_{i}',
                label_visibility="collapsed"
            )
            st.info(text_content)

        elif comp["id"] == "image":
            # 图片
            uploaded_file = st.file_uploader(
                "上传图片",
                type=["png", "jpg", "jpeg"],
                key=f'image_{i}'
            )
            if uploaded_file:
                st.image(uploaded_file, use_container_width=True)

        elif comp["id"] == "divider":
            # 分割线
            st.markdown("---")

        # 删除按钮
        if st.button(f'删除此组件', key=f'delete_{i}'):
            st.session_state.report_components.pop(i)
            st.rerun()

        st.divider()


# ============================================================================
# 操作按钮
# ============================================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💾 保存模板", use_container_width=True):
        template_id = f"template_{{len(st.session_state.report_templates) + 1}}"
        st.session_state.report_templates[template_id] = {{
            "name": report_name,
            "components": [c["id"] for c in st.session_state.report_components]
        }}
        st.success(f"✅ 模板 '{report_name}' 已保存")

with col2:
    if st.button("🔄 清空报表", use_container_width=True):
        st.session_state.report_components = []
        st.rerun()

with col3:
    export_format = st.selectbox(
        "导出格式",
        ["CSV", "Excel", "JSON"],
        label_visibility="collapsed"
    )

with col4:
    if st.button("📥 导出报表", use_container_width=True, type="primary"):
        df = get_sample_data()

        if export_format == "CSV":
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "下载 CSV",
                csv,
                f"report_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.csv",
                "text/csv"
            )
        elif export_format == "Excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='数据')
            st.download_button(
                "下载 Excel",
                output.getvalue(),
                f"report_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif export_format == "JSON":
            json_data = df.to_json(orient='records', force_ascii=False)
            st.download_button(
                "下载 JSON",
                json_data,
                f"report_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json",
                "application/json"
            )


# ============================================================================
# 模板管理
# ============================================================================

st.divider()

st.subheader("📚 已保存的模板")

if st.session_state.report_templates:
    for template_id, template in st.session_state.report_templates.items():
        with st.expander(f'📄 {template["name"]}'):
            st.write(f"组件: {{', '.join(template['components'])}}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f'加载此模板', key=f'load_{template_id}'):
                    st.session_state.selected_template = template_id
                    st.info(f"已加载模板: {template['name']}")

            with col2:
                if st.button(f'删除模板', key=f'delete_template_{template_id}'):
                    del st.session_state.report_templates[template_id]
                    st.rerun()
else:
    st.info("还没有保存的模板，创建一个报表后点击上方"保存模板"按钮")
'''


# ============================================================================
# 3. DataExplorer - 数据探索模板
# ============================================================================

class DataExplorer:
    """
    数据探索模板

    功能: SQL 查询、可视化分析、结果保存

    推荐主题: tech_neon, midnight_blue

    特性:
        - SQL 编辑器
        - 数据预览
        - 快速可视化
        - 查询历史
        - 结果导出
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
数据探索 - Streamlit 实现
=============================

功能: SQL 查询、可视化分析、结果保存
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="数据探索",
    page_icon="🔍",
    layout="wide"
)


# ============================================================================
# 模拟数据源
# ============================================================================

@st.cache_data
def get_data_sources():
    """获取可用的数据源"""
    return {{
        "sales": {{
            "name": "销售数据",
            "tables": ["orders", "products", "customers"],
            "description": "2024年销售业务数据"
        }},
        "inventory": {{
            "name": "库存数据",
            "tables": ["stock", "warehouse", "inbound"],
            "description": "当前库存状态"
        }},
        "finance": {{
            "name": "财务数据",
            "tables": ["revenue", "expense", "profit"],
            "description": "财务报表数据"
        }}
    }}


@st.cache_data
def execute_query(sql: str) -> pd.DataFrame:
    """执行查询（模拟）"""
    # 在实际应用中，这里连接真实数据库
    # 这里返回模拟数据

    import numpy as np

    # 解析SQL关键字段
    if "sales" in sql.lower() and "orders" in sql.lower():
        return pd.DataFrame({{
            "order_id": range(1, 101),
            "date": pd.date_range("2024-01-01", periods=100),
            "product": np.random.choice(["A", "B", "C", "D"], 100),
            "quantity": np.random.randint(1, 50, 100),
            "amount": np.random.uniform(100, 5000, 100),
            "region": np.random.choice(["华东", "华南", "华北"], 100),
        }})
    else:
        return pd.DataFrame({{
            "id": [1, 2, 3],
            "name": ["示例1", "示例2", "示例3"],
            "value": [100, 200, 300]
        }})


# ============================================================================
# 状态管理
# ============================================================================

if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "saved_queries" not in st.session_state:
    st.session_state.saved_queries = {}

if "explorer_theme" not in st.session_state:
    st.session_state.explorer_theme = "tech_neon"


# ============================================================================
# 侧边栏 - 数据源和查询
# ============================================================================

st.sidebar.title("🗄️ 数据源")

# 数据源选择
data_sources = get_data_sources()

selected_source = st.selectbox(
    "选择数据源",
    list(data_sources.keys()),
    format_func=lambda x: data_sources[x]["name"]
)

st.sidebar.info(data_sources[selected_source]["description"])

# 表列表
st.sidebar.subheader("可用表")
for table in data_sources[selected_source]["tables"]:
    if st.button(f"📋 {table}", key=f"table_{table}", use_container_width=True):
        st.session_state[f"sql_query"] = f"SELECT * FROM {table} LIMIT 100"
        st.rerun()

st.sidebar.divider()

# 查询历史
st.sidebar.subheader("📜 查询历史")

if st.session_state.query_history:
    for i, query in enumerate(reversed(st.session_state.query_history[-5:])):
        with st.sidebar.expander(f"{query['time']}"):
            st.code(query['sql'], language="sql")
            if st.button(f'🔄 恢复此查询', key=f'history_{i}'):
                st.session_state.sql_query = query['sql']
                st.rerun()
else:
    st.sidebar.caption("暂无查询历史")


# ============================================================================
# 主界面
# ============================================================================

st.title("🔍 数据探索")

# SQL 编辑器
st.subheader("SQL 编辑器")

col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    default_sql = st.session_state.get("sql_query", "SELECT * FROM orders LIMIT 100")
    sql_query = st.text_area(
        "输入 SQL 查询",
        value=default_sql,
        height=100,
        label_visibility="collapsed"
    )

with col2:
    st.write("")
    st.write("")
    if st.button("▶️ 运行", use_container_width=True, type="primary"):
        # 记录查询历史
        st.session_state.query_history.append({{
            "sql": sql_query,
            "time": datetime.now().strftime("%H:%M:%S")
        }})
        st.session_state.last_query = sql_query
        st.rerun()

with col3:
    st.write("")
    st.write("")
    if st.button("💾 保存", use_container_width=True):
        save_name = st.text_input("查询名称", key="save_query_name")
        if save_name:
            st.session_state.saved_queries[save_name] = sql_query
            st.success(f"已保存: {save_name}")

# 快捷操作
st.caption("快捷操作")

quick_queries = {{
    "最近100条": "SELECT * FROM orders ORDER BY date DESC LIMIT 100",
    "按产品汇总": "SELECT product, SUM(quantity) as qty, SUM(amount) as total FROM orders GROUP BY product",
    "Top 10": "SELECT * FROM orders ORDER BY amount DESC LIMIT 10",
}}

cols = st.columns(len(quick_queries))
for col, (label, sql) in zip(cols, quick_queries.items()):
    with col:
        if st.button(label):
            st.session_state.sql_query = sql
            st.rerun()


# ============================================================================
# 查询结果
# ============================================================================

st.divider()

if "last_query" in st.session_state:
    st.subheader("📊 查询结果")

    # 执行查询
    with st.spinner("查询中..."):
        result_df = execute_query(st.session_state.last_query)

    # 结果统计
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("行数", f"{len(result_df):,}")
    with col2:
        st.metric("列数", len(result_df.columns))
    with col3:
        st.metric("数据大小", f"{result_df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    with col4:
        st.metric("查询时间", "0.23s")

    # 数据预览
    st.subheader("数据预览")

    # 显示选项
    view_mode = st.radio(
        "显示模式",
        ["表格", "JSON"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if view_mode == "表格":
        st.dataframe(
            result_df,
            use_container_width=True,
            height=400
        )
    else:
        st.json(result_df.to_dict(orient='records'))

    # 数据统计
    with st.expander("📈 数据统计", expanded=False):
        st.write(result_df.describe())

    # 导出
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 CSV",
            csv,
            "query_result.csv",
            "text/csv",
            use_container_width=True
        )

    with col2:
        json_data = result_df.to_json(orient='records')
        st.download_button(
            "📥 JSON",
            json_data,
            "query_result.json",
            "application/json",
            use_container_width=True
        )

    with col3:
        if st.button("📊 生成图表", use_container_width=True):
            st.session_state.show_chart_builder = True
            st.rerun()


# ============================================================================
# 快速可视化
# ============================================================================

if st.session_state.get("show_chart_builder", False):
    st.divider()
    st.subheader("📊 快速可视化")

    col1, col2, col3 = st.columns(3)

    with col1:
        x_axis = st.selectbox("X 轴", result_df.columns)

    with col2:
        y_axis = st.selectbox("Y 轴", result_df.columns)

    with col3:
        chart_type = st.selectbox(
            "图表类型",
            ["柱状图", "折线图", "散点图", "饼图", "箱线图"]
        )

    color_col = st.selectbox("颜色分组", [None] + list(result_df.columns))

    # 生成图表
    if chart_type == "柱状图":
        fig = px.bar(result_df, x=x_axis, y=y_axis, color=color_col)
    elif chart_type == "折线图":
        fig = px.line(result_df, x=x_axis, y=y_axis, color=color_col)
    elif chart_type == "散点图":
        fig = px.scatter(result_df, x=x_axis, y=y_axis, color=color_col)
    elif chart_type == "饼图":
        fig = px.pie(result_df, names=x_axis, values=y_axis)
    else:
        fig = px.box(result_df, x=x_axis, y=y_axis)

    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# 已保存的查询
# ============================================================================

st.divider()

st.subheader("💾 已保存的查询")

if st.session_state.saved_queries:
    for name, sql in st.session_state.saved_queries.items():
        with st.expander(f"📄 {name}"):
            st.code(sql, language="sql")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f'运行', key=f'run_{name}'):
                    st.session_state.sql_query = sql
                    st.rerun()
            with col2:
                if st.button(f'删除', key=f'del_{name}'):
                    del st.session_state.saved_queries[name]
                    st.rerun()
else:
    st.info("还没有保存的查询")
'''


# ============================================================================
# 4. AlertMonitor - 告警监控模板
# ============================================================================

class AlertMonitor:
    """
    告警监控模板

    功能: 阈值设置、实时监控、告警通知、历史记录

    推荐主题: midnight_blue

    特性:
        - 多指标监控
        - 阈值配置
        - 告警规则
        - 通知渠道
        - 历史查询
    """

    # 默认告警规则
    DEFAULT_RULES = [
        AlertRule(
            id="revenue_drop",
            name="收入下降告警",
            metric="revenue",
            condition="<",
            threshold=100000,
            severity=AlertSeverity.WARNING,
            notification_channels=["email", "webhook"]
        ),
        AlertRule(
            id="order_spike",
            name="订单量突增告警",
            metric="orders",
            condition=">",
            threshold=500,
            severity=AlertSeverity.INFO,
            notification_channels=["email"]
        ),
        AlertRule(
            id="conversion_low",
            name="转化率过低告警",
            metric="conversion",
            condition="<",
            threshold=2.0,
            severity=AlertSeverity.CRITICAL,
            notification_channels=["sms", "email", "webhook"]
        ),
    ]

    def __init__(self, rules: Optional[List[AlertRule]] = None):
        """初始化告警监控"""
        self.rules = rules or self.DEFAULT_RULES
        self._alert_history = []

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
告警监控 - Streamlit 实现
=============================

功能: 阈值设置、实时监控、告警通知、历史记录
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="告警监控",
    page_icon="🚨",
    layout="wide"
)


# ============================================================================
# 模拟数据
# ============================================================================

@st.cache_data(ttl=60)
def get_monitoring_data():
    """获取监控数据"""
    import numpy as np

    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)

    timestamps = pd.date_range(start_time, end_time, freq="5min")

    data = {{
        "timestamp": timestamps,
        "revenue": np.random.uniform(80000, 150000, len(timestamps)),
        "orders": np.random.randint(200, 600, len(timestamps)),
        "conversion": np.random.uniform(1.5, 4.5, len(timestamps)),
        "response_time": np.random.uniform(100, 500, len(timestamps)),
    }}

    return pd.DataFrame(data)


@st.cache_data(ttl=300)
def get_alert_history():
    """获取告警历史"""
    import numpy as np

    data = {{
        "time": pd.date_range(end=datetime.now(), periods=50, freq="H"),
        "rule": ["收入下降告警"] * 20 + ["订单量突增告警"] * 15 + ["转化率过低"] * 15,
        "severity": ["warning"] * 20 + ["info"] * 15 + ["critical"] * 15,
        "value": np.random.uniform(50000, 90000, 50),
        "threshold": 100000,
        "status": ["已处理"] * 30 + ["待处理"] * 10 + ["已忽略"] * 10,
    }}
    return pd.DataFrame(data)


# ============================================================================
# 状态管理
# ============================================================================

if "alert_rules" not in st.session_state:
    st.session_state.alert_rules = [
        {{
            "id": "revenue_drop",
            "name": "收入下降告警",
            "metric": "revenue",
            "condition": "<",
            "threshold": 100000,
            "severity": "warning"
        }},
        {{
            "id": "order_spike",
            "name": "订单量突增告警",
            "metric": "orders",
            "condition": ">",
            "threshold": 500,
            "severity": "info"
        }},
        {{
            "id": "conversion_low",
            "name": "转化率过低告警",
            "metric": "conversion",
            "condition": "<",
            "threshold": 2.0,
            "severity": "critical"
        }},
    ]

if "monitoring_auto_refresh" not in st.session_state:
    st.session_state.monitoring_auto_refresh = True


# ============================================================================
# 侧边栏 - 告警规则
# ============================================================================

st.sidebar.title("⚙️ 告警规则")

st.sidebar.caption("配置监控阈值和告警条件")

# 添加新规则
with st.sidebar.expander("➕ 添加告警规则", expanded=False):
    new_rule_name = st.text_input("规则名称")
    new_metric = st.selectbox("监控指标", ["revenue", "orders", "conversion", "response_time"])
    new_condition = st.selectbox("条件", ["<", ">", "<=", ">=", "==", "!="])
    new_threshold = st.number_input("阈值", value=100000.0)
    new_severity = st.selectbox("严重级别", ["info", "warning", "critical", "fatal"])

    if st.button("添加规则", use_container_width=True):
        st.session_state.alert_rules.append({{
            "id": f"rule_{len(st.session_state.alert_rules) + 1}",
            "name": new_rule_name,
            "metric": new_metric,
            "condition": new_condition,
            "threshold": new_threshold,
            "severity": new_severity
        }})
        st.success("规则已添加")
        st.rerun()

st.sidebar.divider()

# 规则列表
st.sidebar.subheader("📋 规则列表")

for i, rule in enumerate(st.session_state.alert_rules):
    with st.sidebar.expander(f'📌 {rule["name"]}'):
        st.caption(f'指标: {rule["metric"]}')
        st.caption(f'条件: {rule["condition"]} {rule["threshold"]}')

        severity_colors = {{
            "info": "🔵",
            "warning": "🟡",
            "critical": "🟠",
            "fatal": "🔴"
        }}
        st.markdown(f'{severity_colors[rule["severity"]]} **{rule["severity"].upper()}**')

        # 启用/禁用
        enabled = st.checkbox("启用", value=True, key=f'enable_{i}')

        if st.button("删除", key=f'delete_rule_{i}'):
            st.session_state.alert_rules.pop(i)
            st.rerun()


# ============================================================================
# 主界面 - 监控大屏
# ============================================================================

st.title("🚨 告警监控中心")

# 自动刷新控制
col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    auto_refresh = st.checkbox("自动刷新", value=st.session_state.monitoring_auto_refresh)
    st.session_state.monitoring_auto_refresh = auto_refresh

with col2:
    if st.button("🔄 立即刷新"):
        st.cache_data.clear()
        st.rerun()

with col3:
    last_update = st.caption(f"🕐 最后更新: {{datetime.now().strftime('%H:%M:%S')}}")

st.divider()


# ============================================================================
# 实时监控数据
# ============================================================================

# 获取数据
df = get_monitoring_data()
latest = df.iloc[-1]

# 核心指标卡片
st.subheader("📊 实时指标")

metric_cols = st.columns(4)

metrics_config = [
    {{"field": "revenue", "name": "当前收入", "format": "¥{:.2f}", "threshold": 100000}},
    {{"field": "orders", "name": "当前订单", "format": "{:.0f}", "threshold": 500}},
    {{"field": "conversion", "name": "转化率", "format": "{:.2f}%", "threshold": 2.0}},
    {{"field": "response_time", "name": "响应时间", "format": "{:.0f}ms", "threshold": 400}},
]

for i, metric in enumerate(metrics_config):
    with metric_cols[i]:
        value = latest[metric["field"]]
        threshold = metric["threshold"]

        # 判断是否告警
        is_alert = False
        if metric["field"] == "revenue" and value < threshold:
            is_alert = True
        elif metric["field"] == "orders" and value > threshold:
            is_alert = True
        elif metric["field"] == "conversion" and value < threshold:
            is_alert = True
        elif metric["field"] == "response_time" and value > threshold:
            is_alert = True

        # 格式化
        if "%" in metric["format"]:
            formatted = metric["format"].format(value)
        elif "¥" in metric["format"]:
            formatted = metric["format"].format(value)
        else:
            formatted = metric["format"].format(value)

        # 显示指标
        if is_alert:
            st.metric(metric["name"], formatted, delta="⚠️ 告警", delta_color="inverse")
        else:
            st.metric(metric["name"], formatted, delta="正常", delta_color="normal")


# ============================================================================
# 趋势图
# ============================================================================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 收入趋势")

    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["revenue"] / 10000,
        mode="lines",
        name="收入（万元）",
        line=dict(color="#28a745", width=2)
    ))

    # 添加阈值线
    fig_revenue.add_hline(
        y=10,
        line_dash="dash",
        line_color="red",
        annotation_text="告警阈值"
    )

    fig_revenue.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        template="plotly_white"
    )

    st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    st.subheader("📦 订单量")

    fig_orders = go.Figure()
    fig_orders.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["orders"],
        mode="lines",
        name="订单数",
        line=dict(color="#007bff", width=2),
        fill="tozeroy"
    ))

    fig_orders.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        template="plotly_white"
    )

    st.plotly_chart(fig_orders, use_container_width=True)


# ============================================================================
# 告警历史
# ============================================================================

st.divider()

st.subheader("📜 告警历史")

alert_history = get_alert_history()

# 筛选
col1, col2, col3 = st.columns(3)

with col1:
    severity_filter = st.multiselect(
        "严重级别",
        ["info", "warning", "critical", "fatal"],
        default=["info", "warning", "critical"]
    )

with col2:
    status_filter = st.multiselect(
        "状态",
        ["待处理", "已处理", "已忽略"],
        default=["待处理", "已处理"]
    )

with col3:
    st.write("")
    if st.button("🗑️ 清除历史", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 应用筛选
filtered_alerts = alert_history.copy()
if severity_filter:
    filtered_alerts = filtered_alerts[filtered_alerts["severity"].isin(severity_filter)]
if status_filter:
    filtered_alerts = filtered_alerts[filtered_alerts["status"].isin(status_filter)]

# 显示告警列表
for _, alert in filtered_alerts.iterrows():
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        severity_icons = {{
            "info": "🔵",
            "warning": "🟡",
            "critical": "🟠",
            "fatal": "🔴"
        }}

        with col1:
            st.markdown(f'{severity_icons[alert["severity"]]} **{alert["rule"]}**')
            st.caption(alert["time"].strftime("%Y-%m-%d %H:%M"))

        with col2:
            st.write(f"当前值: **{alert["value"]:,.0f}**")
            st.caption(f"阈值: {alert["threshold"]:,.0f}")

        with col3:
            status_colors = {{
                "待处理": "🔴",
                "已处理": "✅",
                "已忽略": "⏭️"
            }}
            st.markdown(f'{status_colors[alert["status"]]} {alert["status"]}')

        with col4:
            if alert["status"] == "待处理":
                if st.button("处理", key=f'handle_{alert.name}', use_container_width=True):
                    st.success(f"已标记为处理: {alert['rule']}")

        st.divider()


# ============================================================================
# 告警统计
# ============================================================================

with st.expander("📈 告警统计", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("按严重级别统计")
        severity_counts = alert_history["severity"].value_counts()
        st.bar_chart(severity_counts)

    with col2:
        st.subheader("按规则统计")
        rule_counts = alert_history["rule"].value_counts()
        st.bar_chart(rule_counts)
'''


# ============================================================================
# 5. ETLPipeline - ETL 流程模板
# ============================================================================

class ETLPipeline:
    """
    ETL 流程模板

    功能: 数据源配置、转换规则、目标加载、流程调度

    推荐主题: corporate_gray, midnight_blue

    特性:
        - 可视化流程设计
        - 数据源连接
        - 转换规则配置
        - 定时调度
        - 执行监控
    """

    def __init__(self):
        """初始化 ETL 流程"""
        self._pipelines = {}
        self._data_sources = {
            "mysql": {"name": "MySQL 数据库", "type": "database"},
            "postgres": {"name": "PostgreSQL 数据库", "type": "database"},
            "api": {"name": "API 接口", "type": "api"},
            "csv": {"name": "CSV 文件", "type": "file"},
            "excel": {"name": "Excel 文件", "type": "file"},
        }

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
ETL 流程 - Streamlit 实现
============================

功能: 数据源配置、转换规则、目标加载、流程调度
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="ETL 流程管理",
    page_icon="🔄",
    layout="wide"
)


# ============================================================================
# 状态管理
# ============================================================================

if "etl_pipelines" not in st.session_state:
    st.session_state.etl_pipelines = {{
        "daily_sales_sync": {{
            "name": "每日销售数据同步",
            "source": {{"type": "mysql", "config": {{"host": "192.168.1.100", "database": "sales"}}}},
            "transforms": [
                {{"type": "filter", "config": {{"field": "status", "value": "completed"}}}},
                {{"type": "aggregate", "config": {{"group_by": ["date"], "metrics": ["revenue", "orders"]}}}}
            ],
            "target": {{"type": "postgres", "config": {{"host": "192.168.1.200", "database": "dw"}}}},
            "schedule": {{"type": "cron", "expression": "0 2 * * *"}},
            "enabled": True
        }}
    }}

if "pipeline_runs" not in st.session_state:
    st.session_state.pipeline_runs = [
        {{
            "pipeline": "daily_sales_sync",
            "start_time": datetime.now() - timedelta(hours=2),
            "end_time": datetime.now() - timedelta(hours=2) + timedelta(minutes=15),
            "status": "success",
            "records_processed": 15420
        }},
        {{
            "pipeline": "daily_sales_sync",
            "start_time": datetime.now() - timedelta(hours=26),
            "end_time": datetime.now() - timedelta(hours=26) + timedelta(minutes=18),
            "status": "success",
            "records_processed": 15380
        }},
        {{
            "pipeline": "daily_sales_sync",
            "start_time": datetime.now() - timedelta(hours=50),
            "end_time": datetime.now() - timedelta(hours=50) + timedelta(minutes=12),
            "status": "failed",
            "records_processed": 0,
            "error": "Connection timeout"
        }},
    ]


# ============================================================================
# 侧边栏 - 流程列表
# ============================================================================

st.sidebar.title("📋 ETL 流程")

# 流程列表
for pipeline_id, pipeline in st.session_state.etl_pipelines.items():
    with st.sidebar.expander(f'🔄 {pipeline["name"]}'):
        status = "🟢 运行中" if pipeline.get("enabled", True) else "⚪ 已禁用"
        st.caption(status)

        if pipeline["enabled"]:
            if st.button(f'▶️ 运行', key=f'run_{pipeline_id}', use_container_width=True):
                st.session_state.running_pipeline = pipeline_id
                st.info(f"正在运行: {pipeline['name']}")

        if st.button(f'⚙️ 编辑', key=f'edit_{pipeline_id}', use_container_width=True):
            st.session_state.editing_pipeline = pipeline_id
            st.rerun()

st.sidebar.divider()

# 新建流程
if st.sidebar.button("➕ 新建流程", use_container_width=True, type="primary"):
    st.session_state.editing_pipeline = "new"
    st.rerun()


# ============================================================================
# 主界面
# ============================================================================

# 标题页
if "editing_pipeline" not in st.session_state:
    # 流程概览
    st.title("🔄 ETL 流程管理")

    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("流程总数", f"{{len(st.session_state.etl_pipelines)}}")

    with col2:
        enabled_count = sum(1 for p in st.session_state.etl_pipelines.values() if p.get("enabled", True))
        st.metric("运行中", enabled_count)

    with col3:
        success_runs = sum(1 for r in st.session_state.pipeline_runs if r["status"] == "success")
        st.metric("今日成功", success_runs)

    with col4:
        failed_runs = sum(1 for r in st.session_state.pipeline_runs if r["status"] == "failed")
        st.metric("今日失败", failed_runs)

    st.divider()

    # 流程执行历史
    st.subheader("📊 执行历史")

    # 最近的执行记录
    for run in reversed(st.session_state.pipeline_runs[-10:]):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

            with col1:
                pipeline_name = st.session_state.etl_pipelines.get(run["pipeline"], {}).get("name", run["pipeline"])
                st.markdown(f'**{pipeline_name}**')
                st.caption(f"{{run['start_time'].strftime('%Y-%m-%d %H:%M')}}")

            with col2:
                duration = (run['end_time'] - run['start_time']).total_seconds() / 60
                st.write(f"耗时: **{duration:.1f} 分钟**")

            with col3:
                status_icons = {{"success": "✅", "failed": "❌", "running": "⏳"}}
                st.markdown(f'{status_icons[run["status"]]} **{run["status"].upper()}**')

            with col4:
                if run["status"] == "success":
                    st.metric("处理记录", f"{{run['records_processed']:,}}")
                elif run["status"] == "failed":
                    st.error(run.get("error", "未知错误"))

            st.divider()

else:
    # 流程编辑器
    pipeline_id = st.session_state.editing_pipeline
    is_new = pipeline_id == "new"

    if is_new:
        st.title("➕ 新建 ETL 流程")
        pipeline_data = {{
            "name": "",
            "source": {{"type": "mysql", "config": {}}},
            "transforms": [],
            "target": {{"type": "postgres", "config": {}}},
            "schedule": {{"type": "cron", "expression": "0 2 * * *"}},
            "enabled": True
        }}
    else:
        st.title(f'⚙️ 编辑: {st.session_state.etl_pipelines[pipeline_id]["name"]}')
        pipeline_data = st.session_state.etl_pipelines[pipeline_id]

    # 基本信息
    st.subheader("📝 基本信息")

    col1, col2 = st.columns(2)

    with col1:
        pipeline_name = st.text_input("流程名称", value=pipeline_data.get("name", ""))

    with col2:
        enabled = st.checkbox("启用流程", value=pipeline_data.get("enabled", True))

    st.divider()

    # 数据源配置
    st.subheader("📥 数据源")

    col1, col2 = st.columns(2)

    with col1:
        source_type = st.selectbox(
            "数据源类型",
            ["MySQL", "PostgreSQL", "API", "CSV", "Excel"],
            index=0
        )

    with col2:
        if source_type in ["MySQL", "PostgreSQL"]:
            st.text_input("主机地址", value="192.168.1.100")
            st.text_input("端口", value="3306" if source_type == "MySQL" else "5432")
            st.text_input("数据库", value="sales")
            st.text_input("用户名", value="admin")
            st.text_input("密码", type="password")
        elif source_type == "API":
            st.text_input("API 端点", value="https://api.example.com/data")
            st.text_input("API Key", type="password")
        else:
            uploaded_file = st.file_uploader("上传文件", type=["csv", "xlsx"])

    st.divider()

    # 转换规则
    st.subheader("🔧 转换规则")

    transforms = pipeline_data.get("transforms", [])

    if st.button("➕ 添加转换步骤"):
        transforms.append({{"type": "filter", "config": {}}})
        st.rerun()

    for i, transform in enumerate(transforms):
        with st.expander(f'步骤 {i+1}: {transform["type"]}'):
            transform_type = st.selectbox(
                "转换类型",
                ["filter", "aggregate", "join", "split", "derive"],
                index=["filter", "aggregate", "join", "split", "derive"].index(transform["type"]),
                key=f'transform_type_{i}'
            )

            if transform_type == "filter":
                st.text_input("字段名", key=f'filter_field_{i}')
                st.selectbox("条件", ["=", "!=", ">", "<", "contains"], key=f'filter_cond_{i}')
                st.text_input("值", key=f'filter_value_{i}')

            elif transform_type == "aggregate":
                st.text_input("分组字段", key=f'agg_group_{i}')
                st.text_input("聚合字段（逗号分隔）", key=f'agg_fields_{i}')

            if st.button(f'删除此步骤', key=f'delete_transform_{i}'):
                transforms.pop(i)
                st.rerun()

    st.divider()

    # 目标配置
    st.subheader("📤 数据目标")

    col1, col2 = st.columns(2)

    with col1:
        target_type = st.selectbox(
            "目标类型",
            ["PostgreSQL", "MySQL", "API", "CSV", "Excel"]
        )

    with col2:
        if target_type in ["PostgreSQL", "MySQL"]:
            st.text_input("主机地址", value="192.168.1.200")
            st.text_input("数据库", value="dw")
            st.text_input("表名", value="fact_sales")
        else:
            st.text_input("文件路径", value="/data/exports/sales.csv")

    st.divider()

    # 调度配置
    st.subheader("⏰ 调度设置")

    col1, col2 = st.columns(2)

    with col1:
        schedule_type = st.selectbox(
            "调度类型",
            ["Cron 表达式", "间隔执行", "手动执行"]
        )

    with col2:
        if schedule_type == "Cron 表达式":
            cron_expr = st.text_input("Cron 表达式", value="0 2 * * *")
            st.caption("示例: 0 2 * * * 表示每天凌晨2点执行")
        elif schedule_type == "间隔执行":
            interval = st.number_input("间隔（分钟）", value=60)
        else:
            st.info("仅手动执行，不自动调度")

    st.divider()

    # 保存按钮
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 保存流程", use_container_width=True, type="primary"):
            if is_new:
                new_id = f"pipeline_{len(st.session_state.etl_pipelines) + 1}"
                st.session_state.etl_pipelines[new_id] = {{
                    "name": pipeline_name,
                    "source": pipeline_data["source"],
                    "transforms": transforms,
                    "target": pipeline_data["target"],
                    "schedule": {{"type": schedule_type}},
                    "enabled": enabled
                }}
                st.success(f"流程 '{pipeline_name}' 已创建")
            else:
                st.session_state.etl_pipelines[pipeline_id]["name"] = pipeline_name
                st.session_state.etl_pipelines[pipeline_id]["enabled"] = enabled
                st.success(f"流程 '{pipeline_name}' 已更新")

            del st.session_state.editing_pipeline
            st.rerun()

    with col2:
        if st.button("▶️ 测试运行", use_container_width=True):
            st.info("正在测试运行...")
            with st.spinner("执行中..."):
                import time
                time.sleep(2)
            st.success("测试运行成功！处理了 1,542 条记录")

    with col3:
        if st.button("❌ 取消", use_container_width=True):
            del st.session_state.editing_pipeline
            st.rerun()
'''


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "ChartType",
    "AggregationType",
    "ExportFormat",
    "AlertSeverity",
    "PipelineStatus",
    # 数据结构
    "MetricDefinition",
    "DimensionDefinition",
    "ChartDefinition",
    "AlertRule",
    "PipelineStep",
    # 模板类
    "BIDashboard",
    "ReportBuilder",
    "DataExplorer",
    "AlertMonitor",
    "ETLPipeline",
]
