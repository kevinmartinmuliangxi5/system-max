"""
API 重试工具使用示例
展示各种重试模式的实际应用
"""

import asyncio
import logging
from typing import Any

import httpx

from utils.retry_utils import (
    # 配置
    RetryConfig,
    RetryStatistics,
    # 异常
    RateLimitError,
    NetworkError,
    ServerError,
    # 装饰器
    retry_with_exponential_backoff,
    aretry_with_exponential_backoff,
    # Tenacity
    retry_with_tenacity,
    TENACITY_AVAILABLE,
    # 客户端
    RetryableHTTPClient,
    AsyncRetryableHTTPClient,
    # 限流
    RateLimiter,
    # 上下文管理器
    RetryContext,
    # 工具函数
    calculate_exponential_backoff,
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============= 示例 1: 基础指数退避重试 =============

@retry_with_exponential_backoff(
    config=RetryConfig(max_attempts=3, base_delay=1.0)
)
def fetch_user_data(user_id: int) -> dict:
    """
    获取用户数据（同步版本）
    自动重试：500, 502, 503, 504, 429 错误
    """
    url = f"https://api.example.com/users/{user_id}"

    with httpx.Client(timeout=10.0) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


# ============= 示例 2: 使用统计信息 =============

stats = RetryStatistics()


@retry_with_exponential_backoff(
    config=RetryConfig(max_attempts=5, base_delay=2.0, max_delay=30.0),
    stats=stats,
)
def fetch_with_stats(url: str) -> dict:
    """
    带统计信息的API调用
    """
    with httpx.Client(timeout=10.0) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def demo_with_stats():
    """演示统计信息的使用"""
    try:
        result = fetch_with_stats("https://api.example.com/data")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed: {e}")

    print(f"Statistics: {stats}")
    print(f"Success rate: {stats.successful_attempts / stats.total_attempts * 100:.1f}%")


# ============= 示例 3: 异步重试 =============

@aretry_with_exponential_backoff(
    config=RetryConfig(max_attempts=3, base_delay=1.0)
)
async def async_fetch_data(url: str) -> dict:
    """
    获取数据（异步版本）
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def demo_async_retry():
    """演示异步重试"""
    urls = [
        "https://api.example.com/data1",
        "https://api.example.com/data2",
        "https://api.example.com/data3",
    ]

    # 并发请求，每个都有独立的重试逻辑
    tasks = [async_fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"URL {i+1} failed: {result}")
        else:
            print(f"URL {i+1} succeeded: {result}")


# ============= 示例 4: 使用 Tenacity =============

if TENACITY_AVAILABLE:
    @retry_with_tenacity(max_attempts=5, wait_min=1.0, wait_max=30.0)
    def fetch_with_tenacity(url: str) -> dict:
        """
        使用 tenacity 库的重试装饰器
        """
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()


# ============= 示例 5: 自定义重试条件 =============

class MyAPIError(Exception):
    """自定义API错误"""
    pass


def is_my_api_error_retryable(error: Exception) -> bool:
    """判断自定义错误是否可重试"""
    if isinstance(error, MyAPIError):
        # 根据错误消息判断
        return "temporary" in str(error).lower() or "rate limit" in str(error).lower()
    return False


def my_retry_decorator(max_attempts: int = 3):
    """自定义重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except MyAPIError as e:
                    last_error = e
                    if not is_my_api_error_retryable(e):
                        raise

                    if attempt < max_attempts - 1:
                        delay = calculate_exponential_backoff(attempt, 1.0, 2.0, 60.0)
                        print(f"Retrying in {delay:.2f}s...")
                        import time
                        time.sleep(delay)

            raise last_error

        return wrapper
    return decorator


@my_retry_decorator(max_attempts=5)
def call_my_api(data: dict) -> dict:
    """
    调用自定义API
    """
    # 实际调用逻辑
    if "error" in data:
        raise MyAPIError("Temporary error, please retry")

    return {"status": "success", "data": data}


# ============= 示例 6: 处理 429 限流错误 =============

@retry_with_exponential_backoff(
    config=RetryConfig(
        max_attempts=10,  # 429 错误可能需要更多重试
        base_delay=1.0,
        max_delay=120.0,  # 最大延迟更长
        respect_retry_after=True,  # 遵守服务器返回的 Retry-After
    )
)
def fetch_with_rate_limit_handling(url: str) -> dict:
    """
    处理限流的API调用
    自动遵守服务器返回的 Retry-After 头
    """
    with httpx.Client(timeout=10.0) as client:
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


# ============= 示例 7: 使用 HTTP 客户端封装 =============

def demo_http_client():
    """演示使用封装的 HTTP 客户端"""
    stats = RetryStatistics()

    with RetryableHTTPClient(
        config=RetryConfig(max_attempts=3, base_delay=2.0),
        stats=stats,
        timeout=30.0,
    ) as client:
        # 所有请求都会自动重试
        response1 = client.get("https://api.example.com/data1")
        response2 = client.post("https://api.example.com/data2", json={"key": "value"})

        print(f"Responses: {response1.json()}, {response2.json()}")

    print(f"Client statistics: {stats}")


async def demo_async_http_client():
    """演示使用异步 HTTP 客户端"""
    stats = RetryStatistics()

    async with AsyncRetryableHTTPClient(
        config=RetryConfig(max_attempts=3, base_delay=2.0),
        stats=stats,
        timeout=30.0,
    ) as client:
        # 并发请求
        responses = await asyncio.gather(
            client.get("https://api.example.com/data1"),
            client.get("https://api.example.com/data2"),
            client.get("https://api.example.com/data3"),
        )

        for response in responses:
            print(f"Response: {response.json()}")

    print(f"Async client statistics: {stats}")


# ============= 示例 8: 使用限流器 =============

async def demo_rate_limiter():
    """
    演示令牌桶限流器
    确保不超过API的速率限制
    """
    # 创建限流器：每秒最多 5 个请求
    limiter = RateLimiter(rate=5, per=1.0)

    async def fetch_item(item_id: int):
        async with limiter:  # 自动限流
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.example.com/items/{item_id}"
                )
                return response.json()

    # 即使并发执行，也会遵守速率限制
    tasks = [fetch_item(i) for i in range(20)]
    results = await asyncio.gather(*tasks)

    print(f"Fetched {len(results)} items with rate limiting")


