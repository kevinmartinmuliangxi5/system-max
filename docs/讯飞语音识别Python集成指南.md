# 讯飞听见（讯飞语音识别）API Python 集成指南

## 目录
1. [官方Python SDK](#1官方python-sdk)
2. [WebSocket鉴权流程](#2websocket鉴权流程)
3. [音频格式要求](#3音频格式要求)
4. [实时语音流处理](#4实时语音流处理)
5. [错误处理和重试](#5错误处理和重试)
6. [免费额度和限制](#6免费额度和限制)
7. [Python代码示例](#7python代码示例)

---

## 1. 官方Python SDK

### 1.1 星火大模型Python SDK（官方）
- **GitHub仓库**: https://github.com/iflytek/spark-ai-python
- **功能特点**:
  - 无缝对接讯飞Maas平台微调训练托管的大模型API
  - SDK方式适配OpenAI接口ChatCompletion接口
  - 支持大模型相关功能

**安装方式**:
```bash
pip install spark-ai-python
```

### 1.2 第三方SDK
- **iFLYTEK-MSC-Python-SDK**: https://github.com/jm12138/iFLYTEK-MSC-Python-SDK
  - 支持语音唤醒、语音识别、语音合成、语音评测

---

## 2. WebSocket鉴权流程

### 2.1 鉴权参数说明

讯飞语音识别使用 **HMAC-SHA256** 签名算法进行鉴权。

**需要的参数**:
- `APPID`: 应用ID
- `APIKey`: API密钥
- `APISecret`: API密钥

### 2.2 鉴权步骤

```python
import hashlib
import base64
import hmac
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
from urllib.parse import urlencode

def create_auth_url(APPID, APIKey, APISecret):
    """
    生成带鉴权参数的WebSocket URL
    """
    url = 'wss://ws-api.xfyun.cn/v2/iat'

    # 1. 生成RFC1123格式的时间戳
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    # 2. 拼接签名字符串
    signature_origin = 'host: ws-api.xfyun.cn\n'
    signature_origin += f'date: {date}\n'
    signature_origin += 'GET /v2/iat HTTP/1.1'

    # 3. 使用HMAC-SHA256加密
    signature_sha = hmac.new(
        APISecret.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

    # 4. 生成authorization
    authorization_origin = f'api_key="{APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

    # 5. 组合鉴权参数
    v = {
        'authorization': authorization,
        'date': date,
        'host': 'ws-api.xfyun.cn'
    }

    # 6. 生成最终URL
    return url + '?' + urlencode(v)
```

---

## 3. 音频格式要求

### 3.1 基本要求

| 参数 | 要求 |
|------|------|
| **音频格式** | PCM、WAV、MP3（仅中文普通话和英文）、Speex |
| **采样率** | 16K（推荐）或 8K |
| **采样精度** | 16 bit |
| **声道** | 单声道 |
| **编码** | PCM（未压缩） |
| **音频长度** | 最长60s（听写流式版） |

### 3.2 音频帧大小

```python
# 推荐参数
CHUNK = 1024              # 每次读取的音频块大小
FORMAT = pyaudio.paInt16    # 16位深度
CHANNELS = 1              # 单声道
RATE = 16000              # 采样率16kHz
INTERVAL = 0.04           # 发送间隔40ms
```

**不同格式的帧大小**:
- **PCM格式**: 每次发送1280字节，间隔40ms
- **讯飞定制speex** (16k, 压缩等级7): 每次发送61B的整数倍
- **标准开源speex** (16k, 压缩等级7): 每次发送60B的整数倍

---

## 4. 实时语音流处理

### 4.1 音频采集（使用PyAudio）

```python
import pyaudio

# 初始化PyAudio
audio = pyaudio.PyAudio()

# 打开音频流
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

# 读取音频数据
buf = stream.read(CHUNK)
```

### 4.2 数据帧标识

```python
STATUS_FIRST_FRAME = 0      # 第一帧标识
STATUS_CONTINUE_FRAME = 1   # 中间帧标识
STATUS_LAST_FRAME = 2       # 最后一帧标识
```

### 4.3 消息格式

**首帧消息**:
```python
{
    "common": {
        "app_id": "your_app_id"
    },
    "business": {
        "language": "zh_cn",
        "domain": "iat",
        "accent": "mandarin",
        "dwa": "wpgs"  # 开启动态修正
    },
    "data": {
        "status": 0,
        "format": "audio/L16;rate=16000",
        "encoding": "raw",
        "audio": base64编码的音频数据
    }
}
```

**中间帧消息**:
```python
{
    "data": {
        "status": 1,
        "format": "audio/L16;rate=16000",
        "encoding": "raw",
        "audio": base64编码的音频数据
    }
}
```

**尾帧消息**:
```python
{
    "data": {
        "status": 2,
        "format": "audio/L16;rate=16000",
        "encoding": "raw",
        "audio": ""  # 空音频数据
    }
}
```

---

## 5. 错误处理和重试

### 5.1 常见错误码

| 错误码 | 描述 | 处理方式 |
|--------|------|----------|
| 0 | success | 成功 |
| 10005 | licc fail | 检查appid是否开通听写服务 |
| 10101 | engine inavtive | 引擎会话已结束，检查是否已断开 |
| 10114 | session timeout | 会话超时（超过60s） |
| 10163 | invalid param | 缺少必传参数 |
| 10200 | read data timeout | 累计10s未发送数据 |
| 11200 | auth no license | 没有权限或调用次数超限 |

### 5.2 重试机制（指数退避）

```python
import time

class RetryHandler:
    def __init__(self, max_retry=3, initial_backoff=1000):
        self.max_retry = max_retry
        self.initial_backoff = initial_backoff
        self.retry_count = 0

    def retry_with_backoff(self, func):
        while self.retry_count < self.max_retry:
            try:
                return func()
            except Exception as e:
                self.retry_count += 1
                if self.retry_count >= self.max_retry:
                    raise

                # 指数退避
                backoff_time = self.initial_backoff * (2 ** self.retry_count)
                print(f"Retry {self.retry_count}/{self.max_retry}, "
                      f"waiting {backoff_time}ms...")
                time.sleep(backoff_time / 1000)
```

### 5.3 错误处理策略

1. **鉴权错误（401）**: 检查APIKey、APISecret是否正确
2. **超时错误**: 检查网络连接，增加超时时间
3. **授权错误**: 检查是否开通对应服务
4. **参数错误**: 检查音频格式、参数值是否合法

---

## 6. 免费额度和限制

### 6.1 免费额度

根据搜索结果，讯飞开放平台提供：
- **新用户**: 可领取免费套餐
- **个人用户**: 约5小时免费额度
- **企业用户**: 约50小时免费额度

> 注意：具体免费额度请登录[讯飞开放平台控制台](https://www.xfyun.cn)查看

### 6.2 使用限制

| 限制项 | 限制值 |
|--------|--------|
| **单次音频时长** | 最长60s（听写流式版） |
| **音频大小** | Base64编码后不超过13000B |
| **并发连接** | 默认50路 |
| **发送超时** | 累计10s未发送数据会断开 |
| **会话超时** | 整个会话最长60s |
| **热词数量** | 最多2000个应用级热词 |

### 6.3 IP白名单

- 默认关闭，不限制调用IP
- 开启后需在控制台配置外网IP
- 约5分钟生效

---

## 7. Python代码示例

### 7.1 完整的实时语音识别类

```python
# -*- coding: utf-8 -*-
"""
讯飞语音听写流式API Python示例
环境要求: Python3.7+
依赖库: websocket-client, pyaudio
"""

import hashlib
import base64
import hmac
import json
import time
import _thread as thread
import logging
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
from urllib.parse import urlencode

try:
    import pyaudio
    from ws4py.client.threadedclient import WebSocketClient
except ImportError:
    print("请先安装依赖库: pip install pyaudio ws4py")
    exit(1)

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 音频状态常量
STATUS_FIRST_FRAME = 0      # 第一帧标识
STATUS_CONTINUE_FRAME = 1   # 中间帧标识
STATUS_LAST_FRAME = 2        # 最后一帧标识

# 音频参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


class WsParam:
    """WebSocket鉴权参数生成类"""

    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret

        # 公共参数
        self.CommonArgs = {'app_id': self.APPID}

        # 业务参数
        self.BusinessArgs = {
            'domain': 'iat',           # 日常用语
            'language': 'zh_cn',       # 中文
            'accent': 'mandarin',      # 普通话
            'vinfo': 1,              # 返回端点信息
            'vad_eos': 10000,        # 后端点检测10秒
            'dwa': 'wpgs',           # 开启动态修正
            'ptt': 1                 # 开启标点
        }

    def create_url(self):
        """生成鉴权URL"""
        url = 'wss://ws-api.xfyun.cn/v2/iat'

        # 生成RFC1123格式时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接签名字符串
        signature_origin = 'host: ws-api.xfyun.cn\n'
        signature_origin += f'date: {date}\n'
        signature_origin += 'GET /v2/iat HTTP/1.1'

        # HMAC-SHA256加密
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        # 生成authorization
        authorization_origin = (
            f'api_key="{self.APIKey}", '
            f'algorithm="hmac-sha256", '
            f'headers="host date request-line", '
            f'signature="{signature_sha}"'
        )
        authorization = base64.b64encode(
            authorization_origin.encode('utf-8')
        ).decode(encoding='utf-8')

        # 组合鉴权参数
        v = {
            'authorization': authorization,
            'date': date,
            'host': 'ws-api.xfyun.cn'
        }

        return url + '?' + urlencode(v)


class RecognitionWebSocket(WebSocketClient):
    """语音识别WebSocket客户端"""

    def __init__(self, url, ws_param):
        super().__init__(url)
        self.ws_param = ws_param
        self.rec_text = {}      # 识别结果
        self.full_text = ""      # 完整文本
        self.is_running = False

    def opened(self):
        """WebSocket连接建立后的回调"""
        logging.info("WebSocket连接已建立")
        self.is_running = True

        def run():
            interval = 0.04  # 发送间隔40ms
            status = STATUS_FIRST_FRAME

            # 初始化音频
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )

            logging.info("开始录音...按Ctrl+C停止")

            try:
                while self.is_running:
                    buf = stream.read(CHUNK)

                    # 构建数据帧
                    if status == STATUS_FIRST_FRAME:
                        d = {
                            'common': self.ws_param.CommonArgs,
                            'business': self.ws_param.BusinessArgs,
                            'data': {
                                'status': 0,
                                'format': 'audio/L16;rate=16000',
                                'audio': str(base64.b64encode(buf).decode('utf-8')),
                                'encoding': 'raw'
                            }
                        }
                        status = STATUS_CONTINUE_FRAME
                    else:
                        d = {
                            'data': {
                                'status': 1,
                                'format': 'audio/L16;rate=16000',
                                'audio': str(base64.b64encode(buf).decode('utf-8')),
                                'encoding': 'raw'
                            }
                        }

                    self.send(json.dumps(d))
                    time.sleep(interval)

            except KeyboardInterrupt:
                logging.info("用户中断，发送结束帧")
                # 发送结束帧
                d = {
                    'data': {
                        'status': 2,
                        'format': 'audio/L16;rate=16000',
                        'audio': '',
                        'encoding': 'raw'
                    }
                }
                self.send(json.dumps(d))

            finally:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                self.is_running = False
                time.sleep(1)
                self.close()

        thread.start_new_thread(run, ())

    def received_message(self, message):
        """收到消息的回调"""
        try:
            msg = json.loads(message)
            code = msg.get('code', -1)
            sid = msg.get('sid', '')

            if code != 0:
                err_msg = msg.get('message', '未知错误')
                logging.error(f'sid:{sid} call error:{err_msg} code:{code}')
                return

            data = msg.get('data', {})
            result = data.get('result', {})
            ws = result.get('ws', [])
            pgs = result.get('pgs', 'apd')  # apd=追加, rpl=替换
            sn = result.get('sn', 0)

            # 提取文本
            text = ''
            for i in ws:
                for w in i.get('cw', []):
                    text += w.get('w', '')

            # 处理动态修正
            if pgs == 'rpl':
                rg = result.get('rg', [0, 0])
                self.rec_text[rg[0]] = text
                for i in range(rg[0] + 1, rg[1]):
                    self.rec_text.pop(i, None)
            else:
                self.rec_text[sn] = text

            # 更新完整文本
            self.full_text = ''.join(self.rec_text.values())

            if text:
                logging.info(f'识别结果: {self.full_text}')

        except Exception as e:
            logging.error(f'解析消息异常: {e}')
            logging.debug(f'原始消息: {message}')

    def closed(self, code, reason=None):
        """连接关闭的回调"""
        logging.info(f'WebSocket连接已关闭 code:{code} reason:{reason}')
        self.is_running = False
        logging.info(f'最终识别结果: {self.full_text}')

    def on_error(self, error):
        """错误回调"""
        logging.error(f'WebSocket错误: {error}')


def main():
    """主函数"""
    # 请替换为你的实际参数
    APPID = "your_app_id"
    APIKey = "your_api_key"
    APISecret = "your_api_secret"

    # 创建鉴权参数
    ws_param = WsParam(APPID, APIKey, APISecret)

    # 生成连接URL
    ws_url = ws_param.create_url()
    logging.info(f'连接URL: {ws_url}')

    # 创建WebSocket客户端
    ws = RecognitionWebSocket(ws_url, ws_param)

    # 连接并运行
    try:
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        logging.info("程序被用户中断")
        ws.is_running = False
        ws.close()


if __name__ == '__main__':
    main()
```

### 7.2 从音频文件识别

```python
import json
import base64
import time
import websocket
import ssl

def transcribe_audio_file(APPID, APIKey, APISecret, audio_file):
    """
    从音频文件进行语音识别

    Args:
        APPID: 讯飞应用ID
        APIKey: API密钥
        APISecret: API密钥
        audio_file: 音频文件路径（PCM 16kHz 16bit 单声道）
    """
    # 生成鉴权URL（使用上面的WsParam类）
    ws_param = WsParam(APPID, APIKey, APISecret)
    ws_url = ws_param.create_url()

    results = []

    def on_message(ws, message):
        msg = json.loads(message)
        if msg.get('code') == 0:
            data = msg.get('data', {}).get('result', {})
            ws_data = data.get('ws', [])
            for ws_item in ws_data:
                for cw in ws_item.get('cw', []):
                    results.append(cw.get('w', ''))
            print(f'识别结果: {"".join(results)}')

    def on_error(ws, error):
        print(f'错误: {error}')

    def on_close(ws, close_status_code, close_msg):
        print(f'连接关闭')
        print(f'最终结果: {"".join(results)}')

    def on_open(ws):
        frame_size = 1280  # 每次发送1280字节
        interval = 0.04

        with open(audio_file, 'rb') as fp:
            status = STATUS_FIRST_FRAME

            while True:
                buf = fp.read(frame_size)

                if not buf:
                    # 发送结束帧
                    d = {
                        'data': {
                            'status': 2,
                            'format': 'audio/L16;rate=16000',
                            'audio': '',
                            'encoding': 'raw'
                        }
                    }
                    ws.send(json.dumps(d))
                    break

                # 发送音频帧
                if status == STATUS_FIRST_FRAME:
                    d = {
                        'common': ws_param.CommonArgs,
                        'business': ws_param.BusinessArgs,
                        'data': {
                            'status': 0,
                            'format': 'audio/L16;rate=16000',
                            'audio': str(base64.b64encode(buf).decode('utf-8')),
                            'encoding': 'raw'
                        }
                    }
                    status = STATUS_CONTINUE_FRAME
                else:
                    d = {
                        'data': {
                            'status': 1,
                            'format': 'audio/L16;rate=16000',
                            'audio': str(base64.b64encode(buf).decode('utf-8')),
                            'encoding': 'raw'
                        }
                    }

                ws.send(json.dumps(d))
                time.sleep(interval)

    # 创建WebSocket连接
    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open

    # 运行
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
```

### 7.3 安装依赖

```bash
pip install websocket-client pyaudio ws4py
```

> 注意: PyAudio在Windows上可能需要先安装portaudio库

---

## 参考文档

- [语音听写（流式版）WebAPI 文档](https://www.xfyun.cn/doc/asr/voicedictation/API.html)
- [实时语音转写(标准版)API文档](https://www.xfyun.cn/doc/asr/rtasr/API.html)
- [WebSocket协议通用鉴权URL生成说明](https://www.xfyun.cn/doc/spark/general_url_authentication.html)
- [错误码查询](https://www.xfyun.cn/document/error-code)
- [讯飞开放平台](https://www.xfyun.cn)
- [星火大模型Python SDK](https://github.com/iflytek/spark-ai-python)
