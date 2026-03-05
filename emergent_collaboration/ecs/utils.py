"""
ECS - 工具函数模块

提供各种辅助函数
"""

import os
import hashlib
import time
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import numpy as np
from datetime import datetime


def generate_id(prefix: str = "ecs") -> str:
    """
    生成唯一ID

    Args:
        prefix: ID前缀

    Returns:
        唯一ID字符串
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_part = hashlib.md5(str(time.time_ns()).encode()).hexdigest()[:8]
    return f"{prefix}_{timestamp}_{hash_part}"


def format_timestamp(dt: datetime = None) -> str:
    """
    格式化时间戳

    Args:
        dt: datetime对象（可选，默认当前时间）

    Returns:
        格式化的时间字符串
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_duration(seconds: float) -> str:
    """
    格式化持续时间

    Args:
        seconds: 秒数

    Returns:
        格式化的持续时间字符串
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}分{secs}秒"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}小时{minutes}分"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本

    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀

    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    提取关键词（简化版）

    Args:
        text: 输入文本
        top_n: 返回前N个关键词

    Returns:
        关键词列表
    """
    # 简单的分词和词频统计
    words = text.split()

    # 过滤停用词（简化版）
    stopwords = {
        '的', '是', '在', '和', '了', '有', '不', '这', '与', '也',
        'to', 'the', 'a', 'an', 'is', 'are', 'and', 'or', 'but', 'not'
    }

    # 统计词频
    word_freq = {}
    for word in words:
        word = word.strip('.,!?;:""').lower()
        if len(word) > 1 and word not in stopwords:
            word_freq[word] = word_freq.get(word, 0) + 1

    # 排序并返回top_n
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:top_n]]


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    计算两个文本的相似度（基于Jaccard相似度）

    Args:
        text1: 文本1
        text2: 文本2

    Returns:
        相似度（0-1）
    """
    # 简单分词
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    # Jaccard相似度
    intersection = words1 & words2
    union = words1 | words2

    if len(union) == 0:
        return 1.0

    return len(intersection) / len(union)


def merge_dicts(*dicts: Dict) -> Dict:
    """
    合并多个字典

    Args:
        *dicts: 要合并的字典

    Returns:
        合并后的字典
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    将列表分块

    Args:
        lst: 原始列表
        chunk_size: 块大小

    Returns:
        分块后的列表
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_list(nested_list: List) -> List:
    """
    展平嵌套列表

    Args:
        nested_list: 嵌套列表

    Returns:
        展平后的列表
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """
    安全除法

    Args:
        a: 被除数
        b: 除数
        default: 除数为0时的默认值

    Returns:
        除法结果
    """
    if b == 0:
        return default
    return a / b


def normalize_score(score: float,
                   min_val: float = 0.0,
                   max_val: float = 1.0) -> float:
    """
    归一化分数到指定范围

    Args:
        score: 原始分数
        min_val: 最小值
        max_val: 最大值

    Returns:
        归一化后的分数
    """
    if max_val == min_val:
        return min_val

    normalized = (score - min_val) / (max_val - min_val)
    return max(min_val, min(max_val, normalized))


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    将值限制在指定范围内

    Args:
        value: 输入值
        min_val: 最小值
        max_val: 最大值

    Returns:
        限制后的值
    """
    return max(min_val, min(max_val, value))


def percentile(values: List[float], p: float) -> float:
    """
    计算百分位数

    Args:
        values: 值列表
        p: 百分位数（0-100）

    Returns:
        百分位数值
    """
    if not values:
        return 0.0

    sorted_values = sorted(values)
    k = (len(sorted_values) - 1) * (p / 100)
    idx = int(k)

    return sorted_values[idx]


def mean(values: List[float]) -> float:
    """计算平均值"""
    if not values:
        return 0.0
    return float(np.mean(values))


def std(values: List[float]) -> float:
    """计算标准差"""
    if not values:
        return 0.0
    return float(np.std(values))


def median(values: List[float]) -> float:
    """计算中位数"""
    if not values:
        return 0.0
    return float(np.median(values))


def format_percent(value: float, decimals: int = 1) -> str:
    """
    格式化为百分比字符串

    Args:
        value: 值（0-1）
        decimals: 小数位数

    Returns:
        百分比字符串
    """
    return f"{value * 100:.{decimals}f}%"


