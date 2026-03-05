# v2.x → v3.0 升级指南

**从v2.x平滑升级到v3.0**

---

## 📋 升级概述

本指南帮助你从v2.x (Brain Module Edition) 升级到v3.0 (Production Release)。

### 核心变化

| 模块 | v2.x | v3.0 | 变化 |
|------|------|------|------|
| **Brain** | brain.py | brain_v3.py | 全新重写 |
| **Dealer** | dealer_enhanced.py | dealer_v3.py | 全新重写 |
| **Worker** | 无 | PROMPT_V3.md | 新增 |
| **记忆** | Hippocampus | 双记忆系统 | 架构升级 |
| **配置** | .janus/config.json | .ralph/tools/config.json | 新增工具配置 |
| **文档** | 基础 | Context Engineering | 体系化 |

---

## 🔍 兼容性检查

### 1. 检查当前版本

```bash
# 检查是否有v2.x文件
ls brain.py dealer.py dealer_enhanced.py 2>/dev/null

# 检查.janus目录
ls .janus/project_state.json 2>/dev/null
```

### 2. 备份现有数据

```bash
# 备份蓝图文件
cp .janus/project_state.json .janus/project_state.json.v2x.bak

# 备份记忆数据
cp .janus/long_term_memory.json .janus/long_term_memory.json.bak

# 备份配置
cp .janus/config.json .janus/config.json.bak
```

---

## 🚀 升级步骤

### Step 1: 安装新依赖

v3.0需要额外的依赖:

```bash
# 核心依赖（必需）
pip install pyperclip

# 推荐依赖
pip install colorama

# 可选依赖
pip install jieba pytest flake8
```

**验证安装**:
```bash
python .ralph/scripts/check_dependencies.py
```

### Step 2: 理解新目录结构

v3.0新增目录:

```
新增目录:
.ralph/
├─ tools/                    # 🆕 工具集成层
│  ├─ config.json
│  ├─ tools_manager.py
│  ├─ memory_integrator.py
│  ├─ claude_mem_enhanced.py
│  └─ superpowers_rules.md
├─ context/                  # 🆕 Context Engineering
│  ├─ project-info.md
│  ├─ architecture.md
│  ├─ coding-style.md
│  ├─ decisions.md           # 🆕 10个ADR
│  ├─ dependencies.md        # 🆕 依赖管理
│  └─ modules/               # 🆕 模块文档
│      ├─ brain.md
│      ├─ dealer.md
│      └─ worker.md
├─ diagrams/                 # 🆕 可视化图表
├─ memories/                 # 🆕 claude-mem存储
├─ specs/                    # 🆕 规格文档
└─ scripts/                  # 🆕 工具脚本
   ├─ check_dependencies.py
   └─ integration_test.py

保持不变:
.janus/
├─ core/                     # 核心模块（不变）
│  ├─ hippocampus.py
│  ├─ router.py
│  ├─ thinkbank.py
│  └─ cache_manager.py
├─ project_state.json        # 蓝图文件（格式兼容）
└─ long_term_memory.json     # Hippocampus记忆（兼容）
```

### Step 3: 更新Brain使用方式

**v2.x方式**:
```bash
# 旧方式
python brain.py "实现用户登录"
```

**v3.0方式**:
```bash
# 新方式
python brain_v3.py "实现用户登录"

# 生成文件:
# • .janus/project_state.json (蓝图 - 格式兼容)
# • .ralph/specs/[任务名].md (规格 - 新增)
# • .ralph/diagrams/task-flow.txt (流程图 - 新增)
```

**兼容性**: v3.0的蓝图格式**完全兼容**v2.x，你可以继续使用旧蓝图。

### Step 4: 更新Dealer使用方式

**v2.x方式**:
```bash
# 旧方式
python dealer_enhanced.py
```

**v3.0方式**:
```bash
# 新方式
python dealer_v3.py

# 如果你有旧蓝图，v3.0可以直接读取
```

**新增功能**:
- ✅ 双记忆系统集成
- ✅ Context Engineering上下文
- ✅ Superpowers质量纪律
- ✅ 质量门控清单
- ✅ 技能触发提示

### Step 5: 更新Worker提示词

**v2.x方式**:
```
# 直接粘贴Dealer生成的指令给Claude Code
```

**v3.0方式**:
```
# 同样粘贴，但Worker现在会:
# 1. 严格遵守Superpowers Bright-Line Rules
# 2. 完整实现所有功能（无代码省略）
# 3. 编写完整测试
# 4. 系统化质量自检
# 5. 输出learning标签
# 6. 输出完成信号 <promise>COMPLETE</promise>
```

**参考文档**: `.ralph/PROMPT_V3.md`

---

## 📝 配置迁移

### 1. 基础配置（保持不变）

`.janus/config.json` 保持不变:
```json
{
  "ZHIPU_API_KEY": "your_key_here",
  "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7"
}
```

