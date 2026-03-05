# 🚀 快速开始指南

**5分钟上手 system-pro**

---

## Step 1: 验证包完整性（30秒）

```bash
cd system-pro
python verify_package.py
```

看到这个说明包完好：
```
✅ 包验证通过！所有必需文件都存在。
必需文件: 13/13 (100%)
```

---

## Step 2: 部署到项目（1分钟）

### 选项 A: 部署到当前目录

```bash
cd /your/project
python /path/to/system-pro/deploy.py
```

### 选项 B: 部署到指定目录

```bash
python /path/to/system-pro/deploy.py /target/project/dir
```

按照提示完成：
- 备份冲突文件？选 `1`（是）
- 输入 API Key？可以跳过（留空）
- 安装依赖？选 `y`（推荐）

---

## Step 3: 创建第一个任务（2分钟）

编辑 `.janus/project_state.json`:

```json
{
  "blueprint": [
    {
      "task_name": "实现用户登录功能",
      "instruction": "创建认证模块，支持邮箱登录，使用JWT",
      "target_files": ["auth.py"],
      "status": "PENDING"
    }
  ]
}
```

---

## Step 4: 生成AI指令（10秒）

```bash
python dealer_enhanced.py
```

指令已自动复制到剪贴板！显示：
```
✅ 增强指令已复制到剪贴板
```

---

## Step 5: 使用指令（1分钟）

1. 打开 Claude Code
2. 粘贴指令（Ctrl+V / Cmd+V）
3. Claude Code 自动完成任务 ✨

---

## 🎉 完成！

你已经成功：
- ✅ 部署了系统
- ✅ 创建了任务
- ✅ 生成了AI指令
- ✅ 开始高效开发

---

## 📚 下一步

### 学习更多

- `README.md` - 完整功能说明
- `USAGE_EXAMPLES.md` - 详细使用示例

### 进阶使用

**存储经验**:
```python
from core.hippocampus import Hippocampus
hippo = Hippocampus()
hippo.store('优化性能', '添加Redis缓存')
```

**使用简化版**:
```bash
python dealer.py  # 快速简单任务
```

**验证系统**:
```bash
python quick_check.py
```

---

## 💡 提示

- 增强版 = 完整上下文，适合复杂任务
- 简化版 = 极简轻量，适合简单任务
- 记得存储重要经验到海马体

---

**开始享受高效开发吧！** 🚀
