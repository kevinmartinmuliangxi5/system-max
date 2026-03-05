"""
Interaction Patterns - 交互模式库
==================================

定义 10 种常见 UI 交互模式，包括触发条件、状态管理、反馈机制和代码模板。

交互模式:
    1. FormPattern - 表单交互（验证、提交、重置）
    2. SearchPattern - 搜索交互（即时搜索、筛选、排序）
    3. PaginationPattern - 分页交互（翻页、跳转、每页数量）
    4. ModalPattern - 弹窗交互（打开、关闭、确认）
    5. ToastPattern - 提示交互（成功、错误、警告、信息）
    6. LoadingPattern - 加载交互（骨架屏、进度条、旋转图标）
    7. DragDropPattern - 拖拽交互（排序、移动、分组）
    8. InfiniteScrollPattern - 无限滚动（加载更多、回到顶部）
    9. TabSwitchPattern - 标签切换（懒加载、保持状态）
    10. CollapsiblePattern - 折叠展开（手风琴、树形）

使用方式:
    from ui_library.patterns import FormPattern, SearchPattern

    # 获取表单模式配置
    form_pattern = FormPattern()
    print(form_pattern.description)
    print(form_pattern.code_template)
"""

from typing import Dict, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


# ============================================================================
# 通用枚举定义
# ============================================================================

class TriggerType(Enum):
    """触发类型"""
    USER_CLICK = "user_click"           # 用户点击
    USER_INPUT = "user_input"           # 用户输入
    AUTOMATIC = "automatic"             # 自动触发
    TIMER = "timer"                     # 定时触发
    SCROLL = "scroll"                   # 滚动触发
    HOVER = "hover"                     # 悬停触发
    FOCUS = "focus"                     # 焦点触发
    KEYBOARD = "keyboard"               # 键盘触发


class StateType(Enum):
    """状态类型"""
    IDLE = "idle"                       # 空闲
    ACTIVE = "active"                   # 活跃
    LOADING = "loading"                 # 加载中
    SUCCESS = "success"                 # 成功
    ERROR = "error"                     # 错误
    DISABLED = "disabled"               # 禁用
    HIDDEN = "hidden"                   # 隐藏


class FeedbackType(Enum):
    """反馈类型"""
    VISUAL = "visual"                   # 视觉反馈
    AUDIO = "audio"                     # 音频反馈
    HAPTIC = "haptic"                   # 触觉反馈
    TOAST = "toast"                     # 消息提示
    MODAL = "modal"                     # 弹窗反馈
    INLINE = "inline"                   # 内联反馈


class ValidationRule(Enum):
    """验证规则"""
    REQUIRED = "required"               # 必填
    EMAIL = "email"                     # 邮箱格式
    PHONE = "phone"                     # 电话格式
    MIN_LENGTH = "min_length"           # 最小长度
    MAX_LENGTH = "max_length"           # 最大长度
    PATTERN = "pattern"                 # 正则匹配
    CUSTOM = "custom"                   # 自定义验证


# ============================================================================
# 基础交互模式类
# ============================================================================

@dataclass
class TriggerCondition:
    """触发条件"""
    type: TriggerType
    description: str
    selector: Optional[str] = None      # CSS 选择器或组件ID
    event_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "description": self.description,
            "selector": self.selector,
            "event_data": self.event_data,
        }


@dataclass
class StateTransition:
    """状态转换"""
    from_state: StateType
    to_state: StateType
    trigger: TriggerCondition
    action: Optional[str] = None
    feedback: Optional[FeedbackType] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_state.value,
            "to": self.to_state.value,
            "trigger": self.trigger.to_dict(),
            "action": self.action,
            "feedback": self.feedback.value if self.feedback else None,
        }


@dataclass
class FeedbackMechanism:
    """反馈机制"""
    type: FeedbackType
    message: str
    duration: Optional[int] = None      # 持续时间（毫秒）
    position: Optional[str] = None      # 位置
    style: Optional[str] = None         # 样式

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "message": self.message,
            "duration": self.duration,
            "position": self.position,
            "style": self.style,
        }


# ============================================================================
# 交互模式基类
# ============================================================================

class InteractionPattern(ABC):
    """交互模式基类"""

    def __init__(
        self,
        pattern_id: str,
        name: str,
        description: str,
        category: str
    ):
        self.pattern_id = pattern_id
        self.name = name
        self.description = description
        self.category = category
        self._triggers: List[TriggerCondition] = []
        self._states: List[StateType] = []
        self._transitions: List[StateTransition] = []
        self._feedbacks: List[FeedbackMechanism] = []

    @abstractmethod
    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        pass

    def add_trigger(self, trigger: TriggerCondition):
        """添加触发条件"""
        self._triggers.append(trigger)

    def add_state(self, state: StateType):
        """添加状态"""
        self._states.append(state)

    def add_transition(self, transition: StateTransition):
        """添加状态转换"""
        self._transitions.append(transition)

    def add_feedback(self, feedback: FeedbackMechanism):
        """添加反馈机制"""
        self._feedbacks.append(feedback)

    def get_triggers(self) -> List[TriggerCondition]:
        """获取所有触发条件"""
        return self._triggers.copy()

    def get_states(self) -> List[StateType]:
        """获取所有状态"""
        return self._states.copy()

    def get_transitions(self) -> List[StateTransition]:
        """获取所有状态转换"""
        return self._transitions.copy()

    def get_feedbacks(self) -> List[FeedbackMechanism]:
        """获取所有反馈机制"""
        return self._feedbacks.copy()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "pattern_id": self.pattern_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "triggers": [t.to_dict() for t in self._triggers],
            "states": [s.value for s in self._states],
            "transitions": [t.to_dict() for t in self._transitions],
            "feedbacks": [f.to_dict() for f in self._feedbacks],
        }


# ============================================================================
# 1. FormPattern - 表单交互模式
# ============================================================================

class FormPattern(InteractionPattern):
    """
    表单交互模式

    功能: 验证、提交、重置
    状态: 空闲、编辑、验证中、提交中、成功、错误
    """

    def __init__(self):
        super().__init__(
            pattern_id="form",
            name="表单交互",
            description="处理用户输入的表单交互，包括字段验证、提交处理和重置功能",
            category="data_entry"
        )

        # 定义状态
        for state in [StateType.IDLE, StateType.ACTIVE, StateType.LOADING,
                     StateType.SUCCESS, StateType.ERROR]:
            self.add_state(state)

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_INPUT,
            description="用户开始输入表单字段"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击提交按钮",
            selector="form_submit_button"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击重置按钮",
            selector="form_reset_button"
        ))

        # 定义状态转换
        self._setup_form_transitions()

        # 定义反馈机制
        self._setup_form_feedbacks()

    def _setup_form_transitions(self):
        """设置表单状态转换"""
        # 空闲 -> 编辑 (用户输入)
        self.add_transition(StateTransition(
            from_state=StateType.IDLE,
            to_state=StateType.ACTIVE,
            trigger=TriggerCondition(TriggerType.USER_INPUT, "开始输入"),
        ))

        # 编辑 -> 提交中 (点击提交)
        self.add_transition(StateTransition(
            from_state=StateType.ACTIVE,
            to_state=StateType.LOADING,
            trigger=TriggerCondition(TriggerType.USER_CLICK, "点击提交"),
            action="validate_and_submit",
        ))

        # 提交中 -> 成功 (提交成功)
        self.add_transition(StateTransition(
            from_state=StateType.LOADING,
            to_state=StateType.SUCCESS,
            trigger=TriggerCondition(TriggerType.AUTOMATIC, "服务器响应"),
            feedback=FeedbackType.TOAST,
        ))

        # 提交中 -> 错误 (提交失败)
        self.add_transition(StateTransition(
            from_state=StateType.LOADING,
            to_state=StateType.ERROR,
            trigger=TriggerCondition(TriggerType.AUTOMATIC, "服务器错误"),
            feedback=FeedbackType.TOAST,
        ))

    def _setup_form_feedbacks(self):
        """设置表单反馈机制"""
        # 验证错误反馈
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.INLINE,
            message="字段验证失败",
            style="error"
        ))

        # 提交成功反馈
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.TOAST,
            message="表单提交成功",
            duration=3000,
            position="top-right",
            style="success"
        ))

        # 提交失败反馈
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.TOAST,
            message="提交失败，请重试",
            duration=5000,
            position="top-right",
            style="error"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 表单交互模板