### 2. 新增工具配置

创建 `.ralph/tools/config.json`（如果不存在，系统会使用默认值）:

```json
{
  "tools": {
    "superpowers": {
      "enabled": true,
      "auto_trigger": true,
      "bright_line_rules": {
        "no_code_omission": true,
        "must_write_tests": true,
        "must_prepare_review": true,
        "no_placeholders": true,
        "must_handle_errors": true,
        "must_document": true
      }
    },
    "claude_mem": {
      "enabled": true,
      "compression": {
        "enabled": true,
        "min_score": 0.3
      }
    },
    "compound_engineering": {
      "enabled": true,
      "quality_gates": {
        "CREATE": ["requirements_clear", "spec_complete", "code_complete", "tests_pass"],
        "MODIFY": ["code_complete", "tests_pass", "no_regression"],
        "FIX": ["bug_identified", "root_cause", "code_complete", "tests_pass"],
        "REFACTOR": ["code_reviewed", "no_security_issues", "functionality_preserved", "tests_pass"],
        "OPTIMIZE": ["baseline_measured", "optimization_verified", "tests_pass"]
      }
    },
    "speckit": {
      "enabled": true
    },
    "frontend_design": {
      "enabled": true
    },
    "drawio_mcp": {
      "enabled": true
    }
  },
  "memory_integrator": {
    "hippocampus_weight": 0.6,
    "claude_mem_weight": 0.4,
    "merge_strategy": "weighted",
    "deduplication": true
  }
}
```

---

## 🔄 数据迁移

### 1. 蓝图格式（无需迁移）

v3.0**完全兼容**v2.x的蓝图格式:

```json
{
  "blueprint": [
    {
      "task_name": "实现用户登录",
      "instruction": "...",
      "target_files": ["auth.py"],
      "status": "PENDING"
    }
  ]
}
```

**无需修改**，v3.0可以直接读取。

### 2. Hippocampus记忆（无需迁移）

`.janus/long_term_memory.json` 格式不变，v3.0继续使用。

### 3. claude-mem数据（新系统）

v3.0新增claude-mem，会自动创建 `.ralph/memories/` 目录存储。

**首次运行**: claude-mem为空，会逐步积累经验。

---

## ✅ 验证升级

### 1. 运行依赖检查

```bash
python .ralph/scripts/check_dependencies.py
```

**预期输出**:
```
核心依赖:
✓ json
✓ pathlib
✓ re
✓ pyperclip

✓ 核心依赖满足，系统可以运行
```

### 2. 运行集成测试

```bash
python .ralph/scripts/integration_test.py
```

**预期输出**:
```
总测试数: 7
通过: 7 ✅
失败: 0 ❌
通过率: 100.0%

🎉 所有测试通过！系统集成完整，可以投入使用！
```

### 3. 测试Brain v3

```bash
python brain_v3.py "测试升级功能"
```

**预期**: 生成蓝图、规格文档、流程图。

### 4. 测试Dealer v3

```bash
python dealer_v3.py
```

**预期**: 读取蓝图，生成增强版指令。

---

## 🆚 功能对比

### Brain对比

| 功能 | v2.x (brain.py) | v3.0 (brain_v3.py) |
|------|-----------------|-------------------|
| 任务分解 | ✅ | ✅ |
| 需求分析 | ❌ | ✅ CE req-dev |
| 规格生成 | ❌ | ✅ SpecKit |
| 流程图 | ❌ | ✅ draw.io |
| 经验检索 | Hippocampus单一 | 双记忆系统 |
| 输出文件 | 1个 (蓝图) | 3个 (蓝图+规格+流程图) |

### Dealer对比

| 功能 | v2.x (dealer_enhanced.py) | v3.0 (dealer_v3.py) |
|------|--------------------------|---------------------|
| 任务提取 | ✅ | ✅ |
| 文件内容 | ✅ | ✅ |
| 操作类型 | ✅ | ✅ 更智能 |
| 经验检索 | Hippocampus单一 | 双记忆系统 |
| Context | 基础 | Context Engineering |
| 质量规则 | ❌ | ✅ Superpowers |
| 质量门控 | ❌ | ✅ CE质量门控 |
| 技能触发 | ❌ | ✅ 智能提示 |
| Prompt长度 | ~2000字符 | ~4000字符 |

### Worker对比

| 功能 | v2.x (无文档) | v3.0 (PROMPT_V3.md) |
|------|--------------|---------------------|
| 质量纪律 | 无明确规则 | Superpowers 6条规则 |
| 代码完整性 | 80% | 100% |
| 测试要求 | 建议 | 强制 |
| 质量自检 | 无 | 系统化报告 |
| 学习标签 | 简单 | 6字段扩展 |
| 完成信号 | 无 | `<promise>COMPLETE</promise>` |

