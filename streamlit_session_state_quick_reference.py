"""
================================================================================
STREAMLIT SESSION STATE 快速参考卡
================================================================================

这份文件提供了 Streamlit session_state 的快速参考代码片段，
可以直接复制到你的项目中使用。

参考来源：
- https://docs.streamlit.io/develop/concepts/architecture/session-state
- https://medium.com/@jashuamrita360/best-practices-for-streamlit-development-structuring-code-and-managing-session-state-0bdcfb91a745
================================================================================
"""

import streamlit as st
from typing import Any, Callable, Optional
from functools import wraps
import time


# =============================================================================
# 1. 初始化模式（一次性函数）
# =============================================================================

def init_state(key: str, default: Any = None) -> Any:
    """最简洁的初始化模式"""
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def init_state_factory(key: str, factory: Callable) -> Any:
    """工厂函数初始化（用于复杂对象）"""
    if key not in st.session_state:
        st.session_state[key] = factory()
    return st.session_state[key]


# 使用示例
# init_state('counter', 0)
# init_state_factory('config', lambda: {'theme': 'light', 'lang': 'zh'})


# =============================================================================
# 2. 装饰器模式（高级）
# =============================================================================

def session_state_var(key: str, default: Any = None):
    """装饰器：自动初始化 session_state 变量"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key not in st.session_state:
                st.session_state[key] = default if callable(default) is not False else default
                if callable(default) and default is not None:
                    st.session_state[key] = default()
            return func(st.session_state[key], *args, **kwargs)
        return wrapper
    return decorator


# 使用示例
# @session_state_var('app_config', {'theme': 'dark'})
# def get_config(config):
#     return config


# =============================================================================
# 3. 回调辅助函数
# =============================================================================

def create_callback(callback: Callable, *args, **kwargs):
    """创建带参数的回调函数"""
    def wrapper():
        return callback(*args, **kwargs)
    return wrapper


def update_state_value(key: str, value: Any):
    """简单的状态更新回调"""
    st.session_state[key] = value


def increment_state(key: str, amount: int = 1):
    """增加状态值"""
    if key not in st.session_state:
        st.session_state[key] = 0
    st.session_state[key] += amount


# 使用示例
# st.button("增加", on_click=create_callback(increment_state, 'counter', 1))


# =============================================================================
# 4. 状态重置工具
# =============================================================================

def reset_state(*keys: str):
    """重置指定的状态键"""
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]


def reset_state_prefix(prefix: str):
    """重置所有以指定前缀开头的键"""
    keys = [k for k in st.session_state.keys() if k.startswith(prefix)]
    for key in keys:
        del st.session_state[key]
    return len(keys)


def reset_state_except(*keys: str):
    """重置除指定键外的所有状态"""
    all_keys = list(st.session_state.keys())
    for key in all_keys:
        if key not in keys:
            del st.session_state[key]


# =============================================================================
# 5. 状态快照
# =============================================================================

def save_snapshot(name: str = 'snapshot'):
    """保存当前状态快照"""
    if 'snapshots' not in st.session_state:
        st.session_state.snapshots = {}
    st.session_state.snapshots[name] = dict(st.session_state)
    st.session_state.snapshots[f'{name}_time'] = time.time()


def restore_snapshot(name: str = 'snapshot'):
    """恢复状态快照"""
    if 'snapshots' in st.session_state and name in st.session_state.snapshots:
        st.session_state.clear()
        for key, value in st.session_state.snapshots[name].items():
            st.session_state[key] = value


def list_snapshots():
    """列出所有快照"""
    if 'snapshots' not in st.session_state:
        return []
    return [k for k in st.session_state.snapshots.keys() if not k.endswith('_time')]


# =============================================================================
# 6. 多页面状态管理
# =============================================================================

class AppState:
    """应用状态管理器（单例模式）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        # 初始化应用级状态
        init_state('app_started_at', time.time())
        init_state('page_visits', {})

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """获取状态值"""
        return st.session_state.get(key, default)

    @staticmethod
    def set(key: str, value: Any):
        """设置状态值"""
        st.session_state[key] = value

    @staticmethod
    def track_page_visit(page_name: str):
        """跟踪页面访问"""
        if 'page_visits' not in st.session_state:
            st.session_state.page_visits = {}
        visits = st.session_state.page_visits
        visits[page_name] = visits.get(page_name, 0) + 1
        st.session_state.page_visits = visits


# 使用示例
# app_state = AppState()
# app_state.track_page_visit('home')


# =============================================================================
# 7. 表单状态处理
# =============================================================================

class FormState:
    """表单状态管理"""

    def __init__(self, form_key: str):
        self.form_key = form_key
        self.data_key = f"{form_key}_data"

    def init(self, default_data: dict = None):
        """初始化表单数据"""
        return init_state(self.data_key, default_data or {})

    def get(self) -> dict:
        """获取表单数据"""
        return st.session_state.get(self.data_key, {})

    def update(self, key: str, value: Any):
        """更新单个字段"""
        if self.data_key not in st.session_state:
            st.session_state[self.data_key] = {}
        st.session_state[self.data_key][key] = value

    def set(self, data: dict):
        """设置整个表单数据"""
        st.session_state[self.data_key] = data

    def clear(self):
        """清空表单数据"""
        if self.data_key in st.session_state:
            del st.session_state[self.data_key]

    def submit_callback(self):
        """表单提交回调"""
        # 可以在这里添加验证逻辑
        pass


