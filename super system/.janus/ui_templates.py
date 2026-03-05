# ui_templates.py
# Streamlit UI 模板库 - 零基础用户友好 (兼容层)
# 双脑协同·指挥官系统 v2.3

"""
兼容层说明:

⚠️ 废弃警告: 这个文件已迁移到新的组件库系统！

旧 API 仍然可用，但建议迁移到新的 API:

旧 API (此文件):
    >>> from ui_templates import get_template, get_all_templates
    >>> template = get_template("A")

新 API (推荐):
    >>> from ui_library import get_component, list_components
    >>> from ui_library.components.legacy import TEMPLATE_MAPPING
    >>> component = get_component("SidebarMainLayout")

新系统提供:
    - 20+ 组件 (vs 5 个模板)
    - 15+ 主题方案
    - 多框架支持 (Streamlit, React)
    - 智能推荐引擎
    - 行业专用模板

迁移指南:
    1. TEMPLATE_A → SidebarMainLayout
    2. TEMPLATE_B → TabsNavigationLayout
    3. TEMPLATE_C → CardGridLayout
    4. TEMPLATE_D → ChatInterfaceLayout
    5. TEMPLATE_E → StepWizardLayout

使用方法 (旧 API，保持兼容):
    1. Brain 展示模板描述给用户选择
    2. 用户选择后，Brain 将模板代码注入蓝图
    3. Worker 基于模板生成完整代码
    4. 用户可用自然语言微调
"""

import warnings
from typing import Dict, List, Any, Optional

# 导入新系统的组件
try:
    from ui_library.components.legacy import (
        SidebarMainLayout,
        TabsNavigationLayout,
        CardGridLayout,
        ChatInterfaceLayout,
        StepWizardLayout,
        TEMPLATE_MAPPING,
    )
    NEW_SYSTEM_AVAILABLE = True
except ImportError:
    NEW_SYSTEM_AVAILABLE = False


# =============================================================================
# 废弃警告
# =============================================================================

def _show_deprecation_warning():
    """显示废弃警告"""
    warnings.warn(
        "ui_templates.py 已迁移到新系统 ui_library。"
        "建议使用: from ui_library import get_component, list_components, recommend。"
        "旧 API 仍然可用，但将在未来版本中移除。",
        DeprecationWarning,
        stacklevel=3
    )


# =============================================================================
# 旧版模板定义 (兼容层)
# ============================================================================

TEMPLATE_A = {
    "name": "经典左右分栏",
    "id": "sidebar_main",
    "description": "左侧侧边栏配置，右侧主内容区。适合：后台管理、数据面板、工具类应用",
    "preview": """
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
    """,
    "features": ["侧边栏配置区", "主内容展示区", "响应式布局"],
    "code_skeleton": SidebarMainLayout.code_skeleton if NEW_SYSTEM_AVAILABLE else '''
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
}

TEMPLATE_B = {
    "name": "顶部导航标签页",
    "id": "tabs_navigation",
    "description": "顶部标签页切换不同功能模块。适合：多功能应用、文档系统、设置页面",
    "preview": """
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
    """,
    "features": ["标签页导航", "模块化内容", "清晰分区"],
    "code_skeleton": TabsNavigationLayout.code_skeleton if NEW_SYSTEM_AVAILABLE else '''
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
}

TEMPLATE_C = {
    "name": "卡片网格布局",
    "id": "card_grid",
    "description": "多卡片网格展示，每个卡片独立功能。适合：数据仪表盘、产品展示、多指标监控",
    "preview": """
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
    """,
    "features": ["指标卡片", "网格布局", "数据可视化"],
    "code_skeleton": CardGridLayout.code_skeleton if NEW_SYSTEM_AVAILABLE else '''
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
}

TEMPLATE_D = {
    "name": "聊天对话界面",
    "id": "chat_interface",
    "description": "类似 ChatGPT 的对话界面。适合：AI 助手、客服机器人、问答系统",
    "preview": """
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
    """,
    "features": ["对话气泡", "历史记录", "流式输出"],
    "code_skeleton": ChatInterfaceLayout.code_skeleton if NEW_SYSTEM_AVAILABLE else '''
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
}

