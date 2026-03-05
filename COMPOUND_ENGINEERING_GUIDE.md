# Compound Engineering 使用说明手册

> **版本**: 2.31.1
> **更新日期**: 2026-02-12
> **作者**: Kieran Klaassen (Every Inc.)

---

## ⚠️ 重要提示：命令名称已修复

由于原插件使用冒号 `:` 分隔符（如 `workflows:brainstorm`），在 Claude Code 中无法正常加载。

**已修复**：所有命令名称中的冒号已替换为连字符 `-`

---

## 目录

1. [什么是 Compound Engineering](#什么是-compound-engineering)
2. [核心理念](#核心理念)
3. [安装验证](#安装验证)
4. [组件概览](#组件概览)
5. [核心工作流](#核心工作流)
6. [Agent 使用指南](#agent-使用指南)
7. [命令使用指南](#命令使用指南)
8. [技能使用指南](#技能使用指南)
9. [最佳实践](#最佳实践)
10. [常见问题](#常见问题)

---

## 什么是 Compound Engineering

Compound Engineering 是一套由 Every Inc. 开发的 AI 辅助开发工具集，旨在通过**复利效应**让每次工程工作都使后续工作变得更容易。

**传统开发困境**：
- 每次功能添加都会增加技术债务
- 代码库随时间推移变得越来越难维护
- 知识散落在各处，难以复用

**Compound Engineering 解决方案**：
- 每个解决问题的经验都被记录和固化
- 多 Agent 协作从不同角度审查代码
- 知识管理系统自动积累团队智慧

---

## 核心理念

### 工作流程

```
Plan (40%) -> Work (20%) -> Review (40%) -> Compound (持续)
   计划          执行            审查             积累
```

### 时间分配原则

| 阶段 | 占比 | 说明 |
|------|------|------|
| **Plan** | 40% | 写代码前充分规划，避免返工 |
| **Work** | 20% | 实际编写代码，因为已充分规划 |
| **Review** | 40% | 多 Agent 审查，确保质量 |
| **Compound** | 持续 | 将经验固化为知识库 |

---

## 安装验证

### 已安装组件统计

| 组件类型 | 数量 |
|----------|------|
| Agents (代理) | 29 个 |
| Commands (命令) | 24 个 |
| Skills (技能) | 18 个 |
| MCP Servers | 1 个 (Context7) |

### 验证安装

```bash
# 检查插件目录
ls ~/.claude/plugins/cache/every-marketplace/compound-engineering/2.31.1/

# 检查 MCP 服务器配置
cat ~/.claude/settings.json | grep context7

# 检查已安装插件
cat ~/.claude/plugins/installed_plugins.json | grep compound-engineering
```

---

## 组件概览

### 1. Commands (24个命令)

#### 核心工作流命令 (5个)

| 命令 | 用途 |
|------|------|
| `/workflows-brainstorm` | 在规划前探索需求和方案 |
| `/workflows-plan` | 创建详细实现计划 |
| `/workflows-work` | 系统化执行工作项 |
| `/workflows-review` | 全面代码审查 |
| `/workflows-compound` | 记录学习以积累团队知识 |

#### 实用工具命令 (19个)

| 命令 | 用途 |
|------|------|
| `/lfg` | 全自动工程工作流 |
| `/slfg` | 群体模式并行执行 |
| `/deepen-plan` | 用并行研究代理增强计划 |
| `/changelog` | 创建近期合并的变更日志 |
| `/create-agent-skill` | 创建或编辑 Claude Code 技能 |
| `/generate-command` | 生成新的斜杠命令 |
| `/heal-skill` | 修复技能文档问题 |
| `/technical-review` | 多 Agent 技术/架构审查 |
| `/report-bug` | 报告插件中的 Bug |
| `/reproduce-bug` | 使用日志复现 Bug |
| `/resolve-parallel` | 并行解决 TODO 注释 |
| `/resolve-todo-parallel` | 并行解决待办事项 |
| `/test-browser` | 在 PR 影响页面上运行浏览器测试 |
| `/test-xcode` | 在模拟器上构建测试 iOS 应用 |
| `/feature-video` | 录制视频演示并添加到 PR |
| `/agent-native-audit` | 审计 Agent 原生架构 |
| `/deploy-docs` | 部署文档 |
| `/release-docs` | 发布文档 |
| `/triage` | 分类和优先级排序问题 |

### 2. Agents (29个专业代理)

#### Review (审查类) - 15个
| 代理名称 | 用途 |
|----------|------|
| `agent-native-reviewer` | 验证功能是否 Agent 原生 |
| `architecture-strategist` | 分析架构决策和合规性 |
| `code-simplicity-reviewer` | 简洁性和最小化审查 |
| `data-integrity-guardian` | 数据库迁移和数据完整性 |
| `data-migration-expert` | 验证 ID 映射 |
| `deployment-verification-agent` | 创建部署检查清单 |
| `dhh-rails-reviewer` | DHH 风格的 Rails 代码审查 |
| `julik-frontend-races-reviewer` | JavaScript 竞态条件审查 |
| `kieran-rails-reviewer` | Kieran 风格的 Rails 审查 |
| `kieran-python-reviewer` | Kieran 风格的 Python 审查 |
| `kieran-typescript-reviewer` | Kieran 风格的 TypeScript 审查 |
| `pattern-recognition-specialist` | 分析代码模式和反模式 |
| `performance-oracle` | 性能分析和优化 |
| `schema-drift-detector` | 检测 schema.rb 变更 |
| `security-sentinel` | 安全审计和漏洞评估 |

#### Research (研究类) - 5个
| 代理名称 | 用途 |
|----------|------|
| `best-practices-researcher` | 收集外部最佳实践 |
| `framework-docs-researcher` | 研究框架文档 |
| `git-history-analyzer` | 分析 Git 历史和代码演进 |
| `learnings-researcher` | 搜索团队历史解决方案 |
| `repo-research-analyst` | 研究仓库结构和约定 |

#### Design (设计类) - 3个
| 代理名称 | 用途 |
|----------|------|
| `design-implementation-reviewer` | 验证 UI 实现与设计匹配 |
| `design-iterator` | 系统性迭代设计 |
| `figa-design-sync` | 与 Figma 设计同步 |

#### Workflow (工作流类) - 5个
| 代理名称 | 用途 |
|----------|------|
| `bug-reproduction-validator` | 系统性复现和验证 Bug |
| `every-style-editor` | 按 Every 风格编辑内容 |
| `lint` | 运行 Ruby/ERB 代码质量检查 |
| `pr-comment-resolver` | 处理 PR 评论和修复 |
| `spec-flow-analyzer` | 分析用户流程 |

#### Docs (文档类) - 1个
| 代理名称 | 用途 |
|----------|------|
| `ankane-readme-writer` | 创建 Ankane 风格的 README |

### 3. Skills (18个技能)

#### 架构与设计 (2个)
| 技能 | 用途 |
|------|------|
| `agent-native-architecture` | 使用提示原生架构构建 AI Agent |
| `frontend-design` | 创建生产级前端界面 |

#### 开发工具 (6个)
| 技能 | 用途 |
|------|------|
| `andrew-kane-gem-writer` | 按 Andrew Kane 模式编写 Ruby Gems |
| `create-agent-skills` | 创建 Claude Code 技能的专家指导 |
| `dhh-rails-style` | 按 DHH 37signals 风格编写 Ruby/Rails |
| `dspy-ruby` | 使用 DSPy.rb 构建类型安全的 LLM 应用 |
| `skill-creator` | 创建有效 Claude Code 技能的指南 |
| `gemini-imagegen` | 使用 Google Gemini API 生成和编辑图像 |

#### 内容与工作流 (4个)
| 技能 | 用途 |
|------|------|
| `brainstorming` | 通过协作对话探索需求和方案 |
| `document-review` | 通过结构化自我审查改进文档 |
| `every-style-editor` | 审查文本是否符合 Every 风格指南 |
| `file-todos` | 基于文件的待办事项跟踪系统 |

#### 多 Agent 编排 (2个)
| 技能 | 用途 |
|------|------|
| `orchestrating-swarms` | 多 Agent 群体编排综合指南 |
| `compound-docs` | 将已解决的问题捕获为分类文档 |

#### 文件传输 (1个)
| 技能 | 用途 |
|------|------|
| `rclone` | 上传文件到 S3、Cloudflare R2、Backblaze B2 |

#### 浏览器自动化 (1个)
| 技能 | 用途 |
|------|------|
| `agent-browser` | 使用 Vercel agent-browser 进行 CLI 浏览器自动化 |

#### 版本控制 (2个)
| 技能 | 用途 |
|------|------|
| `git-worktree` | 管理用于并行开发的 Git worktree |

---

## 核心工作流

### 完整开发周期

```
1. BRAINSTORM (头脑风暴)
   ↓
2. PLAN (详细规划)
   ↓
3. WORK (执行开发)
   ↓
4. REVIEW (多 Agent 审查)
   ↓
5. COMPOUND (知识积累)
   ↓
6. 重复下一个周期
```

### 阶段详解

#### 1. Brainstorm 头脑风暴

```bash
/workflows-brainstorm
```

**目的**：在深入规划前探索需求、方案和潜在问题

**输出**：
- 需求理解
- 多种实现方案
- 风险和依赖识别
- 推荐方案

#### 2. Plan 详细规划

```bash
/workflows-plan
```

**目的**：创建详细的实现计划

**输出**：
- 分步实施计划
- 文件变更清单
- 测试策略
- 依赖关系图

#### 3. Work 执行开发

```bash
/workflows-work
```

**目的**：系统化执行工作项

**特点**：
- 使用 Git worktree 进行并行开发
- 任务跟踪和进度管理
- 自动保存中间状态

#### 4. Review 代码审查

```bash
/workflows-review
```

**目的**：多 Agent 全面代码审查

**审查维度**：
- 架构合理性
- 代码风格
- 安全性
- 性能
- 测试覆盖
- 文档完整性

#### 5. Compound 知识积累

```bash
/workflows-compound
```

**目的**：将解决的问题记录为团队知识

**输出**：
- 分类的问题解决方案
- 可复用的代码模式
- 最佳实践文档

---

## Agent 使用指南

### 调用语法

```bash
# 基本语法
agent <agent-name> "<prompt>"

# 示例
agent security-sentinel "审查登录页面的安全漏洞"
```

### 常用使用场景

#### 1. 代码审查

```bash
# Rails 代码审查 (DHH 风格)
agent dhh-rails-reviewer "审查以下 Rails 代码是否符合 37signals 风格"

# TypeScript 代码审查
agent kieran-typescript-reviewer "审查 React 组件的类型定义"

# Python 代码审查
agent kieran-python-reviewer "审查数据处理脚本"

# 前端竞态条件审查
agent julik-frontend-races-reviewer "检查 Stimulus 控制器是否存在竞态条件"
```

#### 2. 研究分析

```bash
# 查找最佳实践
agent best-practices-researcher "搜索 Rails 中处理批量更新的最佳实践"

# 研究框架文档
agent framework-docs-researcher "查找 Next.js App Router 的最新文档"

# 分析 Git 历史
agent git-history-analyzer "分析用户模型的历史变更"

# 搜索团队学习
agent learnings-researcher "搜索之前如何解决类似的数据库迁移问题"
```

#### 3. 架构与设计

```bash
# 架构分析
agent architecture-strategist "分析微服务架构的决策是否合理"

# 模式识别
agent pattern-recognition-specialist "识别代码中的反模式"

# 性能分析
agent performance-oracle "分析 API 响应时间慢的原因"

# 安全审查
agent security-sentinel "审查文件上传功能的安全漏洞"
```

#### 4. 数据与部署

```bash
# 数据完整性检查
agent data-integrity-guardian "验证用户数据迁移的完整性"

# Schema 变更检测
agent schema-drift-detector "检查 PR 中的 schema.rb 变更是否相关"

# 部署验证
agent deployment-verification-agent "创建部署前的 Go/No-Go 检查清单"
```

### 多 Agent 并行工作

```bash
# 使用 /slfg 命令启动群体模式
/slfg

# 使用 /technical-review 进行多维度审查
/technical-review
```

---

## 命令使用指南

### 工作流命令详解

#### `/workflows-brainstorm`

```
用途：在深入规划前进行头脑风暴
时机：开始新功能或解决复杂问题前
输入：功能描述或问题描述
输出：需求理解、方案选项、风险评估
```

**示例场景**：
- 添加新功能 "用户评分系统"
- 重构 "支付处理流程"
- 优化 "数据库查询性能"

#### `/workflows-plan`

```
用途：创建详细的实现计划
时机：brainstorm 完成后
输入：brainstorm 的输出或功能需求
输出：分步计划、文件清单、测试策略
```

**计划包含**：
1. 实施步骤（按优先级排序）
2. 需要创建/修改的文件
3. 测试计划
4. 潜在风险和缓解措施

#### `/workflows-work`

```
用途：系统化执行工作项
时机：计划完成后
输入：workflows-plan 生成的计划
输出：完成的代码、测试、文档
```

**特点**：
- 自动创建 Git worktree
- 任务进度跟踪
- 中间状态保存

#### `/workflows-review`

```
用途：全面代码审查
时机：代码完成后，合并 PR 前
输入：PR 或文件变更
输出：审查报告、改进建议
```

**审查包括**：
- 多 Agent 并行审查
- 不同维度分析（架构、安全、性能）
- 可执行的建议

#### `/workflows-compound`

```
用途：将学习固化为知识
时机：解决任何问题后
输入：问题和解决方案
输出：分类的知识条目
```

**知识类型**：
- 问题解决方案
- 代码模式
- 最佳实践
- 反模式警告

### 实用命令详解

#### `/lfg` - 全自动工作流

```
用途：一键启动完整工程流程
包含：brainstorm -> plan -> work -> review
```

#### `/slfg` - 群体模式

```
用途：并行执行多个 Agent
特点：更快的结果，多角度分析
```

#### `/technical-review`

```
用途：多 Agent 技术和架构审查
维度：架构、安全、性能、可维护性
```

#### `/changelog`

```
用途：创建吸引人的变更日志
输入：近期 PR 的描述
输出：格式化的变更日志
```

#### Bug 相关命令

| 命令 | 用途 |
|------|------|
| `/reproduce-bug` | 使用日志和复现步骤复现 Bug |
| `/report-bug` | 向插件维护者报告 Bug |

---

## 技能使用指南

### 调用语法

```bash
skill <skill-name> ["<prompt>"]

# 示例
skill dhh-rails-style "按 DHH 风格编写用户注册控制器"
skill gemini-imagegen "生成一个登录界面的设计图"
```

### 常用技能详解

#### 1. 编码风格技能

**dhh-rails-style**
```bash
skill dhh-rails-style "编写一个用户管理的 Rails 控制器"
```
- 按 37signals/DHH 风格编写代码
- 简洁、可维护的 Rails 实践

#### 2. 前端设计技能

**frontend-design**
```bash
skill frontend-design "创建一个响应式导航栏组件"
```
- 生产级前端界面
- Tailwind CSS 最佳实践
- 可访问性考虑

#### 3. 文档技能

**compound-docs**
```bash
skill compound-docs "记录解决的这个数据库迁移问题"
```
- 分类的问题解决方案
- 可复用的知识库

#### 4. 图像生成技能

**gemini-imagegen**
```bash
skill gemini-imagegen "生成一个现代风格的登录界面设计"
```

**要求**：
- 环境变量 `GEMINI_API_KEY`
- Python 包：`google-genai`, `pillow`

**功能**：
- 文本生成图像
- 图像编辑和操作
- 多轮精炼
- 多参考图像合成（最多 14 张）

#### 5. 浏览器自动化技能

**agent-browser**
```bash
skill agent-browser "如何使用 agent-browser 进行浏览器测试"
```

**安装**：
```bash
npm install -g agent-browser
agent-browser install  # 下载 Chromium
```

#### 6. 文件传输技能

**rclone**
```bash
skill rclone "上传文件到 S3"
```

**支持**：S3、Cloudflare R2、Backblaze B2

---

## 最佳实践

### 1. 遵循 80/20 原则

```
80% 规划和审查 + 20% 执行 = 高质量代码
```

**原因**：
- 充分规划避免返工
- 多 Agent 审查捕获问题
- 执行变得简单直接

### 2. 充分利用研究型 Agent

在写代码前，先做功课：
```bash
# 1. 搜索最佳实践
agent best-practices-researcher "搜索...的最佳实践"

# 2. 研究框架文档
agent framework-docs-researcher "查找...的文档"

# 3. 查看团队历史
agent learnings-researcher "搜索之前如何解决...问题"

# 4. 分析代码演进
agent git-history-analyzer "分析...的历史变更"
```

### 3. 多 Agent 并行审查

```bash
# 使用群体模式
/slfg

# 或使用技术审查命令
/technical-review
```

**好处**：
- 多角度分析
- 更快的结果
- 更全面的问题识别

### 4. 坚持知识复利

每次解决问题后：
```bash
/workflows-compound
```

**积累什么**：
- 解决方案模式
- 避免的错误
- 性能优化技巧
- 安全最佳实践

### 5. 使用 Context7 查询框架文档

Context7 MCP 服务器支持 100+ 框架：
- Rails, React, Next.js, Vue
- Django, Laravel, Spring
- 等等...

### 6. Git Worktree 并行开发

```bash
skill git-worktree "管理多个并行任务"
```

**好处**：
- 同时处理多个功能
- 隔离不同任务
- 更快的迭代

---

## 常见问题

### Q1: MCP 服务器无法自动加载怎么办？

**问题**：Context7 文档查询功能不工作

**解决方案**：
手动添加到 `~/.claude/settings.json`：
```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

### Q2: 如何检查插件是否正确安装？

```bash
# 检查安装
ls ~/.claude/plugins/cache/every-marketplace/compound-engineering/2.31.1/

# 检查组件
ls ~/.claude/plugins/cache/every-marketplace/compound-engineering/2.31.1/agents/
ls ~/.claude/plugins/cache/every-marketplace/compound-engineering/2.31.1/commands/
ls ~/.claude/plugins/cache/every-marketplace/compound-engineering/2.31.1/skills/
```

### Q3: Agent 调用失败怎么办？

**检查清单**：
1. 确认 Agent 名称正确（见上方 Agent 列表）
2. 确认插件已正确安装
3. 检查是否有权限问题
4. 查看 Claude Code 日志

### Q4: 命令显示 Unknown skill 怎么办？

**原因**：原插件命令名称使用冒号（如 `workflows:plan`），已修复为连字符

**解决方案**：使用修复后的命令名称
- `/workflows-brainstorm` （不是 `/workflows:brainstorm`）
- `/workflows-plan`
- `/workflows-work`
- `/workflows-review`
- `/workflows-compound`

### Q5: 如何更新插件？

```bash
cd ~/.claude/plugins/marketplaces/compound-engineering-plugin
git pull
```

### Q6: 技能 gemini-imagegen 无法使用？

**检查**：
1. 设置环境变量：`export GEMINI_API_KEY=your_key`
2. 安装 Python 包：`pip install google-genai pillow`
3. 验证 API Key 有效

### Q7: 浏览器自动化如何设置？

```bash
# 安装 agent-browser
npm install -g agent-browser

# 下载 Chromium
agent-browser install

# 使用技能
skill agent-browser "如何进行浏览器测试"
```

---

## 参考资源

### 官方资源

- **GitHub 仓库**：https://github.com/EveryInc/compound-engineering-plugin
- **官方博客（Compound Engineering 介绍）**：https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents
- **幕后故事**：https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it

### Claude Code 文档

- [Claude Code 插件文档](https://docs.claude.com/en/docs/claude-code/plugins)
- [插件市场文档](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [插件参考](https://docs.claude.com/en/docs/claude-code/plugins-reference)

---

## 附录

### 快速参考卡

```
# 核心工作流
/workflows-brainstorm → /workflows-plan → /workflows-work → /workflows-review → /workflows-compound

# 快速命令
/lfg                   ← 全自动工作流
/slfg                  ← 群体模式并行
/technical-review        ← 多维度技术审查

# 常用 Agent
agent kieran-rails-reviewer       ← Rails 代码审查
agent security-sentinel           ← 安全审查
agent performance-oracle          ← 性能分析
agent best-practices-researcher   ← 搜索最佳实践

# 常用技能
skill dhh-rails-style            ← DHH 风格编码
skill frontend-design             ← 前端设计
skill compound-docs               ← 文档化学习
```

---

**祝你在 Compound Engineering 的道路上越走越顺！** 🚀
