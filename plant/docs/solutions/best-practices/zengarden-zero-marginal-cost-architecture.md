---
title: "ZenGarden AI 零边际成本架构设计"
category: "best-practices"
tags:
  - zero-marginal-cost
  - antifragile
  - quota-circuit-breaker
  - hybrid-recommendation
  - vector-search
  - pgvector
  - supabase
  - framer-motion
  - ar-interaction
  - gamification
  - ceremony-design
module:
  - "zen-garden-ui"
  - "supabase/functions/ai-processor"
  - "lib/recommendation-engine"
  - "components/ARComposer"
  - "components/CeremonyMoment"
problem_type: "architecture-design"
severity: "reference"
created: 2026-02-16
status: "active"
philosophy:
  - "Antifragile: 在资源受限中生存"
  - "Flow: 在交互中产生愉悦"
  - "Co-creation: 用户是生态的建设者"
related_files:
  - "plant/docs/solutions/security-issues/edge-function-jwt-cors-security.md"
  - "plant/docs/plans/2026-02-15-feat-zengarden-fullstack-implementation-plan-deepened.md"
  - "plant/ZenGarden AI-PRD.md"
---

# ZenGarden AI 零边际成本架构设计

## 问题背景

在构建一个基于免费层服务的园艺风水 AI 应用时，面临以下核心挑战：

| 挑战 | 描述 | 影响 |
|------|------|------|
| **API 配额限制** | Gemini Vision/Embedding 有调用频率限制 | 高峰期服务中断 |
| **Supabase Free Tier** | 500MB 数据库, 1GB 存储, 5GB 带宽/月 | 数据增长受限 |
| **项目自动暂停** | 7 天不活动自动暂停 | 服务可用性风险 |
| **用户体验一致性** | 配额耗尽时的降级体验 | 用户满意度下降 |

## 解决方案概述

采用**零边际成本架构**，通过以下五大支柱实现：

```
┌────────────────────────────────────────────────────────────────┐
│                    零边际成本架构 (Soul Stack)                   │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  配额熔断机制  │  │ 混合推荐引擎  │  │   智能幽灵交互 (AR)   │  │
│  │  Circuit      │  │ Hybrid       │  │   Smart Ghost        │  │
│  │  Breaker      │  │ Recommender  │  │   Interaction        │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────────────────────────────────┐ │
│  │  仪式时刻设计  │  │         生态共建系统 (荣誉体系)           │ │
│  │  Ceremony     │  │         Ecosystem Co-creation            │ │
│  │  Moment       │  │                                          │ │
│  └──────────────┘  └──────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

---

## 支柱一：配额熔断机制

### 设计理念

独立计量不同 API 服务的配额，当某个服务配额耗尽时，自动降级到替代方案，而非完全中断服务。

### 降级策略矩阵

| 服务 | 主策略 | 降级策略 | 触发条件 |
|------|--------|----------|----------|
| **Vision** | Gemini 1.5 Flash | 手动标签输入 | 日/月配额耗尽 |
| **Embedding** | text-embedding-004 | 纯标签匹配 | 日/月配额耗尽 |
| **数据库** | 完整查询 | 缓存结果 | 连接池耗尽 |

### 代码实现

#### 1. 配额管理器

```typescript
// lib/quota-manager.ts

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

// 配额配置
const QUOTA_CONFIG = {
  vision: {
    daily_limit: 100,
    monthly_limit: 2000,
  },
  embedding: {
    daily_limit: 500,
    monthly_limit: 10000,
  }
};

export type ServiceType = 'vision' | 'embedding';
export type QuotaStatus = 'available' | 'daily_exhausted' | 'monthly_exhausted';

interface QuotaCheckResult {
  available: boolean;
  status: QuotaStatus;
  remaining: { daily: number; monthly: number };
  fallbackMode: 'manual' | 'tag_only';
}

export class QuotaManager {
  /**
   * 检查服务配额状态
   */
  static async checkQuota(service: ServiceType): Promise<QuotaCheckResult> {
    const now = new Date();
    const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);

