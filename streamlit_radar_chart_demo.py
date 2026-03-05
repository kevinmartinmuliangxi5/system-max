"""
Plotly雷达图在Streamlit中的完整实现
包含：五维能力雷达图、中文支持、颜色主题、响应式布局
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Optional

# ============================================
# 页面配置
# ============================================
st.set_page_config(
    page_title="Plotly雷达图最佳实践",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 1. 中文字体配置
# ============================================
def configure_chinese_font():
    """
    配置Plotly中文字体

    Plotly在Web端显示中文的关键配置：
    - 使用系统自带的中文字体
    - Web浏览器优先使用系统字体
    """
    return {
        'font': {
            'family': '"Microsoft YaHei", "SimHei", "PingFang SC", "Heiti SC", sans-serif',
            'size': 14,
            'color': '#2a3f5f'
        },
        'title_font': {
            'family': '"Microsoft YaHei", "SimHei", "PingFang SC", sans-serif',
            'size': 20,
            'color': '#1f1f1f'
        },
        'legend_font': {
            'family': '"Microsoft YaHei", "SimHei", "PingFang SC", sans-serif',
            'size': 12
        }
    }

# ============================================
# 2. 颜色主题配置
# ============================================
COLOR_THEMES = {
    'professional': {
        'name': '专业蓝',
        'colors': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
        'bg_color': '#f8f9fa',
        'grid_color': '#e0e0e0'
    },
    'vibrant': {
        'name': '活力彩虹',
        'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
        'bg_color': '#ffffff',
        'grid_color': '#dfe6e9'
    },
    'dark': {
        'name': '深色主题',
        'colors': ['#00d4ff', '#00ff9d', '#00ff00', '#ffeb3b', '#ff00ff', '#ff0000'],
        'bg_color': '#1e1e1e',
        'grid_color': '#333333'
    },
    'pastel': {
        'name': '柔和粉彩',
        'colors': ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAFFC9', '#BAE7FF'],
        'bg_color': '#fafafa',
        'grid_color': '#eeeeee'
    },
    'nature': {
        'name': '自然绿色',
        'colors': ['#2d6a4f', '#388d3c', '#57a773', '#76c046', '#95d55b', '#c4e953'],
        'bg_color': '#f0f9f0',
        'grid_color': '#d0e8d8'
    }
}

# Plotly内置颜色序列参考
PLOTLY_COLOR_SEQUENCES = {
    'Viridis': px.colors.sequential.Viridis,
    'Plasma': px.colors.sequential.Plasma,
    'Inferno': px.colors.sequential.Inferno,
    'Magma': px.colors.sequential.Magma,
    'Cividis': px.colors.sequential.Cividis,
    'Aggrnyl': px.colors.diverging.Aggrnyl,
    'Balance': px.colors.diverging.Balance,
    'Delta': px.colors.diverging.Delta,
    'Jet': px.colors.sequential.Jet,
    'Turbo': px.colors.sequential.Turbo
}

def get_color_with_opacity(color: str, opacity: float = 0.8) -> str:
    """为颜色添加透明度"""
    if color.startswith('#'):
        return color[:-1] + f"{int(color[-1], 16):02x}{opacity:02x}"
    return color

# ============================================
# 3. 雷达图核心函数
# ============================================
def create_radar_chart(
    categories: List[str],
    values: List[float],
    name: str = "数据",
    fill_color: Optional[str] = None,
    line_color: Optional[str] = None,
    fill_opacity: float = 0.3,
    line_width: int = 2,
    show_markers: bool = True,
    marker_size: int = 8
) -> go.Scatterpolar:
    """
    创建单个雷达图轨迹

    参数:
        categories: 维度标签列表
        values: 对应数值列表
        name: 数据系列名称
        fill_color: 填充颜色
        line_color: 线条颜色
        fill_opacity: 填充透明度
        line_width: 线条宽度
        show_markers: 是否显示数据点
        marker_size: 数据点大小
    """
    # 闭合多边形
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    trace = go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        name=name,
        fill='toself',
        mode='lines+markers' if show_markers else 'lines',
        line=dict(
            color=line_color or '#1f77b4',
            width=line_width
        ),
        fillcolor=get_color_with_opacity(fill_color or '#1f77b4', fill_opacity) if fill_color else None,
        marker=dict(
            size=marker_size,
            color=line_color or '#1f77b4'
        ),
        hovertemplate='<b>%{theta}</b><br>得分: <b>%{r}</b><extra></extra>'
    )

    return trace

def create_radar_figure(
    data: Dict[str, List[float]],
    categories: List[str],
    title: str = "雷达图",
    theme: str = 'professional',
    value_range: tuple = (0, 100),
    show_grid: bool = True,
    start_angle: float = 90
) -> go.Figure:
    """
    创建完整的雷达图

    参数:
        data: 字典，key为系列名称，value为数值列表
        categories: 维度标签
        title: 图表标题
        theme: 颜色主题名称
        value_range: 数值范围
        show_grid: 是否显示网格
        start_angle: 起始角度
    """
    theme_config = COLOR_THEMES[theme]
    colors = theme_config['colors']
    font_config = configure_chinese_font()

    fig = go.Figure()

    # 添加数据轨迹
    for idx, (series_name, values) in enumerate(data.items()):
        color = colors[idx % len(colors)]
        fig.add_trace(create_radar_chart(
            categories=categories,
            values=values,
            name=series_name,
            fill_color=color,
            line_color=color
        ))

    # 更新布局和极坐标配置
    fig.update_layout(
        title=dict(
            text=title,
            font=font_config['title_font'],
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        font=font_config['font'],
        paper_bgcolor=theme_config['bg_color'],
        plot_bgcolor=theme_config['bg_color'],
        showlegend=True,
        legend=dict(
            font=font_config['legend_font'],
            orientation='h',
            yanchor='bottom',
            xanchor='center',
            y=-0.15,
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#ccc',
            borderwidth=1
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=value_range,
                gridcolor=theme_config['grid_color'],
                gridwidth=1,
                tickfont=font_config['font'],
                ticks='outside',
                tickcolor='#666',
                ticklen=8,
                showline=True,
                linecolor=theme_config['grid_color'],
                linewidth=1
            ),
            angularaxis=dict(
                visible=True,
                gridcolor=theme_config['grid_color'],
                gridwidth=1,
                tickfont=font_config['font'],
                ticks='outside',
                tickcolor='#666',
                ticklen=8,
                rotation=start_angle,
                direction='clockwise',
                showline=True,
                linecolor=theme_config['grid_color'],
                linewidth=1
            ),
            bgcolor=theme_config['bg_color'],
            hole=0.3  # 中心空洞大小
        ),
        margin=dict(l=80, r=80, t=80, b=80, pad=10),
        height=500,
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#ccc',
            font_size=12
        )
    )

    return fig

# ============================================
# 4. 五维能力数据示例
# ============================================
def get_sample_ability_data() -> Dict[str, List[float]]:
    """
    生成五维能力评估数据

    五维能力通常包括：
    1. 技术能力
    2. 沟通能力
    3. 领导力
    4. 创新能力
    5. 学习能力
    """
    return {
        '张三': [85, 78, 72, 88, 82],
        '李四': [75, 85, 80, 70, 90],
        '王五': [90, 82, 78, 85, 75],
        '赵六': [80, 88, 85, 78, 82],
        '平均水准': [75, 75, 75, 75, 75]
    }

def get_five_dimensions() -> List[str]:
    """返回五维能力标准维度"""
    return [
        '技术能力',
        '沟通能力',
        '领导力',
        '创新能力',
        '学习能力'
    ]

# ============================================
# 5. 响应式布局配置
# ============================================
def create_responsive_layout(fig: go.Figure, use_container_width: bool = True) -> None:
    """
    配置响应式布局

    Streamlit响应式要点：
    - use_container_width=True：图表宽度自适应容器
    - 使用st.columns：多列布局
    - 设置合适的height：固定高度避免内容跳动
    """
    st.plotly_chart(
        fig,
        use_container_width=use_container_width,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'radar_chart',
                'height': 500,
                'width': 800,
                'scale': 2
            }
        },
        height=500,
        width=None
    )

def responsive_columns(columns: List) -> tuple:
    """
    创建响应式列布局

    参数:
        columns: 列宽比例列表，如[1, 2, 1]表示三列比例1:2:1

    返回:
        st.columns对象
    """
    return st.columns(columns)

# ============================================
# 6. Streamlit主应用
# ============================================
def main():
    """主应用函数"""

    # 标题
    st.title("📊 Plotly雷达图最佳实践")
    st.markdown("---")

    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置选项")

        # 主题选择
        theme_name = st.selectbox(
            "🎨 颜色主题",
            options=list(COLOR_THEMES.keys()),
            format_func=lambda x: COLOR_THEMES[x]['name'],
            index=0
        )

        st.markdown(f"**当前主题**: {COLOR_THEMES[theme_name]['name']}")

        # 数值范围
        col1, col2 = st.columns(2)
        with col1:
            min_val = st.number_input("最小值", value=0, min_value=0, max_value=100)
        with col2:
            max_val = st.number_input("最大值", value=100, min_value=0, max_value=200)

        # 其他配置
        show_grid = st.checkbox("显示网格", value=True)
        start_angle = st.slider("起始角度", min_value=0, max_value=360, value=90, step=15)

        st.markdown("---")

        # 预设数据选择
        st.subheader("📋 数据选项")
        use_sample = st.checkbox("使用示例数据", value=True)

        if not use_sample:
            st.info("💡 上传自定义数据功能可在此扩展")

    # 主内容区
    # ==================

    # 获取数据
    categories = get_five_dimensions()
    data = get_sample_ability_data()

    # 数据编辑器（可选）
    if st.sidebar.checkbox("启用数据编辑", value=False):
        st.subheader("📝 编辑数据")
        st.write("可以调整各维度的得分：")

        edited_data = {}
        for person in data.keys():
            if person != '平均水准':
                with st.expander(f"编辑 {person} 的数据", expanded=False):
                    values = []
                    for i, cat in enumerate(categories):
                        val = st.slider(
                            f"{cat}得分",
                            min_value=min_val,
                            max_value=max_val,
                            value=data[person][i],
                            key=f"{person}_{i}"
                        )
                        values.append(val)
                    edited_data[person] = values

        if edited_data:
            data = edited_data

    # ==================
    # 创建选项卡
    # ==================

    tab1, tab2, tab3 = st.tabs(["📈 单人雷达图", "👥 多人对比", "🎨 主题预览"])

    # Tab 1: 单人雷达图
    with tab1:
        st.subheader("个人能力雷达图")

        person = st.selectbox("选择人员", options=list(data.keys())[:-1], index=0)

        single_data = {person: data[person]}

        fig = create_radar_figure(
            data=single_data,
            categories=categories,
            title=f"{person} - 五维能力评估",
            theme=theme_name,
            value_range=(min_val, max_val),
            show_grid=show_grid,
            start_angle=start_angle
        )

        create_responsive_layout(fig)

        # 显示数值表格
        with st.expander("📋 查看数据"):
            df = pd.DataFrame({
                '维度': categories,
                '得分': data[person]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

    # Tab 2: 多人对比
    with tab2:
        st.subheader("多人能力对比雷达图")

        # 选择要对比的人员
        selected_people = st.multiselect(
            "选择对比人员",
            options=list(data.keys()),
            default=list(data.keys())[:3]
        )

        if len(selected_people) >= 1:
            compare_data = {k: v for k, v in data.items() if k in selected_people}

            fig = create_radar_figure(
                data=compare_data,
                categories=categories,
                title=f"能力对比 - {', '.join(selected_people)}",
                theme=theme_name,
                value_range=(min_val, max_val),
                show_grid=show_grid,
                start_angle=start_angle
            )

            create_responsive_layout(fig)

            # 对比表格
            with st.expander("📊 数据对比表"):
                compare_df = pd.DataFrame(compare_data, index=categories).T
                st.dataframe(compare_df, use_container_width=True)
        else:
            st.warning("⚠️ 请至少选择一个人员")

    # Tab 3: 主题预览
    with tab3:
        st.subheader("颜色主题预览")

        # 创建所有主题的预览
        preview_data = {'示例': [80, 75, 90, 85, 70]}

        cols = responsive_columns([1, 1, 1])

        theme_keys = list(COLOR_THEMES.keys())[:3]
        for i, theme in enumerate(theme_keys):
            with cols[i]:
                st.markdown(f"**{COLOR_THEMES[theme]['name']}**")

                fig = create_radar_figure(
                    data=preview_data,
                    categories=categories,
                    title="",
                    theme=theme,
                    value_range=(min_val, max_val),
                    show_grid=show_grid
                )

                # 减小高度用于预览
                fig.update_layout(height=300, margin=dict(l=40, r=40, t=40, b=40, pad=5))

                create_responsive_layout(fig)

    # ==================
    # 高级功能
    # ==================

    st.markdown("---")
    st.subheader("🔧 高级功能")

    with st.expander("Plotly配置说明", expanded=False):
        st.markdown("""
        ### 中文字体配置
        Plotly在Web环境中显示中文需要配置字体，推荐使用以下字体栈：
        ```python
        font_family = '"Microsoft YaHei", "SimHei", "PingFang SC", sans-serif'
        ```

        ### 颜色主题
        - **专业蓝**: 适合商务场景
        - **活力彩虹**: 适合创意展示
        - **深色主题**: 适合暗色环境
        - **柔和粉彩**: 适合温馨风格
        - **自然绿色**: 适合环保主题

        ### 响应式布局
        - `use_container_width=True`: 自适应容器宽度
        - `st.columns()`: 响应式多列布局
        - 固定`height`: 避免布局跳动
        """)

    with st.expander("代码实现要点", expanded=False):
        st.markdown("""
        ### 1. 雷达图核心配置
        ```python
        go.Scatterpolar(
            r=values,           # 数值（半径方向）
            theta=categories,    # 类别（角度方向）
            fill='toself',       # 填充到自身
            line=dict(width=2),   # 线条宽度
            marker=dict(size=8)    # 数据点大小
        )
        ```

        ### 2. 极坐标布局
        ```python
        fig.update_layout(
            polar=dict(
                radialaxis=dict(range=[0, 100]),  # 径向轴范围
                angularaxis=dict(rotation=90)        # 角向轴旋转
            )
        )
        ```

        ### 3. Streamlit集成
        ```python
        st.plotly_chart(
            fig,
            use_container_width=True,  # 响应式宽度
            theme="streamlit"           # 使用Streamlit主题
        )
        ```
        """)

    # ==================
    # 使用说明
    # ==================

    st.markdown("---")
    with st.expander("📖 使用指南", expanded=False):
        st.markdown("""
        ### 最佳实践

        1. **数据准备**
           - 确保所有维度在同一数值范围
           - 考虑数据标准化（Min-Max或Z-score）
           - 闭合多边形（首尾数据重复）

        2. **视觉设计**
           - 不要超过5-7个维度（过于复杂）
           - 使用透明填充避免遮挡
           - 选择对比鲜明的颜色

        3. **交互优化**
           - 设置合理的hover信息
           - 添加图例便于识别
           - 使用动画展示趋势

        4. **性能优化**
           - 限制数据系列数量（建议<5个）
           - 使用theme参数快速应用样式
           - 避免过度自定义导致性能下降
        """)

if __name__ == "__main__":
    main()
