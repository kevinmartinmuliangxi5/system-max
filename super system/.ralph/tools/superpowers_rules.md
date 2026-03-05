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

### 2. 必须编写测试
**规则**: 每个新功能必须包含单元测试

**最低要求**:
- 正常情况测试
- 边界情况测试
- 错误处理测试

**示例**:
```python
def test_process_data():
    # 正常情况
    assert process_data(["hello", "world"]) == ["HELLO", "WORLD"]

    # 边界情况
    assert process_data([]) == []
    assert process_data(["  ", ""]) == []

    # 错误处理
    with pytest.raises(ValueError):
        process_data(None)
```

### 3. 必须代码审查
**规则**: 修改代码后自动触发自我审查

**检查清单**:
- [ ] 是否有安全漏洞？
- [ ] 是否有性能问题？
- [ ] 是否遵循项目代码规范？
- [ ] 是否有足够的错误处理？
- [ ] 是否有潜在的边界情况？

### 4. 禁止占位符代码
**规则**: 不允许说"这是简化版"或"待完善"

**错误示例**:
```python
# TODO: 稍后实现
def calculate_total():
    pass
```

**正确做法**: 要么完整实现，要么不写

## ✅ 自动技能触发机制

### 触发规则
当满足以下条件之一时，自动调用相应技能：

| 条件 | 触发技能 | 说明 |
|------|---------|------|
| 修改代码 | code-review | 立即审查变更 |
| 新建功能 | testing | 生成测试用例 |
| 遇到Bug | debugging | 系统化调试流程 |
| 设计阶段 | brainstorming | 通过提问完善设计 |
| 重构代码 | refactoring | 重构指南 |
| 性能问题 | performance | 性能优化建议 |

### 触发阈值
如果有 **1%的可能性** 需要某个技能，就必须触发

### 示例工作流
```
User: "修改登录功能，增加邮箱验证"
    ↓
自动触发 brainstorming
    ├─ 问：需要验证哪些邮箱格式？
    ├─ 问：验证失败如何提示？
    └─ 问：是否需要验证码？
    ↓
执行修改
    ↓
自动触发 code-review
    ├─ 检查：邮箱正则是否安全？
    ├─ 检查：错误提示是否友好？
    └─ 检查：是否有SQL注入风险？
    ↓
自动触发 testing
    ├─ 生成：正确邮箱测试
    ├─ 生成：错误邮箱测试
    └─ 生成：特殊字符测试
```

## 🎯 质量标准

### 代码质量
- ✅ 完整实现（无省略）
- ✅ 错误处理完善
- ✅ 注释清晰（必要时）
- ✅ 命名规范
- ✅ 无安全漏洞

### 测试覆盖
- ✅ 单元测试覆盖率 > 80%
- ✅ 关键路径有集成测试
- ✅ 边界情况全覆盖

### 文档要求
- ✅ 复杂逻辑有说明
- ✅ API有文档注释
- ✅ README保持更新

## 🔄 强制执行流程

### 1. 开发前（Planning）
```
检查清单:
□ 需求是否清晰？
□ 是否有技术方案？
□ 是否考虑边界情况？
```

### 2. 开发中（Execution）
```
实时检查:
□ 代码是否完整？
□ 是否边写边测试？
□ 是否遵循规范？
```

### 3. 开发后（Review）
```
最终检查:
□ 代码审查通过？
□ 测试全部通过？
□ 文档已更新？
```

## ⚠️ 违规处理

如果发现违反Bright-Line Rules的行为：

1. **立即停止** 当前操作
2. **修正问题** 返工修复
3. **记录经验** 避免再犯

## 📊 质量度量

系统会自动追踪：
- 代码完整度（无省略）
- 测试覆盖率
- 代码审查次数
- Bug发现率

目标：
- 完整度 = 100%
- 覆盖率 > 80%
- Bug率 < 5%
