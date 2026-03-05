"""
最佳实践雷达图示例
展示Plotly + Streamlit的所有最佳实践
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="雷达图最佳实践",
    layout="wide",
    page_icon="📊"
)

st.title("🎯 Plotly雷达图最佳实践演示")

# ============================================
# 最佳实践 1: 中文配置
# ============================================
st.header("1️⃣ 中文本配置")

st.markdown("""
### 问题
Plotly在Web环境显示中文时，如果没有正确配置字体，会显示为方框 □□□

### 解决方案
使用字体栈，依次尝试多个中文字体：
""")

with st.expander("查看字体配置代码"):
    st.code("""
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[85, 78, 72, 88, 82],
    theta=['技术能力', '沟通能力', '领导力', '创新能力', '学习能力'],
    fill='toself'
))

# 关键：配置中文字体
fig.update_layout(
    font=dict(
        family='"Microsoft YaHei", "SimHei", "PingFang SC", sans-serif'
    )
)

st.plotly_chart(fig, use_container_width=True)
    """, language="python")

# 演示
categories_ch = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']

fig1 = go.Figure()
fig1.add_trace(go.Scatterpolar(
    r=[85, 78, 72, 88, 82] + [85],
    theta=categories_ch + [categories_ch[0]],
    fill='toself',
    name='正确配置',
    line=dict(color='#1f77b4', width=3)
))

fig1.update_layout(
    title='✓ 中文字体正确显示',
    font=dict(family='"Microsoft YaHei", "SimHei", sans-serif'),
    height=350
)

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    st.info("""
**字体配置要点**：
- Windows: Microsoft YaHei（雅黑）
- Windows: SimHei（黑体）
- 跨平台: PingFang SC

使用字体栈确保至少有一个字体可用！
    """)

# ============================================
# 最佳实践 2: 多边形闭合
# ============================================
st.header("2️⃣ 多边形闭合")

st.markdown("""
### 问题
雷达图需要闭合多边形，否则连线不会形成封闭区域

### 解决方案
将第一个数据点添加到数据末尾
""")

with st.expander("查看闭合代码"):
    st.code("""
# 方法：手动闭合
values = [85, 78, 72, 88, 82]  # 原始数据
values_closed = values + [values[0]]  # 添加第一个值到末尾

categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']
categories_closed = categories + [categories[0]]  # 同样处理类别

fig.add_trace(go.Scatterpolar(
    r=values_closed,
    theta=categories_closed,
    fill='toself'  # 现在可以正确填充
))
    """, language="python")

# 演示
values_open = [85, 78, 72, 88, 82]
values_closed = values_open + [values_open[0]]

fig2 = go.Figure()
fig2.add_trace(go.Scatterpolar(
    r=values_open,
    theta=categories_ch,
    fill='toself',
    name='✗ 未闭合',
    line=dict(color='#ff4444', width=2, dash='dash')
))
fig2.add_trace(go.Scatterpolar(
    r=values_closed,
    theta=categories_ch + [categories_ch[0]],
    fill='toself',
    name='✓ 已闭合',
    line=dict(color='#00cc00', width=3)
))

fig2.update_layout(height=350, showlegend=True)
st.plotly_chart(fig2, use_container_width=True)

# ============================================
# 最佳实践 3: 颜色主题
# ============================================
st.header("3️⃣ 颜色主题")

st.markdown("""
### 推荐颜色方案
- **专业蓝**: #1f77b4, #ff7f0e, #2ca02c
- **活力彩虹**: #FF6B6B, #4ECDC4, #45B7D1
- **自然绿**: #2d6a4f, #388d3c, #57a773
""")

# 使用Plotly内置主题
theme = st.selectbox("选择Plotly主题", ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn"])

fig3 = go.Figure()
fig3.add_trace(go.Scatterpolar(
    r=[85, 78, 72, 88, 82] + [85],
    theta=categories_ch + [categories_ch[0]],
    fill='toself',
    fillcolor='rgba(31, 119, 180, 0.3)',
    line=dict(color='#1f77b4', width=3)
))

fig3.update_layout(
    template=theme,
    title=f'主题: {theme}',
    font=dict(family='"Microsoft YaHei", "SimHei"'),
    height=350
)

st.plotly_chart(fig3, use_container_width=True)

# ============================================
# 最佳实践 4: 响应式布局
# ============================================
st.header("4️⃣ 响应式布局")

st.markdown("""
### Streamlit响应式关键
1. `use_container_width=True` - 图表宽度自适应容器
2. `st.columns()` - 创建响应式列布局
3. 固定`height` - 避免内容跳动
""")

# 响应式演示
col_a, col_b, col_c = st.columns([1, 2, 1])

with col_a:
    st.metric("人员", "5", "人")

with col_b:
    fig4 = go.Figure()
    fig4.add_trace(go.Scatterpolar(
        r=[85, 78, 72, 88, 82] + [85],
        theta=categories_ch + [categories_ch[0]],
        fill='toself',
        line=dict(color='#1f77b4', width=2)
    ))
    fig4.update_layout(
        height=400,
        margin=dict(l=30, r=30, t=30, b=30),
        font=dict(family='"Microsoft YaHei", "SimHei"')
    )
    st.plotly_chart(fig4, use_container_width=True)

with col_c:
    st.success("""
