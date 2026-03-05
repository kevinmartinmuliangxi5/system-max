# 双脑+Ralph系统 v2.0 升级总结

**升级日期**: 2024-02-04

---

## 📋 升级概览

本次升级针对用户提出的6个改进方向，全面增强了双脑+Ralph系统的能力：

| 改进项 | 状态 | 核心变化 |
|--------|------|----------|
| 1. 省API策略 | ✅ | 分层模型选择 + 经验复用 |
| 2. 智慧建议 | ✅ | Brain主动点拨，选项引导 |
| 3. 任务泛化 | ✅ | 知识库 + 技术栈识别 |
| 4. 可复利性 | ✅ | 经验反馈循环闭环 |
| 5. Brain记忆持久化 | ✅ | 身份文件 + 检查点机制 |
| 6. 全流程引导 | ✅ | 四阶段引导直到验收 |

---

## 🔧 修改/新增的文件清单

### 新增文件

| 文件 | 用途 |
|------|------|
| `.janus/brain_identity.json` | Brain身份持久化配置 |
| `brain_prompt_v2.md` | 升级版Brain提示词 |
| `.janus/knowledge/streamlit.json` | Streamlit知识库 |
| `.janus/knowledge/python_web.json` | Python Web知识库 |
| `.janus/knowledge/react.json` | React知识库 |
| `.janus/knowledge/security.json` | 安全最佳实践知识库 |
| `.janus/knowledge/index.json` | 知识库索引 |
| `.janus/core/router_v2.py` | 增强版任务路由器 |
| `SYSTEM_UPGRADE_V2.md` | 本升级说明文档 |

### 修改文件

| 文件 | 修改内容 |
|------|----------|
| `brain_prompt.md` | 替换为v2版本（原版备份为brain_prompt_v1_backup.md） |
| `.ralph/PROMPT.md` | 添加经验学习协议（`<learning>`标签要求） |
| `ralph_auto_stream_fixed.sh` | 添加经验自动提取和存储逻辑 |

---

## 📚 改进详情

### 1. 省API策略

**文件**: `brain_prompt.md`, `.janus/brain_identity.json`

**实现**:
- 分层模型选择：简单任务用Haiku，中等用Sonnet，复杂用Opus
- 经验复用：查询海马体，相似任务直接复用蓝图模板
- 增量规划：小改动不重新规划整个模块

**配置位置**:
```json
// .janus/brain_identity.json
"model_selection_guide": {
  "simple_tasks": {"recommended_model": "haiku"},
  "medium_tasks": {"recommended_model": "sonnet"},
  "complex_tasks": {"recommended_model": "opus"}
}
```

---

### 2. 智慧建议

**文件**: `brain_prompt.md`, `.janus/brain_identity.json`, `.janus/core/router_v2.py`

**触发条件**:
- 登录/密码/认证 → 安全建议
- 慢/优化/性能 → 性能建议
- 重构/架构 → 架构建议
- 数据库/存储 → 数据建议
- 界面/页面 → UI建议

**使用方式**:
Brain在需求确认后、生成蓝图前，自动检测并通过AskUserQuestion提出建议：

```
💡 专家建议

根据您的需求，我有几点建议：

1️⃣ 安全加固（推荐）- 使用bcrypt加密密码
2️⃣ Token刷新 - 实现自动Token刷新
3️⃣ 日志审计 - 记录登录日志

您希望采纳哪些？[多选]
```

---

### 3. 任务泛化能力

**文件**: `.janus/knowledge/*.json`, `.janus/core/router_v2.py`

**知识库内容**:
- `streamlit.json`: Streamlit模式、常见坑点、组件用法
- `python_web.json`: FastAPI/Flask/Django模式、认证、数据库
- `react.json`: Hooks、状态管理、性能优化
- `security.json`: 密码存储、输入验证、常见漏洞防护

**技术栈自动识别**:
```python
# router_v2.py 会自动检测
- .jsx/.tsx → React
- .vue → Vue
- "streamlit"/"st." → Streamlit
- "fastapi"/@app.get → FastAPI
```

---

### 4. 可复利性（经验反馈循环）

**文件**: `.ralph/PROMPT.md`, `ralph_auto_stream_fixed.sh`

**闭环流程**:
```
Worker执行完成
    ↓
输出 <learning> 标签（强制）
    ↓
Ralph脚本自动提取
    ↓
存入Hippocampus海马体
    ↓
下次相似任务自动检索
```

**Worker必须输出的格式**:
```xml
<learning>
  <problem>一句话描述问题</problem>
  <solution>1-3句话描述方案</solution>
  <pitfalls>坑点（可选）</pitfalls>
</learning>

<promise>COMPLETE</promise>
```

