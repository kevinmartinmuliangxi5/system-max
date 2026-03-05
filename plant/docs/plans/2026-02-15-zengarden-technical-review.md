---
title: ZenGarden AI 技术审查报告
date: 2026-02-15
reviewers:
  - kieran-typescript-reviewer
  - security-sentinel
  - performance-oracle
  - code-simplicity-reviewer
---

# ZenGarden AI 技术审查报告

## 执行摘要

| 审查维度 | 严重问题 | 中等问题 | 轻微问题 | 总体评级 |
|---------|---------|---------|---------|---------|
| **TypeScript/前端** | 4 | 5 | 3 | ⚠️ 需要改进 |
| **安全** | 2 | 5 | 3 | 🔴 高风险 |
| **性能** | 3 | 4 | 2 | ⚠️ 需要优化 |
| **代码简洁性** | - | - | - | 🟡 过度设计 |

**总体结论**: 计划架构合理，但需要修复 **2 个 Critical** 和 **4 个 High** 级别问题后方可部署。

---

## 🔴 Critical Issues (必须立即修复)

### 1. [SECURITY-001] CORS 配置允许任意来源
**文件**: Edge Function `corsHeaders`
**问题**: `'Access-Control-Allow-Origin': '*'` 允许任何网站调用 API
**修复**:
```typescript
const ALLOWED_ORIGINS = ['https://your-domain.com']
return { 'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0] }
```

### 2. [SECURITY-002] Gemini API Key 通过 URL 传递
**文件**: Edge Function `callGeminiVision`
**问题**: API Key 作为 URL 查询参数，会泄露到日志
**修复**: 使用 HTTP Header `x-goog-api-key` 传递

### 3. [TS-001] `any` 类型使用
**文件**: Edge Function `handleIdentify`, `handleAnalyze`
**问题**: 使用 `any` 类型绕过类型检查
**修复**: 导入 `SupabaseClient<Database>` 类型

### 4. [TS-002] Database 类型定义缺失
**文件**: `lib/supabase/types.ts`
**问题**: 引用了不存在的类型文件
**修复**: 创建完整的 Database 接口定义

---

## 🟠 High Issues (短期修复)

### 1. [SEC-003] 匿名用户缺少速率限制
**风险**: API 配额耗尽攻击
**修复**: 实现基于 IP + User Agent 的速率限制

### 2. [SEC-004] RLS 策略存在权限提升风险
**风险**: 任意数据注入到公共植物库
**修复**: 添加 credit_score 检查和数据验证触发器

### 3. [PERF-001] Canvas 压缩阻塞主线程
**影响**: 大图片处理时 UI 无响应
**修复**: 使用 WebWorker 或 OffscreenCanvas

### 4. [SIMPLE-001] 数据库 Schema 过度设计
**问题**: 多个未使用的字段和表
**建议移除**:
- `plant_candidates` 表
- `common_names jsonb` 字段
- `toxicity_info` 字段
- `care_requirements` 字段
- `description_embedding` (MVP 阶段)

---

## 📋 审查详细报告

### TypeScript/前端审查 (Kieran)

**主要发现**:
1. ✅ 架构设计良好，使用 React 19 + Next.js 16
2. ⚠️ 类型安全需要加强
3. ⚠️ 未使用 React 19 Actions 特性
4. ⚠️ 缺少运行时类型验证 (建议使用 Zod)

**推荐改进**:
```typescript
// 使用 Zod 进行运行时验证
const PlantIdentificationSchema = z.object({
  scientificName: z.string().min(1),
  commonName: z.string().min(1),
  confidence: z.number().min(0).max(1),
  tags: z.array(z.string()).max(5),
})
```

### 安全审查 (Security Sentinel)

**OWASP Top 10 合规性**:
| 类别 | 状态 |
|------|------|
| A01: Broken Access Control | ❌ FAIL |
| A02: Cryptographic Failures | ⚠️ WARN |
| A03: Injection | ⚠️ WARN |
| A05: Security Misconfiguration | ❌ FAIL |
| A07: Auth Failures | ⚠️ WARN |

**关键建议**:
1. 限制 CORS 来源
2. 完善 RLS 策略
3. 添加输入验证
4. 实现速率限制

### 性能审查 (Performance Oracle)

**性能预测**:
| 场景 | 当前 | 优化后 |
|------|------|--------|
| 首屏加载 (FCP) | 1.8-2.5s | 0.8-1.2s |
| API 响应 (缓存命中) | 2-3s | 0.3-0.5s |
| 图片压缩 | 阻塞主线程 | 后台处理 |

**关键优化建议**:
1. 使用 WebWorker 处理图片压缩
2. 实现多层缓存 (Memory → IndexedDB → API)
3. 动态导入屏幕组件
4. Edge Function 预热机制

### 简洁性审查 (Simplicity Reviewer)

**YAGNI 违反统计**: 10+ 处

**建议移除的功能**:
1. `plant_candidates` 表和投票系统
2. pgvector + HNSW 索引 (MVP 不需要)
3. 多语言 `common_names` 字段
4. 指数退避重试机制 (简单重试足够)
5. Framer Motion (CSS 动画替代)

**预计代码减少**: ~30% (约 170 行)

---

## 🛠 修复路线图

### 阶段 1: 部署前必须完成 (1-2 天)
- [ ] 修复 CORS 配置
- [ ] 修改 API Key 传递方式
- [ ] 完善 RLS 策略
- [ ] 创建 Database 类型定义
- [ ] 移除 `any` 类型

### 阶段 2: 短期修复 (1 周内)
- [ ] 实现速率限制
- [ ] 添加输入验证
- [ ] 使用 Zod 进行运行时类型验证
- [ ] 简化数据库 Schema

### 阶段 3: 性能优化 (2-4 周)
- [ ] WebWorker 图片处理
- [ ] 多层缓存实现
- [ ] 动态组件导入
- [ ] Edge Function 预热

---

## 📊 审查结论

**推荐行动**:
1. ✅ 计划整体架构合理，可以继续实施
2. ⚠️ 必须先修复 2 个 Critical 安全问题
3. ⚠️ 建议简化数据库 Schema，移除未使用的功能
4. 💡 考虑在 MVP 阶段移除 pgvector 功能

**风险评估**: 如果不修复 Critical 问题，可能导致:
- API 配额被滥用
- 数据被污染
- 用户数据泄露
- 服务中断

**下一步**:
1. 修复 Critical 问题后重新提交审查
2. 或者直接开始实施 `/workflows:work`，在实施过程中修复
