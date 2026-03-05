# config.py
import re
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    zhipu_api_key: str
    xfyun_app_id: str
    xfyun_api_key: str
    xfyun_api_secret: str
    cors_origins: list[str] = ["http://localhost:5173"]

    @field_validator('zhipu_api_key')
    @classmethod
    def validate_zhipu_api_key(cls, v: str) -> str:
        """验证智谱 AI API Key 格式"""
        if not v or v == 'your_zhipu_api_key':
            logger.warning("ZhipuAI API Key 未配置，请设置环境变量 ZHIPU_API_KEY")
        elif not re.match(r'^[a-zA-Z0-9._-]{20,}$', v):
            logger.warning(f"ZhipuAI API Key 格式可能不正确: {v[:8]}...")
        return v

    @field_validator('xfyun_app_id')
    @classmethod
    def validate_xfyun_app_id(cls, v: str) -> str:
        """验证讯飞 App ID 格式"""
        if not v or v == 'your_xfyun_app_id':
            logger.warning("讯飞 App ID 未配置，请设置环境变量 XFYUN_APP_ID")
        return v

    @field_validator('xfyun_api_key')
    @classmethod
    def validate_xfyun_api_key(cls, v: str) -> str:
        """验证讯飞 API Key 格式"""
        if not v or v == 'your_xfyun_api_key':
            logger.warning("讯飞 API Key 未配置，请设置环境变量 XFYUN_API_KEY")
        elif not re.match(r'^[a-f0-9]{32}$', v):
            logger.warning(f"讯飞 API Key 格式可能不正确: {v[:8]}...")
        return v

    @field_validator('xfyun_api_secret')
    @classmethod
    def validate_xfyun_api_secret(cls, v: str) -> str:
        """验证讯飞 API Secret 格式"""
        if not v or v == 'your_xfyun_api_secret':
            logger.warning("讯飞 API Secret 未配置，请设置环境变量 XFYUN_API_SECRET")
        elif not re.match(r'^[a-f0-9]{32}$', v):
            logger.warning(f"讯飞 API Secret 格式可能不正确: {v[:8]}...")
        return v

settings = Settings()

# 岗位矩阵 - 三大类
JOB_MATRIX = {
    "行政执法类": {
        "desc": "代表国家行使行政处罚权，强调原则性与现场控制力。",
        "base_weights": {"logic": 0.3, "principle": 0.5, "empathy": 0.1, "expression": 0.1},
        "slider_label": "服务柔性调节 (0% = 铁面无私, 50% = 刚柔并济)",
        "prompt_core": "你是铁面无私的执法者。核心价值观：【依法行政、程序正义、控制局面】。"
    },
    "窗口服务类": {
        "desc": "直接面对群众办理业务，强调沟通耐心与政策解释力。",
        "base_weights": {"logic": 0.2, "principle": 0.2, "empathy": 0.5, "expression": 0.1},
        "slider_label": "原则刚性调节 (0% = 热情服务, 50% = 原则底线)",
        "prompt_core": "你是温和耐心的服务标兵。核心价值观：【为民服务、换位思考、首问负责】。"
    },
    "综合管理类": {
        "desc": "负责机关内部统筹协调与文稿起草，强调大局观与条理性。",
        "base_weights": {"logic": 0.5, "principle": 0.2, "empathy": 0.1, "expression": 0.2},
        "slider_label": "实务落地调节 (0% = 宏观视野, 50% = 具体执行)",
        "prompt_core": "你是高瞻远瞩的机关领导。核心价值观：【大局意识、统筹兼顾、政治站位】。"
    }
}

# 题型思维链规则
QUESTION_RULES = {
    "综合分析": {
        "steps": ["点 (点明观点)", "析 (多角度分析)", "对 (提出对策)", "升 (总结升华)"],
        "guidance": "请检查考生是否透过现象看本质？是否结合了时政热点？"
    },
    "计划组织": {
        "steps": ["定 (明确目标)", "摸 (调查摸底)", "筹 (物资/人员)", "控 (流程控制)", "结 (总结汇报)"],
        "guidance": "重点检查：是否有【调查摸底】环节？方案是否可落地？"
    },
    "应急应变": {
        "steps": ["稳 (控制局面)", "明 (了解情况)", "调 (调动资源)", "解 (解决问题)", "报 (汇报)", "总 (反思)"],
        "guidance": "重点检查：是否优先【控制了局面】？处理顺序是否得当？"
    },
    "人际关系": {
        "steps": ["态度 (尊重/反思)", "原因 (换位思考)", "化解 (沟通/补救)", "避免 (长效)"],
        "guidance": "核心原则：工作为重。严禁'老好人'思想，原则问题不退让。"
    },
    "情景模拟": {
        "steps": ["入戏 (身份代入)", "共情 (拉近距离)", "说理 (解决困惑)", "表态 (实质解决)"],
        "guidance": "检查是否真正【入戏】？语气是否符合身份？"
    }
}

# 6大题型列表
QUESTION_TYPES = list(QUESTION_RULES.keys())

def calculate_weights(category: str, slider: int) -> dict:
    """
    根据滑块值(0-50)动态调整岗位权重

    Args:
        category: 岗位类型（行政执法类/窗口服务类/综合管理类）
        slider: 滑块值 0-50

    Returns:
        归一化后的权重字典
    """
    base = JOB_MATRIX[category]["base_weights"].copy()
    adjustment = slider / 100.0  # 0.0 - 0.5

    if category == "行政执法类":
        # 滑块增加服务柔性 -> 降低原则性，提升共情力
        base["principle"] -= adjustment * 0.4
        base["empathy"] += adjustment * 0.4

    elif category == "窗口服务类":
        # 滑块增加原则刚性 -> 降低共情力，提升原则性
        base["empathy"] -= adjustment * 0.4
        base["principle"] += adjustment * 0.4

    elif category == "综合管理类":
        # 滑块增加实务落地 -> 降低逻辑性，提升表达力
        base["logic"] -= adjustment * 0.3
        base["expression"] += adjustment * 0.3

    # 归一化处理（确保总和为1）
    total = sum(base.values())
    return {k: round(v/total, 2) for k, v in base.items()}
