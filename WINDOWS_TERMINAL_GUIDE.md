# Windows Terminal 分屏使用指南

## 📺 三分屏布局（推荐）

```
┌─────────────────────────────────────────────┐
│  面板1: Brain (您和Claude对话)              │
│  - 使用Claude Pro API                       │
│  - 任务规划和代码审查                        │
├─────────────────────────────────────────────┤
│  面板2: Ralph Worker         │ 面板3: 监控  │
│  - 使用智普API               │ - 实时日志   │
│  - 自动执行任务              │ - 状态监控   │
└─────────────────────────────────────────────┘
```

## 🎯 设置步骤

### 第1步：打开Windows Terminal

```bash
# 方式1：Win + R
wt

# 方式2：开始菜单搜索 "Terminal"
```

### 第2步：创建布局

```bash
# 在Windows Terminal中按：

Alt + Shift + -    # 创建水平分屏（上下布局）
Alt + Shift + D    # 创建垂直分屏（左右布局）
```

### 第3步：设置各面板

#### **面板1 (上方) - Brain**

```bash
cd D:/AI_Projects/system-max

# 不设置任何环境变量
# 正常和Claude对话

您: 你现在是Brain，帮我规划任务...
```

#### **面板2 (左下) - Ralph Worker**

```bash
cd D:/AI_Projects/system-max

# 启动Ralph（智普API）
bash start_ralph_with_zhipu.sh --live --verbose
```

#### **面板3 (右下) - 实时监控**

```bash
cd D:/AI_Projects/system-max

# 方式1：实时日志
tail -f .ralph/live.log

# 方式2：状态监控（每2秒刷新）
watch -n 2 cat .ralph/status.json

# 方式3：组合监控
bash monitor_ralph.sh
```

## ⌨️ 快捷键速查

| 操作 | 快捷键 |
|------|--------|
| 横向分屏 | `Alt + Shift + D` |
| 纵向分屏 | `Alt + Shift + -` |
| 切换面板 | `Alt + ←/→/↑/↓` |
| 关闭面板 | `Ctrl + Shift + W` |
| 新标签页 | `Ctrl + Shift + T` |
| 调整面板大小 | `Alt + Shift + ←/→/↑/↓` |

## 🎨 优势

✅ **原生Windows**
  - 不需要安装额外软件
  - 性能好，资源占用少

✅ **同时监控多个视图**
  - Brain对话
  - Worker执行
  - 实时日志

✅ **比tmux更简单**
  - 图形化界面
  - 鼠标操作友好
  - 复制粘贴方便

## 📊 完整工作流

```bash
# 1. 打开Windows Terminal
wt

# 2. 创建布局（Alt + Shift + D / Alt + Shift + -）

# 3. 面板1：Brain规划
cd D:/AI_Projects/system-max
# 和Claude对话...

# 4. 面板2：Ralph执行
cd D:/AI_Projects/system-max
bash start_ralph_with_zhipu.sh --live --verbose

# 5. 面板3：监控
cd D:/AI_Projects/system-max
tail -f .ralph/live.log
```

## 🎬 效果演示

```
面板1 (Brain):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
您: 帮我实现用户登录功能
Brain: 好的！让我理解需求...
  1. 认证方式？
  2. Token类型？
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

面板2 (Ralph Worker):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Loop 1 Starting...
🔄 Calling Dealer...
✅ Instruction generated
🤖 Worker (智普API): 创建User模型...
[代码生成中...]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

面板3 (监控):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[14:23:15] API Request: POST /messages
[14:23:18] Response: 200 OK (3.2s)
[14:23:18] Tokens: 1,234 input / 2,567 output
[14:23:18] Cost: ¥0.15 ($0.02)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 💡 进阶技巧

### 保存布局

Windows Terminal支持保存自定义布局：

1. 设置 → 配置文件 → 默认值
2. 启动操作 → 添加分屏命令
3. 一键启动三分屏布局

### 自定义配色

```json
// settings.json
{
  "profiles": {
    "defaults": {
      "colorScheme": "One Half Dark",
      "fontSize": 11,
      "fontFace": "Cascadia Code"
    }
  }
}
```

## 🚨 故障排除

### 问题：tail -f 不工作

```bash
# 替代方案：
while true; do clear; cat .ralph/live.log | tail -20; sleep 1; done
```

### 问题：分屏布局乱了

```bash
# 重置：关闭所有面板，重新开始
Ctrl + Shift + W (多次)
```
