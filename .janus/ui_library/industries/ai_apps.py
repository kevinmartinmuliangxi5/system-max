"""
AI Applications Industry Templates - AI应用行业模板
==================================================

包含 AI 应用专用的 5 个完整页面模板：

模板列表:
    1. ChatAssistant - 对话助手（流式输出、上下文、插件）
    2. ImageGenerator - 图像生成（Prompt、参数、画廊）
    3. ModelPlayground - 模型试验场（参数调节、对比、日志）
    4. DataAnnotation - 数据标注（标签、快捷键、进度）
    5. PipelineBuilder - AI 流水线（节点、连线、执行）

推荐主题:
    - tech_neon: 适合 AI 科技感界面
    - cool_mint: 适合清新专业界面
    - midnight_blue: 适合深色模式 AI 应用

使用方式:
    from ui_library.industries.ai_apps import (
        ChatAssistant,
        ImageGenerator,
        ModelPlayground,
        DataAnnotation,
        PipelineBuilder,
    )
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import pandas as pd
from datetime import datetime
import asyncio


# ============================================================================
# 枚举定义
# ============================================================================

class ChatRole(Enum):
    """对话角色"""
    USER = "user"                 # 用户
    ASSISTANT = "assistant"         # 助手
    SYSTEM = "system"             # 系统


class MessageStatus(Enum):
    """消息状态"""
    SENDING = "sending"           # 发送中
    SENT = "sent"                 # 已发送
    ERROR = "error"               # 错误


class ImageStyle(Enum):
    """图像风格"""
    REALISTIC = "realistic"       # 写实
    CARTOON = "cartoon"           # 卡通
    ANIME = "anime"               # 动漫
    OIL_PAINTING = "oil"          # 油画
    WATERCOLOR = "watercolor"      # 水彩
    SKETCH = "sketch"             # 素描


class AnnotationType(Enum):
    """标注类型"""
    CLASSIFICATION = "classification"  # 分类
    DETECTION = "detection"            # 检测
    SEGMENTATION = "segmentation"      # 分割
    KEYPOINT = "keypoint"            # 关键点
    TEXT = "text"                   # 文本
    SENTIMENT = "sentiment"          # 情感


class NodeType(Enum):
    """节点类型"""
    INPUT = "input"               # 输入节点
    PROCESSING = "processing"     # 处理节点
    OUTPUT = "output"             # 输出节点
    CONDITION = "condition"       # 条件节点
    LOOP = "loop"                 # 循环节点
    INTEGRATION = "integration"   # 集成节点


# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class ChatMessage:
    """
    聊天消息定义

    Attributes:
        id: 消息ID
        role: 角色
        content: 内容
        timestamp: 时间戳
        status: 状态
        metadata: 元数据
    """
    id: str
    role: ChatRole
    content: str
    timestamp: datetime
    status: MessageStatus = MessageStatus.SENT
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "metadata": self.metadata,
        }


@dataclass
class GenerationRequest:
    """
    生成请求定义

    Attributes:
        id: 请求ID
        prompt: 提示词
        negative_prompt: 负面提示词
        style: 图像风格
        model: 模型名称
        parameters: 参数配置
    """
    id: str
    prompt: str
    negative_prompt: str
    style: ImageStyle
    model: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "style": self.style.value,
            "model": self.model,
            "parameters": self.parameters,
        }


@dataclass
class ModelConfig:
    """
    模型配置定义

    Attributes:
        id: 配置ID
        name: 名称
        model: 模型
        temperature: 温度
        max_tokens: 最大Token数
        top_p: Top-P采样
        frequency_penalty: 频率惩罚
        presence_penalty: 存在惩罚
    """
    id: str
    name: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        }


@dataclass
class AnnotationTask:
    """
    标注任务定义

    Attributes:
        id: 任务ID
        type: 标注类型
        dataset: 数据集名称
        total_items: 总项目数
        completed_items: 已完成数
        labels: 标签列表
        instructions: 标注说明
    """
    id: str
    type: AnnotationType
    dataset: str
    total_items: int
    completed_items: int
    labels: List[str]
    instructions: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "dataset": self.dataset,
            "total_items": self.total_items,
            "completed_items": self.completed_items,
            "labels": self.labels,
            "instructions": self.instructions,
        }


@dataclass
class PipelineNode:
    """
    流水线节点定义

    Attributes:
        id: 节点ID
        type: 节点类型
        name: 节点名称
        config: 配置参数
        position: 位置坐标
        connections: 连接关系
    """
    id: str
    type: NodeType
    name: str
    config: Dict[str, Any]
    position: tuple[int, int]
    connections: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "name": self.name,
            "config": self.config,
            "position": self.position,
            "connections": self.connections,
        }


# ============================================================================
# 1. ChatAssistant - 对话助手模板
# ============================================================================

class ChatAssistant:
    """
    对话助手模板

    功能: 流式对话、上下文管理、插件扩展

    推荐主题: tech_neon, cool_mint

    特性:
        - 流式输出
        - 多轮对话
        - 上下文保持
        - 插件系统
        - 会话管理
        - 模型切换
    """

    def __init__(self):
        """初始化对话助手"""
        self._messages = []
        self._contexts = {}
        self._plugins = []

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
对话助手 - Streamlit 实现
==========================

功能: 流式对话、上下文管理、插件扩展
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import json


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="AI 对话助手",
    page_icon="🤖",
    layout="center"
)


# ============================================================================
# 状态管理
# ============================================================================

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "chat_context" not in st.session_state:
    st.session_state.chat_context = {
        "system_prompt": "你是一个专业的AI助手，负责回答用户的问题。",
        "temperature": 0.7,
        "max_tokens": 2000
    }

if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = None

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False


# ============================================================================
# 模拟AI响应（流式输出）
# ============================================================================

def simulate_streaming_response(prompt: str, temperature: float = 0.7):
    """模拟流式AI响应"""
    responses = {
        "python": "Python 是一种高级编程语言，以其简洁明了的语法而闻名。以下是 Python 的主要特点：\n\n1. **简单易学**：Python 的语法接近英语，非常适合编程新手。\n\n2. **功能强大**：Python 有丰富的库和框架，可以用于 Web 开发、数据分析、人工智能等多个领域。\n\n3. **跨平台**：Python 可以在 Windows、macOS 和 Linux 上运行。\n\n你想了解 Python 的哪些方面呢？",

        "ai": "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。\n\n**主要分支：**\n\n1. **机器学习（ML）**：让计算机从数据中学习，无需明确编程。\n\n2. **深度学习（DL）**：使用神经网络的机器学习方法。\n\n3. **自然语言处理（NLP）**：理解和生成人类语言。\n\n你对 AI 的哪个方面感兴趣？",

        "default": f"关于"{prompt}"，这是一个很好的问题。让我为你详细解答。\n\n首先，这个主题涉及多个方面。我们需要考虑它的背景、应用场景和实际意义。\n\n有什么其他问题吗？"
    }

    return responses.get("default", responses["python"])


def simulate_streaming_stream(response_text: str):
    """模拟流式输出"""
    import time

    placeholder = st.empty()
    full_response = ""

    for char in response_text:
        full_response += char
        placeholder.markdown(full_response + "▌")
        time.sleep(0.02)

    placeholder.markdown(full_response)


# ============================================================================
# 主界面
# ============================================================================

st.title("🤖 AI 对话助手")

# 会话管理
col_session1, col_session2, col_session3 = st.columns(3)

with col_session1:
    if st.button("💬 新对话", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.chat_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.rerun()

with col_session2:
    if st.button("📜 历史会话", use_container_width=True):
        st.info("历史会话功能开发中...")

with col_session3:
    if st.button("⚙️ 设置", use_container_width=True):
        with st.sidebar:
            st.subheader("⚙️ 对话设置")

            # 系统提示词
            system_prompt = st.text_area(
                "系统提示词",
                value=st.session_state.chat_context["system_prompt"],
                height=100
            )

            if st.button("保存提示词"):
                st.session_state.chat_context["system_prompt"] = system_prompt
                st.success("已保存")

            st.divider()

            # 温度控制
            temperature = st.slider(
                "温度",
                0.0, 1.0,
                float(st.session_state.chat_context["temperature"]),
                0.1,
                help="影响输出随机性，越高越随机"
            )
            st.session_state.chat_context["temperature"] = temperature

            st.divider()

            # 最大Token数
            max_tokens = st.slider(
                "最大Token数",
                256, 4096,
                st.session_state.chat_context.get("max_tokens", 2048),
                256
            )

            st.divider()

            # 模型选择
            model = st.selectbox(
                "AI 模型",
                ["GPT-4", "Claude-3", "Gemini Pro", "Llama 2"],
                index=0
            )
            st.caption(f"当前模型: {model}")

st.divider()


# ============================================================================
# 对话历史显示
# ============================================================================

# 创建聊天容器
chat_container = st.container()

with chat_container:
    # 显示历史消息
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.chat_message("user", msg["content"])
        else:
            # AI 消息
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    # AI 思考状态
    if st.session_state.is_thinking:
        st.info("🤔 正在思考...")


# ============================================================================
# 输入区域
# ============================================================================

st.divider()

# 用户输入
user_input = st.text_area(
    "输入你的问题",
    placeholder="在这里输入你的问题...",
    height=100,
    label_visibility="collapsed"
)

# 快捷操作
col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    if st.button("🚀 发送", use_container_width=True, type="primary"):
        if user_input:
            # 添加用户消息
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })

            # 模拟AI响应
            st.session_state.is_thinking = True
            st.rerun()

with col_input2:
    st.button("📋 提示词库", use_container_width=True)
    st.info("提示词库功能开发中...")

with col_input3:
    if st.button("🔌 插件", use_container_width=True):
        st.info("插件系统开发中...")


# ============================================================================
# 侧边栏 - 插件和工具
# ============================================================================

with st.sidebar:
    st.title("🔌 插件系统")

    st.caption("扩展 AI 能力")

    # 可用插件
    plugins = [
        {"id": "web_search", "name": "网络搜索", "icon": "🌐"},
        {"id": "code_runner", "name": "代码运行", "icon": "💻"},
        {"id": "calculator", "name": "计算器", "icon": "🧮"},
        {"id": "translator", "name": "翻译", "icon": "🌍"},
    ]

    for plugin in plugins:
        with st.container():
            col_p1, col_p2 = st.columns([4, 1])

            with col_p1:
                st.write(f'{plugin["icon"]} {plugin["name"]}')

            with col_p2:
                st.checkbox("", key=f'plugin_{plugin["id"]}', label_visibility="collapsed")

    st.divider()

    # 快捷问题
    st.subheader("💡 快捷问题")

    quick_questions = [
        "解释什么是机器学习？",
        "帮我写一个Python函数",
        "如何优化数据库查询？",
        "这段代码有什么问题？"
    ]

    for i, question in enumerate(quick_questions):
        if st.button(f"Q{i+1}: {question[:20]}...", key=f'quick_{i}'):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": question,
                "timestamp": datetime.now()
            })
            st.rerun()

    st.divider()

    # 对话统计
    st.subheader("📊 对话统计")

    total_messages = len([m for m in st.session_state.chat_messages if m["role"] == "user"])
    st.metric("对话轮次", total_messages)

    # 使用 token 估算
    total_chars = sum(len(m["content"]) for m in st.session_state.chat_messages)
    estimated_tokens = total_chars // 2
    st.metric("估算Token", f"~{estimated_tokens:,}")
'''


# ============================================================================
# 2. ImageGenerator - 图像生成模板
# ============================================================================

class ImageGenerator:
    """
    图像生成模板

    功能: Prompt 构建、参数调节、画廊管理

    推荐主题: tech_neon, cool_mint

    特性:
        - Prompt 编辑器
        - 多风格支持
        - 参数调节
        - 生成历史
        - 图库管理
        - 批量生成
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
图像生成 - Streamlit 实现
==========================