# ============= 示例 9: 使用上下文管理器 =============

def demo_context_manager():
    """演示使用上下文管理器进行代码块级别的重试"""
    config = RetryConfig(max_attempts=3, base_delay=1.0)

    with RetryContext(config) as retry:
        while retry.should_continue():
            try:
                # 复杂的API调用逻辑
                result = complex_api_operation()
                retry.success(result)
                break
            except Exception as e:
                retry.error(e)

    print(f"Result: {retry.get_result()}")


def complex_api_operation() -> dict:
    """复杂的API操作"""
    # 多步骤操作
    with httpx.Client() as client:
        # 步骤 1: 获取 token
        token_response = client.post("https://api.example.com/auth")
        token = token_response.json()["token"]

        # 步骤 2: 使用 token 获取数据
        data_response = client.get(
            "https://api.example.com/data",
            headers={"Authorization": f"Bearer {token}"}
        )

        return data_response.json()


# ============= 示例 10: 组合使用重试和限流 =============

async def demo_combined_retry_and_rate_limit():
    """
    组合使用重试和限流
    这是生产环境推荐的配置
    """
    stats = RetryStatistics()

    # 创建带重试和限流的客户端
    async with AsyncRetryableHTTPClient(
        config=RetryConfig(
            max_attempts=5,  # 每个请求最多重试5次
            base_delay=1.0,
            max_delay=60.0,
            respect_retry_after=True,
        ),
        stats=stats,
        timeout=30.0,
    ) as client:
        # 创建限流器：每秒 10 个请求
        limiter = RateLimiter(rate=10, per=1.0)

        async def fetch_data(url: str):
            # 组合限流和重试
            async with limiter:
                response = await client.get(url)
                return response.json()

        # 批量获取数据
        urls = [f"https://api.example.com/items/{i}" for i in range(100)]
        results = await asyncio.gather(
            *[fetch_data(url) for url in urls],
            return_exceptions=True
        )

        success_count = sum(1 for r in results if not isinstance(r, Exception))
        print(f"Successfully fetched {success_count}/{len(urls)} items")
        print(f"Statistics: {stats}")