    // 并行查询日/月使用量
    const [dailyResult, monthlyResult] = await Promise.all([
      supabase
        .from('api_usage_log')
        .select('id', { count: 'exact', head: true })
        .eq('service', service)
        .gte('created_at', startOfDay.toISOString()),
      supabase
        .from('api_usage_log')
        .select('id', { count: 'exact', head: true })
        .eq('service', service)
        .gte('created_at', startOfMonth.toISOString()),
    ]);

    const dailyUsed = dailyResult.count || 0;
    const monthlyUsed = monthlyResult.count || 0;
    const config = QUOTA_CONFIG[service];

    const dailyRemaining = Math.max(0, config.daily_limit - dailyUsed);
    const monthlyRemaining = Math.max(0, config.monthly_limit - monthlyUsed);

    // 确定状态
    let status: QuotaStatus = 'available';
    if (monthlyRemaining === 0) {
      status = 'monthly_exhausted';
    } else if (dailyRemaining === 0) {
      status = 'daily_exhausted';
    }

    return {
      available: status === 'available',
      status,
      remaining: { daily: dailyRemaining, monthly: monthlyRemaining },
      fallbackMode: service === 'vision' ? 'manual' : 'tag_only',
    } as QuotaCheckResult;
  }

  /**
   * 记录 API 使用
   */
  static async recordUsage(
    service: ServiceType,
    userId: string,
    endpoint: string,
    tokensUsed: number = 1
  ): Promise<void> {
    await supabase.from('api_usage_log').insert({
      user_id: userId,
      service,
      endpoint,
      tokens_used: tokensUsed,
    });
  }
}
```

#### 2. Edge Function 实现

```typescript
// supabase/functions/plant-identify/index.ts

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const GEMINI_API_KEY = Deno.env.get('GEMINI_API_KEY')!;
const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
const SUPABASE_SERVICE_KEY = Deno.env.get('SUPABASE_SERVICE_KEY')!;

