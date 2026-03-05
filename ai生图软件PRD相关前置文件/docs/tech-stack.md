# AI 生图应用技术栈建议（MVP）

- 基于文档：`docs/PRD.md`
- 目标：最简单但足够健壮（优先可交付、可维护、可验收）

## 1. 推荐结论（单一方案）

采用 `Expo + React Native + TypeScript` 的纯前端本地化架构，直连 SiliconFlow API，不引入业务后端。

### 1.1 应用框架
1. `expo@52.x`
2. `react-native@0.77.x`
3. `typescript@5.x`
4. `expo-router@3.x`（轻量路由，满足多页面与深链接基础能力）

### 1.2 状态与数据层
1. `zustand`：仅保存轻状态（UI 状态、会话上下文索引、任务状态）
2. `expo-sqlite`：持久化会话、消息、请求日志、失败回放
3. `expo-file-system`：图片文件落盘（只存 `file://` 路径）
4. `react-native-mmkv`：配置项与非敏感偏好（不存密钥）

### 1.3 网络与容错
1. `axios`
2. `axios-retry`（或自定义 interceptor）
3. `zod`（响应契约校验，未通过不入库不渲染）

### 1.4 图像编辑与交互
1. `@shopify/react-native-skia`（画布与遮罩渲染）
2. `react-native-reanimated@4.x`
3. `react-native-gesture-handler@2.x`

### 1.5 安全与合规
1. `expo-secure-store`（BYOK 密钥存储）
2. `expo-media-library`（保存到相册）
3. `expo-image-manipulator`（导出前压缩/处理）
4. EXIF/AIGC 标记：使用可用的轻量 EXIF 写入库（按平台可行性选型）

### 1.6 工程质量
1. `eslint` + `@typescript-eslint/*`
2. `prettier`
3. `vitest`（单测）
4. `@testing-library/react-native`（组件/集成测试）
5. `detox`（关键路径 E2E，首图生成/局部重绘/导出）

## 2. 为什么这是“最简单但足够健壮”

1. 不引入业务后端，完全符合 PRD 成本红线。
2. 只保留一套本地数据路径：`API -> Base64短驻留 -> 文件落盘 -> SQLite元数据`，可控且易排障。
3. 用 `zod + retry + 日志` 构建最小可靠性闭环，覆盖契约异常、超时、429/503。
4. 图像编辑选 `Skia + Reanimated + Gesture`，是 RN 生态中成熟且性能可达标的最小组合。
5. 测试栈覆盖 `单测 + 集成 + E2E`，直接对齐 PRD 的验收命令与证据要求。

## 3. 明确不推荐（MVP 阶段）

1. 不引入云数据库/对象存储/FaaS：增加运维和成本，不符合边界。
2. 不引入 Redux Toolkit + Saga：对当前规模过重，学习和维护成本高。
3. 不引入复杂微服务或 BFF：当前无必要，且与“零业务后端”冲突。

## 4. 版本基线（建议锁定）

1. Expo SDK：`52.x`
2. React Native：`0.77.x`
3. Reanimated：`4.x`
4. Gesture Handler：`2.x`
5. Skia：`1.x`

## 5. 最小落地清单（可直接建项目）

1. 创建 Expo TS 工程并锁定版本基线。
2. 接入 `zustand + sqlite + file-system + mmkv`。
3. 完成网络层：`axios + retry + zod`。
4. 完成编辑器基础：`skia + reanimated + gesture`。
5. 接入 `secure-store` 实现 BYOK 与日志脱敏。
6. 配置 `test/typecheck/lint/build` 与最小 E2E 流程。
