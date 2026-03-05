"""
API调用重试工具包
提供指数退避、tenacity封装、自定义装饰器、异步重试、限流处理等功能
"""

import asyncio
import functools
import logging
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Awaitable,
    Callable,
    Optional,
    TypeVar,
    Union,
)

import httpx

try:
    from tenacity import (
        retry,
        retry_if_exception_type,
        stop_after_attempt,
        wait_exponential,
        before_sleep_log,
        after_log,
    )
    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False

logger = logging.getLogger(__name__)

T = TypeVar("T")
F = TypeVar("F", bound=Union[Callable[..., T], Callable[..., Awaitable[T]]])


class RateLimitError(Exception):
    """限流错误 (HTTP 429)"""
    def __init__(self, message: str, retry_after: Optional[float] = None):
        super().__init__(message)
        self.retry_after = retry_after


class ErrorCode(Enum):
    """错误代码枚举"""
    NETWORK_ERROR = "NETWORK_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    RATE_LIMIT_ERROR = "RATE_LIMIT_ERROR"
    SERVER_ERROR = "SERVER_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


@dataclass
class RetryConfig:
    """重试配置"""
    max_attempts: int = 3  # 最大重试次数
    base_delay: float = 1.0  # 基础延迟（秒）
    max_delay: float = 60.0  # 最大延迟（秒）
    exponential_base: float = 2.0  # 指数退避的基数
    jitter: bool = True  # 是否添加随机抖动
    jitter_range: float = 0.1  # 抖动范围（0-1之间）
    timeout: Optional[float] = None  # 请求超时时间（秒）
    respect_retry_after: bool = True  # 是否遵守服务器返回的 Retry-After 头

    # 可重试的HTTP状态码
    retryable_status_codes: set = (
        429,  # Too Many Requests
        500,  # Internal Server Error
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
    )


class RetryableError(Exception):
    """可重试的错误基类"""
    pass


class NetworkError(RetryableError):
    """网络错误"""
    pass


class TimeoutError(RetryableError):
    """超时错误"""
    pass


class ServerError(RetryableError):
    """服务器错误"""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


def calculate_exponential_backoff(
    attempt: int,
    base_delay: float,
    exponential_base: float,
    max_delay: float,
    jitter: bool = True,
    jitter_range: float = 0.1,
) -> float:
    """
    计算指数退避延迟时间

    Args:
        attempt: 当前重试次数（从0开始）
        base_delay: 基础延迟时间
        exponential_base: 指数基数
        max_delay: 最大延迟时间
        jitter: 是否添加随机抖动
        jitter_range: 抖动范围（0-1之间）

    Returns:
        计算后的延迟时间（秒）

    Example:
        >>> calculate_exponential_backoff(0, 1.0, 2.0, 60.0)
        1.0
        >>> calculate_exponential_backoff(1, 1.0, 2.0, 60.0)
        2.0
        >>> calculate_exponential_backoff(2, 1.0, 2.0, 60.0)
        4.0
    """
    delay = min(base_delay * (exponential_base ** attempt), max_delay)

    if jitter:
        # 添加抖动以避免"惊群效应"
        jitter_amount = delay * jitter_range
        delay = delay + random.uniform(-jitter_amount, jitter_amount)

    return max(0, delay)


def is_retryable_error(error: Exception, config: RetryConfig) -> bool:
    """
    判断错误是否可重试

    Args:
        error: 捕获的异常
        config: 重试配置

    Returns:
        是否可重试
    """
    # 网络相关错误
    if isinstance(error, (NetworkError, RetryableError)):
        return True

    # HTTP状态码错误
    if isinstance(error, ServerError):
        return error.status_code in config.retryable_status_codes

    # httpx 异常
    if isinstance(error, httpx.HTTPStatusError):
        return error.response.status_code in config.retryable_status_codes

    if isinstance(error, httpx.NetworkError):
        return True

    if isinstance(error, httpx.TimeoutException):
        return True

    return False


def extract_retry_after(error: Exception) -> Optional[float]:
    """
    从错误中提取 Retry-After 时间

    Args:
        error: 捕获的异常

    Returns:
        重试时间（秒），如果没有则返回 None
    """
    if isinstance(error, httpx.HTTPStatusError):
        response = error.response
        retry_after = response.headers.get("Retry-After")

        if retry_after:
            try:
                # Retry-After 可能是秒数或 HTTP-date
                return float(retry_after)
            except ValueError:
                pass

    if isinstance(error, RateLimitError):
        return error.retry_after

    return None


