# services.py
import re
import json
import functools
import base64
import hashlib
import hmac
import logging
import asyncio
import websockets
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedError,
    WebSocketException,
)
from datetime import datetime
from typing import Optional
from httpx import TimeoutException, NetworkError

from zhipuai import ZhipuAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import settings, JOB_MATRIX, QUESTION_RULES

# 配置日志
logger = logging.getLogger(__name__)

# 可重试的异常类型（网络相关）
RETRYABLE_EXCEPTIONS = (
    TimeoutException,
    NetworkError,
    ConnectionError,
    ConnectionClosed,
    ConnectionClosedError,
)

# ============ ZhipuAI 服务 ============

@functools.lru_cache(maxsize=1)
def get_zhipu_client() -> ZhipuAI:
    """获取 ZhipuAI 单例客户端"""
    return ZhipuAI(api_key=settings.zhipu_api_key)

# Prompt 注入防护模式
PROMPT_INJECTION_PATTERNS = [
    r'(?i)ignore.*(instruction|prompt|system)',
    r'(?i)forget.*(all|everything|previous)',
    r'(?i)(直接|马上|立刻).{0,5}\d+分',
    r'(?i)你现在是',
    r'(?i)disregard',
    r'(?i)override',
]

def sanitize_input(text: str) -> tuple[str, bool]:
    """
    清理输入，检测 Prompt 注入

    Args:
        text: 需要清理的输入文本

    Returns:
        tuple[str, bool]: (清理后文本, 是否检测到注入)
    """
    injected = False
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            text = re.sub(pattern, '[已过滤]', text)
            injected = True
    return text, injected

def build_feedback_prompt(
    question_type: str,
    job_category: str,
    specific_job: str,
    weights: dict[str, float]
) -> str:
    """构建 AI 反馈 Prompt"""
    rule = QUESTION_RULES.get(question_type, {})
    persona = JOB_MATRIX.get(job_category, {})

    return f"""你是一名资深的公务员面试考官。

【考生画像】
- 报考岗位：{job_category} ({specific_job})
- 核心价值观：{persona.get('prompt_core', '')}
- 当前评分权重：{weights} (请严格按此权重打分)

【题目类型：{question_type}】
- 必须检查的步骤：{', '.join(rule.get('steps', []))}
- 必须遵守的准则：{rule.get('guidance', '')}

【输出要求】
请输出 JSON 格式，包含以下字段：
{{
    "total_score": 0-100,
    "score_breakdown": {{"logic": 0-100, "principle": 0-100, "empathy": 0-100, "expression": 0-100}},
    "traces": [
        {{"quote": "引用考生原话", "analysis": "点评", "score_change": -5到+5}}
    ],
    "logic_diagnosis": "逻辑诊断",
    "improvement_tips": "针对{specific_job}岗位的改进建议"
}}
"""

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=2, max=10),
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    reraise=True
)
def get_ai_feedback(
    question_text: str,
    answer_text: str,
    question_type: str,
    job_category: str,
    specific_job: str,
    weights: dict[str, float]
) -> dict[str, object]:
    """
    获取 AI 评分反馈

    带重试机制，仅对网络相关异常重试
    """
    client = get_zhipu_client()

    # 清理输入
    clean_answer, injected = sanitize_input(answer_text)
    if injected:
        return {
            "success": False,
            "error": "检测到异常输入，请重新组织语言"
        }

    system_prompt = build_feedback_prompt(
        question_type, job_category, specific_job, weights
    )

    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"题目：{question_text}\n\n考生回答：{clean_answer}"}
            ],
            timeout=30,
        )

        result_text = response.choices[0].message.content

        # 尝试解析 JSON
        # 处理可能的 markdown 代码块
        if "```json" in result_text:
            result_text = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
            if result_text:
                result_text = result_text.group(1)

        result = json.loads(result_text)
        result["success"] = True
        return result

    except json.JSONDecodeError as e:
        # JSON 解析错误不重试
        logger.error(f"AI 响应解析失败: {e}")
        return {
            "success": False,
            "error": "AI 响应格式异常，请稍后重试"
        }
    except (AttributeError, KeyError, IndexError) as e:
        # 响应结构错误不重试
        logger.error(f"AI 响应结构异常: {e}")
        return {
            "success": False,
            "error": "AI 响应格式异常，请稍后重试"
        }
    except (TimeoutException, NetworkError, ConnectionError) as e:
        # 网络错误向上抛出以触发重试
        logger.warning(f"AI 服务网络错误，将重试: {e}")
        raise
    except Exception as e:
        # 其他未知错误不重试
        logger.error(f"AI 服务未知错误: {type(e).__name__}: {e}")
        return {
            "success": False,
            "error": "AI 服务暂时不可用，请稍后重试"
        }

# ============ 讯飞语音服务 ============

