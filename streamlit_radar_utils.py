"""
Streamlit + Plotly 雷达图工具模块
可复用的雷达图组件和工具函数
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# ============================================
# 数据类定义
# ============================================

@dataclass
class RadarData:
    """雷达图数据容器"""
    name: str
    values: List[float]
    category: Optional[str] = None

@dataclass
class RadarChartConfig:
    """雷达图配置"""
    title: str = "雷达图"
    categories: List[str] = None
    value_range: Tuple[float, float] = (0, 100)
    show_grid: bool = True
    show_legend: bool = True
    start_angle: float = 90
    theme: str = 'default'
    height: int = 500
    fill_opacity: float = 0.3
    line_width: int = 2
    marker_size: int = 8
    hole: float = 0.3  # 中心空洞比例

# ============================================
# 颜色配置
# ============================================

class ColorThemes:
    """颜色主题类"""

    PROFESSIONAL = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    VIBRANT = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    PASTEL = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE7FF']
    NATURE = ['#2d6a4f', '#388d3c', '#57a773', '#76c046', '#95d55b']
    WARM = ['#ff0000', '#ff4500', '#ff8c00', '#ffd700', '#ffff00']
    COOL = ['#0000ff', '#0000ff', '#00bfff', '#00ffff', '#7fffd4']

    @staticmethod
    def get_with_opacity(color: str, opacity: float) -> str:
        """添加透明度到颜色"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            return f'rgba({r}, {g}, {b}, {opacity})'
        return color

# ============================================
# 字体配置
# ============================================

class FontConfig:
    """中文字体配置类"""

    # Windows系统字体
    YAHEI = '"Microsoft YaHei"'
    SIMHEI = '"SimHei"'
    KAITI = '"KaiTi"'

    # 通用字体
    SANS_SERIF = 'sans-serif'
    SYSTEM = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif'

    @staticmethod
    def get_chinese_font_config(size: int = 14) -> Dict:
        """获取中文字体配置"""
        return {
            'family': f'{FontConfig.YAHEI}, {FontConfig.SIMHEI}, {FontConfig.SANS_SERIF}',
            'size': size,
            'color': '#2a3f5f'
        }

    @staticmethod
    def get_title_font(size: int = 20) -> Dict:
        """获取标题字体配置"""
        return {
            'family': f'{FontConfig.YAHEI}, {FontConfig.SIMHEI}, {FontConfig.SANS_SERIF}',
            'size': size,
            'color': '#1f1f1f'
        }

# ============================================
# 雷达图生成器
# ============================================

