# API 定义（RESTful + GraphQL）

- 基于文档：`docs/PRD.md`、`docs/tech-stack.md`
- 文档范围：MVP（移动端直连 SiliconFlow，无业务后端）
- 认证原则：发布态 BYOK，客户端从 `SecureStore` 读取用户 Key，直接请求上游 API

## 1. 认证与通用约定

### 1.1 认证方式
1. 类型：`Bearer Token`
2. Header：`Authorization: Bearer <SILICONFLOW_API_KEY>`
3. 来源：用户在 App 内输入后保存在系统安全存储（iOS Keychain / Android Keystore）
4. 禁止：
- 不得把 Key 上传到业务服务端
- 不得在日志输出完整 Key（仅前 3 后 2 掩码）

### 1.2 通用 Header
- `Content-Type: application/json`
- `Accept: application/json`
- `X-Request-Id: <uuid>`（建议）

### 1.3 通用错误体（建议）
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "请求较多，已自动重试",
    "request_id": "req_123",
    "retryable": true
  }
}
```

### 1.4 状态码约定
- `200`：成功
- `400`：请求参数错误（不重试）
- `401`：Key 无效或缺失（不重试）
- `429`：限流（指数退避，最多 3 次）
- `500`：服务端错误（可重试）
- `503`：服务不可用（指数退避，最多 3 次）
- `504`：网关超时（重试 2 次）

## 2. RESTful API（MVP 采用）

> Base URL：`https://api.siliconflow.cn`

### 2.1 Prompt 增强

- URL：`/v1/chat/completions`
- Method：`POST`
- 认证：`Bearer` 必需
- 用途：对用户提示词进行结构化增强

请求体（示例）：
```json
{
  "model": "deepseek-ai/DeepSeek-V3",
  "messages": [
    {"role": "system", "content": "你是图像提示词优化助手"},
    {"role": "user", "content": "生成一个赛博朋克风格的猫"}
  ],
  "temperature": 0.7
}
```

响应体（示例）：
```json
{
  "id": "chatcmpl_001",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "deepseek-ai/DeepSeek-V3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "ultra detailed cyberpunk cat, neon city..."
      },
      "finish_reason": "stop"
    }
  ]
}
```

状态码：`200/400/401/429/500/503/504`

### 2.2 图片生成（文生图 / 图生图 / 局部重绘）

- URL：`/v1/images/generations`
- Method：`POST`
- 认证：`Bearer` 必需
- 用途：统一处理文生图、图生图、Mask 重绘

请求体（文生图示例）：
```json
{
  "model": "black-forest-labs/FLUX.1-Kontext-pro",
  "prompt": "ultra detailed cyberpunk cat, neon city",
  "size": "1024x1024",
  "response_format": "b64_json"
}
```

请求体（图生图/局部重绘示例）：
```json
{
  "model": "black-forest-labs/FLUX.1-Kontext-pro",
  "prompt": "把猫的眼睛改成蓝色霓虹",
  "image": "<base64_or_upstream_supported_ref>",
  "mask": "<base64_mask>",
  "response_format": "b64_json"
}
```

响应体（示例）：
```json
{
  "created": 1700000000,
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ]
}
```

状态码：`200/400/401/429/500/503/504`

实现约束：
1. `b64_json` 仅短生命周期存在，必须立刻落盘为 `file://` URI。
2. 数据库禁止持久化 Base64 原文。

## 3. GraphQL API（可选，非 MVP 必需）

> 说明：MVP 不引入业务后端。以下 GraphQL 定义用于未来扩展（如本地网关或自建 BFF）。

- URL：`/graphql`
- Method：`POST`
- 认证：
1. 调用生成能力的 Mutation 必须带 `Bearer` Key
2. 纯本地查询可不要求远端认证（由客户端本地鉴权策略控制）

### 3.1 Schema（SDL）

```graphql
scalar Timestamp

enum MessageRole {
  system
  user
  assistant
}

enum MessageStatus {
  pending
  running
  succeeded
  failed
  cancelled
}

enum RequestType {
  prompt_enhance
  image_generation
  image_edit
}

type Conversation {
  id: ID!
  title: String!
  createdAt: Timestamp!
  updatedAt: Timestamp!
  archivedAt: Timestamp
  messages(limit: Int = 50, offset: Int = 0): [Message!]!
}

type Message {
  id: ID!
  conversationId: ID!
  parentMessageId: ID
  role: MessageRole!
  text: String
  imageUri: String
  maskUri: String
  model: String
  status: MessageStatus!
  errorCode: String
  width: Int
  height: Int
  createdAt: Timestamp!
  updatedAt: Timestamp!
}

type RequestLog {
  id: ID!
  conversationId: ID
  messageId: ID
  requestType: RequestType!
  provider: String!
  model: String
  requestId: String
  statusCode: Int
  retryCount: Int!
  durationMs: Int!
  costEstimate: Float!
  success: Boolean!
  errorCode: String
  createdAt: Timestamp!
}

type ReplayLog {
  id: ID!
  requestLogId: ID
  requestType: RequestType!
  maskedPrompt: String!
  errorCode: String!
  statusCode: Int
  createdAt: Timestamp!
}

type Query {
  conversations(limit: Int = 20, offset: Int = 0): [Conversation!]!
  conversation(id: ID!): Conversation
  requestLogs(limit: Int = 50, offset: Int = 0, requestType: RequestType): [RequestLog!]!
  replayLogs(limit: Int = 50, offset: Int = 0): [ReplayLog!]!
}

input GenerateImageInput {
  conversationId: ID!
  prompt: String!
  size: String = "1024x1024"
}

input EditImageInput {
  conversationId: ID!
  sourceImageUri: String!
  maskUri: String!
  prompt: String!
}

input EnhancePromptInput {
  conversationId: ID!
  rawPrompt: String!
}

type Mutation {
  enhancePrompt(input: EnhancePromptInput!): Message!
  generateImage(input: GenerateImageInput!): Message!
  editImage(input: EditImageInput!): Message!
  retryMessage(messageId: ID!): Message!
  archiveConversation(id: ID!): Boolean!
}
```

### 3.2 GraphQL 状态与错误
1. HTTP 状态码：
- 成功返回 `200`
- 认证失败可返回 `401`
- 限流可返回 `429`
2. GraphQL 错误结构（示例）：
```json
{
  "errors": [
    {
      "message": "rate limited",
      "extensions": {
        "code": "RATE_LIMITED",
        "retryable": true,
        "httpStatus": 429
      }
    }
  ],
  "data": null
}
```

## 4. MVP 推荐执行结论

1. 生产采用 REST 直连 SiliconFlow（与 PRD 一致）。
2. GraphQL 仅作为后续扩展定义保留，不作为 MVP 上线阻断项。
3. 契约校验使用 `zod`/JSON Schema 在客户端执行，校验失败不入库不渲染。
