#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试GLM API响应格式"""

import sys
import io
import json
from anthropic import Anthropic

# 修复Windows控制台UTF-8输出
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

client = Anthropic(
    api_key="434698bbe0754202aabea54a1b6d184d.zPhgfbdAFrX46GDg",
    base_url="https://open.bigmodel.cn/api/anthropic"
)

print("测试GLM-4.7 API响应格式")
print("=" * 60)

# 测试需求分析
prompt = """你是一个专业的需求分析专家。

用户需求描述：
创建一个用户注册功能，支持邮箱验证

请执行需求开发分析，包括：
1. 深入理解需求意图
2. 提出3-5个关键澄清问题（具体、有针对性）
3. 识别功能性需求
4. 识别非功能性需求（性能、安全、可用性等）
5. 识别技术约束
6. 识别潜在风险

请以JSON格式返回：
{
    "understanding": "你对需求的理解总结",
    "questions": [
        "问题1：关于用户群体的问题",
        "问题2：关于功能范围的问题",
        "问题3：关于技术约束的问题"
    ],
    "requirements": {
        "functional": ["功能需求1", "功能需求2"],
        "non_functional": ["非功能需求1", "非功能需求2"],
        "constraints": ["约束1", "约束2"]
    },
    "risks": ["风险1", "风险2"]
}

请确保问题具体、有价值，避免泛泛而谈。
"""

print("\n发送请求...")
try:
    response = client.messages.create(
        model="glm-4.7",
        max_tokens=2000,
        temperature=0.3,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    content = response.content[0].text
    print("\n原始响应:")
    print("-" * 60)
    print(content)
    print("-" * 60)

    # 尝试解析JSON
    print("\n尝试解析JSON...")
    try:
        parsed = json.loads(content)
        print("✓ JSON解析成功！")
        print("\n解析结果:")
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    except json.JSONDecodeError as e:
        print(f"✗ JSON解析失败: {e}")
        print(f"  错误位置: 第{e.lineno}行，第{e.colno}列")
        print(f"  错误内容: {e.doc[max(0, e.pos-50):e.pos+50]}")

except Exception as e:
    print(f"API调用失败: {e}")
    import traceback
    traceback.print_exc()
