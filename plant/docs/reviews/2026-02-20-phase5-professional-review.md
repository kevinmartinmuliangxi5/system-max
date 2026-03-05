# ZenGarden AI — Phase 5 专业审查综合报告

**审查日期**: 2026-02-20
**项目版本**: V8.0 "灵韵版"
**审查维度**: TypeScript质量 · 安全哨兵 · 性能分析
**总评分**: 5.7 / 10（三维平均）

---

## 审查评分概览

| 审查维度 | 评分 | 主要问题 |
|---------|------|---------|
| TypeScript 代码质量 | 6.2 / 10 | 严重重复代码、类型安全漏洞 |
| 安全哨兵 | 5.5 / 10 | RLS权限漏洞、速率限制可绕过 |
| 性能分析 | 5.5 / 10 | Bundle过大、无代码分割、动画性能差 |

---

## 一、Critical 级别问题（必须立即修复）

### [TS-C1] 代码重复：Hook 和 Screen 组件完全复制

**影响文件**:
- `hooks/usePlantIdentification.ts`（两个 Hook 184行中160行重复）
- `components/screens/plant-id-screen.tsx` + `feng-shui-screen.tsx`（上传区域 JSX 完全相同）

**问题**: `usePlantIdentification` 和 `useFengShuiAnalysis` 除调用不同 API 外逻辑完全相同。两个 Screen 的拖拽上传区域完全复制。

**修复方案**:
```typescript
// 提取通用 useImageAnalysis hook
function useImageAnalysis<T>({ analyzeFile, errorMessage }: UseImageAnalysisOptions<T>) {
  // 统一实现验证、压缩、预览、清理逻辑...
}

// 具体 hook 变成简单包装
export function usePlantIdentification() {
  return useImageAnalysis<PlantIdentification>({
    analyzeFile: identifyPlant,
    errorMessage: '识别失败，请重试',
  });
}
```

---

### [SEC-C1] plant_library INSERT 策略允许任意数据注入

**文件**: `supabase/schema.sql` 第147行

```sql
-- 危险：任何认证用户（含匿名）可写入任意数据
create policy "Authenticated insert" on plant_library
  for insert to authenticated
  with check (true);  -- "true" 无任何字段约束
```

**风险**: 任何用户可伪造植物名称、设置 `verified=true` 绕过审核、伪造他人的 discovered_by。

**修复**:
```sql
-- 仅允许 service_role (Edge Function 服务端) 执行插入
drop policy if exists "Authenticated insert" on plant_library;
create policy "Service role only insert" on plant_library
  for insert to service_role with check (true);
```

---

### [SEC-C2] 速率限制在 DB 查询失败时自动放行（Fail-Open）

**文件**: `supabase/functions/ai-processor/index.ts` 第158行

```typescript
if (error) {
  // Allow on error to avoid blocking legitimate users
  return { allowed: true, remaining: limit }  // 数据库异常时直接放行！
}
```

**修复**: 改为 Fail-Closed（失败时拒绝请求）。

---

### [SEC-C3] SECURITY DEFINER 函数缺少 search_path（Schema 劫持风险）

**文件**: `supabase/schema.sql` 第101行

```sql
-- 修复前
$$ language plpgsql security definer;

-- 修复后
$$ language plpgsql security definer
   set search_path = public, pg_temp;  -- 关键：固定搜索路径
```

---

### [PERF-C1] 所有屏幕同步加载，无代码分割

**文件**: `app/page.tsx` 第6-10行

```typescript
// 当前：全量同步加载，首屏 JS 包含所有屏幕代码
import { PlantIdScreen } from "@/components/screens/plant-id-screen";
import { FengShuiScreen } from "@/components/screens/feng-shui-screen";
import { ArEditorScreen } from "@/components/screens/ar-editor-screen";
import { CeremonyScreen } from "@/components/screens/ceremony-screen";
```

**影响**: 首屏 JS 体积增加 ~150-200KB，FCP 延迟 300-600ms（中端移动设备）。

**修复**:
```typescript
import dynamic from "next/dynamic";
const PlantIdScreen = dynamic(
  () => import("@/components/screens/plant-id-screen").then(m => ({ default: m.PlantIdScreen })),
  { loading: () => <ScreenSkeleton />, ssr: false }
);
```

---

### [PERF-C2] Ceremony Screen 中 Math.random() 在 JSX 渲染时调用

**文件**: `components/screens/ceremony-screen.tsx`

35个动画节点在每次 re-render 时重新生成随机值，导致 Framer Motion 重新启动所有动画，低端设备严重卡顿。

**修复**: 在 `useEffect` 中一次性生成随机值并冻结，作为 props 传入粒子组件。

