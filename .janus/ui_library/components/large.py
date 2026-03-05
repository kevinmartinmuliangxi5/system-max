"""
Large Components - 大型组件库（页面级）
=======================================

包含 8 个页面级组件模板，每个都是完整的功能模块。

组件列表:
    1. DashboardPage - 数据仪表盘
    2. ChatbotPage - 对话机器人
    3. FormWizardPage - 分步表单
    4. DataTablePage - 数据表格
    5. SettingsPage - 设置中心
    6. LandingPage - 落地页
    7. KanbanPage - 看板
    8. ProfilePage - 个人中心
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# 组件分类枚举
# ============================================================================

class LargeComponentCategory(Enum):
    """大型组件分类"""
    DASHBOARD = "dashboard"           # 仪表盘
    COMMUNICATION = "communication"   # 通讯
    FORM = "form"                     # 表单
    DATA = "data"                     # 数据
    SETTINGS = "settings"             # 设置
    MARKETING = "marketing"           # 营销
    PRODUCTIVITY = "productivity"     # 生产力
    USER = "user"                     # 用户


# ============================================================================
# 组件属性定义
# ============================================================================

@dataclass
class ComponentProp:
    """
    组件属性定义

    Attributes:
        name: 属性名称
        type: 属性类型
        default: 默认值
        required: 是否必需
        description: 属性描述
        options: 可选值列表（枚举类型）
    """
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
# 大型组件定义
# ============================================================================

@dataclass
class LargeComponent:
    """
    大型组件定义

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
    """
    id: str
    name: str
    category: LargeComponentCategory
    description: str
    preview: str
    features: List[str]
    code_skeleton: str
    props: List[ComponentProp] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    industry_compatibility: List[str] = field(default_factory=lambda: ["general"])

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
# 1. DashboardPage - 数据仪表盘
# ============================================================================

DASHBOARD_PAGE = LargeComponent(
    id="dashboard_page",
    name="数据仪表盘",
    category=LargeComponentCategory.DASHBOARD,
    description="""
    数据可视化仪表盘页面，用于展示关键业务指标和数据分析结果。
    适用于运营监控、销售分析、系统状态等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────────────┐
    │  📊 销售仪表盘                    [筛选器▼] [日期范围📅]     │
    ├─────────────────────────────────────────────────────────────┤
    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
    │  │总销售额  │ │订单数量  │ │新增客户  │ │转化率    │       │
    │  │¥128,500  │ │  1,234   │ │   +89    │ │  12.5%   │       │
    │  │  ↗15%    │ │  ↗8%     │ │  ↗12%    │ │  ↘2%     │       │
    │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
    ├─────────────────────────────────────────────────────────────┤
    │  ┌─────────────────────┐ ┌─────────────────────┐          │
    │  │  📈 销售趋势图       │ │  🥧 产品分布图      │          │
    │  │  ╱╲    ╱╲╱╲         │ │       ██           │          │
    │  │ ╱  ╲  ╱  ╲╱         │ │     ████           │          │
    │  │╱    ╲╱    ╲         │ │   ██████           │          │
    │  │  [7天] [30天] [90天] │ │  ████████          │          │
    │  └─────────────────────┘ └─────────────────────┘          │
    ├─────────────────────────────────────────────────────────────┤
    │  📋 近期订单                              [查看全部 →]     │
    │  ┌─────────────────────────────────────────────────────┐  │
    │  │ #1234  张三    ¥5,200   2024-01-15   [已完成 ✓]     │  │
    │  │ #1233  李四    ¥3,800   2024-01-15   [处理中 ⏳]     │  │
    │  └─────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘
    """,
    features=[
        "📊 关键指标卡片 - 展示核心 KPI，支持趋势对比",
        "📈 多种图表类型 - 折线图、柱状图、饼图、面积图",
        "🔍 筛选器系统 - 时间范围、分类筛选、搜索功能",
        "🎨 自定义布局 - 拖拽调整卡片位置和大小",
        "📥 数据导出 - 支持 CSV、Excel、PDF 导出",
        "🔄 实时刷新 - 自动更新数据，可配置刷新间隔",
        "📱 响应式设计 - 适配桌面、平板、移动端",
        "🎯 目标对比 - 与设定目标进行对比显示",
    ],
    code_skeleton="""
import streamlit as st
from datetime import datetime, timedelta

# ==================== 配置区 ====================
PAGE_TITLE = "{{page_title}}"  # 页面标题
REFRESH_INTERVAL = {{refresh_interval}}  # 刷新间隔（秒）
SHOW_EXPORT = {{show_export}}  # 显示导出按钮

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 侧边栏筛选器 ====================
st.sidebar.header("🔍 筛选条件")

# 时间范围选择
time_range = st.sidebar.radio(
    "时间范围",
    ["最近7天", "最近30天", "最近90天", "自定义"],
    index=1
)

if time_range == "自定义":
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("开始日期", datetime.now() - timedelta(days=30))
    end_date = col2.date_input("结束日期", datetime.now())
else:
    days_map = {"最近7天": 7, "最近30天": 30, "最近90天": 90}
    start_date = datetime.now() - timedelta(days=days_map[time_range])
    end_date = datetime.now()

# 分类筛选
category = st.sidebar.multiselect(
    "产品分类",
    ["电子产品", "服装", "食品", "其他"],
    default=["电子产品", "服装"]
)

# 数据源选择
data_source = st.sidebar.selectbox(
    "数据源",
    ["实时数据", "历史数据", "预测数据"]
)

# ==================== 顶部操作栏 ====================
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    st.title(f"📊 {PAGE_TITLE}")

with col2:
    if st.button("🔄 刷新", use_container_width=True):
        st.rerun()

with col3:
    if SHOW_EXPORT:
        export_format = st.selectbox("", ["CSV", "Excel", "PDF"])
        st.write("📥")

with col4:
    is_auto_refresh = st.checkbox("自动刷新")

# ==================== 关键指标卡片 ====================
st.divider()

# 计算模拟数据
import random
metrics = {
    "总销售额": {"value": f"¥{random.randint(100000, 200000):,}", "trend": random.choice(["↗", "↘", "→"]), "change": f"{random.randint(-15, 20)}%"},
    "订单数量": {"value": f"{random.randint(1000, 2000):,}", "trend": random.choice(["↗", "↘", "→"]), "change": f"{random.randint(-10, 15)}%"},
    "新增客户": {"value": f"+{random.randint(50, 150)}", "trend": random.choice(["↗", "↘", "→"]), "change": f"{random.randint(-5, 20)}%"},
    "转化率": {"value": f"{random.randint(8, 18)}%", "trend": random.choice(["↗", "↘", "→"]), "change": f"{random.randint(-3, 5)}%"},
}

# 展示指标卡片
cols = st.columns(4)
for idx, (metric_name, metric_data) in enumerate(metrics.items()):
    with cols[idx]:
        trend_color = {"↗": "green", "↘": "red", "→": "gray"}[metric_data["trend"]]
        st.metric(
            label=metric_name,
            value=metric_data["value"],
            delta=f"{metric_data['trend']} {metric_data['change']}",
            delta_color="normal" if metric_data["trend"] in ["↗", "→"] else "inverse"
        )

# ==================== 图表区域 ====================
st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 销售趋势")
    chart_type = st.selectbox("", ["折线图", "柱状图", "面积图"], label_visibility="collapsed")
    # 使用 plotly 或 altair 绘制图表
    st.info("📊 这里插入趋势图表\\n\\n使用 st.line_chart() 或 plotly 图表")

with chart_col2:
    st.subheader("🥧 产品分布")
    st.info("📊 这里插入分布图表\\n\\n使用 st.bar_chart() 或 plotly 饼图")

# ==================== 数据列表 ====================
st.divider()

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("📋 近期订单")
with col2:
    if st.button("查看全部 →", use_container_width=True):
        st.info("跳转到订单详情页")

# 模拟订单数据
import pandas as pd
orders = pd.DataFrame({
    "订单号": [f"#{1000+i}" for i in range(5)],
    "客户": ["张三", "李四", "王五", "赵六", "钱七"],
    "金额": [f"¥{x}" for x in [5200, 3800, 4500, 2100, 6800]],
    "日期": ["2024-01-15", "2024-01-15", "2024-01-14", "2024-01-14", "2024-01-13"],
    "状态": ["已完成", "处理中", "已完成", "待处理", "已完成"]
})

st.dataframe(
    orders,
    column_config={
        "订单号": st.column_config.TextColumn("订单号", width="medium"),
        "客户": st.column_config.TextColumn("客户", width="short"),
        "金额": st.column_config.TextColumn("金额", width="short"),
        "日期": st.column_config.DateColumn("日期", width="short"),
        "状态": st.column_config.SelectboxColumn(
            "状态",
            options=["已完成", "处理中", "待处理"],
            required=True
        )
    },
    hide_index=True,
    use_container_width=True
)

# ==================== 自动刷新 ====================
if is_auto_refresh:
    time.sleep(REFRESH_INTERVAL)
    st.rerun()
""",
    props=[
        ComponentProp("page_title", "str", "销售仪表盘", False, "页面标题"),
        ComponentProp("refresh_interval", "int", 30, False, "自动刷新间隔（秒）"),
        ComponentProp("show_export", "bool", True, False, "是否显示导出按钮"),
        ComponentProp("enable_filter", "bool", True, False, "是否启用筛选器"),
        ComponentProp("max_metrics", "int", 8, False, "最大指标卡片数量"),
    ],
    tags=["仪表盘", "数据可视化", "KPI", "分析"],
    dependencies=["streamlit", "plotly", "pandas"],
    industry_compatibility=["general", "finance", "healthcare", "manufacturing", "ecommerce"],
)


# ============================================================================
# 2. ChatbotPage - 对话机器人
# ============================================================================

CHATBOT_PAGE = LargeComponent(
    id="chatbot_page",
    name="对话机器人",
    category=LargeComponentCategory.COMMUNICATION,
    description="""
    AI 对话机器人页面，支持多轮对话、历史记录、快捷回复。
    适用于客服咨询、智能问答、对话式任务处理等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────────────┐
    │  🤖 AI 助手                           [设置⚙️] [历史🕐]     │
    ├─────────────────────────────────────────────────────────────┤
    │  ┌───────────────────────────────────────────────────────┐ │
    │  │  👤 用户        今天天气怎么样？              14:30   │ │
    │  │                                                       │ │
    │  │  🤖 AI助手      根据最新气象数据...          14:30   │ │
    │  │                 今天是晴天，气温18-25℃，...        │ │
    │  │                                                       │ │
    │  │  👤 用户        那明天呢？                    14:31   │ │
    │  │                                                       │ │
    │  │  🤖 AI助手      明天预计多云转阴...          14:31   │ │
    │  │                 气温15-22℃，建议带伞              │ │
    │  │                                                       │ │
    │  │  🤖 AI助手      💡 还有什么我可以帮您的吗？   14:31   │ │
    │  │                 [查询天气] [日程安排] [其他]      │ │
    │  └───────────────────────────────────────────────────────┘ │
    ├─────────────────────────────────────────────────────────────┤
    │  ┌─────────────────────────────────────────┐ ┌───────────┐ │
    │  │  输入您的消息...             📎 语音🎤   │ │  发送 ➤   │ │
    │  └─────────────────────────────────────────┘ └───────────┘ │
    │                                                              │
    │  快捷回复: [今天天气] [帮助] [清空对话] [联系人工]          │
    └─────────────────────────────────────────────────────────────┘
    """,
    features=[
        "💬 多轮对话 - 上下文理解，连贯对话体验",
        "📝 消息历史 - 自动保存对话历史，支持回看",
        "⚡ 快捷回复 - 预设常用问题，一键发送",
        "🎤 语音输入 - 支持语音转文字输入",
        "📎 文件上传 - 支持发送图片、文档等附件",
        "💡 智能建议 - 根据上下文推荐相关问题",
        "🔍 搜索功能 - 在历史对话中搜索关键词",
        "🌙 深色模式 - 支持明暗主题切换",
        "📱 移动端优化 - 完美适配手机浏览器",
        "🚀 流式响应 - 打字机效果，实时显示回复",
    ],
    code_skeleton="""
