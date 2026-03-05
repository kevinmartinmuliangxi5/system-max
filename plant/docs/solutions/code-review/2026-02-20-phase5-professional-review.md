---
title: "ZenGarden AI Phase 5 专业审查：Critical 问题解决方案"
date: 2026-02-20
category: code-review
severity: medium
status: documented
project: zengarden-ai
tags:
  - typescript
  - security
  - performance
  - rls
  - supabase
  - next.js
  - code-splitting
  - fail-closed
  - security-definer
  - code-duplication
related_docs:
  - docs/solutions/security-issues/edge-function-jwt-cors-security.md
  - docs/solutions/best-practices/zengarden-zero-marginal-cost-architecture.md
  - docs/plans/2026-02-15-feat-zengarden-fullstack-implementation-plan.md
  - docs/reviews/2026-02-20-phase5-professional-review.md
reviewers:
  - kieran-typescript-reviewer
  - security-sentinel
  - performance-oracle
scores:
  typescript: 6.2
  security: 5.5
  performance: 5.5
  overall: 5.7
---

# ZenGarden AI Phase 5 专业审查：Critical 问题解决方案

**项目**: ZenGarden AI (灵犀园) V8.0 "灵韵版"
**审查日期**: 2026-02-20
**总评分**: 5.7 / 10

完整原始报告: [`docs/reviews/2026-02-20-phase5-professional-review.md`](../reviews/2026-02-20-phase5-professional-review.md)

---

## 问题症状

Phase 5 专业审查发现以下**可观测症状**：

1. **安全**: 任何已认证用户（含匿名）可向 `plant_library` 写入任意伪造数据，包括设置 `verified=true` 绕过内容审核
2. **安全**: 数据库查询失败时速率限制自动放行，可通过制造 DB 超时绕过 API 限额
3. **安全**: SECURITY DEFINER 函数未固定 `search_path`，存在 Schema 劫持风险
4. **性能**: 首屏加载全部 5 个 Screen 组件代码，FCP 延迟 300-600ms（中端移动设备）
5. **性能**: `ceremony-screen.tsx` 中 35 个动画节点每次 re-render 生成新随机值，低端设备严重卡顿
6. **TypeScript**: `usePlantIdentification` 和 `useFengShuiAnalysis` 两个 Hook 的 184 行代码中有约 160 行完全重复
7. **构建**: `npm run build` 在未显式设置 `NEXT_TURBOPACK_EXPERIMENTAL_USE_SYSTEM_TLS_CERTS=1` 时失败（Google Fonts 解析错误）

---

## 根本原因分析

### [安全] RLS 策略过于宽泛

`plant_library` 的 INSERT 策略使用 `with check (true)`，对任何已认证用户（含 Supabase 匿名账户）无任何字段约束。数据插入应仅通过 Edge Function 服务端执行，客户端不应有直接写入权限。

### [安全] Fail-Open 设计缺陷

速率限制查询 DB 时若遇错误，当前实现返回 `allowed: true`（放行），这是典型的 Fail-Open 设计——在故障时比正常时更宽松。正确的安全默认应为 Fail-Closed：故障时拒绝请求。

### [安全] SECURITY DEFINER + 未固定 search_path

PostgreSQL `SECURITY DEFINER` 函数以函数所有者权限运行。若 `search_path` 未固定，攻击者可在 `public` schema 中创建同名函数，劫持函数执行路径实现权限提升。

### [性能] 同步全量 Import

`app/page.tsx` 用静态 `import` 加载所有屏幕，Next.js 无法自动进行代码分割。所有屏幕代码均打包进首屏 JS Bundle（额外约 150-200KB）。

### [性能] Math.random() 在渲染路径中

Framer Motion 的 `animate` prop 接受对象字面量，组件每次 re-render 时对象被重新创建。若对象包含 `Math.random()` 调用，动画的 `from` → `to` 目标值在每次渲染时变化，Framer Motion 会重新启动动画序列。

### [TypeScript] 缺乏抽象层

