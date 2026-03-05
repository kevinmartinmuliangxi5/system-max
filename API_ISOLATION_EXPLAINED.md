# API 隔离机制详解

## 🎯 核心原理

### ✅ Brain 和 Ralph 使用完全独立的 API

```
┌─────────────────────────────────────────────────────────────┐
│  Brain 终端（当前对话）                                      │
│  ├─ API: Claude Pro (Anthropic 官方)                        │
│  ├─ 配置: ~/.claude/settings.json                          │
│  ├─ 环境变量: 无（使用默认 Claude Pro API）                 │
│  └─ 不读取 .janus/config.json ❌                            │
└─────────────────────────────────────────────────────────────┘

                         完全隔离 ✅

┌─────────────────────────────────────────────────────────────┐
│  Ralph 终端（Worker 执行）                                   │
│  ├─ API: 智普 API (GLM-4.7)                                 │
│  ├─ 配置: .janus/config.json                                │
│  ├─ 环境变量: 由 ralph_auto_stream.sh 临时设置              │
│  └─ 仅在脚本进程内生效 ✅                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 配置文件说明

### 1. `.janus/config.json` - Ralph Worker 配置

**作用：**
- ✅ 只被 Ralph 脚本读取
- ✅ 配置 Ralph Worker 使用的 API
- ❌ 不影响 Brain 对话

**内容：**
```json
{
  "ZHIPU_API_KEY": "your_zhipu_api_key",
  "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
  "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-4.7",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7",
  "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.5-air"
}
```

**谁使用它：**
- ✅ `ralph_auto_stream.sh` 脚本
- ✅ Ralph Worker 进程
- ❌ Brain 对话（完全不读取）

---

### 2. `~/.claude/settings.json` - Brain 配置

**作用：**
- ✅ Brain 对话的全局配置
- ✅ 使用 Claude Pro API（Anthropic 官方）
- ❌ 不读取 `.janus/config.json`

**内容示例：**
```json
{
  "env": {
    // 通常为空，使用默认 Claude Pro API
    // 或者配置 Anthropic 官方 API Key
  }
}
```

**谁使用它：**
- ✅ Brain 对话（当前终端）
- ✅ 所有直接使用 `claude` 命令的地方
- ❌ Ralph Worker（不读取）

---

## 🔐 隔离机制原理

### 环境变量的作用域

```bash
# Brain 终端（当前对话）
$ echo $ANTHROPIC_BASE_URL
  (空 - 使用 Claude Pro API)

# Ralph 终端（启动 ralph_auto_stream.sh）
$ bash ralph_auto_stream.sh
  ↓
  脚本内部：export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
  ↓
  只在脚本进程和子进程生效 ✅
  ↓
  脚本退出后，环境变量消失 ✅
  ↓
  不影响其他终端 ✅
```

**关键点：**
1. **进程级隔离** - 环境变量只在设置它的进程及其子进程中生效
2. **终端独立** - 不同终端的环境变量完全独立
3. **临时设置** - Ralph 脚本的环境变量在脚本退出后消失

---

## ✅ 验证 API 隔离

### 在 Brain 终端验证：

```bash
# 检查当前终端的 API 配置
echo "ANTHROPIC_BASE_URL: $ANTHROPIC_BASE_URL"
echo "ANTHROPIC_DEFAULT_SONNET_MODEL: $ANTHROPIC_DEFAULT_SONNET_MODEL"

# 应该输出空值，说明使用 Claude Pro API
```

### 在 Ralph 终端验证：

```bash
# 启动 Ralph
bash ralph_auto_stream.sh

# 脚本会显示：
# ✅ API Endpoint: https://open.bigmodel.cn/api/anthropic
# ✅ Opus Model: glm-4.7
# ✅ Sonnet Model: glm-4.7
# ✅ Haiku Model: glm-4.5-air
```

---

## 🎯 常见问题

### Q1：修改 `.janus/config.json` 会影响 Brain 吗？

**答案：不会！**

- `.janus/config.json` 只被 Ralph 脚本读取
- Brain 对话使用 `~/.claude/settings.json`
- 两者完全独立

### Q2：Ralph 脚本退出后，环境变量还在吗？

**答案：不在！**

- Ralph 脚本设置的环境变量是临时的
- 只在脚本进程内生效
- 脚本退出后，环境变量消失
- 不影响其他终端或进程

### Q3：如何确认 Brain 使用的是哪个 API？

**方法1：** 检查环境变量
```bash
echo $ANTHROPIC_BASE_URL
# 如果是空的 → Claude Pro API
# 如果有值 → 自定义 API
```

**方法2：** 检查配置文件
```bash
cat ~/.claude/settings.json
# 查看 env.ANTHROPIC_BASE_URL
# 如果没有或为空 → Claude Pro API
```

### Q4：为什么 Ralph 要使用智普 API？

**原因：**
1. **成本优势** - 智普 API 比 Claude Pro 便宜 4-7 倍
2. **用量增加** - GLM Coding Plan 提供 3 倍用量
3. **性能相当** - GLM-4.7 性能接近 Claude Sonnet
4. **Brain 高效** - Brain 规划用 Claude Pro，Worker 执行用智普 API

---

## 💡 最佳实践

### 推荐配置：

```
Brain 终端（规划）:
  ├─ API: Claude Pro (Anthropic)
  ├─ 用于: 理解需求、生成蓝图、复杂决策
  └─ 成本: 较高，但物有所值

Ralph 终端（执行）:
  ├─ API: 智普 API (GLM-4.7)
  ├─ 用于: 代码编写、文件操作、重复任务
  └─ 成本: 便宜 4-7 倍，用量多 3 倍
```

### 隔离验证脚本：

我已经创建了 `verify_api_isolation.sh` 验证脚本：

```bash
bash verify_api_isolation.sh
```

它会自动检查：
1. Brain 终端的 API 配置
2. Ralph 配置文件是否存在
3. 环境变量隔离是否正确

---

## 📊 API 使用对比

| 场景 | API | 成本 | 用途 |
|------|-----|------|------|
| **Brain 对话** | Claude Pro | 标准 | 需求分析、架构设计 |
| **Ralph Worker** | 智普 GLM-4.7 | 1/4 - 1/7 | 代码实现、文件操作 |
| **总体效果** | 混合使用 | **节省 60-75%** | 完美平衡质量和成本 |

---

## 🎊 总结

### ✅ 安全保证：

1. **Brain 不受影响** - 修改 `.janus/config.json` 不影响 Brain 对话
2. **API 完全隔离** - Brain 和 Ralph 使用不同的 API
3. **进程级隔离** - Ralph 的环境变量不泄漏到其他进程
4. **配置独立** - 两套配置文件，互不干扰

### ✅ 使用建议：

- **放心修改** `.janus/config.json` 来配置 Ralph Worker
- **不要修改** `~/.claude/settings.json`（除非想改变 Brain 的 API）
- **验证隔离** 使用 `bash verify_api_isolation.sh`
- **查看成本** 在智普开放平台查看 API 用量统计

---

**结论：修改 `.janus/config.json` 是安全的，不会影响 Brain 使用 Claude Pro API！** ✅
