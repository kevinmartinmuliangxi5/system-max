# 🚀 Ralph + 双脑系统 - 快速开始指南

**部署已完成！现在可以开始测试MVP了。**

---

## ✅ 系统状态

```
核心整合：已完成 ✅
  ├─ dealer_enhanced.py (支持 --ralph-mode)
  ├─ .ralph/PROMPT.md (双脑集成指令)
  └─ .ralphrc (双脑配置)

辅助脚本：已就绪 ✅
  ├─ start_ralph_with_zhipu.sh (Ralph启动 - 智普API)
  ├─ ralph_interactive.sh (交互式模式 ⭐推荐)
  ├─ monitor_ralph.sh (实时监控)
  ├─ verify_api_isolation.sh (API隔离验证)
  └─ quick_test.sh (环境验证)
```

---

## 📋 启动流程（3步）

### 第1步：验证环境（1分钟）

```bash
cd D:/AI_Projects/system-max
bash quick_test.sh
```

**预期结果：**
```
  通过: 9-10 / 10
  🎉 所有测试通过！系统已就绪
```

**如果有测试失败：**
- Claude Code未安装: `npm install -g @anthropic-ai/claude-code`
- jieba未安装: `pip install jieba`
- 智普API Key未配置: 编辑 `.janus/config.json`

---

### 第2步：Brain生成测试蓝图（3分钟）

**在当前终端（和Claude对话）：**

```
您: 你现在是Brain，帮我规划一个简单的测试任务：
    创建一个 greet.py 文件，包含 hello(name) 函数，
    返回 "Hello, {name}!"

Brain (Claude):
  🧠 Brain模式启动！
  [理解需求]
  [生成蓝图]
  ✅ 蓝图已保存到 .janus/project_state.json
```

**验证蓝图已生成：**

```bash
cat .janus/project_state.json
```

应该看到：
```json
{
  "blueprint": [
    {
      "task_name": "创建问候函数",
      "instruction": "创建 greet.py，实现 hello(name) 函数",
      "target_files": ["greet.py"],
      "status": "PENDING"
    }
  ]
}
```

---

### 第3步：启动Ralph测试（5-10分钟）

#### **方式A：交互式模式（推荐MVP测试）⭐**

**新开Git Bash终端：**

```bash
cd D:/AI_Projects/system-max
bash ralph_interactive.sh
```

**交互式特点：**
- ✅ 每轮后暂停，等待您的指令
- ✅ 可以查看Worker的每一步
- ✅ 可以随时提供反馈
- ✅ 完全可控

**可用命令：**
```
c / continue   → 继续下一轮
f / feedback   → 提供反馈意见
d / diff       → 查看代码差异
v / view       → 查看完整输出
q / quit       → 退出Ralph
```

---

#### **方式B：自动模式（适合简单任务）**

```bash
bash start_ralph_with_zhipu.sh --live --verbose
```

**自动模式特点：**
- ✅ 完全自动运行
- ✅ 显示详细日志
- ⚠️ 无法中途干预

---

#### **方式C：三分屏监控模式（适合观察）**

**使用Windows Terminal：**

1. **打开Windows Terminal**
2. **Alt + Shift + -** 横向分屏
3. **Alt + Shift + D** 纵向分屏（右下）

**设置3个面板：**

```bash
# 面板1 (上方) - Brain对话
cd D:/AI_Projects/system-max
# 正常和Claude对话

# 面板2 (左下) - Ralph执行
cd D:/AI_Projects/system-max
bash start_ralph_with_zhipu.sh --live --verbose

# 面板3 (右下) - 实时监控
cd D:/AI_Projects/system-max
bash monitor_ralph.sh
```

---

## 🎬 预期执行流程

### 交互式模式示例：

```
╔════════════════════════════════════════════════════════════╗
║  Ralph Interactive Mode - 交互式自主开发                   ║
╚════════════════════════════════════════════════════════════╝

📡 配置智普API...
  ✅ API配置完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 Loop 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 生成执行指令...
  ✅ 指令已生成

📋 当前任务: 创建问候函数

🤖 Worker执行中（智普API）...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 Worker输出：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

好的！我来创建 greet.py 文件。

[创建文件]

```python
def hello(name):
    """返回问候语"""
    return f"Hello, {name}!"
