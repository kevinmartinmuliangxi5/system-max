# main.py
import uuid
import json
import base64
import logging
import time
from typing import Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import settings, JOB_MATRIX, QUESTION_TYPES, calculate_weights
from schemas import (
    WeightRequest, WeightResponse,
    QuestionRequest, QuestionResponse,
    FeedbackRequest, FeedbackResponse,
    SpeechMessage, SpeechResult
)
from services import get_ai_feedback, XunfeiSpeechClient, get_zhipu_client

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============ 限流配置 ============

limiter = Limiter(key_func=get_remote_address)

# ============ 应用生命周期 ============

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时验证配置
    try:
        client = get_zhipu_client()
        logger.info("ZhipuAI 客户端初始化成功")
    except Exception as e:
        logger.warning(f"ZhipuAI 初始化失败: {e}")

    yield

    # 关闭时清理
    logger.info("服务关闭")

app = FastAPI(
    title="公考 AI 面试官 API",
    description="基于岗位画像的 AI 面试训练系统",
    version="1.0.0",
    lifespan=lifespan
)

# 添加限流状态
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ============ CORS 配置 ============

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 安全响应头中间件 ============

@app.middleware("http")
async def add_security_headers(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # 添加 CSP 头
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self' ws: wss:"
    )
    return response

# ============ 请求日志中间件 ============

@app.middleware("http")
async def log_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    # 记录请求开始时间
    start_time = time.time()

    # 获取客户端信息
    client_host = request.client.host if request.client else "unknown"
    request_id = str(uuid.uuid4())[:8]

    # 记录请求
    logger.info(
        f"[{request_id}] 请求开始: {request.method} {request.url.path} "
        f"来自 {client_host}"
    )

    # 处理请求
    response = await call_next(request)

    # 计算处理时间
    process_time = (time.time() - start_time) * 1000

    # 记录响应
    logger.info(
        f"[{request_id}] 请求完成: {response.status_code} "
        f"耗时 {process_time:.2f}ms"
    )

    # 添加处理时间头
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    response.headers["X-Request-ID"] = request_id

    return response

# ============ API 路由 ============

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "version": "1.0.0"}

@app.get("/api/test-xunfei")
async def test_xunfei():
    """测试讯飞语音识别配置"""
    import websockets
    from services import XunfeiSpeechClient

    try:
        client = XunfeiSpeechClient()
        ws_url = client._generate_auth_url()

        logger.info(f"测试讯飞连接: {ws_url[:100]}...")

        async with websockets.connect(
            ws_url,
            ping_interval=20,
            ping_timeout=10,
            close_timeout=5
        ) as ws:
            # 发送一个空的开始帧
            frame = client._build_frame(0, 0, b'')
            await ws.send(frame)

            # 发送结束帧
            end_frame = client._build_frame(1, 2, b'')
            await ws.send(end_frame)

            # 接收响应
            result = await ws.recv()
            data = json.loads(result)

            return {
                "success": True,
                "message": "讯飞连接成功",
                "response": data
            }
    except Exception as e:
        logger.error(f"讯飞测试失败: {type(e).__name__}: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

@app.post("/api/weights", response_model=WeightResponse)
async def compute_weights(request: WeightRequest):
    """
    计算动态权重

    根据岗位类型和滑块值返回评分权重
    """
    try:
        weights = calculate_weights(request.category.value, request.slider_value)
        return WeightResponse(**weights)
    except KeyError:
        raise HTTPException(status_code=400, detail="无效的岗位类型")

@app.get("/api/jobs")
async def get_job_categories():
    """获取所有岗位类型"""
    return [
        {
            "key": key,
            "desc": value["desc"],
            "slider_label": value["slider_label"]
        }
        for key, value in JOB_MATRIX.items()
    ]

@app.get("/api/question-types")
async def get_question_types():
    """获取所有题型"""
    return QUESTION_TYPES

@app.post("/api/question", response_model=QuestionResponse)
@limiter.limit("10/minute")
async def generate_question(request: Request, body: QuestionRequest):
    """
    生成面试题目

    使用 AI 根据岗位类型和题型动态生成
    限制: 每分钟最多 10 次请求
    """
    try:
        client = get_zhipu_client()

        prompt = f"""请生成一道公务员面试题目。

要求：
1. 题型：{body.question_type.value}
2. 适用岗位：{body.category.value}
3. 难度：{body.difficulty}
4. 只输出题目本身，不要其他解释

题目应贴合{body.category.value}的实际工作场景。"""

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": prompt}],
            timeout=15,
        )

        question_text = response.choices[0].message.content.strip()

        return QuestionResponse(
            question_id=str(uuid.uuid4()),
            question_text=question_text,
            question_type=body.question_type
        )

    except Exception as e:
        logger.error(f"题目生成错误: {e}")
        raise HTTPException(status_code=500, detail="题目生成失败，请稍后重试")

