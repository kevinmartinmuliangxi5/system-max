"""
Legacy Components - 旧版模板迁移组件
=====================================

将原有 ui_templates.py 的 5 个模板迁移到新组件格式。

这些组件保持了原有的 API 兼容性，同时提供新系统的功能。

组件列表:
    - SidebarMainLayout: 经典左右分栏 (TEMPLATE_A)
    -TabsNavigationLayout: 顶部导航标签页 (TEMPLATE_B)
    - CardGridLayout: 卡片网格布局 (TEMPLATE_C)
    - ChatInterfaceLayout: 聊天对话界面 (TEMPLATE_D)
    - StepWizardLayout: 分步表单向导 (TEMPLATE_E)

迁移说明:
    - 原有 TEMPLATE_A~E 已转换为新的组件类
    - 保持相同的代码骨架和预览
    - 添加新系统的属性和方法
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


# ============================================================================
# 旧版模板组件定义
# ============================================================================

class SidebarMainLayout:
    """
    经典左右分栏布局 (TEMPLATE_A)

    左侧侧边栏配置，右侧主内容区。
    适合: 后台管理、数据面板、工具类应用

    特性:
        - 侧边栏配置区
        - 主内容展示区
        - 响应式布局
    """

    id = "sidebar_main"
    name = "经典左右分栏"
    description = "左侧侧边栏配置，右侧主内容区。适合：后台管理、数据面板、工具类应用"
    category = "layout"
    size = "large"

    preview = """
┌─────────────────────────────────────────────────┐
│  📊 应用标题                                     │
├───────────────┬─────────────────────────────────┤
│  ⚙️ 侧边栏    │                                 │
│               │      📋 主内容区                 │
│  [配置项1]    │                                 │
│  [配置项2]    │      - 数据展示                  │
│  [配置项3]    │      - 表单输入                  │
│               │      - 结果反馈                  │
│  [操作按钮]   │                                 │
└───────────────┴─────────────────────────────────┘
    """

    features = ["侧边栏配置区", "主内容展示区", "响应式布局"]

    code_skeleton = '''
import streamlit as st

# 页面配置
st.set_page_config(
    page_title="应用名称",
    page_icon="📊",
    layout="wide"
)

# ========== 侧边栏 ==========
with st.sidebar:
    st.header("⚙️ 配置")

    # 配置项示例
    option1 = st.selectbox("选项1", ["A", "B", "C"])
    option2 = st.slider("数值调节", 0, 100, 50)
    option3 = st.text_input("文本输入", placeholder="请输入...")

    st.divider()

    if st.button("执行操作", type="primary", use_container_width=True):
        st.session_state.action_triggered = True

# ========== 主内容区 ==========
st.title("📊 应用标题")
st.caption("应用描述信息")

# 内容区域
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("主要内容")
    st.info("这里放置主要内容")

with col2:
    st.subheader("辅助信息")
    st.metric("指标", "100", "+10%")
'''

    props = {
        "title": "应用标题",
        "sidebar_items": ["配置项1", "配置项2", "配置项3"],
        "show_divider": True,
    }

    def render_streamlit(self) -> str:
        """渲染 Streamlit 代码"""
        return self.code_skeleton


class TabsNavigationLayout:
    """
    顶部导航标签页布局 (TEMPLATE_B)

    顶部标签页切换不同功能模块。
    适合: 多功能应用、文档系统、设置页面

    特性:
        - 标签页导航
        - 模块化内容
        - 清晰分区
    """

    id = "tabs_navigation"
    name = "顶部导航标签页"
    description = "顶部标签页切换不同功能模块。适合：多功能应用、文档系统、设置页面"
    category = "layout"
    size = "large"

    preview = """