import streamlit as st
from datetime import datetime
from typing import List, Dict

# ==================== 配置区 ====================
BOT_NAME = "{{bot_name}}"  # 机器人名称
BOT_AVATAR = "{{bot_avatar}}"  # 机器人头像
USER_AVATAR = "{{user_avatar}}"  # 用户头像
MAX_HISTORY = {{max_history}}  # 最大历史记录数
ENABLE_VOICE = {{enable_voice}}  # 启用语音输入
STREAM_RESPONSE = {{stream_response}}  # 流式响应

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=f"{BOT_NAME}",
    page_icon="🤖",
    layout="centered"
)

# ==================== 初始化会话状态 ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

# ==================== 顶部栏 ====================
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.title(f"🤖 {BOT_NAME}")

with col2:
    if st.button("⚙️ 设置"):
        with st.sidebar:
            st.subheader("🛠️ 设置")
            temperature = st.slider("回复随机性", 0.0, 1.0, 0.7)
            max_tokens = st.slider("最大长度", 50, 500, 200)

with col3:
    if st.button("🕐 历史"):
        st.sidebar.subheader("📜 对话历史")
        for i, msg in enumerate(st.session_state.messages[-10:]):
            with st.sidebar:
                st.write(f"{msg['role']}: {msg['content'][:50]}...")

# ==================== 消息显示区域 ====================
st.divider()

# 创建消息容器
message_container = st.container()

with message_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

            # 显示附件
            if "attachments" in message:
                for attachment in message["attachments"]:
                    if attachment["type"] == "image":
                        st.image(attachment["url"])

# ==================== 用户输入区域 ====================
st.divider()

# 快捷回复
quick_replies = ["今天天气", "帮助", "清空对话", "联系人工"]
if st.session_state.messages:
    # 根据上下文动态推荐
    quick_replies.extend(["继续", "换一个说法", "详细说明"])

selected_quick_reply = st.tabs(["💬 对话"])[0].selectbox(
    "快捷回复",
    options=[""] + quick_replies,
    label_visibility="collapsed"
)

# 输入框和发送按钮
col1, col2, col3 = st.columns([5, 1, 1])

with col1:
    user_input = st.text_input(
        "输入您的消息...",
        value=selected_quick_reply,
        placeholder="输入您的消息...",
        label_visibility="collapsed"
    )

with col2:
    uploaded_file = st.file_uploader("", type=["png", "jpg", "pdf"], label_visibility="collapsed")

with col3:
    send_button = st.button("发送 ➤", use_container_width=True)

# 语音输入（可选）
if ENABLE_VOICE:
    if st.button("🎤 语音输入"):
        st.info("🎤 正在录音...\\n\\n请说话")
        # 集成语音识别功能
        # transcribed_text = transcribe_audio()

