# AI 生图应用 TASKS 拆解（A 风格执行版）

我正在使用 writing-plans skill 来创建 implementation plan。

- 输入文档：`docs/PRD.md`、`docs/tech-stack.md`、`docs/db-schema.md`、`docs/api-spec.md`、`docs/ui-acceptance.md`
- 目标：将 MVP 拆成 2-5 分钟可执行任务
- 实现约束：TDD（先红后绿），本地化架构，无业务后端，BYOK

---

## Milestone 0：工程骨架与质量门禁

### Task 0.1：初始化 Expo TS 工程
**文件路径**
- Create: `package.json`
- Create: `app/_layout.tsx`
- Create: `app/index.tsx`

**代码片段**
```tsx
// app/index.tsx
import { Redirect } from 'expo-router';
export default function Index() {
  return <Redirect href="/chat" />;
}
```

**验证命令**
- `pnpm install`
- `pnpm expo start --offline`

### Task 0.2：创建路由占位页（A 风格 3 主页）
**文件路径**
- Create: `app/chat.tsx`
- Create: `app/editor.tsx`
- Create: `app/result.tsx`

**代码片段**
```tsx
// app/chat.tsx
import { View, Text } from 'react-native';
export default function ChatPage() { return <View><Text>A-Chat</Text></View>; }
```

**验证命令**
- `pnpm expo start --offline`
- 手工验证可从 `/chat` 跳转到 `/editor`、`/result`

### Task 0.3：配置 lint/typecheck 脚本
**文件路径**
- Modify: `package.json`
- Create: `tsconfig.json`

**代码片段**
```json
{
  "scripts": {
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "build": "expo export --platform all"
  }
}
```

**验证命令**
- `pnpm lint`
- `pnpm typecheck`

### Task 0.4：添加 Vitest 基线
**文件路径**
- Create: `vitest.config.ts`
- Create: `tests/smoke/smoke.test.ts`

**代码片段**
```ts
import { describe, it, expect } from 'vitest';
describe('smoke', () => it('runs', () => expect(true).toBe(true)));
```

**验证命令**
- `pnpm test`

---

## Milestone 1：契约与 API 层（REST 直连 SiliconFlow）

### Task 1.1：落地契约文件目录
**文件路径**
- Create: `contracts/prompt-enhance.response.schema.json`
- Create: `contracts/image-generation.response.schema.json`
- Create: `contracts/error.schema.json`

**代码片段**
```json
{"type":"object","required":["data"],"properties":{"data":{"type":"array"}}}
```

**验证命令**
- `pnpm test tests/contracts/contracts-parse.test.ts`

### Task 1.2：写失败测试（契约不通过应拦截）
**文件路径**
- Create: `tests/contracts/contract-gate.test.ts`

**代码片段**
```ts
expect(() => validateImageResponse({ foo: 1 })).toThrow();
```

**验证命令**
- `pnpm test tests/contracts/contract-gate.test.ts`
- 期望：FAIL（函数未实现）

### Task 1.3：实现契约校验器
**文件路径**
- Create: `src/contracts/validators.ts`

**代码片段**
```ts
import { z } from 'zod';
export const ImageResponseSchema = z.object({ data: z.array(z.object({ b64_json: z.string() })) });
export const validateImageResponse = (input: unknown) => ImageResponseSchema.parse(input);
```

**验证命令**
- `pnpm test tests/contracts/contract-gate.test.ts`
- 期望：PASS

### Task 1.4：实现 API 客户端（带 Authorization 注入）
**文件路径**
- Create: `src/api/client.ts`

**代码片段**
```ts
import axios from 'axios';
export const api = axios.create({ baseURL: 'https://api.siliconflow.cn', timeout: 20000 });
```

**验证命令**
- `pnpm test tests/api/client.test.ts`

### Task 1.5：实现重试策略（429/503/超时）
**文件路径**
- Create: `src/api/retry.ts`
- Create: `tests/api/retry-policy.test.ts`

**代码片段**
```ts
export const shouldRetry = (status?: number) => status === 429 || status === 503;
```

**验证命令**
- `pnpm test tests/api/retry-policy.test.ts`

### Task 1.6：实现 Prompt 增强接口调用
**文件路径**
- Create: `src/api/prompt.ts`

**代码片段**
```ts
return api.post('/v1/chat/completions', payload, { headers: { Authorization: `Bearer ${key}` } });
```