"""
import streamlit as st

# ============================================================================
# 表单状态管理
# ============================================================================

if "form_state" not in st.session_state:
    st.session_state.form_state = "idle"  # idle, editing, submitting, success, error
if "form_data" not in st.session_state:
    st.session_state.form_data = {}
if "form_errors" not in st.session_state:
    st.session_state.form_errors = {}


# ============================================================================
# 验证函数
# ============================================================================

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    import re
    pattern = r"^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
    return re.match(pattern, email) is not None


def validate_required(value: str) -> bool:
    """验证必填字段"""
    return value and len(value.strip()) > 0


def validate_form(data: Dict[str, Any]) -> Dict[str, str]:
    """
    验证表单数据

    Returns:
        错误字典，字段名 -> 错误消息
    """
    errors = {}

    # 验证姓名（必填）
    if not validate_required(data.get("name", "")):
        errors["name"] = "姓名为必填项"

    # 验证邮箱
    email = data.get("email", "")
    if not validate_required(email):
        errors["email"] = "邮箱为必填项"
    elif not validate_email(email):
        errors["email"] = "邮箱格式不正确"

    # 验证电话（可选，但如果填写则需要格式正确）
    phone = data.get("phone", "")
    if phone and not phone.replace("-", "").isdigit():
        errors["phone"] = "电话只能包含数字和横线"

    return errors


# ============================================================================
# 提交处理
# ============================================================================

def submit_form(data: Dict[str, Any]) -> bool:
    """
    提交表单数据

    Args:
        data: 表单数据

    Returns:
        是否提交成功
    """
    # 这里添加实际的提交逻辑
    # 例如: API 调用、数据库写入等

    import time
    time.sleep(1)  # 模拟网络请求

    # 模拟 90% 成功率
    import random
    return random.random() > 0.1


def reset_form():
    """重置表单"""
    st.session_state.form_data = {}
    st.session_state.form_errors = {}
    st.session_state.form_state = "idle"


# ============================================================================
# UI 渲染
# ============================================================================

st.title("📝 用户信息表单")

# 成功/错误消息显示
if st.session_state.form_state == "success":
    st.success("✅ 表单提交成功！感谢您的反馈。")
    if st.button("填写新的表单"):
        reset_form()
        st.rerun()
    st.stop()  # 停止执行，不显示表单

elif st.session_state.form_state == "error":
    st.error("❌ 提交失败，请检查输入后重试。")


# 表单主体
with st.form("user_info_form", clear_on_submit=False):
    st.subheader("基本信息")

    # 姓名输入
    name = st.text_input(
        "姓名 *",
        value=st.session_state.form_data.get("name", ""),
        help="请输入您的真实姓名"
    )
    if "name" in st.session_state.form_errors:
        st.error(st.session_state.form_errors["name"])

    # 邮箱输入
    email = st.text_input(
        "邮箱 *",
        value=st.session_state.form_data.get("email", ""),
        help="我们将通过此邮箱与您联系"
    )
    if "email" in st.session_state.form_errors:
        st.error(st.session_state.form_errors["email"])

    # 电话输入
    phone = st.text_input(
        "电话",
        value=st.session_state.form_data.get("phone", ""),
        help="选填，格式: 010-12345678"
    )
    if "phone" in st.session_state.form_errors:
        st.error(st.session_state.form_errors["phone"])

    # 备注
    notes = st.text_area(
        "备注",
        value=st.session_state.form_data.get("notes", ""),
        help="任何您想补充的信息"
    )

    st.divider()

    # 按钮组
    col1, col2, col3 = st.columns(3)

    with col1:
        submitted = st.form_submit_button("提交", use_container_width=True, type="primary")

    with col2:
        reset = st.form_submit_button("重置", use_container_width=True)

    with col3:
        cancel = st.form_submit_button("取消", use_container_width=True)


# ============================================================================
# 事件处理
# ============================================================================

# 重置按钮
if reset:
    reset_form()
    st.rerun()

# 取消按钮
if cancel:
    st.session_state.form_data = {}
    st.session_state.form_state = "idle"
    st.rerun()

# 提交按钮
if submitted:
    # 收集表单数据
    form_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "notes": notes,
    }

    # 验证表单
    errors = validate_form(form_data)

    if errors:
        # 有验证错误
        st.session_state.form_data = form_data
        st.session_state.form_errors = errors
        st.session_state.form_state = "error"
        st.rerun()
    else:
        # 验证通过，提交
        st.session_state.form_state = "submitting"
        with st.spinner("正在提交..."):
            success = submit_form(form_data)

        if success:
            st.session_state.form_state = "success"
            st.session_state.form_data = {}
            st.session_state.form_errors = {}
        else:
            st.session_state.form_state = "error"
            st.session_state.form_data = form_data

        st.rerun()
'''

        elif framework == "react":
            return '''"""
React 表单交互模板 (使用 React Hook Form)
"""
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";

// ============================================================================
// 验证 Schema
// ============================================================================

const formSchema = z.object({
  name: z.string().min(2, "姓名至少2个字符"),
  email: z.string().email("邮箱格式不正确"),
  phone: z.string().regex(/^[0-9-]+$/, "电话只能包含数字和横线").optional(),
  notes: z.string().optional(),
});

type FormData = z.infer<typeof formSchema>;


// ============================================================================
// 表单组件
// ============================================================================

export function FormPattern() {
  const [submitState, setSubmitState] = useState<"idle" | "loading" | "success" | "error">("idle");

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = async (data: FormData) => {
    setSubmitState("loading");

    try {
      const response = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        setSubmitState("success");
        reset();
      } else {
        setSubmitState("error");
      }
    } catch (error) {
      setSubmitState("error");
    }
  };

  const handleReset = () => {
    reset();
    setSubmitState("idle");
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">用户信息表单</h1>

      {/* 成功消息 */}
      {submitState === "success" && (
        <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800">✅ 表单提交成功！</p>
        </div>
      )}

      {/* 错误消息 */}
      {submitState === "error" && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800">❌ 提交失败，请重试。</p>
        </div>
      )}

      {/* 表单 */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* 姓名字段 */}
        <div>
          <label className="block text-sm font-medium mb-1">姓名 *</label>
          <input
            {...register("name")}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="请输入您的真实姓名"
          />
          {errors.name && (
            <p className="text-red-500 text-sm mt-1">{errors.name.message}</p>
          )}
        </div>

        {/* 邮箱字段 */}
        <div>
          <label className="block text-sm font-medium mb-1">邮箱 *</label>
          <input
            {...register("email")}
            type="email"
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="your@email.com"
          />
          {errors.email && (
            <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
          )}
        </div>

        {/* 电话字段 */}
        <div>
          <label className="block text-sm font-medium mb-1">电话</label>
          <input
            {...register("phone")}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="010-12345678"
          />
          {errors.phone && (
            <p className="text-red-500 text-sm mt-1">{errors.phone.message}</p>
          )}
        </div>

        {/* 备注字段 */}
        <div>
          <label className="block text-sm font-medium mb-1">备注</label>
          <textarea
            {...register("notes")}
            rows={4}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="任何您想补充的信息"
          />
        </div>

        {/* 按钮组 */}
        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            disabled={submitState === "loading"}
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
          >
            {submitState === "loading" ? "提交中..." : "提交"}
          </button>
          <button
            type="button"
            onClick={handleReset}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            重置
          </button>
        </div>
      </form>
    </div>
  );
}
'''
        else:
            return f"// {framework} 框架的表单交互模板待实现"


# ============================================================================
# 2. SearchPattern - 搜索交互模式
# ============================================================================

class SearchPattern(InteractionPattern):
    """
    搜索交互模式

    功能: 即时搜索、筛选、排序
    状态: 空闲、搜索中、有结果、无结果、错误
    """

    def __init__(self):
        super().__init__(
            pattern_id="search",
            name="搜索交互",
            description="处理搜索输入、结果筛选和排序功能",
            category="data_retrieval"
        )

        # 定义状态
        for state in [StateType.IDLE, StateType.LOADING, StateType.ACTIVE,
                     StateType.ERROR]:
            self.add_state(state)

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_INPUT,
            description="用户输入搜索关键词"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击筛选条件",
            selector="filter_checkbox"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击排序",
            selector="sort_button"
        ))

        # 定义反馈机制
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.INLINE,
            message="找到 X 个结果",
            style="info"
        ))
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.INLINE,
            message="未找到相关结果",
            style="warning"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 搜索交互模板
"""
import streamlit as st
from typing import List, Dict, Any
import time


