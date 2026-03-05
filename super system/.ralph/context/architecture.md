# 双脑Ralph系统 - 架构设计

## 系统总体架构

```
┌─────────────────────────────────────────────────────────┐
│                双脑Ralph系统 v3.0                         │
│           (Dual-Brain Commander System)                 │
└─────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │  User   │    │  Brain  │    │  Tools  │
    │ (输入)   │    │  (规划)  │    │  (工具)  │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
              ┌──────────▼──────────┐
              │   Memory Layer      │
              │  (记忆层)            │
              │  ┌──────────────┐   │
              │  │ Hippocampus  │   │
              │  │ (海马体)      │   │
              │  └──────────────┘   │
              │  ┌──────────────┐   │
              │  │ claude-mem   │   │
              │  │ (会话记忆)    │   │
              │  └──────────────┘   │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │   Dealer Layer      │
              │  (分配层)            │
              │  ┌──────────────┐   │
              │  │ TaskRouter   │   │
              │  └──────────────┘   │
              │  ┌──────────────┐   │
              │  │ Context Mgr  │   │
              │  └──────────────┘   │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │   Worker Layer      │
              │  (执行层)            │
              │  ┌──────────────┐   │
              │  │    Ralph     │   │
              │  │  (自动执行)   │   │
              │  └──────────────┘   │
              │  ┌──────────────┐   │
              │  │Quality Check │   │
              │  └──────────────┘   │
              └─────────────────────┘
```

## 层级设计

### 1. User Layer (用户层)
**职责**: 提供自然语言需求

**输入形式**:
- 自然语言描述任务
- 问答式澄清需求
- 确认任务规划

**交互方式**:
- 直接与Brain对话
- 通过AskUserQuestion回答问题
- 审查Brain的规划结果

### 2. Brain Layer (大脑层)
**职责**: 理解需求、规划任务、审查产出

**核心组件**:
- **需求分析器** (Requirements Analyzer)
  - 使用CE的req-dev代理
  - 主动提问澄清细节
  - 复述确认理解

- **规格生成器** (Spec Generator)
  - 集成SpecKit
  - 生成结构化规格文档
  - 定义验收标准

- **任务分解器** (Task Decomposer)
  - 分解为多个Phase
  - 识别依赖关系
  - 分配优先级

- **质量审查器** (Quality Reviewer)
  - Phase间产出审查
  - 代码质量检查
  - 接口一致性验证

**工作流程**:
```python
def brain_workflow(user_request):
    # 1. 分析需求
    requirements = analyze_requirements(user_request)  # CE req-dev

    # 2. 生成规格
    spec = generate_spec(requirements)  # SpecKit

    # 3. 分解任务
    phases = decompose_to_phases(spec)

    # 4. 生成蓝图
    blueprint = create_blueprint(phases)

    # 5. 生成流程图 (v3.0新增)
    flowchart = generate_flowchart(blueprint)  # draw.io MCP

    return blueprint
```

### 3. Memory Layer (记忆层)
**职责**: 存储和检索经验

**双记忆系统**:

#### Hippocampus (海马体) - 核心经验库
```python
# 特点
- 存储结构化经验 (<learning>标签)
- BM25 + TF-IDF混合检索
- 77个中英文同义词映射
- 跨语言支持

# 数据结构
{
  "problem": "任务核心问题",
  "solution": "解决方案",
  "pitfalls": "注意事项",
  "tags": ["标签1", "标签2"],
  "timestamp": "2026-02-11"
}
```

#### claude-mem - 完整会话记忆
```python
# 特点
- 自动捕获完整对话
- AI智能压缩
- 语义+关键词混合检索
- 5-Hook生命周期

# 数据结构
{
  "session_id": "sess-001",
  "observations": [
    {
      "type": "decision",
      "content": "决定使用BM25算法",
      "context": "为了提升检索准确度",
      "timestamp": "2026-02-11T10:00:00"
    }
  ]
}
```

**记忆融合策略**:
```python
def retrieve_memory(query):
    # 1. 从claude-mem获取完整历史
    full_history = claude_mem.search(query, top_k=3)

    # 2. 从Hippocampus获取核心经验
    core_experience = hippocampus.retrieve(query, top_k=3)

    # 3. 融合结果
    merged = merge_memories(full_history, core_experience)

    return merged
```