功能: Prompt 构建、参数调节、画廊管理
"""

import streamlit as st
from datetime import datetime


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="AI 图像生成",
    page_icon="🎨",
    layout="wide"
)


# ============================================================================
# 状态管理
# ============================================================================

if "image_prompt" not in st.session_state:
    st.session_state.image_prompt = ""

if "image_style" not in st.session_state:
    st.session_state.image_style = "realistic"

if "image_size" not in st.session_state:
    st.session_state.image_size = "1024x1024"

if "generated_images" not in st.session_state:
    st.session_state.generated_images = []


# ============================================================================
# 主界面
# ============================================================================

st.title("🎨 AI 图像生成")

col_gen, col_gallery = st.columns([1, 1])


# ============================================================================
# 左侧 - 生成控制
# ============================================================================

with col_gen:
    st.subheader("🎯 图像生成")

    # Prompt 输入
    prompt = st.text_area(
        "Prompt 描述",
        value=st.session_state.image_prompt,
        height=120,
        placeholder="描述你想要生成的图像，例如：一只可爱的猫，坐在窗台上，阳光透过窗户照进来...",
        label_visibility="collapsed"
    )
    st.session_state.image_prompt = prompt

    st.divider()

    # 风格选择
    st.markdown("### 🎨 图像风格")

    style_options = {
        "realistic": "写实风格",
        "cartoon": "卡通风格",
        "anime": "动漫风格",
        "oil": "油画风格",
        "watercolor": "水彩风格",
        "sketch": "素描风格"
    }

    for style_id, style_name in style_options.items():
        selected = st.radio(
            style_name,
            [""] + list(style_options.keys()),
            index=[""] + list(style_options.keys()).index(st.session_state.image_style) if st.session_state.image_style else 0
        )
        if selected:
            st.session_state.image_style = selected

    st.divider()

    # 参数调节
    st.markdown("### ⚙️ 参数调节")

    # 尺寸选择
    size_options = ["512x512", "768x768", "1024x1024", "1024x768", "768x1024"]
    size_selected = st.select_slider("图像尺寸", size_options, index=2)
    st.session_state.image_size = size_selected

    # 高级参数
    with st.expander("🔧 高级参数", expanded=False):
        cfg_scale = st.slider("引导强度", 1, 20, 7, 1)
        steps = st.slider("迭代步数", 10, 50, 20, 1)
        seed = st.number_input("随机种子", value=-1, help="-1 表示随机")

    # 负面提示词
    negative_prompt = st.text_area(
        "负面提示词（可选）",
        value="低质量, 模糊, 变形",
        height=80,
        label_visibility="collapsed"
    )

    st.divider()

    # 生成按钮
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🎨 生成图像", use_container_width=True, type="primary", size="large"):
            # 模拟生成过程
            with st.spinner("正在生成中..."):
                import time
                time.sleep(2)

            # 模拟生成结果
            new_images = []
            for i in range(4):
                new_images.append({
                    "id": f"img_{datetime.now().timestamp()}_ {i}",
                    "prompt": prompt,
                    "style": st.session_state.image_style,
                    "size": st.session_state.image_size,
                    "timestamp": datetime.now()
                })

            st.session_state.generated_images = new_images + st.session_state.generated_images
            st.success(f"✅ 成功生成 4 张图像！")
            st.rerun()

    with col_btn2:
        if st.button("🗑️ 清空历史", use_container_width=True):
            st.session_state.generated_images = []
            st.success("已清空")
            st.rerun()


# ============================================================================
# 右侧 - 图像画廊
# ============================================================================

with col_gallery:
    st.subheader("🖼️ 图像画廊")

    if not st.session_state.generated_images:
        # 空状态
        st.markdown("""
        <div style='text-align: center; padding: 60px; color: #999;'>
            <div style='font-size: 64px;'>🎨</div>
            <p>还没有生成的图像</p>
            <p>在左侧输入描述，点击生成按钮开始创作</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # 显示最新生成的图像
        latest_images = st.session_state.generated_images[:4]

        # 4列网格显示
        gallery_cols = st.columns(4)

        for i, img in enumerate(latest_images):
            col = gallery_cols[i]

            with col:
                # 图像占位符
                st.markdown(f"""
                <div style='border: 1px solid #e0e0e0; border-radius: 8px; padding: 10px; text-align: center;'>
                    <div style='background: #f5f5f5; height: 200px; display: flex; align-items: center; justify-content: center; border-radius: 4px;'>
                        <span style='font-size: 48px;'>🖼️</span>
                    </div>
                    <p style='margin: 10px 0 4px 0; font-size: 12px; color: #666;'>{img['prompt'][:30]}...</p>
                    <p style='margin: 0; font-size: 12px; color: #999;'>{img['style']} · {img['size']}</p>
                </div>
                """, unsafe_allow_html=True)

                # 操作按钮
                col_act1, col_act2 = st.columns(2)

                with col_act1:
                    if st.button(f"⬇️", key=f'download_{img["id"]}', use_container_width=True):
                        st.success("下载中...")

                with col_act2:
                    if st.button(f'🗑️', key=f'delete_{img["id"]}', use_container_width=True):
                        st.session_state.generated_images.remove(img)
                        st.rerun()


