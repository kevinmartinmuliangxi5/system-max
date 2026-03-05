# Codex 工作流构建 PRD（单脑版，Codex-Ready v5.7）

## 1. 文档信息
- 文档名称：Codex 工作流构建 PRD（单脑）
- 文件路径：`codex工作流构建前置文件/codex工作流构建prd.md`
- 版本：v5.7
- 日期：2026-02-26
- 适用范围：`D:\AI_Projects\system-max`
- 定位：审查版 + 可直接执行版（Vibe Coding）

---

## 2. 执行摘要
v5.7 在 v5.6 基础上继续做“算法口径去模糊化”，目标是降低 Codex 实现分叉风险。

本版关键更新：
1. slow 统计口径写死：按 command signature、最近 2 次窗口、默认不跨 day。
2. 删除“网络抖动自动冷却重试”规则，避免语义判定歧义。
3. 新证据判定收敛：以 logs/raw 与代码 diff 为主，不再依赖 day-notes 行变化。
4. SDD 去除行数硬约束，仅保留结构性必填字段。
5. 增加初始化幂等要求与 Implementation Strict Mode 约束。

---

## 3. 需求收敛

### 3.1 目标（Must）
1. 建立单脑闭环：需求收敛 -> 计划拆解 -> 实施 -> 验证 -> 交付沉淀。
2. 支持高频 Vibe Coding，保持低阻力与高可追溯。
3. 异常场景（循环、超时、缺依赖、分支漂移）可熔断、可恢复、可交接。
4. PRD 可直接用于审查与后续 Codex 连续执行。

### 3.2 非目标
1. 本期不做多代理平台化编排。
2. 本期不做全自动指标大盘。
3. 本期不设全仓覆盖率硬门禁。

### 3.3 约束
1. AGENTS.md 为一级入口。
2. 关键命令仅以 `workflow.json` 的 `commands.sync_fast` 与 `commands.async_ci` 为准。
3. 熔断必须在外部脚本层执行。
4. 跨会话状态必须文件化落盘。

### 3.4 当期验收指标
1. 完成 2 次端到端闭环回放。
2. 完成 3 类异常演练并可恢复：循环、超时、缺依赖。
3. 审查可追溯：关键决策、命令证据、验证证据均可定位。

### 3.5 长期 KPI（观察项）
1. 连续 14 天稳定运行。
2. LOOP_DETECTED 触发率下降。
3. sync_fast 平均耗时下降。

---

## 4. 审查问题逐条处理矩阵（v5.7）

| 审查问题 | 结论 | 处理方式 |
|---|---|---|
| 自动生成 wrapper 风险偏高 | 采纳 | 默认关闭，需显式开启 + 冒烟验证 |
| “短窗口重复失败”缺可计算定义 | 采纳 | 增加 `window_seconds` 配置（默认 600） |
| 熔断条件“无改进且继续失败”不可计算 | 采纳 | 从熔断条件中删除 |
| 命令签名去噪口径过开放 | 采纳 | 改为白名单化 normalize 固定规则 |
| 新证据 diff 统计口径不明确 | 采纳 | 明确 `git diff --name-only/--numstat` 口径 |
| bypass 连续“两天”统计口径不稳 | 采纳 | 改为连续两个 dayNN |
| slow 统计粒度与窗口不明确 | 采纳 | 写死按 signature、最近2次、不跨day |
| 网络抖动自动重试不可自动判定 | 采纳 | 删除该规则 |
| SDD 行数约束对执行有歧义 | 采纳 | 删除行数限制，仅保留结构必填 |
| 建议 AGENTS 增加一句话总指令 | 采纳 | 纳入模板顶部 |
| 建议完全删除结构化证据 | 不采纳 | 保留最小必要证据支持审查回放 |

---

## 5. 唯一执行路径