# ==================== 发送消息逻辑 ====================
if send_button and user_input:
    # 添加用户消息
    user_message = {
        "role": "user",
        "content": user_input,
        "avatar": USER_AVATAR,
        "timestamp": datetime.now().strftime("%H:%M")
    }

    if uploaded_file:
        user_message["attachments"] = [{
            "type": "file",
            "name": uploaded_file.name,
            "size": f"{len(uploaded_file.getvalue())} bytes"
        }]

    st.session_state.messages.append(user_message)

    # 模拟 AI 回复
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        if STREAM_RESPONSE:
            # 流式响应
            response_placeholder = st.empty()
            response = ""

            # 模拟逐字输出
            ai_response = f"感谢您的提问：「{user_input}」\\n\\n这是一个模拟的 AI 回复。在实际应用中，这里会调用 LLM API 生成真实的回复内容。"
            for char in ai_response:
                response += char
                response_placeholder.markdown(response + "▌")
                import time
                time.sleep(0.02)

            response_placeholder.markdown(response)
        else:
            # 直接显示
            ai_response = f"感谢您的提问：「{user_input}」\\n\\n这是一个模拟的 AI 回复。"
            st.markdown(ai_response)
            response = ai_response

    # 保存 AI 回复
    assistant_message = {
        "role": "assistant",
        "content": response,
        "avatar": BOT_AVATAR,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    st.session_state.messages.append(assistant_message)

    # 限制历史记录数量
    if len(st.session_state.messages) > MAX_HISTORY * 2:
        st.session_state.messages = st.session_state.messages[-MAX_HISTORY * 2:]

    st.rerun()

# ==================== 底部操作 ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.rerun()

with col2:
    if st.button("📥 导出对话"):
        import json
        st.download_button(
            "下载 JSON",
            data=json.dumps(st.session_state.messages, ensure_ascii=False),
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

with col3:
    if st.button("🔄 重新生成"):
        if st.session_state.messages:
            st.session_state.messages = st.session_state.messages[:-1]
            st.rerun()

with col4:
    st.write(f"💬 共 {len([m for m in st.session_state.messages if m['role'] == 'user'])} 条对话")
""",
    props=[
        ComponentProp("bot_name", "str", "AI助手", False, "机器人名称"),
        ComponentProp("bot_avatar", "str", "🤖", False, "机器人头像 emoji"),
        ComponentProp("user_avatar", "str", "👤", False, "用户头像 emoji"),
        ComponentProp("max_history", "int", 50, False, "最大历史消息数"),
        ComponentProp("enable_voice", "bool", False, False, "启用语音输入"),
        ComponentProp("stream_response", "bool", True, False, "流式响应效果"),
    ],
    tags=["聊天", "AI", "对话", "客服"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "healthcare", "finance", "ecommerce", "education"],
)


# ============================================================================
# 3. FormWizardPage - 分步表单
# ============================================================================

FORM_WIZARD_PAGE = LargeComponent(
    id="form_wizard_page",
    name="分步表单向导",
    category=LargeComponentCategory.FORM,
    description="""
    多步骤表单向导，将复杂表单分解为多个简单步骤。
    适用于用户注册、产品配置、问卷调查等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────────────┐
    │  📝 用户注册向导                                             │
    ├─────────────────────────────────────────────────────────────┤
    │  步骤进度:                                                   │
    │  ┌────┐    ┌────┐    ┌────┐    ┌────┐                     │
    │  │ 1  │ ➜ │ 2  │ ➜ │ 3  │ ➜ │ 4  │                     │
    │  │账号│    │信息│    │偏好│    │确认│                     │
    │  └────┘    └────┘    └────┘    └────┘                     │
    │   ✓ 当前                                                     │
    ├─────────────────────────────────────────────────────────────┤
    │  步骤 2/4: 基本信息                                         │
    │                                                              │
    │  姓名:           [________________]  ⚠️ 请输入姓名        │
    │                                                              │
    │  性别:           ○ 男  ○ 女  ○ 其他                         │
    │                                                              │
    │  出生日期:       [📅 选择日期]                               │
    │                                                              │
    │  所在城市:       [请选择 ▼]                                  │
    │                  └─ 北京 └─ 上海 └─ 广州 ...                │
    │                                                              │
    │  联系方式:       [手机] [邮箱] [微信]                       │
    │                                                              │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 💡 提示: 请填写真实信息，以便我们为您提供更好的服务  │   │
    │  └─────────────────────────────────────────────────────┘   │
    ├─────────────────────────────────────────────────────────────┤
    │  ┌──────────┐                       ┌──────────┐           │
    │  │  ◀ 上一步 │                       │  下一步 ▶  │           │
    │  └──────────┘                       └──────────┘           │
    │                                                              │
    │  进度: ████████░░░░░░░░░░░░ 50%                              │
    └─────────────────────────────────────────────────────────────┘
    """,
    features=[
        "📊 进度指示器 - 清晰显示当前步骤和整体进度",
        "⬅️➡️ 步骤导航 - 支持前后移动和跳转",
        "✅ 表单验证 - 每步独立验证，错误提示清晰",
        "💾 自动保存 - 定期保存草稿，防止数据丢失",
        "🔙 上一步可编辑 - 返回修改已填内容",
        "📋 步骤摘要 - 每步显示已填信息摘要",
        "🎯 必填标记 - 清晰标识必填字段",
        "💡 帮助提示 - 每个字段的说明和示例",
        "🚀 提交确认 - 最终确认页面，回顾所有信息",
        "📱 响应式 - 适配各种设备屏幕",
    ],
    code_skeleton="""
import streamlit as st
from typing import List, Dict, Callable

# ==================== 配置区 ====================
WIZARD_TITLE = "{{wizard_title}}"  # 向导标题
TOTAL_STEPS = {{total_steps}}  # 总步骤数
ENABLE_AUTO_SAVE = {{enable_auto_save}}  # 启用自动保存
SHOW_SUMMARY = {{show_summary}}  # 显示确认摘要

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=WIZARD_TITLE,
    page_icon="📝",
    layout="centered"
)

# ==================== 定义步骤 ====================
STEPS = [
    {
        "id": "account",
        "title": "账号设置",
        "icon": "🔐",
        "fields": ["username", "email", "password"]
    },
    {
        "id": "basic",
        "title": "基本信息",
        "icon": "👤",
        "fields": ["name", "gender", "birthdate", "city"]
    },
    {
        "id": "preferences",
        "title": "偏好设置",
        "icon": "⚙️",
        "fields": ["interests", "notifications", "language"]
    },
    {
        "id": "confirm",
        "title": "确认信息",
        "icon": "✅",
        "fields": []
    }
]

# ==================== 初始化会话状态 ====================
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 0

if "wizard_data" not in st.session_state:
    st.session_state.wizard_data = {}

if "wizard_completed" not in st.session_state:
    st.session_state.wizard_completed = False

# ==================== 页面标题 ====================
st.title(f"📝 {WIZARD_TITLE}")
st.divider()

# ==================== 进度指示器 ====================
def render_progress_indicator(current_step: int, steps: List[Dict]):
    \"\"\"渲染步骤进度指示器\"\"\"
    cols = st.columns(len(steps))

    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            # 步骤状态
            if i < current_step:
                st.success(f\"✓ {step['title']}\")
            elif i == current_step:
                st.info(f\"📍 {step['title']}\")
            else:
                st.caption(f\"⬜ {step['title']}\")

            # 连接线
            if i < len(steps) - 1:
                st.write(\"---\")

render_progress_indicator(st.session_state.wizard_step, STEPS)

# 进度条
progress_percent = (st.session_state.wizard_step + 1) / len(STEPS) * 100
st.progress(progress_percent / 100)
st.caption(f\"进度: {progress_percent:.0f}% ({st.session_state.wizard_step + 1}/{len(STEPS)})\")

st.divider()

# ==================== 步骤内容 ====================
current_step_data = STEPS[st.session_state.wizard_step]

st.header(f\"{current_step_data['icon']} 步骤 {st.session_state.wizard_step + 1}/{len(STEPS)}: {current_step_data['title']}\")

# === 步骤 1: 账号设置 ===
if st.session_state.wizard_step == 0:
    st.session_state.wizard_data['username'] = st.text_input(
        \"用户名\",
        value=st.session_state.wizard_data.get('username', ''),
        help=\"3-20个字符，字母数字组合\"
    )

    st.session_state.wizard_data['email'] = st.text_input(
        \"邮箱\",
        value=st.session_state.wizard_data.get('email', ''),
        help=\"用于接收通知和找回密码\"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.wizard_data['password'] = st.text_input(
            \"密码\",
            type=\"password\",
            help=\"至少8位，包含字母和数字\"
        )
    with col2:
        st.session_state.wizard_data['confirm_password'] = st.text_input(
            \"确认密码\",
            type=\"password\"
        )

# === 步骤 2: 基本信息 ===
elif st.session_state.wizard_step == 1:
    col1, col2 = st.columns(2)

    with col1:
        st.session_state.wizard_data['name'] = st.text_input(
            \"姓名\",
            value=st.session_state.wizard_data.get('name', '')
        )

        st.session_state.wizard_data['gender'] = st.radio(
            \"性别\",
            [\"男\", \"女\", \"其他\"],
            horizontal=True
        )

    with col2:
        st.session_state.wizard_data['birthdate'] = st.date_input(
            \"出生日期\",
            help=\"必须年满18岁\"
        )

        st.session_state.wizard_data['city'] = st.selectbox(
            \"所在城市\",
            [\"北京\", \"上海\", \"广州\", \"深圳\", \"杭州\", \"其他\"]
        )

    st.session_state.wizard_data['phone'] = st.text_input(
        \"手机号码\",
        help=\"用于身份验证和紧急联系\"
    )

# === 步骤 3: 偏好设置 ===
elif st.session_state.wizard_step == 2:
    st.subheader(\"兴趣领域\")
    st.session_state.wizard_data['interests'] = st.multiselect(
        \"选择您感兴趣的领域\",
        [\"科技\", \"财经\", \"体育\", \"娱乐\", \"教育\", \"健康\", \"旅游\"],
        default=st.session_state.wizard_data.get('interests', [])
    )

    st.subheader(\"通知设置\")
    st.session_state.wizard_data['notifications'] = st.checkbox(
        \"接收邮件通知\",
        value=st.session_state.wizard_data.get('notifications', True)
    )

    st.session_state.wizard_data['language'] = st.selectbox(
        \"语言偏好\",
        [\"简体中文\", \"English\", \"日本語\"]
    )

# === 步骤 4: 确认信息 ===
elif st.session_state.wizard_step == 3:
    st.success(\"🎉 即将完成！请确认以下信息\")

    # 显示摘要
    for step in STEPS[:-1]:
        with st.expander(f\"{step['icon']} {step['title']}\", expanded=True):
            for field in step['fields']:
                if field in st.session_state.wizard_data:
                    st.write(f\"**{field}:** {st.session_state.wizard_data[field]}\")

    if st.checkbox(\"我确认以上信息真实有效，并同意服务条款\", key=\"agree_terms\"):
        st.session_state.wizard_completed = True
    else:
        st.session_state.wizard_completed = False

# ==================== 导航按钮 ====================
st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button(\"◀ 上一步\", use_container_width=True):
        if st.session_state.wizard_step > 0:
            st.session_state.wizard_step -= 1
            st.rerun()

with col3:
    if st.button(\"下一步 ▶\", use_container_width=True):
        # 验证当前步骤
        is_valid = True
        error_msg = \"\"

        # 步骤1验证
        if st.session_state.wizard_step == 0:
            if not st.session_state.wizard_data.get('username'):
                is_valid = False
                error_msg = \"请输入用户名\"
            elif '@' not in st.session_state.wizard_data.get('email', ''):
                is_valid = False
                error_msg = \"请输入有效的邮箱地址\"
            elif st.session_state.wizard_data.get('password') != st.session_state.wizard_data.get('confirm_password'):
                is_valid = False
                error_msg = \"两次密码输入不一致\"

        if is_valid:
            if st.session_state.wizard_step < len(STEPS) - 1:
                st.session_state.wizard_step += 1
                st.rerun()
        else:
            st.error(f\"⚠️ {error_msg}\")

# ==================== 提交处理 ====================
if st.session_state.wizard_step == len(STEPS) - 1:
    if st.button(\"✅ 提交注册\", type=\"primary\", use_container_width=True):
        if st.session_state.wizard_completed:
            st.success(\"🎉 注册成功！\")
            st.json(st.session_state.wizard_data)

            # 清理会话状态
            for key in list(st.session_state.keys()):
                if key.startswith('wizard_'):
                    del st.session_state[key]
        else:
            st.warning(\"请先同意服务条款\")

# ==================== 自动保存提示 ====================
if ENABLE_AUTO_SAVE:
    st.caption(f\"💾 草稿已自动保存 {datetime.now().strftime('%H:%M:%S')}\")
""",
    props=[
        ComponentProp("wizard_title", "str", "用户注册向导", False, "向导标题"),
        ComponentProp("total_steps", "int", 4, False, "总步骤数"),
        ComponentProp("enable_auto_save", "bool", True, False, "启用自动保存"),
        ComponentProp("show_summary", "bool", True, False, "显示确认摘要"),
        ComponentProp("allow_skip", "bool", False, False, "允许跳过步骤"),
        ComponentProp("show_progress", "bool", True, False, "显示进度百分比"),
    ],
    tags=["表单", "向导", "分步", "注册"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "healthcare", "finance", "ecommerce", "education"],
)


# ============================================================================
# 4. DataTablePage - 数据表格
# ============================================================================

DATA_TABLE_PAGE = LargeComponent(
    id="data_table_page",
    name="数据表格页面",
    category=LargeComponentCategory.DATA,
    description="""
    功能完善的数据表格页面，支持筛选、排序、分页、批量操作。
    适用于数据管理、列表展示、批量处理等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────────────┐
    │  📋 用户管理                              [+ 新建] [📥导入] │
    ├─────────────────────────────────────────────────────────────┤
    │  🔍 [搜索框____________] [状态▼] [角色▼]         [应用筛选] │
    │                                                              │
    │  排序: [ID↓] [注册日期↑]  |  显示: [10▼/页]  共: 1,234 条   │
    ├─────────────────────────────────────────────────────────────┤
    │  □  ID    姓名       邮箱              角色      状态  操作 │
    │  ┌───────────────────────────────────────────────────────┐ │
    │  │□  001   张三      zhang@qq.com      管理员   ✓  [✏️][🗑️] │ │
    │  │□  002   李四      li@qq.com         用户     ✓  [✏️][🗑️] │ │
    │  │□  003   王五      wang@qq.com       用户     ⏸️ [✏️][🗑️] │ │
    │  │□  004   赵六      zhao@qq.com       用户     ✓  [✏️][🗑️] │ │
    │  │□  005   钱七      qian@qq.com       访客     ✓  [✏️][🗑️] │ │
    │  │□  006   孙八      sun@qq.com        用户     ⏸️ [✏️][🗑️] │ │
    │  │□  007   周九      zhou@qq.com       用户     ✓  [✏️][🗑️] │ │
    │  └───────────────────────────────────────────────────────┘ │
    ├─────────────────────────────────────────────────────────────┤
    │  □ 全选     已选: 3     [批量删除🗑️] [批量导出📥]           │
    │                                                              │
    │  ◀ 1 2 3 4 5 ... 25 ▶        跳转: [___] 页                  │
    └─────────────────────────────────────────────────────────────┘
    """,
    features=[
        "🔍 搜索过滤 - 实时搜索，支持模糊匹配",
        "⬆️⬇️ 列排序 - 点击列头排序，支持多列",
        "📄 分页导航 - 自定义每页条数",
        "✅ 选择模式 - 单选、多选、全选",
        "🗑️ 批量操作 - 批量删除、导出、状态更新",
        "✏️ 行内编辑 - 直接在表格中编辑",
        "📥 数据导入 - 支持 CSV、Excel 导入",
        "📤 数据导出 - 导出选中或全部数据",
        "🎨 列配置 - 显示/隐藏列，调整列宽",
        "🔄 刷新数据 - 自动或手动刷新",
    ],
    code_skeleton="""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any

# ==================== 配置区 ====================
PAGE_TITLE = \"{{page_title}}\"  # 页面标题
DATA_SOURCE = \"{{data_source}}\"  # 数据源（'mock' 或 API）
DEFAULT_PAGE_SIZE = {{default_page_size}}  # 默认每页条数
ENABLE_EXPORT = {{enable_export}}  # 启用导出功能
ENABLE_BATCH_OPS = {{enable_batch_ops}}  # 启用批量操作

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=\"📋\",
    layout=\"wide\"
)

# ==================== 模拟数据生成 ====================
def generate_mock_data(num_rows: int = 100) -> pd.DataFrame:
    \"\"\"生成模拟数据\"\"\"
    import random
    names = [\"张三\", \"李四\", \"王五\", \"赵六\", \"钱七\", \"孙八\", \"周九\", \"吴十\"]
    roles = [\"管理员\", \"用户\", \"访客\", \"编辑\"]
    statuses = [\"激活\", \"禁用\", \"待审核\"]
    domains = [\"qq.com\", \"gmail.com\", \"163.com\", \"outlook.com\"]

    data = {
        \"ID\": [f\"{i:03d}\" for i in range(1, num_rows + 1)],
        \"姓名\": [random.choice(names) for _ in range(num_rows)],
        \"邮箱\": [f\"{random.choice(names)}{i}@{random.choice(domains)}\" for i in range(num_rows)],
        \"角色\": [random.choice(roles) for _ in range(num_rows)],
        \"状态\": [random.choice(statuses) for _ in range(num_rows)],
        \"注册日期\": [pd.Timestamp.now() - pd.Timedelta(days=random.randint(1, 365)) for _ in range(num_rows)],
        \"最后登录\": [pd.Timestamp.now() - pd.Timedelta(hours=random.randint(1, 72)) for _ in range(num_rows)],
    }
    return pd.DataFrame(data)

# ==================== 初始化数据 ====================
if \"data\" not in st.session_state:
    st.session_state.data = generate_mock_data()

if \"selected_rows\" not in st.session_state:
    st.session_state.selected_rows = []

if \"sort_column\" not in st.session_state:
    st.session_state.sort_column = None

if \"sort_ascending\" not in st.session_state:
    st.session_state.sort_ascending = True

# ==================== 顶部操作栏 ====================
col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

with col1:
    st.title(f\"📋 {PAGE_TITLE}\")

with col2:
    if st.button(\"+ 新建\", use_container_width=True):
        st.info(\"打开新建表单\")

with col3:
    if ENABLE_EXPORT and st.button(\"📥 导入\", use_container_width=True):
        uploaded_file = st.file_uploader(\"\", type=[\"csv\", \"xlsx\"], label_visibility=\"collapsed\")

with col4:
    if ENABLE_EXPORT and st.button(\"📤 导出\", use_container_width=True):
        st.info(\"准备导出数据\")

with col5:
    if st.button(\"🔄 刷新\", use_container_width=True):
        st.session_state.data = generate_mock_data()
        st.rerun()

st.divider()

# ==================== 筛选区域 ====================
with st.expander(\"🔍 筛选条件\", expanded=False):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        search_keyword = st.text_input(\"搜索\", placeholder=\"姓名、邮箱...\")

    with col2:
        filter_status = st.multiselect(
            \"状态\",
            options=[\"激活\", \"禁用\", \"待审核\"],
            default=[]
        )

    with col3:
        filter_role = st.multiselect(
            \"角色\",
            options=[\"管理员\", \"用户\", \"访客\", \"编辑\"],
            default=[]
        )

    with col4:
        date_range = st.date_input(\"注册日期\", value=[])

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        apply_filter = st.button(\"应用筛选\", use_container_width=True)
    with col2:
        clear_filter = st.button(\"清除\", use_container_width=True)

# ==================== 应用筛选 ====================
filtered_data = st.session_state.data.copy()

if search_keyword:
    mask = filtered_data[\"姓名\"].str.contains(search_keyword, na=False) | \
           filtered_data[\"邮箱\"].str.contains(search_keyword, na=False)
    filtered_data = filtered_data[mask]

if filter_status:
    filtered_data = filtered_data[filtered_data[\"状态\"].isin(filter_status)]

if filter_role:
    filtered_data = filtered_data[filtered_data[\"角色\"].isin(filter_role)]

# ==================== 排序和分页 ====================
# 排序
if st.session_state.sort_column:
    filtered_data = filtered_data.sort_values(
        st.session_state.sort_column,
        ascending=st.session_state.sort_ascending
    )

# 分页设置
col1, col2, col3, col4 = st.columns(4)
with col1:
    page_size = st.selectbox(\"每页显示\", [10, 20, 50, 100], index=0)

total_pages = max(1, (len(filtered_data) - 1) // page_size + 1)
with col2:
    st.write(f\"共 {len(filtered_data)} 条记录\")
with col3:
    current_page = st.number_input(\"页码\", min_value=1, max_value=total_pages, value=1)
with col4:
    st.write(f\"/ {total_pages} 页\")

# 分页切片
start_idx = (current_page - 1) * page_size
end_idx = start_idx + page_size
page_data = filtered_data.iloc[start_idx:end_idx]

# ==================== 数据表格 ====================
st.divider()

# 列配置
column_config = {
    \"ID\": st.column_config.TextColumn(\"ID\", width=\"small\"),
    \"姓名\": st.column_config.TextColumn(\"姓名\", width=\"short\"),
    \"邮箱\": st.column_config.TextColumn(\"邮箱\", width=\"medium\"),
    \"角色\": st.column_config.SelectboxColumn(
        \"角色\",
        options=[\"管理员\", \"用户\", \"访客\", \"编辑\"],
        required=True
    ),
    \"状态\": st.column_config.SelectboxColumn(
        \"状态\",
        options=[\"激活\", \"禁用\", \"待审核\"]
    ),
    \"注册日期\": st.column_config.DateColumn(\"注册日期\", width=\"short\"),
    \"最后登录\": st.column_config.DatetimeColumn(\"最后登录\", width=\"medium\", format=\"YYYY-MM-DD HH:mm\"),
}

# 显示表格
selected = st.dataframe(
    page_data,
    column_config=column_config,
    use_container_width=True,
    hide_index=True,
    on_select=\"rerun\",
    selection_mode=[\"multi-row\", \"single-column\"]
)

# 保存选中行
if selected[\"selection\"][\"rows\"]:
    st.session_state.selected_rows = page_data.iloc[selected[\"selection\"][\"rows\"]]

# ==================== 批量操作 ====================
st.divider()

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_count = len(st.session_state.selected_rows) if hasattr(st.session_state, 'selected_rows') else 0
    st.write(f\"✅ 已选择 {selected_count} 条记录\")

with col2:
    if ENABLE_BATCH_OPS and st.button(\"🗑️ 批量删除\", use_container_width=True):
        st.warning(\"确认删除选中记录？\")

with col3:
    if ENABLE_EXPORT and st.button(\"📤 导出选中\", use_container_width=True):
        if st.session_state.selected_rows is not None and len(st.session_state.selected_rows) > 0:
            csv = st.session_state.selected_rows.to_csv(index=False).encode('utf-8')
            st.download_button(
                \"下载 CSV\",
                csv,
                \"selected_data.csv\",
                \"text/csv\"
            )

# ==================== 分页导航 ====================
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])

with col1:
    if st.button(\"◀ 上一页\", use_container_width=True) and current_page > 1:
        st.session_state.current_page = current_page - 1
        st.rerun()

with col2:
    if st.button(\"下一页 ▶\", use_container_width=True) and current_page < total_pages:
        st.session_state.current_page = current_page + 1
        st.rerun()

with col5:
    jump_page = st.number_input(\"跳转\", min_value=1, max_value=total_pages, value=current_page)
    if jump_page != current_page:
        st.session_state.current_page = jump_page
        st.rerun()
""",
    props=[
        ComponentProp("page_title", "str", "用户管理", False, "页面标题"),
        ComponentProp("data_source", "str", "mock", False, "数据源类型"),
        ComponentProp("default_page_size", "int", 10, False, "默认每页条数"),
        ComponentProp("enable_export", "bool", True, False, "启用导出功能"),
        ComponentProp("enable_batch_ops", "bool", True, False, "启用批量操作"),
        ComponentProp("enable_inline_edit", "bool", True, False, "启用行内编辑"),
    ],
    tags=["表格", "数据", "列表", "管理"],
    dependencies=["streamlit", "pandas"],
    industry_compatibility=["general", "finance", "healthcare", "manufacturing", "ecommerce"],
)


# ============================================================================
# 5. SettingsPage - 设置中心
# ============================================================================

SETTINGS_PAGE = LargeComponent(
    id="settings_page",
    name="设置中心",
    category=LargeComponentCategory.SETTINGS,
    description="""
    分组化的设置页面，支持多种设置类型和即时保存。
    适用于用户偏好、系统配置、账户设置等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────────────┐
    │  ⚙️ 设置中心                                  [保存] [取消] │
    ├─────────────────────────────────────────────────────────────┤
    │  ┌─────────┬───────────────────────────────────────────┐   │
    │  │  🎨 外观 │ 当前主题: 🌙 暗黑模式                     │   │
    │  │  👤 账户 │                                           │   │
    │  │  🔔 通知 │ □ 启用桌面通知                            │   │
    │  │         │ □ 启用邮件通知                            │   │
    │  │  🔒 隐私 │ ⚠️ 通知邮箱: [user@example.com]        │   │
    │  │  🌐 语言 │                                           │   │
    │  │  💾 存储 │ ○ 完全公开  ○ 仅好友  ⦿ 仅自己         │   │
    │  │         │                                           │   │
    │  │  ❓ 帮助 │ 语言: [简体中文 ▼]                       │   │
    │  │         │                                           │   │
    │  │         │ 存储空间: ████████░░░░ 2.3GB / 5GB         │   │
    │  │         │                                           │   │
    │  │         │ [清理缓存]  [管理数据]                     │   │
    │  └─────────┴───────────────────────────────────────────┘   │
    │                                                              │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ ⚠️ 危险操作                                          │   │
    │  │                                                     │   │
    │  │ [导出数据]  [删除账户]  [重置所有设置]               │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                              │
    │  💾 所有更改自动保存                                      │
    └─────────────────────────────────────────────────────────────┘
    """,
    features=[
        "📂 分组设置 - 按功能区域分组，清晰易找",
        "💾 自动保存 - 修改即时保存，无需手动",
        "🔄 即时预览 - 设置变更实时生效",
        "🌙 主题切换 - 支持亮色/暗色/自动模式",
        "🌍 多语言 - 支持语言切换",
        "🔔 通知管理 - 细粒度通知控制",
        "🔒 隐私设置 - 可见性、数据共享控制",
        "📊 存储管理 - 空间使用展示，清理缓存",
        "⚠️ 危险区 - 数据导出、账户删除等敏感操作",
        "🔍 搜索设置 - 快速查找设置项",
    ],
    code_skeleton="""
import streamlit as st
from typing import Dict, Any, List

# ==================== 配置区 ====================
PAGE_TITLE = \"{{page_title}}\"  # 页面标题
AUTO_SAVE = {{auto_save}}  # 自动保存
SHOW_PREVIEW = {{show_preview}}  # 显示即时预览
ENABLE_DANGER_ZONE = {{enable_danger_zone}}  # 显示危险操作区

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=\"⚙️\",
    layout=\"wide\"
)

# ==================== 初始化设置 ====================
if \"settings\" not in st.session_state:
    st.session_state.settings = {
        \"theme\": \"light\",
        \"language\": \"zh-CN\",
        \"notifications\": {
            \"desktop\": True,
            \"email\": False,
            \"sms\": False
        },
        \"privacy\": \"private\",
        \"storage_used\": 2.3,
        \"storage_total\": 5.0,
    }

# ==================== 顶部栏 ====================
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.title(f\"⚙️ {PAGE_TITLE}\")

with col2:
    if st.button(\"保存\", use_container_width=True):
        st.success(\"✅ 设置已保存\")

with col3:
    if st.button(\"重置\", use_container_width=True):
        if st.confirm(\"确定重置所有设置？\"):
            st.info(\"设置已重置\")

st.divider()

# ==================== 设置分组 ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([\"🎨 外观\", \"👤 账户\", \"🔔 通知\", \"🔒 隐私\", \"🌐 语言\", \"💾 存储\"])

# === 外观设置 ===
with tab1:
    st.subheader(\"主题设置\")

    # 主题选择
    theme = st.radio(
        \"选择主题\",
        [\"🌞 浅色模式\", \"🌙 暗黑模式\", \"🔄 跟随系统\"],
        index=[\"light\", \"dark\", \"auto\"].index(st.session_state.settings.get(\"theme\", \"light\"))
    )
    st.session_state.settings[\"theme\"] = {\"🌞 浅色模式\": \"light\", \"🌙 暗黑模式\": \"dark\", \"🔄 跟随系统\": \"auto\"}[theme]

    # 即时预览
    if SHOW_PREVIEW:
        st.write(\"**预览:**\")
        if st.session_state.settings[\"theme\"] == \"dark\":
            st.info(\"🌙 暗黑模式预览\")
        else:
            st.success(\"🌞 浅色模式预览\")

    # 字体大小
    font_size = st.slider(\"字体大小\", 12, 20, 16)
    st.session_state.settings[\"font_size\"] = font_size

    # 侧边栏位置
    sidebar_position = st.selectbox(\"侧边栏位置\", [\"左侧\", \"右侧\", \"隐藏\"])
    st.session_state.settings[\"sidebar_position\"] = sidebar_position

# === 账户设置 ===
with tab2:
    st.subheader(\"账户信息\")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(\"用户名\", value=\"current_user\", disabled=True)
    with col2:
        st.text_input(\"邮箱\", value=\"user@example.com\", disabled=True)

    st.divider()

    # 修改密码
    with st.expander(\"🔑 修改密码\"):
        col1, col2 = st.columns(2)
        with col1:
            current_password = st.text_input(\"当前密码\", type=\"password\")
        with col2:
            new_password = st.text_input(\"新密码\", type=\"password\")
        confirm_password = st.text_input(\"确认新密码\", type=\"password\")

        if st.button(\"更新密码\"):
            if new_password == confirm_password:
                st.success(\"密码已更新\")

    # 绑定手机
    with st.expander(\"📱 绑定手机\"):
        phone = st.text_input(\"手机号码\", placeholder=\"请输入手机号\")
        verification_code = st.text_input(\"验证码\", max_chars=6\")
        col1, col2 = st.columns(2)
        with col1:
            st.button(\"获取验证码\")
        with col2:
            st.button(\"确认绑定\")

# === 通知设置 ===
with tab3:
    st.subheader(\"通知偏好\")

    notification_types = [
        (\"desktop\", \"💻 桌面通知\", \"在浏览器中显示通知\"),
        (\"email\", \"📧 邮件通知\", \"发送通知到邮箱\"),
        (\"sms\", \"📱 短信通知\", \"发送短信通知（可能产生费用）\")
    ]

    for key, label, desc in notification_types:
        enabled = st.checkbox(
            f\"{label}\",
            value=st.session_state.settings[\"notifications\"].get(key, False),
            help=desc
        )
        st.session_state.settings[\"notifications\"][key] = enabled
        st.caption(desc)

    st.divider()

    # 通知内容
    st.write(\"**接收哪些通知:**\")
    notification_content = st.multiselect(
        \"\",
        [\"新消息提醒\", \"系统更新\", \"活动通知\", \"安全警告\"],
        default=[\"新消息提醒\", \"安全警告\"]
    )
    st.session_state.settings[\"notification_content\"] = notification_content

# === 隐私设置 ===
with tab4:
    st.subheader(\"隐私控制\")

    # 账户可见性
    privacy_level = st.radio(
        \"谁可以看到我的资料\",
        [\"🌍 完全公开\", \"👥 仅好友\", \"🔒 仅自己\"],
        index=1
    )
    st.session_state.settings[\"privacy\"] = {\"🌍 完全公开\": \"public\", \"👥 仅好友\": \"friends\", \"🔒 仅自己\": \"private\"}[privacy_level]

    st.caption(\"选择谁可以查看您的个人资料和活动\")

    # 数据共享
    st.divider()
    st.write(\"**数据共享设置:**\")
    data_sharing = st.checkbox(
        \"允许分析匿名使用数据以改进服务\",
        value=False,
        help=\"开启后，我们会收集匿名使用数据\"
    )
    st.session_state.settings[\"data_sharing\"] = data_sharing

    # 活动状态
    show_online = st.checkbox(\"显示在线状态\", value=True)
    st.session_state.settings[\"show_online\"] = show_online

# === 语言设置 ===
with tab5:
    st.subheader(\"语言与地区\")

    # 界面语言
    language = st.selectbox(
        \"界面语言\",
        [\"简体中文\", \"English\", \"日本語\", \"한국어\"],
        index=0
    )
    st.session_state.settings[\"language\"] = {\"简体中文\": \"zh-CN\", \"English\": \"en\", \"日本語\": \"ja\", \"한국어\": \"ko\"}[language]

    # 时区
    timezone = st.selectbox(
        \"时区\",
        [\"Asia/Shanghai\", \"America/New_York\", \"Europe/London\", \"Asia/Tokyo\"]
    )
    st.session_state.settings[\"timezone\"] = timezone

    # 日期格式
    date_format = st.selectbox(\"日期格式\", [\"YYYY-MM-DD\", \"MM/DD/YYYY\", \"DD/MM/YYYY\"])
    st.session_state.settings[\"date_format\"] = date_format

# === 存储管理 ===
with tab6:
    st.subheader(\"存储空间\")

    # 存储使用情况
    storage_used = st.session_state.settings[\"storage_used\"]
    storage_total = st.session_state.settings[\"storage_total\"]
    storage_percent = (storage_used / storage_total) * 100

    st.metric(\"已使用\", f\"{storage_used} GB\", f\"/ {storage_total} GB\")

    # 进度条
    st.progress(storage_percent / 100)
    st.caption(f\"使用了 {storage_percent:.1f}% 的存储空间\")

    # 存储分布
    st.divider()
    st.write(\"**存储分布:**\")
    col1, col2 = st.columns(2)
    with col1:
        st.write(\"📄 文档: 1.2 GB\")
        st.write(\"🖼️ 图片: 0.8 GB\")
    with col2:
        st.write(\"🎬 视频: 0.2 GB\")
        st.write(\"🗑️ 缓存: 0.1 GB\")

    # 操作按钮
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(\"🧹 清理缓存\", use_container_width=True):
            st.success(\"已清理 0.1 GB 缓存\")

    with col2:
        if st.button(\"📊 查看详情\", use_container_width=True):
            st.info(\"显示详细存储分析\")

    with col3:
        if st.button(\"⬆️ 升级存储\", use_container_width=True):
            st.info(\"跳转到升级页面\")

# ==================== 危险操作区 ====================
st.divider()

if ENABLE_DANGER_ZONE:
    with st.expander(\"⚠️ 危险操作\", expanded=False):
        st.warning(\"以下操作不可逆，请谨慎操作！\")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(\"📥 导出数据\", use_container_width=True):
                st.info(\"准备导出所有数据...\")

        with col2:
            if st.button(\"🗑️ 删除账户\", use_container_width=True):
                st.error(\"⚠️ 此操作不可逆！\")
                if st.checkbox(\"我确认要删除账户\", key=\"confirm_delete\"):
                    st.error(\"账户删除功能需要二次确认\")

        with col3:
            if st.button(\"🔄 重置设置\", use_container_width=True):
                if st.checkbox(\"我确认要重置\", key=\"confirm_reset\"):
                    st.success(\"设置已重置为默认\")

# ==================== 底部信息 ====================
st.divider()

if AUTO_SAVE:
    from datetime import datetime
    st.caption(f\"💾 所有更改自动保存于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\")
else:
    st.caption(\"⚠️ 请记得保存更改\")

# 显示当前设置（调试用）
with st.expander(\"🔧 查看当前设置\", expanded=False):
    st.json(st.session_state.settings)
""",
    props=[
        ComponentProp("page_title", "str", "设置中心", False, "页面标题"),
        ComponentProp("auto_save", "bool", True, False, "自动保存更改"),
        ComponentProp("show_preview", "bool", True, False, "显示即时预览"),
        ComponentProp("enable_danger_zone", "bool", True, False, "显示危险操作区"),
        ComponentProp("enable_search", "bool", True, False, "启用设置搜索"),
    ],
    tags=["设置", "配置", "偏好", "管理"],
    dependencies=["streamlit"],
    industry_compatibility=["general"],
)


# ============================================================================
# 6. LandingPage - 落地页
# ============================================================================

LANDING_PAGE = LargeComponent(
    id="landing_page",
    name="营销落地页",
    category=LargeComponentCategory.MARKETING,
    description="""
    高转化率的营销落地页，包含 Hero 区域、特性展示、CTA 按钮。
    适用于产品推广、活动宣传、用户获取等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────────────┐
    │  🏠 品牌 | 产品 | 关于 | 联系              [登录] [注册→] │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │           🚀 革命性的产品，改变您的工作方式                │
    │                                                              │
    │     人工智能驱动的智能平台，让效率提升10倍                  │
    │     [免费试用] [观看演示] [了解更多 ▼]                      │
    │                                                              │
    │     ⭐⭐⭐⭐⭐ 10,000+ 用户信赖的选择                        │
    │                                                              │
    ├─────────────────────────────────────────────────────────────┤
    │  ✨ 核心特性                                                │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
    │  │  ⚡ 高效  │  │  🎯 精准  │  │  🔒 安全  │  │  🌐 全球  │  │
    │  │         │  │         │  │         │  │         │  │
    │  │ AI驱动  │  │ 智能推荐  │  │ 数据加密  │  │ 多语言  │  │
    │  │ 效率10x  │  │ 精准匹配  │  │ 合规认证  │  │ 全球部署  │  │
    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
    ├─────────────────────────────────────────────────────────────┤
    │  💬 用户评价                                                │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ \"这个产品彻底改变了我们的工作流程！\"              │   │
    │  │                                                     │   │
    │  │ ─ 张三，某科技公司CEO                               │   │
    │  │    ⭐⭐⭐⭐⭐                                        │   │
    │  └─────────────────────────────────────────────────────┘   │
    │  [◀] [用户] [用户] [用户] [用户] [▶]                     │
    ├─────────────────────────────────────────────────────────────┤
    │  📊 数据证明                                                │
    │  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
    │  │  10,000+ │ │   50+    │ │   99.9%  │                 │
    │  │  活跃用户│ │  国家地区│ │   正常率│                 │
    │  └──────────┘ └──────────┘ └──────────┘                 │
    ├─────────────────────────────────────────────────────────────┤
    │  📢 立即开始                                                │
    │           🎁 免费试用 14 天，无需信用卡                     │
    │                                                              │
    │        [开始免费试用 →]     [预约演示 →]                   │
    │                                                              │
    │        已有 50,000+ 企业加入                                │
    └─────────────────────────────────────────────────────────────┘
    """,
    features=[
        "🎯 Hero 区域 - 强烈的视觉冲击和核心价值主张",
        "✨ 特性展示 - 清晰展示产品核心功能",
        "💬 用户评价 - 社会证明，建立信任",
        "📊 数据统计 - 用数字说话，展示实力",
        "🎁 CTA 按钮 - 多个转化点，引导用户行动",
        "🎬 视频演示 - 嵌入产品介绍视频",
        "📱 响应式设计 - 完美适配各种设备",
        "🌐 多语言支持 - 国际化落地页",
        "🔗 A/B 测试 - 支持多个版本测试",
        "📊 转化追踪 - 集成分析工具",
    ],
    code_skeleton="""
import streamlit as st
from typing import List, Dict

# ==================== 配置区 ====================
PRODUCT_NAME = \"{{product_name}}\"  # 产品名称
TAGLINE = \"{{tagline}}\"  # 产品标语
CTA_BUTTON_TEXT = \"{{cta_button_text}}\"  # CTA按钮文字
THEME_COLOR = \"{{theme_color}}\"  # 主题颜色

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=f\"{PRODUCT_NAME} - 革命性的产品\",
    page_icon=\"🚀\",
    layout=\"wide\",
    initial_sidebar_state=\"collapsed\"
)

# 隐藏侧边栏和菜单
st.markdown(\"\"\"
<style>
    [data-testid=\"stSidebar\"] {display: none;}
    [data-testid=\"stHeader\"] {display: none;}
    .main {padding-top: 0;}
</style>
\"\"\", unsafe_allow_html=True)

# ==================== 导航栏 ====================
st.markdown(\"\"\"
<nav style=\"display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: #f8f9fa; border-bottom: 1px solid #dee2e6;\">
    <div style=\"font-size: 1.5rem; font-weight: bold;\">🏠 {PRODUCT_NAME}</div>
    <div style=\"display: flex; gap: 2rem;\">
        <a href=\"#features\" style=\"text-decoration: none; color: #333;\">产品</a>
        <a href=\"#pricing\" style=\"text-decoration: none; color: #333;\">价格</a>
        <a href=\"#testimonials\" style=\"text-decoration: none; color: #333;\">用户评价</a>
        <a href=\"#contact\" style=\"text-decoration: none; color: #333;\">联系我们</a>
    </div>
    <div style=\"display: flex; gap: 0.5rem;\">
        <button style=\"padding: 0.5rem 1rem; border: 1px solid #007bff; background: white; color: #007bff; border-radius: 4px; cursor: pointer;\">登录</button>
        <button style=\"padding: 0.5rem 1rem; border: none; background: #007bff; color: white; border-radius: 4px; cursor: pointer;\">注册</button>
    </div>
</nav>
\"\"\", unsafe_allow_html=True)

# ==================== Hero 区域 ====================
st.markdown(\"\"\"
<section style=\"text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;\">
    <h1 style=\"font-size: 3rem; margin-bottom: 1rem;\">🚀 {TAGLINE}</h1>
    <p style=\"font-size: 1.25rem; margin-bottom: 2rem; opacity: 0.9;\">
        人工智能驱动的智能平台，让效率提升10倍
    </p>
    <div style=\"display: flex; gap: 1rem; justify-content: center; margin-bottom: 2rem;\">
        <button style=\"padding: 1rem 2rem; font-size: 1.1rem; border: none; background: white; color: #667eea; border-radius: 8px; cursor: pointer; font-weight: bold;\">
            免费试用
        </button>
        <button style=\"padding: 1rem 2rem; font-size: 1.1rem; border: 2px solid white; background: transparent; color: white; border-radius: 8px; cursor: pointer;\">
            观看演示
        </button>
    </div>
    <p style=\"opacity: 0.8;\">⭐⭐⭐⭐⭐ 10,000+ 用户信赖的选择</p>
</section>
\"\"\", unsafe_allow_html=True)

# ==================== 特性展示 ====================
st.markdown(\"---\")
st.markdown(\"<section id='features'>\", unsafe_allow_html=True)

st.markdown(\"<h2 style='text-align: center; margin-bottom: 2rem;'>✨ 核心特性</h2>\", unsafe_allow_html=True)

features = [
    {
        \"icon\": \"⚡\",
        \"title\": \"高效\",
        \"subtitle\": \"AI驱动\",
        \"description\": \"效率提升10倍\",
        \"detail\": \"智能算法优化工作流程，自动化处理重复任务\"
    },
    {
        \"icon\": \"🎯\",
        \"title\": \"精准\",
        \"subtitle\": \"智能推荐\",
        \"description\": \"精准匹配\",
        \"detail\": \"基于机器学习的个性化推荐系统\"
    },
    {
        \"icon\": \"🔒\",
        \"title\": \"安全\",
        \"subtitle\": \"数据加密\",
        \"description\": \"合规认证\",
        \"detail\": \"银行级安全标准，通过多项合规认证\"
    },
    {
        \"icon\": \"🌐\",
        \"title\": \"全球\",
        \"subtitle\": \"多语言\",
        \"description\": \"全球部署\",
        \"detail\": \"支持50+语言，服务覆盖全球100+国家\"
    }
]

cols = st.columns(4)
for col, feature in zip(cols, features):
    with col:
        st.markdown(f\"\"\"
<div style=\"text-align: center; padding: 2rem 1rem;\">
    <div style=\"font-size: 3rem; margin-bottom: 1rem;\">{feature['icon']}</div>
    <h3 style=\"margin-bottom: 0.5rem;\">{feature['title']}</h3>
    <p style=\"color: #666; margin-bottom: 0.5rem;\">{feature['subtitle']}</p>
    <p style=\"font-weight: bold; color: #007bff; margin-bottom: 1rem;\">{feature['description']}</p>
    <p style=\"font-size: 0.9rem; color: #999;\">{feature['detail']}</p>
</div>
\"\"\", unsafe_allow_html=True)

st.markdown(\"</section>\", unsafe_allow_html=True)

# ==================== 数据证明 ====================
st.markdown(\"---\")

st.markdown(\"<h2 style='text-align: center; margin-bottom: 2rem;'>📊 数据证明</h2>\", unsafe_allow_html=True)

metrics = [
    (\"10,000+\", \"活跃用户\", \"个人和企业用户\"),
    (\"50+\", \"国家地区\", \"全球覆盖\"),
    (\"99.9%\", \"正常率\", \"7x24小时稳定运行\"),
    (\"24/7\", \"技术支持\", \"全天候服务\")
]

cols = st.columns(4)
for col, (value, label, desc) in zip(cols, metrics):
    with col:
        st.metric(label, value)
        st.caption(desc)

# ==================== 用户评价 ====================
st.markdown(\"---\")
st.markdown(\"<section id='testimonials'>\", unsafe_allow_html=True)

st.markdown(\"<h2 style='text-align: center; margin-bottom: 2rem;'>💬 用户评价</h2>\", unsafe_allow_html=True)

testimonials = [
    {
        \"content\": \"这个产品彻底改变了我们的工作流程！效率提升了整整10倍。\",
        \"author\": \"张三\",
        \"title\": \"某科技公司 CEO\",
        \"rating\": 5
    },
    {
        \"content\": \"简单易用，功能强大。客户服务响应非常及时。\",
        \"author\": \"李四\",
        \"title\": \"创业公司创始人\",
        \"rating\": 5
    },
    {
        \"content\": \"最好的决策工具，帮我们节省了大量时间和成本。\",
        \"author\": \"王五\",
        \"title\": \"产品经理\",
        \"rating\": 5
    }
]

col1, col2, col3 = st.columns(3)

for col, testimonial in zip([col1, col2, col3], testimonials):
    with col:
        st.markdown(f\"\"\"
<div style=\"padding: 2rem; background: #f8f9fa; border-radius: 8px; height: 100%;\">
    <p style=\"font-style: italic; margin-bottom: 1rem;\">\"{testimonial['content']}\"</p>
    <p style=\"margin-bottom: 0.5rem;\"><strong>─ {testimonial['author']}</strong></p>
    <p style=\"color: #666; font-size: 0.9rem;\">{testimonial['title']}</p>
    <p style=\"color: #ffc107; margin-top: 0.5rem;\">{'⭐' * testimonial['rating']}</p>
</div>
\"\"\", unsafe_allow_html=True)

st.markdown(\"</section>\", unsafe_allow_html=True)

# ==================== CTA 区域 ====================
st.markdown(\"---\")

st.markdown(\"\"\"
<section style=\"text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 8px; margin: 2rem 0;\">
    <h2 style=\"margin-bottom: 1rem;\">📢 立即开始</h2>
    <p style=\"font-size: 1.2rem; margin-bottom: 2rem;\">🎁 免费试用 14 天，无需信用卡</p>
    <div style=\"display: flex; gap: 1rem; justify-content: center;\">
        <button style=\"padding: 1rem 2rem; font-size: 1.1rem; border: none; background: white; color: #f5576c; border-radius: 8px; cursor: pointer; font-weight: bold;\">
            开始免费试用 →
        </button>
        <button style=\"padding: 1rem 2rem; font-size: 1.1rem; border: 2px solid white; background: transparent; color: white; border-radius: 8px; cursor: pointer;\">
            预约演示 →
        </button>
    </div>
    <p style=\"margin-top: 2rem; opacity: 0.9;\">已有 50,000+ 企业加入</p>
</section>
\"\"\", unsafe_allow_html=True)

# ==================== 页脚 ====================
st.divider()

st.markdown(\"\"\"
<footer style=\"text-align: center; padding: 2rem; color: #666;\">
    <div style=\"display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;\">
        <a href=\"#\" style=\"color: #666; text-decoration: none;\">关于我们</a>
        <a href=\"#\" style=\"color: #666; text-decoration: none;\">联系方式</a>
        <a href=\"#\" style=\"color: #666; text-decoration: none;\">隐私政策</a>
        <a href=\"#\" style=\"color: #666; text-decoration: none;\">服务条款</a>
    </div>
    <p>© 2024 {PRODUCT_NAME}. All rights reserved.</p>
    <div style=\"margin-top: 1rem; font-size: 1.5rem;\">
        <span style=\"margin: 0 0.5rem;\">🐦</span>
        <span style=\"margin: 0 0.5rem;\">📘</span>
        <span style=\"margin: 0 0.5rem;\">📸</span>
        <span style=\"margin: 0 0.5rem;\">💼</span>
    </div>
</footer>
\"\"\", unsafe_allow_html=True)
""",
    props=[
        ComponentProp("product_name", "str", "产品名称", True, "产品名称"),
        ComponentProp("tagline", "str", "革命性的产品，改变您的工作方式", True, "产品标语"),
        ComponentProp("cta_button_text", "str", "免费试用", False, "CTA按钮文字"),
        ComponentProp("theme_color", "str", "#007bff", False, "主题颜色"),
        ComponentProp("show_video", "bool", True, False, "显示演示视频"),
        ComponentProp("show_pricing", "bool", True, False, "显示价格表"),
    ],
    tags=["营销", "落地页", "推广", "转化"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "ecommerce", "education"],
)


# ============================================================================
# 7. KanbanPage - 看板页面
# ============================================================================

KANBAN_PAGE = LargeComponent(
    id="kanban_page",
    name="看板页面",
    category=LargeComponentCategory.PRODUCTIVITY,
    description="""
    拖拽式看板页面，支持多列、多卡片、标签管理。
    适用于项目管理、任务跟踪、敏捷开发等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────────────┐
    │  📋 项目看板                                    [+] [⚙️] [▶️] │
    ├─────────────────────────────────────────────────────────────┤
    │  筛选: [标签▼] [负责人▼] [优先级▼]              [应用] [重置]│
    │                                                              │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
    │  │ 📝 待办  │  │ 🚀 进行中│  │ ✅ 已完成│  │ 📁 归档  │   │
    │  │   (5)    │  │   (3)    │  │   (8)    │  │   (12)   │   │
    │  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤   │
    │  │┌────────┐│  │┌────────┐│  │┌────────┐│  │┌────────┐│   │
    │  ││功能A   ││  ││功能B   ││  ││功能C   ││  ││功能D   ││   │
    │  │├────────┤│  │├────────┤│  │├────────┤│  │├────────┤│   │
    │  ││🔴高优先级│  ││🟡中优先级│  ││🟢已完成││  ││⚪归档  ││   │
    │  ││张三负责││  ││李四负责││  ││王五完成││  ││已完成  ││   │
    │  ││ [标签] ││  ││ [标签] ││  ││ [标签] ││  ││ [标签] ││   │
    │  │└────────┘│  │└────────┘│  │└────────┘│  │└────────┘│   │
    │  │          │  │┌────────┐│  │          │  │          │   │
    │  │┌────────┐│  ││功能E   ││  │┌────────┐│  │          │   │
    │  ││功能F   ││  │├────────┤│  ││功能G   ││  │          │   │
    │  │├────────┤│  ││🔴紧急  ││  │├────────┤│  │          │   │
    │  │└────────┘│  │└────────┘│  │└────────┘│  │          │   │
    │  │          │  │          │  │          │  │          │   │
    │  │  [+ 新建]│  │  [+ 新建]│  │          │  │          │   │
    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
    │                                                              │
    │  统计: 待办5 | 进行3 | 完成8 | 归档12  |  总计: 28        │
    └─────────────────────────────────────────────────────────────┘
    """,
    features=[
        "📋 拖拽操作 - 拖拽卡片在列之间移动",
        "🏷️ 标签系统 - 多标签分类，颜色区分",
        "👤 负责人 - 分配任务给团队成员",
        "🔴 优先级 - 高/中/低优先级标识",
        "📊 进度追踪 - 实时显示各列任务数量",
        "🔍 搜索过滤 - 按标签、负责人、优先级筛选",
        "💬 卡片详情 - 点击查看完整信息",
        "👁️ 视图切换 - 看板/列表/日历视图",
        "📤 导出功能 - 导出任务列表",
        "🔄 自动归档 - 完成任务自动归档",
    ],
    code_skeleton="""
import streamlit as st
from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

# ==================== 配置区 ====================
PAGE_TITLE = \"{{page_title}}\"  # 页面标题
COLUMNS = {{columns}}  # 看板列配置
ENABLE_DRAG_DROP = {{enable_drag_drop}}  # 启用拖拽
ENABLE_SWIMLANES = {{enable_swimlanes}}  # 启用泳道

# ==================== 数据结构 ====================
@dataclass
class Card:
    \"\"\"看板卡片\"\"\"
    id: str
    title: str
    description: str = \"\"
    tags: List[str] = field(default_factory=list)
    priority: str = \"medium\"  # high, medium, low
    assignee: str = \"\"
    due_date: str = \"\"
    checklist: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class Column:
    \"\"\"看板列\"\"\"
    id: str
    name: str
    cards: List[Card] = field(default_factory=list)
    color: str = \"#e0e0e0\"
    limit: int = 10  # 工作在进展限制

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=\"📋\",
    layout=\"wide\"
)

# ==================== 初始化数据 ====================
if \"kanban_data\" not in st.session_state:
    # 示例数据
    st.session_state.kanban_data = {
        \"todo\": Column(
            id=\"todo\",
            name=\"📝 待办\",
            color=\"#fff3cd\",
            cards=[
                Card(
                    id=\"c1\",
                    title=\"实现用户登录功能\",
                    description=\"使用JWT实现用户认证\",
                    tags=[\"后端\", \"认证\"],
                    priority=\"high\",
                    assignee=\"张三\",
                    due_date=\"2024-01-20\"
                ),
                Card(
                    id=\"c2\",
                    title=\"设计首页UI\",
                    description=\"使用Figma设计首页原型\",
                    tags=[\"设计\", \"UI\"],
                    priority=\"medium\",
                    assignee=\"李四\"
                )
            ]
        ),
        \"inprogress\": Column(
            id=\"inprogress\",
            name=\"🚀 进行中\",
            color=\"#d1ecf1\",
            cards=[
                Card(
                    id=\"c3\",
                    title=\"API接口开发\",
                    description=\"开发RESTful API\",
                    tags=[\"后端\", \"API\"],
                    priority=\"high\",
                    assignee=\"王五\"
                )
            ]
        ),
        \"done\": Column(
            id=\"done\",
            name=\"✅ 已完成\",
            color=\"#d4edda\",
            cards=[
                Card(
                    id=\"c4\",
                    title=\"需求分析\",
                    description=\"完成产品需求文档\",
                    tags=[\"产品\"],
                    priority=\"high\",
                    assignee=\"赵六\",
                    due_date=\"2024-01-10\"
                )
            ]
        ),
        \"archived\": Column(
            id=\"archived\",
            name=\"📁 归档\",
            color=\"#f8f9fa\",
            cards=[]
        )
    }

# ==================== 顶部操作栏 ====================
col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

with col1:
    st.title(f\"📋 {PAGE_TITLE}\")

with col2:
    if st.button(\"+ 新建卡片\", use_container_width=True):
        st.session_state.show_new_card = True

with col3:
    if st.button(\"⚙️ 设置\", use_container_width=True):
        with st.expander(\"看板设置\", expanded=True):
            col_layout = st.multiselect(
                \"显示列\",
                [\"todo\", \"inprogress\", \"done\", \"archived\"],
                default=[\"todo\", \"inprogress\", \"done\"]
            )
            enable_swimlanes = st.checkbox(\"启用泳道\")
            card_limit = st.slider(\"WIP限制\", 1, 20, 10)

with col4:
    if st.button(\"📊 统计\", use_container_width=True):
        with st.expander(\"任务统计\", expanded=True):
            for col_id, column in st.session_state.kanban_data.items():
                st.metric(column.name, len(column.cards))

with col5:
    if st.button(\"🔄 刷新\", use_container_width=True):
        st.rerun()

st.divider()

# ==================== 筛选器 ====================
with st.expander(\"🔍 筛选条件\", expanded=False):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        filter_tags = st.multiselect(
            \"标签\",
            options=[\"后端\", \"前端\", \"设计\", \"产品\", \"API\"],
            default=[]
        )

    with col2:
        filter_assignee = st.multiselect(
            \"负责人\",
            options=[\"张三\", \"李四\", \"王五\", \"赵六\", \"钱七\"],
            default=[]
        )

    with col3:
        filter_priority = st.multiselect(
            \"优先级\",
            options=[\"high\", \"medium\", \"low\"],
            default=[]
        )

    with col4:
        col1, col2 = st.columns(2)
        with col1:
            apply_filter = st.button(\"应用\", use_container_width=True)
        with col2:
            clear_filter = st.button(\"清除\", use_container_width=True)

# ==================== 看板列 ====================
# 计算列数
columns_data = st.session_state.kanban_data
num_columns = len(columns_data)
kanban_cols = st.columns(num_columns)

for idx, (col, (col_id, column)) in enumerate(zip(kanban_cols, columns_data.items())):
    with col:
        # 列标题
        card_count = len(column.cards)
        st.markdown(f\"\"\"
<div style=\"background: {column.color}; padding: 0.5rem; border-radius: 4px 4px 0 0; margin-bottom: 0.5rem;\">
    <strong>{column.name}</strong> <span style=\"float: right;\">({card_count})</span>
</div>
\"\"\", unsafe_allow_html=True)

        # 显示卡片
        for card in column.cards:
            # 应用筛选
            if filter_tags and not any(tag in card.tags for tag in filter_tags):
                continue
            if filter_assignee and card.assignee not in filter_assignee:
                continue
            if filter_priority and card.priority not in filter_priority:
                continue

            # 优先级颜色
            priority_color = {
                \"high\": \"#dc3545\",
                \"medium\": \"#ffc107\",
                \"low\": \"#28a745\"
            }.get(card.priority, \"#6c757d\")

            # 卡片样式
            st.markdown(f\"\"\"
<div style=\"background: white; padding: 1rem; border-radius: 4px; margin-bottom: 0.5rem; border: 1px solid #dee2e6; border-left: 4px solid {priority_color};\">
    <strong>{card.title}</strong>
    <div style=\"font-size: 0.85rem; color: #666; margin-top: 0.5rem;\">{card.description[:50]}...</div>
    <div style=\"margin-top: 0.5rem;\">
        {', '.join([f'<span style=\"background: #e9ecef; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-right: 0.25rem;\">{tag}</span>' for tag in card.tags])}
    </div>
    <div style=\"margin-top: 0.5rem; font-size: 0.8rem; color: #999;\">
        👤 {card.assignee or '未分配'} | 📅 {card.due_date or '无截止日期'}
    </div>
</div>
\"\"\", unsafe_allow_html=True)

            # 操作按钮
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(\"✏️\", key=f\"edit_{card.id}\"):
                    st.session_state.editing_card = card.id
            with col2:
                if st.button(\"→\", key=f\"move_{card.id}\"):
                    # 移动到下一列
                    col_ids = list(columns_data.keys())
                    current_idx = col_ids.index(col_id)
                    if current_idx < len(col_ids) - 1:
                        new_col_id = col_ids[current_idx + 1]
                        columns_data[new_col_id].cards.append(card)
                        columns_data[col_id].cards.remove(card)
                        st.rerun()
            with col3:
                if st.button(\"🗑️\", key=f\"delete_{card.id}\"):
                    columns_data[col_id].cards.remove(card)
                    st.rerun()

        # 新建卡片按钮
        if st.button(f\"+ 新建 {column.name.split()[1]}\", key=f\"new_{col_id}\", use_container_width=True):
            st.session_state.new_card_column = col_id

# ==================== 新建卡片对话框 ====================
if st.session_state.get(\"show_new_card\") or st.session_state.get(\"new_card_column\"):
    st.divider()

    with st.expander(\"📝 新建卡片\", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            new_title = st.text_input(\"标题\", placeholder=\"输入任务标题\")
            new_description = st.text_area(\"描述\", placeholder=\"输入任务描述\")

        with col2:
            new_tags = st.multiselect(
                \"标签\",
                [\"后端\", \"前端\", \"设计\", \"产品\", \"API\"]
            )
            new_priority = st.selectbox(\"优先级\", [\"high\", \"medium\", \"low\"])
            new_assignee = st.selectbox(
                \"负责人\",
                [\"张三\", \"李四\", \"王五\", \"赵六\", \"钱七\"]
            )
            new_due_date = st.date_input(\"截止日期\")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(\"创建\", use_container_width=True):
                target_col = st.session_state.get(\"new_card_column\", \"todo\")
                new_card = Card(
                    id=f\"c{datetime.now().strftime('%Y%m%d%H%M%S')}\",
                    title=new_title,
                    description=new_description,
                    tags=new_tags,
                    priority=new_priority,
                    assignee=new_assignee,
                    due_date=str(new_due_date)
                )
                columns_data[target_col].cards.append(new_card)
                st.session_state.show_new_card = False
                st.session_state.new_card_column = None
                st.success(\"✅ 卡片已创建\")
                st.rerun()

        with col2:
            if st.button(\"取消\", use_container_width=True):
                st.session_state.show_new_card = False
                st.session_state.new_card_column = None
                st.rerun()

# ==================== 底部统计 ====================
st.divider()

total_cards = sum(len(col.cards) for col in columns_data.values())
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(\"总任务数\", total_cards)

with col2:
    todo_count = len(columns_data.get(\"todo\", Column(\"\", \"\")).cards)
    st.metric(\"待办\", todo_count)

with col3:
    inprogress_count = len(columns_data.get(\"inprogress\", Column(\"\", \"\")).cards)
    st.metric(\"进行中\", inprogress_count)

with col4:
    done_count = len(columns_data.get(\"done\", Column(\"\", \"\")).cards)
    st.metric(\"已完成\", done_count)
""",
    props=[
        ComponentProp("page_title", "str", "项目看板", False, "页面标题"),
        ComponentProp("columns", "list", ["todo", "inprogress", "done"], False, "看板列配置"),
        ComponentProp("enable_drag_drop", "bool", False, False, "启用拖拽（需额外库）"),
        ComponentProp("enable_swimlanes", "bool", False, False, "启用泳道视图"),
        ComponentProp("default_wip_limit", "int", 10, False, "默认WIP限制"),
    ],
    tags=["看板", "项目管理", "任务", "敏捷"],
    dependencies=["streamlit"],
    industry_compatibility=["general", "software", "manufacturing", "education"],
)


# ============================================================================
# 8. ProfilePage - 个人中心
# ============================================================================

PROFILE_PAGE = LargeComponent(
    id="profile_page",
    name="个人中心",
    category=LargeComponentCategory.USER,
    description="""
    用户个人资料页面，展示头像、基本信息、统计数据。
    适用于用户主页、个人名片、社交资料等场景。
    """,
    preview="""
    ┌─────────────────────────────────────────────────────────────┐
    │  🎨 背景封面图                                               │
    │  ┌───────────────────────────────────────────────────────┐ │
    │  │                                                        │ │
    │  │   ┌──────┐                                             │ │
    │  │   │      │  张三                                      │ │
    │  │   │ 头像 │  @zhangsan                                  │ │
    │  │   │      │  全栈开发工程师 | 北京                      │ │
    │  │   └──────┘  [✏️ 编辑资料]                              │ │
    │  │                                                        │ │
    │  │   📊 1,234 关注者  |  📝 56 项目  |  ⭐ 4.8 评分       │ │
    │  └───────────────────────────────────────────────────────┘ │
    ├─────────────────────────────────────────────────────────────┤
    │  ┌─────────────┬───────────────────────────────────────────┐│
    │  │  📋 基本信息 │  姓名: 张三                              ││
    │  │  💼 工作     │  邮箱: zhang@example.com                 ││
    │  │  🎓 教育     │  电话: 138****1234                       ││
    │  │  🏆 成就     │  位置: 北京市朝阳区                      ││
    │  │  ⚙️ 设置    │                                           ││
    │  │             │  简介:                                   ││
    │  │             │  全栈开发工程师，5年经验，热爱开源...    ││
    │  │             │                                           ││
    │  │             │  技能:                                   ││
    │  │             │  [Python] [React] [Node.js] [SQL]        ││
    │  └─────────────┴───────────────────────────────────────────┘│
    │                                                              │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │  📊 活动统计                                        │   │
    │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │   │
    │  │  │   56     │ │   1,234  │ │   89%    │           │   │
    │  │  │  项目    │ │  关注者  │ │  完成率  │           │   │
    │  │  └──────────┘ └──────────┘ └──────────┘           │   │
    │  │                                                     │   │
    │  │  活动图表: ╱╲╱╲___╱╲╱╲___                         │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                              │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │  📝 最近动态                                        │   │
    │  │  ┌─────────────────────────────────────────────┐   │   │
    │  │  │ ✅ 完成了项目「AI客服系统」        2小时前     │   │   │
    │  │  │ 💬 评论了「如何优化数据库」        5小时前     │   │   │
    │  │  │ 🌟 获得了「社区贡献者」徽章        1天前       │   │   │
    │  │  └─────────────────────────────────────────────┘   │   │
    │  └─────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────┘
    """,
    features=[
        "👤 头像上传 - 支持图片裁剪和上传",
        "🖼️ 封面图片 - 自定义个人封面",
        "📊 统计数据 - 关注者、项目、评分等",
        "🏆 成就徽章 - 展示获得的成就",
        "💼 工作经历 - 时间线展示",
        "🎓 教育背景 - 学历和证书",
        "📝 活动历史 - 最近动态记录",
        "🔗 社交链接 - 关联社交媒体",
        "💡 技能标签 - 专业技能展示",
        "📞 联系方式 - 邮箱、电话等",
    ],
    code_skeleton="""
import streamlit as st
from typing import List, Dict
from datetime import datetime, timedelta

# ==================== 配置区 ====================
SHOW_EDIT_BUTTON = {{show_edit_button}}  # 显示编辑按钮
SHOW_ACTIVITY_STATS = {{show_activity_stats}}  # 显示活动统计
SHOW_RECENT_ACTIVITY = {{show_recent_activity}}  # 显示最近动态
ENABLE_SOCIAL_LINKS = {{enable_social_links}}  # 社交链接

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=\"个人中心\",
    page_icon=\"👤\",
    layout=\"wide\"
)

# ==================== 模拟用户数据 ====================
user_data = {
    \"id\": \"user_001\",
    \"name\": \"张三\",
    \"username\": \"zhangsan\",
    \"avatar\": \"👨‍💻\",
    \"cover_image\": None,
    \"bio\": \"全栈开发工程师，5年经验，热爱开源和新技术\",
    \"location\": \"北京市朝阳区\",
    \"website\": \"https://zhangsan.dev\",
    \"joined_date\": \"2022-01-15\",
    \"stats\": {
        \"followers\": 1234,
        \"following\": 567,
        \"projects\": 56,
        \"rating\": 4.8
    },
    \"skills\": [\"Python\", \"React\", \"Node.js\", \"SQL\", \"Docker\", \"AWS\"],
    \"social\": {
        \"github\": \"https://github.com/zhangsan\",
        \"twitter\": \"@zhangsan\",
        \"linkedin\": \"https://linkedin.com/in/zhangsan\"
    },
    \"achievements\": [
        {\"name\": \"社区贡献者\", \"icon\": \"🌟\", \"date\": \"2024-01-10\"},
        {\"name\": \"项目达人\", \"icon\": \"🏆\", \"date\": \"2024-01-05\"},
        {\"name\": \"早起鸟\", \"icon\": \"🌅\", \"date\": \"2023-12-20\"}
    ]
}

# ==================== 封面区域 ====================
st.markdown(\"\"\"
<div style=\"height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; position: relative;\"></div>
\"\"\", unsafe_allow_html=True)

# 个人信息卡片
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.markdown(\"<div style='height: 60px;'></div>\", unsafe_allow_html=True)
    st.markdown(f\"\"\"
<div style='text-align: center;'>
    <div style='font-size: 6rem;'>{user_data['avatar']}</div>
</div>
\"\"\", unsafe_allow_html=True)

with col2:
    st.markdown(\"<div style='height: 40px;'></div>\", unsafe_allow_html=True)

    # 用户名和基本信息
    st.markdown(f\"\"\"
<div style='margin-top: 1rem;'>
    <h1 style='margin: 0;'>{user_data['name']} <small style='color: #666;'>@{user_data['username']}</small></h1>
    <p style='color: #666; margin-top: 0.5rem;'>📍 {user_data['location']} | 🌐 <a href='{user_data['website']}'>{user_data['website']}</a></p>
</div>
\"\"\", unsafe_allow_html=True)

    # 统计数据
    st.markdown(f\"\"\"
<div style='display: flex; gap: 2rem; margin-top: 1rem;'>
    <div>
        <strong style='font-size: 1.5rem;'>{user_data['stats']['followers']:,}</strong>
        <div style='color: #666;'>关注者</div>
    </div>
    <div>
        <strong style='font-size: 1.5rem;'>{user_data['stats']['projects']}</strong>
        <div style='color: #666;'>项目</div>
    </div>
    <div>
        <strong style='font-size: 1.5rem;'>{user_data['stats']['rating']} ⭐</strong>
        <div style='color: #666;'>评分</div>
    </div>
</div>
\"\"\", unsafe_allow_html=True)

    # 编辑按钮
    if SHOW_EDIT_BUTTON:
        if st.button(\"✏️ 编辑资料\"):
            st.info(\"打开编辑表单\")

with col3:
    st.write(\"\")
    st.write(\"\")
    if st.button(\"⚙️ 设置\", use_container_width=True):
        st.info(\"跳转到设置页面\")
    if st.button(\"🔗 分享\", use_container_width=True):
        st.info(\"复制个人主页链接\"

st.divider()

# ==================== 标签页内容 ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([\"📋 基本信息\", \"💼 工作\", \"🎓 教育\", \"🏆 成就\", \"⚙️ 设置\"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(\"个人简介\")

        # 基本信息
        st.write(f\"**姓名:** {user_data['name']}\")
        st.write(f\"**用户名:** @{user_data['username']}\")
        st.write(f\"**邮箱:** zhang@example.com\")
        st.write(f\"**电话:** 138****1234\")
        st.write(f\"**位置:** {user_data['location']}\")

        st.divider()

        # 详细简介
        st.write(f\"**简介:**\")
        st.write(user_data['bio'])

        st.divider()

        # 技能标签
        st.write(\"**技能:**\")
        skill_cols = st.columns(3)
        for i, skill in enumerate(user_data['skills']):
            with skill_cols[i % 3]:
                st.markdown(f\"\"\"
<div style='background: #e9ecef; padding: 0.5rem 1rem; border-radius: 20px; text-align: center; margin: 0.25rem 0;'>
    {skill}
</div>
\"\"\", unsafe_allow_html=True)

    with col2:
        st.subheader(\"社交链接\")
        if ENABLE_SOCIAL_LINKS:
            social_links = user_data.get('social', {})
            if 'github' in social_links:
                st.markdown(f\"[🐙 GitHub]({social_links['github']})\")
            if 'twitter' in social_links:
                st.markdown(f\"[🐦 Twitter]({social_links['twitter']})\")
            if 'linkedin' in social_links:
                st.markdown(f\"[💼 LinkedIn]({social_links['linkedin']})\")

        st.divider()

        # 加入时间
        st.write(\"**加入时间:**\")
        st.write(f\"📅 {user_data['joined_date']}\")

        # 账户状态
        st.write(\"**账户状态:**\")
        st.success(\"✅ 已验证\"

with tab2:
    st.subheader(\"工作经历\")

    work_experience = [
        {
            \"title\": \"高级全栈工程师\",
            \"company\": \"某科技公司\",
            \"period\": \"2021 - 至今\",
            \"description\": \"负责产品架构设计和团队技术管理\"
        },
        {
            \"title\": \"后端工程师\",
            \"company\": \"创业公司\",
            \"period\": \"2019 - 2021\",
            \"description\": \"参与核心API开发和系统优化\"
        }
    ]

    for exp in work_experience:
        with st.expander(f\"{exp['title']} @ {exp['company']} ({exp['period']})\", expanded=True):
            st.write(exp['description'])

with tab3:
    st.subheader(\"教育背景\")

    education = [
        {
            \"school\": \"某大学\",
            \"degree\": \"计算机科学与技术 本科\",
            \"period\": \"2015 - 2019\",
            \"gpa\": \"3.8/4.0\"
        }
    ]

    for edu in education:
        st.write(f\"**{edu['school']}**\")
        st.write(f\"{edu['degree']} | {edu['period']}\")
        st.write(f\"GPA: {edu['gpa']}\")
        st.divider()

with tab4:
    st.subheader(\"成就徽章\")

    achievements = user_data.get('achievements', [])

    # 成就统计
    col1, col2 = st.columns([2, 1])
    with col1:
        for achievement in achievements:
            st.markdown(f\"\"\"
<div style='display: flex; align-items: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.5rem;'>
    <div style='font-size: 2rem; margin-right: 1rem;'>{achievement['icon']}</div>
    <div>
        <strong>{achievement['name']}</strong>
        <div style='color: #666; font-size: 0.9rem;'>获得于 {achievement['date']}</div>
    </div>
</div>
\"\"\", unsafe_allow_html=True)

    with col2:
        st.metric(\"总成就数\", len(achievements))
        st.metric(\"稀有度\", \"⭐⭐⭐\")

with tab5:
    st.subheader(\"账户设置\")

    col1, col2 = st.columns(2)

    with col1:
        st.write(\"**隐私设置:**\")
        st.checkbox(\"公开个人资料\", value=True)
        st.checkbox(\"显示邮箱\", value=False)
        st.checkbox(\"显示位置\", value=True)

    with col2:
        st.write(\"**通知设置:**\")
        st.checkbox(\"邮件通知\", value=True)
        st.checkbox(\"推送通知\", value=False)
        st.checkbox(\"短信通知\", value=False)

    st.divider()

    if st.button(\"💾 保存更改\", type=\"primary\"):
        st.success(\"✅ 设置已保存\")

# ==================== 活动统计 ====================
if SHOW_ACTIVITY_STATS:
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(\"本月项目\", 8, \"+2\")

    with col2:
        st.metric(\"贡献次数\", 156, \"+23\")

    with col3:
        st.metric(\"连续活跃\", 15, \"天\")

    # 活动图表
    st.subheader(\"活动趋势\")
    import random
    activity_data = [random.randint(5, 20) for _ in range(30)]
    st.bar_chart(activity_data)

# ==================== 最近动态 ====================
if SHOW_RECENT_ACTIVITY:
    st.divider()

    st.subheader(\"📝 最近动态\")

    recent_activities = [
        {\"type\": \"project\", \"icon\": \"✅\", \"text\": \"完成了项目「AI客服系统」\", \"time\": \"2小时前\"},
        {\"type\": \"comment\", \"icon\": \"💬\", \"text\": \"评论了「如何优化数据库」\", \"time\": \"5小时前\"},
        {\"type\": \"achievement\", \"icon\": \"🌟\", \"text\": \"获得了「社区贡献者」徽章\", \"time\": \"1天前\"},
        {\"type\": \"follow\", \"icon\": \"👥\", \"text\": \"开始关注「李四」\", \"time\": \"2天前\"},
        {\"type\": \"project\", \"icon\": \"🚀\", \"text\": \"创建了新项目「数据分析平台」\", \"time\": \"3天前\"},
    ]

    for activity in recent_activities:
        st.markdown(f\"\"\"
<div style='display: flex; align-items: center; padding: 0.75rem; border-bottom: 1px solid #e9ecef;'>
    <div style='font-size: 1.5rem; margin-right: 1rem;'>{activity['icon']}</div>
    <div style='flex: 1;'>
        <div>{activity['text']}</div>
        <div style='color: #999; font-size: 0.85rem;'>{activity['time']}</div>
    </div>
</div>
\"\"\", unsafe_allow_html=True)
""",
    props=[
        ComponentProp("show_edit_button", "bool", True, False, "显示编辑按钮"),
        ComponentProp("show_activity_stats", "bool", True, False, "显示活动统计"),
        ComponentProp("show_recent_activity", "bool", True, False, "显示最近动态"),
        ComponentProp("enable_social_links", "bool", True, False, "显示社交链接"),
        ComponentProp("achievements_display", "str", "grid", False, "成就显示方式"),
    ],
    tags=["个人资料", "用户", "主页", "社交"],
    dependencies=["streamlit"],
    industry_compatibility=["general"],
)


# ============================================================================
# 组件注册表
# ============================================================================

LARGE_COMPONENTS = {
    "dashboard_page": DASHBOARD_PAGE,
    "chatbot_page": CHATBOT_PAGE,
    "form_wizard_page": FORM_WIZARD_PAGE,
    "data_table_page": DATA_TABLE_PAGE,
    "settings_page": SETTINGS_PAGE,
    "landing_page": LANDING_PAGE,
    "kanban_page": KANBAN_PAGE,
    "profile_page": PROFILE_PAGE,
}


# ============================================================================
# 便捷函数
# ============================================================================

def get_large_component(component_id: str) -> Optional[LargeComponent]:
    """
    获取大型组件

    Args:
        component_id: 组件ID

    Returns:
        大型组件实例，不存在则返回 None
    """
    return LARGE_COMPONENTS.get(component_id)


def list_large_components(
    category: Optional[LargeComponentCategory] = None
) -> List[LargeComponent]:
    """
    列出大型组件

    Args:
        category: 指定分类，None 表示全部

    Returns:
        大型组件列表
    """
    if category:
        return [c for c in LARGE_COMPONENTS.values() if c.category == category]
    return list(LARGE_COMPONENTS.values())


def get_components_by_industry(industry: str) -> List[LargeComponent]:
    """
    按行业获取推荐组件

    Args:
        industry: 行业名称

    Returns:
        适用于该行业的大型组件列表
    """
    return [
        c for c in LARGE_COMPONENTS.values()
        if industry in c.industry_compatibility or "general" in c.industry_compatibility
    ]


def search_large_components(keyword: str) -> List[LargeComponent]:
    """
    搜索大型组件

    Args:
        keyword: 搜索关键词

    Returns:
        匹配的大型组件列表
    """
    keyword_lower = keyword.lower()
    results = []
    for component in LARGE_COMPONENTS.values():
        if (keyword_lower in component.name.lower() or
            keyword_lower in component.description.lower() or
            any(keyword_lower in tag.lower() for tag in component.tags)):
            results.append(component)
    return results


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "LargeComponentCategory",
    # 数据类
    "ComponentProp",
    "LargeComponent",
    # 组件定义
    "DASHBOARD_PAGE",
    "CHATBOT_PAGE",
    "FORM_WIZARD_PAGE",
    "DATA_TABLE_PAGE",
    "SETTINGS_PAGE",
    "LANDING_PAGE",
    "KANBAN_PAGE",
    "PROFILE_PAGE",
    # 注册表
    "LARGE_COMPONENTS",
    # 便捷函数
    "get_large_component",
    "list_large_components",
    "get_components_by_industry",
    "search_large_components",
]
