# 双脑Ralph系统 v3.0 快速上手指南

**5分钟了解并开始使用v3.0的新功能**

---

## 🎯 v3.0核心亮点

```
双脑Ralph v3.0 = 原有系统 + 11大工具集成

新增能力:
✅ 智能需求分析 (Compound Engineering)
✅ 规格驱动开发 (SpecKit)
✅ 双记忆系统 (Hippocampus + claude-mem)
✅ 质量自动保证 (Superpowers)
✅ 前端审美提升 (frontend-design)
✅ 流程可视化 (draw.io MCP)
✅ 结构化上下文 (Context Engineering)
```

---

## 📦 1分钟快速验证

### 检查集成状态
```bash
# 进入项目目录
cd D:\AI_Projects\system-max

# 测试工具管理器
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

如果看到这个输出，说明基础集成成功！✅

---

## 🚀 2分钟体验新功能

### 使用Brain v3规划任务

```bash
python brain_v3.py "实现用户登录功能"
```

**新增功能展示**:

1. **Compound Engineering分析**
   ```
   🤖 [Compound Engineering] 调用req-dev代理分析需求...

   📊 需求分析结果:
      ❓ 这个功能的主要用户是谁？
      ❓ 成功的标准是什么？
      ❓ 有哪些边界情况需要考虑？
      ❓ 依赖哪些外部系统？
   ```

2. **SpecKit生成规格**
   ```
   📝 [SpecKit] 生成规格文档...
   ✓ 规格文档已生成: .ralph/specs/实现用户登录功能.md
   ```

3. **流程图生成**
   ```
   📊 [draw.io MCP] 生成任务流程图...
   ✓ 流程图已保存: .ralph/diagrams/task-flow.txt
   ```

4. **双记忆检索**
   ```
   🧠 从双记忆系统检索相关经验...
   ✓ 找到相关经验:
      - Hippocampus: 0条
      - claude-mem: 0条
   ```

---

## 📁 3分钟探索新文件结构

### 新增的目录和文件
```bash
# 查看新增的目录结构
tree .ralph -L 2

.ralph/
├─ tools/                    # 🆕 工具集成层
│  ├─ config.json
│  ├─ tools_manager.py
│  ├─ memory_integrator.py
│  └─ superpowers_rules.md
├─ context/                  # 🆕 Context Engineering
│  ├─ project-info.md
│  ├─ architecture.md
│  └─ coding-style.md
├─ diagrams/                 # 🆕 可视化图表
├─ memories/                 # 🆕 claude-mem存储
└─ specs/                    # 🆕 规格文档
```

### 查看关键文档
```bash
# 1. 查看项目信息
cat .ralph/context/project-info.md

# 2. 查看系统架构
cat .ralph/context/architecture.md

# 3. 查看编码规范
cat .ralph/context/coding-style.md

# 4. 查看Superpowers规则
cat .ralph/tools/superpowers_rules.md

# 5. 查看工具配置
cat .ralph/tools/config.json
```

---

## 🎯 5分钟理解核心概念

### 1. 工具管理器 (tools_manager)

**作用**: 统一管理11大工具的配置和触发

**使用方式**:
```python
from tools_manager import get_tools_manager

tm = get_tools_manager()

# 检查工具是否启用
if tm.is_tool_enabled("superpowers"):
    print("Superpowers已启用")

# 检查是否应该触发技能
context = {
    "action": "code_change",
    "description": "修改登录逻辑"
}
if tm.should_trigger_skill("code_review", context):
    print("应该触发code-review")
```

### 2. 记忆集成器 (memory_integrator)

**作用**: 融合Hippocampus和claude-mem的双记忆系统

**使用方式**:
```python
from memory_integrator import get_memory_integrator

mi = get_memory_integrator()

# 检索相关经验
results = mi.retrieve_combined("用户登录", top_k=5)

# 格式化为上下文
context = mi.format_for_context(results)
print(context)
```

### 3. Brain v3

**新增方法**:
```python
brain = BrainV3()

# 完整规划流程（集成所有工具）
blueprint = brain.plan_task("实现用户注册")

