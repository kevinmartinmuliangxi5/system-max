# Streamlit 会话状态管理高级模式完整指南

## 📚 概述

本指南全面介绍了 Streamlit 的 `st.session_state` 高级使用模式，包含可运行的代码示例和多页面应用演示。

## 📁 文件结构

```
D:\AI_Projects\system-max\
├── streamlit_session_state_guide.py          # 主应用（完整指南）
├── streamlit_session_state_quick_reference.py # 快速参考代码片段
└── pages/                                      # 多页面示例
    ├── 1__page_one.py                         # 页面1：跨页面状态共享
    ├── 2__page_two.py                         # 页面2：购物车演示
    └── 3__page_three.py                       # 页面3：状态查看器
```

## 🚀 运行应用

```bash
cd D:\AI_Projects\system-max
streamlit run streamlit_session_state_guide.py
```

## 📖 内容覆盖

### 1️⃣ Session State 最佳实践

**核心原则：**
- 使用唯一的键名避免冲突
- 始终检查键是否存在
- 使用有意义的前缀组织状态
- 避免存储过大的对象
- 考虑序列化兼容性

**代码示例：**
```python
# 带前缀的状态初始化
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = True
    st.session_state.app_version = "1.0.0"
```

### 2️⃣ 状态初始化模式

| 模式 | 代码 | 适用场景 |
|------|------|----------|
| if-not-in | `if 'key' not in st.session_state: ...` | 最常用，清晰明确 |
| setdefault | `st.session_state.setdefault('key', default)` | 简洁，一行代码 |
| getattr | `getattr(st.session_state, 'key', default)` | 类属性风格读取 |
| 工厂函数 | `st.session_state.setdefault('key', create_obj())` | 复杂对象初始化 |
| 单例模式 | `if 'conn' not in st.session_state: ...` | 数据库连接等 |
| 类型化状态 | 使用 dataclass | 类型安全，IDE支持 |

### 3️⃣ 跨页面状态共享

**关键点：**
- `st.session_state` 在多页面应用中全局共享
- 任何页面设置的状态变量可以在其他页面访问
- 适用于用户认证、偏好设置、购物车等场景

**代码示例：**
```python
class CrossPageStateManager:
    SHARED_KEYS = [
        'user_authenticated',
        'username',
        'preferences',
        'cart_items',
        'navigation_history'
    ]

    @classmethod
    def init_shared_state(cls):
        for key in cls.SHARED_KEYS:
            if key not in st.session_state:
                st.session_state[key] = get_default(key)
```

### 4️⃣ 状态重置和清理

**重置模式：**
- `reset_specific_keys(*keys)` - 重置特定键
- `reset_prefix(prefix)` - 重置前缀匹配的键
- `reset_all()` - 重置所有状态（危险）
- `reset_except(*keys)` - 保留指定键，重置其他
- 状态快照保存和恢复

### 5️⃣ 复杂对象存储

**支持的对象类型：**
- 数据类和 Pydantic 模型
- Pandas DataFrame
- NumPy 数组
- 自定义类实例（可序列化）
- 嵌套数据结构
- 序列化对象（使用 pickle）

**代码示例：**
```python
@dataclass
class TypedSessionState:
    counter: int = 0
    messages: List[str] = field(default_factory=list)

# 使用
typed_state = TypedSessionState.from_session_state()
```

### 6️⃣ 性能考虑和优化

**优化策略：**
1. **大数据缓存**: 使用 `@st.cache_data` 而非 session_state
2. **极大对象**: 使用 `@st.cache_resource` (慎用)
3. **引用问题**: 使用 `.copy()` 避免共享引用
4. **分页加载**: 大数据集分页显示
5. **内存监控**: 监控 session_state 内存使用

**缓存对比：**
| 装饰器 | 用途 | 复制 | 适用场景 |
|--------|------|------|----------|
| `@st.cache_data` | 数据函数 | 是 | DataFrame <1亿行 |
| `@st.cache_resource` | 资源对象 | 否 | DB连接、ML模型 |

## 📚 快速参考模块

`streamlit_session_state_quick_reference.py` 提供了可直接复用的工具函数：

### 初始化函数
```python
init_state(key, default)              # 简单初始化
init_state_factory(key, factory)      # 工厂函数初始化
```

### 回调辅助
```python
create_callback(callback, *args)      # 创建带参数的回调
increment_state(key, amount)         # 增加状态值
update_state_value(key, value)       # 更新状态值
```

### 状态管理
```python
reset_state(*keys)                   # 重置指定键
reset_state_prefix(prefix)           # 重置前缀键
save_snapshot(name)                  # 保存快照
restore_snapshot(name)               # 恢复快照
```

### 类型安全访问
```python
TypedState.get_int(key, default)      # 获取整数
TypedState.get_str(key, default)      # 获取字符串
TypedState.get_bool(key, default)     # 获取布尔值
TypedState.get_list(key, default)     # 获取列表
TypedState.get_dict(key, default)     # 获取字典
```

## 🔗 参考资源

- [Streamlit 官方文档 - Session State](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- [Streamlit 最佳实践 - Medium](https://medium.com/@jashuamrita360/best-practices-for-streamlit-development-structuring-code-and-managing-session-state-0bdcfb91a745)
- [Session State API 参考](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
- [多页面应用指南](https://docs.streamlit.io/develop/concepts/multipage-apps/page_directory)
- [缓存最佳实践](https://docs.streamlit.io/develop/concepts/architecture/caching)

## 🎯 使用建议

1. **简单应用**: 使用 `if 'key' not in st.session_state` 模式
2. **中型应用**: 使用 `setdefault` 和工具类
3. **复杂应用**: 使用类型化状态和专门的 StateManager
4. **多页面应用**: 使用 CrossPageStateManager 统一管理
5. **大数据应用**: 结合 @st.cache_data 使用
