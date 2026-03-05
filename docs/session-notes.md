# 主脑交接记录

> 时间：2026-02-23
> 执行脑：主脑（Claude Sonnet 4.6 / Pro Plan）
> 状态：本次会话全部任务完成，无需副脑接手

---

## 本次完成的工作

- GitHub 热榜调研（2026年2月），识别并完成 5 个高价值集成项目
- 安装并验证 Claude-Mem v10.3.1（跨会话记忆，SessionStart hook 已确认触发）
- 配置 Chrome DevTools MCP（`npx chrome-devtools-mcp@latest`，写入 settings.json）
- 安装 continuous-learning-v2 skill（Windows 适配版，observe.js + homunculus 目录树）
- 集成 6 类代码质量 Hooks（Prettier/TypeScript/console.log/git push/PR URL/连续学习）
- 更新 `docs/integration-plan.md`（完整调研决策文档）
- 更新 `D:/Obsidian/.../ce+sp.md`（三层架构 + 主副脑分工标注 + 新工具章节）

## 关键决策及理由

| 决策 | 选择 | 理由 |
|------|------|------|
| observe.sh → observe.js | Node.js 版 | `python3` 未安装，Node.js 更可靠 |
| Chrome DevTools MCP 安装方式 | settings.json mcpServers | 无需全局 npm 安装，npx 按需拉取 |
| claude-mem 安装路径 | 手动 clone + 注册两个 JSON | `/plugin marketplace add` 在 Windows 上 EBUSY 锁文件问题 |
| bun.exe 路径 | 复制到 npm 全局目录 | bun-runner.js 的 `spawn('bun')` 需要无 shell 模式可找到的 .exe |
| installed_plugins.json 手动注册 | 必须同时更新 | Claude Code 靠该文件定位插件缓存路径，仅 enabledPlugins 不够 |
| "禁止创建 .md 文件" hook | 不引入 | 会阻断 session-notes.md / integration-plan.md 创建 |

## 修改的关键文件

- **`C:/Users/24140/.claude/settings.json`** — mcpServers（chrome-devtools）+ hooks（6类）+ enabledPlugins（claude-mem）
- **`C:/Users/24140/.claude/plugins/installed_plugins.json`** — 新增 claude-mem@thedotmack 条目
- **`C:/Users/24140/.claude/plugins/known_marketplaces.json`** — 新增 thedotmack 条目
- **`C:/Users/24140/.claude/plugins/cache/thedotmack/claude-mem/10.3.1/`** — 完整插件安装（依赖已安装）
- **`C:/Users/24140/.claude/skills/continuous-learning-v2/`** — SKILL.md + config.json + hooks/observe.js
- **`C:/Users/24140/.claude/homunculus/`** — 目录结构 + observations.jsonl（已在记录）
- **`C:/Users/24140/AppData/Roaming/npm/bun.exe`** — 解决 bun-runner.js spawn 路径问题
- **`D:/AI_Projects/system-max/docs/integration-plan.md`** — 调研决策文档
- **`D:/Obsidian/AI架构师相关知识/AI架构师相关知识/ce+sp.md`** — 工作流文档全面更新

## 副脑下一步任务

当前无待执行任务。若需继续工作，建议副脑：

1. **验证 Chrome DevTools MCP 实际功能**：重启后打开 Chrome，使用 `mcp__chrome-devtools__*` 工具执行一次真实截图或性能分析
2. **观察 continuous-learning-v2 本能积累**：经过几次会话后运行 `/instinct-status` 查看是否生成了有效本能
3. **验证 Claude-Mem 历史注入**：下次重启后确认看到已记录的会话摘要（而不是"No previous sessions found"）

## 注意事项 / 陷阱

- **Chrome DevTools MCP 首次启动需联网拉包**（npx），约数秒延迟
- **observe.js 是自定义 Windows 版**：原版 observe.sh 依赖 `python3`（本机不存在），本版等价替代
- **claude-mem 绕过了官方 /plugin 命令**：若后续官方命令可用，可用 `/plugin update claude-mem` 覆盖更新
- **bun.exe 复制了两份**：`~/.bun/bin/bun.exe` 和 `npm/bun.exe`，均为同一版本 v1.3.9
- **本项目无 git 仓库**：所有文件追踪只能靠文件系统

