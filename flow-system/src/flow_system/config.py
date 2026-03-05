"""
配置管理模块

负责加载环境变量、管理系统配置、提供跨平台路径处理
"""

import os
import platform
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


class Config:
    """全局配置类"""

    # === 项目路径 ===
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    CHECKPOINTS_DIR = BASE_DIR / "checkpoints"

    # === GLM API配置 (OpenAI协议) ===
    API_KEY = os.getenv("ZHIPUAI_API_KEY")
    # GLM Coding Plan专属端点
    BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4")
    # 模型配置
    MODEL_NAME = os.getenv("MODEL_NAME", "GLM-4.7")  # GLM Coding Plan默认模型
    EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI协议的embedding模型

    # === 系统配置 ===
    PLATFORM = platform.system()  # Windows, Darwin, Linux
    CPU_COUNT = os.cpu_count() or 4
    MAX_WORKERS = (
        CPU_COUNT - 1
        if os.getenv("MAX_WORKERS", "auto") == "auto"
        else int(os.getenv("MAX_WORKERS", CPU_COUNT - 1))
    )

    # === 日志配置 ===
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "flow_system.log"

    # === 演化参数 ===
    POPULATION_SIZE = int(os.getenv("POPULATION_SIZE", "8"))
    MAX_GENERATIONS = int(os.getenv("MAX_GENERATIONS", "20"))
    INITIAL_MUTATION_RATE = float(os.getenv("INITIAL_MUTATION_RATE", "0.3"))
    EARLY_STOP_PATIENCE = int(os.getenv("EARLY_STOP_PATIENCE", "3"))

    # === 缓存配置 ===
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_DB_PATH = DATA_DIR / "cache.db"

    # === 知识库配置 ===
    ENABLE_KNOWLEDGE = os.getenv("ENABLE_KNOWLEDGE", "true").lower() == "true"
    KNOWLEDGE_DB_PATH = DATA_DIR / "knowledge.db"
    FAISS_INDEX_PATH = DATA_DIR / "faiss_index"
    PATTERN_THRESHOLD = float(os.getenv("PATTERN_THRESHOLD", "0.9"))

    # === 真涌现配置 ===
    ENABLE_DOWNWARD_CAUSATION = (
        os.getenv("ENABLE_DOWNWARD_CAUSATION", "true").lower() == "true"
    )
    LYAPUNOV_THRESHOLD = float(os.getenv("LYAPUNOV_THRESHOLD", "-0.1"))
    EFFECTIVE_INFO_THRESHOLD = float(os.getenv("EFFECTIVE_INFO_THRESHOLD", "0.5"))

    # === UI配置 ===
    ENABLE_VISUALIZATION = (
        os.getenv("ENABLE_VISUALIZATION", "true").lower() == "true"
    )
    UPDATE_INTERVAL = float(os.getenv("UPDATE_INTERVAL", "0.5"))

    # === 沙箱配置 ===
    SANDBOX_TIMEOUT = 2  # 代码执行超时(秒)
    SANDBOX_BLACKLIST = [
        "os",
        "sys",
        "subprocess",
        "socket",
        "shutil",
        "pickle",
        "eval",
        "exec",
        "__import__",
    ]

    @classmethod
    def validate(cls) -> None:
        """验证配置有效性"""
        # 检查API Key
        if not cls.API_KEY:
            raise ValueError(
                "❌ 缺少 ZHIPUAI_API_KEY\n"
                "请在 .env 文件中设置: ZHIPUAI_API_KEY=your_api_key"
            )

        # 创建必要目录
        for directory in [cls.DATA_DIR, cls.LOGS_DIR, cls.CHECKPOINTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

        # 创建FAISS索引目录
        if cls.ENABLE_KNOWLEDGE:
            cls.FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_safe_globals(cls) -> dict:
        """获取安全的globals环境（用于代码执行）"""
        # 构建受限的builtins
        safe_builtins = {
            # 允许的内置函数
            "abs": abs,
            "all": all,
            "any": any,
            "bool": bool,
            "chr": chr,
            "dict": dict,
            "divmod": divmod,
            "enumerate": enumerate,
            "filter": filter,
            "float": float,
            "format": format,
            "frozenset": frozenset,
            "int": int,
            "isinstance": isinstance,
            "issubclass": issubclass,
            "iter": iter,
            "len": len,
            "list": list,
            "map": map,
            "max": max,
            "min": min,
            "next": next,
            "ord": ord,
            "pow": pow,
            "print": print,
            "range": range,
            "reversed": reversed,
            "round": round,
            "set": set,
            "slice": slice,
            "sorted": sorted,
            "str": str,
            "sum": sum,
            "tuple": tuple,
            "type": type,
            "zip": zip,
            # 允许的异常
            "Exception": Exception,
            "ValueError": ValueError,
            "TypeError": TypeError,
            "IndexError": IndexError,
            "KeyError": KeyError,
            "AttributeError": AttributeError,
            # 常用常量
            "True": True,
            "False": False,
            "None": None,
        }

        return {"__builtins__": safe_builtins}

    @classmethod
    def get_info(cls) -> dict:
        """获取配置信息摘要"""
        return {
            "platform": cls.PLATFORM,
            "cpu_count": cls.CPU_COUNT,
            "max_workers": cls.MAX_WORKERS,
            "population_size": cls.POPULATION_SIZE,
            "max_generations": cls.MAX_GENERATIONS,
            "enable_knowledge": cls.ENABLE_KNOWLEDGE,
            "enable_downward_causation": cls.ENABLE_DOWNWARD_CAUSATION,
            "model": cls.MODEL_NAME,
        }


class AdaptiveConfig:
    """自适应配置管理器

    根据任务执行结果动态调整参数
    """

    def __init__(self):
        self.params = {
            "population_size": Config.POPULATION_SIZE,
            "mutation_rate": Config.INITIAL_MUTATION_RATE,
            "early_stop_patience": Config.EARLY_STOP_PATIENCE,
        }
        self.performance_history = []

    def update_from_result(self, task_metrics: dict) -> None:
        """根据任务结果更新参数

        Args:
            task_metrics: 任务指标，包含generations, final_score等
        """
        generations = task_metrics.get("generations", 0)
        final_score = task_metrics.get("final_score", 0)

        # 如果花费代数过多且未完全解决，增加种群大小
        if generations > 15 and final_score < 1.0:
            self.params["population_size"] = min(
                20, self.params["population_size"] + 2
            )

        # 如果快速收敛，降低变异率（减少探索）
        if generations < 5 and final_score >= 0.9:
            self.params["mutation_rate"] = max(
                0.1, self.params["mutation_rate"] * 0.9
            )

        # 记录历史
        self.performance_history.append(task_metrics)

        # 保持历史记录不超过100条
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]

    def get_params(self) -> dict:
        """获取当前参数"""
        return self.params.copy()


# 初始化时验证配置
try:
    Config.validate()
except ValueError as e:
    # 如果是在导入时缺少API_KEY，不立即报错
    # 让main.py来处理
    pass