**验证命令**
- `pnpm test tests/api/prompt.test.ts`

### Task 1.7：实现图片生成接口调用
**文件路径**
- Create: `src/api/images.ts`

**代码片段**
```ts
return api.post('/v1/images/generations', payload, { headers: { Authorization: `Bearer ${key}` } });
```

**验证命令**
- `pnpm test tests/api/images.test.ts`

---

## Milestone 2：数据库与本地存储

### Task 2.1：引入 migration 执行器
**文件路径**
- Create: `src/db/migrate.ts`
- Copy: `db/migrations/0001_initial_schema.sql` -> `src/db/migrations/0001_initial_schema.sql`

**代码片段**
```ts
await db.execAsync(migrationSql);
```

**验证命令**
- `pnpm test tests/db/migrate.test.ts`

### Task 2.2：写会话仓储（conversations）
**文件路径**
- Create: `src/db/repositories/conversations.repo.ts`

**代码片段**
```ts
export async function createConversation(db, id: string, title: string) { /* insert */ }
```

**验证命令**
- `pnpm test tests/db/conversations.repo.test.ts`

### Task 2.3：写消息仓储（messages）
**文件路径**
- Create: `src/db/repositories/messages.repo.ts`

**代码片段**
```ts
export async function insertMessage(db, message) { /* insert with conversation_id */ }
```

**验证命令**
- `pnpm test tests/db/messages.repo.test.ts`

### Task 2.4：写请求日志仓储（request_logs）
**文件路径**
- Create: `src/db/repositories/request-logs.repo.ts`

**代码片段**
```ts
export async function insertRequestLog(db, log) { /* insert */ }
```

**验证命令**
- `pnpm test tests/db/request-logs.repo.test.ts`

### Task 2.5：写失败回放仓储与 N=50 淘汰
**文件路径**
- Create: `src/db/repositories/replay-logs.repo.ts`

**代码片段**
```ts
await db.runAsync('DELETE FROM replay_logs WHERE id NOT IN (SELECT id FROM replay_logs ORDER BY created_at DESC LIMIT 50)');
```

**验证命令**
- `pnpm test tests/db/replay-retention.test.ts`

### Task 2.6：实现 BYOK 安全存储封装
**文件路径**
- Create: `src/security/secure-key.ts`

**代码片段**
```ts
import * as SecureStore from 'expo-secure-store';
export const setApiKey = (k: string) => SecureStore.setItemAsync('siliconflow_api_key', k);
```

**验证命令**
- `pnpm test tests/security/secure-key.test.ts`

---

## Milestone 3：首图生成链路（Chat）

### Task 3.1：写失败测试（首图 3 步链路）
**文件路径**
- Create: `tests/flows/first-image.flow.test.ts`

**代码片段**
```ts
expect(result.status).toBe('succeeded');
expect(result.imageUri.startsWith('file://')).toBe(true);
```

**验证命令**
- `pnpm test tests/flows/first-image.flow.test.ts`
- 期望：FAIL

### Task 3.2：实现 Base64 落盘工具
**文件路径**
- Create: `src/storage/image-file.ts`

**代码片段**
```ts
const uri = `${FileSystem.cacheDirectory}${id}.png`;
await FileSystem.writeAsStringAsync(uri, b64, { encoding: FileSystem.EncodingType.Base64 });
```

**验证命令**
- `pnpm test tests/storage/image-file.test.ts`

### Task 3.3：实现首图 orchestrator
**文件路径**
- Create: `src/flows/generate-first-image.ts`

**代码片段**
```ts
const enhanced = await enhancePrompt(...);
const res = await generateImage(...);
const uri = await persistBase64Image(...);
```

**验证命令**
- `pnpm test tests/flows/first-image.flow.test.ts`
- 期望：PASS

### Task 3.4：接入 Chat 页面交互
**文件路径**
- Modify: `app/chat.tsx`
- Create: `src/stores/chat.store.ts`

**代码片段**
```tsx
<Button title="发送" onPress={onGenerate} />
```

**验证命令**
- `pnpm typecheck`
- 手工验证：输入提示词后显示结果卡

---

## Milestone 4：局部重绘链路（Editor）

### Task 4.1：写失败测试（局部重绘流程）
**文件路径**
- Create: `tests/flows/inpaint.flow.test.ts`

