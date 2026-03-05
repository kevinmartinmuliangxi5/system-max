# 双脑Ralph系统 v3.0 完整版 - 打包清单

**Dual-Brain Ralph System v3.0 Complete - Package Manifest**

版本: v3.0.0-alpha
打包日期: 2026-02-11

---

## 📦 打包内容

### 核心Python模块 (根目录)

| 文件 | 说明 |
|------|------|
| `brain_v3.py` | 增强版任务规划模块 (v3.0核心) |
| `dealer_v3.py` | 增强版指令生成模块 (v3.0核心) |
| `brain.py` | 基础任务规划模块 (v2.x兼容) |
| `dealer_enhanced.py` | 增强指令生成器 (v2.x兼容) |
| `setup.py` | 安装脚本 |
| `quickstart.py` | 快速测试脚本 |
| `quick_test.sh` | 快速测试Shell脚本 |

### 文档文件 (根目录)

| 文件 | 说明 |
|------|------|
| `README.md` | 系统使用说明 |
| `DEPLOYMENT.md` | 部署指南 |
| `requirements.txt` | Python依赖列表 |
| `QUICK_START_V3.md` | v3.0快速上手指南 |
| `README_V3.md` | v3.0详细说明 |
| `INTEGRATION_COMPLETE_SUMMARY.md` | 集成完成摘要 |

### .janus/ 目录 - 核心记忆系统

```
.janus/
├── core/                    # 核心模块
│   ├── __init__.py
│   ├── cache_manager.py     # 缓存管理器
│   ├── hippocampus.py       # 海马体记忆系统 (BM25+TF-IDF)
│   ├── router.py            # 基础任务路由器
│   ├── router_v2.py         # 增强任务路由器
│   ├── thinkbank.py         # 思考库
│   └── validator.py         # 验证器
├── knowledge/               # 知识库
│   ├── index.json           # 知识索引
│   ├── python_web.json      # Python Web开发知识
│   ├── react.json           # React框架知识
│   ├── security.json        # 安全知识
│   └── streamlit.json       # Streamlit框架知识
├── config.json              # 系统配置文件
└── ui_templates.py          # UI模板
```

### .ralph/ 目录 - 工具集成层

```
.ralph/
├── tools/                   # 工具集成代码
│   ├── tools_manager.py     # 工具管理器 (v3.0核心)
│   ├── memory_integrator.py # 记忆集成器 (双记忆系统)
│   ├── claude_mem_enhanced.py    # claude-mem增强版
│   ├── drawio_mcp_client.py      # draw.io MCP客户端
│   ├── session_hooks.py          # 会话钩子
│   ├── parallel_brain.py         # 并行Brain
│   ├── parallel_executor.py      # 并行执行器
│   ├── config.json               # 工具配置文件
│   ├── superpowers_rules.md      # Superpowers质量规则
│   ├── openclaw_config.json      # OpenClaw配置
│   ├── test_dealer_v3.py         # Dealer v3测试
│   └── test_phase3.py            # Phase 3测试
├── context/                 # Context Engineering文档
│   ├── project-info.md     # 项目信息
│   ├── architecture.md     # 系统架构
│   ├── coding-style.md     # 编码规范
│   ├── decisions.md        # 架构决策记录
│   ├── dependencies.md     # 依赖说明
│   └── modules/            # 模块文档
│       ├── brain.md        # Brain模块说明
│       ├── dealer.md       # Dealer模块说明
│       └── worker.md       # Worker模块说明
├── PROMPT_V3.md            # Worker指令模板 (v3.0)
├── AGENT.md                # Agent配置
├── diagrams/               # 流程图存储目录 (空)
├── specs/                  # 规格文档存储目录 (空)
├── memories/               # claude-mem存储目录 (空)
└── logs/                   # 日志存储目录 (空)
```

### .ralph-worker/ 目录 - Worker 自动化层 (v3.1 新增)