### 5.1 会话读取顺序（强制）
在 AGENTS.md 被加载后，新会话按以下顺序读取：
1. `docs/handover.md`
2. `docs/active-backlog.md`
3. `config/workflow.json`
4. `codex-tasks/today.md`
5. `codex-tasks/dayNN.md`

### 5.2 命令执行策略（强制）
1. 关键命令定义：`workflow.json` 中 `commands.sync_fast` 与 `commands.async_ci`。
2. 关键命令必须通过 `scripts/log_cmd.ps1` 或 `scripts/log_cmd.sh` 执行。
3. wrapper 不可用时允许 `WRAPPER_BYPASS`，但必须在 day-notes 记录：原因、风险、旁路命令、回归计划。
4. 未记录 `WRAPPER_BYPASS` 而直跑关键命令，视为 DoD 失败。
5. 连续两个 dayNN 发生 `WRAPPER_BYPASS`，必须写入 `docs/active-backlog.md` 且标记高优先级修复。

### 5.3 wrapper 自检协议（强制）
1. 会话开始先检测 `scripts/log_cmd.ps1` 或 `scripts/log_cmd.sh` 是否存在且可执行。
2. 若不存在：
- `runtime.auto_bootstrap_wrapper=false`（默认）：返回 `20 BLOCKED` 并写恢复动作；
- `runtime.auto_bootstrap_wrapper=true`：按固定模板生成最小 wrapper，记录 `AUTO_BOOTSTRAP_WRAPPER` 并立即执行冒烟测试。
3. 冒烟测试失败必须回退为 `20 BLOCKED`。
4. wrapper 最小参数能力：`--cmd`、`--cwd`、`--timeout`、`--tag`。

---

## 6. 标准执行流（单脑）
1. 需求收敛：明确目标、非目标、约束、风险、验收。
2. 计划拆解：拆成 3-7 步，每步定义验证方式。
3. SDD 蓝图：先蓝图后编码。
4. 最小实现：只做当前目标最小改动。
5. 重构清理：在验证通过前提下提升可读性。
6. 完成前验证：测试 + Lint/Typecheck + Build + 关键路径功能验证。
7. 交付沉淀：更新 day-notes 与 handover，记录剩余风险。

TDD 不作为流程强制步骤，仅按第 13 章条件触发。

---

## 7. 单一状态源与退出码

### 7.1 状态机
`INIT -> PLAN_READY -> IMPLEMENTING -> VERIFYING -> DAY_DONE`
异常分支：
`IMPLEMENTING/VERIFYING -> CHECKPOINT(10) -> RESUME`
`IMPLEMENTING/VERIFYING -> BLOCKED(20)`
`IMPLEMENTING/VERIFYING -> LOOP_DETECTED(21)`

### 7.2 状态归属（强制）
1. 仅 wrapper 可写 `.codex_runtime.json`。
2. Codex 只读状态文件，不直接写状态。
3. 每次关键命令后必须刷新状态与时间戳。
4. 初始化行为必须幂等：重复初始化不得覆盖已有有效状态。

### 7.3 初始化与恢复（强制）
1. 状态文件不存在：wrapper 自动初始化为 `INIT`。
2. 状态文件 JSON 损坏：wrapper 返回 `20 BLOCKED`，生成恢复建议并写入 day-notes。
3. 分支/day 不一致：wrapper 返回 `20 BLOCKED`，并给出三选一恢复动作：
- 切回原分支；
- 更新 `today.md` 与 day 卡；
- 重置到 `INIT` 并开新 day 卡。

### 7.4 退出码
1. `0`：成功。
2. `10`：CHECKPOINT。
3. `20`：BLOCKED。
4. `21`：LOOP_DETECTED。
5. `30+`：脚本或环境异常。

### 7.5 `.codex_runtime.json` 最小结构
```json
{
  "schema_version": 1,
  "day": "day03",
  "state": "IMPLEMENTING",
  "last_exit_code": 0,
  "updated_at": "2026-02-26T10:30:00Z",
  "last_command": {
    "signature": "sig_ab12cd",
    "digest": "err_9f31b2"
  },
  "fuse": {
    "retry_count": 1,
    "max_attempts": 3,
    "window_seconds": 600,
    "slow_count": 0,
    "slow_avg_ratio": 1.0
  }
}
```

