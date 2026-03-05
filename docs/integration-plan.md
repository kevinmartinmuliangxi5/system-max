# GitHub 热榜调研：集成方案文档

> 时间：2026-02-22
> 执行脑：主脑（Claude Sonnet 4.6 / Pro Plan）
> 状态：调研完成，待执行安装

---

## 一、当前环境状态

| 工具 | 状态 | 说明 |
|------|------|------|
| **compound-engineering** plugin | ✅ 已安装 | `every-marketplace` 版，提供 agents/skills/workflows |
| **superpowers** plugin | ✅ 已安装 | `claude-plugins-official` 版 |
| **Context7 MCP** | ✅ 已安装 | HTTP 模式，`https://mcp.context7.com/mcp` |
| **agent-browser** skill | ✅ 已安装 | via compound-engineering，Vercel CLI 浏览器自动化 |
| **Claude-Mem** plugin | ❌ 未安装 | 需手动安装 |
| **everything-claude-code** plugin | ❌ 未安装 | 建议选择性采纳，不建议全量安装 |
| **Chrome DevTools MCP** | ❌ 未安装 | 可选安装，与 agent-browser 互补 |
| **Desktop Commander MCP** | ⚠️ 暂缓 | 安全风险：完整终端访问权限，需主脑专项安全评估 |

---

## 二、Claude-Mem：跨会话记忆方案

### 2.1 功能概述

- **核心能力**：跨对话持久化记忆，不依赖 session-notes.md 手动记录
- **存储**：SQLite（结构化记忆）+ ChromaDB（语义向量检索）
- **令牌效率**：90-95% 令牌节省（相比每次重新提供完整上下文）
- **3层渐进式披露**：Short-term（快速摘要）→ Mid-term（详细上下文）→ Long-term（完整档案）
- **5个生命周期钩子**：自动在会话开始/结束时加载/保存记忆

### 2.2 与现有 session-notes.md 的关系

| 维度 | session-notes.md | Claude-Mem |
|------|-----------------|------------|
| 目标读者 | 人类（可快速审阅） | AI（机器可读，完整上下文） |
| 内容 | 关键决策、方向性判断 | 完整操作历史、代码上下文 |
| 更新方式 | `/handoff` 技能手动写入 | 自动保存（SessionEnd 钩子） |
| 定位 | 人可读决策层 | AI 可读上下文补充层 |

**结论**：两者互补，Claude-Mem **不替代** session-notes.md，而是补充完整的 AI 可读历史。

### 2.3 安装步骤（用户手动执行）

> **注意**：以下为 Claude Code 内部斜杠命令，需在 Claude Code 终端中执行，非 bash 命令。

```
# 步骤 1：通过 marketplace 添加
/plugin marketplace add thedotmack/claude-mem

# 步骤 2：安装插件
/plugin install claude-mem

# 步骤 3：重启 Claude Code 后验证
/mcp   # 确认 claude-mem 出现在已连接列表中
```

**前置条件**：
- Node.js 18+：`node --version` 确认
- Bun 运行时：`bun --version` 确认（如未安装：`npm install -g bun`）

### 2.4 安装后验证

```bash
# 在 Claude Code 对话中测试：
# 1. 结束会话前询问 Claude 记住某个事实
# 2. 开启新会话后询问该事实，验证是否恢复
```

---

## 三、everything-claude-code：选择性采纳方案

### 3.1 项目概述

- **仓库**：`affaan-m/everything-claude-code`（42K stars，Anthropic Hackathon 冠军）
- **规模**：13 agents + 43 skills + 31 commands + hooks 系统
- **安装限制**：Windows 环境下 rules 无法通过插件自动分发，需手动 clone 后运行 install 脚本

### 3.2 推荐采纳组件

#### 3.2.1 continuous-learning-v2 Skill（最高优先级）

**核心价值**：基于钩子的自动学习系统，实现 100% 工具调用观察覆盖率

