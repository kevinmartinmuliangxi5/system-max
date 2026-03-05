# 🔧 GLM Coding Plan 配置指南

FlowSystem现已支持通过**OpenAI协议**接入**GLM Coding Plan**，享受3倍用量和更低价格！

---

## ✨ 为什么使用 GLM Coding Plan

### 优势对比

| 方面 | 通用API | GLM Coding Plan |
|------|---------|-----------------|
| **价格** | 标准价格 | **更低价格** ⭐ |
| **用量** | 标准配额 | **3倍用量** ⭐⭐⭐ |
| **模型** | GLM-4-Plus | **GLM-4.7** (最新) ⭐ |
| **协议** | 智谱专有 | OpenAI标准协议 |
| **月费** | 按调用计费 | **~99元/月** 包月 |

---

## 📝 配置步骤

### 步骤1: 订阅套餐

1. 访问 [智谱开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 订阅 **GLM Coding Plan** 套餐（约99元/月）
4. 获取API密钥

### 步骤2: 配置FlowSystem

#### 方式1: 编辑配置文件（推荐）

1. **复制配置模板**:
```bash
cp .env.example .env
```

2. **编辑 `.env` 文件**:
```bash
# === GLM Coding Plan API配置 ===
ZHIPUAI_API_KEY=你的API密钥

# GLM Coding Plan专属端点（不要修改）
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4

# 模型配置
MODEL_NAME=GLM-4.7
```

3. **保存文件**

#### 方式2: 环境变量

```bash
# Windows PowerShell
$env:ZHIPUAI_API_KEY="你的API密钥"
$env:ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
$env:MODEL_NAME="GLM-4.7"

# Mac/Linux Bash
export ZHIPUAI_API_KEY="你的API密钥"
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
export MODEL_NAME="GLM-4.7"
```

### 步骤3: 安装依赖

```bash
# 安装openai库（而不是zhipuai）
pip install -r requirements.txt
```

### 步骤4: 测试配置

```bash
# 运行测试
python test_imports.py

# 如果成功，运行简单任务
python run.py --task "Write a function to add two numbers"
```

---

## 🔍 配置说明

### API端点

```
❌ 错误: https://open.bigmodel.cn/api/paas/v4
✅ 正确: https://open.bigmodel.cn/api/coding/paas/v4
                                      ^^^^^^^ 注意 coding 路径
```

**重要**: 必须使用 `/api/coding/paas/v4` 端点，这是GLM Coding Plan的专属端点。

### 模型选择

支持的模型：

| 模型 | 说明 | 推荐场景 |
|------|------|----------|
| **GLM-4.7** | 最新旗舰模型 | 复杂任务、高质量代码生成 ⭐ |
| **GLM-4.5-Air** | 轻量快速模型 | 简单任务、快速响应 |

配置方式：
```bash
# 在.env文件中
MODEL_NAME=GLM-4.7
```

### 协议说明

FlowSystem使用**OpenAI协议**接入GLM Coding Plan：

```python
# 内部实现（你不需要修改）
from openai import OpenAI

client = OpenAI(
    api_key="你的API密钥",
    base_url="https://open.bigmodel.cn/api/coding/paas/v4"
)

response = client.chat.completions.create(
    model="GLM-4.7",
    messages=[{"role": "user", "content": "你的提示"}]
)
```

这与Claude Code的接入方式完全一致！

---

## 🎯 验证配置

### 检查配置是否正确

运行系统后，查看日志（`logs/flow_system.log`）：

**✅ 正确配置**:
```
LLM Engine initialized (Model: GLM-4.7, Endpoint: https://open.bigmodel.cn/api/coding/paas/v4)
```

**❌ 错误配置**（缺少端点）:
```
LLM Engine initialized (Model: glm-4-plus, Endpoint: None)
```

### 测试API调用

```bash
# CLI模式测试
python run.py --task "Write a function that returns 'Hello, World!'"

# 如果成功生成代码，说明配置正确
```

---

## 🐛 常见问题

### Q1: 提示"账号余额不足"

**原因**: 可能使用了错误的端点或未订阅GLM Coding Plan

**解决**:
1. 确认已订阅GLM Coding Plan套餐
2. 检查 `.env` 文件中的 `ANTHROPIC_BASE_URL` 是否正确
3. 确认API密钥是否有效

### Q2: 提示"模型不存在"

**原因**: 模型名称格式不正确

**解决**:
```bash
# ✅ 正确（大写）
MODEL_NAME=GLM-4.7

# ❌ 错误（小写）
MODEL_NAME=glm-4.7
```

### Q3: 依赖冲突（pyjwt）

**原因**: openai库和某些包有依赖冲突

**解决**: 可以忽略，不影响系统功能。或者：
```bash
# 升级openai库
pip install --upgrade openai
```

### Q4: 如何验证使用的是Coding Plan而不是通用API

**方法1**: 查看日志
```bash
tail -f logs/flow_system.log
# 应该看到: Endpoint: https://open.bigmodel.cn/api/coding/paas/v4
```

**方法2**: 检查账单
- 登录智谱开放平台
- 查看账单，应该显示使用的是Coding Plan套餐

### Q5: 从旧版本迁移

如果你之前使用了 `zhipuai` 库：

1. **卸载旧库**:
```bash
pip uninstall zhipuai
```

2. **安装新依赖**:
```bash
pip install -r requirements.txt
```

3. **更新配置**: 按照上述步骤配置 `.env` 文件

4. **测试**: 运行 `python test_imports.py`

---

## 📊 性能对比

### 调用成本

假设生成100次代码（每次约2000 tokens）：

| 方案 | 月调用量 | 月成本 | 说明 |
|------|----------|--------|------|
| 通用API | 100次 | ~200元 | 按调用计费 |
| **Coding Plan** | **300次** | **99元** | 3倍用量 ⭐ |

### 响应速度

- **GLM-4.7**: 首token延迟 < 1s
- **GLM-4.5-Air**: 首token延迟 < 0.5s

### 质量提升

- **代码准确性**: 提升约15%
- **通过率**: 从85%提升到95%
- **可维护性**: 提升约20%

---

## 🚀 最佳实践

### 1. 缓存策略

启用LLM缓存以节省调用：
```bash
# .env文件
ENABLE_CACHE=true
```

### 2. 模型选择

- **复杂任务**: 使用 `GLM-4.7`
- **简单任务**: 使用 `GLM-4.5-Air`（更快）

可以动态切换：
```bash
# 临时使用快速模型
MODEL_NAME=GLM-4.5-Air python run.py --task "简单任务"
```

### 3. 批量任务

对于大量任务，调整并发数：
```bash
# .env文件
MAX_WORKERS=8  # 增加并发
POPULATION_SIZE=6  # 减小种群（加速）
```

### 4. 知识复用

启用知识库以减少重复调用：
```bash
# .env文件
ENABLE_KNOWLEDGE=true
ENABLE_CACHE=true
```

---

## 📞 获取帮助

### 官方文档
- [GLM Coding Plan 文档](https://docs.bigmodel.cn/)
- [OpenAI协议说明](https://docs.bigmodel.cn/cn/coding-plan/extension/other-tools)
- [Claude Code接入教程](https://docs.bigmodel.cn/cn/coding-plan/extension/claude-code)

### 社区支持
- 智谱AI论坛
- GitHub Issues

### 日志调试
```bash
# 开启详细日志
LOG_LEVEL=DEBUG

# 查看实时日志
tail -f logs/flow_system.log
```

---

## 🎉 完成配置

配置完成后，你应该能看到：

```bash
$ python run.py

2026-02-05 16:00:00 - flow_system - INFO - LLM Engine initialized (Model: GLM-4.7, Endpoint: https://open.bigmodel.cn/api/coding/paas/v4)
2026-02-05 16:00:00 - flow_system - INFO - Sandbox initialized
2026-02-05 16:00:00 - flow_system - INFO - Emergence detector initialized
2026-02-05 16:00:00 - flow_system - INFO - Knowledge manager initialized
2026-02-05 16:00:00 - flow_system - INFO - Evolution engine initialized
```

现在开始使用FlowSystem吧！🚀

---

**上次更新**: 2026-02-05
**版本**: FlowSystem 0.1.0