**代码片段**
```ts
expect(result.updatedImageUri).toMatch(/^file:\/\//);
```

**验证命令**
- `pnpm test tests/flows/inpaint.flow.test.ts`
- 期望：FAIL

### Task 4.2：实现 mask 文件读写工具
**文件路径**
- Create: `src/storage/mask-file.ts`

**代码片段**
```ts
export async function saveMask(uri: string, data: string) { /* write file */ }
```

**验证命令**
- `pnpm test tests/storage/mask-file.test.ts`

### Task 4.3：实现局部重绘 orchestrator
**文件路径**
- Create: `src/flows/inpaint-image.ts`

**代码片段**
```ts
const res = await generateImage({ prompt, image, mask, response_format: 'b64_json' });
```

**验证命令**
- `pnpm test tests/flows/inpaint.flow.test.ts`
- 期望：PASS

### Task 4.4：接入 Editor 页工具条与提交
**文件路径**
- Modify: `app/editor.tsx`

**代码片段**
```tsx
<Button title="应用" onPress={onApplyInpaint} />
```

**验证命令**
- `pnpm typecheck`
- 手工验证：选区 -> 输入指令 -> 返回新图 URI

---

## Milestone 5：结果页、合规、错误恢复

### Task 5.1：实现结果页动作（保存/继续编辑/重试）
**文件路径**
- Modify: `app/result.tsx`

**代码片段**
```tsx
<Button title="保存" onPress={onSave} />
```

**验证命令**
- 手工验证：三按钮均可触发对应动作

### Task 5.2：实现错误映射与统一文案
**文件路径**
- Create: `src/errors/map-error.ts`

**代码片段**
```ts
if (status === 429) return '请求较多，已自动重试';
```

**验证命令**
- `pnpm test tests/errors/map-error.test.ts`

### Task 5.3：实现日志脱敏
**文件路径**
- Create: `src/logging/redact.ts`

**代码片段**
```ts
export const maskKey = (k: string) => `${k.slice(0,3)}***${k.slice(-2)}`;
```

**验证命令**
- `pnpm test tests/logging/redact.test.ts`

### Task 5.4：实现 AIGC 标识导出占位
**文件路径**
- Create: `src/export/aigc-export.ts`

**代码片段**
```ts
export async function exportWithAigcMeta(uri: string) { return { uri, watermark: 'AI生成/AIGC' }; }
```

**验证命令**
- `pnpm test tests/export/aigc-export.test.ts`

---

## Milestone 6：验收与发布前门禁

### Task 6.1：补充 E2E 首图生成用例
**文件路径**
- Create: `e2e/first-image.e2e.ts`

**代码片段**
```ts
await expect(element(by.text('Result Center'))).toBeVisible();
```

**验证命令**
- `pnpm detox test e2e/first-image.e2e.ts`

### Task 6.2：补充 E2E 局部重绘用例
**文件路径**
- Create: `e2e/inpaint.e2e.ts`

**代码片段**
```ts
await expect(element(by.text('局部重绘面板'))).toBeVisible();
```

**验证命令**
- `pnpm detox test e2e/inpaint.e2e.ts`

### Task 6.3：补充 E2E 异常恢复用例
**文件路径**
- Create: `e2e/error-recovery.e2e.ts`

**代码片段**
```ts
await expect(element(by.text('请求较多，已自动重试'))).toBeVisible();
```

**验证命令**
- `pnpm detox test e2e/error-recovery.e2e.ts`

### Task 6.4：执行全量验收命令
**文件路径**
- Modify: `README.md`（新增验收命令段）

**代码片段**
```md
pnpm test
pnpm typecheck
pnpm lint
pnpm build
```

**验证命令**
- `pnpm test && pnpm typecheck && pnpm lint && pnpm build`

---

## Milestone DoD（每个里程碑都必须满足）

1. 功能与 PRD 对齐，无越界修改。
2. 新增/受影响测试通过。
3. `typecheck`/`lint`/`build` 通过。
4. 关键路径手工验证并记录证据（截图/日志）。
5. 输出：变更说明 + 验证证据 + 剩余风险。

---

## 建议执行顺序

1. M0 -> M1 -> M2（先搭底座）
2. M3 -> M4（核心链路）
3. M5（可用性与合规）
4. M6（验收收口）