# ============================================================================
# 历史记录
# ============================================================================

st.divider()

st.subheader("📚 生成历史")

if len(st.session_state.generated_images) > 4:
    # 分页显示
    page_size = 8
    pages = [st.session_state.generated_images[i:i+page_size] for i in range(0, len(st.session_state.generated_images), page_size)]

    page_num = st.number_input("页码", min_value=1, max_value=len(pages), value=1)

    if page_num <= len(pages):
        current_page = pages[page_num - 1]

        # 网格显示
        history_cols = st.columns(4)

        for i, img in enumerate(current_page):
            col = history_cols[i % 4]

            with col:
                st.markdown(f"""
                <div style='border: 1px solid #e0e0e0; border-radius: 8px; padding: 10px;'>
                    <div style='background: #f5f5f5; height: 120px; display: flex; align-items: center; justify-content: center; border-radius: 4px;'>
                        <span style='font-size: 32px;'>🖼️</span>
                    </div>
                    <p style='margin: 8px 0 4px 0; font-size: 12px;'>{img['prompt'][:20]}...</p>
                    <p style='margin: 0; font-size: 12px; color: #999;'>{img['timestamp'].strftime('%H:%M')}</p>
                </div>
                """, unsafe_allow_html=True)
else:
    st.caption("还没有更多图像了")