@app.post("/api/feedback", response_model=FeedbackResponse)
@limiter.limit("20/minute")
async def get_feedback(request: Request, body: FeedbackRequest):
    """
    获取 AI 评分反馈

    包含：综合得分、评分溯源、逻辑诊断、改进建议
    限制: 每分钟最多 20 次请求
    """
    weights_dict = body.weights.model_dump()

    result = get_ai_feedback(
        question_text=body.question_text,
        answer_text=body.answer_text,
        question_type=body.question_type.value,
        job_category=body.category.value,
        specific_job=body.specific_job,
        weights=weights_dict
    )

    if not result.get("success"):
        return FeedbackResponse(
            success=False,
            error=result.get("error", "未知错误")
        )

    return FeedbackResponse(
        success=True,
        total_score=result.get("total_score"),
        score_breakdown=result.get("score_breakdown"),
        traces=result.get("traces", []),
        logic_diagnosis=result.get("logic_diagnosis"),
        improvement_tips=result.get("improvement_tips")
    )

# ============ WebSocket 语音识别 ============

def validate_websocket_origin(origin: str | None) -> bool:
    """验证 WebSocket Origin 是否在允许列表中"""
    # 开发模式：允许 localhost 的任何端口
    if origin:
        # 允许 localhost 的任何端口
        if "localhost" in origin or "127.0.0.1" in origin:
            return True
        # 检查 origin 是否在允许的 CORS origins 列表中
        return any(origin.startswith(allowed.rstrip('/')) for allowed in settings.cors_origins)
    return False

@app.websocket("/api/ws/speech")
async def speech_websocket(websocket: WebSocket):
    """
    WebSocket 语音识别端点

    协议：
    - 客户端发送: {"type": "audio", "audio_data": "base64..."}
    - 服务端返回: {"text": "识别文本", "is_final": false}

    安全：验证 Origin 头防止跨站 WebSocket 劫持
    """
    # 记录连接信息用于调试
    origin = websocket.headers.get("origin")
    logger.info(f"WebSocket 连接请求来自 Origin: {origin}")
    logger.info(f"允许的 CORS Origins: {settings.cors_origins}")

    # 验证 Origin
    if not validate_websocket_origin(origin):
        logger.warning(f"拒绝来自未授权 Origin 的 WebSocket 连接: {origin}")
        await websocket.close(code=4003, reason="Unauthorized origin")
        return

    await websocket.accept()

    xunfei_client = XunfeiSpeechClient()
    audio_buffer = []

    try:
        while True:
            data = await websocket.receive_text()
            message = SpeechMessage.model_validate_json(data)

            if message.type == "start":
                audio_buffer = []
                await websocket.send_json({"text": "", "is_final": False})

            elif message.type == "audio" and message.audio_data:
                # 解码 base64 音频
                audio_data = base64.b64decode(message.audio_data)
                audio_buffer.append(audio_data)

                # 每 5 块返回一次中间结果
                if len(audio_buffer) % 5 == 0:
                    try:
                        partial_text = await xunfei_client.transcribe(audio_buffer)
                        await websocket.send_json({
                            "text": partial_text,
                            "is_final": False
                        })
                    except Exception as e:
                        logger.debug(f"中间识别失败: {e}")

            elif message.type == "stop":
                # 最终识别
                try:
                    final_text = await xunfei_client.transcribe(audio_buffer)
                    await websocket.send_json({
                        "text": final_text,
                        "is_final": True
                    })
                except Exception as e:
                    logger.error(f"语音识别失败: {e}")
                    await websocket.send_json({
                        "text": "",
                        "is_final": True,
                        "error": "语音识别服务暂时不可用"
                    })
                audio_buffer = []

    except WebSocketDisconnect:
        logger.info("WebSocket 连接断开")
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")
        await websocket.close()

# ============ 错误处理 ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"未处理异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "服务器内部错误"}
    )

# ============ 入口 ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