---

## 8. 外部熔断器规范（强制）

### 8.1 原则
1. 熔断在 wrapper 层执行。
2. LLM 不负责重试计数。
3. 熔断必须可审计、可重置。

### 8.2 触发条件
1. 同签名 + 同 digest 连续失败 `>= max_attempts`（默认 3）。
2. 在 `window_seconds`（默认 600）内，参数完全重复且失败次数 `>=3`。

### 8.3 误熔断抑制
1. 同签名但 digest 不同，不累计连续失败计数。

### 8.4 熔断动作
1. 停止自动执行并退出 `21`。
2. 在 day-notes 写 `LOOP_DETECTED` 区块。
3. 输出最近三次失败摘要与人工问题列表。

### 8.5 命令签名规范（强制）
1. 签名输入：`command + normalized_args`。
2. normalize 仅允许：`trim`、连续空白压缩为单空格、路径分隔符统一 `/`、引号统一为 `"`。
3. 仅对白名单参数值做占位替换：`--log-file`、`--output`、`--tmp-dir` -> `<PATH>`。
4. 其他参数值不得自动改写。
5. 签名算法：`sha256(normalized_command_string)`。

### 8.6 新证据判定（强制）
以下任一成立即视为“有新证据”：
1. `logs/raw/` 新增日志文件。
2. 代码变更满足“非平凡 diff”判定：
- 统计命令固定为 `git diff --name-only HEAD` 与 `git diff --numstat HEAD`；
- 仅统计白名单路径（默认 `src/`,`app/`,`lib/`,`config/`）；
- 排除锁文件（`package-lock.json`,`yarn.lock`,`pnpm-lock.yaml`,`poetry.lock`,`Cargo.lock`,`go.sum`）；
- 有效新增/修改行数（numstat）合计 >= 10。

---

## 9. Error-Digest 规范（强制）

### 9.1 流程
1. 原始日志写入 `logs/raw/*.log`。
2. 提取 `Error|Exception|Traceback|Failed` 及上下文 5 行。
3. 生成 digest 并记录到 day-notes。

### 9.2 摘要模板
```md
## ERROR_DIGEST
- digest: err_9f31b2
- top_error: TypeError: cannot read property 'x' of undefined
- source_log: logs/raw/build-20260226-153000.log
- next_action: 检查 src/foo.ts:42 的空值保护
```

### 9.3 top_error 选择规则（强制）
1. 优先第一条匹配 `Error|Exception|Traceback` 的行。
2. 若无上述匹配，选择第一条 `Failed` 行。
3. 若仍无匹配，标记 `top_error: UNKNOWN`。

---

## 10. 证据与记忆模型（最小必要）

### 10.1 必须文件
1. `docs/conventions.md`
2. `docs/session-notes.md`（append-only）
3. `docs/active-backlog.md`
4. `docs/handover.md`
5. `evidence/dayNN/day-notes.md`

### 10.2 可选文件（真实事件驱动）
1. `logs/raw/*.log`
2. `evidence/dayNN/tests.log`
3. `evidence/dayNN/build.log`
4. `evidence/dayNN/acceptance.log`

### 10.3 强制规则
1. 不得创建空日志文件。
2. 不得把超长堆栈直接作为主输入喂给模型。
3. 非必须文件只有发生对应事件时才创建。

---

## 11. 交接机制（强制）

### 11.1 何时更新 handover
以下状态都必须更新 `docs/handover.md`：
1. `DAY_DONE`
2. `BLOCKED`
3. `LOOP_DETECTED`

### 11.2 异常日标记
若状态为 `BLOCKED` 或 `LOOP_DETECTED`，handover 必须包含：
1. `status: INTERRUPTED`
2. 阻塞根因
3. 已尝试动作
4. 需要人工输入的最小问题列表