### 4. Dealer Layer (分配层)
**职责**: 生成详细执行指令

**核心组件**:

#### TaskRouter (任务路由器)
```python
# 功能
- 根据任务类型分配角色
- 6种专业策略 (frontend, backend, test, debug, devops, data)
- 基于关键词和文件扩展名

# 路由规则
def route_task(task):
    if "UI" in task or "前端" in task:
        return "frontend"
    elif "数据库" in task or "API" in task:
        return "backend"
    elif "测试" in task:
        return "test"
    # ...
```

#### ContextManager (上下文管理器)
```python
# 功能
- 加载项目上下文
- 动态注入相关信息
- Context Engineering支持

# 上下文构建
def build_context(task):
    context = []

    # 基础上下文
    context.append(load_file(".ralph/context/project-info.md"))

    # 动态上下文
    if task["category"] == "frontend":
        context.append(load_file(".ralph/context/coding-style.md"))

    # 历史决策
    decisions = search_decisions(task["name"])
    context.append(decisions)

    # 记忆检索
    memories = retrieve_memory(task["name"])
    context.append(memories)

    return "\n\n".join(context)
```

#### SuperpowersIntegrator (质量纪律集成器)
```python
# 功能
- 注入Bright-Line Rules
- 配置技能自动触发
- 设置质量门禁

# 规则注入
def inject_superpowers_rules(instruction):
    rules = load_bright_line_rules()
    instruction += "\n\n## Superpowers质量纪律\n"
    instruction += rules
    return instruction
```

**Dealer工作流程**:
```python
def dealer_workflow(task):
    # 1. 路由任务
    category, role = route_task(task)

    # 2. 构建上下文
    context = build_context(task)

    # 3. 检索记忆
    memories = retrieve_memory(task["name"])

    # 4. 注入质量规则
    rules = inject_superpowers_rules()

    # 5. 生成指令
    instruction = generate_instruction(
        task=task,
        context=context,
        memories=memories,
        rules=rules
    )

    # 6. 生成架构图 (v3.0新增)
    if len(task["target_files"]) > 3:
        architecture_diagram = generate_architecture(task)

    return instruction
```

### 5. Worker Layer (执行层)
**职责**: 自动化循环执行任务

**核心组件**:

#### Ralph (循环执行器)
```python
# 功能
- 读取Dealer生成的指令
- 循环迭代执行
- 自我验证
- 强制学习

# 执行循环
def ralph_loop(instruction):
    max_iterations = 50
    for i in range(max_iterations):
        # 1. 执行当前迭代
        result = execute_iteration(instruction)

        # 2. 自动触发技能 (v3.0新增)
        if code_changed:
            trigger_skill("code_review")

        if new_feature:
            trigger_skill("testing")

        # 3. 质量检查
        if not quality_check(result):
            continue  # 重试

        # 4. 检查完成条件
        if task_completed:
            # 5. 强制输出学习标签
            output_learning_tag()
            output_promise_tag("COMPLETE")
            break
```

#### QualityChecker (质量检查器)
```python
# 功能
- 自动代码审查
- 测试覆盖率检查
- 安全漏洞扫描
- 性能问题检测

# 检查流程
def quality_check(result):
    checks = []

    # Superpowers Bright-Line Rules
    if code_omitted(result):
        return False  # 不允许省略代码

    if no_tests(result):
        return False  # 必须有测试

    # Compound Engineering质量门禁
    if not validate_quality_gate("execution", result):
        return False

    return True
```

## 数据流

### 任务执行数据流
```
User Request
    ↓
[Brain] 需求分析
    ↓
Spec Document
    ↓
[Brain] 任务分解
    ↓
Task Blueprint
    ↓
[Dealer] 指令生成
    ├─ 检索记忆(Hippocampus + claude-mem)
    ├─ 构建上下文(Context Engineering)
    └─ 注入规则(Superpowers)
    ↓
Detailed Instruction
    ↓
[Worker] 循环执行
    ├─ 自动触发技能
    ├─ 质量检查
    └─ 输出学习标签
    ↓
Completed Task + Learning Tag
    ↓
[Memory] 存储经验
    ├─ learning标签 → Hippocampus
    └─ 完整会话 → claude-mem
    ↓
[Brain] Phase审查
    ├─ 验证产出
    ├─ 检查质量
    └─ 决定是否继续
```