两个图像分析 Hook（植物识别、风水分析）的业务逻辑完全相同（验证、压缩、预览 URL 管理、清理），唯一区别是调用不同的 API 函数。缺乏通用 Hook 层导致 160 行代码重复。

### [构建] 环境变量依赖

`NEXT_TURBOPACK_EXPERIMENTAL_USE_SYSTEM_TLS_CERTS=1` 仅写入 `.env.local`，该文件仅在 `next dev` 时自动加载。`npm run build`（生产构建）和 CI/CD 环境不自动读取 `.env.local`，需要显式设置。

---

## 解决方案

### 修复 1：plant_library INSERT RLS 策略（SEC-C1）

**文件**: `supabase/schema.sql` 第 147 行

```sql
-- 删除过宽的策略
drop policy if exists "Authenticated insert" on plant_library;

-- 仅允许服务端（Edge Function 使用 service_role）执行插入
create policy "Service role only insert" on plant_library
  for insert to service_role with check (true);
```

**验证**: 用匿名/已认证客户端 JWT 尝试直接 INSERT，应收到 `permission denied` 错误。

---

### 修复 2：速率限制 Fail-Closed（SEC-C2）

**文件**: `supabase/functions/ai-processor/index.ts` 第 158 行

```typescript
// 修复前（Fail-Open — 危险）
if (error) {
  return { allowed: true, remaining: limit }
}

// 修复后（Fail-Closed — 安全默认）
if (error) {
  console.error('[RateLimit] DB query failed, denying request:', error.message)
  return { allowed: false, remaining: 0 }
}
```

**验证**: 模拟 DB 连接失败（如临时断开 DB），API 请求应返回 429 而非成功响应。

---

### 修复 3：Edge Function 改用 SERVICE_ROLE_KEY（SEC-H3）

**文件**: `supabase/functions/ai-processor/index.ts`

```typescript
// 修复前
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_ANON_KEY')!  // 受 RLS 约束
)

// 修复后
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!  // 绕过 RLS，仅服务端使用
)
```

**注意**: `SERVICE_ROLE_KEY` 永远不能暴露给客户端，仅限服务端 Edge Function 使用。

---

### 修复 4：SECURITY DEFINER 固定 search_path（SEC-C3）

**文件**: `supabase/schema.sql` 第 101 行（所有 SECURITY DEFINER 函数）

```sql
-- 修复前
$$ language plpgsql security definer;

-- 修复后（固定搜索路径，防止 schema 劫持）
$$ language plpgsql security definer
   set search_path = public, pg_temp;
```

**适用范围**: 检索所有 `security definer` 函数，全部添加此配置。

---

### 修复 5：屏幕懒加载（PERF-C1）

**文件**: `app/page.tsx`

```typescript
import dynamic from "next/dynamic"

// 骨架屏（首屏立即显示）
const ScreenSkeleton = () => (
  <div className="flex items-center justify-center h-full">
    <div className="animate-pulse bg-muted rounded-lg w-full h-64" />
  </div>
)

// 非首屏组件：延迟加载
const PlantIdScreen = dynamic(
  () => import("@/components/screens/plant-id-screen").then(m => ({ default: m.PlantIdScreen })),
  { loading: () => <ScreenSkeleton />, ssr: false }
)
const FengShuiScreen = dynamic(
  () => import("@/components/screens/feng-shui-screen").then(m => ({ default: m.FengShuiScreen })),
  { loading: () => <ScreenSkeleton />, ssr: false }
)
const ArEditorScreen = dynamic(
  () => import("@/components/screens/ar-editor-screen").then(m => ({ default: m.ArEditorScreen })),
  { loading: () => <ScreenSkeleton />, ssr: false }
)
const CeremonyScreen = dynamic(
  () => import("@/components/screens/ceremony-screen").then(m => ({ default: m.CeremonyScreen })),
  { loading: () => <ScreenSkeleton />, ssr: false }
)

// HomeScreen 保持静态 import（首屏）
import { HomeScreen } from "@/components/screens/home-screen"
```

**预期收益**: 首屏 JS Bundle 减少约 150-200KB，FCP 提升 300-600ms（中端移动设备）。

---