# ============================================================================
# 搜索状态管理
# ============================================================================

if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "search_filters" not in st.session_state:
    st.session_state.search_filters = {
        "category": [],
        "date_range": None,
        "status": [],
    }
if "search_sort" not in st.session_state:
    st.session_state.search_sort = "relevance"  # relevance, date_asc, date_desc
if "search_page" not in st.session_state:
    st.session_state.search_page = 1


# ============================================================================
# 模拟数据
# ============================================================================

SAMPLE_DATA = [
    {"id": 1, "title": "Python 数据分析入门", "category": "编程", "date": "2024-01-15", "status": "published"},
    {"id": 2, "title": "机器学习实战指南", "category": "AI", "date": "2024-01-20", "status": "published"},
    {"id": 3, "title": "Web 开发最佳实践", "category": "编程", "date": "2024-02-01", "status": "draft"},
    {"id": 4, "title": "深度学习框架对比", "category": "AI", "date": "2024-02-10", "status": "published"},
    {"id": 5, "title": "数据库优化技巧", "category": "数据库", "date": "2024-02-15", "status": "published"},
    {"id": 6, "title": "前端性能优化", "category": "编程", "date": "2024-02-20", "status": "published"},
    {"id": 7, "title": "容器化部署指南", "category": "运维", "date": "2024-03-01", "status": "draft"},
    {"id": 8, "title": "自然语言处理基础", "category": "AI", "date": "2024-03-05", "status": "published"},
]


# ============================================================================
# 搜索函数
# ============================================================================

def perform_search(
    query: str,
    filters: Dict[str, Any],
    sort_by: str
) -> List[Dict[str, Any]]:
    """
    执行搜索

    Args:
        query: 搜索关键词
        filters: 筛选条件
        sort_by: 排序方式

    Returns:
        搜索结果列表
    """
    # 模拟搜索延迟
    time.sleep(0.3)

    results = SAMPLE_DATA.copy()

    # 关键词过滤
    if query:
        query_lower = query.lower()
        results = [r for r in results if query_lower in r["title"].lower()]

    # 分类筛选
    if filters.get("category"):
        results = [r for r in results if r["category"] in filters["category"]]

    # 状态筛选
    if filters.get("status"):
        results = [r for r in results if r["status"] in filters["status"]]

    # 排序
    if sort_by == "date_asc":
        results.sort(key=lambda x: x["date"])
    elif sort_by == "date_desc":
        results.sort(key=lambda x: x["date"], reverse=True)
    # relevance 默认顺序

    return results


# ============================================================================
# UI 渲染
# ============================================================================

st.title("🔍 搜索中心")

# ============================================================================
# 搜索栏
# ============================================================================

col1, col2 = st.columns([4, 1])

with col1:
    search_query = st.text_input(
        "搜索关键词",
        value=st.session_state.search_query,
        placeholder="输入关键词搜索...",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("搜索", use_container_width=True, type="primary")


# ============================================================================
# 筛选和排序
# ============================================================================

with st.expander("🔧 筛选和排序", expanded=False):
    col1, col2, col3 = st.columns(3)

    with col1:
        # 分类筛选
        categories = list(set(d["category"] for d in SAMPLE_DATA))
        selected_categories = st.multiselect(
            "分类",
            categories,
            default=st.session_state.search_filters.get("category", []),
            label_visibility="visible"
        )

    with col2:
        # 状态筛选
        statuses = list(set(d["status"] for d in SAMPLE_DATA))
        selected_statuses = st.multiselect(
            "状态",
            statuses,
            default=st.session_state.search_filters.get("status", []),
            label_visibility="visible"
        )

    with col3:
        # 排序方式
        sort_options = {
            "relevance": "相关性",
            "date_asc": "日期 (升序)",
            "date_desc": "日期 (降序)",
        }
        selected_sort = st.selectbox(
            "排序方式",
            options=list(sort_options.keys()),
            format_func=lambda x: sort_options[x],
            index=list(sort_options.keys()).index(st.session_state.search_sort),
            label_visibility="visible"
        )


# ============================================================================
# 搜索执行
# ============================================================================

# 检测是否需要重新搜索
should_search = (
    search_button or
    search_query != st.session_state.search_query or
    selected_categories != st.session_state.search_filters.get("category", []) or
    selected_statuses != st.session_state.search_filters.get("status", []) or
    selected_sort != st.session_state.search_sort
)

if should_search:
    # 更新状态
    st.session_state.search_query = search_query
    st.session_state.search_filters["category"] = selected_categories
    st.session_state.search_filters["status"] = selected_statuses
    st.session_state.search_sort = selected_sort
    st.session_state.search_page = 1

    # 执行搜索
    with st.spinner("正在搜索..."):
        st.session_state.search_results = perform_search(
            query=search_query,
            filters=st.session_state.search_filters,
            sort_by=selected_sort
        )


# ============================================================================
# 结果展示
# ============================================================================

st.divider()

results = st.session_state.search_results

if not search_query and not st.session_state.search_filters.get("category") and not st.session_state.search_filters.get("status"):
    # 初始状态
    st.info("💡 请输入关键词或选择筛选条件开始搜索")
    st.markdown("### 热门搜索")
    st.markdown("- Python 教程\\n- 机器学习\\n- Web 开发")

elif not results:
    # 无结果
    st.warning(f"⚠️ 未找到与 '{search_query}' 相关的结果")
    st.markdown("**建议:**")
    st.markdown("- 检查关键词拼写\\n- 尝试更通用的关键词\\n- 减少筛选条件")

else:
    # 有结果
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"### 找到 {len(results)} 个结果")

    with col2:
        st.metric("当前页", st.session_state.search_page)

    # 结果列表
    for i, item in enumerate(results, 1):
        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"**{item['title']}**")
                st.caption(f"分类: {item['category']} | 日期: {item['date']}")

            with col2:
                status_color = "🟢" if item['status'] == "published" else "🟡"
                st.markdown(f"{status_color} {item['status']}")

            st.divider()


# ============================================================================
# 清除按钮
# ============================================================================

if st.session_state.search_query or st.session_state.search_filters.get("category") or st.session_state.search_filters.get("status"):
    if st.button("🗑️ 清除筛选", use_container_width=True):
        st.session_state.search_query = ""
        st.session_state.search_filters = {"category": [], "date_range": None, "status": []}
        st.session_state.search_sort = "relevance"
        st.session_state.search_results = []
        st.rerun()