# ============= 示例 11: 自定义超时配置 =============

def demo_custom_timeout():
    """
    演示自定义超时配置
    包括连接超时和读取超时
    """
    timeout_config = httpx.Timeout(
        connect=5.0,  # 连接超时
        read=30.0,  # 读取超时
        write=10.0,  # 写入超时
        pool=5.0,  # 连接池超时
    )

    @retry_with_exponential_backoff(
        config=RetryConfig(max_attempts=3)
    )
    def fetch_with_custom_timeout(url: str):
        """使用自定义超时的请求"""
        with httpx.Client(timeout=timeout_config) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    return fetch_with_custom_timeout("https://api.example.com/data")


# ============= 示例 12: 错误处理和回退策略 =============

class CircuitBreakerOpenError(Exception):
    """熔断器开启错误"""
    pass


class CircuitBreaker:
    """
    熔断器模式
    当错误率超过阈值时，暂时停止请求
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_attempts: int = 1,
    ):
        """
        Args:
            failure_threshold: 失败阈值
            timeout: 熔断器开启后的超时时间
            half_open_attempts: 半开状态的尝试次数
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.half_open_attempts = half_open_attempts

        self._failure_count = 0
        self._last_failure_time = 0
        self._state = "closed"  # closed, open, half_open
        self._half_open_count = 0

    def call(self, func: Callable, *args, **kwargs):
        """通过熔断器调用函数"""
        if self._is_open():
            raise CircuitBreakerOpenError("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _is_open(self) -> bool:
        """判断熔断器是否开启"""
        if self._state == "open":
            if time.time() - self._last_failure_time > self.timeout:
                self._state = "half_open"
                self._half_open_count = 0
                return False
            return True
        return False

    def _on_success(self):
        """成功时的处理"""
        self._failure_count = 0
        if self._state == "half_open":
            self._half_open_count += 1
            if self._half_open_count >= self.half_open_attempts:
                self._state = "closed"

    def _on_failure(self):
        """失败时的处理"""
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._failure_count >= self.failure_threshold:
            self._state = "open"


import time


def demo_circuit_breaker():
    """演示熔断器模式"""
    circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=10.0)

    @retry_with_exponential_backoff(
        config=RetryConfig(max_attempts=2)
    )
    def risky_api_call() -> dict:
        """可能失败的API调用"""
        # 模拟失败的API
        raise ServerError("Service unavailable", status_code=503)

    # 尝试多次调用
    for i in range(10):
        try:
            result = circuit_breaker.call(risky_api_call)
            print(f"Call {i+1}: Success")
        except CircuitBreakerOpenError:
            print(f"Call {i+1}: Circuit breaker is open, skipping")
            time.sleep(1)
        except Exception as e:
            print(f"Call {i+1}: Failed - {e}")


if __name__ == "__main__":
    # 运行各种示例
    print("=== Demo 1: Basic exponential backoff ===")
    try:
        fetch_user_data(123)
    except Exception as e:
        print(f"Error: {e}")

    print("\n=== Demo 2: With statistics ===")
    demo_with_stats()

    print("\n=== Demo 3: Async retry ===")
    asyncio.run(demo_async_retry())

    print("\n=== Demo 5: Custom retry condition ===")
    call_my_api({"key": "value"})

    print("\n=== Demo 7: HTTP client wrapper ===")
    demo_http_client()

    print("\n=== Demo 8: Rate limiter ===")
    asyncio.run(demo_rate_limiter())

    print("\n=== Demo 10: Combined retry and rate limit ===")
    asyncio.run(demo_combined_retry_and_rate_limit())

    print("\n=== Demo 12: Circuit breaker ===")
    demo_circuit_breaker()
