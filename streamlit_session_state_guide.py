"""
================================================================================
STREAMLIT 会话状态管理高级模式完整指南
================================================================================
涵盖内容：
1. session_state最佳实践
2. 状态初始化模式
3. 跨页面状态共享
4. 状态重置和清理
5. 复杂对象存储
6. 性能考虑

参考来源：
- Streamlit官方文档: https://docs.streamlit.io/develop/concepts/architecture/session-state
- Streamlit社区最佳实践: https://medium.com/@jashuamrita360/best-practices-for-streamlit-development-structuring-code-and-managing-session-state-0bdcfb91a745
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import json
import pickle


# =============================================================================
# 1. SESSION STATE 最佳实践
# =============================================================================

def best_practices_demo():
    """
    Streamlit Session State 最佳实践演示
    """
    st.title("1️⃣ Session State 最佳实践")

    st.markdown("""
    ### 核心原则：
    1. **使用唯一的键名** - 避免冲突，特别是在多个页面间共享状态时
    2. **初始化前检查** - 始终检查键是否存在以避免覆盖
    3. **使用有意义的前缀** - 便于组织和管理状态变量
    4. **避免存储过大的对象** - 可能导致性能问题
    5. **考虑序列化兼容性** - 在某些环境中需要可序列化的对象
    """)

    # 带前缀的状态初始化
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True
        st.session_state.app_version = "1.0.0"
        st.session_state.user_preferences = {}

    st.info(f"✅ 应用已初始化 - 版本: {st.session_state.app_version}")


# =============================================================================
# 2. 状态初始化模式
# =============================================================================

class SessionStateInitializer:
    """
    状态初始化模式 - 提供多种初始化方法
    """

    @staticmethod
    def pattern_if_not_in():
        """模式1: 使用 if-not-in 检查（最常用）"""
        if 'counter' not in st.session_state:
            st.session_state.counter = 0
        return st.session_state.counter

    @staticmethod
    def pattern_setdefault():
        """模式2: 使用 setdefault 方法（更简洁）"""
        st.session_state.setdefault('messages', [])
        st.session_state.setdefault('current_page', 'home')
        return st.session_state.messages

    @staticmethod
    def pattern_getattr():
        """模式3: 使用 getattr 带默认值（类属性风格）"""
        return getattr(st.session_state, 'user_id', None)

    @staticmethod
    def pattern_getattr_with_default():
        """模式4: getattr 赋值模式"""
        if not hasattr(st.session_state, 'config'):
            st.session_state.config = {
                'theme': 'light',
                'language': 'zh'
            }
        return st.session_state.config

    @staticmethod
    def pattern_factory():
        """模式5: 工厂函数模式 - 复杂对象初始化"""
        def create_user_session():
            return {
                'login_time': datetime.now(),
                'activity_log': [],
                'preferences': {}
            }

        st.session_state.setdefault('user_session', create_user_session())
        return st.session_state.user_session

    @staticmethod
    def pattern_singleton():
        """模式6: 单例模式 - 确保只初始化一次"""
        if 'database_connection' not in st.session_state:
            st.session_state.database_connection = "Simulated DB Connection"
        return st.session_state.database_connection


@dataclass
class TypedSessionState:
    """
    类型化会话状态 - 使用 dataclass 提供类型提示
    """
    counter: int = 0
    messages: List[str] = field(default_factory=list)
    user_data: Dict[str, Any] = field(default_factory=dict)
    last_updated: Optional[datetime] = None

    def to_session_state(self):
        """将类型化状态同步到 st.session_state"""
        for key, value in self.__dict__.items():
            st.session_state[key] = value

    @classmethod
    def from_session_state(cls):
        """从 st.session_state 创建类型化对象"""
        return cls(
            counter=getattr(st.session_state, 'counter', 0),
            messages=getattr(st.session_state, 'messages', []),
            user_data=getattr(st.session_state, 'user_data', {}),
            last_updated=getattr(st.session_state, 'last_updated', None)
        )


def initialization_patterns_demo():
    """初始化模式演示"""
    st.title("2️⃣ 状态初始化模式")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "if-not-in", "setdefault", "getattr", "getattr赋值", "工厂函数", "单例模式", "类型化状态"
    ])

    with tab1:
        st.subheader("模式1: if-not-in 检查")
        st.code("""