# 使用示例
# form = FormState('login_form')
# form.init({'username': '', 'password': ''})
# username = st.text_input('用户名', value=form.get().get('username', ''),
#                          key=f'{form.form_key}_username')
# form.update('username', username)


# =============================================================================
# 8. 缓存辅助
# =============================================================================

@st.cache_data(ttl=3600)
def cached_data_loader(key: str, loader: Callable):
    """带缓存的数据加载器"""
    return loader()


def get_or_load(key: str, loader: Callable, use_cache: bool = True):
    """获取数据或加载（可选缓存）"""
    session_key = f"loaded_{key}"
    if session_key not in st.session_state:
        if use_cache:
            st.session_state[session_key] = cached_data_loader(key, loader)
        else:
            st.session_state[session_key] = loader()
    return st.session_state[session_key]


# =============================================================================
# 9. 向后兼容（处理旧的状态键）
# =============================================================================

def migrate_state(old_key: str, new_key: str, transform: Callable = None):
    """迁移旧的状态键到新键"""
    if old_key in st.session_state and new_key not in st.session_state:
        value = st.session_state[old_key]
        if transform:
            value = transform(value)
        st.session_state[new_key] = value
        del st.session_state[old_key]


# =============================================================================
# 10. 调试工具
# =============================================================================

def print_state(filter_prefix: str = None):
    """打印所有状态（调试用）"""
    states = dict(st.session_state)
    if filter_prefix:
        states = {k: v for k, v in states.items() if k.startswith(filter_prefix)}
    for key, value in states.items():
        print(f"{key}: {value}")


def state_summary():
    """获取状态摘要"""
    return {
        'count': len(st.session_state),
        'keys': list(st.session_state.keys()),
        'size_bytes': sum(len(str(v)) for v in st.session_state.values())
    }


# =============================================================================
# 11. 类型安全的状态访问
# =============================================================================

class TypedState:
    """类型安全的状态访问"""

    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        """获取整数类型状态"""
        value = st.session_state.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def get_str(key: str, default: str = "") -> str:
        """获取字符串类型状态"""
        value = st.session_state.get(key, default)
        return str(value) if value is not None else default

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """获取布尔类型状态"""
        value = st.session_state.get(key, default)
        return bool(value)

    @staticmethod
    def get_list(key: str, default: list = None) -> list:
        """获取列表类型状态"""
        if default is None:
            default = []
        value = st.session_state.get(key, default)
        return list(value) if isinstance(value, (list, tuple)) else default

    @staticmethod
    def get_dict(key: str, default: dict = None) -> dict:
        """获取字典类型状态"""
        if default is None:
            default = {}
        value = st.session_state.get(key, default)
        return dict(value) if isinstance(value, dict) else default


# 使用示例
# counter = TypedState.get_int('counter')
# username = TypedState.get_str('username', 'Guest')


# =============================================================================
# 12. 事件跟踪
# =============================================================================

class EventTracker:
    """简单的事件跟踪器"""

    def __init__(self, max_events: int = 100):
        self.events_key = '_event_tracker_events'
        self.max_events = max_events
        init_state(self.events_key, [])

    def track(self, event_type: str, data: dict = None):
        """记录事件"""
        events = st.session_state[self.events_key]
        events.append({
            'type': event_type,
            'data': data or {},
            'timestamp': time.time(),
            'time': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        # 限制事件数量
        if len(events) > self.max_events:
            st.session_state[self.events_key] = events[-self.max_events:]

    def get_events(self, event_type: str = None) -> list:
        """获取事件"""
        events = st.session_state.get(self.events_key, [])
        if event_type:
            return [e for e in events if e['type'] == event_type]
        return events

    def clear(self):
        """清除所有事件"""
        st.session_state[self.events_key] = []


# 使用示例
# tracker = EventTracker()
# tracker.track('button_click', {'button': 'submit'})
# tracker.track('page_view', {'page': 'home'})


# =============================================================================
# 快速使用示例
# =============================================================================

def demo_basic_usage():
    """基础使用示例"""
    st.title("Session State 快速参考示例")

    # 1. 简单初始化
    init_state('counter', 0)

    # 2. 按钮 + 回调
    col1, col2 = st.columns(2)
    with col1:
        st.button("增加", on_click=create_callback(increment_state, 'counter'))
    with col2:
        st.button("减少", on_click=create_callback(increment_state, 'counter', -1))

    st.metric("计数器", st.session_state.counter)

    # 3. 类型安全访问
    username = TypedState.get_str('username', '访客')
    st.write(f"欢迎, {username}!")

    # 4. 事件跟踪
    tracker = EventTracker()
    tracker.track('demo_page_visit')


if __name__ == "__main__":
    demo_basic_usage()