class RadarChartBuilder:
    """雷达图构建器"""

    def __init__(self, config: RadarChartConfig):
        self.config = config
        self.fig = go.Figure()
        self.font = FontConfig.get_chinese_font_config()

    def add_trace(
        self,
        data: RadarData,
        color: str,
        show_marker: bool = True
    ) -> 'RadarChartBuilder':
        """添加单个数据轨迹"""

        # 闭合多边形
        categories = self.config.categories or []
        values_closed = data.values + [data.values[0]]
        categories_closed = categories + [categories[0]]

        self.fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            name=data.name,
            fill='toself',
            mode='lines+markers' if show_marker else 'lines',
            line=dict(
                color=color,
                width=self.config.line_width
            ),
            fillcolor=ColorThemes.get_with_opacity(
                color,
                self.config.fill_opacity
            ),
            marker=dict(
                size=self.config.marker_size if show_marker else 0,
                color=color
            ),
            hovertemplate='<b>%{theta}</b><br>得分: <b>%{r}</b>'
        ))

        return self

    def add_reference_line(
        self,
        values: List[float],
        name: str = "参考线",
        color: str = 'red',
        line_style: str = 'dash'
    ) -> 'RadarChartBuilder':
        """添加参考线"""

        categories = self.config.categories or []
        values_closed = values + [values[0]]
        categories_closed = categories + [categories[0]]

        self.fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            name=name,
            fill='none',
            line=dict(
                color=color,
                width=self.config.line_width,
                dash=line_style
            ),
            marker=dict(size=0),
            hovertemplate='<b>%{theta}</b><br>参考: <b>%{r}</b>'
        ))

        return self

    def build(self) -> go.Figure:
        """构建最终图表"""

        # 应用主题颜色
        theme_colors = self._get_theme_colors()

        # 更新布局
        self.fig.update_layout(
            title=dict(
                text=self.config.title,
                font=FontConfig.get_title_font()
            ),
            font=self.font,
            paper_bgcolor=self._get_bg_color(),
            plot_bgcolor=self._get_bg_color(),
            showlegend=self.config.show_legend,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                x=0.5,
                y=-0.15,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#ccc',
                borderwidth=1,
                font=self.font
            ),
            polar=dict(
                radialaxis=dict(
                    visible=self.config.show_grid,
                    range=self.config.value_range,
                    gridcolor=self._get_grid_color(),
                    gridwidth=1,
                    tickfont=self.font,
                    ticks='outside',
                    tickcolor='#666',
                    ticklen=8,
                    showline=True,
                    linecolor=self._get_grid_color(),
                    linewidth=1
                ),
                angularaxis=dict(
                    visible=self.config.show_grid,
                    gridcolor=self._get_grid_color(),
                    gridwidth=1,
                    tickfont=self.font,
                    rotation=self.config.start_angle,
                    direction='clockwise',
                    showline=True,
                    linecolor=self._get_grid_color(),
                    linewidth=1
                ),
                bgcolor=self._get_bg_color(),
                hole=self.config.hole
            ),
            margin=dict(l=80, r=80, t=80, b=80, pad=10),
            height=self.config.height,
            hovermode='closest',
            hoverlabel=dict(
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#ccc',
                font_size=12
            ),
            template=self.config.theme if self.config.theme != 'default' else None
        )

        return self.fig

    def _get_theme_colors(self) -> List[str]:
        """获取主题颜色"""
        theme_map = {
            'professional': ColorThemes.PROFESSIONAL,
            'vibrant': ColorThemes.VIBRANT,
            'pastel': ColorThemes.PASTEL,
            'nature': ColorThemes.NATURE,
            'warm': ColorThemes.WARM,
            'cool': ColorThemes.COOL
        }
        return theme_map.get(self.config.theme, ColorThemes.PROFESSIONAL)

    def _get_bg_color(self) -> str:
        """获取背景颜色"""
        if self.config.theme == 'dark':
            return '#1e1e1e'
        return '#ffffff'

    def _get_grid_color(self) -> str:
        """获取网格颜色"""
        if self.config.theme == 'dark':
            return '#333333'
        return '#e0e0e0'

# ============================================
# 高级雷达图生成器
# ============================================

class AdvancedRadarChart(RadarChartBuilder):
    """高级雷达图生成器，支持更多自定义"""

    def add_area_ranges(
        self,
        ranges: List[Tuple[float, float]],
        names: List[str],
        colors: List[str]
    ) -> 'AdvancedRadarChart':
        """
        添加区域范围

        参数:
            ranges: 每个维度的(min, max)范围列表
            names: 区域名称列表
            colors: 区域颜色列表
        """

        categories = self.config.categories or []

        for (min_val, max_val), name, color in zip(ranges, names, colors):
            # 创建闭合区域
            theta = categories + [categories[0]]
            r = [min_val, max_val, max_val, min_val, min_val]

            self.fig.add_trace(go.Scatterpolar(
                r=r,
                theta=theta,
                name=name,
                fill='toself',
                fillcolor=ColorThemes.get_with_opacity(color, 0.15),
                line=dict(color=color, width=1),
                marker=dict(size=0),
                showlegend=True
            ))

        return self

    def add_average_trace(
        self,
        all_data: List[List[float]]
    ) -> 'AdvancedRadarChart':
        """添加平均值线"""

        if not all_data:
            return self

        # 计算每个维度的平均值
        categories = self.config.categories or []
        avg_values = [sum(vals) / len(vals) for vals in zip(*all_data)]

        avg_values_closed = avg_values + [avg_values[0]]
        categories_closed = categories + [categories[0]]

        self.fig.add_trace(go.Scatterpolar(
            r=avg_values_closed,
            theta=categories_closed,
            name='平均值',
            fill='toself',
            fillcolor=ColorThemes.get_with_opacity('#808080', 0.2),
            line=dict(color='#808080', width=2, dash='dot'),
            marker=dict(size=6)
        ))

        return self