---

### [PERF-C3] 安装了 26 个 Radix UI 包但大量未使用

**文件**: `package.json`

同时安装了 `recharts`、`embla-carousel-react`、`react-day-picker`、`cmdk`、`vaul`、`input-otp` 等在现有 5 个屏幕中无直接使用的重型依赖。

**预计 Bundle 增量**: 约 200-350KB（gzip 前）。

---

## 二、High 级别问题（本周处理）

### TypeScript

| ID | 文件 | 问题 | 修复优先级 |
|----|------|------|-----------|
| TS-H1 | `lib/supabase/client.ts` | `onAuthStateChange` 使用 `unknown` 类型，应用 Supabase 精确类型 | P1 |
| TS-H2 | `lib/types/index.ts` | `ApiResponse<T>` 允许 data 和 error 同时存在，应改为判别联合类型 | P1 |
| TS-H3 | `ceremony-screen.tsx` | `handleShare` 错误处理丢弃非 AbortError 异常 | P1 |
| TS-H4 | `ceremony-screen.tsx` | 使用 `alert()` 而非 toast（已安装 sonner 库） | P1 |
| TS-H5 | `ar-editor-screen.tsx` | 整个组件是功能存根但无任何 TODO 标注，`constraintsRef` 类型缺失 | P1 |

### 安全

| ID | 文件 | 问题 |
|----|------|------|
| SEC-H1 | `next.config.mjs` | 缺少 Content-Security-Policy 和 HSTS 头 |
| SEC-H2 | `supabase/schema.sql` | 匿名用户可无限制向 plant_candidates 写入垃圾数据 |
| SEC-H3 | `ai-processor/index.ts` | Edge Function 应使用 SERVICE_ROLE_KEY 而非 ANON_KEY |
| SEC-H4 | `lib/api/plant-service.ts` | 文件上传仅验证 MIME 类型，未检查 Magic Bytes（可伪造） |
| SEC-H5 | `ai-processor/index.ts` | Base64 图片内容未在服务端验证格式 |
| SEC-H6 | `supabase/schema.sql` | api_usage_log 缺少 INSERT RLS 策略，日志写入可能静默失败 |

### 性能

| ID | 文件 | 问题 |
|----|------|------|
| PERF-H1 | `plant-id-screen.tsx` + `feng-shui-screen.tsx` | 使用原生 `<img>` 标签，绕过 Next.js 图片优化 |
| PERF-H2 | `ar-editor-screen.tsx` | 无限循环动画在后台 Tab 仍持续运行，耗费 GPU |
| PERF-H3 | `lib/api/quota-manager.ts` | 每次 API 调用触发 4 次 Supabase 查询（无缓存） |
| PERF-H4 | `lib/api/plant-service.ts` | Canvas 压缩后未调用 `canvas.width = 0` 释放 GPU 内存 |

---

## 三、Medium 级别问题（两周内处理）

### TypeScript

- `app/page.tsx`: `renderScreen` 的 switch 缺少 `assertNever` 穷举守卫
- `app/page.tsx`: `TabId` 类型定义在入口文件内联，应导出到 `lib/types`
- `lib/types/index.ts`: `EnvironmentLevel` 应从 `EnvironmentTags` 值中派生，而非手动同步
- `lib/types/index.ts`: 两个文件中 `Profile` 类型命名冲突
- `feng-shui-screen.tsx`: 内联嵌套三元映射，应改为 `ENV_KEY_LABELS` 常量

### 安全

- `chart.tsx` 第80行: `dangerouslySetInnerHTML` 注入未经转义的 CSS（chart id 和 color 值）
- 匿名用户速率限制仅按 userId，清除 Cookie 即可重置
- `plant_candidates` 缺少 UPDATE/DELETE 策略（用户无法撤回提交）
- `plant_library` 公开读取暴露用户 UUID（discovered_by 字段）
- `lib/supabase/client.ts`: 缺少环境变量时用占位符代替，应 Fail-Fast

### 性能

- `app/page.tsx`: `renderScreen()` 内联函数每次渲染重建，应 `useMemo` 包装
- `plant-id-screen.tsx`: 事件处理器未用 `useCallback`，每次 dragActive 变化触发重建
- `hooks/usePlantIdentification.ts`: `previewUrl` 作为 useCallback 依赖导致函数频繁重建
- `supabase/schema.sql`: `plant_candidates` 缺少名称查询索引，无向量索引规划

---

## 四、跨模块架构问题

**[架构断裂] FengShuiScreen 与 ArEditorScreen 之间无数据传递**

风水分析获得的 `fengShuiAdvice`（包含财位/健康位坐标）应流转到 AR 编辑器，但两组件完全隔离。AR 编辑器使用的是硬编码的假数据，功能上是断开的。

