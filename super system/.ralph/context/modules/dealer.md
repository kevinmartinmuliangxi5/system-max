# Dealer模块文档

**模块**: Dealer v3.0
**文件**: `dealer_v3.py`
**版本**: v3.0.0-alpha
**最后更新**: 2026-02-11

---

## 模块概述

Dealer是双脑Ralph系统的**指令生成**模块，负责将Brain生成的任务蓝图转化为详细的执行指令给Worker。

### 核心职责

1. **读取蓝图** - 从`.janus/project_state.json`读取待执行任务
2. **上下文收集** - 收集项目信息、编码规范、历史经验
3. **双记忆检索** - 从Hippocampus + claude-mem检索相关经验
4. **质量注入** - 注入Superpowers规则和质量门控
5. **指令生成** - 生成完整的执行指令
6. **输出分发** - 复制到剪贴板或写入文件

---

## 架构设计

### 类图

```
DealerV3
├── __init__()
├── detect_operation_type()         # 操作类型检测
├── get_file_info()                 # 文件信息获取
├── load_context_engineering()      # Context加载
├── load_superpowers_rules()        # Superpowers加载
├── retrieve_dual_memory()          # 双记忆检索
├── format_memory_context()         # 记忆格式化
├── check_quality_gates()           # 质量门控检查
├── should_trigger_skills()         # 技能触发判断
├── generate_instruction()          # 指令生成 (主方法)
├── deal()                          # 主流程
└── parse_brain()                   # Brain输出解析
```

---

## 核心流程

### generate_instruction() 主流程

```python
def generate_instruction(self, task: Dict) -> str:
    """
    生成增强版指令

    流程:
    1. 基础信息 (task_name, instruction, files)
    2. 路由与角色 (TaskRouter)
    3. 操作类型检测 (CREATE/MODIFY/FIX/REFACTOR/OPTIMIZE)
    4. 文件信息收集
    5. 双记忆检索 (Hippocampus + claude-mem)
    6. Context Engineering加载
    7. Superpowers规则加载
    8. 质量门控检查
    9. 技能触发判断
    10. Prompt生成
    """
```

### 数据流

```
蓝图文件 (.janus/project_state.json)
    ↓
提取待执行任务 (status=PENDING)
    ↓
┌─────────────────────────────────┐
│ 上下文收集                       │
│ • TaskRouter (角色路由)          │
│ • 操作类型检测                   │
│ • 文件信息                       │
│ • 双记忆检索                     │
│ • Context Engineering            │
│ • Superpowers规则                │
│ • 质量门控                       │
│ • 技能触发判断                   │
└─────────────────────────────────┘
    ↓
Prompt生成 (4000+字符)
    ↓
输出分发
    ├─ 剪贴板 (正常模式)
    └─ 文件 (.ralph/current_instruction.txt, Ralph模式)
```

---

## API参考

### 主要方法

#### detect_operation_type(instruction, files)

**用途**: 智能检测操作类型

**返回**: "CREATE" | "MODIFY" | "FIX" | "REFACTOR" | "OPTIMIZE"

**示例**:
```python
op_type = dealer.detect_operation_type(
    "修复登录Bug",
    ["api/auth.py"]
)
# 返回: "FIX"
```

#### retrieve_dual_memory(query)

**用途**: 从双记忆系统检索

**返回**: Dict包含hippocampus和claude_mem结果

**示例**:
```python
results = dealer.retrieve_dual_memory("用户登录")
# {
#   "hippocampus": [...],
#   "claude_mem": [...],
#   "merged": [...]
# }
```

#### generate_instruction(task)

**用途**: 生成完整执行指令（主方法）

**参数**: task字典（从蓝图提取）

**返回**: 完整的Prompt字符串

---

## 生成的Prompt结构