### 11.3 新会话启动
1. 读 `AGENTS.md`。
2. 读 `handover.md`。
3. 读 `active-backlog.md`。
4. 读 `today.md -> dayNN.md`。

---

## 12. 质量闸门（Fast/Async）

### 12.1 sync_fast
1. 预算字段：`execution.sync_fast_budget_seconds`（默认 60）。
2. slow 统计粒度：按 command signature。
3. slow 统计窗口：最近 2 次相同 signature 执行。
4. 统计边界：默认不跨 day。
5. 当连续 2 次 slow 且平均耗时 > 预算 1.5 倍，才剥离到 `async_ci`。
6. 剥离动作必须记录在 day-notes。
7. baseline 报告触发条件：`sync_fast` 命令数 >1 或平均耗时 >30 秒。

### 12.2 async_ci
1. 全量测试、构建、安全扫描异步执行。
2. 失败可阻塞合并，不阻塞同步编码。
3. 必须按固定块回写 day-notes：
```md
## ASYNC_CI
- job: ci-main-20260226-01
- result: failed
- log: logs/raw/ci-main-20260226-01.log
- digest: err_1ab2cd
- next_action: 修复 src/a.ts:12 的 eslint 错误
```

---

## 13. SDD/TDD 策略（唯一准则）

### 13.1 SDD（强制）
1. 蓝图必须覆盖：数据结构、接口变更、关键 I/O、回滚点。

### 13.2 TDD（条件触发）
1. 业务逻辑且可测试：执行 RED -> GREEN -> REFACTOR。
2. 配置/文档/脚手架：可标记 `TDD_NA`，并给替代验证。

---

## 14. workflow.json 规范（v5.7）

### 14.1 必填字段
1. `commands.sync_fast`
2. `commands.async_ci`
3. `execution.sync_fast_budget_seconds`
4. `retry.max_attempts`
5. `retry.loop_exit_code`
6. `runtime.state_file`
7. `runtime.auto_bootstrap_wrapper`
8. `fuse.window_seconds`
9. `logging.error_digest`
10. `logging.signature_mode`
11. `memory.handover_file`
12. `day_pointer.file`
13. `evidence.diff_stat_command`
14. `evidence.diff_name_command`
15. `execution.stats_scope`

### 14.2 示例
```json
{
  "project": "system-max",
  "execution_mode": "day-card-first",
  "execution": {
    "sync_fast_budget_seconds": 60,
    "stats_scope": "day"
  },
  "commands": {
    "sync_fast": [
      "npm run lint:staged",
      "npm run test:smoke"
    ],
    "async_ci": [
      "npm ci",
      "npm run lint",
      "npm test",
      "npm run build"
    ]
  },
  "retry": {
    "max_attempts": 3,
    "loop_exit_code": 21
  },
  "runtime": {
    "state_file": ".codex_runtime.json",
    "auto_bootstrap_wrapper": false
  },
  "fuse": {
    "window_seconds": 600
  },
  "logging": {
    "error_digest": true,
    "raw_log_dir": "logs/raw",
    "signature_mode": "whitespace_path_whitelist"
  },
  "evidence": {
    "diff_stat_command": "git diff --numstat HEAD",
    "diff_name_command": "git diff --name-only HEAD"
  },
  "memory": {
    "handover_file": "docs/handover.md",
    "session_notes": "docs/session-notes.md",
    "backlog": "docs/active-backlog.md"
  },
  "day_pointer": {
    "file": "codex-tasks/today.md"
  }
}
```

