# 双脑Ralph系统 v3.0 完整版 - 部署指南

**Dual-Brain Ralph System v3.0 Complete - Deployment Guide**

版本: v3.0.0-alpha
最后更新: 2026-02-11

---

## 📦 部署包内容

本部署包包含双脑Ralph系统v3.0完整版的所有核心文件：

```
super system/
├── brain_v3.py              # 增强版任务规划模块
├── dealer_v3.py             # 增强版指令生成模块
├── brain.py                 # 基础任务规划模块
├── setup.py                 # 安装脚本
├── quickstart.py            # 快速测试脚本
├── requirements.txt         # Python依赖列表
├── README.md                # 使用说明
├── DEPLOYMENT.md            # 本文档
│
├── .janus/                  # 核心记忆和路由系统
│   ├── core/                # 核心模块
│   │   ├── hippocampus.py   # 海马体记忆系统
│   │   ├── router.py        # 任务路由器
│   │   ├── router_v2.py     # 增强路由器
│   │   ├── thinkbank.py     # 思考库
│   │   └── validator.py     # 验证器
│   ├── knowledge/           # 知识库
│   ├── config.json          # 配置文件
│   └── ui_templates.py      # UI模板
│
├── .ralph/                  # 工具集成和配置
│   ├── tools/               # 工具集成层
│   │   ├── tools_manager.py        # 工具管理器
│   │   ├── memory_integrator.py    # 记忆集成器
│   │   ├── config.json             # 工具配置
│   │   ├── superpowers_rules.md    # 质量规则
│   │   └── ...                     # 其他工具文件
│   ├── context/             # Context Engineering
│   │   ├── project-info.md         # 项目信息
│   │   ├── architecture.md         # 系统架构
│   │   ├── coding-style.md         # 编码规范
│   │   └── decisions.md            # 架构决策
│   ├── PROMPT_V3.md         # Worker指令模板
│   ├── AGENT.md             # Agent配置
│   ├── diagrams/            # 流程图存储
│   ├── specs/               # 规格文档存储
│   ├── memories/            # claude-mem存储
│   └── logs/                # 日志文件
│
└── .ralph-worker/           # Ralph Worker 自动化层 (NEW!)
    ├── install_ralph_worker.sh   # Worker 安装脚本
    ├── ralph_loop.sh             # Worker 主循环脚本
    └── lib/                      # Worker 辅助函数库
        ├── circuit_breaker.sh    # 熔断器
        ├── date_utils.sh         # 日期工具
        ├── enable_core.sh        # 核心启用
        ├── response_analyzer.sh  # 响应分析器
        ├── task_sources.sh       # 任务源管理
        ├── timeout_utils.sh      # 超时工具
        └── wizard_utils.sh       # 向导工具
```

---

## 🚀 快速部署

### 1. 系统要求

- Python 3.8 或更高版本
- Bash 4.0+ (用于 Worker)
- 操作系统: Windows / Linux / macOS
- 内存: 建议 4GB 以上
- 硬盘: 至少 100MB 可用空间

### 2. 安装步骤

#### Windows系统

```powershell
# 1. 解压部署包到目标目录
# 例如: D:\AI_Projects\ralph-v3

# 2. 进入目录
cd "D:\AI_Projects\ralph-v3"

# 3. 创建虚拟环境 (推荐)
python -m venv venv

# 4. 激活虚拟环境
venv\Scripts\activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 验证安装
python .ralph\tools\tools_manager.py
```

#### Linux/macOS系统

```bash
# 1. 解压部署包到目标目录
# 例如: ~/ai-projects/ralph-v3

# 2. 进入目录
cd ~/ai-projects/ralph-v3

# 3. 创建虚拟环境 (推荐)
python3 -m venv venv

# 4. 激活虚拟环境
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 验证安装
python .ralph/tools/tools_manager.py
```

### 3. 验证安装

运行以下命令验证系统是否正确安装：

```bash
python .ralph/tools/tools_manager.py
```

**预期输出**:
```
启用的工具:
  ✓ superpowers
  ✓ claude_mem
  ✓ frontend_design
  ✓ drawio_mcp
  ✓ compound_engineering
  ✓ speckit

Brain层工具:
  - compound_engineering
  - speckit
  - drawio_mcp
```

---

## 🤖 Ralph Worker 安装

Ralph Worker 是系统的自动化执行层，可以自动循环读取和执行任务。

### 安装 Worker

#### Linux/macOS

```bash
# 进入 .ralph-worker 目录
cd .ralph-worker

# 运行安装脚本
bash install_ralph_worker.sh
```

#### Windows (Git Bash / WSL)