def parse_task_input(task_input: str) -> str:
    """
    解析任务输入

    Args:
        task_input: 任务输入（可能是文件路径或直接文本）

    Returns:
        任务描述
    """
    # 检查是否是文件路径
    path = Path(task_input)
    if path.exists():
        # 从文件读取任务
        return path.read_text(encoding='utf-8').strip()

    return task_input.strip()


def create_workspace(base_dir: str = "workspace") -> Path:
    """
    创建工作空间目录

    Args:
        base_dir: 基础目录路径

    Returns:
        工作空间路径
    """
    workspace = Path(base_dir)
    workspace.mkdir(parents=True, exist_ok=True)

    # 创建子目录
    (workspace / "logs").mkdir(exist_ok=True)
    (workspace / "output").mkdir(exist_ok=True)
    (workspace / "cache").mkdir(exist_ok=True)

    return workspace


def clean_workspace(workspace: Path, keep_recent: int = 5):
    """
    清理工作空间

    Args:
        workspace: 工作空间路径
        keep_recent: 保留最近多少个文件
    """
    output_dir = workspace / "output"

    if not output_dir.exists():
        return

    # 获取所有输出文件
    files = list(output_dir.glob("*.json"))

    # 按修改时间排序
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    # 删除旧文件
    for old_file in files[keep_recent:]:
        old_file.unlink()


def format_emergence_report(report: Any, verbose: bool = True) -> str:
    """
    格式化涌现报告

    Args:
        report: 涌现报告对象
        verbose: 是否显示详细信息

    Returns:
        格式化的报告字符串
    """
    from .emergence import EmergenceReport, EmergenceType

    if not isinstance(report, EmergenceReport):
        # 尝试从字典创建
        report = EmergenceReport(**report)

    lines = [
        "=" * 60,
        "涌现检测报告",
        "=" * 60,
        "",
        f"涌现类型: {report.emergence_type.value}",
        f"系统阶段: {report.system_phase.value}",
        f"轮次: {report.round_num}",
        "",
        "核心指标:",
        f"  涌现强度: {format_percent(report.metrics.emergence_score)}",
        f"  多样性: {format_percent(report.metrics.diversity)}",
        f"  共识度: {format_percent(report.metrics.consensus)}",
        f"  新颖度: {format_percent(report.metrics.novelty)}",
        f"  整合度: {format_percent(report.metrics.integration)}",
        "",
    ]

    if verbose:
        lines.extend([
            "详细指标:",
            f"  观点离散度: {report.metrics.dispersion:.3f}",
            f"  极化程度: {report.metrics.polarization:.3f}",
            f"  观点簇数: {report.metrics.cluster_count}",
            f"  连接密度: {format_percent(report.metrics.connectivity)}",
            f"  收敛速率: {report.metrics.convergence_rate:.3f}",
            f"  突破性得分: {report.metrics.breakthrough:.3f}",
            f"  协同得分: {format_percent(report.metrics.synergy_score)}",
            "",
        ])

    if report.recommendations:
        lines.extend([
            "建议:",
        ])
        for rec in report.recommendations:
            lines.append(f"  • {rec}")

    return "\n".join(lines)


def validate_api_key() -> Tuple[bool, str]:
    """
    验证API密钥

    Returns:
        (是否有效, 提示消息)
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        return False, "未设置ANTHROPIC_API_KEY环境变量"

    if api_key.startswith("sk-ant-"):
        return True, "API密钥格式正确"
    else:
        return False, "API密钥格式不正确，应该以'sk-ant-'开头"


def setup_logging(level: str = "INFO", log_file: str = "ecs.log"):
    """
    设置日志系统

    Args:
        level: 日志级别
        log_file: 日志文件路径
    """
    import logging

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level))

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(message)s'
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


__all__ = [
    'generate_id',
    'format_timestamp',
    'format_duration',
    'truncate_text',
    'extract_keywords',
    'calculate_text_similarity',
    'merge_dicts',
    'chunk_list',
    'flatten_list',
    'safe_divide',
    'normalize_score',
    'clamp',
    'percentile',
    'mean',
    'std',
    'median',
    'format_percent',
    'parse_task_input',
    'create_workspace',
    'clean_workspace',
    'format_emergence_report',
    'validate_api_key',
    'setup_logging',
]
