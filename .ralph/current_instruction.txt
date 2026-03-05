# 🎯 任务执行指令 (Dealer v3.0)

## 📋 任务概览

**角色**: 前端架构师 (Vue/React)
**任务名称**: Package Ralph Worker... - Phase 1: 核心功能实现
**操作类型**: MODIFY
**任务类别**: frontend

---

## 📝 任务详情

### 目标
Package Ralph Worker automation layer: copy ~/.ralph/ directory (ralph_loop.sh, lib/) to super system/.ralph-worker/, create install_ralph_worker.sh script, update DEPLOYMENT.md with Worker installation guide, verify complete Brain-Dealer-Worker workflow

### 目标文件


---

## 📁 当前文件内容

---

## 🏗️ 项目信息 (Context Engineering)

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

---

## 📐 编码规范 (Context Engineering)


---

## 💡 相关经验 (双记忆系统)

## 完整历史上下文 (来自claude-mem)

### 记录 1
**类型**: learning
**内容**: 邮箱验证链接有效期设置为24小时
**上下文**: {'situation': '用户注册流程', 'outcome': '减少过期投诉'}

### 记录 2
**类型**: learning
**内容**: 邮箱验证链接有效期设置为24小时
**上下文**: {'situation': '用户注册流程', 'outcome': '减少过期投诉'}

### 记录 3
**类型**: learning
**内容**: 邮箱验证链接有效期设置为24小时
**上下文**: {'situation': '用户注册流程', 'outcome': '减少过期投诉'}

### 记录 4
**类型**: error_solution
**内容**: 问题: 邮件发送失败 | 解决: 使用SMTP重试机制
**上下文**: {'error_type': 'email', 'stack_trace': ''}

### 记录 5
**类型**: decision
**内容**: 使用临时Token而非新密码直接发送
**上下文**: {'alternatives': ['临时Token', '发送新密码'], 'rationale': '更安全，避免密码明文传输'}

---

## ⚡ Superpowers质量纪律

# Superpowers 质量纪律规则

## 🚫 Bright-Line Rules（明确边界规则）

### 1. 禁止省略代码
**规则**: 永远不要使用 `// ...rest`, `# ... 其余代码` 或类似占位符

**错误示例**:
```python
def process_data(data):
    # 处理逻辑
    # ...rest of the code
    return result
```

**正确示例**:
```python
def process_data(data):
    if not data:
        raise ValueError("Data cannot be empty")

    processed = []
    for item in data:
        cleaned = item.strip()
        if cleaned:
            processed.append(cleaned.upper())

    return processed
```

##
---

## 🚦 质量门控 (Compound Engineering)

请确保通过以下质量检查:

- [ ] code_complete
- [ ] tests_pass

---

## ✅ 成功标准

1. ✓ 正确实现所有修改需求
2. ✓ 保持代码整体一致性
3. ✓ 更新所有相关注释和文档
4. ✓ 不破坏任何现有功能
5. ✓ 处理所有边界情况
6. ✓ 代码可直接运行测试

---

## 🎯 自动触发的技能

根据Superpowers配置，以下技能将自动触发:

- ✓ **code_review**: 任务完成后自动执行
- ✓ **testing**: 任务完成后自动执行

---

## 🚀 执行协议

### 代码规范
1. **所有代码必须包裹在正确的 Markdown 代码块中**（使用 ```python）
2. **🚫 严禁省略代码**（不允许使用 `// ...rest`、`# ... 其余代码`或任何省略符号）
3. **必须提供完整的文件内容**（如需修改文件，提供从头到尾的完整代码）
4. **保持原有的缩进和代码风格**（与现有代码保持一致）
5. **添加必要的中文注释**（解释关键逻辑和复杂算法）

### 操作步骤
1. 📖 **仔细阅读** - 理解当前文件内容和项目上下文
2. 💡 **吸收经验** - 学习相关历史经验和决策
3. 📐 **规划方案** - 设计实现方案和代码结构
4. ⚙️ **实现代码** - 编写完整的、可运行的代码
5. ✅ **自我检查** - 对照成功标准和质量纪律

### 输出要求
1. **📝 实现思路** - 简要说明你的设计思路和关键决策
2. **💻 完整代码** - 提供所有文件的完整代码（不省略）
3. **💬 关键解释** - 解释重要的技术决策和权衡
4. **🧪 测试说明** - 说明如何测试和验证功能

---

## 📌 开始执行

请严格按照以上要求完成任务。记住：

- ⚠️ **禁止省略代码** - 这是最重要的规则
- ✅ **完整实现** - 不留TODO，不留占位符
- 🎯 **质量第一** - 代码质量比速度更重要
- 📚 **学习经验** - 充分利用历史经验避免重复错误

祝你顺利完成任务！🚀