## 当前计划文件位置

`docs/integration-plan.md`（2026-02-22，完整调研结论与行动清单）

## 2026-02-26 Pencil MCP setup note (Codex)
- Source of truth: Pencil docs `AI Integration` says MCP runs automatically after Pencil desktop app starts.
- On Windows, avoid non-ASCII executable paths in Codex MCP config when startup errors show `os error 3`.
- Stable pattern used here:
  1. Copy `mcp-server-windows-x64.exe` to project ASCII path: `tools/pencil-mcp-server.exe`.
  2. Register MCP with project CODEX_HOME: `codex mcp add pencil -- "D:\AI_Projects\system-max\tools\pencil-mcp-server.exe" --app desktop`.
  3. Start Pencil desktop app before launching Codex, then run `/mcp` to verify connection.
- Helper scripts added:
  - `setup_pencil_mcp.ps1`
  - `start_codex_with_pencil.ps1`


## 2026-02-26 AI生图PRD v3 修订记录（Codex）
- 触发来源：`ai生图软件PRD相关前置文件/审查问题清单.md` 新一轮审核。
- 本次动作：重写完整 PRD 并同步覆盖：
  - `ai生图软件PRD.md`
  - `ai生图软件PRD相关前置文件/AI生图软件PRD（MVP）.md`
- 关键修订：
  1. 发布态安全改为 BYOK，本地安全存储，禁止内置共享生产 Key。
  2. 成本口径改为“仅硅基流动 API 调用成本；不引入其他付费云基础设施”。
  3. 新增版本治理（Minimum/Recommended/Rollback + 兼容矩阵）。
  4. 新增 contracts 契约校验、失败回放、成本日志与 CI 护栏。
  5. 新增分阶段 DoD（输入/输出/验收/回滚）与 ClaudeCode 执行规则。
- 风险残留：
  1. BYOK 可能影响首日转化，需要后续引导文案优化。
  2. 端侧性能在低端机仍有波动风险，需真机压测。
- 后续建议：
  1. 按 PRD 创建 `contracts/` 初版 schema。
  2. 先做 Phase 0 技术骨架与 CI 护栏，再进入功能实现。

- 追加修订（同日）：按用户要求将执行主体由 ClaudeCode 全量切换为 Codex，并同步更新交付指令章节标题与文案。

## 2026-02-27 Superpowers for Codex (Windows) setup note
- Goal: install `obra/superpowers` for Codex skill discovery and verify key functionality.
- Install actions executed:
  1. `git clone https://github.com/obra/superpowers.git C:\Users\24140\.codex\superpowers`
  2. `cmd /c mklink /J C:\Users\24140\.agents\skills\superpowers C:\Users\24140\.codex\superpowers\skills`
  3. `cmd /c mklink /J D:\AI_Projects\system-max\.codex-home\skills\superpowers C:\Users\24140\.codex\superpowers\skills`
- Verification evidence:
  - `fsutil reparsepoint query C:\Users\24140\.agents\skills\superpowers` shows target `C:\Users\24140\.codex\superpowers\skills`.
  - `dir C:\Users\24140\.agents\skills\superpowers` lists core skills (e.g. `brainstorming`, `using-superpowers`, `systematic-debugging`).
  - `codex exec --skip-git-repo-check` diagnostic outputs `brainstorming` and `using-superpowers` (skills visible to Codex).
- Operational note:
  - If using project launcher (`start_codex_with_mcp.bat`), keep `.codex-home\skills\superpowers` junction in place.
  - After updates: `git -C C:\Users\24140\.codex\superpowers pull`.


## 2026-02-27 PRD 结构化生成（AI生图 MVP）
- 输入来源：`ai生图软件PRD相关前置文件/AI生图软件（MVP）--idea.md`
- 方法：先收敛目标/边界，再按固定章节重排（产品概述、优先级、用户故事、NFR、验收、范围外）。
- 复用点：将长文档重组为可审查 PRD 时，优先保留约束与验收条款，避免新增未证实需求。