- **工作原理**：PreToolUse / PostToolUse 钩子自动捕捉工具调用，分析模式，动态更新「本能」
- **置信度评分系统**：0.3（弱信号）→ 0.9（强确认）
- **`/evolve` 命令**：将积累的本能聚合为正式 skill/command/agent

**与现有系统对比**：当前 compound-engineering 有 Phase 7 知识沉淀，但依赖人工触发 `/workflows:compound`；continuous-learning-v2 实现**全自动**观察和积累，两者可并行运行，形成互补：

| 机制 | 触发方式 | 粒度 | 适合场景 |
|------|----------|------|---------|
| CE:/workflows:compound | 人工，会话后 | 问题级别 | 复杂解决方案归档 |
| continuous-learning-v2 | 自动，实时 | 工具调用级别 | 模式识别与快速本能积累 |

**采纳建议**：直接将 `continuous-learning-v2/SKILL.md` 内容添加为本地 skill。

#### 3.2.2 code-reviewer Agent（高优先级）

- 使用 Claude Opus 模型进行深度代码审查
- 专注于 git diff，自动识别 CRITICAL/HIGH/MEDIUM 问题
- **与现有 `superpowers:code-reviewer` 互补**：当前 code-reviewer 是通用审查；该 agent 更专注于代码质量的系统性分类

#### 3.2.3 hooks.json 中的有用钩子（中等优先级）

可选择性集成以下钩子规则到本地 Claude Code hooks 配置：

| 钩子 | 事件 | 功能 |
|------|------|------|
| Prettier 自动格式化 | PostToolUse (write_file) | JS/TS 写入后自动 prettier 格式化 |
| TypeScript 类型检查 | PostToolUse (write_file) | TS 文件写入后自动 tsc --noEmit |
| console.log 警告 | PostToolUse (write_file) | 生产代码中检测 console.log 遗留 |
| 禁止随意创建 .md | PreToolUse (write_file) | 防止 AI 私自创建 README/文档文件 |

> **注意**：multi-plan 命令（`commands/multi-plan.md`）依赖 `mcp__ace-tool__enhance_prompt` 外部工具，当前环境不具备，**不建议采纳**。

### 3.3 不建议采纳的组件

| 组件 | 原因 |
|------|------|
| `/multi-plan` command | 依赖 ace-tool MCP 和 Codex/Gemini 后端，与当前技术栈不兼容 |
| 全量 rules 安装 | Windows 环境脚本兼容性风险；可能引入与现有 compound-engineering 的冲突 |
| 全量 skills 安装 | 43 个 skills 中许多与 compound-engineering 功能重叠，需逐一甄别 |

### 3.4 安装步骤（如选择采纳）

```bash
# 克隆仓库
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# 仅提取 continuous-learning-v2 skill
# 将 skills/continuous-learning-v2/SKILL.md 内容复制到本地技能文件
# Windows 用 Node.js 版本的 install 脚本（如提供）
```

---

## 四、Chrome DevTools MCP vs agent-browser：功能对比与推荐

### 4.1 详细对比

| 维度 | agent-browser (Vercel CLI) | Chrome DevTools MCP |
|------|---------------------------|---------------------|
| **接口类型** | Bash CLI 命令 | MCP 工具（26个） |
| **元素选择** | refs (@e1, @e2) | refs (e1) |
| **浏览器控制** | 高层自动化（click/fill/nav） | 低层 DevTools 协议 |
| **性能分析** | ❌ 不支持 | ✅ 支持（CPU/内存分析） |
| **网络请求** | ❌ 不支持 | ✅ 支持（拦截/修改） |
| **JavaScript 调试** | ❌ 不支持 | ✅ 支持（断点/调用栈） |
| **无头模式** | ✅ 支持 | ✅ 支持 |
| **并行会话** | ✅ --session 参数 | ✅ 多标签页 |
| **安装复杂度** | npm install -g | npx（无需全局安装） |
| **前置条件** | Node.js 任意版本 | Node.js v20.19+ |
| **适合场景** | 快速 UI 自动化、表单填写、截图 | 性能调试、网络分析、JS 调试 |

