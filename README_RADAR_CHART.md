# Plotly + Streamlit 雷达图项目

## 项目概述

本项目包含完整的Plotly雷达图在Streamlit中的最佳实践实现，包括：

- 中文字体配置
- 五维能力雷达图
- 多人对比雷达图
- 颜色主题系统
- 响应式布局
- 可复用工具模块

## 文件结构

```
stream-max/
├── streamlit_radar_chart_demo.py          # 完整功能演示应用
├── streamlit_radar_chart_quick_reference.py  # 快速代码参考
├── streamlit_radar_chart_best_practices.py # 最佳实践演示
├── streamlit_radar_utils.py               # 可复用工具模块
├── RADAR_CHART_GUIDE.md                  # 完整使用文档
├── README_RADAR_CHART.md                   # 本文件
├── requirements.txt                        # Python依赖
└── run_radar_demo.bat                    # 快速启动脚本
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行示例

**Windows用户**:
```bash
run_radar_demo.bat
```

**Linux/Mac用户**:
```bash
# 运行完整演示
streamlit run streamlit_radar_chart_demo.py

# 运行快速参考
streamlit run streamlit_radar_chart_quick_reference.py

# 运行最佳实践
streamlit run streamlit_radar_chart_best_practices.py
```

## 核心功能

### 1. 五维能力雷达图

展示个人或团队能力评估的标准雷达图：

```python
from streamlit_radar_utils import radar_chart_component, get_five_dimensions, get_demo_data

# 数据
data = get_demo_data()
categories = get_five_dimensions()

# 创建雷达图
radar_chart_component(
    data=data,
    categories=categories,
    title="五维能力评估",
    theme="professional"
)
```

**五维能力标准**：
- 技术能力 (Technical Skills)
- 沟通能力 (Communication)
- 领导力 (Leadership)
- 创新能力 (Innovation)
- 学习能力 (Learning Ability)

### 2. 中文字体支持

自动配置中文显示，无需额外设置：

```python
# 方式1：使用工具组件
from streamlit_radar_utils import radar_chart_component

radar_chart_component(
    data={'张三': [85, 78, 72, 88, 82]},
    categories=['技术能力', '沟通能力', '领导力', '创新能力', '学习能力'],
    title="能力评估"
)  # 自动应用中文字体

# 方式2：手动配置
import plotly.graph_objects as go

fig.update_layout(
    font=dict(
        family='"Microsoft YaHei", "SimHei", "PingFang SC", sans-serif'
    )
)
```

### 3. 颜色主题

内置6种专业颜色主题：

```python
from streamlit_radar_utils import ColorThemes

# 可用主题
themes = {
    'professional': ColorThemes.PROFESSIONAL,  # 专业蓝
    'vibrant': ColorThemes.VIBRANT,      # 活力彩虹
    'pastel': ColorThemes.PASTEL,         # 柔和粉彩
    'nature': ColorThemes.NATURE,         # 自然绿色
    'warm': ColorThemes.WARM,             # 暖色系
    'cool': ColorThemes.COOL              # 冷色系
}
```

### 4. 响应式布局

使用`st.columns()`实现响应式布局：

```python
import streamlit as st

# 创建列：1:2:1比例
left_col, main_col, right_col = st.columns([1, 2, 1])

with main_col:
    # 雷达图（自适应宽度）
    st.plotly_chart(fig, use_container_width=True)

with left_col:
    st.metric("总人数", "5")

with right_col:
    st.info("说明信息")
```

### 5. 高级功能

工具模块提供的高级类：

```python
from streamlit_radar_utils import AdvancedRadarChart, RadarChartConfig

config = RadarChartConfig(
    categories=['技术能力', '沟通能力', '领导力', '创新能力', '学习能力'],
    theme="professional"
)

builder = AdvancedRadarChart(config)

# 添加区域范围
builder.add_area_ranges(
    ranges=[(60, 90), (70, 100), (50, 80)],
    names=['优秀区', '达标区', '需改进'],
    colors=['green', 'blue', 'red']
)