## 2026-02-27 Brainstorm 驱动 PRD 修订
- 先完成单题收敛：文档基调、优先级粒度、验收严格度、技术深度、用户故事分组。
- 产出策略：开发落地优先 + 评审字段，P0/P1/P2 用子功能级拆分，验收采用可量化 + 可执行命令。
- 可复用点：在 PRD 中把功能验收、工程验收、数据安全验收、可观测性验收分层，减少执行歧义。

## 2026-02-27 技术栈建议文档输出
- 输入：`docs/PRD.md`；输出：`docs/tech-stack.md`。
- 原则：优先单一推荐栈，减少可选分叉，同时保留健壮性必需件（契约校验、重试、落盘、日志、测试）。
- 复用点：在 MVP 阶段显式列出“不推荐项”，可以防止过度架构。

## 2026-02-27 数据库 Schema 与初始化迁移
- 输入：`docs/PRD.md` + `docs/tech-stack.md`。
- 输出：`docs/db-schema.md` + `db/migrations/0001_initial_schema.sql`。
- 复用点：以 SQLite 为中心，先固化约束（外键/检查/索引），再由应用层做回放上限清理策略。

## 2026-02-28 OpenSpec installation and Codex configuration
- Source: https://github.com/Fission-AI/OpenSpec
- Installation steps executed:
  1. Verified Node.js: `node -v` -> `v24.14.0` (meets >= 20.19.0)
  2. Installed CLI globally: `npm install -g @fission-ai/openspec@latest`
  3. Verified CLI: `openspec --version` -> `1.2.0`
  4. Checked global config: `openspec config list` (profile set to `core`, delivery `both`)
  5. Initialized project (Codex): `openspec init --tools codex --profile core` in `D:\AI_Projects\system-max\openspec-playground`
  6. Synced generated files: `openspec update`
- Verification evidence:
  - Skills generated at `.codex/skills/openspec-*` (propose, explore, apply-change, archive-change)
  - Codex prompt commands generated at `C:\Users\24140\.codex\prompts\opsx-*.md`
  - Project structure generated: `openspec/specs`, `openspec/changes/archive`
  - Validation command: `openspec validate --all --json` returned zero failures
- Gotcha:
  - On Windows, local folder `OpenSpec` conflicts with `openspec/` init directory due case-insensitive paths. Avoid cloning OpenSpec repo directly in target project root before running `openspec init`.


## 2026-02-28 OpenSpec formal init in real project directory
- Target project: `D:\AI_Projects\system-max`
- Cleanup before init:
  - Removed leftover `OpenSpec` folder (Windows case-insensitive conflict with `openspec/`)
- Commands executed:
  1. `openspec init --tools codex --profile core`
  2. `openspec update`
  3. `openspec validate --all --json`
- Verification evidence:
  - Created `openspec/changes/archive` and `openspec/specs`
  - Created skills under `.codex/skills/openspec-*` (4 skills)
  - Updated slash prompts under `C:\Users\24140\.codex\prompts\opsx-*.md` (4 commands)
  - Validation JSON summary shows `failed: 0`
- Note:
  - `openspec update` reported optional additional tool detection (`Claude Code`) but current init scope was intentionally `--tools codex` only.


## 2026-02-28 Chat image generation bugfix (`/chat` -> "Request failed, please retry.")
- Symptom:
  - Web chat page failed after successful `POST /v1/images/generations` (`200` with image URL payload).
- Root cause:
  - Legacy SQLite `messages.image_uri` constraint only accepted `file://...`.
  - Provider returned signed `https://...` URLs, causing insert failure and surfacing generic error.