if 'counter' not in st.session_state:
    st.session_state.counter = 0
        """, language="python")
        count = SessionStateInitializer.pattern_if_not_in()
        st.metric("当前计数", count)
        if st.button("增加计数 (if-not-in)", key="btn1"):
            st.session_state.counter += 1
            st.rerun()

    with tab2:
        st.subheader("模式2: setdefault 方法")
        st.code("""
st.session_state.setdefault('messages', [])
st.session_state.setdefault('current_page', 'home')
        """, language="python")
        SessionStateInitializer.pattern_setdefault()
        st.write("消息列表:", st.session_state.messages)
        if st.button("添加消息 (setdefault)", key="btn2"):
            st.session_state.messages.append(f"消息 {len(st.session_state.messages) + 1}")
            st.rerun()

    with tab3:
        st.subheader("模式3: getattr 读取")
        st.code("""
user_id = getattr(st.session_state, 'user_id', None)
        """, language="python")
        user_id = SessionStateInitializer.pattern_getattr()
        st.write(f"用户ID: {user_id or '未设置'}")
        if st.button("设置用户ID", key="btn3"):
            st.session_state.user_id = "user_12345"
            st.rerun()

    with tab4:
        st.subheader("模式4: getattr 赋值检查")
        st.code("""
if not hasattr(st.session_state, 'config'):
    st.session_state.config = {'theme': 'light', 'language': 'zh'}
        """, language="python")
        config = SessionStateInitializer.pattern_getattr_with_default()
        st.json(config)

    with tab5:
        st.subheader("模式5: 工厂函数")
        st.code("""
def create_user_session():
    return {
        'login_time': datetime.now(),
        'activity_log': [],
        'preferences': {}
    }

st.session_state.setdefault('user_session', create_user_session())
        """, language="python")
        session = SessionStateInitializer.pattern_factory()
        st.json(session)

    with tab6:
        st.subheader("模式6: 单例模式")
        st.code("""
if 'database_connection' not in st.session_state:
    st.session_state.database_connection = connect_to_database()
        """, language="python")
        conn = SessionStateInitializer.pattern_singleton()
        st.success(f"数据库连接: {conn}")

    with tab7:
        st.subheader("模式7: 类型化状态")
        st.code("""
@dataclass
class TypedSessionState:
    counter: int = 0
    messages: List[str] = field(default_factory=list)
    # ... 更多字段

