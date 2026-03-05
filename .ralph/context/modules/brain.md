# Brain模块文档

**模块**: Brain v3.0
**文件**: `brain_v3.py`
**版本**: v3.0.0-alpha
**最后更新**: 2026-02-11

---

## 模块概述

Brain是双脑Ralph系统的**任务理解与规划**模块，负责将用户的自然语言需求转化为结构化的任务蓝图。

### 核心职责

1. **需求分析** - 使用Compound Engineering方法论分析用户需求
2. **规格生成** - 使用SpecKit自动生成规格文档
3. **任务分解** - 将复杂任务分解为多个Phase
4. **流程可视化** - 生成任务流程图
5. **经验检索** - 从双记忆系统检索相关经验
6. **蓝图保存** - 保存任务蓝图供Dealer使用

---

## 架构设计

### 类图

```
BrainV3
├── __init__()
├── print_header()
├── load_blueprint()
├── save_blueprint()
├── analyze_with_ce()           # Compound Engineering分析
├── generate_spec()             # SpecKit规格生成
├── decompose_to_phases()       # 任务分解
├── generate_flowchart()        # 流程图生成
├── retrieve_relevant_experience()  # 经验检索
├── review_phase_output()       # Phase审查
├── plan_task()                 # 主流程
├── interactive_mode()          # 交互模式
└── _extract_task_name()        # 工具方法
```

### 集成组件

| 组件 | 类型 | 用途 |
|------|------|------|
| **CompoundEngineeringAgent** | 内部类 | CE方法论代理模拟 |
| **SpecKitGenerator** | 内部类 | 规格文档生成器 |
| **DrawioMCPSimulator** | 内部类 | 流程图生成模拟器 |
| **tools_manager** | 外部 | 工具配置管理 |
| **memory_integrator** | 外部 | 双记忆系统集成 |

---

## 核心流程

### plan_task() 主流程

```python
def plan_task(self, user_input: str) -> List[Dict]:
    """
    完整的任务规划流程

    Args:
        user_input: 用户输入的需求描述

    Returns:
        生成的任务蓝图（Phase列表）
    """
    # Step 1: CE需求分析
    ce_analysis = self.analyze_with_ce(user_input)

    # Step 2: 构建任务信息
    task_info = {
        'task_name': self._extract_task_name(user_input),
        'instruction': user_input,
        'target_files': [],
        'ce_analysis': ce_analysis
    }

    # Step 3: SpecKit生成规格
    spec = self.generate_spec(task_info)

    # Step 4: 分解为多个Phase
    phases = self.decompose_to_phases(task_info)

    # Step 5: 生成流程图
    flowchart_file = self.generate_flowchart(phases)

    # Step 6: 检索相关经验
    experience_context = self.retrieve_relevant_experience(task_info['task_name'])

    # Step 7: 保存蓝图
    self.save_blueprint(phases)

    return phases
```

### 数据流

```
用户输入 (自然语言)
    ↓
CE需求分析 (CompoundEngineeringAgent)
    ↓
任务信息构建 {task_name, instruction, target_files}
    ↓
SpecKit规格生成 → .ralph/specs/xxx.md
    ↓
任务分解 → Phase列表 [{task_name, instruction, status}, ...]
    ↓
流程图生成 → .ralph/diagrams/task-flow.txt
    ↓
经验检索 (memory_integrator) → 双记忆系统
    ↓
蓝图保存 → .janus/project_state.json
```

---

## API参考

### 类初始化

```python
brain = BrainV3()
```

**初始化做什么**:
- 创建必要的目录（.ralph/specs, .ralph/diagrams）
- 加载tools_manager和memory_integrator（如果可用）
- 初始化CE代理、SpecKit、draw.io模拟器
- 加载现有蓝图

### 主要方法

#### analyze_with_ce(user_input)

**用途**: 使用Compound Engineering的req-dev代理分析需求

**参数**:
- `user_input` (str): 用户输入的需求描述

**返回**:
- Dict: 需求分析结果，包含questions和requirements

**示例**:
```python
analysis = brain.analyze_with_ce("实现用户登录功能")
# 返回:
# {
#   'agent': 'req_dev',
#   'questions': ['这个功能的主要用户是谁？', ...],
#   'requirements': {
#     'functional': [],
#     'non_functional': [],
#     'constraints': []
#   }
# }
```