### 修复 6：Ceremony Screen 动画随机值（PERF-C2）

**文件**: `components/screens/ceremony-screen.tsx`

```typescript
// 修复前（每次 re-render 生成新随机值，触发动画重启）
const particles = Array.from({ length: 35 }, (_, i) => ({
  x: Math.random() * 100,  // 危险：JSX 渲染时调用
  y: Math.random() * 100,
  delay: Math.random() * 2,
}))

// 修复后（仅在 mount 时生成一次，并冻结）
const [particles] = useState(() =>
  Object.freeze(
    Array.from({ length: 35 }, () => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      delay: Math.random() * 2,
    }))
  )
)
```

或使用 `useRef` 确保跨渲染引用稳定：

```typescript
const particlesRef = useRef(
  Array.from({ length: 35 }, () => ({
    x: Math.random() * 100,
    y: Math.random() * 100,
    delay: Math.random() * 2,
  }))
)
```

---

### 修复 7：提取 useImageAnalysis 通用 Hook（TS-C1）

**新文件**: `hooks/useImageAnalysis.ts`

```typescript
interface UseImageAnalysisOptions<T> {
  analyzeFile: (file: File) => Promise<T>
  errorMessage: string
}

export function useImageAnalysis<T>({ analyzeFile, errorMessage }: UseImageAnalysisOptions<T>) {
  const [result, setResult] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [dragActive, setDragActive] = useState(false)

  // 统一实现：验证、压缩、预览 URL 管理、清理
  useEffect(() => {
    return () => { if (previewUrl) URL.revokeObjectURL(previewUrl) }
  }, [previewUrl])

  // ... 统一实现 handleFile, handleDrop, handleDragOver, reset
  return { result, isLoading, error, previewUrl, dragActive, handleFile, reset }
}

// 具体 Hook 变为简单包装（约 5 行）
export function usePlantIdentification() {
  return useImageAnalysis<PlantIdentification>({
    analyzeFile: identifyPlant,
    errorMessage: '识别失败，请重试',
  })
}

export function useFengShuiAnalysis() {
  return useImageAnalysis<FengShuiAnalysis>({
    analyzeFile: analyzeFengShui,
    errorMessage: '风水分析失败，请重试',
  })
}
```

**效果**: 消除约 160 行重复代码，bug 修复只需在一处进行。

---

### 修复 8：Supabase Client Fail-Fast（SEC-M5）

**文件**: `lib/supabase/client.ts`

```typescript
// 修复前（占位符回退，掩盖配置错误）
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co'
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-key'

// 修复后（明确失败，便于快速发现配置问题）
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseKey) {
  throw new Error(
    'Missing Supabase environment variables. ' +
    'Please set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in .env.local'
  )
}
```

---

## 构建环境说明

**症状**: `npm run build` 失败，21 个 Google Fonts 模块解析错误。

**根本原因**: `NEXT_TURBOPACK_EXPERIMENTAL_USE_SYSTEM_TLS_CERTS=1` 仅在 `.env.local` 中定义，该文件仅被 `next dev` 自动加载，`next build` 不会自动读取。

**CI/CD 修复**:
```bash
# 在 CI/CD pipeline 中显式设置
export NEXT_TURBOPACK_EXPERIMENTAL_USE_SYSTEM_TLS_CERTS=1
npm run build
```

**本地构建修复**:
```bash
# Windows CMD
set NEXT_TURBOPACK_EXPERIMENTAL_USE_SYSTEM_TLS_CERTS=1 && npm run build

# 或直接在 shell 中
NEXT_TURBOPACK_EXPERIMENTAL_USE_SYSTEM_TLS_CERTS=1 npm run build
```