### 14.3 Implementation Contract（强制）
1. `scripts/log_cmd.(ps1|sh)` 输入参数必须支持：`--cmd`、`--cwd`、`--timeout`、`--tag`。
2. `scripts/log_cmd.(ps1|sh)` 输出必须包含：`EXIT_CODE=<n>`、`DURATION_MS=<n>`、`DIGEST=<id|NONE>`。
3. 原始日志命名规则：`logs/raw/<tag>-<timestamp>.log`。
4. 每次关键命令结束后必须刷新 `.codex_runtime.json`：`updated_at`、`last_exit_code`、`last_command.signature`、`last_command.digest`、`fuse.*`。
5. day-notes 追加写入必须进入固定区块：`COMMANDS`、`DIGESTS`、`RISKS`。
6. 禁止新增未在本 PRD 声明的新顶层目录。

### 14.4 Implementation Strict Mode（强制）
1. 未定义的统计窗口默认仅针对当前 day。
2. 不得新增隐含统计维度（如全局跨命令 slow 聚合）。
3. 不得基于语义猜测错误类型；仅按配置与规则匹配执行。
4. 不得擅自扩展状态字段、退出码、证据判定口径。

---

## 15. 必备模板

### 15.1 `AGENTS.md` 最小模板
```md
# AGENTS

一句话总指令：严格按 Read Order 读文件；按 workflow 执行命令且关键命令必须走 wrapper；每步写 day-notes；遇到 20/21 必须写 handover 并停止。
Do not invent：不得新增未声明的顶层目录；不得新增未定义状态字段/退出码；不得自行更改签名与证据口径。

## Read Order (Must)
1. docs/handover.md
2. docs/active-backlog.md
3. config/workflow.json
4. codex-tasks/today.md
5. codex-tasks/dayNN.md

## Command Policy (Must)
- Key commands are exactly what workflow.json declares in commands.sync_fast/commands.async_ci
- Key commands must run via scripts/log_cmd.ps1 (or scripts/log_cmd.sh)
- If wrapper unavailable: write WRAPPER_BYPASS in day-notes with reason/risk/recovery

## Output Policy
- Update evidence/dayNN/day-notes.md
- Update docs/handover.md on DAY_DONE/BLOCKED/LOOP_DETECTED
```

### 15.2 `codex-tasks/today.md` 模板
```md
current_day: day03
reason: wrapper hardening and digest tuning
updated_at: 2026-02-26T10:30:00Z
```

### 15.3 `evidence/dayNN/day-notes.md` 模板
```md
# Day Notes - dayNN

## PLAN
-

## CHANGES
-

## COMMANDS
-

## DIGESTS
-

## FUNCTIONAL_VERIFY
-

## RISKS
-

## WRAPPER_BYPASS (optional)
-
```

### 15.4 `docs/handover.md` 模板
```md
# CONTEXT_HANDOVER

## STATUS
- DAY_DONE | BLOCKED | LOOP_DETECTED

## TODAY_RESULT
-

## KEY_DECISIONS
-

## OPEN_BLOCKERS
-

## NEXT_MIN_ACTION
-

## EVIDENCE_REF
-
```

---

## 16. Day 任务卡模板
```md
# Day NN - <任务名>

## 1. 需求收敛
- 目标：
- 非目标：
- 约束：
- 风险：
- 验收标准：

## 2. 计划拆解（3-7 步）
1.
2.
3.

## 3. SDD 蓝图
- 数据结构：
- 接口变更：
- 关键 I/O：
- 回滚点：

## 4. TDD 策略
- [ ] 适用（RED->GREEN->REFACTOR）
- [ ] 不适用（TDD_NA，替代验证：）

## 5. 实施范围
- 输入文件：
- 输出文件：

## 6. 验证命令
1.
2.
3.

## 7. 交付
- 变更摘要：
- 证据路径：
- 剩余风险：
```

---