# 添加平均值线
builder.add_average_trace([
    [85, 78, 72, 88, 82],
    [75, 85, 80, 70, 90]
])

# 生成图表
fig = builder.build()
```

## 最佳实践要点

### DO（推荐做法）

1. **数据准备**
   - [x] 始终闭合多边形（首尾数据重复）
   - [x] 使用统一的数值范围便于对比
   - [x] 考虑数据标准化

2. **视觉设计**
   - [x] 维度控制在5-7个（过多难以阅读）
   - [x] 使用透明填充（alpha 0.2-0.4）
   - [x] 确保颜色对比鲜明

3. **响应式布局**
   - [x] `use_container_width=True` 实现自适应
   - [x] 使用`st.columns()`合理分区
   - [x] 固定图表高度避免跳动

4. **性能优化**
   - [x] 使用`@st.cache_data`缓存数据
   - [x] 限制同时显示的图表数量
   - [x] 避免过度自定义导致性能下降

### DON'T（避免做法）

1. **[x] 不要**使用超过7个维度
2. **[x] 不要**忽略多边形闭合
3. **[x] 不要**硬编码单一字体（使用字体栈）
4. **[x] 不要**在Streamlit中使用复杂动画

## API参考

### radar_chart_component

创建标准雷达图组件。

```python
radar_chart_component(
    data: Dict[str, List[float]],  # 数据字典
    categories: List[str],              # 维度标签
    title: str = "雷达图",           # 图表标题
    theme: str = 'professional',        # 主题
    height: int = 500,                # 高度
    key: str = None                   # 唯一标识
)
```

### ColorThemes

颜色主题类。

```python
# 静态颜色
ColorThemes.PROFESSIONAL  # 专业蓝
ColorThemes.VIBRANT      # 活力彩虹
ColorThemes.PASTEL        # 柔和粉彩
ColorThemes.NATURE        # 自然绿色
ColorThemes.WARM          # 暖色系
ColorThemes.COOL           # 冷色系

# 方法
ColorThemes.get_with_opacity(color, opacity)  # 添加透明度
```

### RadarChartBuilder

雷达图构建器类。

```python
config = RadarChartConfig(
    title="标题",
    categories=["维度1", "维度2"],
    value_range=(0, 100),
    theme="professional"
)

builder = RadarChartBuilder(config)
builder.add_trace(RadarData(name="系列1", values=[80, 90]))
builder.add_reference_line([70, 70, 70, 70, 70])
fig = builder.build()
```

## 常见问题

### Q1: 中文显示为方框怎么办？

**A**: 确保字体配置正确：
```python
fig.update_layout(
    font=dict(
        family='"Microsoft YaHei", "SimHei", "PingFang SC", sans-serif'
    )
)
```

### Q2: 雷达图不闭合？

**A**: 添加首点数据到末尾：
```python
values = [85, 78, 72, 88, 82]
values_closed = values + [values[0]]  # 闭合
```

### Q3: 多个雷达图如何对比？

**A**: 使用不同颜色，添加图例：
```python
for idx, (name, scores) in enumerate(data.items()):
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        name=name,  # 显示在图例
        fill='toself',
        line=dict(color=colors[idx])
    ))
```

### Q4: 如何实现响应式？

**A**: 使用`use_container_width=True`：
```python
st.plotly_chart(fig, use_container_width=True)
```

## 示例效果

### 单人雷达图

```
        技术能力
            /|\
    88  |  学习能力
      /  |
创新  |  82
  /  |
沟通  |  78
  \  |
      领导
      72
```

### 多人对比雷达图

```
        技术能力
            /|\  张三 -- 李四 -- 王五
    88  |  90
      /  |
创新  |  88  |  85
  /  |
沟通  |  78  |  82
  \  |
      领导
      72  |  78
```

## 更新日志

### v1.0.0 (2025-02-12)
- 初始版本发布
- 完整的五维能力雷达图实现
- 中文字体自动配置
- 6种颜色主题
- 响应式布局支持
- 可复用工具模块

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

---

**Created with**: Streamlit + Plotly
**Author**: AI Assistant
**Date**: 2025-02-12
