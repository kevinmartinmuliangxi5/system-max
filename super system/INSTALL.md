# 双脑Ralph系统 v3.0 快速安装指南

**5分钟安装并开始使用**

---

## 📦 系统内容

本部署包包含双脑Ralph系统v3.0完整版的所有核心文件：

- **54个** Python模块文件
- **20个** 文档文件
- **8个** 配置文件
- **84个** 总文件数

---

## 🚀 快速安装 (3步)

### Step 1: 安装依赖

```bash
pip install -r requirements.txt
```

**最小安装** (仅核心功能):
```bash
pip install jieba anthropic pyperclip colorama requests
```

### Step 2: 验证安装

```bash
python .ralph/tools/tools_manager.py
```

**预期输出**:
```
启用的工具:
  ✓ superpowers
  ✓ claude_mem
  ✓ frontend_design
  ✓ drawio_mcp
  ✓ compound_engineering
  ✓ speckit
```

如果看到上述输出，说明安装成功！✅

### Step 3: 开始使用

```bash
# 方式1: 单任务模式
python brain_v3.py "实现用户登录功能"

# 方式2: 交互式模式
python brain_v3.py
```

---

## 📚 文档导航

### 新用户必读

1. **[README.md](README.md)** - 系统概述和基本使用
2. **[QUICK_START_V3.md](QUICK_START_V3.md)** - 5分钟快速上手
3. **[DEPLOYMENT.md](DEPLOYMENT.md)** - 详细部署指南

### 技术文档

4. **[.ralph/context/architecture.md](.ralph/context/architecture.md)** - 系统架构
5. **[.ralph/context/coding-style.md](.ralph/context/coding-style.md)** - 编码规范
6. **[.ralph/docs/tools-integration-analysis.md](.ralph/docs/tools-integration-analysis.md)** - 工具集成分析

### 打包信息

7. **[PACKAGE_MANIFEST.md](PACKAGE_MANIFEST.md)** - 打包清单
8. **[PACKAGE_COMPLETE_REPORT.md](PACKAGE_COMPLETE_REPORT.md)** - 最终打包报告

---

## 🎯 核心功能

### v3.0 新增能力

- ✅ **智能需求分析** - Compound Engineering方法论
- ✅ **规格驱动开发** - SpecKit自动生成规格
- ✅ **双记忆体系** - Hippocampus + claude-mem
- ✅ **质量自动保证** - Superpowers质量纪律
- ✅ **前端审美提升** - frontend-design指导
- ✅ **流程可视化** - draw.io MCP绘图
- ✅ **结构化上下文** - Context Engineering

---

## 🔧 配置说明

### API配置 (可选)

编辑 `.janus/config.json`:

```json
{
  "ZHIPU_API_KEY": "your_api_key_here",
  "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7"
}
```

> **注意**: API配置是可选的。不配置时系统将使用基础功能。

### 工具配置

编辑 `.ralph/tools/config.json`:

```json
{
  "tools": {
    "superpowers": {
      "enabled": true
    },
    "claude_mem": {
      "enabled": true
    }
  }
}
```

---

## 📋 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows / Linux / macOS
- **内存**: 建议 4GB 以上
- **硬盘**: 至少 100MB 可用空间

---

## 🐛 常见问题

### Q1: ImportError 怎么办？

```bash
# 确保依赖已安装
pip install -r requirements.txt
```

### Q2: 中文显示乱码？

```bash
# Windows
chcp 65001

# Linux/Mac
export LANG=zh_CN.UTF-8
```

### Q3: 工具无法加载？

这是正常的降级行为。系统会自动使用基础功能。

---

## ✅ 验证清单

安装完成后，请验证以下项目：

- [ ] Python版本 >= 3.8
- [ ] 所有依赖已安装 (`pip list`)
- [ ] 工具管理器运行正常
- [ ] Brain v3可以正常启动
- [ ] 终端中文显示正常

---

## 🎉 安装完成

**恭喜！双脑Ralph系统v3.0已安装成功！**

### 下一步

1. 阅读 [QUICK_START_V3.md](QUICK_START_V3.md) 了解基础用法
2. 使用Brain v3规划第一个任务
3. 查看 [README.md](README.md) 了解详细功能

---

**版本**: v3.0.0-complete
**安装日期**: 2026-02-11
**打包状态**: ✅ 验证通过 (41/41, 100%)

**让AI开发更智能、更高效！** 🚀✨