'''
        return self._generate_generic_template("搜索交互")


# ============================================================================
# 3. PaginationPattern - 分页交互模式
# ============================================================================

class PaginationPattern(InteractionPattern):
    """
    分页交互模式

    功能: 翻页、跳转、每页数量
    状态: 首页、中间页、末页、跳转中
    """

    def __init__(self):
        super().__init__(
            pattern_id="pagination",
            name="分页交互",
            description="处理数据分页展示、页码切换和每页数量设置",
            category="navigation"
        )

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击页码",
            selector="page_number"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击上一页/下一页",
            selector="prev_next_button"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_INPUT,
            description="用户输入跳转页码",
            selector="page_jump_input"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_INPUT,
            description="用户更改每页数量",
            selector="page_size_select"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 分页交互模板
"""
import streamlit as st
from typing import List, Any


# ============================================================================
# 分页状态管理
# ============================================================================

if "pagination_page" not in st.session_state:
    st.session_state.pagination_page = 1
if "pagination_size" not in st.session_state:
    st.session_state.pagination_size = 10


# ============================================================================
# 分页组件
# ============================================================================

def render_pagination(
    total_items: int,
    page: int,
    page_size: int,
    page_key: str = "default"
) -> int:
    """
    渲染分页控件

    Args:
        total_items: 总项目数
        page: 当前页码
        page_size: 每页数量
        page_key: 分页组件唯一标识

    Returns:
        新的页码
    """
    total_pages = max(1, (total_items + page_size - 1) // page_size)

    # 确保页码在有效范围内
    page = max(1, min(page, total_pages))

    st.divider()

    col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 2, 2])

    with col1:
        st.caption(f"共 {total_items} 项，第 {page}/{total_pages} 页")

    with col2:
        # 每页数量选择
        new_size = st.selectbox(
            "每页",
            options=[5, 10, 20, 50, 100],
            index=[5, 10, 20, 50, 100].index(page_size),
            label_visibility="collapsed",
            key=f"page_size_{page_key}"
        )
        if new_size != page_size:
            st.session_state.pagination_size = new_size
            st.session_state.pagination_page = 1  # 重置到第一页
            st.rerun()

    with col3:
        # 上一页按钮
        if st.button("⬅️ 上一页", disabled=page <= 1, use_container_width=True, key=f"prev_{page_key}"):
            st.session_state.pagination_page = page - 1
            st.rerun()

    with col4:
        # 页码输入
        new_page = st.number_input(
            "跳转",
            min_value=1,
            max_value=total_pages,
            value=page,
            label_visibility="collapsed",
            key=f"page_jump_{page_key}"
        )
        if new_page != page:
            st.session_state.pagination_page = int(new_page)
            st.rerun()

    with col5:
        # 下一页按钮
        if st.button("下一页 ➡️", disabled=page >= total_pages, use_container_width=True, key=f"next_{page_key}"):
            st.session_state.pagination_page = page + 1
            st.rerun()

    # 页码快捷按钮
    if total_pages <= 7:
        # 总页数较少，显示全部
        page_nums = list(range(1, total_pages + 1))
    else:
        # 总页数较多，显示部分
        if page <= 3:
            page_nums = [1, 2, 3, 4, "...", total_pages]
        elif page >= total_pages - 2:
            page_nums = [1, "...", total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
        else:
            page_nums = [1, "...", page - 1, page, page + 1, "...", total_pages]

    cols = st.columns(len(page_nums))
    for col, p in zip(cols, page_nums):
        with col:
            if p == "...":
                st.write("...")
            elif p == page:
                st.button(str(p), disabled=True, use_container_width=True, key=f"page_{p}_{page_key}")
            else:
                if st.button(str(p), use_container_width=True, key=f"page_{p}_{page_key}"):
                    st.session_state.pagination_page = p
                    st.rerun()

    return page


def get_paginated_data(data: List[Any], page: int, page_size: int) -> List[Any]:
    """
    获取当前页数据

    Args:
        data: 完整数据列表
        page: 当前页码（从1开始）
        page_size: 每页数量

    Returns:
        当前页的数据
    """
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return data[start_idx:end_idx]


# ============================================================================
# 使用示例
# ============================================================================

st.title("📄 分页示例")

# 模拟数据
sample_data = [f"项目 {i+1}" for i in range(100)]

# 获取分页数据
current_page = st.session_state.pagination_page
page_size = st.session_state.pagination_size
paginated_data = get_paginated_data(sample_data, current_page, page_size)

# 显示当前页数据
st.subheader(f"第 {current_page} 页内容")

for item in paginated_data:
    st.write(f"- {item}")

# 渲染分页控件
render_pagination(
    total_items=len(sample_data),
    page=current_page,
    page_size=page_size,
    page_key="example"
)
'''
        return self._generate_generic_template("分页交互")


# ============================================================================
# 4. ModalPattern - 弹窗交互模式
# ============================================================================

class ModalPattern(InteractionPattern):
    """
    弹窗交互模式

    功能: 打开、关闭、确认
    状态: 关闭、打开中、已打开、确认中
    """

    def __init__(self):
        super().__init__(
            pattern_id="modal",
            name="弹窗交互",
            description="处理模态对话框的显示、隐藏和用户确认操作",
            category="feedback"
        )

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户触发打开弹窗",
            selector="modal_trigger"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击关闭按钮",
            selector="modal_close"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击遮罩层",
            selector="modal_overlay"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.KEYBOARD,
            description="用户按 ESC 键"
        ))

        # 定义反馈机制
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.VISUAL,
            message="淡入动画",
            style="fade_in"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 弹窗交互模板
"""
import streamlit as st


# ============================================================================
# 弹窗状态管理
# ============================================================================

if "modal_open" not in st.session_state:
    st.session_state.modal_open = False
if "modal_title" not in st.session_state:
    st.session_state.modal_title = ""
if "modal_content" not in st.session_state:
    st.session_state.modal_content = ""
if "modal_type" not in st.session_state:
    st.session_state.modal_type = "info"  # info, warning, error, success
if "modal_on_confirm" not in st.session_state:
    st.session_state.modal_on_confirm = None


# ============================================================================
# 弹窗组件
# ============================================================================

def open_modal(
    title: str,
    content: str,
    modal_type: str = "info",
    on_confirm: Optional[callable] = None
):
    """打开弹窗"""
    st.session_state.modal_open = True
    st.session_state.modal_title = title
    st.session_state.modal_content = content
    st.session_state.modal_type = modal_type
    st.session_state.modal_on_confirm = on_confirm


def close_modal():
    """关闭弹窗"""
    st.session_state.modal_open = False
    st.session_state.modal_title = ""
    st.session_state.modal_content = ""
    st.session_state.modal_on_confirm = None


def render_modal():
    """渲染弹窗"""
    if not st.session_state.modal_open:
        return

    # 根据类型设置图标和样式
    type_config = {
        "info": {"icon": "ℹ️", "color": "blue"},
        "warning": {"icon": "⚠️", "color": "yellow"},
        "error": {"icon": "❌", "color": "red"},
        "success": {"icon": "✅", "color": "green"},
        "confirm": {"icon": "❓", "color": "blue"},
    }

    config = type_config.get(st.session_state.modal_type, type_config["info"])

    # 创建弹窗容器
    with st.container():
        # 遮罩层样式
        st.markdown("""
        <style>
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999;
        }
        .modal-content {
            background-color: white;
            padding: 2rem;
            border-radius: 0.5rem;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)

        # 弹窗内容
        col1, col2, col3 = st.columns([1, 4, 1])

        with col2:
            st.markdown(f"### {config['icon']} {st.session_state.modal_title}")
            st.write(st.session_state.modal_content)

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("取消", use_container_width=True, key="modal_cancel"):
                    close_modal()
                    st.rerun()

            with col2:
                st.write("")

            with col3:
                if st.button("确认", use_container_width=True, key="modal_confirm", type="primary"):
                    if st.session_state.modal_on_confirm:
                        st.session_state.modal_on_confirm()
                    close_modal()
                    st.rerun()


# ============================================================================
# 使用示例
# ============================================================================

st.title("🪟 弹窗交互示例")

# 不同类型的弹窗
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("信息弹窗", use_container_width=True):
        open_modal(
            title="系统信息",
            content="这是一条普通的信息消息，用于向用户传达某些信息。",
            modal_type="info"
        )
        st.rerun()

with col2:
    if st.button("确认弹窗", use_container_width=True):
        open_modal(
            title="删除确认",
            content="您确定要删除此项目吗？此操作不可撤销。",
            modal_type="confirm",
            on_confirm=lambda: st.success("已删除")
        )
        st.rerun()

with col3:
    if st.button("警告弹窗", use_container_width=True):
        open_modal(
            title="操作警告",
            content="此操作可能会影响系统性能，建议在低峰期执行。",
            modal_type="warning"
        )
        st.rerun()

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("成功弹窗", use_container_width=True):
        open_modal(
            title="操作成功",
            content="您的操作已成功完成！",
            modal_type="success"
        )
        st.rerun()

with col2:
    if st.button("错误弹窗", use_container_width=True):
        open_modal(
            title="操作失败",
            content="操作失败，请检查输入后重试。",
            modal_type="error"
        )
        st.rerun()