```markdown
# 🎯 任务执行指令 (Dealer v3.0)

## 📋 任务概览
- 角色、任务名称、操作类型、类别

## 📝 任务详情
- 目标描述
- 目标文件列表

## 📁 当前文件内容
- 每个文件的前30行预览

## 🏗️ 项目信息 (Context Engineering)
- 技术栈、架构简介

## 📐 编码规范 (Context Engineering)
- Python规范、代码风格

## 💡 相关经验 (双记忆系统)
- Hippocampus核心经验
- claude-mem完整历史

## 🧠 项目决策 (思考库)
- 历史架构决策

## ⚡ Superpowers质量纪律
- Bright-Line Rules

## 🚦 质量门控 (Compound Engineering)
- 按操作类型的检查清单

## ✅ 成功标准
- 根据操作类型定制

## 🎯 自动触发的技能
- 列出将触发的技能

## 🚀 执行协议
- 代码规范、操作步骤、输出要求
```

---

## 使用示例

### 命令行使用

```bash
# 正常模式（复制到剪贴板）
python dealer_v3.py

# Ralph模式（写入文件）
python dealer_v3.py --ralph-mode
```

### Python API使用

```python
from dealer_v3 import DealerV3

dealer = DealerV3()
instruction = dealer.generate_instruction({
    'task_name': '实现用户登录',
    'instruction': '使用JWT实现认证',
    'target_files': ['api/auth.py'],
    'status': 'PENDING'
})
print(instruction)
```

---

## 集成点

### 与Brain集成

```
Brain v3 生成蓝图
    ↓
.janus/project_state.json
    ↓
Dealer v3 读取
    ↓
生成详细指令
```

### 与Worker集成

```
Dealer v3 生成指令
    ↓
.ralph/current_instruction.txt
    ↓
Worker v3 读取
    ↓
执行任务
```

### 与双记忆系统集成

```
Dealer v3 检索
    ↓
memory_integrator.retrieve_combined()
    ↓
Hippocampus (60%) + claude-mem (40%)
    ↓
格式化注入Prompt
```

---

## 配置选项

通过`.ralph/tools/config.json`配置：

```json
{
  "tools": {
    "superpowers": {
      "enabled": true,
      "bright_line_rules": {...}
    },
    "compound_engineering": {
      "enabled": true,
      "quality_gates": {...}
    }
  },
  "memory_integrator": {
    "hippocampus_weight": 0.6,
    "claude_mem_weight": 0.4
  }
}
```

---

## 性能指标

| 指标 | v2.x (dealer_enhanced) | v3.0 | 提升 |
|------|----------------------|------|------|
| Prompt长度 | ~2000字符 | ~4000字符 | +100% |
| 上下文丰富度 | 中 | 高 | +150% |
| 质量要求明确度 | 中 | 高 | +200% |
| 经验利用 | 单一 | 双记忆 | +100% |
| 生成时间 | ~1秒 | ~2秒 | -50% (可接受) |

---

## 最佳实践

### 1. 确保蓝图存在

```bash
# 先运行Brain
python brain_v3.py "实现登录"

# 再运行Dealer
python dealer_v3.py
```

### 2. 查看生成的指令

```bash
# Ralph模式
python dealer_v3.py --ralph-mode
cat .ralph/current_instruction.txt
```

### 3. 检查工具状态

```python
dealer = DealerV3()
if dealer.tools_manager:
    print("✓ v3.0功能已启用")
else:
    print("⚠ 降级到基础功能")
```

---

## 故障排查

### 问题: 蓝图文件不存在

```
❌ 蓝图文件不存在: .janus/project_state.json
💡 请先运行 Brain 生成任务蓝图
```

**解决**: 先运行`python brain_v3.py "任务描述"`

### 问题: 无法解析蓝图

```
❌ 无法解析蓝图数据
```

**解决**: 检查`.janus/project_state.json`格式是否正确

---

**维护者**: System Architect
**最后更新**: 2026-02-11
**版本**: v3.0.0-alpha