'''


# ============================================================================
# 3. ModelPlayground - 模型试验场模板
# ============================================================================

class ModelPlayground:
    """
    模型试验场模板

    功能: 参数调节、模型对比、性能测试

    推荐主题: tech_neon, midnight_blue

    特性:
        - 参数调节
        - 实时测试
        - 性能对比
        - 日志记录
        - 结果导出
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
模型试验场 - Streamlit 实现
============================

功能: 参数调节、模型对比、性能测试
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="模型试验场",
    page_icon="🧪",
    layout="wide"
)


# ============================================================================
# 模拟测试数据
# ============================================================================

@st.cache_data
def get_test_models():
    """获取可测试模型列表"""
    return [
        {
            "id": "gpt-4",
            "name": "GPT-4",
            "provider": "OpenAI",
            "type": "LLM",
            "description": "最先进的大型语言模型",
            "max_tokens": 8192,
            "default_temp": 0.7
        },
        {
            "id": "claude-3",
            "name": "Claude 3",
            "provider": "Anthropic",
            "type": "LLM",
            "description": "注重安全的AI助手",
            "max_tokens": 200000,
            "default_temp": 0.7
        },
        {
            "id": "llama-2",
            "name": "Llama 2 70B",
            "provider": "Meta",
            "type": "LLM",
            "description": "开源高性能模型",
            "max_tokens": 4096,
            "default_temp": 0.8
        },
    ]


@st.cache_data
def get_test_results():
    """获取测试结果"""
    return [
        {
            "model_id": "gpt-4",
            "test_case": "文本生成",
            "temperature": 0.7,
            "latency_ms": 1250,
            "tokens_per_second": 8.5,
            "quality_score": 9.2,
            "timestamp": datetime.now()
        },
        {
            "model_id": "claude-3",
            "test_case": "文本生成",
            "temperature": 0.7,
            "latency_ms": 980,
            "tokens_per_second": 12.3,
            "quality_score": 8.8,
            "timestamp": datetime.now()
        },
    ]


# ============================================================================
# 主界面
# ============================================================================

st.title("🧪 AI 模型试验场")


# ============================================================================
# 模型选择
# ============================================================================

st.subheader("🔬 模型选择")

models = get_test_models()

selected_models = st.multiselect(
    "选择要测试的模型",
    [m["id"] for m in models],
    default=["gpt-4", "claude-3"],
    format_func=lambda x: next((m["name"] for m in models if m["id"] == x), x)
)

st.caption(f"已选择 {len(selected_models)} 个模型")

st.divider()


# ============================================================================
# 参数配置
# ============================================================================

st.subheader("⚙️ 参数配置")

col_param1, col_param2, col_param3 = st.columns(3)

with col_param1:
    st.markdown("#### 🌡️ 温度")
    temperature = st.slider(
        "Temperature",
        0.0, 1.0,
        0.7,
        0.1,
        help="影响输出随机性"
    )

with col_param2:
    st.markdown("#### 📏 最大Token数")
    max_tokens = st.slider(
        "Max Tokens",
        128, 4096,
        2048,
        256
    )

with col_param3:
    st.markdown("#### 🎯 Top-P")
    top_p = st.slider(
        "Top-P",
        0.0, 1.0,
        0.9,
        0.05,
        help="核采样参数"
    )

st.divider()


# ============================================================================
# 测试输入
# ============================================================================

st.subheader("📝 测试输入")

test_input = st.text_area(
    "测试输入",
    value="请写一个关于人工智能的简短介绍。",
    height=100,
    label_visibility="collapsed"
)

st.caption("💡 建议使用相同的输入进行模型对比测试")


# ============================================================================
# 运行测试
# ============================================================================

st.divider()

col_run1, col_run2, col_run3 = st.columns(3)

with col_run1:
    if st.button("▶️ 开始测试", use_container_width=True, type="primary", size="large"):
        st.session_state.test_running = True

        # 测试过程
        progress = st.progress(0)
        status_text = st.empty()

        for i in range(101):
            progress.progress(i / 100)
            status_text.text(f"测试进行中... {i}%")
            time.sleep(0.02)

        status_text.empty()
        st.success("✅ 测试完成！")

if st.session_state.get("test_running", False):
    st.session_state.test_running = False

with col_run2:
    if st.button("📊 查看结果", use_container_width=True):
        st.info("结果分析功能开发中...")

with col_run3:
    if st.button("🧪 压力测试", use_container_width=True):
        st.info("压力测试功能开发中...")


# ============================================================================
# 结果对比
# ============================================================================

st.divider()

st.subheader("📊 性能对比")

# 模拟测试结果
results = [
    {"model": "GPT-4", "latency": 1250, "tps": 8.5, "quality": 9.2},
    {"model": "Claude 3", "latency": 980, "tps": 12.3, "quality": 8.8},
    {"model": "Llama 2", "latency": 2100, "tps": 3.8, "quality": 7.5},
]

# 创建对比图表
fig = go.Figure()

# 延迟对比
fig.add_trace(go.Bar(
    x=[r["model"] for r in results],
    y=[r["latency"] for r in results],
    name="延迟 (ms)",
    marker_color="orange"
)

# TPS对比
fig.add_trace(go.Bar(
    x=[r["model"] for r in results],
    y=[r["tps"] for r in results],
    name="TPS",
    marker_color="green",
    yaxis="y2"
)

fig.update_layout(
    title="模型性能对比",
    xaxis_title="模型",
    yaxis_title="延迟 (ms)",
    yaxis2_title="TPS",
    barmode="group",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# 详细数据表
st.markdown("### 📋 详细数据")

df_results = pd.DataFrame(results)
st.dataframe(df_results, use_container_width=True)


# ============================================================================
# 测试日志
# ============================================================================

st.divider()

st.subheader("📋 测试日志")

log_data = [
    {"time": "14:23:15", "model": "GPT-4", "event": "测试开始"},
    {"time": "14:23:17", "model": "GPT-4", "event": "生成完成", "details": "延迟: 1250ms"},
    {"time": "14:23:17", "model": "Claude 3", "event": "测试开始"},
    {"time": "14:23:18", "model": "Claude 3", "event": "生成完成", "details": "延迟: 980ms"},
]

st.table(log_data, use_container_width=True)
'''


