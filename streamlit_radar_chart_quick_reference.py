"""
Plotly + Streamlit 雷达图快速参考
精简版代码示例，方便直接复制使用
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ============================================
# 基础雷达图 - Plotly Express
# ============================================

def basic_rar_chart_px():
    """最简单的雷达图示例"""

    # 数据
    categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']

    # 单人数据
    fig = px.line_polar(
        r=[85, 78, 72, 88, 82],
        theta=categories,
        line_close=True,
        title="五维能力评估",
        labels=categories
    )
    fig.update_traces(fill='toself')

    # 中文配置
    fig.update_layout(
        font=dict(family='"Microsoft YaHei", "SimHei", sans-serif')
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 多人对比雷达图 - Graph Objects
# ============================================

def multi_compare_radar():
    """多人对比雷达图"""

    categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']

    # 多人数据
    data = {
        '张三': [85, 78, 72, 88, 82],
        '李四': [75, 85, 80, 70, 90],
        '王五': [90, 82, 78, 85, 75]
    }

    fig = go.Figure()

    # 颜色方案
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for idx, (name, values) in enumerate(data.items()):
        # 闭合多边形（首尾数据重复）
        values_closed = values + [values[0]]
        categories_closed = categories + [categories[0]]

        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            name=name,
            fill='toself',
            line=dict(color=colors[idx], width=2),
            fillcolor=f"rgba({int(colors[idx][1:3], 16):02x}, {int(colors[idx][3:5], 16):02x}, {int(colors[idx][5:7], 16):02x}, 0.3)",
            marker=dict(size=6, color=colors[idx])
        ))

    # 配置
    fig.update_layout(
        title=dict(
            text="五维能力对比",
            font=dict(family='"Microsoft YaHei", "SimHei", sans-serif', size=18)
        ),
        font=dict(family='"Microsoft YaHei", "SimHei", sans-serif'),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#e0e0e0'
            ),
            angularaxis=dict(
                gridcolor='#e0e0e0',
                tickfont=dict(size=11)
            )
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            x=0.5,
            y=-0.1,
            font=dict(size=12)
        ),
        margin=dict(l=60, r=60, t=60, b=60, pad=10),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 带参考线的雷达图
# ============================================

def radar_with_reference():
    """带平均参考线的雷达图"""

    categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']

    fig = go.Figure()

    # 个人数据
    fig.add_trace(go.Scatterpolar(
        r=[85, 78, 72, 88, 82] + [85],
        theta=categories + [categories[0]],
        name='个人得分',
        fill='toself',
        fillcolor='rgba(31, 119, 180, 0.3)',
        line=dict(color='#1f77b4', width=2)
    ))

    # 参考线（虚线）
    fig.add_trace(go.Scatterpolar(
        r=[75, 75, 75, 75, 75] + [75],
        theta=categories + [categories[0]],
        name='团队平均',
        fill='none',
        line=dict(color='red', width=2, dash='dash')
    ))

    fig.update_layout(
        title=dict(text="能力评估 vs 团队平均", font=dict(size=18)),
        font=dict(family='"Microsoft YaHei", "SimHei"'),
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 响应式布局示例
# ============================================

def responsive_demo():
    """响应式布局演示"""

    st.title("响应式雷达图布局")

    # 使用columns创建响应式布局
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.metric("总人数", "5", "人")

    with col2:
        # 主图表区域
        categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']

        fig = go.Figure()

        for person, color in [('张三', '#1f77b4'), ('李四', '#ff7f0e')]:
            values = [85, 78, 72, 88, 82]
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                name=person,
                fill='toself',
                line=dict(color=color, width=2),
                fillcolor=f"rgba({int(color[1:3], 16):02x}, {int(color[3:5], 16):02x}, {int(color[5:7], 16):02x}, 0.3)"
            ))

        fig.update_layout(
            title=None,
            font=dict(family='"Microsoft YaHei", "SimHei"'),
            polar=dict(radialaxis=dict(range=[0, 100])),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.info("""
        **提示**:
        - 左侧：KPI指标
        - 中间：雷达图
        - 右侧：其他信息

        `use_container_width=True` 确保图表自适应容器宽度
        """)

# ============================================
# 主题应用示例
# ============================================

def theme_demo():
    """使用Plotly内置主题"""

    categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']
    values = [85, 78, 72, 88, 82]

    # 创建基础图
    fig = px.line_polar(
        r=values,
        theta=categories,
        line_close=True
    )
    fig.update_traces(fill='toself')

    # 应用不同主题
    themes = {
        'plotly': '默认Plotly',
        'plotly_white': '白色简洁',
        'plotly_dark': '深色主题',
        'ggplot2': 'GGplot风格',
        'seaborn': 'Seaborn风格',
        'simple_white': '极简白色'
    }

    selected_theme = st.selectbox("选择主题", list(themes.keys()))

    fig.update_layout(
        template=selected_theme,
        font=dict(family='"Microsoft YaHei", "SimHei"'),
        title=dict(text=f"{themes[selected_theme]} - 五维能力评估")
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 主菜单
# ============================================

st.set_page_config(page_title="雷达图快速参考", layout="wide")

st.sidebar.title("📊 雷达图示例")

demo_type = st.sidebar.radio(
    "选择示例",
    ["基础雷达图(PX)", "多人对比(GO)", "参考线图", "响应式布局", "主题演示"]
)

if demo_type == "基础雷达图(PX)":
    basic_rar_chart_px()
elif demo_type == "多人对比(GO)":
    multi_compare_radar()
elif demo_type == "参考线图":
    radar_with_reference()
elif demo_type == "响应式布局":
    responsive_demo()
elif demo_type == "主题演示":
    theme_demo()