### 记忆检索数据流
```
Query
    ↓
[Memory Layer] 并行检索
    ├─ [Hippocampus] BM25检索结构化经验
    └─ [claude-mem] 混合检索完整历史
    ↓
Merge Results
    ↓
Ranked Memories
    ↓
[Dealer] 注入上下文
```

## 技能触发机制

### Superpowers技能自动触发
```
触发条件检测
    ↓
条件满足？
    ├─ 是 → 自动调用技能
    │     ├─ code_review
    │     ├─ testing
    │     ├─ debugging
    │     └─ brainstorming
    └─ 否 → 继续执行
```

### 触发规则表
| 条件 | 触发技能 | 时机 |
|------|---------|------|
| 代码修改 | code-review | 修改后立即 |
| 新功能 | testing | 实现后 |
| Bug | debugging | 发现后 |
| 设计阶段 | brainstorming | 开始前 |
| 重构 | refactoring | 重构中 |

## 并行执行架构 (v3.0新增)

### OpenClaw + tmux并行模式
```
[OpenClaw Scheduler]
    │
    ├─ tmux session 1: Ralph实例A
    │  └─ Phase 1: 前端开发
    │
    ├─ tmux session 2: Ralph实例B
    │  └─ Phase 2: 后端开发
    │
    └─ tmux session 3: Ralph实例C
       └─ Phase 3: 测试编写

各实例独立执行，互不干扰
完成后通过Hook回调OpenClaw
```

## 可视化架构 (v3.0新增)

### draw.io MCP集成
```
[Brain] 规划阶段
    ↓
生成任务流程图
    ↓
保存到 .ralph/diagrams/task-flow.drawio
    ↓
[Dealer] 指令中引用

[Dealer] 指令生成
    ↓
分析文件依赖
    ↓
生成架构图
    ↓
保存到 .ralph/diagrams/architecture.drawio
```

## 设计原则

### 1. 单一职责
每个层级只负责自己的核心功能

### 2. 依赖倒置
上层不依赖下层具体实现，通过接口交互

### 3. 开放封闭
对扩展开放（易于集成新工具），对修改封闭（不破坏现有功能）

### 4. 接口隔离
各层级通过清晰的接口通信

### 5. 可测试性
每个组件可独立测试

## 扩展性

### 新工具集成
1. 在 `.ralph/tools/config.json` 添加配置
2. 在 `tools_manager.py` 添加检测逻辑
3. 在对应层级集成调用

### 新技能添加
1. 定义触发条件
2. 添加到 `superpowers_rules.md`
3. 在Worker中实现触发逻辑

### 新代理接入
1. 在 CE agents配置中添加
2. 在Brain或Dealer中集成调用
3. 定义输入输出格式

## 性能优化

### 记忆检索优化
- LRU缓存热点查询
- 异步并行检索
- 结果缓存复用

### 并行执行优化
- 独立Phase并行执行
- tmux会话隔离
- 资源限制配置

### 上下文优化
- 动态按需加载
- 相关性过滤
- Token使用优化

## 安全考虑

### 代码审查
- Superpowers强制代码审查
- 安全漏洞扫描
- 敏感信息检测

### 权限控制
- 文件访问权限
- 工具调用权限
- API调用限制

### 数据隔离
- 项目间数据隔离
- 会话间数据隔离
- 敏感数据加密

## 监控与日志

### 系统监控
- 任务执行状态
- 工具调用统计
- 质量指标追踪

### 日志记录
- 执行日志: `.ralph/logs/`
- 错误日志: `.ralph/logs/errors/`
- 性能日志: `.ralph/logs/performance/`

## 版本演进

### v1.0 (2026-01-28)
- 基础双脑架构
- 海马体记忆系统
- 任务路由器

### v2.0 (2026-01-28)
- Dealer增强版
- Brain Phase审查
- 完整工作流

### v3.0 (2026-02-11)
- 集成11大工具
- 双记忆系统
- 并行执行支持
- 可视化增强
- Context Engineering

## 未来规划

### v3.1 (计划中)
- 完整OpenClaw集成
- 更多CE代理支持
- 增强可视化

### v4.0 (长期)
- 多模型支持
- 分布式执行
- Web界面