### 4.2 推荐策略：保留两者，按场景选择

```
场景决策树：
├── 需要点击/填表/导航/截图？
│   └── → 使用 agent-browser（已安装，更简单）
├── 需要分析页面性能/内存？
│   └── → 使用 Chrome DevTools MCP
├── 需要调试 JavaScript/断点？
│   └── → 使用 Chrome DevTools MCP
├── 需要拦截/分析网络请求？
│   └── → 使用 Chrome DevTools MCP
└── 两者都能完成的情况？
    └── → 优先 agent-browser（更轻量）
```

### 4.3 Chrome DevTools MCP 安装配置

**安装命令（在 Claude Code 终端执行）**：

```bash
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

**或直接修改 `C:/Users/24140/.claude/settings.json`**（见第五节）：

**前置条件**：
```bash
node --version  # 确认 >= v20.19.0
```

---

## 五、更新后的 settings.json 配置

以下为集成 Chrome DevTools MCP 后的完整配置（Claude-Mem 安装后将由插件系统自动添加）：

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "SHELL": "C:\\Program Files\\Git\\bin\\bash.exe"
  },
  "permissions": {
    "allow": [
      "mcp__pencil"
    ]
  },
  "enabledPlugins": {
    "compound-engineering@every-marketplace": true,
    "superpowers@claude-plugins-official": true
  },
  "skipDangerousModePermissionPrompt": true,
  "bashPath": "C:\\Program Files\\Git\\bin\\bash.exe",
  "bypassPermissionsMode": true,
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    },
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    }
  }
}
```

> **注意**：如需手动添加 chrome-devtools，直接将 `"chrome-devtools"` 块加入 `mcpServers` 对象即可。Node.js v20.19+ 为必要条件。

---

## 六、执行优先级与行动清单

### 立即可执行（高价值，低风险）

- [ ] **安装 Chrome DevTools MCP**：修改 settings.json 或运行 `claude mcp add` 命令。验证：`/mcp` 确认连接
- [ ] **采纳 continuous-learning-v2 skill**：从 everything-claude-code 仓库提取 SKILL.md，添加为本地 skill

### 用户手动执行（需在 Claude Code 终端操作）

- [ ] **安装 Claude-Mem**：`/plugin marketplace add thedotmack/claude-mem` + `/plugin install claude-mem`。前置：确认 Node.js 18+ 和 Bun 已安装

### 评估后执行（中等优先级）

- [ ] **测试 Chrome DevTools MCP**：安装后执行一次真实的性能分析任务，验证工具可用性
- [ ] **集成有用 hooks**：从 everything-claude-code/hooks/hooks.json 提取 Prettier/TypeScript 相关钩子

### 暂缓执行（需安全评估）

- [ ] **Desktop Commander MCP**：主脑需专项安全评估，确认可接受风险后再安装

---

## 七、关键决策汇总

| 决策 | 选择 | 理由 |
|------|------|------|
| everything-claude-code 采纳策略 | 选择性（3个组件） | 全量安装有 Windows 兼容风险且与现有工具重叠 |
| agent-browser vs Chrome DevTools MCP | 保留两者 | 定位不同：前者做 UI 自动化，后者做深度调试 |
| Claude-Mem 与 session-notes.md 关系 | 互补，不替代 | session-notes.md 供人类决策审阅；Claude-Mem 供 AI 完整上下文恢复 |
| multi-plan command | 不采纳 | 依赖 ace-tool 外部 MCP，当前技术栈不兼容 |
| Desktop Commander MCP | 暂缓 | 安全风险过高，给 AI 完整终端控制权需专项评估 |
| Context7 MCP | 无需操作 | 已通过 HTTP 模式集成，工具 `mcp__plugin_compound-engineering_context7` 可用 |

---

*文档生成于：2026-02-22 | 主脑（Claude Sonnet 4.6）*