# 渲染弹窗
render_modal()
'''
        return self._generate_generic_template("弹窗交互")


# ============================================================================
# 5. ToastPattern - 提示交互模式
# ============================================================================

class ToastPattern(InteractionPattern):
    """
    提示交互模式

    功能: 成功、错误、警告、信息
    状态: 显示、消失
    """

    def __init__(self):
        super().__init__(
            pattern_id="toast",
            name="提示交互",
            description="处理临时消息提示的显示和自动消失",
            category="feedback"
        )

        # 定义触发条件
        for msg_type in ["success", "error", "warning", "info"]:
            self.add_trigger(TriggerCondition(
                type=TriggerType.AUTOMATIC,
                description=f"{msg_type} 消息触发"
            ))

        # 定义反馈机制
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.TOAST,
            message="操作成功",
            duration=3000,
            position="top-right"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 提示交互模板
"""
import streamlit as st
import time


# ============================================================================
# Toast 状态管理
# ============================================================================

if "toast_queue" not in st.session_state:
    st.session_state.toast_queue = []


# ============================================================================
# Toast 组件
# ============================================================================

def show_toast(
    message: str,
    toast_type: str = "info",
    duration: int = 3000,
    position: str = "top-right"
):
    """
    显示 Toast 提示

    Args:
        message: 消息内容
        toast_type: 类型 (success, error, warning, info)
        duration: 持续时间（毫秒）
        position: 位置
    """
    toast = {
        "message": message,
        "type": toast_type,
        "duration": duration,
        "position": position,
        "timestamp": time.time()
    }
    st.session_state.toast_queue.append(toast)


def render_toasts():
    """渲染待显示的 Toast"""
    if not st.session_state.toast_queue:
        return

    current_time = time.time()
    active_toasts = []

    for toast in st.session_state.toast_queue:
        # 检查是否应该过期
        if current_time - toast["timestamp"] < toast["duration"] / 1000:
            active_toasts.append(toast)

    st.session_state.toast_queue = active_toasts

    # 渲染 Toast
    for i, toast in enumerate(active_toasts):
        _render_single_toast(toast, i)


def _render_single_toast(toast: dict, index: int):
    """渲染单个 Toast"""
    type_config = {
        "success": {"icon": "✅", "bg": "#d4edda", "border": "#c3e6cb", "text": "#155724"},
        "error": {"icon": "❌", "bg": "#f8d7da", "border": "#f5c6cb", "text": "#721c24"},
        "warning": {"icon": "⚠️", "bg": "#fff3cd", "border": "#ffeaa7", "text": "#856404"},
        "info": {"icon": "ℹ️", "bg": "#d1ecf1", "border": "#bee5eb", "text": "#0c5460"},
    }

    config = type_config.get(toast["type"], type_config["info"])

    # 位置样式
    position_styles = {
        "top-right": "position: fixed; top: 20px; right: 20px;",
        "top-left": "position: fixed; top: 20px; left: 20px;",
        "bottom-right": "position: fixed; bottom: 20px; right: 20px;",
        "bottom-left": "position: fixed; bottom: 20px; left: 20px;",
        "top-center": "position: fixed; top: 20px; left: 50%; transform: translateX(-50%);",
    }

    position_style = position_styles.get(toast["position"], position_styles["top-right"])

    st.markdown(f"""
    <div style="{position_style} z-index: {9990 - index}; margin-bottom: 10px;">
        <div style="background: {config['bg']}; border: 1px solid {config['border']};
                    border-radius: 4px; padding: 12px 20px; display: flex; align-items: center;
                    gap: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <span style="font-size: 20px;">{config['icon']}</span>
            <span style="color: {config['text']}; font-size: 14px;">{toast['message']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# 使用示例
# ============================================================================

st.title("🔔 Toast 提示示例")

# Toast 触发按钮
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("成功提示", use_container_width=True, type="primary"):
        show_toast("操作成功完成！", "success", 3000)

with col2:
    if st.button("错误提示", use_container_width=True):
        show_toast("操作失败，请重试", "error", 5000)

with col3:
    if st.button("警告提示", use_container_width=True):
        show_toast("请注意检查输入", "warning", 4000)

with col4:
    if st.button("信息提示", use_container_width=True):
        show_toast("这是一条普通信息", "info", 3000)

st.divider()

# 自定义 Toast
st.subheader("自定义 Toast")

col1, col2 = st.columns(2)

with col1:
    message = st.text_input("消息内容", value="自定义消息")

with col2:
    duration = st.slider("持续时间 (秒)", 1, 10, 3)

position = st.selectbox(
    "位置",
    ["top-right", "top-left", "bottom-right", "bottom-left", "top-center"],
    index=0
)

toast_type = st.selectbox(
    "类型",
    ["success", "error", "warning", "info"],
    index=0
)

if st.button("显示自定义 Toast", use_container_width=True):
    show_toast(message, toast_type, duration * 1000, position)

# 渲染 Toast
render_toasts()
'''
        return self._generate_generic_template("提示交互")


# ============================================================================
# 6. LoadingPattern - 加载交互模式
# ============================================================================