```bash
# 进入 .ralph-worker 目录
cd .ralph-worker

# 运行安装脚本
bash install_ralph_worker.sh
```

### 安装脚本功能

`install_ralph_worker.sh` 会自动：

1. **检测操作系统** - 识别 Linux/macOS/Windows
2. **检查依赖** - 验证必要命令是否可用
3. **备份现有文件** - 如果已安装旧版本，会自动备份
4. **创建目录** - 在 `~/.ralph/` 创建必要目录结构
5. **安装文件** - 复制 ralph_loop.sh 和 lib/ 目录
6. **设置权限** - 为脚本添加执行权限
7. **创建配置** - 生成 .ralphrc 配置文件
8. **验证安装** - 检查所有文件是否正确安装

### 手动安装 (可选)

如果自动安装脚本无法运行，可以手动安装：

```bash
# 1. 创建目录
mkdir -p ~/.ralph/lib

# 2. 复制文件
cp .ralph-worker/ralph_loop.sh ~/.ralph/
cp -r .ralph-worker/lib/* ~/.ralph/lib/

# 3. 设置执行权限
chmod +x ~/.ralph/ralph_loop.sh
chmod +x ~/.ralph/lib/*.sh

# 4. 验证
ls -la ~/.ralph/ralph_loop.sh
ls -la ~/.ralph/lib/
```

---

## ⚙️ 配置

### API配置 (可选)

编辑 `.janus/config.json` 配置Claude API：

```json
{
  "ZHIPU_API_KEY": "your_api_key_here",
  "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7"
}
```

> **注意**: API配置是可选的。不配置时系统将使用基础功能。

### 工具配置

编辑 `.ralph/tools/config.json` 定制工具行为：

```json
{
  "tools": {
    "superpowers": {
      "enabled": true,      // 设为false可关闭
      "auto_trigger": true
    },
    "claude_mem": {
      "enabled": true
    }
  }
}
```

### Worker 配置

编辑 `~/.ralph/.ralphrc` 自定义 Worker 行为：

```bash
# Worker 模式设置
RALPH_WORKER_MODE="auto"        # auto, interactive, silent

# API 设置
RALPH_API_MODEL="sonnet"        # sonnet, haiku, opus
RALPH_API_TIMEOUT=300           # 超时时间(秒)

# 日志设置
RALPH_LOG_ENABLED=true
RALPH_LOG_LEVEL="info"          # debug, info, warn, error

# 任务循环设置
RALPH_LOOP_ENABLED=true
RALPH_LOOP_INTERVAL=5           # 检查间隔(秒)
```

### Context Engineering配置

在 `.ralph/context/` 目录下维护项目上下文文档：

- `project-info.md` - 项目基本信息
- `architecture.md` - 系统架构说明
- `coding-style.md` - 编码规范
- `decisions.md` - 架构决策记录

---

## 📝 首次使用

### Brain-Dealer-Worker 工作流

系统支持完整的 Brain → Dealer → Worker 自动化工作流：

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│    Brain    │ ───> │   Dealer    │ ───> │   Worker    │
│  任务规划    │      │  指令生成    │      │  自动执行    │
└─────────────┘      └─────────────┘      └─────────────┘
     v3.py               v3.py           ralph_loop.sh
```

### 方式1: 完整自动化工作流

```bash
# 终端1: 启动 Worker (后台自动执行任务)
bash ~/.ralph/ralph_loop.sh

# 终端2: 使用 Brain 规划任务
python brain_v3.py "实现用户登录功能"

# Worker 会自动检测并执行新生成的任务
```

### 方式2: 使用Brain v3规划任务

```bash
python brain_v3.py "实现用户登录功能"
```

### 方式3: 交互式模式

```bash
python brain_v3.py
```

然后输入你的任务描述。

### 方式4: 基础模式

```bash
# 1. Brain规划
python brain.py

# 2. Dealer生成指令
python dealer_enhanced.py

# 3. 查看指令
cat .ralph/current_instruction.txt
```

---

## 📊 目录说明

### .janus/ - 核心记忆系统

| 文件/目录 | 说明 |
|-----------|------|
| core/ | 核心模块(海马体、路由器等) |
| knowledge/ | 知识库存储 |
| config.json | 系统配置 |
| thinking/ | 思考记录存储 |

### .ralph/ - 工具集成层

| 文件/目录 | 说明 |
|-----------|------|
| tools/ | 工具集成代码 |
| context/ | Context Engineering文档 |
| diagrams/ | 流程图存储 |
| specs/ | 规格文档存储 |
| memories/ | claude-mem记忆存储 |
| logs/ | 系统日志 |

### ~/.ralph/ - Worker 安装目录

| 文件/目录 | 说明 |
|-----------|------|
| ralph_loop.sh | Worker 主循环脚本 |
| lib/ | Worker 辅助函数库 |
| .ralphrc | Worker 配置文件 |

---

## 🔧 故障排除

### 问题1: ImportError

**症状**: `ImportError: No module named 'xxx'`

**解决**:
```bash
# 确保依赖已安装
pip install -r requirements.txt