class XunfeiSpeechClient:
    """讯飞语音 WebSocket 客户端"""

    WS_URL = "wss://iat-api.xfyun.cn/v2/iat"

    def __init__(self):
        self.app_id = settings.xfyun_app_id
        self.api_key = settings.xfyun_api_key
        self.api_secret = settings.xfyun_api_secret
        logger.info(f"XunfeiSpeechClient 初始化: app_id={self.app_id}, api_key={self.api_key[:8]}...")

    def _generate_auth_url(self) -> str:
        """生成带鉴权的 WebSocket URL"""
        from datetime import timezone

        # 使用 UTC 时间
        now = datetime.now(timezone.utc)
        # RFC1123 格式日期（必须用英文）
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        date = f"{weekdays[now.weekday()]}, {now.day:02d} {months[now.month-1]} {now.year} {now.hour:02d}:{now.minute:02d}:{now.second:02d} GMT"

        logger.debug(f"生成认证URL，日期: {date}")

        signature_origin = f"host: iat-api.xfyun.cn\n"
        signature_origin += f"date: {date}\n"
        signature_origin += "GET /v2/iat HTTP/1.1"

        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            hashlib.sha256
        ).digest()

        signature = base64.b64encode(signature_sha).decode()

        authorization_origin = f'api_key="{self.api_key}", '
        authorization_origin += f'algorithm="hmac-sha256", '
        authorization_origin += f'headers="host date request-line", '
        authorization_origin += f'signature="{signature}"'

        authorization = base64.b64encode(authorization_origin.encode()).decode()

        # URL 编码日期
        import urllib.parse
        date_encoded = urllib.parse.quote(date)

        return f"{self.WS_URL}?authorization={authorization}&date={date_encoded}&host=iat-api.xfyun.cn"

    async def transcribe(self, audio_chunks: list[bytes]) -> str:
        """
        流式语音识别

        Args:
            audio_chunks: 音频数据块列表（16KHz, 16bit, 单声道）

        Returns:
            str: 识别的文本
        """
        # 检查音频数据
        if not audio_chunks:
            logger.warning("音频缓冲区为空，无法进行识别")
            return ""

        # 合并所有音频块
        all_audio = b''.join(audio_chunks)
        total_size = len(all_audio)
        logger.info(f"开始语音识别，音频总大小: {total_size} 字节")

        if total_size < 1000:
            logger.warning(f"音频数据太少 ({total_size} 字节)，可能无法识别")
            return ""

        ws_url = self._generate_auth_url()
        result_text: list[str] = []

        try:
            logger.info(f"连接讯飞 WebSocket: {self.WS_URL}")

            async with websockets.connect(
                ws_url,
                ping_interval=20,
                ping_timeout=10,
                close_timeout=5,
                max_size=10 * 1024 * 1024
            ) as ws:
                logger.info("讯飞 WebSocket 连接成功")

                # 将音频分成小块发送（每块约 1280 字节，约 40ms 音频）
                chunk_size = 1280
                audio_offset = 0
                seq = 0

                while audio_offset < len(all_audio):
                    chunk = all_audio[audio_offset:audio_offset + chunk_size]
                    audio_offset += chunk_size

                    # 确定帧状态
                    if seq == 0:
                        status = 0  # 第一帧
                    elif audio_offset >= len(all_audio):
                        status = 2  # 最后一帧
                    else:
                        status = 1  # 中间帧

                    frame = self._build_frame(seq, status, chunk)
                    await ws.send(frame)
                    logger.debug(f"发送帧 {seq}, 状态 {status}, 大小 {len(chunk)} 字节")
                    seq += 1

                    # 接收响应（不阻塞发送）
                    try:
                        result = await asyncio.wait_for(ws.recv(), timeout=0.1)
                        data = json.loads(result)

                        if data.get("code") and data["code"] != 0:
                            logger.error(f"讯飞返回错误: code={data.get('code')}, message={data.get('message')}")
                            raise RuntimeError(f"语音识别错误: {data.get('message', '未知错误')}")

                        if data.get("data"):
                            result_text.clear()  # 清空之前的结果，使用最新的
                            for ws_result in data["data"]["result"]["ws"]:
                                for word in ws_result["cw"]:
                                    result_text.append(word["w"])
                    except asyncio.TimeoutError:
                        pass  # 继续发送

                # 等待最终结果
                logger.info("等待最终识别结果...")
                while True:
                    try:
                        result = await asyncio.wait_for(ws.recv(), timeout=3.0)
                        data = json.loads(result)

                        if data.get("code") and data["code"] != 0:
                            logger.error(f"讯飞返回错误: code={data.get('code')}, message={data.get('message')}")
                            break

                        if data.get("data"):
                            result_text.clear()
                            for ws_result in data["data"]["result"]["ws"]:
                                for word in ws_result["cw"]:
                                    result_text.append(word["w"])

                        # 检查是否结束
                        if data.get("data", {}).get("result", {}).get("ls", False):
                            logger.info("收到最终结果标记")
                            break

                    except asyncio.TimeoutError:
                        logger.warning("等待最终结果超时")
                        break

                final_text = "".join(result_text)
                logger.info(f"语音识别完成，结果长度: {len(final_text)} 字符")
                if final_text:
                    logger.info(f"识别结果: {final_text[:100]}..." if len(final_text) > 100 else f"识别结果: {final_text}")
                return final_text

        except ConnectionClosed as e:
            logger.error(f"WebSocket 连接被关闭: {e.code} {e.reason}")
            raise RuntimeError("语音识别连接中断，请重试")
        except WebSocketException as e:
            logger.error(f"WebSocket 错误: {e}")
            raise RuntimeError("语音识别服务连接失败")
        except json.JSONDecodeError as e:
            logger.error(f"语音识别响应解析失败: {e}")
            raise RuntimeError("语音识别响应格式错误")
        except asyncio.TimeoutError:
            logger.error("语音识别超时")
            raise RuntimeError("语音识别超时，请重试")
        except Exception as e:
            logger.error(f"语音识别内部错误: {type(e).__name__}: {e}", exc_info=True)
            raise RuntimeError(f"语音识别服务暂时不可用: {str(e)}")

    def _build_frame(self, seq: int, status: int, audio: bytes) -> str:
        """构建 WebSocket 帧"""
        frame = {
            "common": {"app_id": self.app_id},
            "business": {
                "language": "zh_cn",
                "domain": "iat",
                "accent": "mandarin",
                "vad_eos": 3000,  # 3秒静音结束
                "ptt": 1  # 开启标点
            },
            "data": {
                "status": status,
                "format": "audio/L16;rate=16000",
                "encoding": "raw",
                "audio": base64.b64encode(audio).decode()
            }
        }
        return json.dumps(frame)
