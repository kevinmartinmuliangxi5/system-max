# 双脑Ralph系统 - 编码规范

## Python代码规范

### 基本原则
- 遵循PEP 8标准
- 代码可读性第一
- 简单优于复杂
- 明确优于隐晦

### 命名规范

#### 变量命名
```python
# ✅ 好的命名
user_name = "Alice"
is_valid = True
max_retry_count = 3

# ❌ 避免的命名
un = "Alice"         # 太简短
isValid = True       # 使用驼峰（Python推荐下划线）
MAX_RETRY = 3        # 普通变量不用大写
```

#### 函数命名
```python
# ✅ 动词开头，清晰表达功能
def get_user_info(user_id):
    pass

def validate_email(email):
    pass

def calculate_total_price(items):
    pass

# ❌ 避免
def user():  # 不清楚是获取还是创建
    pass

def process():  # 太泛化
    pass
```

#### 类命名
```python
# ✅ 使用驼峰命名法
class UserManager:
    pass

class DatabaseConnection:
    pass

# ❌ 避免
class user_manager:  # 应该使用驼峰
    pass
```

### 代码结构

#### 模块组织
```python
"""模块文档字符串"""
# 1. 标准库导入
import os
import json
from pathlib import Path

# 2. 第三方库导入
import jieba
from anthropic import Anthropic

# 3. 本地导入
from core.hippocampus import Hippocampus
from core.router import TaskRouter

# 4. 常量定义
DEFAULT_MODEL = "claude-sonnet-4-5"
MAX_TOKENS = 100000

# 5. 类和函数定义
class MyClass:
    pass

def my_function():
    pass
```

#### 函数结构
```python
def process_task(task_name: str, options: dict = None) -> dict:
    """
    处理任务的核心函数

    Args:
        task_name: 任务名称
        options: 可选配置项，默认None

    Returns:
        包含处理结果的字典

    Raises:
        ValueError: 当task_name为空时
        RuntimeError: 当处理失败时

    Example:
        >>> result = process_task("build", {"verbose": True})
        >>> print(result["status"])
        "success"
    """
    # 1. 参数验证
    if not task_name:
        raise ValueError("Task name cannot be empty")

    options = options or {}

    # 2. 核心逻辑
    result = {"status": "pending"}

    try:
        # 执行处理
        result["status"] = "success"
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        raise RuntimeError(f"Task processing failed: {e}")

    # 3. 返回结果
    return result
```

### 注释规范

#### 文档字符串
```python
# ✅ Google风格
def retrieve_memory(query: str, top_k: int = 5) -> list:
    """
    从记忆库检索相关经验

    使用BM25算法进行混合检索，支持中英文查询。

    Args:
        query: 搜索查询词
        top_k: 返回结果数量，默认5

    Returns:
        相关经验列表，按相关性排序

    Example:
        memories = retrieve_memory("用户登录", top_k=3)
    """
    pass
```

#### 行内注释
```python
# ✅ 解释"为什么"，而非"做什么"
# 使用BM25算法可以更好地处理中文分词
bm25_scores = calculate_bm25(query, documents)

# 设置超时为30秒，防止长时间阻塞
response = requests.get(url, timeout=30)

# ❌ 避免冗余注释
# 计算总和
total = sum(numbers)  # 代码本身已经很清楚了
```

### 错误处理

#### 具体异常捕获
```python
# ✅ 捕获具体异常
try:
    with open(file_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    data = {}
except json.JSONDecodeError:
    logger.error(f"Invalid JSON in {file_path}")
    data = {}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# ❌ 避免裸except
try:
    risky_operation()
except:  # 不要这样做
    pass
```

#### 自定义异常
```python
class TaskExecutionError(Exception):
    """任务执行失败异常"""
    pass

class MemoryNotFoundError(Exception):
    """记忆未找到异常"""
    pass

def execute_task(task):
    if not task.is_valid():
        raise TaskExecutionError(f"Invalid task: {task.name}")
```

### 类型提示

#### 基本类型
```python
from typing import List, Dict, Optional, Union, Tuple

def process_users(
    users: List[str],
    config: Dict[str, Any],
    max_count: Optional[int] = None
) -> Tuple[List[str], int]:
    """处理用户列表"""
    processed = []
    count = 0
    # ... 处理逻辑
    return processed, count
```

#### 复杂类型
```python
from typing import TypedDict, Callable

class TaskConfig(TypedDict):
    name: str
    priority: int
    dependencies: List[str]

ProcessorFunc = Callable[[str], Dict[str, Any]]

def register_processor(func: ProcessorFunc) -> None:
    """注册处理器函数"""
    pass
```

### 代码组织

#### 单一职责
```python
# ✅ 每个函数只做一件事
def load_config(path: str) -> dict:
    """只负责加载配置"""
    with open(path) as f:
        return json.load(f)

def validate_config(config: dict) -> bool:
    """只负责验证配置"""
    return "api_key" in config

def initialize_system(config_path: str):
    """组合使用"""
    config = load_config(config_path)
    if not validate_config(config):
        raise ValueError("Invalid config")
    return config

# ❌ 避免一个函数做太多事
def load_and_validate_and_process_config(path: str):
    """做了太多事情"""
    pass
```

#### 避免魔法数字
```python
# ✅ 使用常量
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

for attempt in range(MAX_RETRY_COUNT):
    response = api_call(timeout=DEFAULT_TIMEOUT)

# ❌ 避免魔法数字
for attempt in range(3):  # 3是什么意思？
    response = api_call(timeout=30)  # 30是什么单位？
```

## 项目特定规范

