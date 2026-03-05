# 双脑Ralph系统 - 项目信息

## 项目概述

**项目名称**: 双脑协同·指挥官系统 (Dual-Brain Ralph System)
**版本**: v3.0.0 (集成11大工具增强版)
**创建日期**: 2026-01-28
**最后更新**: 2026-02-11

## 项目目标

构建一个智能、高效、可自我进化的AI辅助开发系统，通过双脑协同（Brain规划 + Worker执行）实现：
- 零学习成本的自然语言任务规划
- 智能记忆检索与经验沉淀
- 自动化质量保证
- 多任务并行执行
- 可视化流程展示

## 技术栈

### 核心语言
- Python 3.8+
- Bash Shell

### 主要依赖
- jieba (中文分词)
- anthropic (Claude API)
- json, os, pathlib (标准库)

### AI模型
- Claude Sonnet 4.5 (主力模型)
- GLM-4.7 (备用模型，通过智谱API)

### 集成工具 (v3.0新增)
1. **Compound Engineering** - 复合工程方法论
2. **Superpowers** - 质量纪律框架
3. **claude-mem** - 持久化记忆系统
4. **frontend-design** - 前端审美增强
5. **draw.io MCP** - 可视化绘图
6. **Context Engineering** - 上下文管理
7. **SpecKit** - 规格驱动开发
8. **OpenClaw** - 任务调度器(可选)
9. **tmux** - 终端复用器

## 系统架构

```
双脑Ralph系统 v3.0
├─ Brain层 (规划)
│  ├─ brain.py
│  ├─ Compound Engineering集成
│  └─ SpecKit规格生成
├─ Memory层 (记忆)
│  ├─ Hippocampus (海马体)
│  └─ claude-mem (会话记忆)
├─ Dealer层 (分配)
│  ├─ dealer_enhanced.py
│  ├─ TaskRouter
│  └─ Superpowers集成
├─ Worker层 (执行)
│  ├─ Ralph (循环执行)
│  └─ 质量检查集成
└─ Tools层 (工具)
   ├─ frontend-design
   ├─ draw.io MCP
   └─ Context Engineering
```

## 核心概念

### Brain (大脑)
- 负责任务规划和Phase审查
- 使用自然语言理解需求
- 自动生成任务蓝图
- 审查每个Phase的产出质量

### Hippocampus (海马体)
- 长期记忆存储
- BM25 + TF-IDF混合检索
- 跨语言同义词映射
- 经验自动沉淀

### Dealer (分配器)
- 生成详细执行指令
- 检索历史经验
- 智能角色路由
- 上下文完整注入

### Worker/Ralph (执行者)
- 完全自动化循环执行
- 强制经验学习
- 自我验证
- 质量自检

## 工作流程

```
User (自然语言)
  ↓
Brain (理解+规划)
  ├─ 调用CE的req-dev分析需求
  ├─ 使用SpecKit生成规格
  ├─ 分解为多个Phase
  └─ 生成任务蓝图
  ↓
Dealer (生成指令)
  ├─ 检索双记忆系统(Hippocampus + claude-mem)
  ├─ 注入完整上下文
  ├─ 应用Superpowers规则
  └─ 生成详细指令
  ↓
Worker (执行)
  ├─ 循环迭代开发
  ├─ 自动触发技能(code-review, testing)
  ├─ 强制质量检查
  └─ 输出<learning>标签
  ↓
Brain (审查)
  ├─ 验证产出完整性
  ├─ 检查代码质量
  └─ 决定是否推进下一Phase
```

## 环境变量

```bash
# API配置
ZHIPU_API_KEY=your_api_key_here
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.7

# Ralph配置
CLAUDE_DISABLE_SANDBOX=1
ALLOWED_TOOLS=*
WORKING_DIRECTORY=D:\AI_Projects\system-max

# 工具配置
TOOLS_CONFIG_PATH=.ralph/tools/config.json
CONTEXT_DIR=.ralph/context
DIAGRAMS_DIR=.ralph/diagrams
MEMORIES_DIR=.ralph/memories
```

## 文件结构

```
system-max/
├─ .janus/                  # 核心系统
│  ├─ core/                 # 核心模块
│  │  ├─ hippocampus.py     # 海马体
│  │  ├─ router.py          # 任务路由
│  │  └─ thinkbank.py       # 思考库
│  ├─ config.json           # API配置
│  └─ project_state.json    # 任务蓝图
├─ .ralph/                  # Ralph系统
│  ├─ tools/                # 工具集成 (v3.0新增)
│  │  ├─ config.json        # 工具配置
│  │  ├─ tools_manager.py   # 工具管理器
│  │  └─ superpowers_rules.md
│  ├─ context/              # 上下文工程 (v3.0新增)
│  │  ├─ project-info.md
│  │  ├─ architecture.md
│  │  └─ coding-style.md
│  ├─ diagrams/             # 可视化图表 (v3.0新增)
│  ├─ memories/             # claude-mem存储 (v3.0新增)
│  ├─ specs/                # 规格文档 (v3.0新增)
│  ├─ AGENT.md              # Ralph代理配置
│  ├─ PROMPT.md             # Worker提示词
│  └─ current_instruction.txt
├─ brain.py                 # Brain模块
├─ dealer_enhanced.py       # Dealer增强版
└─ README.md                # 项目文档
```

## 关键特性

### v3.0 新特性
- ✅ 集成Compound Engineering 27个专业代理
- ✅ Superpowers质量纪律强制执行
- ✅ 双记忆系统 (Hippocampus + claude-mem)
- ✅ 前端审美自动提升 (frontend-design)
- ✅ 可视化流程图自动生成 (draw.io MCP)
- ✅ Context Engineering结构化上下文
- ✅ SpecKit规格驱动开发
- ✅ 并行执行支持 (OpenClaw + tmux)

### 核心优势
- 🎯 零学习成本（自然语言交互）
- 🧠 智能记忆（经验自动沉淀）
- ⚡ 高效执行（减少50-75%交互轮次）
- ✅ 质量保证（自动化检查）
- 📊 可视化（流程图自动生成）
- 🔄 持续进化（经验复用率80%+）

## 开发规范

### 代码规范
- Python代码遵循PEP 8
- 使用类型提示
- 文档字符串使用Google风格
- 变量命名清晰明确

### Git规范
- 提交信息使用中文
- 格式：`类型: 简短描述`
- 每个功能独立分支
- 主分支保持稳定

### 测试规范
- 单元测试覆盖率 > 80%
- 关键路径必须有集成测试
- 使用pytest框架

## 许可证

MIT License

## 联系方式

通过GitHub Issues联系