┌─────────────────────────────────────────────────┐
│  📊 应用标题                                     │
├─────────────────────────────────────────────────┤
│  [标签1] [标签2] [标签3] [标签4]                 │
├─────────────────────────────────────────────────┤
│                                                 │
│              当前标签页内容                       │
│                                                 │
│              - 功能区域 A                        │
│              - 功能区域 B                        │
│                                                 │
└─────────────────────────────────────────────────┘
    """

    features = ["标签页导航", "模块化内容", "清晰分区"]

    code_skeleton = '''
import streamlit as st

# 页面配置
st.set_page_config(
    page_title="应用名称",
    page_icon="📊",
    layout="wide"
)

st.title("📊 应用标题")

# ========== 标签页导航 ==========
tab1, tab2, tab3, tab4 = st.tabs(["📝 功能一", "📊 功能二", "⚙️ 设置", "❓ 帮助"])

with tab1:
    st.header("功能一")
    st.write("这里是功能一的内容")

    # 示例表单
    with st.form("form1"):
        input1 = st.text_input("输入项")
        submitted = st.form_submit_button("提交")

with tab2:
    st.header("功能二")
    st.write("这里是功能二的内容")

    # 示例图表区
    col1, col2, col3 = st.columns(3)
    col1.metric("指标A", "100", "+5%")
    col2.metric("指标B", "200", "-3%")
    col3.metric("指标C", "300", "+12%")

with tab3:
    st.header("设置")
    st.toggle("开关选项1")
    st.toggle("开关选项2")

with tab4:
    st.header("帮助")
    st.info("使用说明...")
'''

    props = {
        "title": "应用标题",
        "tabs": ["功能一", "功能二", "设置", "帮助"],
        "default_tab": 0,
    }

    def render_streamlit(self) -> str:
        """渲染 Streamlit 代码"""
        return self.code_skeleton


class CardGridLayout:
    """
    卡片网格布局 (TEMPLATE_C)

    多卡片网格展示，每个卡片独立功能。
    适合: 数据仪表盘、产品展示、多指标监控

    特性:
        - 指标卡片
        - 网格布局
        - 数据可视化
    """

    id = "card_grid"
    name = "卡片网格布局"
    description = "多卡片网格展示，每个卡片独立功能。适合：数据仪表盘、产品展示、多指标监控"
    category = "dashboard"
    size = "large"

    preview = """
┌─────────────────────────────────────────────────┐
│  📊 应用标题                        [筛选] [刷新]│
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │ 卡片 1  │  │ 卡片 2  │  │ 卡片 3  │         │
│  │  指标   │  │  指标   │  │  指标   │         │
│  │  +10%   │  │  -5%    │  │  +20%   │         │
│  └─────────┘  └─────────┘  └─────────┘         │
│  ┌─────────────────────────────────────┐       │
│  │           大卡片 / 图表区            │       │
│  │                                     │       │
│  └─────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
    """

    features = ["指标卡片", "网格布局", "数据可视化"]

    code_skeleton = '''
import streamlit as st

# 页面配置
st.set_page_config(
    page_title="应用名称",
    page_icon="📊",
    layout="wide"
)

# ========== 顶部标题栏 ==========
col_title, col_actions = st.columns([3, 1])
with col_title:
    st.title("📊 数据仪表盘")
with col_actions:
    st.button("🔄 刷新")

st.divider()

# ========== 指标卡片行 ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("总用户数", "1,234", "+12%")
with col2:
    st.metric("活跃用户", "567", "+5%")
with col3:
    st.metric("转化率", "23.4%", "-2%")
with col4:
    st.metric("收入", "¥89,000", "+18%")

st.divider()

# ========== 内容卡片 ==========
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 趋势图表")
    # 这里放图表
    st.area_chart({"数据": [1, 5, 2, 6, 2, 1]})

with col_right:
    st.subheader("📋 最新动态")
    st.info("动态 1: ...")
    st.info("动态 2: ...")
    st.info("动态 3: ...")
'''

    props = {
        "title": "数据仪表盘",
        "metrics": [
            {"label": "总用户数", "value": "1,234", "delta": "+12%"},
            {"label": "活跃用户", "value": "567", "delta": "+5%"},
            {"label": "转化率", "value": "23.4%", "delta": "-2%"},
            {"label": "收入", "value": "¥89,000", "delta": "+18%"},
        ],
        "grid_columns": 4,
    }

    def render_streamlit(self) -> str:
        """渲染 Streamlit 代码"""
        return self.code_skeleton


class ChatInterfaceLayout:
    """
    聊天对话界面 (TEMPLATE_D)

    类似 ChatGPT 的对话界面。
    适合: AI 助手、客服机器人、问答系统

    特性:
        - 对话气泡
        - 历史记录
        - 流式输出
    """

    id = "chat_interface"
    name = "聊天对话界面"
    description = "类似 ChatGPT 的对话界面。适合：AI 助手、客服机器人、问答系统"
    category = "chat"
    size = "large"

    preview = """
