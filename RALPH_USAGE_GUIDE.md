# Ralph for Claude Code - 完整使用说明

> 版本: v0.11.2 | 更新时间: 2026年2月

---

## 目录

1. [什么是 Ralph？](#什么是-ralph)
2. [快速开始](#快速开始)
3. [安装指南](#安装指南)
4. [配置说明](#配置说明)
5. [使用方法](#使用方法)
6. [最佳实践](#最佳实践)
7. [注意事项](#注意事项)
8. [故障排除](#故障排除)
9. [高级技巧](#高级技巧)

---

## 什么是 Ralph？

**Ralph for Claude Code** 是一个自主 AI 开发循环管理器，让 Claude Code 能够在无人干预的情况下持续工作数小时，直到项目完成。

### 核心特性

- **自主开发循环** - 持续执行直到任务完成
- **智能退出检测** - 双重条件检查防止过早退出
- **会话连续性** - 跨迭代保持上下文
- **速率限制** - 防止 API 超限
- **实时监控** - tmux 仪表板显示进度
- **熔断器** - 自动检测和恢复卡死循环

### 工作原理

```
你给任务 → Claude 做 → 尝试退出 → Hook 拦截 → 把提示再喂给 Claude
    ↓
再次做 → 再尝试退出 → 再拦截 → 再提示
    ↓
...循环直到满足"完成条件"
```

---

## 快速开始

### 最简使用流程

```bash
# 1. 克隆并安装（只需一次）
git clone https://github.com/frankbria/ralph-claude-code.git
cd ralph-claude-code
./install.sh

# 2. 在现有项目中启用
cd your-project
ralph-enable

# 3. 启动自动开发
ralph --monitor
```

### Windows 用户注意

由于 Ralph 是基于 Bash 的，Windows 用户需要：

1. 安装 **Git Bash** 或 **WSL (Windows Subsystem for Linux)**
2. 确保所有依赖在 Bash 环境中可用
3. 使用 Bash 运行 Ralph 命令

---

## 安装指南

### 系统要求

| 依赖 | 说明 | 安装命令 |
|------|------|----------|
| Bash 4.0+ | 脚本执行 | Linux/Mac 自带，Windows 用 Git Bash/WSL |
| Claude Code CLI | AI 编码助手 | `npm install -g @anthropic-ai/claude-code` |
| tmux | 终端复用器 | `apt install tmux` / `brew install tmux` |
| jq | JSON 处理 | `apt install jq` / `brew install jq` |
| Git | 版本控制 | `apt install git` / 下载安装 |

### 安装步骤

#### 方法一：从 GitHub 安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/frankbria/ralph-claude-code.git
cd ralph-claude-code

# 运行安装脚本
./install.sh

# 验证安装
ralph --version
```

#### 方法二：手动安装

如果无法克隆，可以手动创建文件结构：

```bash
# 1. 创建目录
mkdir -p ~/.ralph
mkdir -p ~/.ralph/logs

# 2. 下载核心脚本
# 从 GitHub 获取 ralph_loop.sh, ralph_monitor.sh 等

# 3. 设置权限
chmod +x ~/.ralph/*.sh

# 4. 添加到 PATH
export PATH="$PATH:$HOME/.ralph"
```

### 卸载

```bash
# 使用卸载脚本
ralph-uninstall

# 或手动删除
rm -rf ~/.ralph
rm -f /usr/local/bin/ralph*
```

---

## 配置说明

### 项目结构

```
your-project/
├── .ralph/                 # Ralph 配置和状态（隐藏文件夹）
│   ├── PROMPT.md           # 主要开发指令
│   ├── fix_plan.md         # 优先任务列表
│   ├── AGENT.md            # 构建和运行指令（自动维护）
│   ├── specs/              # 项目规格和需求
│   │   └── stdlib/         # 标准库规格
│   ├── logs/               # 执行日志
│   └── .ralph_session      # 会话状态
├── .ralphrc                # 项目配置文件
└── src/                    # 源代码实现
```

### .ralphrc 配置文件

这是项目的核心配置文件，包含所有可设置选项：

```bash
# 项目基本信息
PROJECT_NAME="my-project"
PROJECT_TYPE="typescript"    # auto, typescript, python, rust, go

# 循环设置
MAX_CALLS_PER_HOUR=100       # 每小时最大 API 调用数
CLAUDE_TIMEOUT_MINUTES=15    # Claude Code 执行超时
CLAUDE_OUTPUT_FORMAT="json"  # json 或 text

# 工具权限（逗号分隔）
ALLOWED_TOOLS="Write,Read,Edit,Bash(git *),Bash(npm *)"

# 会话管理
SESSION_CONTINUITY=true      # 启用会话连续性
SESSION_EXPIRY_HOURS=24      # 会话过期时间

# 熔断器阈值
CB_NO_PROGRESS_THRESHOLD=3   # 无进度循环数
CB_SAME_ERROR_THRESHOLD=5    # 相同错误循环数

# 退出检测阈值
MAX_CONSECUTIVE_TEST_LOOPS=3     # 连续测试循环数
MAX_CONSECUTIVE_DONE_SIGNALS=2   # 连续完成信号数
TEST_PERCENTAGE_THRESHOLD=30     # 测试循环百分比
```

### PROMPT.md 模板

这是 Ralph 的主要指令文件：

```markdown
# Ralph 开发指令

## 项目概述
[项目描述]

## 核心原则
1. 持续迭代 - 不要期望一次完成
2. 失败是数据 - 从错误中学习
3. 坚持就是胜利 - 不断尝试

## 项目目标

### 具体要求
- [ ] 要求 1
- [ ] 要求 2
- [ ] 要求 3

### 完成标准
当满足以下条件时完成：
- [完成标准 1]
- [完成标准 2]

完成后输出: `<promise>COMPLETE</promise>`

## 开发流程
1. 分析当前状态
2. 实现功能
3. 运行测试
4. 修复问题
5. 重复直到完成
```

### fix_plan.md 模板

```markdown
# Ralph 任务计划

## 任务列表

### 🔴 高优先级
- [ ] **任务 1**: [描述]
  - 状态: 待完成
  - 依赖: 无

### 🟡 中优先级
- [ ] **任务 2**: [描述]
  - 状态: 待完成
  - 依赖: 任务 1

### 🟢 低优先级
- [ ] **任务 3**: [描述]
  - 状态: 待完成
  - 依赖: 任务 2

## 完成标准
所有任务完成时输出 `<promise>COMPLETE</promise>` 并设置 `EXIT_SIGNAL: true`。
```

---

## 使用方法

### 基本命令

```bash
# 启动 Ralph（带监控）
ralph --monitor

# 启动 Ralph（不带监控）
ralph

# 检查状态
ralph --status

# 详细模式
ralph --verbose

# 设置超时（分钟）
ralph --timeout 30

# 设置每小时调用限制
ralph --calls 50

# 禁用会话连续性
ralph --no-continue

# 重置会话
ralph --reset-session

# 重置熔断器
ralph --reset-circuit

# 显示帮助
ralph --help
```

### 项目初始化

#### 方法一：在新项目中

```bash
# 创建新项目
ralph-setup my-awesome-project
cd my-awesome-project

# 编辑配置
# .ralph/PROMPT.md - 项目目标
# .ralph/fix_plan.md - 任务列表

# 启动
ralph --monitor
```

#### 方法二：在现有项目中

```bash
cd your-existing-project

# 交互式向导
ralph-enable

# 从 PRD 导入
ralph-enable --from prd ./docs/requirements.md

# 从 GitHub Issues 导入
ralph-enable --from github --label "sprint-1"

# 从 beads 导入
ralph-enable --from beads

# 启动
ralph --monitor
```

#### 方法三：导入现有文档

```bash
# 导入 PRD
ralph-import product-requirements.md my-app
cd my-app

# 查看生成的文件
ls .ralph/

# 启动
ralph --monitor
```

### 监控和管理

#### 使用 tmux 监控（推荐）

```bash
# 启动带监控的 Ralph
ralph --monitor

# tmux 控制命令
Ctrl+B 然后 D    # 分离会话（Ralph 继续运行）
Ctrl+B 然后 ←/→  # 切换面板
tmux list-sessions        # 查看活动会话
tmux attach -t <name>     # 重新连接
```

#### 手动监控

```bash
# 终端 1：启动 Ralph
ralph

# 终端 2：启动监控
ralph-monitor

# 查看日志
tail -f .ralph/logs/ralph.log

# 检查状态
ralph --status
```

---

## 最佳实践

### 1. 编写有效的提示词

#### ❌ 不好的例子

```markdown
Build a todo API and make it good.
```

#### ✅ 好的例子

```markdown
Build a REST API for todos with the following requirements:

## 功能要求
- CRUD operations for todos
- Input validation
- Unit tests with 80%+ coverage
- API documentation

## 技术栈
- Node.js + Express
- MongoDB for data storage
- Jest for testing

## 完成标准
When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- README with API docs

Output: <promise>COMPLETE</promise>
```

### 2. 任务优先级管理

在 `fix_plan.md` 中明确优先级：

```markdown
### 🔴 高优先级（必须完成）
- [ ] 用户认证
- [ ] 核心业务逻辑

### 🟡 中优先级（应该完成）
- [ ] UI 优化
- [ ] 性能改进

### 🟢 低优先级（可以延后）
- [ ] 文档完善
- [ ] 示例代码
```

### 3. 设置合理的限制

```bash
# 总是设置迭代上限作为安全网
ralph --monitor --max-iterations 20

# 在提示词中包含卡住时的处理
"""
After 15 iterations, if not complete:
- Document what's blocking progress
- List what was attempted
- Suggest alternative approaches
"""
```

### 4. 使用会话连续性

```bash
# 启用会话连续性（默认）
ralph --monitor

# 复杂任务可能需要更长会话
# 编辑 .ralphrc
SESSION_EXPIRY_HOURS=48

# 简单任务可以禁用
ralph --no-continue
```

### 5. 监控和日志

```bash
# 使用详细模式了解进度
ralph --verbose --monitor

# 定期检查日志
tail -f .ralph/logs/ralph.log

# 保存日志用于调试
cp .ralph/logs/ralph.log .ralph/logs/ralph_$(date +%Y%m%d_%H%M%S).log
```

---

## 注意事项

### ⚠️ 重要警告

1. **API 成本**
   - Ralph 可能运行数小时，产生大量 API 调用
   - 始终设置 `MAX_CALLS_PER_HOUR` 限制
   - 监控 Claude 的 5 小时使用限制

2. **无限循环风险**
   - 总是设置 `--max-iterations` 上限
   - 确保完成标准明确可检测
   - 使用熔断器防止卡死

3. **代码安全**
   - Ralph 会修改代码，建议使用 Git
   - 定期提交：`git commit -am "checkpoint"`
   - 可以轻松回滚：`git reset --hard`

4. **生产环境**
   - 不要在生产代码上直接运行
   - 使用分支：`git checkout -b ralph-work`
   - 审查后合并：`git checkout main && git merge ralph-work`

### ✅ 适用场景

| 适合 | 不适合 |
|------|--------|
| 有明确成功标准 | 需要人类审美判断 |
| 可以自动验证 | 一次性操作 |
| 新项目/功能开发 | 紧急生产调试 |
| 测试驱动开发 | 成功标准模糊 |
| 重构和优化 | 需要创意设计 |

### ❌ 避免使用

- 需要人类审查的敏感代码
- 没有自动化测试的项目
- 不明确的探索性任务
- 涉及机密数据的项目

---

## 故障排除

### 常见问题

#### 1. Ralph 停止太早

**原因**：完成检测阈值太低

**解决**：
```bash
# 编辑 .ralphrc
MAX_CONSECUTIVE_DONE_SIGNALS=5  # 增加到 5
```

#### 2. Ralph 永不停止

**原因**：完成标准不明确或无法达到

**解决**：
```bash
# 设置最大迭代次数
ralph --max-iterations 20

# 检查 PROMPT.md 中的完成标准
```

#### 3. 权限被拒绝错误

**原因**：Claude Code 没有工具权限

**解决**：
```bash
# 编辑 .ralphrc
ALLOWED_TOOLS="Write,Read,Edit,Bash(git *),Bash(npm *),Bash(pytest)"

# 重置会话
ralph --reset-session
```

#### 4. 速率限制问题

**原因**：API 调用超过限制

**解决**：
```bash
# 减少每小时调用数
ralph --calls 50

# Ralph 会自动等待并显示倒计时
```

#### 5. tmux 会话丢失

**原因**：网络断开或终端关闭

**解决**：
```bash
# 列出会话
tmux list-sessions

# 重新连接
tmux attach -t ralph
```

#### 6. 5 小时 API 限制

**原因**：Claude 的 5 小时使用限制

**解决**：
```bash
# Ralph 会自动检测并提示
# 选择等待 60 分钟或退出
```

### 调试技巧

```bash
# 启用详细日志
ralph --verbose --monitor

# 查看完整日志
cat .ralph/logs/ralph.log

# 检查会话状态
cat .ralph/.ralph_session

# 查看熔断器状态
ralph --circuit-status

# 重置所有状态
ralph --reset-session
ralph --reset-circuit
```

---

## 高级技巧

### 1. 多阶段开发

```markdown
# PROMPT.md

## 第一阶段：基础设施
- [ ] 项目结构
- [ ] 构建配置
- [ ] 测试框架

完成第一阶段后输出: `<promise>PHASE1_COMPLETE</promise>`

## 第二阶段：核心功能
- [ ] 功能 A
- [ ] 功能 B

完成第二阶段后输出: `<promise>PHASE2_COMPLETE</promise>`

## 第三阶段：优化
- [ ] 性能优化
- [ ] 文档完善

全部完成后输出: `<promise>COMPLETE</promise>`
```

### 2. 条件退出

```markdown
# fix_plan.md

## 退出条件

满足以下任一条件时退出：
1. 所有任务完成 → `<promise>COMPLETE</promise>`
2. 遇到阻塞问题 15 次迭代 → `<promise>BLOCKED</promise>`
3. 完成核心功能 → `<promise>CORE_COMPLETE</promise>`

## 阻塞报告模板

如果输出 `BLOCKED`，请包含：
- 阻塞问题描述
- 已尝试的解决方案
- 建议的替代方案
```

### 3. 自定义工作流

```bash
# 创建自定义启动脚本
cat > ralph-custom.sh << 'EOF'
#!/bin/bash
cd ~/my-project

# 导出环境变量
export NODE_ENV=development
export DEBUG=ralph:*

# 启动 Ralph
ralph --monitor --verbose --timeout 30 --calls 80
EOF

chmod +x ralph-custom.sh
./ralph-custom.sh
```

### 4. 集成 CI/CD

```yaml
# .github/workflows/ralph.yml
name: Ralph Auto-Development

on:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨 2 点

jobs:
  ralph:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Ralph
        run: |
          curl -sL https://raw.githubusercontent.com/frankbria/ralph-claude-code/main/install.sh | bash
      - name: Run Ralph
        run: |
          cd $GITHUB_WORKSPACE
          ralph-enable-ci
          ralph --max-iterations 10
```

### 5. 多项目并行

```bash
# 项目 A
cd ~/projects/project-a
ralph --monitor &

# 项目 B
cd ~/projects/project-b
ralph --monitor &

# 监控两个项目
tmux new-session -d 'cd ~/projects/project-a && ralph'
tmux split-window 'cd ~/projects/project-b && ralph'
tmux attach
```

### 6. 备份和回滚

```bash
# 启动前创建备份点
git checkout -b ralph-$(date +%Y%m%d)
git commit -am "Before Ralph"

# 启动 Ralph
ralph --monitor

# 完成后审查差异
git diff main..ralph-$(date +%Y%m%d)

# 合并或丢弃
git checkout main
git merge ralph-$(date +%Y%mdd)  # 或
git branch -D ralph-$(date +%Y%m%d)
```

---

## 参考资料

### 官方资源

- **GitHub 仓库**: https://github.com/frankbria/ralph-claude-code
- **原始技术**: https://ghuntley.com/ralph/
- **Claude Code**: https://claude.ai/code
- **Awesome Claude Code**: https://github.com/hesreallyhim/awesome-claude-code

### 社区资源

- **博客文章**: https://yuv.ai/blog/ralph-claude-code
- **Reddit 讨论**: r/ClaudeAI
- **YouTube 教程**: 搜索 "Ralph Wiggum Claude Code"

### 版本历史

- v0.11.2 - 设置权限修复
- v0.11.1 - 完成指标修复
- v0.11.0 - Ralph Enable 向导
- v0.10.1 - Bug 修复
- v0.10.0 - .ralph/ 子文件夹结构

---

## 许可证

MIT License - Copyright (c) 2025 Frank Bria

---

**有问题？** 查看 [故障排除](#故障排除) 或提交 GitHub Issue。