- Fix:
  - Added legacy-safe fallback in `src/db/runtime-history.ts`:
    - if legacy `image_uri` check constraint rejects remote URL, retry insert with `imageUri: null` to avoid breaking generation flow.
  - Updated schema for new databases to accept `file://`, `http://`, `https://` in:
    - `src/db/runtime-db.ts`
    - `src/db/migrations/0001_initial_schema.sql`
  - Added/updated tests:
    - `tests/db/runtime-history.test.ts` (legacy constraint fallback case)
    - `tests/integration/db-migration-repositories.integration.test.ts` (remote URL insert case)
- Verification evidence:
  - Tests:
    - `npx vitest run tests/db/runtime-history.test.ts`
    - `npx vitest run tests/integration/db-migration-repositories.integration.test.ts`
    - `npx vitest run tests/unit/generate-first-image.unit.test.ts tests/flows/first-image.flow.test.ts tests/integration/first-image-chain.integration.test.ts`
    - `npx vitest run tests/unit/inpaint-image.unit.test.ts tests/flows/inpaint.flow.test.ts tests/integration/inpaint-chain.integration.test.ts`
  - Static/build checks:
    - `npm run lint`
    - `npm run typecheck`
    - `npm run build`
  - Manual check (Chrome DevTools MCP):
    - Reproduced before fix: `/chat` showed "Request failed, please retry." with generations `200`.
    - Verified after fix and server restart: `/chat` shows `Result Card` and image URL with generations `200`.


## 2026-02-28 Home page inline image preview (`/chat`)
- User request:
  - Show generated image directly on chat home page, not only URI text.
- TDD evidence:
  - Added failing smoke test first: `tests/smoke/chat-page-preview.smoke.test.ts`
  - RED: test failed because `chat-preview-image` was missing from `app/chat.tsx`.
  - GREEN: added inline `Image` preview with `testID="chat-preview-image"`, test passed.
- Code changes:
  - `app/chat.tsx`
    - import `Image` from `react-native`
    - render preview image in Result Card when `state.imageUri` exists
    - keep existing URI text for fallback/traceability
  - `tests/smoke/chat-page-preview.smoke.test.ts` (new)
- Verification evidence:
  - `npx vitest run tests/smoke/chat-page-preview.smoke.test.ts`
  - `npm run test` (all pass)
  - `npm run lint`
  - `npm run typecheck`
  - `npm run build`
  - Manual (Chrome DevTools MCP): `/chat` generated result now includes visible image preview in Result Card.


## 2026-02-28 Chat page visual alignment to `ai-image-ui-enterprise-calm.pen` (`Yhr64`)
- User request:
  - Align `/chat` UI with `ai-image-ui-enterprise-calm.pen` (A style), after functional bugfixes.
- Root cause of mismatch:
  - Existing `app/chat.tsx` was a simplified functional page, not the `Yhr64` enterprise layout from `.pen`.
- TDD evidence:
  - Updated smoke gate first (`tests/smoke/chat-page-preview.smoke.test.ts`) to require:
    - `A-ENTERPRISE`
    - `chat-bottom-pill`
    - `chat-preview-image`
  - RED confirmed before refactor, GREEN after refactor.
- Implementation:
  - Refactored `app/chat.tsx` to match `Yhr64` structure:
    - status bar (`9:41`, signal text)
    - enterprise header (`A-ENTERPRISE`, `AI Image Console`, `NEW` action)
    - KPI row (`P50`, `Cost`, `Retry`)
    - main enterprise card (`Prompt`, `BYOK Secure`, API key + prompt input rows, action buttons)
    - result preview card with image
    - bottom pill tab (`CHAT/EDITOR/RESULT`) with `chat-bottom-pill` testID
  - Kept existing behavior and critical testIDs (`api-key-input`, `save-api-key-btn`, `prompt-input`, `send-btn`).
- Verification evidence:
  - `npx vitest run tests/smoke/chat-page-preview.smoke.test.ts`
  - `npm run test` (30 files / 52 tests all passed)
  - `npm run lint`
  - `npm run typecheck`
  - `npm run build`
  - Manual (Chrome DevTools MCP):
    - Reloaded `/chat` after server restart.
    - Confirmed new enterprise layout markers on page.
    - Generated image successfully and confirmed preview visible in Result Card.