# 或单独安装缺失的模块
pip install jieba anthropic
```

### 问题2: 权限错误

**症状**: `Permission denied`

**解决**:
```bash
# Linux/macOS: 添加执行权限
chmod +x brain_v3.py
chmod +x dealer_v3.py
chmod +x ~/.ralph/ralph_loop.sh
```

### 问题3: 中文显示乱码

**症状**: 终端中文显示为乱码

**解决**:
```bash
# Windows: 设置终端编码为UTF-8
chcp 65001

# 或在PowerShell中:
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### 问题4: 工具无法加载

**症状**: 提示"无法导入v3.0工具"

**解决**:
这是正常的降级行为。系统会自动使用基础功能。

### 问题5: Worker 无法启动

**症状**: `bash: ~/.ralph/ralph_loop.sh: No such file or directory`

**解决**:
```bash
# 重新运行安装脚本
cd "super system/.ralph-worker"
bash install_ralph_worker.sh

# 或手动安装
mkdir -p ~/.ralph/lib
cp .ralph-worker/ralph_loop.sh ~/.ralph/
cp -r .ralph-worker/lib/* ~/.ralph/lib/
chmod +x ~/.ralph/ralph_loop.sh
```

---

## 🚀 生产部署建议

### 1. 使用虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 2. 固定依赖版本

```bash
pip freeze > requirements-lock.txt
```

### 3. 日志管理

日志文件默认存储在 `.ralph/logs/` 目录，建议：

- 定期清理旧日志
- 设置日志轮转策略
- 监控日志文件大小

### 4. 备份重要数据

定期备份以下目录：

- `.janus/knowledge/` - 海马体知识库
- `.ralph/memories/` - claude-mem记忆
- `.janus/thinking/` - 思考记录
- `~/.ralph/` - Worker 配置和脚本

### 5. 安全建议

- 不要将包含API密钥的`config.json`提交到版本控制
- 使用环境变量存储敏感信息
- 定期更新依赖包

### 6. Worker 生产部署

```bash
# 使用 systemd 管理 Worker (Linux)
sudo cp scripts/ralph-worker.service /etc/systemd/system/
sudo systemctl enable ralph-worker
sudo systemctl start ralph-worker

# 或使用 screen/tmux 保持运行
screen -S ralph-worker
bash ~/.ralph/ralph_loop.sh
# Ctrl+A, D 分离会话
```

---

## 📚 更多文档

- [README.md](README.md) - 系统使用说明
- [WORKER.md](WORKER.md) - Worker 详细使用指南
- [QUICK_START_V3.md](../QUICK_START_V3.md) - 快速上手指南
- [INTEGRATION_STATUS_V3.md](../INTEGRATION_STATUS_V3.md) - 集成状态报告

---

## 🆘 获取帮助

### 文档资源

- 查看项目文档了解更多信息
- 检查 `.ralph/context/architecture.md` 了解系统架构
- 查看 WORKER.md 了解 Worker 详细用法

### 报告问题

如遇到问题，请提供：

1. Python版本: `python --version`
2. 操作系统版本
3. Bash版本: `bash --version`
4. 错误信息完整输出
5. 复现步骤

---

## 📋 版本信息

- **版本**: v3.0.0-alpha
- **发布日期**: 2026-02-11
- **打包内容**: 核心功能完整版 + Worker 自动化层
- **排除内容**:
  - `.git/` - 版本控制目录
  - `__pycache__/` - Python缓存
  - 个人数据和会话记录

---

## ✅ 部署检查清单

部署完成后，请检查以下项目：

### 基础系统
- [ ] Python版本 >= 3.8
- [ ] 所有依赖已安装 (`pip list`)
- [ ] 工具管理器运行正常
- [ ] Brain v3可以正常启动
- [ ] 配置文件已根据需要修改
- [ ] 终端中文显示正常
- [ ] 虚拟环境已创建(可选但推荐)

### Worker 系统
- [ ] ~/.ralph/ralph_loop.sh 已安装
- [ ] ~/.ralph/lib/ 目录完整
- [ ] ~/.ralph/.ralphrc 配置文件存在
- [ ] Worker 可以正常启动
- [ ] Worker 能够检测 Dealer 生成的任务

---

**祝部署顺利！** 🚀✨

如有任何问题，请参考文档或联系技术支持。
