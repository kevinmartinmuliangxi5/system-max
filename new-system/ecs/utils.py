"""
ECS - 工具函数
包含格式化、验证、文本处理等实用工具
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path


# ============================================================
# 格式化函数
# ============================================================

def format_emergence_report(report, detailed: bool = True) -> str:
    """
    格式化涌现报告

    Args:
        report: 涌现报告
        detailed: 是否包含详细信息

    Returns:
        格式化的字符串
    """
    lines = [
        "=== 涌现报告 ===",
        "",
        f"涌现类型: {report.emergence_type.value}",
        f"系统阶段: {report.system_phase.value}",
        f"涌现强度: {report.metrics.emergence_score:.2f}",
        ""
    ]

    if detailed:
        lines.extend([
            "## 详细指标",
            f"  多样性: {report.metrics.diversity:.2f}",
            f"  共识度: {report.metrics.consensus:.2f}",
            f"  新颖度: {report.metrics.novelty:.2f}",
            f"  整合度: {report.metrics.integration:.2f}",
            f"  协同度: {report.metrics.synergy:.2f}",
            f"  离散度: {report.metrics.dispersion:.3f}",
            f"  极化度: {report.metrics.polarization:.3f}",
            f"  连接密度: {report.metrics.connectivity:.2f}",
            ""
        ])

        lines.extend([
            "## 涌现类型说明",
            get_emergence_type_description(report.emergence_type.value),
            "",
            "## 系统阶段说明",
            get_system_phase_description(report.system_phase.value),
            ""
        ])

    if report.insights:
        lines.extend([
            "## 关键洞察"
        ])
        for insight in report.insights:
            lines.append(f"  - {insight}")
        lines.append("")

    if report.recommendations:
        lines.extend([
            "## 建议"
        ])
        for rec in report.recommendations:
            lines.append(f"  - {rec}")
        lines.append("")

    return "\n".join(lines)


def get_emergence_type_description(emergence_type: str) -> str:
    """获取涌现类型描述"""
    descriptions = {
        "aggregation": "聚合涌现 - 观点简单聚合，尚未产生深度协作",
        "coordination": "协调涌现 - 角色分工明确，开始有效协作",
        "synergy": "协同涌现 - 深度观点整合，产生协同效应",
        "innovation": "创新涌现 - 产生突破性洞察和创造性解决方案",
        "meta_emergence": "元涌现 - 范式转移级别的涌现，超越原有框架"
    }
    return descriptions.get(emergence_type, "未知类型")


def get_system_phase_description(phase: str) -> str:
    """获取系统阶段描述"""
    descriptions = {
        "exploration": "探索期 - 团队正在探索多种可能性",
        "debate": "辩论期 - 观点碰撞，深度讨论中",
        "convergence": "收敛期 - 观点趋向一致",
        "consensus": "共识期 - 达成高度共识",
        "stagnation": "停滞期 - 需要引入新视角打破僵局"
    }
    return descriptions.get(phase, "未知阶段")


def format_discussion_summary(messages: List[Dict], max_per_agent: int = 3) -> str:
    """
    格式化讨论摘要

    Args:
        messages: 消息列表
        max_per_agent: 每个Agent最多显示的消息数

    Returns:
        格式化的字符串
    """
    # 按Agent分组
    by_agent: Dict[str, List[Dict]] = {}
    for msg in messages:
        agent_id = msg.get("agent_id", "unknown")
        if agent_id not in by_agent:
            by_agent[agent_id] = []
        by_agent[agent_id].append(msg)

    lines = ["## 讨论摘要", ""]

    for agent_id, agent_messages in by_agent.items():
        lines.append(f"### {agent_id}")
        for msg in agent_messages[-max_per_agent:]:
            content = msg.get("content", "")
            round_num = msg.get("round_num", 0)
            lines.append(f"  [轮次{round_num}] {content[:150]}...")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# 验证函数
# ============================================================

def validate_api_key(api_key: str, provider: str = "anthropic") -> bool:
    """
    验证API密钥格式

    Args:
        api_key: API密钥
        provider: 提供商（anthropic或openai）

    Returns:
        是否有效
    """
    if not api_key:
        return False

    if provider == "anthropic":
        # Anthropic密钥格式: sk-ant-api03-...
        return api_key.startswith("sk-ant-")
    elif provider == "openai":
        # OpenAI密钥格式: sk-...
        return api_key.startswith("sk-")
    else:
        return len(api_key) > 20


def validate_task_description(task: str) -> Tuple[bool, Optional[str]]:
    """
    验证任务描述

    Args:
        task: 任务描述

    Returns:
        (是否有效, 错误消息)
    """
    if not task or not task.strip():
        return False, "任务描述不能为空"

    task = task.strip()

    if len(task) < 10:
        return False, "任务描述太短，请提供更多细节"

    if len(task) > 5000:
        return False, "任务描述太长，请精简到5000字符以内"

    return True, None


def validate_config(config: Dict) -> Tuple[bool, List[str]]:
    """
    验证配置

    Args:
        config: 配置字典

    Returns:
        (是否有效, 错误列表)
    """
    errors = []

    # 验证Agent数量
    agent_count = config.get("agents", {}).get("count", 5)
    if agent_count < 2:
        errors.append("Agent数量至少为2")
    elif agent_count > 15:
        errors.append("Agent数量建议不超过15")

    # 验证轮次
    max_rounds = config.get("collaboration", {}).get("max_rounds", 3)
    if max_rounds < 1:
        errors.append("讨论轮次至少为1")
    elif max_rounds > 10:
        errors.append("讨论轮次建议不超过10")

    # 验证阈值
    emergence_threshold = config.get("emergence", {}).get("emergence_threshold", 0.7)
    if not (0 <= emergence_threshold <= 1):
        errors.append("涌现阈值必须在0-1之间")

    consensus_threshold = config.get("collaboration", {}).get("consensus_threshold", 0.7)
    if not (0 <= consensus_threshold <= 1):
        errors.append("共识阈值必须在0-1之间")

    return len(errors) == 0, errors


# ============================================================
# 文本处理函数
# ============================================================

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    计算两段文本的相似度

    Args:
        text1: 第一段文本
        text2: 第二段文本

    Returns:
        相似度值 0-1
    """
    # 简单的词袋模型
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    提取文本中的关键词

    Args:
        text: 输入文本
        top_n: 返回前N个关键词

    Returns:
        关键词列表
    """
    # 简单的词频统计
    words = re.findall(r'\w+', text.lower())
    word_freq = {}

    # 过滤常见停用词
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        '的', '了', '是', '在', '和', '有', '就', '不', '人', '都', '一',
        '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着'
    }

    for word in words:
        if len(word) > 2 and word not in stopwords:
            word_freq[word] = word_freq.get(word, 0) + 1

    # 按频率排序
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:top_n]]


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    截断文本

    Args:
        text: 输入文本
        max_length: 最大长度
        suffix: 截断后缀

    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def clean_text(text: str) -> str:
    """
    清理文本

    Args:
        text: 输入文本

    Returns:
        清理后的文本
    """
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    # 移除特殊字符（保留中英文、数字、常用标点）
    text = re.sub(r'[^\w\s\u4e00-\u9fff,.;:!?()\-"\']', '', text)
    return text.strip()


# ============================================================
# 文件处理函数
# ============================================================

def ensure_directory(path: str) -> Path:
    """
    确保目录存在

    Args:
        path: 目录路径

    Returns:
        Path对象
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_json(data: Any, file_path: str):
    """
    保存JSON文件

    Args:
        data: 要保存的数据
        file_path: 文件路径
    """
    ensure_directory(str(Path(file_path).parent))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path: str) -> Any:
    """
    加载JSON文件

    Args:
        file_path: 文件路径

    Returns:
        加载的数据
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_markdown(content: str, file_path: str):
    """
    保存Markdown文件

    Args:
        content: Markdown内容
        file_path: 文件路径
    """
    ensure_directory(str(Path(file_path).parent))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


# ============================================================
# 时间和日期函数
# ============================================================

def get_timestamp() -> str:
    """获取当前时间戳字符串"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_duration(seconds: float) -> str:
    """
    格式化时长

    Args:
        seconds: 秒数

    Returns:
        格式化的时长字符串
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}分钟"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}小时"


# ============================================================
# 成本估算函数
# ============================================================

def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "claude-sonnet-4-20250514",
    enable_cache: bool = True
) -> Dict[str, float]:
    """
    估算API调用成本

    Args:
        input_tokens: 输入token数
        output_tokens: 输出token数
        model: 模型名称
        enable_cache: 是否启用缓存

    Returns:
        成本字典（美元）
    """
    # Claude Sonnet 4 定价 (2025年)
    if "claude" in model:
        input_price = 3.0 / 1_000_000  # $3 per million tokens
        output_price = 15.0 / 1_000_000  # $15 per million tokens

        # 缓存读取价格
        cache_price = 0.3 / 1_000_000 if enable_cache else 0

        # 假设缓存命中率
        cache_hit_rate = 0.9 if enable_cache else 0

        input_cost = input_tokens * input_price
        cache_cost = input_tokens * cache_hit_rate * cache_price
        output_cost = output_tokens * output_price

        total_cost = input_cost + cache_cost + output_cost

        return {
            "input": input_cost,
            "cache": cache_cost,
            "output": output_cost,
            "total": total_cost,
            "cached": enable_cache
        }

    # GPT-4 定价 (示例)
    elif "gpt" in model:
        input_price = 30.0 / 1_000_000
        output_price = 60.0 / 1_000_000

        input_cost = input_tokens * input_price
        output_cost = output_tokens * output_price
        total_cost = input_cost + output_cost

        return {
            "input": input_cost,
            "cache": 0.0,
            "output": output_cost,
            "total": total_cost,
            "cached": False
        }

    else:
        # 默认定价
        return {
            "input": 0.0,
            "cache": 0.0,
            "output": 0.0,
            "total": 0.0,
            "cached": False
        }


def estimate_collaboration_cost(
    agent_count: int,
    rounds: int,
    avg_input_tokens: int = 5000,
    avg_output_tokens: int = 1000,
    model: str = "claude-sonnet-4-20250514"
) -> Dict[str, Any]:
    """
    估算协作成本

    Args:
        agent_count: Agent数量
        rounds: 讨论轮次
        avg_input_tokens: 平均输入token数
        avg_output_tokens: 平均输出token数
        model: 模型名称

    Returns:
        成本估算字典
    """
    # 估算总调用次数
    total_calls = agent_count * rounds

    # 每次调用的token数（随着讨论增长）
    total_input = 0
    total_output = 0

    for r in range(rounds):
        # 每轮上下文增长
        round_input = avg_input_tokens + (r * agent_count * avg_output_tokens)
        total_input += round_input * agent_count
        total_output += avg_output_tokens * agent_count

    # 计算成本
    cost_no_cache = estimate_cost(total_input, total_output, model, enable_cache=False)
    cost_with_cache = estimate_cost(total_input, total_output, model, enable_cache=True)

    savings = cost_no_cache["total"] - cost_with_cache["total"]
    savings_percent = (savings / cost_no_cache["total"] * 100) if cost_no_cache["total"] > 0 else 0

    return {
        "total_calls": total_calls,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "cost_no_cache": cost_no_cache["total"],
        "cost_with_cache": cost_with_cache["total"],
        "savings": savings,
        "savings_percent": savings_percent,
        "currency": "USD"
    }


# ============================================================
# 涌现关键词检测
# ============================================================

EMERGENCE_KEYWORDS = [
    "新想法", "突然想到", "更好的方案", "结合",
    "创新", "改进", "优化", "综合", "突破",
    "换个角度", "重新考虑", "发现", "启发",
    "insight", "breakthrough", "novel", "innovative",
    "realize", "aha", "epiphany", "组合", "融合",
    "意识到", "灵感", "顿悟", "重构"
]


def detect_emergence_keywords(text: str) -> List[str]:
    """
    检测文本中的涌现关键词

    Args:
        text: 输入文本

    Returns:
        匹配的关键词列表
    """
    matched = []
    text_lower = text.lower()
    for keyword in EMERGENCE_KEYWORDS:
        if keyword.lower() in text_lower:
            matched.append(keyword)
    return matched


def count_emergence_moments(messages: List[Dict]) -> int:
    """
    统计涌现时刻数量

    Args:
        messages: 消息列表

    Returns:
        涌现时刻数量
    """
    count = 0
    for msg in messages:
        content = msg.get("content", "")
        if detect_emergence_keywords(content):
            count += 1
    return count


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 格式化
    "format_emergence_report",
    "get_emergence_type_description",
    "get_system_phase_description",
    "format_discussion_summary",

    # 验证
    "validate_api_key",
    "validate_task_description",
    "validate_config",

    # 文本处理
    "calculate_text_similarity",
    "extract_keywords",
    "truncate_text",
    "clean_text",

    # 文件处理
    "ensure_directory",
    "save_json",
    "load_json",
    "save_markdown",

    # 时间
    "get_timestamp",
    "format_duration",

    # 成本估算
    "estimate_cost",
    "estimate_collaboration_cost",

    # 涌现检测
    "EMERGENCE_KEYWORDS",
    "detect_emergence_keywords",
    "count_emergence_moments"
]