```
.ralph-worker/
├── ralph_loop.sh           # Worker 主循环脚本 (1742 行)
├── install_ralph_worker.sh # Worker 安装脚本 (347 行)
├── verify_install.sh        # 安装验证脚本
├── verify_worker_package.sh # 包完整性验证脚本
└── lib/                      # Worker 辅助函数库
    ├── circuit_breaker.sh    # 熔断器 (393 行)
    ├── response_analyzer.sh  # 响应分析器 (880 行)
    ├── date_utils.sh         # 日期工具 (53 行)
    ├── timeout_utils.sh      # 超时工具 (145 行)
    ├── task_sources.sh       # 任务源管理 (577 行)
    ├── enable_core.sh        # 核心启用 (815 行)
    └── wizard_utils.sh       # 向导工具 (547 行)
```

---

## ✅ 已包含内容

### 核心 Brain-Dealer-Worker 三层架构
- ✅ **Brain 层** (brain_v3.py, brain.py) - 任务规划与分解
- ✅ **Dealer 层** (dealer_v3.py, dealer_enhanced.py) - 指令生成
- ✅ **Worker 层** (.ralph-worker/) - 自动化执行 (v3.1 新增)

### 记忆与工具系统
- ✅ .janus/ 核心记忆系统 (Hippocampus + Router + ThinkBank)
- ✅ .ralph/ 工具集成层 (Tools Manager + Memory Integrator)
- ✅ .ralph/ Context Engineering 文档 (项目上下文管理)
- ✅ ~/.ralph/ Worker 全局安装目录 (通过 install_ralph_worker.sh)

### 文档与配置
- ✅ WORKER.md - Worker 详细使用指南 (新增)
- ✅ DEPLOYMENT.md - 完整部署指南 (含 Worker 安装)
- ✅ README.md, README_V3.md - 系统说明
- ✅ QUICK_START_V3.md - 快速上手指南
- ✅ requirements.txt - Python 依赖
- ✅ verify_worker_package.sh - 包完整性验证脚本 (新增)

---

## ❌ 已排除内容

- ❌ .git/ - 版本控制目录
- ❌ __pycache__/ - Python缓存目录
- ❌ *.pyc - 编译的Python文件
- ❌ 个人会话数据
- ❌ 实时日志文件
- ❌ 临时文件

---

## 📋 文件统计

| 类别 | 数量 |
|------|------|
| Python文件 (.py) | 21 |
| 配置文件 (.json) | 10 |
| 文档文件 (.md) | 15 |
| Shell脚本 (.sh) | 12 |
| 总文件数 | 58+ |

### Worker 层文件统计
| 类别 | 数量 | 总行数 |
|------|------|--------|
| Worker 主脚本 | 1 | 1,742 |
| 安装脚本 | 2 | 400+ |
| lib/ 函数库 | 7 | 3,410 |
| **Worker 层合计** | **10** | **5,550+** |

---

## 🚀 快速开始

### 1. 安装系统依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 安装 Worker 层 (新增)

```bash
# 进入 Worker 安装目录
cd .ralph-worker

# 运行安装脚本
bash install_ralph_worker.sh

# 验证安装
bash verify_install.sh
```

### 3. 验证安装

```bash
# 验证工具管理器
python .ralph/tools/tools_manager.py

# 验证包完整性
bash verify_worker_package.sh
```

### 4. 完整工作流使用

```bash
# 终端1: 启动 Worker (后台自动执行)
bash ~/.ralph/ralph_loop.sh

# 终端2: Brain 规划任务
python brain_v3.py "实现用户登录功能"

# 终端3: Dealer 生成指令 (可选，Worker 会自动调用)
python dealer_v3.py

# Worker 会自动检测并执行新生成的任务
```

---

## 📚 更多信息

- 查看 [README.md](README.md) 了解系统使用
- 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 了解部署步骤
- 查看 [QUICK_START_V3.md](QUICK_START_V3.md) 快速上手

---

## 📝 注意事项

1. **依赖安装**: 运行前请先安装 `requirements.txt` 中的依赖
2. **Python版本**: 需要 Python 3.8 或更高版本
3. **配置可选**: API配置是可选的，不配置可使用基础功能
4. **目录结构**: 请保持目录结构完整，不要移动文件

---

## 🆘 获取帮助

如遇问题，请查看:
1. [DEPLOYMENT.md](DEPLOYMENT.md) - 部署和故障排除
2. [README.md](README.md) - 系统使用说明

---

**打包完成日期**: 2026-02-11
**版本**: v3.0.0-alpha
**状态**: ✅ 完整打包