class LoadingPattern(InteractionPattern):
    """
    加载交互模式

    功能: 骨架屏、进度条、旋转图标
    状态: 空闲、加载中、完成、失败
    """

    def __init__(self):
        super().__init__(
            pattern_id="loading",
            name="加载交互",
            description="处理数据加载过程中的视觉反馈",
            category="feedback"
        )

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.AUTOMATIC,
            description="数据请求开始"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.AUTOMATIC,
            description="数据请求完成"
        ))

        # 定义反馈机制
        for style in ["spinner", "skeleton", "progress_bar"]:
            self.add_feedback(FeedbackMechanism(
                type=FeedbackType.VISUAL,
                message="加载中...",
                style=style
            ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 加载交互模板
"""
import streamlit as st
import time
import random


# ============================================================================
# 加载状态管理
# ============================================================================

if "loading_state" not in st.session_state:
    st.session_state.loading_state = "idle"  # idle, loading, success, error
if "loading_progress" not in st.session_state:
    st.session_state.loading_progress = 0


# ============================================================================
# 骨架屏组件
# ============================================================================

def render_skeleton(rows: int = 3, height: int = 100):
    """渲染骨架屏"""
    skeleton_css = """
    <style>
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s infinite;
        border-radius: 4px;
    }
    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    </style>
    """
    st.markdown(skeleton_css, unsafe_allow_html=True)

    for i in range(rows):
        st.markdown(f'<div class="skeleton" style="height: {height}px; margin-bottom: 10px;"></div>',
                   unsafe_allow_html=True)


# ============================================================================
# 进度条组件
# ============================================================================

def render_progress_with_steps(steps: list, current_step: int):
    """渲染步骤进度条"""
    cols = st.columns(len(steps))

    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if i < current_step:
                st.success(step)
            elif i == current_step:
                st.info(step)
            else:
                st.caption(step)


# ============================================================================
# 模拟加载函数
# ============================================================================

def simulate_loading(style: str = "spinner") -> bool:
    """模拟加载过程"""
    st.session_state.loading_state = "loading"

    if style == "spinner":
        with st.spinner("正在加载..."):
            time.sleep(2)
        st.success("加载完成！")

    elif style == "progress_bar":
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(101):
            progress_bar.progress(i)
            status_text.text(f"加载进度: {i}%")
            time.sleep(0.02)

        status_text.empty()
        st.success("加载完成！")

    elif style == "skeleton":
        st.info("正在加载内容...")
        render_skeleton(rows=3, height=80)
        time.sleep(2)
        st.rerun()

    elif style == "steps":
        steps = ["初始化", "加载数据", "处理中", "完成"]
        for i, step in enumerate(steps):
            render_progress_with_steps(steps, i)
            time.sleep(0.8)
        st.success("全部完成！")

    st.session_state.loading_state = "success"
    return True


# ============================================================================
# 使用示例
# ============================================================================

st.title("⏳ 加载交互示例")

# 加载方式选择
st.subheader("选择加载方式")

col1, col2 = st.columns(2)

with col1:
    style = st.selectbox(
        "加载样式",
        ["spinner", "progress_bar", "skeleton", "steps"],
        label_visibility="visible"
    )

with col2:
    duration = st.slider("持续时间 (秒)", 1, 5, 2)

# 触发加载
if st.button("开始加载", use_container_width=True, type="primary"):
    simulate_loading(style)

st.divider()

# ============================================================================
# 各样式预览
# ============================================================================

st.subheader("样式预览")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**旋转图标**")
    if st.button("演示", key="spinner_btn", use_container_width=True):
        with st.spinner("加载中..."):
            time.sleep(1)

with col2:
    st.markdown("**进度条**")
    if st.button("演示", key="progress_btn", use_container_width=True):
        bar = st.progress(0)
        for i in range(101):
            bar.progress(i)
            time.sleep(0.01)

with col3:
    st.markdown("**骨架屏**")
    if st.button("演示", key="skeleton_btn", use_container_width=True):
        render_skeleton(rows=2, height=60)

with col4:
    st.markdown("**步骤条**")
    if st.button("演示", key="steps_btn", use_container_width=True):
        steps = ["步骤1", "步骤2", "步骤3"]
        render_progress_with_steps(steps, 0)
        time.sleep(0.5)
        render_progress_with_steps(steps, 1)
        time.sleep(0.5)
        render_progress_with_steps(steps, 2)
'''
        return self._generate_generic_template("加载交互")


# ============================================================================
# 7. DragDropPattern - 拖拽交互模式
# ============================================================================

class DragDropPattern(InteractionPattern):
    """
    拖拽交互模式

    功能: 排序、移动、分组
    状态: 空闲、拖拽中、放置中、完成
    """

    def __init__(self):
        super().__init__(
            pattern_id="drag_drop",
            name="拖拽交互",
            description="处理拖拽操作，包括排序、移动和分组",
            category="interaction"
        )

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户开始拖拽"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_INPUT,
            description="用户拖拽移动中"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户释放放置"
        ))

        # 定义反馈机制
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.VISUAL,
            message="高亮拖拽元素",
            style="highlight"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 拖拽交互模板（使用 streamlit-sortables）
"""
import streamlit as st
from typing import List, Dict, Any


# ============================================================================
# 拖拽状态管理
# ============================================================================

if "drag_items" not in st.session_state:
    st.session_state.drag_items = [
        {"id": "1", "title": "任务 A", "status": "todo"},
        {"id": "2", "title": "任务 B", "status": "in_progress"},
        {"id": "3", "title": "任务 C", "status": "done"},
        {"id": "4", "title": "任务 D", "status": "todo"},
    ]
if "drag_columns" not in st.session_state:
    st.session_state.drag_columns = {
        "todo": "待办",
        "in_progress": "进行中",
        "done": "已完成",
    }


# ============================================================================
# 简化的拖拽实现（使用选择器模拟）
# ============================================================================

def render_kanban_board(items: List[Dict[str, Any]], columns: Dict[str, str]):
    """渲染看板（简化版，使用选择器模拟拖拽）"""

    # 按列分组
    column_items = {col_id: [] for col_id in columns.keys()}
    for item in items:
        status = item["status"]
        if status in column_items:
            column_items[status].append(item)

    # 渲染列
    cols = st.columns(len(columns))

    for col, (col_id, col_name) in zip(cols, columns.items()):
        with col:
            st.markdown(f"### {col_name}")
            st.markdown(f"**{len(column_items[col_id])} 项**")

            for item in column_items[col_id]:
                with st.container():
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.write(item["title"])

                    with col2:
                        # 移动按钮（模拟拖拽）
                        if len(columns) > 1:
                            for target_col in columns.keys():
                                if target_col != item["status"]:
                                    if st.button("→", key=f"move_{item['id']}_{target_col}",
                                               help=f"移到{columns[target_col]}"):
                                        item["status"] = target_col
                                        st.rerun()

                    st.divider()


# ============================================================================
# 排序功能（使用上下按钮）
# ============================================================================

def render_sortable_list(items: List[str], key: str = "default") -> List[str]:
    """渲染可排序列表"""

    if "sort_order" not in st.session_state:
        st.session_state.sort_order = {key: list(range(len(items)))}

    order = st.session_state.sort_order.get(key, list(range(len(items))))

    sorted_items = [items[i] for i in order]

    st.markdown("**拖拽排序列表**")
    st.caption("（使用上下按钮模拟拖拽排序）")

    for i, item in enumerate(sorted_items):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(item)

        with col2:
            if i > 0 and st.button("↑", key=f"up_{key}_{i}"):
                order[i], order[i-1] = order[i-1], order[i]
                st.session_state.sort_order[key] = order
                st.rerun()

        with col3:
            if i < len(sorted_items) - 1 and st.button("↓", key=f"down_{key}_{i}"):
                order[i], order[i+1] = order[i+1], order[i]
                st.session_state.sort_order[key] = order
                st.rerun()

    return sorted_items


# ============================================================================
# 使用示例
# ============================================================================

st.title("🎯 拖拽交互示例")

tab1, tab2 = st.tabs(["看板", "排序列表"])

with tab1:
    st.subheader("看板拖拽")
    st.caption("点击箭头按钮模拟拖拽移动任务到不同列")

    render_kanban_board(
        items=st.session_state.drag_items,
        columns=st.session_state.drag_columns
    )

with tab2:
    st.subheader("列表排序")
    st.caption("使用上下按钮模拟拖拽排序")

    sample_items = ["项目 1", "项目 2", "项目 3", "项目 4", "项目 5"]
    render_sortable_list(sample_items, key="sample")
'''
        return self._generate_generic_template("拖拽交互")


# ============================================================================
# 8. InfiniteScrollPattern - 无限滚动模式
# ============================================================================

class InfiniteScrollPattern(InteractionPattern):
    """
    无限滚动模式

    功能: 加载更多、回到顶部
    状态: 空闲、滚动中、加载中、无更多
    """

    def __init__(self):
        super().__init__(
            pattern_id="infinite_scroll",
            name="无限滚动",
            description="处理滚动加载更多内容和返回顶部功能",
            category="navigation"
        )

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.SCROLL,
            description="滚动到接近底部"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击加载更多"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击回到顶部"
        ))

        # 定义反馈机制
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.INLINE,
            message="加载中...",
            style="spinner"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 无限滚动模板
"""
import streamlit as st
from typing import List, Any
import time


# ============================================================================
# 无限滚动状态管理
# ============================================================================

if "infinite_items" not in st.session_state:
    st.session_state.infinite_items = []
if "infinite_page" not in st.session_state:
    st.session_state.infinite_page = 0
if "infinite_loading" not in st.session_state:
    st.session_state.infinite_loading = False
if "infinite_has_more" not in st.session_state:
    st.session_state.infinite_has_more = True


# ============================================================================
# 数据加载函数
# ============================================================================

def load_more_items(page: int, page_size: int = 10) -> List[str]:
    """
    加载更多数据

    Args:
        page: 页码
        page_size: 每页数量

    Returns:
        新数据列表
    """
    # 模拟 API 调用
    time.sleep(0.5)

    start_idx = page * page_size
    end_idx = start_idx + page_size

    # 模拟最多 50 条数据
    if start_idx >= 50:
        return []

    actual_end = min(end_idx, 50)
    return [f"项目 {i+1}" for i in range(start_idx, actual_end)]


# ============================================================================
# 渲染组件
# ============================================================================

def render_infinite_scroll(items: List[str], page_size: int = 10):
    """渲染无限滚动列表"""

    # 显示当前加载的内容
    for i, item in enumerate(items):
        st.write(f"{i+1}. {item}")

    st.divider()

    # 加载状态
    if st.session_state.infinite_loading:
        st.info("⏳ 加载中...")
        return

    # 没有更多内容
    if not st.session_state.infinite_has_more:
        st.success("✅ 已加载全部内容")
        return

    # 加载更多按钮
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("📥 加载更多", use_container_width=True, key="load_more"):
            st.session_state.infinite_loading = True
            st.rerun()

    # 执行加载
    if st.session_state.infinite_loading:
        new_items = load_more_items(st.session_state.infinite_page, page_size)

        if new_items:
            st.session_state.infinite_items.extend(new_items)
            st.session_state.infinite_page += 1
        else:
            st.session_state.infinite_has_more = False

        st.session_state.infinite_loading = False
        st.rerun()


def render_back_to_top():
    """渲染回到顶部按钮"""
    if st.session_state.infinite_items and len(st.session_state.infinite_items) > 10:
        if st.button("⬆️ 回到顶部", use_container_width=True):
            st.session_state.infinite_items = []
            st.session_state.infinite_page = 0
            st.session_state.infinite_has_more = True
            st.rerun()


# ============================================================================
# 使用示例
# ============================================================================

st.title("📜 无限滚动示例")

# 控制面板
with st.sidebar:
    st.subheader("设置")
    page_size = st.slider("每页加载数量", 5, 20, 10)

    if st.button("重置列表"):
        st.session_state.infinite_items = []
        st.session_state.infinite_page = 0
        st.session_state.infinite_has_more = True
        st.rerun()

    st.divider()
    st.metric("已加载", len(st.session_state.infinite_items))
    st.metric("当前页", st.session_state.infinite_page + 1)

# 初始加载提示
if not st.session_state.infinite_items:
    st.info("👇 点击下方按钮开始加载内容")
    if st.button("开始加载", use_container_width=True, type="primary"):
        st.session_state.infinite_loading = True
        st.rerun()

# 渲染列表
if st.session_state.infinite_items or st.session_state.infinite_loading:
    render_infinite_scroll(st.session_state.infinite_items, page_size)

    st.divider()
    render_back_to_top()
'''
        return self._generate_generic_template("无限滚动")


# ============================================================================
# 9. TabSwitchPattern - 标签切换模式
# ============================================================================

class TabSwitchPattern(InteractionPattern):
    """
    标签切换模式

    功能: 懒加载、保持状态
    状态: 空闲、切换中、已加载
    """

    def __init__(self):
        super().__init__(
            pattern_id="tab_switch",
            name="标签切换",
            description="处理标签页切换和内容状态保持",
            category="navigation"
        )

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击标签"
        ))

        # 定义反馈机制
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.VISUAL,
            message="高亮当前标签",
            style="active_tab"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 标签切换模板