# ============================================================================
# 4. DataAnnotation - 数据标注模板
# ============================================================================

class DataAnnotation:
    """
    数据标注模板

    功能: 标签管理、快捷键操作、进度跟踪

    推荐主题: cool_mint, forest_green

    特性:
        - 多种标注类型
        - 键盘快捷键
        - 批量标注
        - 质量检查
        - 进度统计
        - 导出功能
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
数据标注 - Streamlit 实现
==========================

功能: 标签管理、快捷键操作、进度跟踪
"""

import streamlit as st
from datetime import datetime, timedelta


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="数据标注平台",
    page_icon="🏷️",
    layout="wide"
)


# ============================================================================
# 状态管理
# ============================================================================

if "annotation_task" not in st.session_state:
    st.session_state.annotation_task = {
        "id": "task_001",
        "type": "classification",
        "dataset": "product_images",
        "current_index": 0,
        "labels": ["电子产品", "服装", "食品", "家居", "其他"],
        "total": 100,
        "completed": 45,
        "instructions": "为每张图片选择最合适的分类标签"
    }

if "annotation_shortcuts" not in st.session_state:
    st.session_state.annotation_shortcuts = {
        "1": "电子产品",
        "2": "服装",
        "3": "食品",
        "4": "家居",
        "5": "其他",
        "space": "下一张",
        "backspace": "上一张",
        "s": "跳过",
        "enter": "确认"
    }


