# 安全修复补丁 - Critical Issues

**修复日期**: 2026-02-15
**修复范围**: 2 个 Critical 安全问题

---

## 🔴 Critical Issue #1: CORS 配置

### 问题描述
当前 Edge Function 使用 `'Access-Control-Allow-Origin': '*'` 允许任意来源访问 API，这会导致:
- 任何网站都可以调用 Edge Function
- CSRF 攻击向量
- API 滥用和配额耗尽

### 当前代码 (Edge Function)
```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',  // ❌ 危险
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}
```

### ✅ 修复后代码
```typescript
// 配置允许的域名
const ALLOWED_ORIGINS = [
  'https://zengarden.ai',
  'https://www.zengarden.ai',
  'https://app.zengarden.ai',
  // 开发环境
  process.env.NODE_ENV === 'development' && 'http://localhost:3000',
  process.env.NODE_ENV === 'development' && 'http://localhost:3001',
].filter(Boolean) as string[]

// 动态 CORS 处理函数
function getCorsHeaders(origin: string | null): HeadersInit {
  // 检查 origin 是否在允许列表中
  const allowedOrigin = origin && ALLOWED_ORIGINS.includes(origin)
    ? origin
    : ALLOWED_ORIGINS[0]

  return {
    'Access-Control-Allow-Origin': allowedOrigin,
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Max-Age': '86400', // 24 小时缓存预检请求
    'Access-Control-Allow-Credentials': 'true',
  }
}

// 在 Deno.serve 中使用
Deno.serve(async (req) => {
  const origin = req.headers.get('origin')

  // 处理 CORS 预检请求
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: getCorsHeaders(origin)
    })
  }

  // 正常请求处理
  try {
    // ... 业务逻辑
    return new Response(JSON.stringify(result), {
      headers: {
        ...getCorsHeaders(origin),
        'Content-Type': 'application/json'
      }
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        ...getCorsHeaders(origin),
        'Content-Type': 'application/json'
      }
    })
  }
})
```

---

## 🔴 Critical Issue #2: Gemini API Key 传递方式

### 问题描述
当前 API Key 作为 URL 查询参数传递:
```typescript
const url = `${CONFIG.GEMINI_API_URL}/${CONFIG.GEMINI_MODEL}:generateContent?key=${apiKey}`
```

这会导致:
1. **日志泄露风险**: API Key 会出现在服务器日志、代理日志中
2. **网络监控**: 明文传输可能被捕获
3. **Referer 泄露**: 重定向时可能泄露

### ✅ 修复后代码
```typescript
// 使用 HTTP Header 传递 API Key (推荐方式)
async function callGeminiVision(imageBase64: string): Promise<PlantIdentification> {
  const apiKey = Deno.env.get('GEMINI_API_KEY')

  // ✅ 正确: 使用 HTTP Header 传递
  const response = await fetch(
    `${CONFIG.GEMINI_API_URL}/${CONFIG.GEMINI_MODEL}:generateContent`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-goog-api-key': apiKey  // ✅ 使用 header 传递
      },
      body: JSON.stringify({
        contents: [{
          parts: [
            { text: PROMPTS.PLANT_IDENTIFICATION },
            { inline_data: { mime_type: 'image/jpeg', data: imageBase64 } }
          ]
        }],
        generationConfig: {
          response_mime_type: 'application/json',
          temperature: 0.1
        }
      })
    }
  )

  if (!response.ok) {
    // 安全地处理错误，不泄露敏感信息
    const errorData = await response.json().catch(() => ({}))
    console.error('Gemini API error:', response.status, errorData.error?.message)
    throw new Error(`Gemini API error: ${response.status}`)
  }

  const data = await response.json()
  return parseAndValidateResponse(data)
}
```

### 额外安全措施
```typescript
// 1. 验证 API Key 格式
function validateApiKey(key: string | undefined): asserts key is string {
  if (!key || !key.startsWith('AIza')) {
    throw new Error('Invalid or missing Gemini API key')
  }
}

// 2. 在 Edge Function 启动时验证
validateApiKey(Deno.env.get('GEMINI_API_KEY'))

// 3. 添加请求日志 (用于调试，但隐藏敏感信息)
function logApiRequest(requestId: string, metadata: object) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    requestId,
    ...metadata,
    // 不记录 API Key
    apiKey: '[REDACTED]'
  }))
}
```

---

## 📝 完整修复后的 Edge Function