"""
import streamlit as st
from typing import Dict, Any, List


# ============================================================================
# 标签状态管理
# ============================================================================

if "tab_data" not in st.session_state:
    st.session_state.tab_data = {
        "tab1": {"value": "", "checked": False},
        "tab2": {"value": 50, "options": ["A", "B", "C"]},
        "tab3": {"items": ["项目 1", "项目 2"]},
        "tab4": {"text": ""},
    }


# ============================================================================
# 懒加载内容
# ============================================================================

def lazy_load_tab_content(tab_id: str):
    """懒加载标签内容（只在首次访问时加载）"""

    if f"{tab_id}_loaded" not in st.session_state:
        st.session_state[f"{tab_id}_loaded"] = True
        # 这里可以执行昂贵的数据加载操作
        # 例如: API 调用、数据库查询等

    return st.session_state.tab_data.get(tab_id, {})


# ============================================================================
# 标签内容渲染
# ============================================================================

def render_tab1():
    """标签 1: 表单输入"""
    st.markdown("### 📝 表单输入")

    data = lazy_load_tab_content("tab1")

    text = st.text_area(
        "输入内容",
        value=data["value"],
        key="tab1_text",
        help="在标签间切换后内容会保持"
    )

    if st.button("保存", key="tab1_save"):
        st.session_state.tab_data["tab1"]["value"] = text
        st.success("已保存")


def render_tab2():
    """标签 2: 控制组件"""
    st.markdown("### 🎛️ 控制组件")

    data = lazy_load_tab_content("tab2")

    col1, col2 = st.columns(2)

    with col1:
        value = st.slider("数值", 0, 100, data["value"], key="tab2_slider")

    with col2:
        option = st.selectbox("选项", data["options"], key="tab2_select")

    if st.checkbox("记住选择", key="tab2_remember"):
        st.session_state.tab_data["tab2"]["value"] = value
        st.info("状态已保存")


def render_tab3():
    """标签 3: 列表管理"""
    st.markdown("### 📋 列表管理")

    data = lazy_load_tab_content("tab3")

    # 显示列表
    for i, item in enumerate(data["items"]):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(item)

        with col2:
            if st.button("删除", key=f"tab3_del_{i}"):
                st.session_state.tab_data["tab3"]["items"].pop(i)
                st.rerun()

    # 添加新项
    new_item = st.text_input("新项目", key="tab3_new_item")
    if st.button("添加", key="tab3_add"):
        if new_item:
            st.session_state.tab_data["tab3"]["items"].append(new_item)
            st.rerun()


def render_tab4():
    """标签 4: 懒加载示例"""
    st.markdown("### ⏱️ 懒加载示例")

    if "tab4_loaded" not in st.session_state:
        with st.spinner("首次加载中..."):
            import time
            time.sleep(1)  # 模拟加载延迟
        st.success("首次加载完成")

    st.info("再次切换到此标签不会显示加载动画")

    text = st.text_input("输入", value=st.session_state.tab_data["tab4"]["text"], key="tab4_input")
    st.session_state.tab_data["tab4"]["text"] = text


# ============================================================================
# 使用示例
# ============================================================================

st.title("🏷️ 标签切换示例")

st.caption("在标签间切换，内容状态会保持")

# ============================================================================
# Streamlit 原生标签（自动状态保持）
# ============================================================================

st.subheader("Streamlit 原生标签")

tab1, tab2, tab3, tab4 = st.tabs(["表单", "控制", "列表", "懒加载"])

with tab1:
    render_tab1()

with tab2:
    render_tab2()

with tab3:
    render_tab3()

with tab4:
    render_tab4()

st.divider()

# ============================================================================
# 自定义标签（使用选择器）
# ============================================================================

st.subheader("自定义标签实现")

if "custom_tab" not in st.session_state:
    st.session_state.custom_tab = "A"

custom_tabs = ["标签 A", "标签 B", "标签 C"]

# 标签按钮
cols = st.columns(len(custom_tabs))
for col, tab in zip(cols, custom_tabs):
    tab_key = tab.split(" ")[1]
    is_active = st.session_state.custom_tab == tab_key

    with col:
        if st.button(
            tab,
            use_container_width=True,
            key=f"custom_tab_{tab_key}",
            type="primary" if is_active else "secondary"
        ):
            st.session_state.custom_tab = tab_key
            st.rerun()

# 内容区域
st.divider()

if st.session_state.custom_tab == "A":
    st.markdown("### 标签 A 内容")
    st.write("这是标签 A 的内容")

elif st.session_state.custom_tab == "B":
    st.markdown("### 标签 B 内容")
    st.write("这是标签 B 的内容")

elif st.session_state.custom_tab == "C":
    st.markdown("### 标签 C 内容")
    st.write("这是标签 C 的内容")

st.divider()

# ============================================================================
# 状态检查
# ============================================================================

st.subheader("状态检查")
st.write("当前标签状态：")
st.json(st.session_state.tab_data)
'''
        return self._generate_generic_template("标签切换")


# ============================================================================
# 10. CollapsiblePattern - 折叠展开模式
# ============================================================================

class CollapsiblePattern(InteractionPattern):
    """
    折叠展开模式

    功能: 手风琴、树形
    状态: 折叠、展开中、已展开
    """

    def __init__(self):
        super().__init__(
            pattern_id="collapsible",
            name="折叠展开",
            description="处理可折叠内容的展开和收起，包括手风琴和树形结构",
            category="navigation"
        )

        # 定义触发条件
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击展开/收起"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击全部展开"
        ))
        self.add_trigger(TriggerCondition(
            type=TriggerType.USER_CLICK,
            description="用户点击全部收起"
        ))

        # 定义反馈机制
        self.add_feedback(FeedbackMechanism(
            type=FeedbackType.VISUAL,
            message="展开/收起动画",
            style="slide"
        ))

    def get_code_template(self, framework: str = "streamlit") -> str:
        """获取代码模板"""
        if framework == "streamlit":
            return '''"""