# ============================================================================
# 模拟数据
# ============================================================================

@st.cache_data
def get_annotation_data():
    """获取标注数据"""
    data = []
    categories = ["电子产品", "服装", "食品", "家居", "其他"]

    for i in range(100):
        data.append({
            "id": f"img_{i:04d}",
            "filename": f"image_{i:04d}.jpg",
            "category": categories[i % len(categories)] if i < 90 else categories[-1],
            "annotator": "管理员",
            "annotated_at": datetime.now() - timedelta(days=i),
            "confidence": 0.95 if i < 90 else 0.7
        })

    return data


# ============================================================================
# 主界面
# ============================================================================

st.title("🏷️ 数据标注平台")

task = st.session_state.annotation_task


# ============================================================================
# 进度统计
# ============================================================================

st.subheader("📊 标注进度")

progress = task["completed"] / task["total"] * 100

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.metric("已完成", f"{task['completed']}/{task['total']}")

with col_stat2:
    remaining = task["total"] - task["completed"]
    st.metric("待标注", remaining)

with col_stat3:
    eta_minutes = remaining * 0.5
    st.metric("预计剩余", f"{eta_minutes} 分钟")

with col_stat4:
    st.metric("进度", f"{progress:.0f}%")

st.progress(progress / 100)


# ============================================================================
# 标注工作区
# ============================================================================

st.divider()

# 获取当前数据
all_data = get_annotation_data()
current_index = task["current_index"]

if 0 <= current_index < len(all_data):
    current_data = all_data[current_index]
else:
    st.warning("🎉 所有数据已标注完成！")
    st.stop()


# 标注区域
col_work1, col_work2 = st.columns([3, 1])