# 步骤包括:
# 1. CE req-dev分析需求 ✅
# 2. SpecKit生成规格 ✅
# 3. 分解为Phase ✅
# 4. 生成流程图 ✅
# 5. 检索经验 ✅
# 6. 保存蓝图 ✅
```

### 4. Context Engineering

**结构化上下文管理**:

| 文件 | 用途 |
|------|------|
| project-info.md | 项目基本信息、技术栈 |
| architecture.md | 系统架构详细说明 |
| coding-style.md | 编码规范、最佳实践 |
| decisions.md (待创建) | 架构决策记录 |

### 5. Superpowers质量纪律

**Bright-Line Rules**（明确边界规则）:

```markdown
🚫 禁止省略代码 - 不允许 "// ...rest"
✅ 必须编写测试 - 每个功能都要有测试
✅ 必须代码审查 - 自动触发审查
🚫 禁止占位符 - 不允许 "TODO: 稍后实现"
```

---

## 🔧 配置和定制

### 开启/关闭工具

编辑 `.ralph/tools/config.json`:

```json
{
  "tools": {
    "superpowers": {
      "enabled": true,      // 改为false可关闭
      "auto_trigger": true
    },
    "claude_mem": {
      "enabled": true,
      "compression": {
        "enabled": true
      }
    }
  }
}
```

### 调整权重

```json
{
  "memory_integrator": {
    "hippocampus_weight": 0.6,  // Hippocampus权重
    "claude_mem_weight": 0.4     // claude-mem权重
  }
}
```

---

## 📊 新旧版本对比

### 任务规划流程对比

**v2.x流程**:
```
User输入 → Brain简单分解 → 保存蓝图 → 结束
```

**v3.0流程**:
```
User输入
    ↓
CE需求分析 (新)
    ↓
SpecKit生成规格 (新)
    ↓
Brain智能分解
    ↓
生成流程图 (新)
    ↓
检索双记忆 (新)
    ↓
保存蓝图
```

### 功能对比表

| 功能 | v2.x | v3.0 |
|------|------|------|
| 需求分析 | ❌ | ✅ CE代理 |
| 规格生成 | ❌ | ✅ SpecKit |
| 流程可视化 | ❌ | ✅ draw.io |
| 记忆系统 | Hippocampus单一 | Hippocampus + claude-mem双记忆 |
| 质量保证 | 基础验证 | Superpowers全面检查 |
| 上下文管理 | JSON配置 | Context Engineering体系 |

---

## 🎓 实战示例

### 示例1: 规划一个新功能

```bash
# 使用v3.0规划
python brain_v3.py "实现用户找回密码功能，支持邮箱和手机"

