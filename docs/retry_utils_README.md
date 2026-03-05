# Python API 调用重试最佳实践工具包

一个生产级别的 Python API 重试工具包，提供完整的重试、退避、限流和统计功能。

## 功能特性

- **指数退避算法**: 智能计算重试延迟，避免服务器过载
- **Tenacity 集成**: 支持流行的 tenacity 库
- **同步/异步支持**: 完整的 sync 和 async/await 支持
- **自定义重试装饰器**: 灵活的重试装饰器
- **429 错误处理**: 自动处理限流错误，遵守 Retry-After 头
- **超时配置**: 全面的超时控制
- **统计信息**: 重试统计和监控
- **限流器**: 令牌桶限流器
- **上下文管理器**: 代码块级别的重试控制

## 快速开始

### 安装

```bash
pip install httpx tenacity pytest pytest-asyncio
```

### 基础使用

```python
from utils.retry_utils import retry_with_exponential_backoff, RetryConfig
import httpx

@retry_with_exponential_backoff()
def fetch_data(url: str) -> dict:
    """自动重试的 API 调用"""
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()

result = fetch_data("https://api.example.com/data")
```

### 异步使用

```python
from utils.retry_utils import aretry_with_exponential_backoff
import httpx

@aretry_with_exponential_backoff()
async def fetch_data(url: str) -> dict:
    """异步自动重试的 API 调用"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

result = await fetch_data("https://api.example.com/data")
```

## 文件结构

```
D:\AI_Projects\system-max\
├── utils/
│   ├── __init__.py          # 包初始化，导出所有公共接口
│   ├── retry_utils.py       # 核心重试工具实现
│   └── retry_examples.py    # 使用示例
├── tests/
│   ├── __init__.py
│   └── test_retry_utils.py  # 单元测试
└── docs/
    ├── retry_utils_guide.md      # 详细使用指南
    └── retry_quick_reference.md  # 快速参考
```

## 核心组件

### 1. RetryConfig - 重试配置

```python
config = RetryConfig(
    max_attempts=3,           # 最大重试次数
    base_delay=1.0,           # 基础延迟（秒）
    max_delay=60.0,           # 最大延迟（秒）
    exponential_base=2.0,      # 指数退避基数
    jitter=True,              # 添加随机抖动
    jitter_range=0.1,         # 抖动范围
    timeout=30.0,             # 请求超时
    respect_retry_after=True, # 遵守 Retry-After 头
)
```

### 2. 装饰器

- `@retry_with_exponential_backoff()` - 同步重试装饰器
- `@aretry_with_exponential_backoff()` - 异步重试装饰器
- `@retry_with_tenacity()` - Tenacity 库装饰器

### 3. HTTP 客户端

- `RetryableHTTPClient` - 同步 HTTP 客户端
- `AsyncRetryableHTTPClient` - 异步 HTTP 客户端

### 4. 限流器

```python
from utils.retry_utils import RateLimiter

limiter = RateLimiter(rate=10, per=1.0)  # 每秒10个请求

async with limiter:
    await api_call()
```

### 5. 统计信息

```python
from utils.retry_utils import RetryStatistics

stats = RetryStatistics()

# 使用后查看统计
print(stats)
# RetryStatistics(total=5, success=3, failed=2, total_delay=12.50s)
```

## 可重试的 HTTP 状态码

- `429` - Too Many Requests
- `500` - Internal Server Error
- `502` - Bad Gateway
- `503` - Service Unavailable
- `504` - Gateway Timeout

## 指数退避算法

```
延迟 = min(base_delay * (exponential_base ^ attempt), max_delay)

示例：base_delay=1, exponential_base=2
- 第1次重试: 1秒
- 第2次重试: 2秒
- 第3次重试: 4秒
- 第4次重试: 8秒
- ...（直到 max_delay）
```

## 运行测试

```bash
# 运行所有测试
pytest tests/test_retry_utils.py -v

# 运行特定测试
pytest tests/test_retry_utils.py::TestRetryDecorator -v
```

## 更多示例

查看 `utils/retry_examples.py` 获取更多使用示例：

- 基础重试
- 异步重试
- 统计信息
- 限流处理
- HTTP 客户端封装
- 限流器
- 上下文管理器
- Tenacity 集成
- 自定义重试条件

## 最佳实践

1. **根据场景选择重试次数**
   - 不重要的操作: `max_attempts=2`
   - 一般 API 调用: `max_attempts=3`
   - 重要操作: `max_attempts=5`
   - 关键操作: `max_attempts=10, max_delay=300.0`

2. **合理配置延迟**
   - 快速 API: `base_delay=0.5, max_delay=10.0`
   - 一般 API: `base_delay=1.0, max_delay=60.0`
   - 慢速 API: `base_delay=2.0, max_delay=300.0`

3. **使用抖动避免惊群效应**
   ```python
   RetryConfig(jitter=True, jitter_range=0.1)
   ```

4. **遵守 Retry-After 头**
   ```python
   RetryConfig(respect_retry_after=True)
   ```

5. **组合使用限流和重试**
   ```python
   async with AsyncRetryableHTTPClient(config=retry_config) as client:
       limiter = RateLimiter(rate=10, per=1.0)

       async def fetch(url):
           async with limiter:
               return await client.get(url)
   ```

## 许可证

MIT License