with col_work1:
    st.markdown("### 🏷️ 标注工作区")

    # 图像显示
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background: #f9f9f9;'>
        <div style='font-size: 64px;'>🖼️</div>
        <p style='color: #666;'>{current_data['filename']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 标签按钮
    st.markdown("### 选择标签")

    # 快捷键提示
    st.caption("💡 快捷键：1-5 快速选择 | Space 跳过 | Backspace 返回")

    # 标签按钮网格
    label_cols = st.columns(len(task["labels"]))

    for i, label in enumerate(task["labels"]):
        with label_cols[i]:
            shortcut = str(i + 1)

            is_selected = (
                current_data.get("selected_label") == label
            )

            button_type = "primary" if is_selected else "secondary"

            if st.button(
                f"**{shortcut}** {label}",
                key=f'label_{i}',
                use_container_width=True,
                type=button_type
            ):
                current_data["selected_label"] = label
                all_data[current_index] = current_data
                st.session_state.annotation_task["current_index"] = current_index
                st.success(f"已选择: {label}")
                # 自动保存
                st.rerun()

    st.divider()

    # 置信度
    confidence = current_data.get("confidence", 0.95)
    st.markdown(f"**置信度:** {confidence:.0%}")

    col_conf1, col_conf2 = st.columns(2)

    with col_conf1:
        if st.button("✅ 高质量", use_container_width=True):
            current_data["confidence"] = 0.95

    with col_conf2:
        if st.button("⚠️ 低质量", use_container_width=True):
            current_data["confidence"] = 0.70

    st.divider()

    # 备注
    notes = st.text_area(
        "添加备注",
        value=current_data.get("notes", ""),
        height=60,
        key="annotation_notes"
    )

    if st.button("💾 保存备注"):
        current_data["notes"] = notes
        st.success("备注已保存")


# ============================================================================
# 侧边栏 - 控制面板
# ============================================================================

with col_work2:
    st.subheader("🎛️ 控制面板")

    # 进度
    st.markdown("### 📊 任务进度")

    current_num = current_index + 1
    total_num = task["total"]
    st.metric(f"{current_num}/{total_num}")

    st.caption("图像编号")

    st.divider()

    # 批量操作
    st.markdown("### 🔧 批量操作")

    if st.button("⏭️ 跳到", use_container_width=True):
        st.session_state.annotation_task["current_index"] = min(current_index + 5, len(all_data) - 1)
        st.rerun()

    if st.button("📥 导出数据", use_container_width=True):
        # 导出标注结果
        export_data = [
            {
                "filename": data["filename"],
                "category": data.get("selected_label", "未标注"),
                "confidence": data.get("confidence", 0),
                "notes": data.get("notes", "")
            }
            for data in all_data
        ]
        st.download_button(
            "下载标注结果",
            json.dumps(export_data, ensure_ascii=False, indent=2),
            "annotation_results.json",
            "application/json"
        )

    st.divider()

    # 快捷键参考
    st.markdown("### ⌨️ 快捷键")

    shortcut_html = """
    | 快捷键 | 功能 |
    |--------|------|
    | 1-5 | 选择标签 |
    | Space | 跳过当前 |
    | Backspace | 返回上一张 |
    | S | 跳到未处理项 |
    | Enter | 确认选择 |
    """

    st.markdown(shortcut_html)


# ============================================================================
# 导航控制
# ============================================================================

st.divider()

st.subheader("🧭 导航")

col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

with col_nav1:
    if st.button("⬅️ 上一张", use_container_width=True):
        if current_index > 0:
            st.session_state.annotation_task["current_index"] = current_index - 1
            st.rerun()

with col_nav2:
    if st.button("⏭️ 下一张", use_container_width=True):
        if current_index < len(all_data) - 1:
            st.session_state.annotation_task["current_index"] = current_index + 1
            st.rerun()

with col_nav3:
    if st.button("🔢 跳转到", use_container_width=True):
        jump_to = st.number_input("输入页码", min_value=1, max_value=len(all_data), value=1)
        if st.button("跳转", use_container_width=True):
            st.session_state.annotation_task["current_index"] = jump_to - 1
            st.rerun()

with col_nav4:
    if st.button("🏠️ 返回列表", use_container_width=True):
        st.info("返回任务列表")
'''


# ============================================================================
# 5. PipelineBuilder - AI 流水线模板
# ============================================================================

class PipelineBuilder:
    """
    AI 流水线构建器

    功能: 可视化设计、节点配置、流程执行

    推荐主题: tech_neon, midnight_blue

    特性:
        - 可视化画布
        - 拖拽节点
        - 参数配置
        - 流程执行
        - 日志监控
        - 模板保存
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
AI 流水线构建器 - Streamlit 实现
================================

功能: 可视化设计、节点配置、流程执行
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="AI 流水线构建器",
    page_icon="🔄",
    layout="wide"
)


# ============================================================================
# 状态管理
# ============================================================================

if "pipeline_nodes" not in st.session_state:
    st.session_state.pipeline_nodes = [
        {
            "id": "node_1",
            "type": "input",
            "name": "数据输入",
            "position": (100, 200),
            "config": {
                "source": "api",
                "format": "json"
            },
            "connections": ["node_2"]
        },
        {
            "id": "node_2",
            "type": "processing",
            "name": "数据清洗",
            "position": (100, 400),
            "config": {
                "operation": "clean",
                "remove_duplicates": True
            },
            "connections": ["node_3"]
        },
        {
            "id": "node_3",
            "type": "processing",
            "name": "AI 分析",
            "position": (100, 600),
            "config": {
                "model": "gpt-4",
                "prompt": "分析数据"
            },
            "connections": ["node_4"]
        },
        {
            "id": "node_4",
            "type": "output",
            "name": "结果输出",
            "position": (100, 800),
            "config": {
                "format": "json",
                "destination": "database"
            },
            "connections": []
        }
    ]

if "pipeline_running" not in st.session_state:
    st.session_state.pipeline_running = False

if "pipeline_logs" not in st.session_state:
    st.session_state.pipeline_logs = []


# ============================================================================
# 主界面
# ============================================================================

st.title("🔄 AI 流水线构建器")


# ============================================================================
# 顶部工具栏
# ============================================================================

st.subheader("🛠️ 工具栏")

col_tool1, col_tool2, col_tool3, col_tool4 = st.columns(4)

with col_tool1:
    if st.button("➕ 添加节点", use_container_width=True):
        st.info("添加节点功能开发中...")

with col_tool2:
    if st.button("💾 保存流水线", use_container_width=True):
        st.success("流水线已保存")

with col_tool3:
    if st.button("📋 加载模板", use_container_width=True):
        st.info("模板加载功能开发中...")

with col_tool4:
    if st.button("🗑️ 清空画布", use_container_width=True):
        st.session_state.pipeline_nodes = []
        st.success("画布已清空")
        st.rerun()

st.divider()


# ============================================================================
# 画布区域（简化版）
# ============================================================================

st.subheader("🎨 流水线画布")

# 空画布提示
canvas_height = 600

st.markdown(f"""
<style>
.pipeline-canvas {{
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border: 2px dashed #b0bddb;
    border-radius: 8px;
    height: {canvas_height}px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
}}
</style>
<div class='pipeline-canvas'>
    <div style='text-align: center;'>
        <div style='font-size: 64px;'>🔄</div>
        <p>流水线画布</p>
        <p>💡 拖拽节点到画布，创建 AI 流水线</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# 节点列表
# ============================================================================

st.divider()

st.subheader("📋 节点列表")

# 显示现有节点
for i, node in enumerate(st.session_state.pipeline_nodes):
    with st.expander(f"📍 {node['name']} ({node['type']})", expanded=False):
        col_node1, col_node2 = st.columns(2)

        with col_node1:
            st.markdown(f"**ID:** {node['id']}")

            st.markdown(f"**类型:** {node['type']}")

            # 配置显示
            st.markdown("**配置:**")
            st.json(node["config"])

        with col_node2:
            # 编辑按钮
            if st.button(f'⚙️ 编辑', key=f'edit_node_{i}', use_container_width=True):
                st.info(f"编辑节点: {node['name']}")

            if st.button(f'🗑️ 删除', key=f'delete_node_{i}', use_container_width=True):
                st.session_state.pipeline_nodes.pop(i)
                st.warning(f"已删除: {node['name']}")
                st.rerun()

        st.markdown("**连接:**")
        st.write(f"→ {', '.join(node['connections']) if node['connections'] else '无'}")


# ============================================================================
# 流程执行
# ============================================================================

st.divider()

st.subheader("🚀 流程执行")

if st.session_state.pipeline_nodes:
    col_exec1, col_exec2 = st.columns(2)

    with col_exec1:
        if st.button("▶️ 运行流水线", use_container_width=True, type="primary"):
            st.session_state.pipeline_running = True
            st.info("正在执行流水线...")

    with col_exec2:
        if st.button("⏹️ 停止", use_container_width=True):
            st.session_state.pipeline_running = False
            st.info("流水线已停止")

    # 模拟执行日志
    if st.session_state.pipeline_running:
        with st.container():
            st.markdown("### 📋 执行日志")

            # 模拟日志
            logs = [
                {"time": "14:23:15", "node": "数据输入", "status": "success", "message": "数据加载成功"},
                {"time": "14:23:16", "node": "数据清洗", "status": "success", "message": "去重完成，1024条→512条"},
                {"time": "14:23:17", "node": "AI 分析", "status": "success", "message": "GPT-4 处理完成"},
                {"time": "14:23:19", "node": "结果输出", "status": "success", "message": "结果已写入数据库"},
            ]

            for log in logs:
                status_icon = "✅" if log["status"] == "success" else "❌"
                st.markdown(f"{status_icon} `{log['time']}` - **{log['node']}**")
                st.write(log['message'])


# ============================================================================
# 模板示例
# ============================================================================

st.divider()

st.subheader("📚 预设模板")

templates = {
    "etl_pipeline": "ETL 数据处理流水线",
    "chatbot": "对话机器人流程",
    "data_analysis": "数据分析流程",
    "content_moderation": "内容审核流程",
    "document_processing": "文档处理流程"
}

for template_id, template_name in templates.items():
    if st.button(f'📋 {template_name}', key=f'template_{template_id}'):
        st.info(f"加载模板: {template_name}")


# ============================================================================
# 节点类型参考
# ============================================================================

st.divider()

st.subheader("📖 节点类型参考")

st.markdown("""
| 类型 | 说明 | 配置示例 |
|------|------|----------|
| **输入** | 数据源接入 | `{"source": "api", "format": "json"}` |
| **处理** | 数据处理 | `{"operation": "filter", "conditions": {...}}` |
| **模型** | AI 模型调用 | `{"model": "gpt-4", "prompt": "..."}` |
| **输出** | 结果输出 | `{"destination": "database", "format": "json"}` |
| **条件** | 条件分支 | `{"condition": "field == value", "true_node": "xxx", "false_node": "yyy"}` |
""")
'''


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "ChatRole",
    "MessageStatus",
    "ImageStyle",
    "AnnotationType",
    "NodeType",
    # 数据类
    "ChatMessage",
    "GenerationRequest",
    "ModelConfig",
    "AnnotationTask",
    "PipelineNode",
    # 模板类
    "ChatAssistant",
    "ImageGenerator",
    "ModelPlayground",
    "DataAnnotation",
    "PipelineBuilder",
]