# 使用
typed_state = TypedSessionState.from_session_state()
        """, language="python")
        typed = TypedSessionState.from_session_state()
        st.json({
            "counter": typed.counter,
            "messages_count": len(typed.messages),
            "user_data": typed.user_data,
            "last_updated": str(typed.last_updated) if typed.last_updated else None
        })


# =============================================================================
# 3. 跨页面状态共享
# =============================================================================

class CrossPageStateManager:
    """
    跨页面状态共享管理器
    使用方法：
    1. 在 pages/ 目录下创建多个页面文件
    2. 在每个页面使用相同的状态键名
    3. session_state 会自动在所有页面间共享
    """

    SHARED_KEYS = [
        'user_authenticated',
        'username',
        'preferences',
        'cart_items',
        'navigation_history'
    ]

    @classmethod
    def init_shared_state(cls):
        """初始化跨页面共享的状态"""
        for key in cls.SHARED_KEYS:
            if key not in st.session_state:
                if key == 'user_authenticated':
                    st.session_state[key] = False
                elif key == 'username':
                    st.session_state[key] = None
                elif key == 'preferences':
                    st.session_state[key] = {'theme': 'light', 'language': 'zh'}
                elif key == 'cart_items':
                    st.session_state[key] = []
                elif key == 'navigation_history':
                    st.session_state[key] = []

    @classmethod
    def add_navigation_history(cls, page_name: str):
        """添加导航历史"""
        if 'navigation_history' not in st.session_state:
            st.session_state.navigation_history = []
        st.session_state.navigation_history.append({
            'page': page_name,
            'timestamp': datetime.now().isoformat()
        })

    @classmethod
    def get_shared_state(cls) -> Dict[str, Any]:
        """获取所有共享状态"""
        return {key: st.session_state.get(key) for key in cls.SHARED_KEYS}


def cross_page_sharing_demo():
    """跨页面状态共享演示"""
    st.title("3️⃣ 跨页面状态共享")

    st.markdown("""
    ### 跨页面共享原理：
    - st.session_state 在多页面应用中全局共享
    - 在任何页面设置的状态变量可以在其他页面访问
    - 适用于用户认证、偏好设置、购物车等场景
    """)

    # 初始化共享状态
    CrossPageStateManager.init_shared_state()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("当前共享状态")
        shared_state = CrossPageStateManager.get_shared_state()
        st.json(shared_state)

    with col2:
        st.subheader("状态操作")

        # 模拟用户登录
        if not st.session_state.user_authenticated:
            username = st.text_input("用户名")
            if st.button("登录"):
                st.session_state.user_authenticated = True
                st.session_state.username = username
                CrossPageStateManager.add_navigation_history("login")
                st.success(f"欢迎, {username}!")
                st.rerun()
        else:
            st.success(f"已登录: {st.session_state.username}")

            # 更改偏好设置
            theme = st.selectbox(
                "主题",
                ['light', 'dark'],
                index=['light', 'dark'].index(st.session_state.preferences['theme'])
            )
            if theme != st.session_state.preferences['theme']:
                st.session_state.preferences['theme'] = theme
                st.rerun()

            # 添加购物车项
            item = st.text_input("添加商品")
            if st.button("添加到购物车"):
                st.session_state.cart_items.append(item)
                st.rerun()

            # 导航历史
            st.write("导航历史:")
            for item in st.session_state.navigation_history:
                st.text(f"- {item['page']} at {item['timestamp']}")

    st.info("💡 提示：导航到其他页面（pages/目录下的文件）时，这些状态会保持不变")


# =============================================================================
# 4. 状态重置和清理
# =============================================================================

class SessionStateManager:
    """
    会话状态管理器 - 提供重置和清理功能
    """

    @staticmethod
    def reset_specific_keys(*keys: str):
        """重置特定的状态键"""
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]

    @staticmethod
    def reset_prefix(prefix: str):
        """重置所有以特定前缀开头的键"""
        keys_to_delete = [
            key for key in st.session_state.keys()
            if key.startswith(prefix)
        ]
        for key in keys_to_delete:
            del st.session_state[key]
        return len(keys_to_delete)

    @staticmethod
    def reset_all(confirm: bool = False):
        """重置所有会话状态（危险操作）"""
        if not confirm:
            raise ValueError("需要确认才能重置所有状态")
        st.session_state.clear()

    @staticmethod
    def reset_except(*except_keys: str):
        """重置除指定键之外的所有状态"""
        all_keys = list(st.session_state.keys())
        for key in all_keys:
            if key not in except_keys:
                del st.session_state[key]

    @staticmethod
    def get_state_snapshot() -> Dict[str, Any]:
        """获取当前状态的快照"""
        return dict(st.session_state)

    @staticmethod
    def restore_state_snapshot(snapshot: Dict[str, Any]):
        """从快照恢复状态"""
        st.session_state.clear()
        for key, value in snapshot.items():
            st.session_state[key] = value


def state_reset_demo():
    """状态重置和清理演示"""
    st.title("4️⃣ 状态重置和清理")

    st.markdown("### 当前会话状态")
    st.write(f"状态键数量: {len(st.session_state)}")

    # 添加一些演示状态
    if 'demo_data' not in st.session_state:
        st.session_state.demo_data = {
            'temp_counter': 0,
            'temp_list': [1, 2, 3],
            'temp_config': {'a': 1, 'b': 2}
        }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("重置特定键")
        st.code("""