#### generate_spec(task_info)

**用途**: 使用SpecKit生成规格文档

**参数**:
- `task_info` (Dict): 任务信息字典

**返回**:
- str: 生成的规格文档内容

**副作用**:
- 保存规格文档到`.ralph/specs/{task_name}.md`

**示例**:
```python
spec = brain.generate_spec({
    'task_name': '实现用户登录',
    'instruction': '使用JWT实现用户认证'
})
```

#### decompose_to_phases(task_info)

**用途**: 将任务分解为多个Phase

**参数**:
- `task_info` (Dict): 任务信息字典

**返回**:
- List[Dict]: Phase列表

**示例**:
```python
phases = brain.decompose_to_phases({
    'task_name': '实现用户登录',
    'instruction': '使用JWT实现用户认证',
    'target_files': ['api/auth.py']
})
# 返回:
# [
#   {
#     'task_name': '实现用户登录 - Phase 1: 核心功能实现',
#     'instruction': '使用JWT实现用户认证',
#     'target_files': ['api/auth.py'],
#     'status': 'PENDING'
#   }
# ]
```

#### generate_flowchart(blueprint)

**用途**: 生成任务流程图

**参数**:
- `blueprint` (List[Dict]): 任务蓝图

**返回**:
- str: 流程图文件路径

**副作用**:
- 保存流程图到`.ralph/diagrams/task-flow.txt`

#### retrieve_relevant_experience(task_name)

**用途**: 从双记忆系统检索相关经验

**参数**:
- `task_name` (str): 任务名称

**返回**:
- Optional[str]: 格式化的经验上下文，如果没有结果返回None

**示例**:
```python
experience = brain.retrieve_relevant_experience("用户登录")
# 返回格式化的Markdown文本
```

#### plan_task(user_input)

**用途**: 完整的任务规划流程（主入口）

**参数**:
- `user_input` (str): 用户输入

**返回**:
- List[Dict]: 生成的任务蓝图

**示例**:
```python
blueprint = brain.plan_task("实现用户注册功能，支持邮箱验证")
```

---

## 使用示例

### 命令行使用

```bash
# 单任务模式
python brain_v3.py "实现用户登录功能"

# 交互式模式
python brain_v3.py
```

### Python API使用

```python
from brain_v3 import BrainV3

# 创建实例
brain = BrainV3()

# 规划任务
blueprint = brain.plan_task("实现用户注册功能，支持邮箱验证")

# 查看结果
print(f"生成了 {len(blueprint)} 个Phase")
for i, phase in enumerate(blueprint, 1):
    print(f"Phase {i}: {phase['task_name']}")
```

---

## 配置选项

Brain v3通过`.ralph/tools/config.json`配置集成工具：

```json
{
  "tools": {
    "compound_engineering": {
      "enabled": true,
      "agents": {
        "req_dev": {"enabled": true},
        "brainstorm": {"enabled": true}
      }
    },
    "speckit": {
      "enabled": true,
      "spec_format": "markdown",
      "spec_dir": ".ralph/specs"
    },
    "drawio_mcp": {
      "enabled": true,
      "output_dir": ".ralph/diagrams"
    }
  }
}
```

---

## 输出文件

### 蓝图文件

**路径**: `.janus/project_state.json`

**格式**:
```json
{
  "blueprint": [
    {
      "task_name": "实现用户登录 - Phase 1",
      "instruction": "...",
      "target_files": ["api/auth.py"],
      "status": "PENDING",
      "ce_analysis": {...},
      "spec_file": ".ralph/specs/实现用户登录.md"
    }
  ]
}
```

### 规格文档

**路径**: `.ralph/specs/{task_name}.md`

**内容**:
- 概述
- 输入/输出
- 业务规则
- 技术约束
- 测试用例
- 验收标准

### 流程图

**路径**: `.ralph/diagrams/task-flow.txt`

**格式**: 简单的文本流程图（未来升级为draw.io XML）

---

## 扩展点

### 1. 自定义CE代理

```python
class CustomCEAgent:
    def analyze(self, user_input):
        # 自定义需求分析逻辑
        return {...}

# 替换默认代理
brain.ce_agent = CustomCEAgent()
```

