# API 重试快速参考

## 快速开始

### 同步版本

```python
from utils.retry_utils import retry_with_exponential_backoff, RetryConfig
import httpx

@retry_with_exponential_backoff()
def fetch_data(url: str) -> dict:
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()

result = fetch_data("https://api.example.com/data")
```

### 异步版本

```python
from utils.retry_utils import aretry_with_exponential_backoff, RetryConfig
import httpx

@aretry_with_exponential_backoff()
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

result = await fetch_data("https://api.example.com/data")
```

## 常用配置

```python
# 默认配置（3次重试，1秒基础延迟）
RetryConfig()

# 快速失败
RetryConfig(max_attempts=2, base_delay=0.5)

# 标准配置
RetryConfig(max_attempts=3, base_delay=1.0, max_delay=60.0)

# 耐心配置
RetryConfig(max_attempts=5, base_delay=2.0, max_delay=120.0)

# 激进配置（处理429）
RetryConfig(max_attempts=10, base_delay=1.0, max_delay=300.0, respect_retry_after=True)

# 禁用抖动（测试用）
RetryConfig(jitter=False)
```

## 使用封装的客户端

```python
from utils.retry_utils import RetryableHTTPClient, AsyncRetryableHTTPClient

# 同步
with RetryableHTTPClient() as client:
    response = client.get("https://api.example.com/data")

# 异步
async with AsyncRetryableHTTPClient() as client:
    response = await client.get("https://api.example.com/data")
```

## 限流器

```python
from utils.retry_utils import RateLimiter

limiter = RateLimiter(rate=10, per=1.0)  # 每秒10个请求

async with limiter:
    await api_call()
```

## 装饰器对比

| 装饰器 | 类型 | 说明 |
|--------|------|------|
| `@retry_with_exponential_backoff()` | 同步 | 自定义实现 |
| `@aretry_with_exponential_backoff()` | 异步 | 自定义实现 |
| `@retry_with_tenacity()` | 同步 | Tenacity库 |

## 可重试的HTTP状态码

- `429` - Too Many Requests
- `500` - Internal Server Error
- `502` - Bad Gateway
- `503` - Service Unavailable
- `504` - Gateway Timeout

## 退避时间计算

```
attempt=0: base_delay * (2^0) = 1.0s
attempt=1: base_delay * (2^1) = 2.0s
attempt=2: base_delay * (2^2) = 4.0s
attempt=3: base_delay * (2^3) = 8.0s
...（直到max_delay）
```

## 完整示例

```python
from utils.retry_utils import (
    RetryConfig,
    RetryStatistics,
    AsyncRetryableHTTPClient,
    RateLimiter,
)
import asyncio

async def main():
    stats = RetryStatistics()

    async with AsyncRetryableHTTPClient(
        config=RetryConfig(max_attempts=5),
        stats=stats,
    ) as client:
        limiter = RateLimiter(rate=10, per=1.0)

        async def fetch(url):
            async with limiter:
                return await client.get(url)

        results = await asyncio.gather(
            *[fetch(f"https://api.example.com/items/{i}") for i in range(100)],
            return_exceptions=True
        )

        print(f"成功: {sum(1 for r in results if not isinstance(r, Exception))}")
        print(f"统计: {stats}")

asyncio.run(main())
```