**参考**: [Next.js Discussion #61886](https://github.com/vercel/next.js/discussions/61886)

---

## 验证证据（Phase 6 实际运行结果）

```
# TypeScript 编译检查
$ npx tsc --noEmit
→ 退出码: 0（无错误）✓

# ESLint 检查
$ npx eslint app/ components/screens/ lib/ hooks/ --ext .ts,.tsx
→ 7 warnings, 0 errors ✓
→ 警告项：unused vars (setPlantPosition, Download, err, Leaf, AlertCircle, supabase)

# 生产构建（需显式设置环境变量）
$ set NEXT_TURBOPACK_EXPERIMENTAL_USE_SYSTEM_TLS_CERTS=1 && npm run build
→ ✓ Compiled successfully in 1856.1ms
→ 4 static pages generated ✓
```

---

## 预防策略

### PR Review Checklist

在每个 PR 合并前检查：

**安全**
- [ ] 新增 RLS 策略是否使用了 `with check (true)` 不加任何字段约束？
- [ ] 所有 SECURITY DEFINER 函数是否有 `set search_path = public, pg_temp`？
- [ ] 错误处理分支是 Fail-Open 还是 Fail-Closed？（应为 Fail-Closed）
- [ ] 新的 Edge Function 是否使用 ANON_KEY 而非 SERVICE_ROLE_KEY？

**性能**
- [ ] 新增大型组件（>10KB）是否需要通过 `next/dynamic` 懒加载？
- [ ] 动画随机值是否在组件 mount 时一次性生成（而非每次渲染）？
- [ ] `package.json` 新增依赖是否真正使用？（警惕未使用的重型依赖）

**TypeScript**
- [ ] 新 Hook 与现有 Hook 是否有 70%+ 相同逻辑？应先抽象通用层
- [ ] 错误类型是 `unknown` 还是具体类型？（应用 `instanceof Error` 收窄）
- [ ] 环境变量访问是否有 Fail-Fast 检查而非占位符回退？

### 自动化防护

```typescript
// .eslintrc 添加规则防止代码重复（推荐安装 eslint-plugin-sonarjs）
{
  "rules": {
    "sonarjs/no-duplicate-string": "warn",
    "sonarjs/cognitive-complexity": ["warn", 15]
  }
}
```

```sql
-- 定期运行：检查是否有 SECURITY DEFINER 函数缺少 search_path
SELECT proname, prosrc
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
  AND p.prosecdef = true
  AND p.prosrc NOT LIKE '%search_path%';
```

---

## 跨模块架构问题（P2 待解决）

当前架构断裂：`FengShuiScreen` 的分析结果（财位/健康位坐标）未流转到 `ArEditorScreen`，后者使用硬编码假数据。

**推荐方案**: 在 `app/page.tsx` 中建立 React Context 或 Zustand store，共享：
- `plantIdentificationResult`: PlantIdScreen → CeremonyScreen
- `fengShuiAdvice`: FengShuiScreen → ArEditorScreen

参考: [零边际成本架构文档](../best-practices/zengarden-zero-marginal-cost-architecture.md)

---

## 相关文档

- [Edge Function JWT & CORS 安全](../security-issues/edge-function-jwt-cors-security.md)
- [ZenGarden 零边际成本架构最佳实践](../best-practices/zengarden-zero-marginal-cost-architecture.md)
- [Phase 5 完整审查原始报告](../../reviews/2026-02-20-phase5-professional-review.md)
- [ZenGarden 全栈实现计划](../../plans/2026-02-15-feat-zengarden-fullstack-implementation-plan.md)

---

## OWASP Top 10 违规状态（Phase 5 发现）

| OWASP | 类别 | 状态 | 修复引用 |
|-------|------|------|---------|
| A01 | 权限控制失效 | **违规** | 修复 1（RLS 策略） |
| A04 | 不安全设计 | **违规** | 修复 2（Fail-Closed） |
| A05 | 安全配置错误 | **违规** | `next.config.mjs` 缺 CSP/HSTS |
| A06 | 易受攻击组件 | **违规** | 16 个 npm 漏洞（run `npm audit fix`） |
| A09 | 安全日志监控失败 | **违规** | `api_usage_log` 缺 INSERT RLS |
| A02 | 密码学失败 | 合规 | JWT via Bearer Header |
| A03 | 注入攻击 | 合规 | 使用参数化查询 |

---

*文档生成: 2026-02-20 | /workflows:compound Phase 7 知识沉淀*
*审查团队: kieran-typescript-reviewer + security-sentinel + performance-oracle*