### 文件命名
- Python文件: 小写+下划线 `user_manager.py`
- 测试文件: `test_` 前缀 `test_user_manager.py`
- 配置文件: 小写+连字符 `config-prod.json`
- 文档文件: 大写+下划线 `README.md`, `API_DOCS.md`

### 目录结构
```
module/
├─ __init__.py          # 模块初始化
├─ core/                # 核心逻辑
│  ├─ __init__.py
│  ├─ engine.py         # 主引擎
│  └─ utils.py          # 工具函数
├─ models/              # 数据模型
│  └─ task.py
├─ tests/               # 测试代码
│  └─ test_engine.py
└─ README.md            # 模块文档
```

### 导入顺序
```python
# 1. __future__ imports
from __future__ import annotations

# 2. 标准库
import os
import sys
from pathlib import Path

# 3. 第三方库
import anthropic
import jieba

# 4. 本地导入 - 绝对导入
from core.hippocampus import Hippocampus
from core.router import TaskRouter

# 5. 本地导入 - 相对导入 (谨慎使用)
from .utils import helper_function
```

### 日志规范
```python
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 使用日志
logger.debug("Detailed debug info")
logger.info("Task started")
logger.warning("Potential issue detected")
logger.error("Operation failed", exc_info=True)

# ✅ 包含上下文信息
logger.info(f"Processing task: {task.name}, priority: {task.priority}")

# ❌ 避免日志泛滥
logger.debug("Entering function")  # 太多了
logger.debug("Exiting function")
```

## Git提交规范

### 提交信息格式
```
类型: 简短描述（不超过50字符）

详细说明（可选，与简短描述空一行）
- 为什么做这个改动
- 改动的影响范围
- 相关的Issue或PR

Refs: #123
```

### 类型定义
- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建、配置等

### 示例
```
feat: 集成claude-mem记忆系统

- 添加claude-mem配置和集成代码
- 实现双记忆系统融合逻辑
- 更新Dealer以支持记忆检索

完成后能够在生成指令时同时检索Hippocampus和claude-mem。

Refs: #42
```

## 测试规范

### 测试文件组织
```python
# tests/test_hippocampus.py
import pytest
from core.hippocampus import Hippocampus

class TestHippocampus:
    """海马体测试套件"""

    def setup_method(self):
        """每个测试前的设置"""
        self.hippo = Hippocampus()

    def teardown_method(self):
        """每个测试后的清理"""
        pass

    def test_store_and_retrieve(self):
        """测试存储和检索功能"""
        self.hippo.store("test_key", "test_value")
        result = self.hippo.retrieve("test_key")
        assert result == "test_value"

    def test_empty_query(self):
        """测试空查询"""
        with pytest.raises(ValueError):
            self.hippo.retrieve("")
```

### 测试覆盖要求
- 单元测试覆盖率 > 80%
- 关键路径100%覆盖
- 每个公共API都有测试
- 边界情况和错误情况都覆盖

## 性能规范

### 避免常见陷阱
```python
# ✅ 使用列表推导
squares = [x**2 for x in range(1000)]

# ❌ 避免循环append
squares = []
for x in range(1000):
    squares.append(x**2)

# ✅ 使用生成器（节省内存）
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

# ✅ 使用join拼接字符串
result = "".join(parts)

# ❌ 避免重复字符串拼接
result = ""
for part in parts:
    result += part  # 每次都创建新字符串
```

### 缓存策略
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n):
    """使用缓存避免重复计算"""
    return sum(range(n))
```

## 安全规范

### 输入验证
```python
def process_user_input(user_input: str) -> str:
    """处理用户输入"""
    # 验证
    if not user_input or len(user_input) > 1000:
        raise ValueError("Invalid input length")

    # 清理
    sanitized = user_input.strip()

    # 转义特殊字符（如果需要）
    return sanitized
```

### 敏感信息
```python
# ✅ 使用环境变量
import os
API_KEY = os.getenv("ZHIPU_API_KEY")

# ❌ 避免硬编码
API_KEY = "sk-xxxxx"  # 不要这样做！

# ✅ 日志中隐藏敏感信息
logger.info(f"Using API key: {API_KEY[:8]}...")
```

## 文档规范

### README结构
```markdown
# 项目名称

简短描述

## 快速开始

安装和使用步骤

## 功能特性

核心功能列表

## 配置说明

配置文件和环境变量

## API文档

主要API说明

## 开发指南

如何参与开发

## 许可证

MIT License
```

### 代码注释比例
- 复杂算法: 详细注释
- 业务逻辑: 必要注释
- 简单代码: 少量或无注释
- 公共API: 完整文档字符串

## 工具推荐

### 代码质量
- `pylint`: 代码检查
- `black`: 代码格式化
- `isort`: 导入排序
- `mypy`: 类型检查

### 测试工具
- `pytest`: 测试框架
- `pytest-cov`: 覆盖率
- `pytest-mock`: Mock工具

## 持续改进

### 代码审查清单
- [ ] 是否遵循命名规范？
- [ ] 是否有足够的注释？
- [ ] 是否有类型提示？
- [ ] 是否有单元测试？
- [ ] 是否处理了异常？
- [ ] 是否考虑了边界情况？
- [ ] 是否有性能问题？
- [ ] 是否有安全隐患？

### 重构时机
- 代码重复超过3次
- 函数超过50行
- 类超过300行
- 复杂度过高
- 测试困难

## 总结

遵循这些规范能够：
- ✅ 提高代码可读性
- ✅ 减少Bug
- ✅ 便于团队协作
- ✅ 简化维护工作
- ✅ 提升代码质量