**[缺少全局状态] 所有 Screen 组件完全孤立**

无 React Context 或 Zustand，PlantIdScreen 的识别结果、FengShuiScreen 的分析结果无法跨组件共享。随功能完善，这将是最大的架构障碍。

---

## 五、npm 依赖漏洞

```
16 vulnerabilities (4 moderate, 12 high)
- ajv < 8.18.0: ReDoS 漏洞（仅 devDependencies，不影响生产）
- minimatch < 10.2.1: ReDoS 漏洞（仅 devDependencies）

修复命令:
npm audit fix          # 安全修复
npm audit fix --force  # 包含破坏性变更的修复
```

---

## 六、综合优先修复清单

### P0 - 本周必须完成

| # | 问题 | 文件 |
|---|------|------|
| 1 | plant_library INSERT RLS 策略漏洞 | `schema.sql` |
| 2 | 速率限制 Fail-Open → Fail-Closed | `ai-processor/index.ts` |
| 3 | Edge Function 改用 SERVICE_ROLE_KEY | `ai-processor/index.ts` |
| 4 | SECURITY DEFINER 添加 search_path | `schema.sql` |
| 5 | 屏幕懒加载（Dynamic Import） | `app/page.tsx` |
| 6 | Supabase client 缺少环境变量时 Fail-Fast | `lib/supabase/client.ts` |

### P1 - 两周内完成

| # | 问题 | 文件 |
|---|------|------|
| 7 | 提取 useImageAnalysis 通用 Hook | `hooks/usePlantIdentification.ts` |
| 8 | 提取 ImageUploadArea 通用组件 | `components/screens/*.tsx` |
| 9 | 修复 ceremony-screen Math.random 动画 | `ceremony-screen.tsx` |
| 10 | 清理未使用重型依赖（recharts等） | `package.json` |
| 11 | 添加 CSP 和 HSTS 安全头 | `next.config.mjs` |
| 12 | 文件上传 Magic Bytes 验证 | `plant-service.ts` |
| 13 | Quota Manager 添加 30s 内存缓存 | `quota-manager.ts` |
| 14 | alert() 替换为 toast | `ceremony-screen.tsx` |

### P2 - 下一个迭代

| # | 问题 |
|---|------|
| 15 | FengShuiScreen → ArEditorScreen 数据流设计 |
| 16 | 全局状态管理方案（React Context 或 Zustand） |
| 17 | Canvas 粒子化（替代 50+ Framer Motion 节点） |
| 18 | AR 编辑器后台动画暂停（visibilitychange） |
| 19 | plant_candidates 补充 RLS 策略和触发器限频 |
| 20 | 补充 pgvector 向量索引规划 |

---

## 七、OWASP Top 10 合规状态

| OWASP | 类别 | 状态 |
|-------|------|------|
| A01 | 权限控制失效 | 违规 - plant_library INSERT 策略过宽 |
| A02 | 密码学失败 | 合规 - JWT 通过 Header 传输 |
| A03 | 注入攻击 | 合规 - 使用参数化查询 |
| A04 | 不安全设计 | 违规 - 客户端速率限制无法作为安全边界 |
| A05 | 安全配置错误 | 违规 - 缺少 CSP/HSTS |
| A06 | 易受攻击组件 | 违规 - 16 个已知 npm 漏洞 |
| A07 | 认证授权失败 | 部分违规 - 匿名用户可滥用 plant_candidates |
| A08 | 数据完整性失败 | 部分违规 - 图片内容验证不足 |
| A09 | 安全日志监控失败 | 违规 - api_usage_log 缺少 INSERT RLS |
| A10 | SSRF | 低风险 - image_url 写入未校验域名 |

---

## 八、优势与亮点（保留的良好实践）

- JWT 通过 Bearer Header 传递，服务端验证用户身份，不信任客户端传来的 userId
- Gemini API Key 通过 `x-goog-api-key` 请求头传递，未暴露在 URL 中
- AI 响应有结构验证（`validatePlantIdentification`、`validateFengShuiAnalysis`）
- 图片预览 URL 有完整的生命周期管理（`revokeObjectURL` 在 unmount 时清理）
- Supabase RLS 基础架构完整（tables + basic policies），方向正确
- `lib/utils.ts` 代码精简，评分 9.5/10，作为参考标准
- `home-screen.tsx` 代码质量最佳，评分 8/10
- `.env.local` 已正确加入 `.gitignore`

---

*报告生成: 2026-02-20 by Phase 5 专业审查 (kieran-typescript-reviewer + security-sentinel + performance-oracle)*