## 17. 14 天计划（执行版）
| Day | 核心目标 | 验证方式 | 关键产出 |
|---:|---|---|---|
| 1 | 入口与 wrapper 自检落地 | 文件检查 + 自检执行 | AGENTS + wrapper |
| 2 | runtime 初始化/恢复落地 | 首次运行 + 损坏注入 | `.codex_runtime.json` |
| 3 | Error-Digest 落地 | 长日志提纯演练 | digest 记录 |
| 4 | day-notes/handover 模板接入 | 模板核查 | 证据主档 |
| 5 | sync_fast 基线测量（条件触发） | 预算压测 | baseline 报告或豁免记录 |
| 6 | async_ci 接通 | 回写检查 | ASYNC_CI 块 |
| 7 | 第一次闭环回放 | 全链路复盘 | DAY_DONE 记录 |
| 8 | 循环异常演练 | 熔断触发验证 | LOOP_DETECTED 记录 |
| 9 | 超时异常演练 | slow 规则验证 | 降级记录 |
| 10 | 缺依赖异常演练 | 恢复验证 | 恢复步骤 |
| 11 | 第二次闭环回放 | 全链路复盘 | DAY_DONE 记录 |
| 12 | bypass 治理复盘 | 连续 dayNN 统计 | backlog 条目 |
| 13 | 缺口修复 | 回归验证 | 修复记录 |
| 14 | 终验交付 | DoD 检查 | 终版交付包 |

---

## 18. 交付清单

### 18.1 必交
1. `AGENTS.md`
2. `config/workflow.json`
3. `config/workflow.schema.json`
4. `codex-tasks/today.md`
5. `codex-tasks/day01.md`（后续 day 文件按需创建）
6. `scripts/log_cmd.sh` 或 `scripts/log_cmd.ps1`
7. `.codex_runtime.json`
8. `docs/conventions.md`
9. `docs/session-notes.md`
10. `docs/active-backlog.md`
11. `docs/handover.md`
12. `evidence/dayNN/day-notes.md`
13. `docs/gap-close-report.md`

### 18.2 必交（二选一）
1. `tests/wrapper/*`（有测试框架时），或
2. `scripts/smoke_wrapper.sh|ps1` + `docs/wrapper-smoke.md`（无测试框架时）。

### 18.3 可选增强
1. `scripts/plan.ps1`
2. `scripts/work.ps1`
3. `scripts/review.ps1`
4. `scripts/finish.ps1`
5. `.githooks/pre-commit`
6. `.githooks/pre-push`

---

## 19. DoD（完成定义）

### 19.1 必须满足
- [ ] 目标功能与需求一致，无越界修改。
- [ ] 新增/受影响测试通过；或 `TDD_NA` + 替代验证通过。
- [ ] Lint/Typecheck 通过（如项目有）。
- [ ] Build 通过（如项目有）。
- [ ] 至少一次关键路径功能验证并留痕（CLI/API/UI 任一）。
- [ ] 异常触发时可熔断且有恢复记录。
- [ ] 输出“变更说明 + 验证证据 + 剩余风险”。

### 19.2 一票否决
1. 未定位根因即宣称修复完成。
2. 无证据链即宣称完成。
3. 触发 `21` 后继续自动重试。
4. 关键命令绕过 wrapper 且未记录 `WRAPPER_BYPASS`。

---

## 20. 风险与降级策略
| 风险 | 触发信号 | 降级动作 |
|---|---|---|
| 循环暴走 | 同签名同digest失败 `>=3` | 熔断退出 `21`，转人工问题列表 |
| sync_fast 超预算 | 连续2次slow且均值>1.5x预算 | 剥离慢命令到 async_ci |
| 日志污染上下文 | 单次日志过长 | 启用 digest，仅传摘要 |
| day 指针错乱 | today 与实际任务不一致 | 返回 `20` 并执行恢复动作模板 |
| wrapper 不可用 | 脚本不存在或报错 | 自检后自动生成或返回 `20 BLOCKED` |

---

## 21. 结论
v5.7 已逐条吸收本轮审查问题，并进一步消除统计与判定歧义，形成更稳定的 Codex 执行契约。该版本可直接提交审查，并可直接用于后续 Codex Vibe Coding 执行。