SessionStateManager.reset_specific_keys('key1', 'key2')
        """, language="python")
        if st.button("重置 demo_data", key="reset_demo"):
            SessionStateManager.reset_specific_keys('demo_data')
            st.rerun()

    with col2:
        st.subheader("重置前缀键")
        st.code("""
count = SessionStateManager.reset_prefix('temp_')
        """, language="python")
        if st.button("重置所有 temp_ 开头的键"):
            count = SessionStateManager.reset_prefix('temp_')
            st.success(f"重置了 {count} 个键")
            st.rerun()

    with col3:
        st.subheader("保存/恢复快照")
        if 'state_snapshot' not in st.session_state:
            if st.button("保存当前状态快照"):
                st.session_state.state_snapshot = SessionStateManager.get_state_snapshot()
                st.success("快照已保存")
                st.rerun()
        else:
            if st.button("恢复快照"):
                SessionStateManager.restore_state_snapshot(st.session_state.state_snapshot)
                st.success("快照已恢复")
                st.rerun()
            if st.button("清除快照"):
                del st.session_state.state_snapshot
                st.rerun()

    st.divider()
    st.subheader("⚠️ 危险操作")
    dangerous_col1, dangerous_col2 = st.columns(2)

    with dangerous_col1:
        st.markdown("**重置除用户数据外的所有状态**")
        st.code("""