```

✅ greet.py 已创建

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏸️  暂停 - 请审查Worker的工作
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

可用命令：
  c / continue   → 继续下一轮
  f / feedback   → 提供反馈意见
  d / diff       → 查看代码差异
  v / view       → 查看完整输出
  s / skip       → 跳过当前任务
  q / quit       → 退出Ralph

👉 您的指令: d

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
diff --git a/greet.py b/greet.py
new file mode 100644
index 0000000..abcd123
--- /dev/null
+++ b/greet.py
@@ -0,0 +1,3 @@
+def hello(name):
+    """返回问候语"""
+    return f"Hello, {name}!"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 您的指令: c

  ✅ 继续下一轮...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 Loop 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 Worker检查任务...

✅ 任务已完成
<promise>COMPLETE</promise>

🎉 Ralph Interactive Mode 完成

📊 统计：
  总循环次数: 2
  输出日志: .ralph/loop_*.txt
```

---

## 🎯 成功标志

### 如果一切正常，您会看到：

1. ✅ **Dealer生成指令成功**
   - 文件：`.ralph/current_instruction.txt`
   - 包含任务详情和历史经验

2. ✅ **Worker执行任务成功**
   - 创建了 `greet.py` 文件
   - 代码正确且完整

3. ✅ **API隔离有效**
   - Brain终端使用Claude Pro API
   - Ralph终端使用智普API
   - 两者互不影响

4. ✅ **完成信号输出**
   - `<promise>COMPLETE</promise>`

---

## 🔍 验证结果

### 检查生成的文件：

```bash
# 查看生成的代码
cat greet.py

# 测试函数
python -c "from greet import hello; print(hello('World'))"
# 预期输出: Hello, World!
```

### 检查API使用情况：

```bash
# 查看Ralph日志
cat .ralph/live.log | grep "API"

# 应该看到：
# API Endpoint: https://open.bigmodel.cn/api/anthropic
# ✅ 说明使用的是智普API
```

---

## 🚨 故障排除

### 问题1：quick_test.sh 测试失败

```bash
# 检查Claude Code CLI
claude --version

# 如果没安装
npm install -g @anthropic-ai/claude-code

# 检查Python依赖
pip install jieba
```

### 问题2：蓝图生成失败

```bash
# 检查Brain是否正确理解任务
# 重新在Brain终端说：
您: "你现在是Brain，帮我规划任务..."
```

### 问题3：Ralph执行失败

```bash
# 检查指令文件是否存在
cat .ralph/current_instruction.txt

# 检查智普API配置
cat .janus/config.json | grep ZHIPU
```

### 问题4：API隔离问题

```bash
# 验证隔离
bash verify_api_isolation.sh

# 确保当前终端没有设置 ANTHROPIC_BASE_URL
echo $ANTHROPIC_BASE_URL
# 应该输出空白
```

---

## 📚 参考文档

- **Windows Terminal分屏指南**: `WINDOWS_TERMINAL_GUIDE.md`
- **三种模式对比**: `RALPH_MODES_COMPARISON.md`
- **API隔离验证**: 运行 `bash verify_api_isolation.sh`

---

## 🎊 下一步

### MVP测试成功后：

1. **尝试更复杂的任务**
   - 多文件项目
   - 包含测试的任务
   - 需要调试的任务

2. **体验三种模式**
   - 交互式：学习和把关
   - 自动式：简单任务
   - 监控式：观察进度

3. **验证记忆积累**
   - 查看海马体：`cat .janus/long_term_memory.json`
   - 运行类似任务，验证经验复用

---

## 💡 关键要点

✅ **API完全隔离**
  - Brain终端：Claude Pro API
  - Ralph终端：智普API（便宜4-7倍）

✅ **MVP推荐：交互式模式**
  - 可以看到每一步
  - 可以随时干预
  - 完全可控

✅ **持续优化**
  - 每次任务完成后存储经验
  - 海马体越来越智能
  - 预估越来越准确

---

**现在就开始测试吧！🚀**

有问题随时在Brain终端问我！
