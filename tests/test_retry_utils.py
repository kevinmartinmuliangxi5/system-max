"""
API 重试工具测试
"""

import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock
import pytest
import httpx

from utils.retry_utils import (
    RetryConfig,
    RetryStatistics,
    RateLimitError,
    ServerError,
    NetworkError,
    retry_with_exponential_backoff,
    aretry_with_exponential_backoff,
    calculate_exponential_backoff,
    is_retryable_error,
    extract_retry_after,
    RateLimiter,
    RetryContext,
)


class TestExponentialBackoff:
    """测试指数退避算法"""

    def test_basic_calculation(self):
        """测试基础计算"""
        delay = calculate_exponential_backoff(0, 1.0, 2.0, 60.0, jitter=False)
        assert delay == 1.0

        delay = calculate_exponential_backoff(1, 1.0, 2.0, 60.0, jitter=False)
        assert delay == 2.0

        delay = calculate_exponential_backoff(2, 1.0, 2.0, 60.0, jitter=False)
        assert delay == 4.0

    def test_max_delay_cap(self):
        """测试最大延迟上限"""
        delay = calculate_exponential_backoff(10, 1.0, 2.0, 60.0, jitter=False)
        assert delay == 60.0

    def test_jitter(self):
        """测试随机抖动"""
        delay1 = calculate_exponential_backoff(1, 1.0, 2.0, 60.0, jitter=True)
        delay2 = calculate_exponential_backoff(1, 1.0, 2.0, 60.0, jitter=True)
        # 抖动应该产生不同的值
        assert delay1 != delay2


class TestRetryableError:
    """测试可重试错误判断"""

    def test_server_error_500(self):
        """测试 500 错误"""
        config = RetryConfig()
        error = ServerError("Internal Server Error", 500)
        assert is_retryable_error(error, config) is True

    def test_server_error_502(self):
        """测试 502 错误"""
        config = RetryConfig()
        error = ServerError("Bad Gateway", 502)
        assert is_retryable_error(error, config) is True

    def test_server_error_429(self):
        """测试 429 错误"""
        config = RetryConfig()
        error = ServerError("Too Many Requests", 429)
        assert is_retryable_error(error, config) is True

    def test_non_retryable_error(self):
        """测试不可重试的错误"""
        config = RetryConfig()
        error = ValueError("Invalid input")
        assert is_retryable_error(error, config) is False


class TestExtractRetryAfter:
    """测试 Retry-After 提取"""

    def test_from_http_status_error(self):
        """测试从 HTTP 状态错误提取"""
        mock_response = Mock()
        mock_response.headers = {"Retry-After": "60"}
        mock_response.status_code = 429

        error = httpx.HTTPStatusError(
            "Too Many Requests",
            request=Mock(),
            response=mock_response
        )

        retry_after = extract_retry_after(error)
        assert retry_after == 60.0

    def test_from_rate_limit_error(self):
        """测试从限流错误提取"""
        error = RateLimitError("Rate limited", retry_after=120.0)
        retry_after = extract_retry_after(error)
        assert retry_after == 120.0

    def test_no_retry_after(self):
        """测试没有 Retry-After 的情况"""
        mock_response = Mock()
        mock_response.headers = {}
        mock_response.status_code = 500

        error = httpx.HTTPStatusError(
            "Internal Server Error",
            request=Mock(),
            response=mock_response
        )

        retry_after = extract_retry_after(error)
        assert retry_after is None


class TestRetryStatistics:
    """测试重试统计"""

    def test_record_success(self):
        """测试记录成功"""
        stats = RetryStatistics()
        stats.record_attempt(True, delay=1.0)

        assert stats.total_attempts == 1
        assert stats.successful_attempts == 1
        assert stats.failed_attempts == 0
        assert stats.total_delay == 1.0

    def test_record_failure(self):
        """测试记录失败"""
        stats = RetryStatistics()
        stats.record_attempt(False, delay=2.0, error_type=ServerError)

        assert stats.total_attempts == 1
        assert stats.successful_attempts == 0
        assert stats.failed_attempts == 1
        assert stats.total_delay == 2.0
        assert stats.errors_by_type.get("ServerError") == 1


class TestRetryDecorator:
    """测试重试装饰器"""

    def test_success_on_first_attempt(self):
        """测试第一次尝试就成功"""
        call_count = 0
        stats = RetryStatistics()

        @retry_with_exponential_backoff(stats=stats)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 1
        assert stats.successful_attempts == 1

    def test_success_after_retry(self):
        """测试重试后成功"""
        call_count = 0
        stats = RetryStatistics()

        @retry_with_exponential_backoff(
            config=RetryConfig(max_attempts=3, base_delay=0.1),
            stats=stats
        )
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ServerError("Temporary error", 503)
            return "success"

        start_time = time.time()
        result = test_func()
        elapsed = time.time() - start_time

        assert result == "success"
        assert call_count == 2
        assert stats.successful_attempts == 1
        assert stats.failed_attempts == 1
        assert elapsed >= 0.1  # 至少延迟了一次

    def test_max_attempts_exceeded(self):
        """测试超过最大尝试次数"""
        call_count = 0
        stats = RetryStatistics()

        @retry_with_exponential_backoff(
            config=RetryConfig(max_attempts=3, base_delay=0.1),
            stats=stats
        )
        def test_func():
            nonlocal call_count
            call_count += 1
            raise ServerError("Persistent error", 503)

        with pytest.raises(ServerError):
            test_func()

        assert call_count == 3
        assert stats.failed_attempts == 3

    def test_non_retryable_error(self):
        """测试不可重试的错误"""
        call_count = 0

        @retry_with_exponential_backoff(
            config=RetryConfig(max_attempts=3)
        )
        def test_func():
            nonlocal call_count
            call_count += 1
            raise ValueError("Invalid input")

        with pytest.raises(ValueError):
            test_func()

        # 不可重试的错误应该立即失败
        assert call_count == 1