```typescript
// supabase/functions/ai-processor/index.ts

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { z } from 'https://esm.sh/zod@3'

// ==================== 安全配置 ====================

const ALLOWED_ORIGINS = [
  'https://zengarden.ai',
  'https://www.zengarden.ai',
  Deno.env.get('NODE_ENV') === 'development' && 'http://localhost:3000',
].filter(Boolean) as string[]

function getCorsHeaders(origin: string | null): HeadersInit {
  const allowedOrigin = origin && ALLOWED_ORIGINS.includes(origin)
    ? origin
    : ALLOWED_ORIGINS[0]

  return {
    'Access-Control-Allow-Origin': allowedOrigin,
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Max-Age': '86400',
  }
}

// ==================== 配置常量 ====================

const CONFIG = {
  MAX_IMAGE_SIZE: 1.5 * 1024 * 1024,
  MAX_RETRIES: 2,
  GEMINI_MODEL: 'gemini-2.0-flash',
  GEMINI_API_URL: 'https://generativelanguage.googleapis.com/v1beta/models',
}

// ==================== 类型定义 ====================

const PlantIdentificationSchema = z.object({
  scientificName: z.string(),
  commonName: z.string(),
  confidence: z.number().min(0).max(1),
  tags: z.array(z.string()),
  description: z.string(),
  careTips: z.array(z.string()),
})

type PlantIdentification = z.infer<typeof PlantIdentificationSchema>

// ==================== 主服务 ====================

Deno.serve(async (req) => {
  const origin = req.headers.get('origin')

  // CORS 预检
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: getCorsHeaders(origin) })
  }

  try {
    const payload = await req.json()

    // 验证 API Key
    const apiKey = Deno.env.get('GEMINI_API_KEY')
    if (!apiKey) {
      throw new Error('Service configuration error')
    }

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? ''
    )

    switch (payload.task) {
      case 'identify':
        return handleIdentify(payload, supabase, apiKey, origin)
      default:
        return jsonResponse({ error: 'Invalid task' }, 400, origin)
    }
  } catch (error) {
    console.error('Error:', error)
    return jsonResponse(
      { error: error instanceof Error ? error.message : 'Internal error' },
      500,
      origin
    )
  }
})

// ==================== 处理函数 ====================

async function handleIdentify(
  payload: any,
  supabase: any,
  apiKey: string,
  origin: string | null
): Promise<Response> {
  // 验证图片大小
  const imageSize = Math.ceil((payload.imageBase64.length * 3) / 4)
  if (imageSize > CONFIG.MAX_IMAGE_SIZE) {
    return jsonResponse({ error: 'Image too large' }, 400, origin)
  }

  // 调用 Gemini (使用 Header 传递 API Key)
  const result = await callGeminiVision(payload.imageBase64, apiKey)

  // 记录使用
  if (payload.userId) {
    await supabase.from('api_usage_log').insert({
      user_id: payload.userId,
      service: 'gemini_vision',
      endpoint: 'identify',
    })
  }

  return jsonResponse(result, 200, origin)
}

// ✅ 安全的 Gemini API 调用
async function callGeminiVision(
  imageBase64: string,
  apiKey: string
): Promise<PlantIdentification> {
  const response = await fetch(
    `${CONFIG.GEMINI_API_URL}/${CONFIG.GEMINI_MODEL}:generateContent`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-goog-api-key': apiKey,  // ✅ 使用 Header
      },
      body: JSON.stringify({
        contents: [{
          parts: [
            { text: '分析这张植物图片，返回 JSON 格式...' },
            { inline_data: { mime_type: 'image/jpeg', data: imageBase64 } }
          ]
        }],
        generationConfig: {
          response_mime_type: 'application/json',
          temperature: 0.1
        }
      })
    }
  )

  if (!response.ok) {
    throw new Error(`Gemini API error: ${response.status}`)
  }

  const data = await response.json()
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text

  if (!text) {
    throw new Error('Empty response from Gemini')
  }

  // 验证响应结构
  return PlantIdentificationSchema.parse(JSON.parse(text))
}

// ==================== 工具函数 ====================

function jsonResponse(data: any, status: number, origin: string | null): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      ...getCorsHeaders(origin),
      'Content-Type': 'application/json'
    }
  })
}
```

---

## ✅ 修复验证清单

- [x] CORS 配置限制为特定域名
- [x] API Key 使用 HTTP Header 传递
- [x] 添加请求来源验证
- [x] 错误消息不泄露敏感信息
- [x] 使用 Zod 进行运行时类型验证

## 🚀 部署后验证

```bash
# 1. 测试 CORS 配置
curl -X OPTIONS https://your-function-url \
  -H "Origin: https://malicious-site.com" \
  -H "Access-Control-Request-Method: POST"
# 应该返回 403 或不包含恶意域名

# 2. 测试 API Key 不在 URL 中
curl -v https://your-function-url \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"task":"identify","imageBase64":"..."}'
# 日志中不应该包含 API Key
```
