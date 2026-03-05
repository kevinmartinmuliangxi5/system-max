# Ralph Worker 使用指南

**Ralph Worker User Guide**

版本: v3.0.0-alpha
最后更新: 2026-02-11

---

## 📖 概述

Ralph Worker 是双脑 Ralph 系统 v3.0 的自动化执行层。它实现了完整的 **Brain → Dealer → Worker** 工作流，可以自动检测、读取和执行由 Dealer 生成的任务指令。

### 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     双脑 Ralph 系统架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │    Brain    │───>│   Dealer    │───>│   Worker    │          │
│  │  任务规划层   │    │  指令生成层   │    │  自动执行层   │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│       v3.py             v3.py         ralph_loop.sh              │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                    共享数据层                              │   │
│  │  .ralph/current_instruction.txt  (当前任务指令)            │   │
│  │  .ralph/task_queue.json          (任务队列)                │   │
│  │  .ralph/logs/                    (执行日志)                │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                   工具与记忆系统                           │   │
│  │  .janus/           - 核心记忆系统                          │   │
│  │  .ralph/tools/     - 工具集成层                            │   │
│  │  .ralph/context/   - Context Engineering                   │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 安装 Worker

```bash
# 1. 进入安装目录
cd "super system/.ralph-worker"

# 2. 运行安装脚本
bash install_ralph_worker.sh
```

安装完成后，Worker 会被安装到 `~/.ralph/` 目录。

### 启动 Worker

```bash
# 直接运行
bash ~/.ralph/ralph_loop.sh

# 或者在后台运行
nohup bash ~/.ralph/ralph_loop.sh > ~/.ralph/worker.log 2>&1 &
```

---

## 🔄 Brain-Dealer-Worker 工作流

### 完整工作流程

```
用户需求
    │
    v
┌─────────────┐
│  Brain v3   │  任务规划、分解、优先级排序
└──────┬──────┘
       │ 生成任务计划
       v
┌─────────────┐
│  Dealer v3  │  生成详细执行指令
└──────┬──────┘
       │ 写入指令文件
       v
┌─────────────┐
│  Worker     │  自动检测并执行
│  ralph_loop │
└──────┬──────┘
       │
       v
   任务完成
```

### 步骤详解

#### 1. Brain - 任务规划

```bash
# 交互式模式
python brain_v3.py

# 直接输入任务
python brain_v3.py "实现用户登录功能"
```

**Brain 的职责**：
- 分析用户需求
- 将复杂任务分解为子任务
- 确定任务优先级
- 生成结构化任务计划

**输出**：
- 任务列表 (`.ralph/tasks.json`)
- 任务优先级
- 任务依赖关系

#### 2. Dealer - 指令生成

```bash
# 使用 Dealer 生成执行指令
python dealer_v3.py
```

**Dealer 的职责**：
- 读取 Brain 生成的任务计划
- 为每个任务生成详细的执行指令
- 集成 Superpowers 质量规则
- 集成 Context Engineering 上下文
- 集成 claude-mem 历史记忆

**输出**：
- 当前指令 (`.ralph/current_instruction.txt`)
- 任务上下文
- 工具配置

#### 3. Worker - 自动执行

```bash
# Worker 会自动运行，持续监控指令文件
bash ~/.ralph/ralph_loop.sh
```

**Worker 的职责**：
- 持续监控 `.ralph/current_instruction.txt`
- 检测新指令时自动执行
- 调用 Claude API 执行任务
- 记录执行日志
- 处理错误和重试
- 通知任务完成状态

---

## 📁 Worker 目录结构

```
~/.ralph/
├── ralph_loop.sh           # Worker 主循环脚本
├── .ralphrc                # Worker 配置文件
├── lib/                    # 辅助函数库
│   ├── circuit_breaker.sh      # 熔断器 - 防止 API 过载
│   ├── date_utils.sh           # 日期时间工具
│   ├── enable_core.sh          # 核心功能启用
│   ├── response_analyzer.sh    # 响应分析器
│   ├── task_sources.sh         # 任务源管理
│   ├── timeout_utils.sh        # 超时处理工具
│   └── wizard_utils.sh         # 交互向导工具
├── logs/                   # 执行日志
│   ├── worker_YYYYMMDD.log     # 每日日志
│   └── error_YYYYMMDD.log      # 错误日志
└── backup/                 # 自动备份目录
```

---

## ⚙️ 配置 Worker

### 配置文件位置

Worker 的配置文件位于 `~/.ralph/.ralphrc`

### 配置项说明

