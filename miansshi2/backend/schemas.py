# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum


class JobCategory(str, Enum):
    ADMIN_LAW = "行政执法类"
    WINDOW_SERVICE = "窗口服务类"
    GENERAL_MGMT = "综合管理类"


class QuestionType(str, Enum):
    COMPREHENSIVE = "综合分析"
    PLANNING = "计划组织"
    EMERGENCY = "应急应变"
    INTERPERSONAL = "人际关系"
    SCENARIO = "情景模拟"


# 权重计算
class WeightRequest(BaseModel):
    category: JobCategory
    slider_value: int = Field(..., ge=0, le=50, description="滑块值 0-50")


class WeightResponse(BaseModel):
    logic: float = Field(..., ge=0, le=1)
    principle: float = Field(..., ge=0, le=1)
    empathy: float = Field(..., ge=0, le=1)
    expression: float = Field(..., ge=0, le=1)


# 题目生成
class QuestionRequest(BaseModel):
    category: JobCategory
    question_type: QuestionType
    difficulty: Optional[str] = Field(default="medium", description="easy/medium/hard")


class QuestionResponse(BaseModel):
    question_id: str
    question_text: str
    question_type: QuestionType
    time_limit: int = Field(default=240, description="思考时间(秒)")
    answer_time: int = Field(default=180, description="作答时间(秒)")


# AI 反馈
class FeedbackRequest(BaseModel):
    question_id: str
    question_text: str
    question_type: QuestionType
    category: JobCategory
    specific_job: str = Field(..., min_length=1, max_length=50)
    weights: WeightResponse
    answer_text: str = Field(..., min_length=10, max_length=5000)


class FeedbackTrace(BaseModel):
    quote: str = Field(..., description="引用考生原话")
    analysis: str = Field(..., description="点评说明")
    score_change: int = Field(..., ge=-10, le=10, description="分数变化")


class FeedbackResponse(BaseModel):
    success: bool
    total_score: Optional[int] = Field(None, ge=0, le=100)
    score_breakdown: Optional[Dict[str, float]] = None
    traces: Optional[List[FeedbackTrace]] = None
    logic_diagnosis: Optional[str] = None
    improvement_tips: Optional[str] = None
    error: Optional[str] = None


# WebSocket 语音识别
class SpeechMessageType(str, Enum):
    AUDIO = "audio"
    START = "start"
    STOP = "stop"


class SpeechMessage(BaseModel):
    type: SpeechMessageType
    audio_data: Optional[str] = None  # base64 encoded


class SpeechResult(BaseModel):
    text: str
    is_final: bool = Field(default=False)
    confidence: Optional[float] = None