**响应式布局**：
- 左侧：KPI指标卡
- 中间：主图表区（自适应）
- 右侧：操作提示

使用 `st.columns([1, 2, 1])` 实现不同比例列！
    """)

# ============================================
# 最佳实践 5: 多人对比
# ============================================
st.header("5️⃣ 多人对比")

col1, col2 = st.columns(2)

with col1:
    compare_data = {
        '张三': [85, 78, 72, 88, 82],
        '李四': [75, 85, 80, 70, 90],
        '王五': [90, 82, 78, 85, 75]
    }

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    fig5 = go.Figure()

    for idx, (name, scores) in enumerate(compare_data.items()):
        scores_closed = scores + [scores[0]]
        fig5.add_trace(go.Scatterpolar(
            r=scores_closed,
            theta=categories_ch + [categories_ch[0]],
            name=name,
            fill='toself',
            fillcolor=f'rgba({int(colors[idx][1:3], 16):02x}, {int(colors[idx][3:5], 16):02x}, {int(colors[idx][5:7], 16):02x}, 0.3)',
            line=dict(color=colors[idx], width=2)
        ))

    fig5.update_layout(
        title='团队能力对比',
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        font=dict(family='"Microsoft YaHei", "SimHei"'),
        height=400
    )

    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.info("""
**对比图表要点**：
1. 使用不同颜色区分人员
2. 保持统一的数值范围
3. 添加图例便于识别
4. 透明填充避免遮挡
    """)

    # 数据表
    df = pd.DataFrame(compare_data, index=categories_ch).T
    st.dataframe(df, use_container_width=True)

# ============================================
# 最佳实践 6: 性能优化
# ============================================
st.header("6️⃣ 性能优化")

st.markdown("""
### 优化建议

1. **使用@st.cache_data缓存数据**
   ```python
   @st.cache_data(ttl=3600)
   def load_data():
       return pd.read_csv("data.csv")
   ```

2. **限制数据系列数量**
   - 建议不超过5个系列
   - 过多会影响渲染性能

3. **禁用不必要的动画**
   ```python
   fig.update_layout(transition_duration=0)
   ```

4. **使用合适的图表尺寸**
   - 移动端：300-400px
   - 桌面端：500-600px
""")

# ============================================
# 完整示例代码
# ============================================

st.header("📋 完整示例代码")

with st.expander("点击查看完整可运行代码"):
    st.code("""
import streamlit as st
import plotly.graph_objects as go

# 页面配置
st.set_page_config(layout="wide")

# 数据
categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']
data = {
    '张三': [85, 78, 72, 88, 82],
    '李四': [75, 85, 80, 70, 90]
}

# 创建图表
fig = go.Figure()

colors = ['#1f77b4', '#ff7f0e']
for idx, (name, scores) in enumerate(data.items()):
    # 闭合多边形
    scores_closed = scores + [scores[0]]

    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=categories + [categories[0]],
        name=name,
        fill='toself',
        fillcolor=f'rgba({int(colors[idx][1:3], 16):02x}, {int(colors[idx][3:5], 16):02x}, {int(colors[idx][5:7], 16):02x}, 0.3)',
        line=dict(color=colors[idx], width=3)
    ))

# 配置中文和布局
fig.update_layout(
    title='五维能力对比',
    font=dict(
        family='"Microsoft YaHei", "SimHei", sans-serif'
    ),
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    height=500
)

# 显示
st.plotly_chart(fig, use_container_width=True)
    """, language="python")

# ============================================
# 运行说明
# ============================================

st.markdown("---")
st.markdown("""
### 运行方式

```bash
# 方式1：运行完整演示
streamlit run streamlit_radar_chart_best_practices.py

# 方式2：运行快速参考
streamlit run streamlit_radar_chart_quick_reference.py

# 方式3：使用工具模块
python -c "from streamlit_radar_utils import *; print('模块导入成功')"
```

### 文件说明

| 文件 | 说明 |
|------|------|
| `streamlit_radar_chart_demo.py` | 完整功能演示应用 |
| `streamlit_radar_chart_quick_reference.py` | 快速代码参考 |
| `streamlit_radar_utils.py` | 可复用工具模块 |
| `RADAR_CHART_GUIDE.md` | 完整使用文档 |
| `requirements.txt` | 依赖列表 |
| `run_radar_demo.bat` | 快速启动脚本（Windows） |

---

**Created with**: Streamlit + Plotly
**Last Updated**: 2025-02-12
""")

# 底部链接
st.markdown("---")
st.markdown("""
📖 **查看完整文档**: [RADAR_CHART_GUIDE.md](RADAR_CHART_GUIDE.md)

🔧 **使用工具模块**: `from streamlit_radar_utils import *`

""")