TEMPLATE_E = {
    "name": "分步表单向导",
    "id": "step_wizard",
    "description": "分步骤引导用户完成复杂表单。适合：注册流程、调查问卷、配置向导",
    "preview": """
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
    """,
    "features": ["步骤指示器", "表单验证", "进度保存"],
    "code_skeleton": StepWizardLayout.code_skeleton if NEW_SYSTEM_AVAILABLE else '''
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
}


# =============================================================================
# 模板索引
# ============================================================================

TEMPLATES = {
    "A": TEMPLATE_A,
    "B": TEMPLATE_B,
    "C": TEMPLATE_C,
    "D": TEMPLATE_D,
    "E": TEMPLATE_E,
}


# =============================================================================
# 旧版 API (保持兼容)
# ============================================================================

def get_template(template_id: str) -> Optional[Dict[str, Any]]:
    """
    获取模板 (旧 API - 保持兼容)

    ⚠️ 废弃警告: 建议使用新 API
    >>> from ui_library import get_component
    >>> component = get_component("SidebarMainLayout")

    Args:
        template_id: 模板 ID ("A" - "E")

    Returns:
        模板字典
    """
    _show_deprecation_warning()
    return TEMPLATES.get(template_id.upper())


def get_all_templates() -> Dict[str, Dict[str, Any]]:
    """
    获取所有模板 (旧 API - 保持兼容)

    ⚠️ 废弃警告: 建议使用新 API
    >>> from ui_library import list_components
    >>> components = list_components()

    Returns:
        所有模板的字典
    """
    _show_deprecation_warning()
    return TEMPLATES


def get_template_summary() -> List[Dict[str, Any]]:
    """
    获取模板摘要 (旧 API - 保持兼容)

    ⚠️ 废弃警告: 建议使用新 API
    >>> from ui_library import list_components
    >>> components = list_components()

    Returns:
        模板摘要列表
    """
    _show_deprecation_warning()
    summary = []
    for key, tpl in TEMPLATES.items():
        summary.append({
            "id": key,
            "name": tpl["name"],
            "description": tpl["description"],
            "preview": tpl["preview"]
        })
    return summary


# =============================================================================
# 新系统快捷方式 (推荐使用)
# ============================================================================

def migrate_to_new_system():
    """
    迁移到新系统的快捷方式

    返回新系统的主要函数:
    - get_component: 获取组件
    - list_components: 列出组件
    - recommend: 智能推荐

    Example:
        >>> from ui_templates import migrate_to_new_system
        >>> get_component, list_components, recommend = migrate_to_new_system()
        >>> component = get_component("DashboardPage")
    """
    if not NEW_SYSTEM_AVAILABLE:
        raise ImportError(
            "新系统不可用。请确保 ui_library 模块已正确安装。"
        )

    from ui_library import get_component, list_components, recommend

    return get_component, list_components, recommend


def get_component_mapping() -> Dict[str, str]:
    """
    获取旧模板到新组件的映射关系

    Returns:
        映射字典
    """
    return {
        "A": "SidebarMainLayout",
        "B": "TabsNavigationLayout",
        "C": "CardGridLayout",
        "D": "ChatInterfaceLayout",
        "E": "StepWizardLayout",
    }


# =============================================================================
# 测试
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Streamlit UI 模板库 (兼容层)")
    print("=" * 60)

    # 显示新系统可用性
    if NEW_SYSTEM_AVAILABLE:
        print("\n✅ 新系统已可用!")
        print("建议迁移到: from ui_library import get_component, list_components")
        print("\n模板映射:")
        for old_id, new_name in get_component_mapping().items():
            print(f"  TEMPLATE_{old_id} → {new_name}")
    else:
        print("\n⚠️ 新系统不可用，使用兼容模式")

    print("\n" + "=" * 60)
    print("可用模板:")
    print("=" * 60)

    for key, tpl in TEMPLATES.items():
        print(f"\n[{key}] {tpl['name']}")
        print(f"    {tpl['description']}")
        print(f"    特性: {', '.join(tpl['features'])}")

    print("\n" + "=" * 60)
    print("使用新 API (推荐):")
    print("=" * 60)
    print("""
from ui_library import get_component, list_components, recommend

# 获取组件
component = get_component("DashboardPage")

# 列出所有组件
all_components = list_components()

# 智能推荐
recommendations = recommend(industry="data_analytics", use_case="dashboard")
    """)