```bash
# ============================================
# Ralph Worker 配置文件
# Ralph Worker Configuration File
# ============================================

# Worker 模式设置 (Worker mode settings)
# 可选值: auto, interactive, silent
RALPH_WORKER_MODE="auto"

# API 设置 (API settings)
RALPH_API_MODEL="sonnet"           # API 模型: sonnet, haiku, opus
RALPH_API_TIMEOUT=300               # API 超时时间(秒)
RALPH_MAX_RETRIES=3                 # 最大重试次数

# 日志设置 (Logging settings)
RALPH_LOG_ENABLED=true              # 是否启用日志
RALPH_LOG_LEVEL="info"              # 日志级别: debug, info, warn, error
RALPH_LOG_DIR="$HOME/.ralph/logs"   # 日志目录

# 任务循环设置 (Task loop settings)
RALPH_LOOP_ENABLED=true             # 是否启用循环检查
RALPH_LOOP_INTERVAL=5               # 检查间隔(秒)
RALPH_IDLE_SLEEP=30                 # 空闲时休眠时间(秒)

# 任务源设置 (Task source settings)
RALPH_DEFAULT_SOURCE="dealer"       # 默认任务源: dealer, manual
RALPH_WATCH_FILES=true              # 是否监控文件变化

# 熔断器设置 (Circuit breaker settings)
RALPH_CIRCUIT_ENABLED=true          # 是否启用熔断器
RALPH_CIRCUIT_THRESHOLD=5           # 失败阈值
RALPH_CIRCUIT_TIMEOUT=60            # 熔断超时(秒)

# 通知设置 (Notification settings)
RALPH_NOTIFY_ON_COMPLETE=true       # 任务完成时通知
RALPH_NOTIFY_ON_ERROR=true          # 任务错误时通知
RALPH_NOTIFY_METHOD="console"       # 通知方式: console, desktop, email

# 高级设置 (Advanced settings)
RALPH_PARALLEL_TASKS=false          # 是否并行执行任务
RALPH_MAX_PARALLEL=3                # 最大并行数
RALPH_AUTO_BACKUP=true              # 自动备份
RALPH_BACKUP_DIR="$HOME/.ralph/backup"
```

---

## 🔧 Worker 使用模式

### 模式 1: 自动模式 (auto)

```bash
# 默认模式，自动检测和执行任务
RALPH_WORKER_MODE="auto"
bash ~/.ralph/ralph_loop.sh
```

**特点**：
- 持续监控指令文件
- 自动执行新任务
- 最小人工干预

### 模式 2: 交互模式 (interactive)

```bash
# 在执行前确认每个任务
RALPH_WORKER_MODE="interactive"
bash ~/.ralph/ralph_loop.sh
```

**特点**：
- 执行前显示任务摘要
- 等待用户确认
- 适合调试和学习

### 模式 3: 静默模式 (silent)

```bash
# 静默执行，不输出详细日志
RALPH_WORKER_MODE="silent"
bash ~/.ralph/ralph_loop.sh
```

**特点**：
- 最小输出
- 适合后台运行
- 仅记录错误

---

## 📝 任务指令格式

Worker 读取的任务指令文件格式：

```
# 任务指令文件格式
# .ralph/current_instruction.txt

========================================
任务ID: TASK-2026-0211-001
任务名称: 实现用户登录功能
优先级: 高
创建时间: 2026-02-11 16:00:00
========================================

## 📋 任务描述

实现一个完整的用户登录功能，包括：
- 用户名密码登录
- 邮箱验证
- 密码重置
- 记住登录状态

## 🎯 执行指令

1. 分析现有代码结构
2. 设计数据库模型
3. 实现后端 API
4. 实现前端界面
5. 编写单元测试
6. 集成测试

## 🛠️ 工具配置

启用的工具:
- superpowers: 质量规则检查
- claude_mem: 历史记忆检索
- speckit: 规格驱动开发

## 📚 上下文信息

项目类型: Web 应用
技术栈: Python + React
编码规范: PEP 8
架构模式: MVC

## ✅ 完成标准

- [ ] 代码通过所有测试
- [ ] 符合编码规范
- [ ] 通过安全审查
- [ ] 文档完整

========================================
任务结束标记: EOF
========================================
```

---

## 📊 日志和监控

### 日志文件位置

```
~/.ralph/logs/
├── worker_20260211.log       # 今日工作日志
├── error_20260211.log        # 错误日志
└── task_history.json         # 任务历史记录
```

### 查看实时日志

```bash
# 实时查看 Worker 日志
tail -f ~/.ralph/logs/worker_$(date +%Y%m%d).log

# 查看错误日志
tail -f ~/.ralph/logs/error_$(date +%Y%m%d).log
```

### 日志格式