---

## 🎯 升级检查清单

### 必做项

- [ ] 备份 `.janus/project_state.json`
- [ ] 备份 `.janus/long_term_memory.json`
- [ ] 运行 `python .ralph/scripts/check_dependencies.py`
- [ ] 运行 `python .ralph/scripts/integration_test.py`
- [ ] 测试 `python brain_v3.py "测试任务"`
- [ ] 测试 `python dealer_v3.py`
- [ ] 查看 `.ralph/context/` 下的Context文档
- [ ] 查看 `.ralph/PROMPT_V3.md` 理解Worker v3

### 推荐项

- [ ] 阅读 `README.md` v3.0完整说明
- [ ] 阅读 `.ralph/context/decisions.md` 理解设计决策
- [ ] 阅读 `.ralph/context/modules/brain.md` 详细了解Brain
- [ ] 阅读 `.ralph/context/modules/dealer.md` 详细了解Dealer
- [ ] 阅读 `.ralph/context/modules/worker.md` 详细了解Worker
- [ ] 配置 `.ralph/tools/config.json` 定制工具

### 可选项

- [ ] 安装可选依赖 `pip install jieba pytest flake8`
- [ ] 更新Context Engineering文档（根据你的项目）
- [ ] 扩展Superpowers规则（如有需要）
- [ ] 调整双记忆权重（默认60/40）

---

## 🐛 常见升级问题

### 问题1: ImportError - 找不到模块

**症状**:
```
ImportError: No module named 'tools_manager'
```

**原因**: 新增模块未找到。

**解决**:
```bash
# 确认目录结构
ls .ralph/tools/tools_manager.py

# 如果文件不存在，说明升级不完整
# 重新从v3.0完整包复制 .ralph/ 目录
```

### 问题2: 蓝图无法读取

**症状**:
```
❌ 蓝图文件不存在: .janus/project_state.json
```

**原因**: 未运行Brain生成蓝图。

**解决**:
```bash
# 先运行Brain
python brain_v3.py "你的任务"

# 再运行Dealer
python dealer_v3.py
```

### 问题3: 测试失败

**症状**:
```
❌ Brain v3功能 - 测试失败
```

**原因**: 可能是依赖问题或模块缺失。

**解决**:
```bash
# 详细查看错误
python .ralph/scripts/integration_test.py 2>&1 | tee test.log

# 检查特定模块
python -c "from brain_v3 import BrainV3; print('Brain OK')"
python -c "from dealer_v3 import DealerV3; print('Dealer OK')"
```

### 问题4: Worker不遵守质量规则

**症状**: Worker仍然省略代码、不写测试。

**原因**: 未使用v3.0指令模板。

**解决**:
```bash
# 确保使用Dealer v3生成指令
python dealer_v3.py

# Worker会自动接收Superpowers规则
# 或者直接查看 .ralph/PROMPT_V3.md 理解完整规则
```

### 问题5: 双记忆系统不工作

**症状**: 检索不到任何经验。

**原因**: 首次运行，claude-mem为空。

**解决**:
- Hippocampus会从 `.janus/long_term_memory.json` 读取v2.x数据（兼容）
- claude-mem需要逐步积累，每次Worker完成任务都会记录
- 可以查看 `.ralph/memories/` 目录验证

---

## 📚 延伸阅读

### 必读文档

1. **README.md** - v3.0完整功能介绍
2. **QUICK_START_V3.md** - 快速上手指南
3. **.ralph/context/architecture.md** - 系统架构详解
4. **.ralph/context/decisions.md** - 10个ADR设计决策

### 模块文档

1. **.ralph/context/modules/brain.md** - Brain v3详解
2. **.ralph/context/modules/dealer.md** - Dealer v3详解
3. **.ralph/context/modules/worker.md** - Worker v3详解

### 参考资料

1. **.ralph/context/dependencies.md** - 完整依赖说明
2. **PHASE5_COMPLETION.md** - Worker v3实现报告
3. **PHASE8_COMPLETION.md** - Context Engineering报告
4. **PHASE10_COMPLETION.md** - 文档更新报告

---

## 🎉 升级完成

恭喜！你已经成功升级到v3.0。

### 主要收获

- ✅ Brain v3 - CE需求分析 + SpecKit规格
- ✅ Dealer v3 - 双记忆 + 质量门控
- ✅ Worker v3 - Superpowers质量纪律
- ✅ Context Engineering - 完整文档体系
- ✅ 100%测试通过 - 生产就绪

### 下一步

1. 使用Brain v3规划一个实际任务
2. 使用Dealer v3生成增强指令
3. 体验Worker v3的质量自检
4. 查看生成的规格文档和流程图
5. 感受代码完整性的提升

---

**版本**: v3.0.0
**最后更新**: 2026-02-11

🚀 **享受更智能、更高质量的AI开发体验！**