Streamlit 折叠展开模板
"""
import streamlit as st
from typing import Dict, List, Any


# ============================================================================
# 折叠状态管理
# ============================================================================

if "accordion_state" not in st.session_state:
    st.session_state.accordion_state = {
        "section1": False,
        "section2": False,
        "section3": False,
    }
if "tree_state" not in st.session_state:
    st.session_state.tree_state = {
        "root": True,
        "branch1": False,
        "branch2": False,
        "branch1_1": False,
        "branch1_2": False,
    }


# ============================================================================
# 手风琴组件
# ============================================================================

def render_accordion(
    sections: Dict[str, Dict[str, Any]],
    state_key: str = "accordion"
):
    """
    渲染手风琴组件

    Args:
        sections: {section_id: {"title": str, "content": callable}}
        state_key: 状态键名
    """
    state_key_full = f"{state_key}_state"

    if state_key_full not in st.session_state:
        st.session_state[state_key_full] = {
            section_id: False for section_id in sections.keys()
        }

    current_state = st.session_state[state_key_full]

    for section_id, section in sections.items():
        is_open = current_state.get(section_id, False)

        # 展开/收起按钮
        icon = "🔽" if is_open else "▶️"

        if st.button(
            f"{icon} {section['title']}",
            key=f"accordion_{state_key}_{section_id}",
            use_container_width=True,
            help="点击展开/收起"
        ):
            # 手风琴模式：关闭其他
            for sid in current_state.keys():
                current_state[sid] = False
            current_state[section_id] = is_open  # 切换当前
            st.rerun()

        # 内容
        if is_open and callable(section.get("content")):
            st.markdown("---")
            section["content"]()
            st.markdown("---")


def render_all_accordion(
    sections: Dict[str, Dict[str, Any]],
    state_key: str = "all_accordion"
):
    """
    渲染独立折叠组件（可同时展开多个）

    Args:
        sections: {section_id: {"title": str, "content": callable}}
        state_key: 状态键名
    """
    state_key_full = f"{state_key}_state"

    if state_key_full not in st.session_state:
        st.session_state[state_key_full] = {
            section_id: False for section_id in sections.keys()
        }

    current_state = st.session_state[state_key_full]

    for section_id, section in sections.items():
        is_open = current_state.get(section_id, False)

        with st.expander(section["title"], expanded=is_open):
            if callable(section.get("content")):
                section["content"]()
            # 同步状态
            current_state[section_id] = True


# ============================================================================
# 树形组件
# ============================================================================

def render_tree(nodes: Dict[str, Dict[str, Any]], parent_id: str = ""):
    """
    渲染树形结构

    Args:
        nodes: {node_id: {"label": str, "children": dict, "content": callable}}
        parent_id: 父节点ID
    """
    for node_id, node in nodes.items():
        full_id = f"{parent_id}_{node_id}" if parent_id else node_id
        state_key = f"tree_{full_id}"

        has_children = bool(node.get("children"))
        is_leaf = not has_children

        # 检查展开状态
        if state_key not in st.session_state:
            st.session_state[state_key] = False

        is_open = st.session_state[state_key]

        # 渲染节点
        indent = "　　" * (parent_id.count("_") if parent_id else 0)

        if is_leaf:
            # 叶子节点
            st.markdown(f"{indent}📄 {node['label']}")
        else:
            # 父节点
            icon = "🔽" if is_open else "▶️"

            if st.button(
                f"{indent}{icon} 📁 {node['label']}",
                key=state_key,
                help="点击展开/收起"
            ):
                st.session_state[state_key] = not is_open
                st.rerun()

            # 递归渲染子节点
            if is_open and has_children:
                render_tree(node["children"], full_id)

                # 节点内容
                if callable(node.get("content")):
                    with st.container():
                        node["content"]()


# ============================================================================
# 使用示例
# ============================================================================

st.title("📁 折叠展开示例")

tab1, tab2, tab3 = st.tabs(["手风琴", "独立折叠", "树形结构"])

# ============================================================================
# 手风琴（同时只能展开一个）
# ============================================================================

with tab1:
    st.subheader("手风琴效果")
    st.caption("同时只能展开一个章节")

    # 手风琴数据
    accordion_sections = {
        "section1": {
            "title": "第 1 章：简介",
            "content": lambda: st.write("这是第一章的内容，介绍基本概念。")
        },
        "section2": {
            "title": "第 2 章：核心功能",
            "content": lambda: (
                st.write("这是第二章的内容。"),
                st.success("✨ 核心功能亮点"),
                st.info("📚 相关文档")
            )
        },
        "section3": {
            "title": "第 3 章：进阶用法",
            "content": lambda: st.write("这是第三章的高级内容。")
        },
    }

    render_accordion(accordion_sections, state_key="example_accordion")

    st.divider()

    # 全部展开/收起
    col1, col2 = st.columns(2)
    with col1:
        if st.button("展开第一个", use_container_width=True):
            st.session_state.example_accordion_state = {
                "section1": True,
                "section2": False,
                "section3": False,
            }
            st.rerun()

    with col2:
        if st.button("全部收起", use_container_width=True):
            st.session_state.example_accordion_state = {
                "section1": False,
                "section2": False,
                "section3": False,
            }
            st.rerun()


# ============================================================================
# 独立折叠（可同时展开多个）
# ============================================================================

with tab2:
    st.subheader("独立折叠区域")
    st.caption("可以同时展开多个区域")

    all_sections = {
        "faq1": {
            "title": "❓ 什么是 Streamlit？",
            "content": lambda: st.info("Streamlit 是一个用于构建数据应用的 Python 框架。")
        },
        "faq2": {
            "title": "❓ 如何安装？",
            "content": lambda: st.code("pip install streamlit")
        },
        "faq3": {
            "title": "❓ 支持哪些组件？",
            "content": lambda: st.markdown("- 文本输入\\n- 按钮\\n- 图表\\n- 数据框...")
        },
    }

    render_all_accordion(all_sections, state_key="faq")


# ============================================================================
# 树形结构
# ============================================================================

with tab3:
    st.subheader("树形结构")

    # 树形数据
    tree_data = {
        "root": {
            "label": "项目根目录",
            "children": {
                "src": {
                    "label": "src (源代码)",
                    "children": {
                        "components": {
                            "label": "components (组件)",
                            "children": {},
                            "content": lambda: st.write("组件文件列表")
                        },
                        "utils": {
                            "label": "utils (工具)",
                            "children": {},
                            "content": lambda: st.write("工具函数")
                        },
                    }
                },
                "docs": {
                    "label": "docs (文档)",
                    "children": {
                        "readme": {
                            "label": "README.md",
                            "children": {}
                        },
                        "guide": {
                            "label": "guide.md",
                            "children": {}
                        },
                    }
                },
                "config": {
                    "label": "config (配置)",
                    "children": {},
                    "content": lambda: st.json({"app": "settings"})
                },
            }
        }
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 方式 1: 自定义树")
        render_tree(tree_data)

    with col2:
        st.markdown("#### 方式 2: 使用 delta JSON")
        st.json({
            "项目": {
                "📁 src": {
                    "📁 components": {},
                    "📁 utils": {},
                },
                "📁 docs": {
                    "📄 README.md": {},
                    "📄 guide.md": {},
                },
                "📄 config.json": {},
            }
        }, expanded=3)
'''
        return self._generate_generic_template("折叠展开")


# ============================================================================
# 辅助方法
# ============================================================================

    def _generate_generic_template(self, pattern_name: str) -> str:
        """生成通用模板"""
        return f"""
// {pattern_name} 交互模式模板
// 此框架的代码模板待实现

// 触发条件示例:
{chr(10).join(f'// - {t.description}' for t in self._triggers)}

// 状态转换:
{chr(10).join(f'// - {t.from_state.value} -> {t.to_state.value}' for t in self._transitions)}

// 反馈机制:
{chr(10).join(f'// - {f.type.value}: {f.message}' for f in self._feedbacks)}
"""


# ============================================================================
# 交互模式注册表
# ============================================================================

INTERACTION_PATTERNS: Dict[str, InteractionPattern] = {
    "form": FormPattern(),
    "search": SearchPattern(),
    "pagination": PaginationPattern(),
    "modal": ModalPattern(),
    "toast": ToastPattern(),
    "loading": LoadingPattern(),
    "drag_drop": DragDropPattern(),
    "infinite_scroll": InfiniteScrollPattern(),
    "tab_switch": TabSwitchPattern(),
    "collapsible": CollapsiblePattern(),
}


def get_pattern(pattern_id: str) -> Optional[InteractionPattern]:
    """获取交互模式"""
    return INTERACTION_PATTERNS.get(pattern_id)


def list_patterns() -> List[InteractionPattern]:
    """列出所有交互模式"""
    return list(INTERACTION_PATTERNS.values())


def list_patterns_by_category(category: str) -> List[InteractionPattern]:
    """按类别列出交互模式"""
    return [p for p in INTERACTION_PATTERNS.values() if p.category == category]


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "TriggerType",
    "StateType",
    "FeedbackType",
    "ValidationRule",
    # 数据类
    "TriggerCondition",
    "StateTransition",
    "FeedbackMechanism",
    # 基类
    "InteractionPattern",
    # 10种交互模式
    "FormPattern",
    "SearchPattern",
    "PaginationPattern",
    "ModalPattern",
    "ToastPattern",
    "LoadingPattern",
    "DragDropPattern",
    "InfiniteScrollPattern",
    "TabSwitchPattern",
    "CollapsiblePattern",
    # 注册表和函数
    "INTERACTION_PATTERNS",
    "get_pattern",
    "list_patterns",
    "list_patterns_by_category",
]