# 输出:
# ✓ CE分析需求
# ✓ 生成规格文档
# ✓ 分解为Phase
# ✓ 生成流程图
# ✓ 检索相关经验
```

**生成的文件**:
- `.janus/project_state.json` - 任务蓝图
- `.ralph/specs/实现用户找回密码功能....md` - 规格文档
- `.ralph/diagrams/task-flow.txt` - 流程图

### 示例2: 查看生成的规格

```bash
cat .ralph/specs/*.md
```

**内容示例**:
```markdown
# 实现用户找回密码功能 - 功能规格

## 概述
实现用户找回密码功能，支持邮箱和手机

## 输入
- 待定义

## 输出
- 待定义

## 测试用例
- [ ] 正常情况测试
- [ ] 边界情况测试
- [ ] 错误处理测试
```

---

## ⚙️ 高级用法

### 在Python代码中使用

```python
# 导入工具
from tools_manager import get_tools_manager
from memory_integrator import get_memory_integrator
from brain_v3 import BrainV3

# 初始化
tm = get_tools_manager()
mi = get_memory_integrator()
brain = BrainV3()

# 检查配置
print("启用的工具:", tm.enabled_tools)

# 规划任务
blueprint = brain.plan_task("你的任务描述")

# 检索记忆
memories = mi.retrieve_combined("查询关键词")
context = mi.format_for_context(memories)
print(context)
```

### 自定义工具配置

```python
# 读取配置
import json
with open('.ralph/tools/config.json', 'r') as f:
    config = json.load(f)

# 修改配置
config['tools']['superpowers']['enabled'] = False

# 保存配置
with open('.ralph/tools/config.json', 'w') as f:
    json.dump(config, f, indent=2)
```

---

## 🐛 故障排除

### 问题1: ImportError

**症状**:
```
ImportError: No module named 'tools_manager'
```

**解决**:
```bash
# 确保在正确的目录
cd D:\AI_Projects\system-max

# 检查文件是否存在
ls .ralph/tools/tools_manager.py

# 使用绝对路径运行
python -c "import sys; sys.path.append('.ralph/tools'); from tools_manager import get_tools_manager; print('OK')"
```

### 问题2: 配置文件未找到

**症状**:
```
警告: 配置文件未找到: .ralph/tools/config.json
```

**解决**:
```bash
# 检查文件
cat .ralph/tools/config.json

# 如果不存在，从集成文档重新创建
# 参考: INTEGRATION_STATUS_V3.md
```

### 问题3: Brain v3运行错误

**症状**:
```
NameError: name 'get_tools_manager' is not defined
```

**解决**:
```bash
# 这是正常的，模块会降级到基础功能
# 检查提示信息
python brain_v3.py 2>&1 | grep "警告"
```

---

## 📚 延伸阅读

### 核心文档

1. **集成状态报告** - `INTEGRATION_STATUS_V3.md`
   - 查看完整的集成状态
   - 了解待完成的Phase

2. **工具分析** - `.ralph/docs/tools-integration-analysis.md`
   - 11大工具详细分析
   - 集成方案说明

3. **系统架构** - `.ralph/context/architecture.md`
   - 完整的系统架构设计
   - 数据流和调用关系

4. **编码规范** - `.ralph/context/coding-style.md`
   - Python代码规范
   - Git提交规范

### 代码文件

- `brain_v3.py` - Brain增强版
- `.ralph/tools/tools_manager.py` - 工具管理器
- `.ralph/tools/memory_integrator.py` - 记忆集成器
- `.ralph/tools/config.json` - 工具配置

---

## 🎯 下一步

### 建议学习路径

1. **初级** (已完成✅)
   - ✅ 理解v3.0架构
   - ✅ 运行Brain v3
   - ✅ 查看生成的文件

2. **中级** (进行中)
   - [ ] 定制工具配置
   - [ ] 使用Python API
   - [ ] 实现Dealer v3

3. **高级** (未开始)
   - [ ] 集成OpenClaw并行执行
   - [ ] 真实claude-mem集成
   - [ ] 贡献代码改进

### 推荐实践

1. 先使用默认配置熟悉流程
2. 尝试规划几个实际任务
3. 查看生成的规格和流程图
4. 根据需要调整配置
5. 参与后续Phase的开发

---

## 💡 小贴士

### Tip 1: 善用工具配置
根据项目特点，开启/关闭不同的工具。例如纯后端项目可以关闭frontend-design。

### Tip 2: 查看生成文件
Brain v3会生成多个文件，建议都看一遍了解系统的思考过程。

### Tip 3: 渐进式启用
不必一次性启用所有功能，可以逐步启用各个工具。

### Tip 4: 保持文档更新
定期更新`.ralph/context/`下的文档，保持上下文准确。

### Tip 5: 利用记忆系统
每次完成任务后，系统会自动学习经验，下次相似任务会更智能。

---

## 🤝 获取帮助

### 遇到问题？

1. 查看 `INTEGRATION_STATUS_V3.md`
2. 查看 `.ralph/context/architecture.md`
3. 查看代码注释
4. GitHub Issues

### 想贡献代码？

1. 查看待完成的Phase (Phase 3-10)
2. 选择感兴趣的模块
3. Fork项目并提交PR

---

## 🎉 总结

**恭喜！你已经掌握了双脑Ralph系统v3.0的基础使用！**

核心要点回顾:
- ✅ v3.0集成了11大AI开发工具
- ✅ Brain v3提供智能规划能力
- ✅ 双记忆系统增强经验复用
- ✅ Superpowers保证代码质量
- ✅ Context Engineering结构化上下文

**现在你可以**:
- 使用Brain v3规划任务
- 查看自动生成的规格和流程图
- 理解系统的工作原理
- 参与后续开发

**下一步**:
建议阅读 `INTEGRATION_STATUS_V3.md` 了解完整的系统状态和开发计划。

---

**版本**: v3.0.0-alpha
**最后更新**: 2026-02-11

**让AI开发更智能、更高效！** 🚀✨
