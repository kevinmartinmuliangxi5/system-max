---
name: skill-creator
description: Meta-skill for creating new Claude Code skills. Use when user wants to create, build, or generate a new skill with proper structure and best practices. Guides through skill creation from concept to packaged .skill file.
argument-hint: [skill-name]
---

# Skill Creator

用于创建新 Claude Code Skills 的元技能（Meta-Skill）。

## 核心功能

当用户想要创建新 skill 时，引导完成以下步骤：

1. **理解需求** - 通过具体例子明确 skill 的功能
2. **规划内容** - 确定需要的 scripts/references/assets
3. **初始化结构** - 创建标准目录和 SKILL.md 模板
4. **编写内容** - 实现技能功能和文档
5. **验证打包** - 检查并生成 .skill 文件

## Skill 目录结构

```
skill-name/
├── SKILL.md           # 必需：主指令文件（YAML + Markdown）
├── scripts/           # 可选：可执行脚本（Python/Bash等）
├── references/        # 可选：参考文档（按需加载）
└── assets/            # 可选：资源文件（模板、图标等）
```

## SKILL.md 模板

每个 SKILL.md 必须包含两部分：

### 1. YAML Frontmatter（必需）

```yaml
---
name: my-skill
description: 这个技能做什么，何时使用。包含触发关键词和使用场景。
argument-hint: [参数提示]  # 可选
---
```

**重要：**
- `description` 是主要触发机制，必须清晰完整
- 包含 "做什么" + "何时使用"
- 不要在 body 中写 "When to Use"（body 只在触发后加载）

### 2. Markdown Body（指令内容）

使用**祈使句/不定式**形式编写指令。

## 核心原则

### 简洁即关键
> Context window is a public good.（上下文窗口是公共资源）

- 只添加 Claude 没有的知识
- 用简洁示例代替冗长解释
- 挑战每条信息："这真的需要吗？"

### 渐进式披露
三层加载机制：
| 层级 | 内容 | 何时加载 |
|------|------|----------|
| Metadata | name + description | 始终 (~100词) |
| SKILL.md | 指令主体 | 触发时 (<5000词) |
| Resources | scripts/references/assets | 按需加载 |

### 适当的自由度
- **高自由度**（文本指令）：多种方法有效时
- **中自由度**（伪代码/脚本）：有首选模式时
- **低自由度**（严格脚本）：操作脆弱必须一致时

## 创建新 Skill 步骤

### 步骤 1：理解需求

通过具体例子明确功能：
- "这个 skill 应该支持什么功能？"
- "能给我一些使用场景的例子吗？"
- "用户会说什么来触发这个 skill？"

### 步骤 2：规划内容

分析每个例子，确定需要的资源：

**scripts/** - 当需要：
- 重复重写相同代码
- 需要确定性可靠性
- 例如：`rotate_pdf.py`

**references/** - 当需要：
- 领域知识、API 文档
- 数据库 schema、公司政策
- 例如：`schema.md`, `api_docs.md`

**assets/** - 当需要：
- 模板、图标、字体
- 输出中使用的文件
- 例如：`logo.png`, `template.html`

### 步骤 3：初始化结构

```bash
# 创建目录
mkdir -p .claude/skills/<skill-name>/{scripts,references,assets}

# 创建 SKILL.md（使用下面的模板）
```

### 步骤 4：编写内容

**优先级顺序：**
1. 先实现 scripts/（需要测试确保无 bug）
2. 准备 references/（详细参考文档）
3. 收集 assets/（模板和资源）
4. 最后编写 SKILL.md

**SKILL.md 写作指南：**
- 使用祈使句（"Create...", "Generate..."）
- description 包含触发场景
- body 保持精简（<500行）
- 详细内容放 references/

### 步骤 5：验证检查

确保 SKILL.md 包含：
- ✅ YAML frontmatter 有效
- ✅ `name` 字段存在
- ✅ `description` 清晰完整（含触发场景）
- ✅ Body 使用祈使句
- ✅ 无冗余文件（README.md 等）

## 输出模式参考

当需要特定输出格式时，参考 [references/output-patterns.md](references/output-patterns.md)

## 使用示例

用户只需说：
- "创建一个 skill 用于处理植物数据"
- "帮我建一个 skill 来生成 ZenGarden 组件"
- "/skill-creator PlantManager"

## 注意事项

- 检查 skill 是否已存在，避免覆盖
- 遵循现有项目代码风格
- script 必须经过测试
- 删除不需要的示例文件