SessionStateManager.reset_except('user_authenticated', 'username')
        """, language="python")
        if st.button("执行重置（保留用户数据）", key="reset_except"):
            SessionStateManager.reset_except('user_authenticated', 'username', 'preferences')
            st.success("已重置")
            st.rerun()

    with dangerous_col2:
        st.markdown("**重置所有状态**")
        st.warning("这将清除所有会话数据！")
        if st.button("🔴 全部重置", key="reset_all"):
            SessionStateManager.reset_all(confirm=True)
            st.success("已重置所有状态")
            st.rerun()

    st.divider()
    st.subheader("当前所有状态键")
    st.json(list(st.session_state.keys()))


# =============================================================================
# 5. 复杂对象存储
# =============================================================================

class ComplexObjectStorage:
    """
    复杂对象存储模式

    支持的对象类型：
    - 数据类和 Pydantic 模型
    - Pandas DataFrame
    - NumPy 数组
    - 自定义类实例（可序列化）
    - Lambda 函数（有限支持）
    """

    @staticmethod
    def store_dataframe():
        """存储和操作 DataFrame"""
        if 'df' not in st.session_state:
            # 生成示例数据
            st.session_state.df = pd.DataFrame({
                'x': np.random.randn(100),
                'y': np.random.randn(100),
                'category': np.random.choice(['A', 'B', 'C'], 100)
            })
        return st.session_state.df

    @staticmethod
    def store_dataclass():
        """存储 dataclass 对象"""
        @dataclass
        class UserProfile:
            username: str
            email: str
            preferences: Dict[str, Any] = field(default_factory=dict)
            created_at: datetime = field(default_factory=datetime.now)

        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = UserProfile(
                username="demo_user",
                email="demo@example.com",
                preferences={'theme': 'dark'}
            )
        return st.session_state.user_profile

    @staticmethod
    def store_nested_structures():
        """存储嵌套结构"""
        if 'nested_data' not in st.session_state:
            st.session_state.nested_data = {
                'users': [
                    {'id': 1, 'name': 'Alice', 'scores': [85, 90, 88]},
                    {'id': 2, 'name': 'Bob', 'scores': [78, 82, 80]}
                ],
                'metadata': {
                    'version': '1.0',
                    'last_updated': datetime.now().isoformat(),
                    'tags': ['production', 'v1']
                }
            }
        return st.session_state.nested_data

    @staticmethod
    def store_with_serialization():
        """带序列化的对象存储（用于需要持久化的场景）"""
        if 'serialized_object' not in st.session_state:
            obj = {'data': [1, 2, 3], 'timestamp': datetime.now()}
            st.session_state.serialized_object = pickle.dumps(obj)

        # 反序列化
        return pickle.loads(st.session_state.serialized_object)


def complex_object_storage_demo():
    """复杂对象存储演示"""
    st.title("5️⃣ 复杂对象存储")

    tab1, tab2, tab3, tab4 = st.tabs(["DataFrame", "DataClass", "嵌套结构", "序列化"])

    with tab1:
        st.subheader("Pandas DataFrame 存储")
        df = ComplexObjectStorage.store_dataframe()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("行数", len(df))
            st.metric("列数", len(df.columns))
        with col2:
            st.metric("内存使用", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")

        st.dataframe(df.head(10))

        if st.button("重新生成数据"):
            st.session_state.df = pd.DataFrame({
                'x': np.random.randn(100),
                'y': np.random.randn(100),
                'category': np.random.choice(['A', 'B', 'C'], 100)
            })
            st.rerun()

    with tab2:
        st.subheader("DataClass 对象存储")
        profile = ComplexObjectStorage.store_dataclass()

        st.json({
            'username': profile.username,
            'email': profile.email,
            'preferences': profile.preferences,
            'created_at': profile.created_at.isoformat()
        })

        # 更新偏好
        new_theme = st.selectbox(
            "主题",
            ['light', 'dark'],
            index=['light', 'dark'].index(profile.preferences.get('theme', 'light'))
        )
        if st.button("更新偏好"):
            st.session_state.user_profile.preferences['theme'] = new_theme
            st.rerun()

    with tab3:
        st.subheader("嵌套数据结构")
        nested = ComplexObjectStorage.store_nested_structures()
        st.json(nested)

        # 添加新用户
        with st.expander("添加用户"):
            new_name = st.text_input("用户名")
            if st.button("添加"):
                nested['users'].append({
                    'id': len(nested['users']) + 1,
                    'name': new_name,
                    'scores': []
                })
                st.session_state.nested_data = nested
                st.rerun()

    with tab4:
        st.subheader("序列化对象存储")
        serialized_obj = ComplexObjectStorage.store_with_serialization()
        st.json(serialized_obj)
        st.info("此对象通过 pickle 序列化存储，适合需要持久化的复杂对象")


# =============================================================================
# 6. 性能考虑和优化
# =============================================================================

class PerformanceOptimizer:
    """
    性能优化策略

    关键点：
    1. 大数据对象使用 @st.cache_data 而非 session_state
    2. 极大对象使用 @st.cache_resource
    3. 避免在 session_state 中存储可变对象的引用
    4. 考虑使用分页处理大数据集
    5. 使用适当的序列化格式
    """

    @staticmethod
    @st.cache_data(ttl=3600)  # 缓存1小时
    def load_large_dataset(size: int = 1000000):
        """加载大数据集 - 使用缓存而非 session_state"""
        # 模拟大数据集加载
        import time
        time.sleep(1)  # 模拟加载延迟
        return pd.DataFrame({
            'id': range(size),
            'value': np.random.randn(size),
            'category': np.random.choice(['A', 'B', 'C', 'D'], size)
        })

    @staticmethod
    def paginated_data_display(data: pd.DataFrame, page_size: int = 100):
        """分页显示大数据"""
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0
        if 'page_size' not in st.session_state:
            st.session_state.page_size = page_size

        total_pages = len(data) // st.session_state.page_size + 1
        current_page = st.session_state.current_page

        start_idx = current_page * st.session_state.page_size
        end_idx = start_idx + st.session_state.page_size

        # 显示当前页
        st.dataframe(data.iloc[start_idx:end_idx])

        # 分页控制
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("◀ 上一页", disabled=(current_page == 0)):
                st.session_state.current_page -= 1
                st.rerun()
        with col2:
            st.write(f"第 {current_page + 1} / {total_pages} 页")
        with col3:
            if st.button("下一页 ▶", disabled=(current_page >= total_pages - 1)):
                st.session_state.current_page += 1
                st.rerun()
        with col4:
            new_page = st.number_input("跳转到页", min_value=1, max_value=total_pages)
            if st.button("跳转"):
                st.session_state.current_page = new_page - 1
                st.rerun()

    @staticmethod
    def store_reference_optimized():
        """优化引用存储 - 避免共享引用问题"""
        # 错误方式 - 多个键引用同一对象
        # st.session_state.data1 = large_df
        # st.session_state.data2 = large_df  # 共享引用！

        # 正确方式 - 使用 .copy()
        if 'base_data' not in st.session_state:
            st.session_state.base_data = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

        if 'copied_data' not in st.session_state:
            st.session_state.copied_data = st.session_state.base_data.copy()

        return st.session_state.copied_data

    @staticmethod
    def estimate_memory_usage():
        """估算 session_state 内存使用"""
        import sys

        def get_size(obj, seen=None):
            """递归获取对象大小"""
            size = sys.getsizeof(obj)
            if seen is None:
                seen = set()

            obj_id = id(obj)
            if obj_id in seen:
                return 0

            seen.add(obj_id)

            if isinstance(obj, dict):
                size += sum(get_size(k, seen) + get_size(v, seen) for k, v in obj.items())
            elif hasattr(obj, '__dict__'):
                size += get_size(obj.__dict__, seen)
            elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
                try:
                    size += sum(get_size(i, seen) for i in obj)
                except:
                    pass

            return size

        total_size = 0
        breakdown = {}

        for key, value in st.session_state.items():
            try:
                size = get_size(value)
                breakdown[key] = size
                total_size += size
            except:
                breakdown[key] = 0

        return total_size, breakdown


def performance_optimization_demo():
    """性能优化演示"""
    st.title("6️⃣ 性能考虑和优化")

    st.markdown(r"""
    ### 性能优化指南：

    1. **大数据缓存**: 使用 `@st.cache_data` 而非 session_state
    2. **极大对象**: 使用 `@st.cache_resource` (慎用，可能导致并发问题)
    3. **引用问题**: 使用 `.copy()` 避免共享引用
    4. **分页加载**: 大数据集分页显示
    5. **内存监控**: 监控 session_state 内存使用
    """)

    tab1, tab2, tab3, tab4 = st.tabs(["缓存策略", "分页显示", "引用优化", "内存监控"])

    with tab1:
        st.subheader("缓存 vs Session State")
        st.markdown("""
        **何时使用 @st.cache_data:**
        - 大型 DataFrame (>100MB)
        - 数据库查询结果
        - ML 模型加载

        **何时使用 session_state:**
        - 用户交互状态
        - 小型配置对象
        - UI 组件状态
        """)

        if st.button("加载大数据集 (使用缓存)"):
            with st.spinner("加载中..."):
                df = PerformanceOptimizer.load_large_dataset(100000)
                st.session_state.cached_df_ref = df
            st.success(f"已加载 {len(df)} 行数据")

        if 'cached_df_ref' in st.session_state:
            st.metric("数据行数", f"{len(st.session_state.cached_df_ref):,}")

    with tab2:
        st.subheader("分页显示大数据")
        size = st.slider("数据集大小", 1000, 10000, 5000, step=1000)

        if 'demo_df' not in st.session_state or len(st.session_state.demo_df) != size:
            st.session_state.demo_df = pd.DataFrame({
                'id': range(size),
                'value': np.random.randn(size),
                'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], size)
            })

        PerformanceOptimizer.paginated_data_display(st.session_state.demo_df, page_size=50)

    with tab3:
        st.subheader("引用优化")
        st.markdown("""
        ### 问题：共享引用
        ```python
        # 错误 - data1 和 data2 指向同一对象
        st.session_state.data1 = large_df
        st.session_state.data2 = large_df
        # 修改 data1 会影响 data2！

        # 正确 - 创建副本
        st.session_state.data1 = large_df
        st.session_state.data2 = large_df.copy()
        ```
        """)
        copied = PerformanceOptimizer.store_reference_optimized()
        st.dataframe(copied)

        if st.button("修改副本"):
            st.session_state.copied_data.loc[0, 'a'] = 999
            st.rerun()

        st.write("原始数据:")
        st.dataframe(st.session_state.base_data)

    with tab4:
        st.subheader("内存监控")
        total_size, breakdown = PerformanceOptimizer.estimate_memory_usage()

        st.metric("总内存使用", f"{total_size / 1024:.2f} KB")

        with st.expander("详细分解"):
            # 按大小排序
            sorted_breakdown = dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))
            for key, size in sorted_breakdown.items():
                st.progress(size / total_size if total_size > 0 else 0)
                st.text(f"{key}: {size / 1024:.2f} KB")


# =============================================================================
# 主应用入口
# =============================================================================

def main():
    """主应用"""
    st.set_page_config(
        page_title="Streamlit Session State 高级模式",
        page_icon="📊",
        layout="wide"
    )

    # 侧边栏导航
    with st.sidebar:
        st.title("📚 导航")
        st.markdown("---")
        page = st.radio(
            "选择主题",
            [
                "📖 简介",
                "1️⃣ 最佳实践",
                "2️⃣ 初始化模式",
                "3️⃣ 跨页面共享",
                "4️⃣ 状态重置",
                "5️⃣ 复杂对象",
                "6️⃣ 性能优化"
            ]
        )

        st.markdown("---")
        st.markdown("### 快速统计")
        st.metric("状态键数量", len(st.session_state))
        if hasattr(st, 'runtime') and hasattr(st.runtime, 'get_instance'):
            # 尝试获取运行时信息（如果可用）
            pass

    # 路由到不同页面
    if page == "📖 简介":
        st.title("📖 Streamlit Session State 高级模式指南")

        st.markdown(r"""
        ## 概述

        本指南全面介绍 Streamlit 的 `st.session_state` 高级使用模式，帮助开发者构建更复杂、更健壮的 Streamlit 应用。

        ## 涵盖内容

        ### 1️⃣ 最佳实践
        - 使用唯一键名避免冲突
        - 始终检查键是否存在
        - 使用有意义的前缀组织状态

        ### 2️⃣ 初始化模式
        - if-not-in 检查
        - setdefault() 方法
        - getattr 带默认值
        - 工厂函数模式
        - 单例模式
        - 类型化状态

        ### 3️⃣ 跨页面共享
        - 多页面应用中的状态共享原理
        - 导航历史追踪
        - 用户认证状态管理

        ### 4️⃣ 状态重置和清理
        - 选择性重置
        - 前缀匹配重置
        - 状态快照和恢复

        ### 5️⃣ 复杂对象存储
        - DataFrame 存储
        - DataClass 对象
        - 嵌套数据结构
        - 序列化策略

        ### 6️⃣ 性能考虑
        - 缓存策略 (@st.cache_data vs @st.cache_resource)
        - 大数据分页显示
        - 引用优化
        - 内存监控

        ## 参考资源

        - [Streamlit 官方文档 - Session State](https://docs.streamlit.io/develop/concepts/architecture/session-state)
        - [Streamlit 最佳实践 - Medium](https://medium.com/@jashuamrita360/best-practices-for-streamlit-development-structuring-code-and-managing-session-state-0bdcfb91a745)
        """)

    elif page == "1️⃣ 最佳实践":
        best_practices_demo()
    elif page == "2️⃣ 初始化模式":
        initialization_patterns_demo()
    elif page == "3️⃣ 跨页面共享":
        cross_page_sharing_demo()
    elif page == "4️⃣ 状态重置":
        state_reset_demo()
    elif page == "5️⃣ 复杂对象":
        complex_object_storage_demo()
    elif page == "6️⃣ 性能优化":
        performance_optimization_demo()


if __name__ == "__main__":
    main()
