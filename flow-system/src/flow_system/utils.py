"""
工具函数模块

提供日志、计时、文件处理等通用功能
"""

import logging
import time
import json
import pickle
import hashlib
from pathlib import Path
from typing import Any, Callable, Optional
from functools import wraps
from datetime import datetime

from .config import Config


# === 日志配置 ===
def setup_logging() -> logging.Logger:
    """配置日志系统"""
    logger = logging.getLogger("flow_system")
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    # 文件处理器
    fh = logging.FileHandler(Config.LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)

    # 控制台处理器
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# 全局logger
logger = setup_logging()


# === 装饰器 ===
def timeit(func: Callable) -> Callable:
    """计时装饰器"""

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        logger.debug(f"{func.__name__} took {elapsed:.2f}s")
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.debug(f"{func.__name__} took {elapsed:.2f}s")
        return result

    # 判断是否为async函数
    import asyncio

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def safe_execute(default_return: Any = None):
    """安全执行装饰器，捕获异常并返回默认值"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{func.__name__} failed: {e}")
                return default_return

        return wrapper

    return decorator


# === 哈希与缓存 ===
def get_hash(content: str) -> str:
    """获取内容的MD5哈希"""
    return hashlib.md5(content.encode()).hexdigest()


def get_cache_key(prompt: str, sys_prompt: str, temp: float) -> str:
    """生成缓存键"""
    # 温度分桶以提高命中率
    bucketed_temp = round(temp * 5) / 5.0
    content = f"{prompt}|{sys_prompt}|{bucketed_temp}"
    return get_hash(content)


# === 文件操作 ===
def save_json(data: dict, filepath: Path) -> None:
    """保存JSON文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.debug(f"Saved JSON to {filepath}")


def load_json(filepath: Path) -> Optional[dict]:
    """加载JSON文件"""
    if not filepath.exists():
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_pickle(data: Any, filepath: Path) -> None:
    """保存Pickle文件"""
    with open(filepath, "wb") as f:
        pickle.dump(data, f)
    logger.debug(f"Saved pickle to {filepath}")


def load_pickle(filepath: Path) -> Optional[Any]:
    """加载Pickle文件"""
    if not filepath.exists():
        return None
    with open(filepath, "rb") as f:
        return pickle.load(f)


# === 代码处理 ===
def clean_code_block(text: str) -> str:
    """清理LLM输出的代码块

    去除markdown代码块标记
    """
    import re

    # 移除```python 或 ``` 标记
    if "```" in text:
        match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()

    return text.strip()


def extract_function_name(code: str) -> Optional[str]:
    """从代码中提取函数名"""
    import ast

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                return node.name
    except:
        pass
    return None


# === 时间格式化 ===
def format_duration(seconds: float) -> str:
    """格式化时间长度"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}min"
    else:
        return f"{seconds/3600:.1f}h"


def get_timestamp() -> str:
    """获取时间戳字符串"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# === 数据统计 ===
def calculate_stats(values: list[float]) -> dict:
    """计算统计指标"""
    import numpy as np

    if not values:
        return {"mean": 0, "std": 0, "min": 0, "max": 0, "median": 0}

    return {
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "median": float(np.median(values)),
    }


# === 进度显示 ===
class ProgressTracker:
    """进度追踪器"""

    def __init__(self, total: int, desc: str = "Processing"):
        self.total = total
        self.current = 0
        self.desc = desc
        self.start_time = time.time()

    def update(self, n: int = 1) -> None:
        """更新进度"""
        self.current += n
        self._print_progress()

    def _print_progress(self) -> None:
        """打印进度条"""
        percent = 100 * self.current / self.total
        elapsed = time.time() - self.start_time
        eta = elapsed / self.current * (self.total - self.current) if self.current > 0 else 0

        bar_length = 30
        filled = int(bar_length * self.current / self.total)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(
            f"\r{self.desc}: [{bar}] {percent:.1f}% | ETA: {format_duration(eta)}",
            end="",
        )

        if self.current >= self.total:
            print()  # 换行


# === 颜色输出 ===
class Colors:
    """终端颜色代码"""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"


def colorize(text: str, color: str) -> str:
    """给文本添加颜色"""
    return f"{color}{text}{Colors.RESET}"


# === 验证函数 ===
def validate_code_syntax(code: str) -> tuple[bool, Optional[str]]:
    """验证代码语法

    Returns:
        (是否有效, 错误信息)
    """
    import ast

    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)


def is_safe_code(code: str) -> tuple[bool, Optional[str]]:
    """检查代码是否安全

    Returns:
        (是否安全, 警告信息)
    """
    import ast

    # 黑名单检查
    for keyword in Config.SANDBOX_BLACKLIST:
        if keyword in code:
            return False, f"Detected blacklisted keyword: {keyword}"

    # AST深度检查
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            # 检查导入
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                else:
                    modules = [node.module] if node.module else []

                for module in modules:
                    base_module = module.split(".")[0] if module else ""
                    if base_module in Config.SANDBOX_BLACKLIST:
                        return False, f"Detected unsafe import: {module}"

            # 检查危险函数调用
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in Config.SANDBOX_BLACKLIST:
                        return False, f"Detected unsafe call: {node.func.id}"

    except:
        return False, "Failed to parse AST"

    return True, None


# === 调试工具 ===
def debug_print(obj: Any, name: str = "Object") -> None:
    """调试打印"""
    if Config.LOG_LEVEL == "DEBUG":
        import pprint

        print(f"\n=== {name} ===")
        pprint.pprint(obj)
        print("=" * (len(name) + 8))