**Ralph自动存储**:
```bash
# ralph_auto_stream_fixed.sh 在检测到完成信号后自动执行
# 提取<learning>标签内容
# 调用 Hippocampus.store(problem, solution)
# 显示存储结果
```

---

### 5. Brain记忆持久化

**文件**: `.janus/brain_identity.json`

**快速激活**:
用户只需说"你是Brain"，Brain立即恢复完整身份和职责。

**身份检查点**:
```json
"checkpoints": {
  "before_blueprint": "我是否完成了需求澄清和确认？",
  "after_blueprint": "我是否告知用户下一步运行bash start.sh？",
  "during_review": "我是否存储了经验到海马体？",
  "after_completion": "我是否引导用户完成验收？"
}
```

**禁止行为**:
- 不直接执行代码（那是Worker的事）
- 不跳过需求确认直接生成蓝图
- 不忘记存储经验到海马体
- 不在验收阶段前结束引导

---

### 6. 全流程引导

**文件**: `brain_prompt.md`

**四阶段流程**:

```
阶段1: 需求阶段
├─ 接收需求
├─ 需求澄清（AskUserQuestion）
├─ 需求确认（复述）
└─ 💡智慧建议

阶段2: 规划阶段
├─ 经验查询（海马体）
├─ 复杂度判断
├─ 智能拆解
├─ 生成蓝图
└─ 下一步指引

阶段3: 执行阶段
├─ Ralph/Worker执行
├─ Brain审查（每Phase）
└─ 经验存储（强制）

阶段4: 验收阶段【新增】
├─ 完成确认
├─ 功能检查清单
├─ 问题收集
├─ 问题修复
├─ 最终确认
└─ 经验归档
```

---

## 🚀 使用指南

### 激活Brain

```
用户: 你是Brain

Brain: 🧠 Brain模式已激活！

我的核心职责：
• 需求握手 → 澄清确认
• 智慧建议 → 主动点拨
• 智能拆解 → 分阶段规划
• 全流程引导 → 从接收到验收

请描述您的需求。
```

### 完整工作流示例

```
1. 用户: 你是Brain
2. Brain: [激活问候]

3. 用户: 我想给应用添加用户登录功能
4. Brain: [需求澄清 - AskUserQuestion]
5. 用户: [选择选项]

6. Brain: [需求确认 - 复述]
7. 用户: 正确

8. Brain: 💡专家建议 [检测到安全相关]
9. 用户: 采纳建议1和2

10. Brain: ✅蓝图已生成！
    📌下一步: bash start.sh

11. [用户运行Ralph]
12. [Worker执行Phase 1]

13. 用户: Phase 1完成了
14. Brain: [审查Phase 1] [存储经验]

15. [继续执行...]

16. 用户: 全部完成了
17. Brain: 🎯进入验收阶段 [功能检查清单]

18. 用户: 全部✅
19. Brain: 🎉项目验收完成！[经验归档]
```

---

## 📊 预期效果

### 成本优化
- 简单任务API成本降低 50-70%
- 经验复用减少重复推理 30-40%

### 质量提升
- 智慧建议覆盖安全、性能等关键领域
- 知识库提供最佳实践参考
- 全流程引导确保项目完整交付

### 效率提升
- 系统越用越聪明（经验积累）
- 预计第10个任务后效率提升 40%
- 预计第50个任务后接近专家级表现

---

## 🔍 验证测试

### 测试1: 经验存储

```bash
# 运行一个测试任务
bash ralph_auto_stream_fixed.sh

# 检查是否输出:
# ✅ 经验已存入海马体（Hippocampus）
# 📊 海马体当前记忆数: X 条
```

### 测试2: Brain身份持久化

```
# 新会话
用户: 你是Brain
# 预期: Brain立即显示激活问候和核心职责
```

### 测试3: 智慧建议触发

```
用户: 你是Brain
用户: 帮我实现用户登录功能

# 预期: Brain在需求确认后显示安全相关建议
```

### 测试4: 知识库加载

```python
# 测试router_v2
python .janus/core/router_v2.py

# 预期输出技术栈识别和智慧触发检测
```

---

## 📝 后续优化建议

1. **可视化仪表盘**: 开发Web界面展示系统运行状态和经验积累
2. **并行执行**: 支持多Worker并行处理独立任务
3. **自动测试**: Worker完成后自动运行测试验证
4. **知识库扩展**: 持续补充更多技术栈的最佳实践
5. **模型自适应**: 根据任务执行效果动态调整模型选择

---

## 📞 遇到问题？

1. 检查 `.janus/brain_identity.json` 是否存在
2. 检查 `.ralph/PROMPT.md` 是否包含学习协议
3. 检查 `ralph_auto_stream_fixed.sh` 是否更新
4. 查看 `.janus/memory.json` 验证经验存储

---

**双脑+Ralph v2.0 - 更智慧、更完整、更省心！** 🧠✨