┌─────────────────────────────────────────────────┐
│  🤖 AI 助手                          [清空对话] │
├─────────────────────────────────────────────────┤
│                                                 │
│  👤 用户: 你好，请帮我...                        │
│                                                 │
│  🤖 助手: 好的，我来帮您...                      │
│                                                 │
│  👤 用户: 还有一个问题...                        │
│                                                 │
│  🤖 助手: 这个问题的答案是...                    │
│                                                 │
├─────────────────────────────────────────────────┤
│  [请输入您的问题...                    ] [发送] │
└─────────────────────────────────────────────────┘
    """

    features = ["对话气泡", "历史记录", "流式输出"]

    code_skeleton = '''
import streamlit as st

# 页面配置
st.set_page_config(
    page_title="AI 助手",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI 助手")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 生成回复（这里替换为实际 AI 调用）
    response = f"这是对 '{prompt}' 的回复"

    # 添加助手消息
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# 侧边栏
with st.sidebar:
    st.header("设置")
    if st.button("清空对话"):
        st.session_state.messages = []
        st.rerun()
'''

    props = {
        "title": "AI 助手",
        "show_clear_button": True,
        "streaming": True,
    }

    def render_streamlit(self) -> str:
        """渲染 Streamlit 代码"""
        return self.code_skeleton


class StepWizardLayout:
    """
    分步表单向导 (TEMPLATE_E)

    分步骤引导用户完成复杂表单。
    适合: 注册流程、调查问卷、配置向导

    特性:
        - 步骤指示器
        - 表单验证
        - 进度保存
    """

    id = "step_wizard"
    name = "分步表单向导"
    description = "分步骤引导用户完成复杂表单。适合：注册流程、调查问卷、配置向导"
    category = "form"
    size = "large"

    preview = """
┌─────────────────────────────────────────────────┐
│  📝 表单标题                                     │
├─────────────────────────────────────────────────┤
│     ① ─────── ② ─────── ③ ─────── ④            │
│   基本信息    详细设置    确认提交    完成       │
├─────────────────────────────────────────────────┤
│                                                 │
│              当前步骤的表单内容                   │
│                                                 │
│              [输入框]                            │
│              [选择框]                            │
│                                                 │
├─────────────────────────────────────────────────┤
│                      [上一步]  [下一步]          │
└─────────────────────────────────────────────────┘
    """

    features = ["步骤指示器", "表单验证", "进度保存"]

    code_skeleton = '''
import streamlit as st

# 页面配置
st.set_page_config(
    page_title="配置向导",
    page_icon="📝",
    layout="centered"
)

st.title("📝 配置向导")

# 初始化步骤
if "step" not in st.session_state:
    st.session_state.step = 1

# 步骤指示器
steps = ["基本信息", "详细设置", "确认提交", "完成"]
cols = st.columns(len(steps))
for i, (col, step_name) in enumerate(zip(cols, steps), 1):
    if i < st.session_state.step:
        col.success(f"✅ {step_name}")
    elif i == st.session_state.step:
        col.info(f"📍 {step_name}")
    else:
        col.write(f"⬜ {step_name}")

st.divider()

# 步骤内容
if st.session_state.step == 1:
    st.subheader("步骤 1: 基本信息")
    st.session_state.name = st.text_input("姓名")
    st.session_state.email = st.text_input("邮箱")

elif st.session_state.step == 2:
    st.subheader("步骤 2: 详细设置")
    st.session_state.option = st.selectbox("选择选项", ["A", "B", "C"])
    st.session_state.level = st.slider("级别", 1, 10, 5)

elif st.session_state.step == 3:
    st.subheader("步骤 3: 确认信息")
    st.write(f"姓名: {st.session_state.get('name', '')}")
    st.write(f"邮箱: {st.session_state.get('email', '')}")
    st.write(f"选项: {st.session_state.get('option', '')}")

elif st.session_state.step == 4:
    st.balloons()
    st.success("🎉 配置完成！")

# 导航按钮
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.session_state.step > 1:
        if st.button("⬅️ 上一步"):
            st.session_state.step -= 1
            st.rerun()
with col3:
    if st.session_state.step < 4:
        if st.button("下一步 ➡️", type="primary"):
            st.session_state.step += 1
            st.rerun()
'''

    props = {
        "title": "配置向导",
        "steps": ["基本信息", "详细设置", "确认提交", "完成"],
        "show_progress": True,
    }

    def render_streamlit(self) -> str:
        """渲染 Streamlit 代码"""
        return self.code_skeleton


# ============================================================================
# 模板映射表
# ============================================================================

TEMPLATE_MAPPING = {
    "A": SidebarMainLayout,
    "B": TabsNavigationLayout,
    "C": CardGridLayout,
    "D": ChatInterfaceLayout,
    "E": StepWizardLayout,
}

# ============================================================================
# 导出
# ============================================================================

__all__ = [
    "SidebarMainLayout",
    "TabsNavigationLayout",
    "CardGridLayout",
    "ChatInterfaceLayout",
    "StepWizardLayout",
    "TEMPLATE_MAPPING",
]