### 2. 自定义规格模板

修改`SpecKitGenerator.generate_spec()`方法：

```python
class CustomSpecKit(SpecKitGenerator):
    def generate_spec(self, task_info):
        # 自定义规格模板
        return f"# {task_info['task_name']}\n..."
```

### 3. 自定义分解策略

重写`decompose_to_phases()`方法：

```python
class CustomBrain(BrainV3):
    def decompose_to_phases(self, task_info):
        # 自定义分解逻辑
        # 例如：使用LLM智能分解
        return [...]
```

---

## 性能考虑

### 时间复杂度

| 操作 | 复杂度 | 说明 |
|------|--------|------|
| analyze_with_ce | O(1) | 模拟版本，常数时间 |
| generate_spec | O(n) | n为task_info大小 |
| decompose_to_phases | O(1) | 简化版本 |
| generate_flowchart | O(m) | m为Phase数量 |
| retrieve_relevant_experience | O(n*m) | n为记忆数量，m为查询复杂度 |

### 内存使用

- **蓝图**: ~1KB per Phase
- **规格文档**: ~2-5KB per task
- **流程图**: ~1KB per diagram
- **经验上下文**: ~5-10KB per retrieval

---

## 测试

### 单元测试

```python
def test_brain_v3_initialization():
    brain = BrainV3()
    assert brain.spec_dir.exists()
    assert brain.diagram_dir.exists()

def test_plan_task():
    brain = BrainV3()
    blueprint = brain.plan_task("测试任务")
    assert len(blueprint) > 0
    assert blueprint[0]['status'] == 'PENDING'
```

### 集成测试

```bash
# 完整流程测试
python brain_v3.py "实现用户登录功能"

# 验证输出文件
ls .janus/project_state.json
ls .ralph/specs/
ls .ralph/diagrams/
```

---

## 故障排查

### 问题1: 无法导入tools_manager

**症状**: `ImportError: No module named 'tools_manager'`

**原因**: Python路径未正确设置

**解决**:
```python
import sys
sys.path.append('.ralph/tools')
```

### 问题2: 规格文档未生成

**症状**: `.ralph/specs/`目录为空

**原因**: 目录权限问题或路径错误

**解决**:
```bash
# 检查目录
ls -la .ralph/specs

# 手动创建
mkdir -p .ralph/specs
chmod 755 .ralph/specs
```

### 问题3: 经验检索失败

**症状**: `警告: Hippocampus检索失败`

**原因**: Hippocampus API不兼容

**解决**: 系统会自动降级，仅影响经验检索质量，不影响主流程

---

## 最佳实践

### 1. 清晰的需求描述

❌ 不好:
```python
brain.plan_task("做登录")
```

✅ 好:
```python
brain.plan_task("实现用户登录功能，使用JWT认证，支持邮箱和密码登录")
```

### 2. 检查生成的文件

```python
blueprint = brain.plan_task("...")

# 检查规格文档
spec_file = f".ralph/specs/{blueprint[0]['task_name']}.md"
if os.path.exists(spec_file):
    print(f"✓ 规格已生成: {spec_file}")
```

### 3. 利用经验检索

Brain v3会自动检索相关经验，查看经验可以帮助理解任务：

```python
experience = brain.retrieve_relevant_experience("用户登录")
if experience:
    print("相关经验:")
    print(experience)
```

---

## 未来改进

### 短期 (1-2周)

- [ ] 真实的CE代理集成（调用LLM）
- [ ] 智能任务分解（使用LLM）
- [ ] 真实draw.io MCP集成

### 中期 (1-2月)

- [ ] 支持多语言需求（英文、日文）
- [ ] 依赖关系分析
- [ ] 优先级排序

### 长期 (3-6月)

- [ ] 需求变更管理
- [ ] 版本控制集成
- [ ] 项目管理集成（Jira、Trello）

---

## 参考资料

- [Compound Engineering方法论](https://github.com/PallavAg/CompoundEngineering)
- [SpecKit文档](https://github.com/your-org/speckit)
- [双记忆系统设计](../decisions.md#adr-001)

---

**维护者**: System Architect
**最后更新**: 2026-02-11
**版本**: v3.0.0-alpha
