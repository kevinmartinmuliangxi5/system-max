# API 重试工具包使用指南

完整的Python API调用重试最佳实践解决方案。

## 目录

1. [概述](#概述)
2. [安装依赖](#安装依赖)
3. [核心概念](#核心概念)
4. [使用示例](#使用示例)
5. [最佳实践](#最佳实践)
6. [API参考](#api参考)

## 概述

本工具包提供了生产级别的API重试功能，包括：

- **指数退避算法**：智能计算重试延迟
- **Tenacity集成**：支持流行的tenacity库
- **自定义装饰器**：灵活的重试装饰器
- **异步重试**：完整的async/await支持
- **限流处理**：自动处理429错误和Retry-After头
- **超时配置**：全面的超时控制
- **统计信息**：重试统计和监控

## 安装依赖

```bash
# 必需依赖
pip install httpx

# 可选依赖（推荐）
pip install tenacity

# 测试依赖
pip install pytest pytest-asyncio
```

## 核心概念

### 1. 重试配置（RetryConfig）

```python
from utils.retry_utils import RetryConfig

config = RetryConfig(
    max_attempts=3,           # 最大重试次数
    base_delay=1.0,           # 基础延迟（秒）
    max_delay=60.0,           # 最大延迟（秒）
    exponential_base=2.0,     # 指数退避基数
    jitter=True,              # 添加随机抖动
    jitter_range=0.1,         # 抖动范围
    timeout=30.0,             # 请求超时
    respect_retry_after=True, # 遵守Retry-After头
)
```

### 2. 可重试的HTTP状态码

默认处理以下状态码：
- `429` - Too Many Requests
- `500` - Internal Server Error
- `502` - Bad Gateway
- `503` - Service Unavailable
- `504` - Gateway Timeout

### 3. 指数退避算法

```
延迟 = min(base_delay * (exponential_base ^ attempt), max_delay)

示例：base_delay=1, exponential_base=2
- 第1次重试: 1秒
- 第2次重试: 2秒
- 第3次重试: 4秒
- 第4次重试: 8秒
- ...（直到max_delay）
```

## 使用示例

### 示例 1: 基础重试装饰器

```python
from utils.retry_utils import retry_with_exponential_backoff, RetryConfig
import httpx

@retry_with_exponential_backoff(
    config=RetryConfig(max_attempts=3, base_delay=1.0)
)
def fetch_user_data(user_id: int) -> dict:
    """自动重试的API调用"""
    with httpx.Client() as client:
        response = client.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()

# 使用
result = fetch_user_data(123)
```

### 示例 2: 异步重试

```python
from utils.retry_utils import aretry_with_exponential_backoff, RetryConfig

@aretry_with_exponential_backoff(
    config=RetryConfig(max_attempts=3, base_delay=1.0)
)
async def async_fetch_data(url: str) -> dict:
    """异步自动重试的API调用"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# 使用
result = await async_fetch_data("https://api.example.com/data")
```

### 示例 3: 使用统计信息

```python
from utils.retry_utils import (
    retry_with_exponential_backoff,
    RetryConfig,
    RetryStatistics
)

stats = RetryStatistics()

@retry_with_exponential_backoff(
    config=RetryConfig(max_attempts=5),
    stats=stats,
)
def fetch_with_stats(url: str) -> dict:
    """带统计信息的API调用"""
    # ... API调用逻辑
    pass

# 使用后查看统计
try:
    result = fetch_with_stats("https://api.example.com/data")
except Exception as e:
    print(f"最终失败: {e}")

print(f"统计信息: {stats}")
# 输出: RetryStatistics(total=5, success=0, failed=5, total_delay=15.00s)
print(f"错误分类: {stats.errors_by_type}")
```

### 示例 4: 处理429限流错误

```python
from utils.retry_utils import (
    retry_with_exponential_backoff,
    RetryConfig,
    RateLimitError
)

@retry_with_exponential_backoff(
    config=RetryConfig(
        max_attempts=10,       # 429可能需要更多重试
        base_delay=1.0,
        max_delay=120.0,        # 更长的最大延迟
        respect_retry_after=True,  # 遵守服务器的Retry-After
    )
)
def fetch_with_rate_limit_handling(url: str) -> dict:
    """处理限流的API调用"""
    with httpx.Client() as client:
        response = client.get(url)

        # 检查是否限流
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "60")
            raise RateLimitError(
                f"Rate limited. Retry after {retry_after}s",
                retry_after=float(retry_after)
            )

        response.raise_for_status()
        return response.json()
```

### 示例 5: 使用HTTP客户端封装

```python
from utils.retry_utils import RetryableHTTPClient, RetryConfig

def demo_http_client():
    """使用封装的HTTP客户端"""
    with RetryableHTTPClient(
        config=RetryConfig(max_attempts=3),
        timeout=30.0,
    ) as client:
        # 所有请求自动重试
        response1 = client.get("https://api.example.com/data1")
        response2 = client.post("https://api.example.com/data2", json={"key": "value"})

        print(response1.json())
        print(response2.json())
```

### 示例 6: 异步HTTP客户端

```python
from utils.retry_utils import AsyncRetryableHTTPClient, RetryConfig
import asyncio

async def demo_async_client():
    """使用异步HTTP客户端"""
    async with AsyncRetryableHTTPClient(
        config=RetryConfig(max_attempts=3),
        timeout=30.0,
    ) as client:
        # 并发请求
        responses = await asyncio.gather(
            client.get("https://api.example.com/data1"),
            client.get("https://api.example.com/data2"),
            client.get("https://api.example.com/data3"),
        )

        for response in responses:
            print(response.json())

asyncio.run(demo_async_client())
```

### 示例 7: 使用限流器

```python
from utils.retry_utils import RateLimiter
import asyncio

async def demo_rate_limiter():
    """确保不超过API速率限制"""
    # 创建限流器：每秒最多5个请求
    limiter = RateLimiter(rate=5, per=1.0)

    async def fetch_item(item_id: int):
        async with limiter:  # 自动限流
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.example.com/items/{item_id}"
                )
                return response.json()

    # 并发执行，但自动遵守速率限制
    tasks = [fetch_item(i) for i in range(20)]
    results = await asyncio.gather(*tasks)
    print(f"获取了 {len(results)} 个项目")

asyncio.run(demo_rate_limiter())
```

### 示例 8: 组合重试和限流

```python
from utils.retry_utils import (
    AsyncRetryableHTTPClient,
    RateLimiter,
    RetryConfig,
    RetryStatistics
)
import asyncio

async def demo_combined():
    """组合使用重试和限流（生产环境推荐）"""
    stats = RetryStatistics()

    async with AsyncRetryableHTTPClient(
        config=RetryConfig(
            max_attempts=5,
            respect_retry_after=True,
        ),
        stats=stats,
    ) as client:
        # 限流器：每秒10个请求
        limiter = RateLimiter(rate=10, per=1.0)

        async def fetch_data(url: str):
            # 组合限流和重试
            async with limiter:
                response = await client.get(url)
                return response.json()

        # 批量获取
        urls = [f"https://api.example.com/items/{i}" for i in range(100)]
        results = await asyncio.gather(
            *[fetch_data(url) for url in urls],
            return_exceptions=True
        )

        success_count = sum(1 for r in results if not isinstance(r, Exception))
        print(f"成功: {success_count}/{len(urls)}")
        print(f"统计: {stats}")

asyncio.run(demo_combined())
```

### 示例 9: 使用Tenacity

```python
from utils.retry_utils import retry_with_tenacity

if TENACITY_AVAILABLE:
    @retry_with_tenacity(
        max_attempts=5,
        wait_min=1.0,
        wait_max=30.0,
    )
    def fetch_with_tenacity(url: str) -> dict:
        """使用tenacity库的重试"""
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
```

### 示例 10: 自定义重试条件

```python
from utils.retry_utils import retry_with_exponential_backoff, RetryConfig

class MyAPIError(Exception):
    """自定义API错误"""
    pass

def is_my_error_retryable(error: Exception) -> bool:
    """判断自定义错误是否可重试"""
    if isinstance(error, MyAPIError):
        error_msg = str(error).lower()
        return "temporary" in error_msg or "rate limit" in error_msg
    return False

@retry_with_exponential_backoff(
    config=RetryConfig(max_attempts=5)
)
def call_my_api(data: dict) -> dict:
    """调用自定义API"""
    # 调用逻辑
    if "error" in data:
        raise MyAPIError("Temporary error, please retry")

    return {"status": "success", "data": data}
```

## 最佳实践

### 1. 选择合适的重试次数

```python
# 不重要或快速失败的场景
RetryConfig(max_attempts=2)

# 一般API调用
RetryConfig(max_attempts=3)

# 重要但不紧急的操作
RetryConfig(max_attempts=5)

# 关键操作（如支付）
RetryConfig(max_attempts=10, max_delay=300.0)
```

### 2. 合理配置延迟

```python
# 快速API（内部服务）
RetryConfig(base_delay=0.5, max_delay=10.0)

# 一般API
RetryConfig(base_delay=1.0, max_delay=60.0)

# 慢速API（外部服务）
RetryConfig(base_delay=2.0, max_delay=300.0)
```

### 3. 使用抖动避免惊群效应

```python
# 推荐配置
RetryConfig(
    jitter=True,       # 启用抖动
    jitter_range=0.1,  # 10%的抖动范围
)
```

### 4. 遵守Retry-After头

```python
# 对限流敏感的场景
RetryConfig(
    respect_retry_after=True,  # 必须遵守服务器的指令
)
```

### 5. 设置合理的超时

```python
import httpx

timeout = httpx.Timeout(
    connect=5.0,   # 连接超时
    read=30.0,     # 读取超时
    write=10.0,    # 写入超时
    pool=5.0,      # 连接池超时
)
```

### 6. 监控和日志

```python
from utils.retry_utils import RetryStatistics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stats = RetryStatistics()

@retry_with_exponential_backoff(stats=stats)
def api_call():
    # ... 调用逻辑
    pass

# 定期检查统计信息
if stats.failed_attempts > stats.successful_attempts:
    logger.warning(f"高失败率: {stats}")
```

### 7. 组合使用限流和重试

```python
# 生产环境推荐配置
async def production_api_call(url: str):
    limiter = RateLimiter(rate=10, per=1.0)

    @aretry_with_exponential_backoff(
        config=RetryConfig(
            max_attempts=5,
            respect_retry_after=True,
        )
    )
    async def call():
        async with limiter:
            async with httpx.AsyncClient() as client:
                return await client.get(url)

    return await call()
```

## API参考

### RetryConfig

重试配置类。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_attempts` | int | 3 | 最大重试次数 |
| `base_delay` | float | 1.0 | 基础延迟（秒） |
| `max_delay` | float | 60.0 | 最大延迟（秒） |
| `exponential_base` | float | 2.0 | 指数退避基数 |
| `jitter` | bool | True | 是否添加抖动 |
| `jitter_range` | float | 0.1 | 抖动范围（0-1） |
| `timeout` | float | None | 请求超时（秒） |
| `respect_retry_after` | bool | True | 遵守Retry-After |
| `retryable_status_codes` | set | (429,500,502,503,504) | 可重试的状态码 |

### RetryStatistics

重试统计类。

| 属性 | 类型 | 说明 |
|------|------|------|
| `total_attempts` | int | 总尝试次数 |
| `successful_attempts` | int | 成功次数 |
| `failed_attempts` | int | 失败次数 |
| `total_delay` | float | 总延迟时间（秒） |
| `errors_by_type` | dict | 按类型分类的错误 |

### RateLimiter

令牌桶限流器。

```python
limiter = RateLimiter(rate=10, per=1.0)  # 每秒10个请求

async with limiter:
    # 执行请求
    pass
```

### 异常类

- `RateLimitError`: 限流错误
- `RetryableError`: 可重试错误基类
- `NetworkError`: 网络错误
- `TimeoutError`: 超时错误
- `ServerError`: 服务器错误（带状态码）

## 测试

运行测试：

```bash
pytest tests/test_retry_utils.py -v
```

## 常见问题

### Q: 如何禁用重试？

A: 将 `max_attempts` 设置为 1：

```python
@retry_with_exponential_backoff(
    config=RetryConfig(max_attempts=1)
)
def no_retry():
    pass
```

### Q: 如何永久禁用某个错误的重试？

A: 自定义重试装饰器，过滤特定错误：

```python
def should_retry(error: Exception) -> bool:
    return not isinstance(error, AuthenticationError)

# 然后在装饰器中使用此函数
```

### Q: 异步和同步版本性能有差异吗？

A: 异步版本在并发场景下性能更好，但单个请求的重试逻辑相同。

### Q: 如何处理认证失败？

A: 认证失败（401）不应重试，应该刷新token后重试：

```python
@retry_with_exponential_backoff(
    config=RetryConfig(max_attempts=3)
)
def fetch_data():
    try:
        return make_request()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            refresh_token()
            return make_request()
        raise
```

## 许可证

MIT License