```
[2026-02-11 16:00:00] [INFO] [WORKER] Worker 启动，版本 v3.0.0
[2026-02-11 16:00:05] [INFO] [TASK] 检测到新任务: TASK-2026-0211-001
[2026-02-11 16:00:06] [INFO] [TASK] 任务名称: 实现用户登录功能
[2026-02-11 16:00:07] [INFO] [EXEC] 开始执行任务...
[2026-02-11 16:05:30] [INFO] [EXEC] 任务执行完成
[2026-02-11 16:05:31] [INFO] [RESULT] 状态: 成功
```

---

## 🛡️ 熔断器机制

Worker 内置了熔断器机制，防止 API 过载：

### 工作原理

```
正常状态
    │
    │ 失败次数达到阈值
    v
打开状态 (拒绝请求)
    │
    │ 超时后进入半开状态
    v
半开状态 (允许少量请求测试)
    │
    │ 成功则关闭，失败则打开
    v
正常状态 / 打开状态
```

### 配置熔断器

```bash
# 在 .ralphrc 中配置
RALPH_CIRCUIT_ENABLED=true          # 启用熔断器
RALPH_CIRCUIT_THRESHOLD=5           # 5次失败后打开
RALPH_CIRCUIT_TIMEOUT=60            # 60秒后尝试恢复
```

---

## 🔍 故障排除

### 问题 1: Worker 无法启动

**症状**: `bash: ~/.ralph/ralph_loop.sh: No such file or directory`

**解决方案**:
```bash
# 重新安装 Worker
cd "super system/.ralph-worker"
bash install_ralph_worker.sh
```

### 问题 2: Worker 检测不到任务

**症状**: Worker 运行但不执行任务

**检查清单**:
1. 确认 Dealer 已生成指令文件
2. 检查指令文件路径: `.ralph/current_instruction.txt`
3. 检查文件权限
4. 查看日志: `tail -f ~/.ralph/logs/*.log`

### 问题 3: API 调用失败

**症状**: Worker 报告 API 错误

**解决方案**:
```bash
# 检查 API 配置
cat ~/.janus/config.json

# 检查网络连接
ping open.bigmodel.cn

# 增加超时时间
# 在 .ralphrc 中设置
RALPH_API_TIMEOUT=600
```

### 问题 4: 熔断器频繁触发

**症状**: Worker 频繁进入熔断状态

**解决方案**:
```bash
# 调整熔断器参数
RALPH_CIRCUIT_THRESHOLD=10          # 提高阈值
RALPH_CIRCUIT_TIMEOUT=120           # 延长超时

# 或临时禁用
RALPH_CIRCUIT_ENABLED=false
```

---

## 🚀 生产部署

### 使用 systemd 管理 (Linux)

创建服务文件 `/etc/systemd/system/ralph-worker.service`:

```ini
[Unit]
Description=Ralph Worker Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username
ExecStart=/home/your-username/.ralph/ralph_loop.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动和管理服务：

```bash
# 启用服务
sudo systemctl enable ralph-worker

# 启动服务
sudo systemctl start ralph-worker

# 查看状态
sudo systemctl status ralph-worker

# 查看日志
sudo journalctl -u ralph-worker -f

# 停止服务
sudo systemctl stop ralph-worker
```

### 使用 tmux/screen

```bash
# 使用 tmux
tmux new-session -d -s ralph-worker 'bash ~/.ralph/ralph_loop.sh'
tmux attach-session -t ralph-worker

# 使用 screen
screen -dmS ralph-worker bash ~/.ralph/ralph_loop.sh
screen -r ralph-worker
```

---

## 📚 高级用法

### 自定义任务源

你可以扩展 Worker 支持自定义任务源：

```bash
# 在 task_sources.sh 中添加新任务源
add_custom_source() {
    local source_name="$1"
    local source_path="$2"

    # 注册自定义任务源
    TASK_SOURCES["$source_name"]="$source_path"
}
```

### 集成 Webhook

```bash
# 启动 Webhook 服务器
bash ~/.ralph/ralph_loop.sh --webhook --port 8080

# 发送任务
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{"task": "你的任务描述"}'
```

---

## 📖 更多资源

- [DEPLOYMENT.md](DEPLOYMENT.md) - 完整部署指南
- [README.md](README.md) - 系统概述
- [QUICK_START_V3.md](../QUICK_START_V3.md) - 快速入门

---

## 📋 版本信息

- **Worker 版本**: v3.0.0-alpha
- **发布日期**: 2026-02-11
- **兼容系统**: Linux / macOS / Windows (WSL)
- **依赖**: Bash 4.0+, curl, jq

---

**祝使用愉快！** 🚀✨

如有问题，请参考故障排除章节或查看日志文件。