serve(async (req) => {
  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

  const { imageBase64, userId } = await req.json();

  // Step 1: 配额检查
  const quotaStatus = await checkVisionQuota(supabase);

  if (!quotaStatus.available) {
    // 配额耗尽 - 降级模式
    return new Response(
      JSON.stringify({
        mode: 'fallback',
        reason: quotaStatus.reason,
        message: 'AI 识别配额已用尽，请手动输入植物特征',
        suggestions: await getTagSuggestions(supabase),
      }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  }

  try {
    // 主策略 - Gemini Vision
    const result = await callGeminiVision(imageBase64);

    // 记录使用
    await supabase.from('api_usage_log').insert({
      user_id: userId,
      service: 'vision',
      endpoint: 'identify',
      tokens_used: 1,
    });

    return new Response(
      JSON.stringify({
        mode: 'ai',
        confidence: result.confidence,
        candidates: result.candidates,
        quotaRemaining: quotaStatus.remaining,
      }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    // API 调用失败也触发降级
    return new Response(
      JSON.stringify({
        mode: 'fallback',
        reason: 'api_error',
        message: 'AI 服务暂时不可用，请稍后重试或手动输入',
      }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  }
});
```

---

## 支柱二：混合推荐引擎

### 设计理念

优先使用向量语义搜索获得高质量推荐，当向量搜索不可用时，自动降级到标签匹配。

### 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     混合推荐引擎架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   查询输入                                                      │
│      │                                                          │
│      ▼                                                          │
│   ┌─────────────────┐                                          │
│   │  配额检查        │                                          │
│   │  checkQuota()   │                                          │
│   └────────┬────────┘                                          │
│            │                                                    │
│   ┌────────┴────────┐                                          │
│   │                 │                                          │
│   ▼                 ▼                                          │
│ ┌───────────┐   ┌───────────┐                                  │
│ │ 向量搜索   │   │ 标签匹配   │                                  │
│ │ (主策略)   │   │ (降级策略) │                                  │
│ │ pgvector  │   │ JSONB     │                                  │
│ └─────┬─────┘   └─────┬─────┘                                  │
│       │               │                                        │
│       └───────┬───────┘                                        │
│               ▼                                                │
│        ┌─────────────┐                                         │
│        │ 结果合并/排序 │                                         │
│        └─────────────┘                                         │
│               │                                                │
│               ▼                                                │
│        Top 3 推荐                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 代码实现

```typescript
// lib/recommendation-engine.ts

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

export interface PlantRecommendation {
  id: string;
  scientific_name: string;
  common_name: string;
  tags: string[];
  similarity_score: number;
  match_type: 'vector' | 'tag';
}

export class RecommendationEngine {
  /**
   * 主策略：向量相似度搜索
   */
  private static async vectorSearch(
    queryText: string,
    queryTags: string[],
    userId: string,
    limit: number
  ): Promise<PlantRecommendation[]> {
    const quota = await QuotaManager.checkQuota('embedding');

    if (!quota.available) {
      return this.tagBasedSearch(queryTags, limit);
    }

    try {
      // 1. 获取查询文本的 embedding
      const embedding = await this.getEmbedding(queryText);
      await QuotaManager.recordUsage('embedding', userId, 'search');

      // 2. pgvector 余弦相似度搜索
      const { data, error } = await supabase.rpc('vector_search_plants', {
        query_embedding: embedding,
        match_threshold: 0.7,
        match_count: limit,
      });

      if (error) throw error;

      return (data || []).map((item: any) => ({
        ...item,
        similarity_score: item.similarity,
        match_type: 'vector' as const,
      }));
    } catch (error) {
      console.error('Vector search failed, falling back to tag search:', error);
      return this.tagBasedSearch(queryTags, limit);
    }
  }

  /**
   * 降级策略：纯标签匹配
   */
  private static async tagBasedSearch(
    tags: string[],
    limit: number
  ): Promise<PlantRecommendation[]> {
    if (!tags || tags.length === 0) {
      return [];
    }

    // PostgreSQL JSONB 数组重叠查询
    const { data, error } = await supabase
      .from('plant_library')
      .select('*')
      .overlaps('tags', tags)
      .order('vote_count', { ascending: false })
      .limit(limit);

    if (error) {
      console.error('Tag search error:', error);
      return [];
    }

    // 计算标签重叠分数
    return (data || []).map((item) => {
      const itemTags = item.tags || [];
      const overlapCount = tags.filter((t) => itemTags.includes(t)).length;
      const similarity = overlapCount / Math.max(tags.length, itemTags.length);

      return {
        id: item.id,
        scientific_name: item.scientific_name,
        common_name: item.common_name,
        tags: itemTags,
        similarity_score: similarity,
        match_type: 'tag' as const,
      };
    });
  }

  /**
   * 统一推荐入口 - 自动选择策略
   */
  static async recommend(
    query: {
      text?: string;
      tags?: string[];
      userId: string;
    },
    options: { limit?: number } = {}
  ): Promise<PlantRecommendation[]> {
    const limit = options.limit || 3;

    // 优先使用向量搜索
    if (query.text) {
      return this.vectorSearch(
        query.text,
        query.tags || [],
        query.userId,
        limit
      );
    }

    // 纯标签搜索
    if (query.tags?.length) {
      return this.tagBasedSearch(query.tags, limit);
    }

    return [];
  }
}
```

### PostgreSQL 向量搜索函数

```sql
-- 向量搜索函数
CREATE OR REPLACE FUNCTION vector_search_plants(
  query_embedding vector(768),
  match_threshold float DEFAULT 0.7,
  match_count int DEFAULT 3
)
RETURNS TABLE (
  id uuid,
  scientific_name text,
  common_name text,
  tags jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    pl.id,
    pl.scientific_name,
    pl.common_name,
    pl.tags,
    1 - (pl.description_embedding <=> query_embedding) as similarity
  FROM plant_library pl
  WHERE 1 - (pl.description_embedding <=> query_embedding) > match_threshold
  ORDER BY pl.description_embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

---

## 支柱三：智能幽灵交互 (AR)

### 设计理念

在 AR 编辑模式中，通过"智能幽灵"引导用户将植物放置到最佳风水位置，提供磁吸式交互反馈。

### 交互层级

| 幽灵类型 | 透明度 | 效果 | 触发条件 |
|----------|--------|------|----------|
| **主幽灵** | 0.6 | 脉冲呼吸动画 | AI 推荐最佳位 |
| **次幽灵** | 0.2 | 靠近时变亮 | 备选位置 |
| **磁吸效果** | - | 吸附感动画 | 拖拽接近时 |

### 代码实现

```typescript
// components/GhostInteraction.tsx

import React, { useRef, useState, useEffect } from 'react';
import { motion, useAnimation, PanInfo } from 'framer-motion';

interface GhostConfig {
  id: string;
  opacity: number;
  scale: number;
  isPrimary: boolean;
  position: { x: number; y: number };
  label?: string;  // "财位" 等
}

export const GhostInteraction: React.FC = () => {
  const [ghosts, setGhosts] = useState<GhostConfig[]>([]);
  const [draggedGhost, setDraggedGhost] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const controls = useAnimation();

  // 脉冲呼吸效果 (主幽灵)
  useEffect(() => {
    const primaryGhost = ghosts.find((g) => g.isPrimary);
    if (primaryGhost) {
      controls.start({
        scale: [1, 1.05, 1],
        opacity: [0.6, 0.8, 0.6],
        transition: {
          duration: 3,
          repeat: Infinity,
          ease: 'easeInOut',
        },
      });
    }
  }, [ghosts, controls]);

  // 磁吸吸附逻辑
  const handleDragEnd = (
    ghostId: string,
    info: PanInfo,
    targetPosition: { x: number; y: number }
  ) => {
    const MAGNET_THRESHOLD = 50; // 吸附阈值像素
    const distance = Math.sqrt(
      Math.pow(info.point.x - targetPosition.x, 2) +
        Math.pow(info.point.y - targetPosition.y, 2)
    );

    if (distance < MAGNET_THRESHOLD) {
      // 触发吸附动画
      controls.start({
        x: targetPosition.x,
        y: targetPosition.y,
        transition: { type: 'spring', stiffness: 300, damping: 20 },
      });

      // 触发合并/完成事件
      onGhostMerge?.(ghostId);
    }
  };

  // 靠近时变亮效果 (次幽灵)
  const handleProximity = (ghostId: string, distance: number) => {
    const PROXIMITY_THRESHOLD = 100;

    setGhosts((prev) =>
      prev.map((ghost) => {
        if (ghost.id === ghostId && !ghost.isPrimary) {
          const newOpacity = distance < PROXIMITY_THRESHOLD
            ? Math.min(0.6, 0.2 + (1 - distance / PROXIMITY_THRESHOLD) * 0.4)
            : 0.2;
          return { ...ghost, opacity: newOpacity };
        }
        return ghost;
      })
    );
  };

  return (
    <div ref={containerRef} className="relative w-full h-full overflow-hidden">
      {ghosts.map((ghost) => (
        <motion.div
          key={ghost.id}
          className="absolute cursor-grab"
          initial={{ opacity: ghost.opacity, scale: ghost.scale }}
          animate={ghost.isPrimary ? controls : undefined}
          drag
          dragMomentum={false}
          onDragStart={() => setDraggedGhost(ghost.id)}
          onDragEnd={(_, info) => handleDragEnd(ghost.id, info, { x: 0, y: 0 })}
          whileDrag={{ scale: 1.1, cursor: 'grabbing' }}
          style={{
            left: ghost.position.x,
            top: ghost.position.y,
            filter: `drop-shadow(0 0 20px rgba(255, 255, 255, ${ghost.opacity}))`,
          }}
        >
          <GhostSVG opacity={ghost.opacity} />
          {ghost.label && (
            <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-xs text-white/80">
              {ghost.label}
            </span>
          )}
        </motion.div>
      ))}
    </div>
  );
};
```

---

## 支柱四：仪式时刻设计

### 设计理念

当用户完成植物放置时，触发"仪式时刻"——通过动画和诗意文案，将功能性操作升华为情感化体验。

### 组成要素

| 要素 | 实现方式 | 效果 |
|------|----------|------|
| **粒子光晕** | Framer Motion 动画 | 植物从中心向四周扩散光晕 |
| **诗意文案** | 本地模板随机选择 | 情感连接 |
| **音效 (可选)** | Web Audio API | 沉浸感增强 |

### 代码实现

```typescript
// components/RitualCeremony.tsx

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface RitualCeremonyProps {
  trigger: boolean;
  plantName: string;
  onComplete: () => void;
}

// 诗意风水语本地模板
const RITUAL_MESSAGES = {
  zh: [
    '🌱 青叶入室，生机以此为始',
    '🍃 风带来了生命的低语',
    '✨ 天地之间，万物共生',
    '🌸 春华秋实，生生不息',
    '💧 上善若水，润泽万物',
  ],
};

export const RitualCeremony: React.FC<RitualCeremonyProps> = ({
  trigger,
  plantName,
  onComplete,
}) => {
  const [stage, setStage] = useState<'idle' | 'particles' | 'glow' | 'message' | 'complete'>('idle');
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (trigger) {
      // 仪式阶段序列
      setStage('particles');

      setTimeout(() => setStage('glow'), 1000);
      setTimeout(() => {
        setStage('message');
        const messages = RITUAL_MESSAGES.zh;
        setMessage(messages[Math.floor(Math.random() * messages.length)]);
      }, 2000);
      setTimeout(() => {
        setStage('complete');
        onComplete();
      }, 4500);
    }
  }, [trigger, onComplete]);

  // 粒子效果生成
  const particles = Array.from({ length: 30 }, (_, i) => ({
    id: i,
    angle: (360 / 30) * i,
    delay: Math.random() * 0.5,
  }));

  return (
    <AnimatePresence>
      {trigger && stage !== 'complete' && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {/* 半透明遮罩 */}
          <motion.div
            className="absolute inset-0 bg-black/30"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          />

          {/* 粒子光晕扩散 */}
          {stage !== 'idle' && (
            <div className="relative">
              {particles.map((particle) => (
                <motion.div
                  key={particle.id}
                  className="absolute w-2 h-2 rounded-full bg-gradient-to-r from-green-300 to-emerald-500"
                  initial={{ x: 0, y: 0, scale: 0, opacity: 0 }}
                  animate={
                    stage === 'particles' || stage === 'glow'
                      ? {
                          x: Math.cos((particle.angle * Math.PI) / 180) * 150,
                          y: Math.sin((particle.angle * Math.PI) / 180) * 150,
                          scale: [0, 1.5, 0.5],
                          opacity: [0, 1, 0.5],
                        }
                      : {}
                  }
                  transition={{
                    duration: 2,
                    delay: particle.delay,
                    ease: 'easeOut',
                  }}
                />
              ))}

              {/* 中心光晕 */}
              <motion.div
                className="absolute w-40 h-40 -translate-x-1/2 -translate-y-1/2 rounded-full"
                style={{
                  background: 'radial-gradient(circle, rgba(16, 185, 129, 0.6) 0%, transparent 70%)',
                }}
                initial={{ scale: 0, opacity: 0 }}
                animate={stage === 'glow' ? { scale: [0, 2, 1.5], opacity: [0, 1, 0.8] } : {}}
                transition={{ duration: 1.5 }}
              />

              {/* 植物图标 */}
              <motion.div
                className="text-6xl"
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 200, delay: 0.5 }}
              >
                🌿
              </motion.div>
            </div>
          )}

          {/* 诗意文案 */}
          <AnimatePresence>
            {stage === 'message' && (
              <motion.div
                className="absolute bottom-1/3 text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <p className="text-2xl text-white font-light tracking-wider mb-2">
                  {message}
                </p>
                <p className="text-lg text-emerald-200">
                  「{plantName}」已加入你的禅园
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
```

---

## 支柱五：生态共建系统

### 设计理念

通过荣誉体系激励用户贡献，让用户成为生态的建设者，实现内容自增长。

### 成就层级

| 等级 | 名称 | 阈值 | 稀有度 | 特权 |
|------|------|------|--------|------|
| 1 | 初播种者 | 1 贡献 | common | 基础配额 |
| 2 | 园丁 | 5 贡献 | common | - |
| 3 | 植物学家 | 10 贡献 | rare | 扩展配额 |
| 4 | 园艺师 | 25 贡献 | rare | 冷却缩减 |
| 5 | 园艺宗师 | 50 贡献 | epic | 优先审核 + 专属幽灵 |
| 6 | 传奇发现者 | 100 贡献 | legendary | 跳过审核 + 定制徽章 |

### 数据模型

```sql
-- 用户档案 (含信用与成就)
create table profiles (
  id uuid references auth.users primary key,
  display_name text,
  avatar_url text,
  credit_score int default 10,
  badges jsonb default '[]'::jsonb,
  contributions_count int default 0,
  verified_count int default 0,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- 公共植物库 (含荣誉体系 - 宗师留名)
create table plant_library (
  id uuid default gen_random_uuid() primary key,
  scientific_name text unique not null,
  common_name text,
  tags jsonb default '[]'::jsonb,
  description text,
  description_embedding vector(768),
  discovered_by uuid references auth.users,  -- 宗师留名！
  discovery_date timestamp with time zone default now(),
  verified boolean default false,
  vote_count int default 0
);
```

---

## 预防检查清单

### 日常检查

```yaml
daily_checks:
  - name: "Supabase 配额监控"
    items:
      - [ ] 检查数据库使用量 (警告阈值: 400MB / 500MB)
      - [ ] 检查存储使用量 (警告阈值: 800MB / 1GB)
      - [ ] 检查本月带宽消耗 (警告阈值: 4GB / 5GB)
      - [ ] 验证项目活跃状态 (防止7天暂停)

  - name: "API 服务健康检查"
    items:
      - [ ] Gemini Vision API 调用次数与配额
      - [ ] Embedding API 调用次数与配额
      - [ ] Edge Functions 执行次数
```

### 部署前检查

```yaml
pre_deployment:
  resilience:
    - [ ] 所有外部调用有超时设置
    - [ ] 降级路径已测试
    - [ ] 错误消息对用户友好
    - [ ] 配额边界条件已覆盖

  security:
    - [ ] RLS 策略已配置
    - [ ] API 密钥无硬编码
    - [ ] 用户输入已验证/清洗
```

---

## 参考资料

- [Supabase 官方成本控制文档](https://supabase.com/docs/guides/platform/cost-control)
- [pgvector 向量搜索文档](https://github.com/pgvector/pgvector)
- [Framer Motion 动画库](https://www.framer.com/motion/)
- [混合搜索最佳实践 - Elastic](https://www.elastic.co/what-is/hybrid-search)
- [混合搜索详解 - Weaviate](https://weaviate.io/blog/hybrid-search-explained)

---

## 相关文档

- [Edge Function JWT 与 CORS 安全](../security-issues/edge-function-jwt-cors-security.md)
- [ZenGarden 全栈实现计划](../../plans/2026-02-15-feat-zengarden-fullstack-implementation-plan-deepened.md)
- [ZenGarden AI PRD](../../ZenGarden AI-PRD.md)

---

**沉淀日期**: 2026-02-16
**知识类型**: 架构设计最佳实践
**适用项目**: ZenGarden AI / 类似零成本架构应用
