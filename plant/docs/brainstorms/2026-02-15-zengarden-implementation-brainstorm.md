---
date: 2026-02-15
topic: zengarden-implementation
---

# ZenGarden AI (灵犀园) 实现设计

## What We're Building

基于 **ZenGarden AI-PRD V8.0 (灵韵版)** 实现一个完整的园艺风水移动应用。该应用将：
- 使用 **Gemini 1.5 Flash** 进行植物视觉识别
- 使用 **Supabase** (Auth, DB, Storage, Edge Functions, pgvector) 作为后端
- 实现零边际成本架构（反脆弱设计）
- 提供仪式感用户体验

## Why This Approach

**技术选型理由：**
- **Gemini 1.5 Flash**: 免费、快速、支持视觉识别
- **Supabase Free Tier**: 提供 Auth + DB + Edge Functions + Realtime + pgvector
- **Framer Motion**: 实现仪式感动效
- **@imgly/background-removal**: 本地 WASM 抠图，无需后端

**现有 UI 骨架：**
- 已有 5 个屏幕组件 (Home, PlantID, FengShui, ArEditor, Ceremony)
- 已有 Tailwind 配置 (sage green, warm white, gold 颜色系统)
- 已有 Framer Motion 动画基础

## Key Decisions

1. **开发位置**: 在 `zen-garden-ui` 目录继续开发
2. **认证方式**: Supabase Auth + 匿名登录（降低使用门槛）
3. **API 配额管理**: 独立熔断机制，Gemini Vision 和 Embedding 分别计量
4. **降级策略**:
   - Vision 耗尽 → 手动标签输入
   - Embedding 耗尽 → 纯标签匹配
5. **荣誉系统**: 记录 `discovered_by` 用户 ID，在植物卡片底部显示

## Implementation Phases

### Phase 1: 数据库与基础设施
- [ ] 创建 Supabase 项目
- [ ] 执行 SQL Schema (api_usage_log, plant_library, plant_candidates, profiles)
- [ ] 启用 pgvector 扩展
- [ ] 插入 20 种常见植物种子数据
- [ ] 创建 `match_plants` RPC 函数

### Phase 2: Edge Functions (AI 网关)
- [ ] 创建 `ai-processor` Edge Function
- [ ] 实现 `identify` 任务 (自动晋升逻辑)
- [ ] 实现 `analyze` 任务 (结构化输出 + 异步 Embedding)
- [ ] 添加配额熔断逻辑

### Phase 3: 前端集成
- [ ] 配置 Supabase Client
- [ ] 实现真实 API 调用替换 Mock 数据
- [ ] 实现 WASM 抠图预加载
- [ ] 完善错误处理和降级 UI

### Phase 4: 仪式感体验
- [ ] 完善 CeremonyMoment 组件
- [ ] 实现光晕粒子效果
- [ ] 添加风水诗意文案模板

## Open Questions

- ~~Supabase 项目创建~~ → 需要指导
- ~~Gemini API Key~~ → 已获取

## Next Steps

→ 使用 `/workflows:plan` 生成详细的实施计划

## File Structure

```
zen-garden-ui/
├── app/
│   ├── page.tsx              # 主入口 (已有)
│   ├── layout.tsx            # 布局 (已有)
│   └── api/                  # API 路由 (新增)
│       └── identify/
│           └── route.ts
├── components/
│   ├── screens/              # 5个屏幕 (已有，需增强)
│   ├── ui/                   # shadcn/ui (已有)
│   └── lib/                  # 工具函数 (新增)
│       ├── supabase.ts       # Supabase 客户端
│       ├── gemini.ts         # Gemini API 封装
│       └── wasm-manager.ts   # WASM 抠图管理
├── lib/
│   └── supabase/             # Supabase 相关
│       ├── client.ts
│       ├── types.ts
│       └── queries.ts
└── supabase/
    └── schema.sql            # 数据库 Schema
```