# ============================================
# Streamlit组件
# ============================================

def radar_chart_component(
    data: Dict[str, List[float]],
    categories: List[str],
    title: str = "雷达图",
    theme: str = 'professional',
    height: int = 500,
    key: str = None
) -> None:
    """
    Streamlit雷达图组件

    参数:
        data: 数据字典 {名称: [数值列表]}
        categories: 维度标签
        title: 图表标题
        theme: 主题名称
        height: 图表高度
        key: 组件唯一标识
    """

    config = RadarChartConfig(
        title=title,
        categories=categories,
        theme=theme,
        height=height
    )

    builder = RadarChartBuilder(config)

    # 添加所有数据轨迹
    colors = builder._get_theme_colors()
    for idx, (name, values) in enumerate(data.items()):
        builder.add_trace(
            RadarData(name=name, values=values),
            color=colors[idx % len(colors)]
        )

    fig = builder.build()

    st.plotly_chart(
        fig,
        use_container_width=True,
        key=key,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': title.replace(' ', '_'),
                'height': height,
                'scale': 2
            }
        }
    )

def comparison_radar_component(
    data: pd.DataFrame,
    group_col: str,
    value_cols: List[str],
    title: str = "对比雷达图",
    theme: str = 'professional'
) -> None:
    """
    多系列对比雷达图组件

    参数:
        data: DataFrame数据
        group_col: 分组列名
        value_cols: 数值列名列表
        title: 图表标题
        theme: 主题
    """

    categories = value_cols
    groups = data[group_col].unique()

    config = RadarChartConfig(
        title=title,
        categories=categories,
        theme=theme
    )

    builder = RadarChartBuilder(config)
    colors = builder._get_theme_colors()

    for idx, group in enumerate(groups):
        group_data = data[data[group_col] == group]
        values = [group_data[col].iloc[0] for col in value_cols]

        builder.add_trace(
            RadarData(name=str(group), values=values),
            color=colors[idx % len(colors)]
        )

    fig = builder.build()
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 辅助函数
# ============================================

@st.cache_data(ttl=3600)
def get_demo_data() -> Dict[str, List[float]]:
    """获取演示数据"""
    return {
        '张三': [85, 78, 72, 88, 82],
        '李四': [75, 85, 80, 70, 90],
        '王五': [90, 82, 78, 85, 75],
        '赵六': [80, 88, 85, 78, 82],
        '平均水准': [75, 75, 75, 75, 75]
    }

@st.cache_data(ttl=3600)
def get_five_dimensions() -> List[str]:
    """获取五维能力维度"""
    return [
        '技术能力',
        '沟通能力',
        '领导力',
        '创新能力',
        '学习能力'
    ]

def normalize_data(
    data: List[float],
    method: str = 'minmax'
) -> List[float]:
    """
    数据标准化

    参数:
        data: 原始数据
        method: 'minmax' 或 'zscore'

    返回: 标准化后的数据
    """
    if method == 'minmax':
        min_val = min(data)
        max_val = max(data)
        if max_val == min_val:
            return [0.5] * len(data)
        return [(x - min_val) / (max_val - min_val) * 100 for x in data]
    elif method == 'zscore':
        import statistics
        mean = statistics.mean(data)
        stdev = statistics.stdev(data) if len(data) > 1 else 1
        if stdev == 0:
            return [0] * len(data)
        return [(x - mean) / stdev for x in data]
    else:
        return data

# ============================================
# 导出函数
# ============================================

def export_to_csv(
    data: Dict[str, List[float]],
    categories: List[str],
    filename: str = "radar_data.csv"
) -> bytes:
    """导出数据为CSV"""

    df = pd.DataFrame(data, index=categories).T
    return df.to_csv(index=True).encode('utf-8')

def export_fig_to_html(
    fig: go.Figure,
    filename: str = "radar_chart.html"
) -> str:
    """导出图表为HTML"""

    return fig.to_html(
        include_plotlyjs=True,
        config={'displayModeBar': False, 'displaylogo': False}
    )
