# Plotly在Streamlit中创建雷达图的完整指南

## 目录
1. [雷达图配置](#1-雷达图配置)
2. [五维能力雷达图](#2-五维能力雷达图)
3. [中文本配置](#3-中文本配置)
4. [颜色主题](#4-颜色主题)
5. [响应式布局](#5-响应式布局)
6. [Streamlit集成代码](#6-streamlit集成代码)

---

## 1. 雷达图配置

### 1.1 基础概念

雷达图（Radar Chart），又称蜘蛛图（Spider Chart）或星形图（Star Chart），是一种用于多维数据可视化的图表类型。

### 1.2 Plotly创建雷达图的两种方式

#### 方式一：使用Plotly Express（推荐新手）

```python
import plotly.express as px
import pandas as pd

# 准备数据
df = pd.DataFrame({
    '维度': ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力'],
    '得分': [85, 78, 72, 88, 82]
})

# 创建雷达图
fig = px.line_polar(
    df,
    r='得分',           # 半径方向的数据
    theta='维度',       # 角度方向的类别
    line_close=True,     # 闭合多边形
    title='能力评估'
)

# 添加填充效果
fig.update_traces(fill='toself')
```

#### 方式二：使用Graph Objects（更灵活）

```python
import plotly.graph_objects as go

categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']
values = [85, 78, 72, 88, 82]

# 重要：闭合多边形
values_closed = values + [values[0]]
categories_closed = categories + [categories[0]]

fig = go.Figure(data=go.Scatterpolar(
    r=values_closed,
    theta=categories_closed,
    fill='toself',     # 填充到自身形成闭合区域
    name='能力评估',
    line=dict(
        color='#1f77b4',
        width=2
    ),
    marker=dict(
        size=8
    )
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]  # 设置数值范围
        )
    )
)
```

### 1.3 核心参数说明

| 参数 | 说明 | 推荐值 |
|------|------|----------|
| `r` | 半径方向的数值（决定点到中心的距离） | 数据值 |
| `theta` | 角度方向的类别标签 | 维度名称 |
| `fill` | 填充模式 | `'toself'` 闭合填充，`'none'` 不填充 |
| `line_close` | 是否闭合线条（PX） | `True` |
| `line.width` | 线条宽度 | 2-3 |
| `marker.size` | 数据点大小 | 6-10 |
| `fillcolor` | 填充颜色 | 可带透明度的颜色 |

---

## 2. 五维能力雷达图

### 2.1 常见五维能力定义

| 维度 | 说明 | 英文翻译 |
|------|------|----------|
| 技术能力 | 专业技能、编程能力等 | Technical Skills |
| 沟通能力 | 表达、协调、团队合作 | Communication |
| 领导力 | 决策、管理、激励 | Leadership |
| 创新能力 | 创造思维、问题解决 | Innovation |
| 学习能力 | 学习速度、适应能力 | Learning Ability |

### 2.2 完整五维雷达图代码

```python
import plotly.graph_objects as go
import streamlit as st

# 定义五维能力
categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']

# 个人能力数据
personal_scores = [85, 78, 72, 88, 82]

# 闭合多边形
categories_closed = categories + [categories[0]]
scores_closed = personal_scores + [personal_scores[0]]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=scores_closed,
    theta=categories_closed,
    name='个人能力',
    fill='toself',
    fillcolor='rgba(31, 119, 180, 0.3)',  # 半透明蓝色
    line=dict(
        color='#1f77b4',
        width=3
    ),
    marker=dict(
        size=10,
        color='#1f77b4',
        line=dict(width=2, color='white')
    )
))

fig.update_layout(
    title=dict(
        text='五维能力评估雷达图',
        font=dict(size=20, family='Microsoft YaHei, SimHei')
    ),
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickmode='linear',
            tick0=0,
            dtick=20,
            gridcolor='#e0e0e0',
            gridwidth=1
        ),
        angularaxis=dict(
            visible=True,
            gridcolor='#e0e0e0',
            gridwidth=1,
            categoryarray=categories,
            tickfont=dict(size=12)
        )
    ),
    showlegend=True,
    height=500,
    margin=dict(l=80, r=80, t=80, b=80, pad=10)
)

st.plotly_chart(fig, use_container_width=True)
```

### 2.3 多人对比雷达图

```python
# 多人数据
compare_data = {
    '张三': [85, 78, 72, 88, 82],
    '李四': [75, 85, 80, 70, 90],
    '王五': [90, 82, 78, 85, 75]
}

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

fig = go.Figure()

for idx, (name, scores) in enumerate(compare_data.items()):
    scores_closed = scores + [scores[0]]

    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=categories_closed,
        name=name,
        fill='toself',
        fillcolor=f'rgba({int(colors[idx][1:3], 16):02x}, {int(colors[idx][3:5], 16):02x}, {int(colors[idx][5:7], 16):02x}, 0.3)',
        line=dict(color=colors[idx], width=2)
    ))

fig.update_layout(
    title='团队能力对比',
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    height=500
)
```

---

## 3. 中文本配置

### 3.1 问题说明

Plotly在Web环境中显示中文时，如果系统没有对应的中文字体，会显示为方框（□□□）。

### 3.2 解决方案

#### 方案一：使用系统字体栈

```python
fig.update_layout(
    font=dict(
        # 字体栈：依次尝试这些字体
        family='"Microsoft YaHei", "SimHei", "PingFang SC", "Heiti SC", sans-serif'
    )
)
```

#### 方案二：使用Web安全字体

```python
fig.update_layout(
    font=dict(
        family='"Noto Sans SC", "Microsoft YaHei", "SimHei", sans-serif'
    )
)
```

### 3.3 推荐的中文字体

| 操作系统 | 推荐字体 | CSS Font Family |
|----------|-----------|----------------|
| Windows | Microsoft YaHei（微软雅黑） | `"Microsoft YaHei"` |
| Windows | SimHei（黑体） | `"SimHei"` |
| Mac/Linux | PingFang SC | `"PingFang SC"` |
| 跨平台 | Noto Sans SC（Google字体） | `"Noto Sans SC"` |

### 3.4 完整字体配置代码

```python
def configure_chinese_font():
    """配置中文字体"""
    return {
        'title_font': dict(
            family='"Microsoft YaHei", "SimHei", sans-serif',
            size=20,
            color='#1f1f1f'
        ),
        'axis_font': dict(
            family='"Microsoft YaHei", "SimHei", sans-serif',
            size=12
        ),
        'legend_font': dict(
            family='"Microsoft YaHei", "SimHei", sans-serif',
            size=12
        )
    }

# 应用到图表
fig.update_layout(
    title=configure_chinese_font()['title_font'],
    font=configure_chinese_font()['axis_font'],
    legend=dict(font=configure_chinese_font()['legend_font'])
)
```

---

## 4. 颜色主题

### 4.1 使用Plotly内置主题

```python
import plotly.express as px

# 查看可用主题
print(px.templates.keys())
# ['ggplot2', 'seaborn', 'simple_white', 'plotly',
#  'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
#  'ygridoff', 'gridon', 'none']

# 应用主题
fig.update_layout(template='plotly_dark')
# 或
fig = px.line_polar(..., template='plotly_white')
```

### 4.2 内置主题效果

| 主题 | 适用场景 | 特点 |
|------|----------|------|
| `plotly` | 通用 | 默认配色，灰色背景 |
| `plotly_white` | 报告/打印 | 白色背景，简洁 |
| `plotly_dark` | 深色环境 | 深色背景 |
| `ggplot2` | 数据分析 | 类似R的ggplot2 |
| `seaborn` | 科学研究 | 类似Seaborn风格 |
| `simple_white` | 极简需求 | 无网格线 |

### 4.3 自定义颜色方案

#### 渐变色填充

```python
# 使用rgba实现透明填充
fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    fillcolor='rgba(31, 119, 180, 0.3)',  # 30%透明度
    line=dict(color='#1f77b4')
))
```

#### 颜色序列

```python
# 为多人对比设置颜色
colors = [
    '#1f77b4',  # 蓝色
    '#ff7f0e',  # 橙色
    '#2ca02c',  # 青色
    '#d62728',  # 红色
    '#9467bd'   # 紫色
]
```

### 4.4 使用Plotly内置颜色序列

```python
import plotly.express as px

# 顺序色（Sequential）- 适合单向数据
colors_seq = px.colors.sequential.Viridis
colors_seq2 = px.colors.sequential.Plasma

# 发散色（Diverging）- 适合有中点的数据
colors_div = px.colors.diverging.RdBu

# 循环色（Cyclical）- 适合周期性数据
colors_cyc = px.colors.cyclical.HSV

# 应用到trace
fig.add_trace(go.Scatterpolar(
    marker=dict(
        color=colors_seq[5],  # 使用颜色序列中的颜色
        colorscale=colors_seq   # 或直接使用色阶
    )
))
```

---

## 5. 响应式布局

### 5.1 Streamlit响应式布局关键点

1. **use_container_width=True**
   ```python
   st.plotly_chart(fig, use_container_width=True)
   ```
   让图表宽度自适应容器

2. **st.columns()**
   ```python
   col1, col2 = st.columns([1, 1])  # 等宽两列
   col1, col2, col3 = st.columns([1, 2, 1])  # 1:2:1比例
   ```

3. **固定图表高度**
   ```python
   fig.update_layout(height=500)  # 避免内容跳动
   ```

### 5.2 响应式布局示例

```python
import streamlit as st
import plotly.graph_objects as go

# 页面配置
st.set_page_config(layout="wide")

# 创建响应式列
left_col, main_col, right_col = st.columns([1, 3, 1])

with left_col:
    st.metric("评估人数", "5", "人")

with main_col:
    categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[85, 78, 72, 88, 82, 85],
        theta=categories,
        fill='toself'
    ))

    # 固定高度，自适应宽度
    fig.update_layout(height=400)

    # 关键：use_container_width=True
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.info("""
    **响应式要点**：
    - st.columns([1,3,1])
    - use_container_width=True
    - 固定height=400
    """)
```

### 5.3 移动端适配建议

```python
# 获取屏幕类型
is_mobile = st.sidebar.checkbox("移动端视图")

if is_mobile:
    # 移动端：更紧凑的布局
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=10)
    )
else:
    # 桌面端：完整布局
    fig.update_layout(
        height=500,
        margin=dict(l=80, r=80, t=80, b=80),
        font=dict(size=12)
    )
```

---

## 6. Streamlit集成代码

### 6.1 基础集成

```python
import streamlit as st
import plotly.graph_objects as go

# 创建雷达图
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[85, 78, 72, 88, 82],
    theta=['技术', '沟通', '领导', '创新', '学习'],
    fill='toself'
))

# 显示图表
st.plotly_chart(fig, use_container_width=True)
```

### 6.2 完整应用示例

```python
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="能力评估系统",
    layout="wide",
    page_icon="📊"
)

# 标题
st.title("📊 团队能力评估雷达图")

# 侧边栏
with st.sidebar:
    st.header("配置选项")

    # 主题选择
    theme = st.selectbox(
        "颜色主题",
        ["专业蓝", "活力彩虹", "深色模式"],
        index=0
    )

    # 数值范围
    min_val = st.slider("最小值", 0, 50, 0)
    max_val = st.slider("最大值", 50, 150, 100)

# 主内容
col1, col2 = st.columns([2, 1])

with col1:
    # 数据输入
    st.subheader("能力数据录入")

    names = st.text_input("姓名", value="张三")
    scores = [
        st.slider("技术能力", 0, 100, 85),
        st.slider("沟通能力", 0, 100, 78),
        st.slider("领导力", 0, 100, 72),
        st.slider("创新能力", 0, 100, 88),
        st.slider("学习能力", 0, 100, 82)
    ]

    # 创建图表
    categories = ['技术能力', '沟通能力', '领导力', '创新能力', '学习能力']
    scores_closed = scores + [scores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=categories + [categories[0]],
        name=names,
        fill='toself',
        fillcolor='rgba(31, 119, 180, 0.3)',
        line=dict(color='#1f77b4', width=3)
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[min_val, max_val])),
        font=dict(family='"Microsoft YaHei", "SimHei"'),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    # 信息面板
    st.subheader("评估说明")
    st.info(f"""
    **评估标准**：
    - 优秀: 90-100分
    - 良好: 80-89分
    - 中等: 70-79分
    - 需提升: <70分

    **当前评估**：{names}
    - 平均分: {sum(scores)/len(scores):.1f}
    - 最高项: {categories[scores.index(max(scores))]}
    - 最低项: {categories[scores.index(min(scores))]}
    """)
```

### 6.3 交互功能扩展

```python
# 添加数据导出
if st.button("导出数据"):
    export_data = pd.DataFrame({
        '维度': categories,
        '得分': scores
    })
    st.download_button(
        "下载CSV",
        export_data.to_csv(index=False),
        "text/csv",
        "ability_scores.csv"
    )

# 添加图片导出
if st.button("保存图表"):
    # 需要安装 kaleido
    fig.write_image("radar_chart.png", scale=2)
    st.success("图表已保存")
```

### 6.4 性能优化建议

```python
# 1. 使用@st.cache_data缓存数据
@st.cache_data(ttl=3600)
def load_ability_data():
    # 加载数据的函数
    return pd.read_csv("ability_data.csv")

# 2. 限制同时显示的图表数量
if st.checkbox("高性能模式"):
    # 减少动画效果
    fig.update_layout(transition_duration=0)

# 3. 使用session state保持状态
if 'history' not in st.session_state:
    st.session_state.history = []
```

---

## 7. 最佳实践总结

### 7.1 DO（推荐）

1. **数据准备**
   - 始终闭合多边形（首尾数据重复）
   - 使用统一的数值范围便于对比
   - 考虑数据标准化

2. **视觉设计**
   - 维度控制在5-7个
   - 使用透明填充（alpha 0.2-0.4）
   - 确保颜色对比鲜明

3. **性能优化**
   - `use_container_width=True` 实现响应式
   - 固定图表高度避免跳动
   - 使用`st.columns()`合理布局

4. **中文支持**
   - 配置字体栈：`"Microsoft YaHei", "SimHei", sans-serif`
   - 测试不同浏览器的兼容性

### 7.2 DON'T（避免）

1. **不要**使用超过7个维度
   - 图表会过于复杂难以阅读

2. **不要**忽略数据闭合
   - 必须将第一个数据点添加到末尾

3. **不要**过度使用动画
   - 在Streamlit中可能导致性能问题

4. **不要**硬编码字体
   - 使用字体栈提供备选方案

---

## 8. 运行示例

```bash
# 安装依赖
pip install streamlit plotly pandas

# 运行完整示例
streamlit run streamlit_radar_chart_demo.py

# 运行快速参考
streamlit run streamlit_radar_chart_quick_reference.py
```

---

## 附录：快速代码片段

### A. 最小雷达图

```python
import plotly.express as px
fig = px.line_polar(
    r=[8, 7, 9, 6, 8],
    theta=['摄像头', '电池', '屏幕', '处理器', '设计'],
    line_close=True
)
fig.update_traces(fill='toself')
```

### B. 多人对比

```python
import plotly.graph_objects as go
fig = go.Figure()
for person, color in [('A', 'blue'), ('B', 'red')]:
    fig.add_trace(go.Scatterpolar(
        r=[8, 7, 9, 6, 8] + [8],
        theta=['摄像头', '电池', '屏幕', '处理器', '设计', '摄像头'],
        name=person,
        fill='toself',
        line=dict(color=color)
    ))
```

### C. 中文字体配置

```python
fig.update_layout(
    font=dict(family='"Microsoft YaHei", "SimHei", sans-serif')
)
```

---

**文档版本**: 1.0
**最后更新**: 2025-02-12
**适用版本**: Streamlit 1.16+, Plotly 5.0+