class TestAsyncRetryDecorator:
    """测试异步重试装饰器"""

    @pytest.mark.asyncio
    async def test_success_on_first_attempt(self):
        """测试第一次尝试就成功"""
        call_count = 0
        stats = RetryStatistics()

        @aretry_with_exponential_backoff(stats=stats)
        async def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = await test_func()
        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_success_after_retry(self):
        """测试重试后成功"""
        call_count = 0
        stats = RetryStatistics()

        @aretry_with_exponential_backoff(
            config=RetryConfig(max_attempts=3, base_delay=0.1),
            stats=stats
        )
        async def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ServerError("Temporary error", 503)
            return "success"

        start_time = time.time()
        result = await test_func()
        elapsed = time.time() - start_time

        assert result == "success"
        assert call_count == 2
        assert stats.successful_attempts == 1
        assert elapsed >= 0.1

    @pytest.mark.asyncio
    async def test_max_attempts_exceeded(self):
        """测试超过最大尝试次数"""
        call_count = 0
        stats = RetryStatistics()

        @aretry_with_exponential_backoff(
            config=RetryConfig(max_attempts=3, base_delay=0.1),
            stats=stats
        )
        async def test_func():
            nonlocal call_count
            call_count += 1
            raise ServerError("Persistent error", 503)

        with pytest.raises(ServerError):
            await test_func()

        assert call_count == 3


class TestRateLimiter:
    """测试令牌桶限流器"""

    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """测试限流功能"""
        # 每秒 5 个请求
        limiter = RateLimiter(rate=5, per=1.0)

        call_count = 0
        start_time = time.time()

        # 发送 10 个请求
        for _ in range(10):
            await limiter.acquire()
            call_count += 1

        elapsed = time.time() - start_time

        assert call_count == 10
        # 10 个请求以每秒 5 个的速度应该需要约 2 秒
        assert elapsed >= 1.8  # 允许一些误差

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """测试上下文管理器"""
        limiter = RateLimiter(rate=10, per=1.0)

        async with limiter:
            pass  # 正常获取令牌

        assert True  # 如果能到这里，说明正常工作


class TestRetryContext:
    """测试重试上下文管理器"""

    def test_success_on_first_attempt(self):
        """测试第一次尝试就成功"""
        config = RetryConfig(max_attempts=3)

        with RetryContext(config) as retry:
            assert retry.should_continue()
            retry.success("result")
            assert not retry.should_continue()

        assert retry.get_result() == "result"

    def test_success_after_retry(self):
        """测试重试后成功"""
        call_count = 0

        def failing_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ServerError("Temporary error", 503)
            return "result"

        config = RetryConfig(max_attempts=3, base_delay=0.1)

        with RetryContext(config) as retry:
            while retry.should_continue():
                try:
                    result = failing_operation()
                    retry.success(result)
                except Exception as e:
                    retry.error(e)

        assert retry.get_result() == "result"
        assert call_count == 2

    def test_max_attempts_exceeded(self):
        """测试超过最大尝试次数"""
        config = RetryConfig(max_attempts=2, base_delay=0.1)

        with RetryContext(config) as retry:
            while retry.should_continue():
                try:
                    raise ServerError("Persistent error", 503)
                except Exception as e:
                    retry.error(e)

        with pytest.raises(ServerError):
            retry.get_result()


# ============= 集成测试 =============

class TestIntegration:
    """集成测试"""

    def test_full_retry_workflow(self):
        """测试完整的重试工作流"""
        stats = RetryStatistics()
        call_count = 0

        @retry_with_exponential_backoff(
            config=RetryConfig(
                max_attempts=5,
                base_delay=0.1,
                max_delay=5.0,
                jitter=False,  # 禁用抖动以获得确定的结果
            ),
            stats=stats
        )
        def api_call():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ServerError("Service unavailable", 503)
            return {"data": "success"}

        result = api_call()

        assert result == {"data": "success"}
        assert call_count == 3
        assert stats.total_attempts == 3
        assert stats.successful_attempts == 1
        assert stats.failed_attempts == 2

        # 验证延迟时间
        # 第1次失败后: 0.1秒
        # 第2次失败后: 0.2秒
        # 总延迟: 0.3秒左右
        assert 0.25 <= stats.total_delay <= 0.5

    @pytest.mark.asyncio
    async def test_async_full_retry_workflow(self):
        """测试完整的异步重试工作流"""
        stats = RetryStatistics()
        call_count = 0

        @aretry_with_exponential_backoff(
            config=RetryConfig(
                max_attempts=5,
                base_delay=0.1,
                max_delay=5.0,
                jitter=False,
            ),
            stats=stats
        )
        async def api_call():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ServerError("Service unavailable", 503)
            return {"data": "success"}

        result = await api_call()

        assert result == {"data": "success"}
        assert call_count == 3
        assert stats.total_attempts == 3
        assert stats.successful_attempts == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