class RetryStatistics:
    """重试统计信息"""

    def __init__(self):
        self.total_attempts = 0
        self.successful_attempts = 0
        self.failed_attempts = 0
        self.total_delay = 0.0
        self.errors_by_type = {}

    def record_attempt(self, success: bool, delay: float = 0.0, error_type: Optional[type] = None):
        """记录一次尝试"""
        self.total_attempts += 1
        self.total_delay += delay

        if success:
            self.successful_attempts += 1
        else:
            self.failed_attempts += 1
            if error_type:
                error_name = error_type.__name__
                self.errors_by_type[error_name] = self.errors_by_type.get(error_name, 0) + 1

    def __repr__(self) -> str:
        return (
            f"RetryStatistics("
            f"total={self.total_attempts}, "
            f"success={self.successful_attempts}, "
            f"failed={self.failed_attempts}, "
            f"total_delay={self.total_delay:.2f}s)"
        )


def retry_with_exponential_backoff(
    config: Optional[RetryConfig] = None,
    stats: Optional[RetryStatistics] = None,
) -> Callable:
    """
    指数退避重试装饰器（同步版本）

    Args:
        config: 重试配置
        stats: 重试统计对象

    Returns:
        装饰器函数

    Example:
        >>> @retry_with_exponential_backoff()
        ... def fetch_data(url):
        ...     return requests.get(url)

        >>> @retry_with_exponential_backoff(
        ...     config=RetryConfig(max_attempts=5, base_delay=2.0)
        ... )
        ... def fetch_data(url):
        ...     return requests.get(url)
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error = None

            for attempt in range(config.max_attempts):
                try:
                    result = func(*args, **kwargs)
                    if stats:
                        stats.record_attempt(True)
                    return result

                except Exception as e:
                    last_error = e

                    if not is_retryable_error(e, config):
                        logger.error(f"Non-retryable error: {e}")
                        raise

                    if attempt < config.max_attempts - 1:
                        # 检查是否有 Retry-After 头
                        if config.respect_retry_after:
                            retry_after = extract_retry_after(e)
                            if retry_after is not None:
                                delay = min(retry_after, config.max_delay)
                                logger.warning(
                                    f"Rate limited, retrying after {delay:.2f}s "
                                    f"(attempt {attempt + 1}/{config.max_attempts})"
                                )
                                time.sleep(delay)
                                if stats:
                                    stats.record_attempt(False, delay, type(e))
                                continue

                        # 计算退避延迟
                        delay = calculate_exponential_backoff(
                            attempt,
                            config.base_delay,
                            config.exponential_base,
                            config.max_delay,
                            config.jitter,
                            config.jitter_range,
                        )

                        logger.warning(
                            f"Attempt {attempt + 1}/{config.max_attempts} failed: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        time.sleep(delay)
                        if stats:
                            stats.record_attempt(False, delay, type(e))
                    else:
                        logger.error(f"All {config.max_attempts} attempts failed")

            # 所有重试都失败
            if stats:
                stats.record_attempt(False, error_type=type(last_error))
            raise last_error

        return wrapper

    return decorator


def aretry_with_exponential_backoff(
    config: Optional[RetryConfig] = None,
    stats: Optional[RetryStatistics] = None,
) -> Callable:
    """
    指数退避重试装饰器（异步版本）

    Args:
        config: 重试配置
        stats: 重试统计对象

    Returns:
        异步装饰器函数

    Example:
        >>> @aretry_with_exponential_backoff()
        ... async def fetch_data(url):
        ...     async with httpx.AsyncClient() as client:
        ...         return await client.get(url)
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_error = None

            for attempt in range(config.max_attempts):
                try:
                    result = await func(*args, **kwargs)
                    if stats:
                        stats.record_attempt(True)
                    return result

                except Exception as e:
                    last_error = e

                    if not is_retryable_error(e, config):
                        logger.error(f"Non-retryable error: {e}")
                        raise

                    if attempt < config.max_attempts - 1:
                        # 检查是否有 Retry-After 头
                        if config.respect_retry_after:
                            retry_after = extract_retry_after(e)
                            if retry_after is not None:
                                delay = min(retry_after, config.max_delay)
                                logger.warning(
                                    f"Rate limited, retrying after {delay:.2f}s "
                                    f"(attempt {attempt + 1}/{config.max_attempts})"
                                )
                                await asyncio.sleep(delay)
                                if stats:
                                    stats.record_attempt(False, delay, type(e))
                                continue

                        # 计算退避延迟
                        delay = calculate_exponential_backoff(
                            attempt,
                            config.base_delay,
                            config.exponential_base,
                            config.max_delay,
                            config.jitter,
                            config.jitter_range,
                        )

                        logger.warning(
                            f"Attempt {attempt + 1}/{config.max_attempts} failed: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        await asyncio.sleep(delay)
                        if stats:
                            stats.record_attempt(False, delay, type(e))
                    else:
                        logger.error(f"All {config.max_attempts} attempts failed")

            # 所有重试都失败
            if stats:
                stats.record_attempt(False, error_type=type(last_error))
            raise last_error

        return async_wrapper

    return decorator


# ============= Tenacity 封装 =============

if TENACITY_AVAILABLE:

    def create_tenacity_retry(
        max_attempts: int = 3,
        wait_min: float = 1.0,
        wait_max: float = 60.0,
        wait_multiplier: float = 2.0,
        retryable_exceptions: tuple = (
            httpx.NetworkError,
            httpx.TimeoutException,
            httpx.HTTPStatusError,
            RetryableError,
        ),
    ) -> Callable:
        """
        使用 tenacity 创建重试装饰器

        Args:
            max_attempts: 最大重试次数
            wait_min: 最小等待时间
            wait_max: 最大等待时间
            wait_multiplier: 指数乘数
            retryable_exceptions: 可重试的异常类型

        Returns:
            tenacity 重试装饰器

        Example:
            >>> @create_tenacity_retry(max_attempts=5)
            ... def fetch_data(url):
            ...     return requests.get(url)
        """

        def is_retryable_http_error(exception: Exception) -> bool:
            """判断 HTTP 错误是否可重试"""
            if isinstance(exception, httpx.HTTPStatusError):
                return exception.response.status_code in (429, 500, 502, 503, 504)
            return True

        return retry(
            reraise=True,
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=wait_multiplier, min=wait_min, max=wait_max),
            retry=retry_if_exception_type(retryable_exceptions) & retry_if_exception_type(
                lambda e: is_retryable_http_error(e) if isinstance(e, httpx.HTTPStatusError) else True
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            after=after_log(logger, logging.INFO),
        )

    def retry_with_tenacity(
        max_attempts: int = 3,
        wait_min: float = 1.0,
        wait_max: float = 60.0,
        wait_multiplier: float = 2.0,
    ) -> Callable:
        """
        tenacity 重试装饰器（简化版）

        Example:
            >>> @retry_with_tenacity(max_attempts=5)
            ... def fetch_data(url):
            ...     return requests.get(url)
        """
        return create_tenacity_retry(
            max_attempts=max_attempts,
            wait_min=wait_min,
            wait_max=wait_max,
            wait_multiplier=wait_multiplier,
        )


# ============= HTTP 客户端封装 =============

class RetryableHTTPClient:
    """
    支持重试的 HTTP 客户端（同步版本）

    Example:
        >>> client = RetryableHTTPClient(
        ...     config=RetryConfig(max_attempts=5)
        ... )
        >>> response = client.get("https://api.example.com/data")
    """

    def __init__(
        self,
        config: Optional[RetryConfig] = None,
        stats: Optional[RetryStatistics] = None,
        timeout: Optional[float] = 30.0,
    ):
        self.config = config or RetryConfig()
        self.stats = stats or RetryStatistics()
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def get(self, url: str, **kwargs) -> httpx.Response:
        """GET 请求"""
        return self._retry_request(lambda: self._client.get(url, **kwargs))

    def post(self, url: str, **kwargs) -> httpx.Response:
        """POST 请求"""
        return self._retry_request(lambda: self._client.post(url, **kwargs))

    def put(self, url: str, **kwargs) -> httpx.Response:
        """PUT 请求"""
        return self._retry_request(lambda: self._client.put(url, **kwargs))

    def delete(self, url: str, **kwargs) -> httpx.Response:
        """DELETE 请求"""
        return self._retry_request(lambda: self._client.delete(url, **kwargs))

    def _retry_request(self, request_func: Callable) -> httpx.Response:
        """执行带重试的请求"""
        last_error = None

        for attempt in range(self.config.max_attempts):
            try:
                response = request_func()
                self._check_response(response)
                if self.stats:
                    self.stats.record_attempt(True)
                return response

            except Exception as e:
                last_error = e

                if not is_retryable_error(e, self.config):
                    logger.error(f"Non-retryable error: {e}")
                    raise

                if attempt < self.config.max_attempts - 1:
                    # 检查是否有 Retry-After 头
                    if self.config.respect_retry_after:
                        retry_after = extract_retry_after(e)
                        if retry_after is not None:
                            delay = min(retry_after, self.config.max_delay)
                            logger.warning(
                                f"Rate limited, retrying after {delay:.2f}s "
                                f"(attempt {attempt + 1}/{self.config.max_attempts})"
                            )
                            time.sleep(delay)
                            if self.stats:
                                self.stats.record_attempt(False, delay, type(e))
                            continue

                    # 计算退避延迟
                    delay = calculate_exponential_backoff(
                        attempt,
                        self.config.base_delay,
                        self.config.exponential_base,
                        self.config.max_delay,
                        self.config.jitter,
                        self.config.jitter_range,
                    )

                    logger.warning(
                        f"Attempt {attempt + 1}/{self.config.max_attempts} failed: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)
                    if self.stats:
                        self.stats.record_attempt(False, delay, type(e))
                else:
                    logger.error(f"All {self.config.max_attempts} attempts failed")

        # 所有重试都失败
        if self.stats:
            self.stats.record_attempt(False, error_type=type(last_error))
        raise last_error

    def _check_response(self, response: httpx.Response):
        """检查响应状态"""
        if response.status_code in self.config.retryable_status_codes:
            raise ServerError(
                f"HTTP {response.status_code}: {response.text}",
                status_code=response.status_code,
            )
        response.raise_for_status()

    def get_statistics(self) -> RetryStatistics:
        """获取统计信息"""
        return self.stats

    def close(self):
        """关闭客户端"""
        self._client.close()


class AsyncRetryableHTTPClient:
    """
    支持重试的 HTTP 客户端（异步版本）

    Example:
        >>> async with AsyncRetryableHTTPClient(
        ...     config=RetryConfig(max_attempts=5)
        ... ) as client:
        ...     response = await client.get("https://api.example.com/data")
    """

    def __init__(
        self,
        config: Optional[RetryConfig] = None,
        stats: Optional[RetryStatistics] = None,
        timeout: Optional[float] = 30.0,
    ):
        self.config = config or RetryConfig()
        self.stats = stats or RetryStatistics()
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """GET 请求"""
        return await self._retry_request(lambda: self._client.get(url, **kwargs))

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """POST 请求"""
        return await self._retry_request(lambda: self._client.post(url, **kwargs))

    async def put(self, url: str, **kwargs) -> httpx.Response:
        """PUT 请求"""
        return await self._retry_request(lambda: self._client.put(url, **kwargs))

    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """DELETE 请求"""
        return await self._retry_request(lambda: self._client.delete(url, **kwargs))

    async def _retry_request(self, request_func: Callable) -> httpx.Response:
        """执行带重试的请求"""
        last_error = None

        for attempt in range(self.config.max_attempts):
            try:
                response = await request_func()
                self._check_response(response)
                if self.stats:
                    self.stats.record_attempt(True)
                return response

            except Exception as e:
                last_error = e

                if not is_retryable_error(e, self.config):
                    logger.error(f"Non-retryable error: {e}")
                    raise

                if attempt < self.config.max_attempts - 1:
                    # 检查是否有 Retry-After 头
                    if self.config.respect_retry_after:
                        retry_after = extract_retry_after(e)
                        if retry_after is not None:
                            delay = min(retry_after, self.config.max_delay)
                            logger.warning(
                                f"Rate limited, retrying after {delay:.2f}s "
                                f"(attempt {attempt + 1}/{self.config.max_attempts})"
                            )
                            await asyncio.sleep(delay)
                            if self.stats:
                                self.stats.record_attempt(False, delay, type(e))
                            continue

                    # 计算退避延迟
                    delay = calculate_exponential_backoff(
                        attempt,
                        self.config.base_delay,
                        self.config.exponential_base,
                        self.config.max_delay,
                        self.config.jitter,
                        self.config.jitter_range,
                    )

                    logger.warning(
                        f"Attempt {attempt + 1}/{self.config.max_attempts} failed: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    await asyncio.sleep(delay)
                    if self.stats:
                        self.stats.record_attempt(False, delay, type(e))
                else:
                    logger.error(f"All {self.config.max_attempts} attempts failed")

        # 所有重试都失败
        if self.stats:
            self.stats.record_attempt(False, error_type=type(last_error))
        raise last_error

    def _check_response(self, response: httpx.Response):
        """检查响应状态"""
        if response.status_code in self.config.retryable_status_codes:
            raise ServerError(
                f"HTTP {response.status_code}: {response.text}",
                status_code=response.status_code,
            )
        response.raise_for_status()

    def get_statistics(self) -> RetryStatistics:
        """获取统计信息"""
        return self.stats

    async def close(self):
        """关闭客户端"""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# ============= 限流处理器 =============

class RateLimiter:
    """
    令牌桶限流器

    Example:
        >>> limiter = RateLimiter(rate=10, per=1.0)  # 每秒10个请求
        >>> async with limiter:
        ...     await api_call()
    """

    def __init__(self, rate: int, per: float = 1.0):
        """
        Args:
            rate: 令牌数量
            per: 时间周期（秒）
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
        self._lock = asyncio.Lock()

    def _update_allowance(self):
        """更新令牌数量"""
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current
        self.allowance += time_passed * (self.rate / self.per)

        if self.allowance > self.rate:
            self.allowance = self.rate

    async def acquire(self):
        """获取令牌"""
        async with self._lock:
            self._update_allowance()

            if self.allowance < 1.0:
                # 计算需要等待的时间
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                await asyncio.sleep(sleep_time)
                self._update_allowance()

            self.allowance -= 1.0

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


# ============= 上下文管理器 =============

class RetryContext:
    """
    重试上下文管理器（用于代码块级别的重试）

    Example:
        >>> config = RetryConfig(max_attempts=3)
        >>> with RetryContext(config) as retry:
        ...     while retry.should_continue():
        ...         try:
        ...             result = api_call()
        ...             retry.success(result)
        ...             break
        ...         except Exception as e:
        ...             retry.error(e)
    """

    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
        self._attempt = 0
        self._success = False
        self._result = None
        self._last_error = None

    def should_continue(self) -> bool:
        """是否应该继续重试"""
        return self._attempt < self.config.max_attempts and not self._success

    def success(self, result: Any):
        """标记成功"""
        self._success = True
        self._result = result

    def error(self, error: Exception):
        """记录错误"""
        self._last_error = error
        self._attempt += 1

        if not self._success and self._attempt < self.config.max_attempts:
            if is_retryable_error(error, self.config):
                delay = calculate_exponential_backoff(
                    self._attempt - 1,
                    self.config.base_delay,
                    self.config.exponential_base,
                    self.config.max_delay,
                    self.config.jitter,
                    self.config.jitter_range,
                )

                logger.warning(
                    f"Attempt {self._attempt}/{self.config.max_attempts} failed: {error}. "
                    f"Retrying in {delay:.2f}s..."
                )
                time.sleep(delay)
            else:
                raise

    def get_result(self) -> Any:
        """获取结果"""
        if self._success:
            return self._result
        raise self._last_error or RuntimeError("No result available")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


__all__ = [
    # 配置
    "RetryConfig",
    "RetryStatistics",
    # 异常
    "RateLimitError",
    "RetryableError",
    "NetworkError",
    "TimeoutError",
    "ServerError",
    "ErrorCode",
    # 装饰器
    "retry_with_exponential_backoff",
    "aretry_with_exponential_backoff",
    # Tenacity
    "create_tenacity_retry",
    "retry_with_tenacity",
    "TENACITY_AVAILABLE",
    # 客户端
    "RetryableHTTPClient",
    "AsyncRetryableHTTPClient",
    # 限流
    "RateLimiter",
    # 上下文管理器
    "RetryContext",
    # 工具函数
    "calculate_exponential_backoff",
    "is_retryable_error",
    "extract_retry_after",
]
