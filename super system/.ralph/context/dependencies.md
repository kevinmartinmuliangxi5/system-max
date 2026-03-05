# 依赖说明文档

**项目**: 双脑Ralph系统 v3.0
**最后更新**: 2026-02-11

---

## 概述

本文档详细说明双脑Ralph系统v3.0的所有依赖项，包括核心依赖、可选依赖、开发依赖和外部服务依赖。

---

## 核心依赖

### Python运行时

| 名称 | 版本要求 | 用途 | 必需性 |
|------|---------|------|--------|
| Python | >= 3.8 | 系统运行时 | ✅ 必需 |

**安装方式**:
```bash
# Windows
choco install python --version=3.11

# Linux/macOS
sudo apt-get install python3.11  # Ubuntu/Debian
brew install python@3.11         # macOS
```

### Python包依赖

| 包名 | 版本 | 用途 | 必需性 | 安装 |
|------|------|------|--------|------|
| **pyperclip** | latest | 剪贴板操作 | ✅ 必需 | `pip install pyperclip` |
| **colorama** | latest | 终端彩色输出 | ⚠️ 推荐 | `pip install colorama` |
| **json** | stdlib | JSON处理 | ✅ 必需 | 内置 |
| **pathlib** | stdlib | 路径操作 | ✅ 必需 | 内置 |
| **re** | stdlib | 正则表达式 | ✅ 必需 | 内置 |

**安装所有依赖**:
```bash
pip install -r requirements.txt
```

**requirements.txt内容**:
```
pyperclip>=1.8.2
colorama>=0.4.6
```

---

## 可选依赖

### 增强功能依赖

| 包名 | 版本 | 用途 | 必需性 | 安装 |
|------|------|------|--------|------|
| **jieba** | latest | 中文分词（搜索增强） | 🔷 可选 | `pip install jieba` |
| **sentence-transformers** | latest | 向量化搜索 | 🔷 可选 | `pip install sentence-transformers` |
| **pytest** | >= 7.0 | 单元测试 | 🔷 可选 | `pip install pytest` |
| **flake8** | latest | 代码检查 | 🔷 可选 | `pip install flake8` |

**增强安装**:
```bash
pip install -r requirements-enhanced.txt
```

**requirements-enhanced.txt内容**:
```
jieba>=0.42
pytest>=7.0
flake8>=6.0
```

---

## 外部工具依赖

### MCP Servers (Model Context Protocol)

| 工具 | 版本 | 用途 | 必需性 | 文档 |
|------|------|------|--------|------|
| **pencil MCP** | latest | .pen设计文件操作 | 🔷 可选 | 内置 |
| **web-search-prime** | latest | 网络搜索 | 🔷 可选 | 内置 |
| **web-reader** | latest | 网页内容读取 | 🔷 可选 | 内置 |
| **zread** | latest | GitHub仓库读取 | 🔷 可选 | 内置 |
| **zai-mcp-server** | latest | AI图像分析 | 🔷 可选 | 内置 |
| **draw.io MCP** | latest | 流程图生成 | 🔷 可选 | [安装说明](#drawio-mcp-安装) |

**说明**: 这些MCP工具已在Claude Code中集成，无需单独安装。

### Claude Code CLI

| 名称 | 版本 | 用途 | 必需性 | 安装 |
|------|------|------|--------|------|
| **Claude Code** | latest | AI开发助手 | ✅ 必需 | [官方安装](https://claude.ai/claude-code) |

**安装方式**:
```bash
# 从官网下载安装包
# Windows: Claude-Code-Setup.exe
# macOS: Claude-Code.dmg
# Linux: Claude-Code.AppImage
```

---

## 开发依赖

### 测试工具

| 包名 | 版本 | 用途 | 安装 |
|------|------|------|------|
| **pytest** | >= 7.0 | 单元测试框架 | `pip install pytest` |
| **pytest-cov** | latest | 测试覆盖率 | `pip install pytest-cov` |
| **mock** | stdlib | 单元测试mock | 内置 (unittest.mock) |

### 代码质量工具

| 包名 | 版本 | 用途 | 安装 |
|------|------|------|------|
| **flake8** | latest | Python代码检查 | `pip install flake8` |
| **black** | latest | 代码格式化 | `pip install black` |
| **mypy** | latest | 类型检查 | `pip install mypy` |

### 文档工具

| 包名 | 版本 | 用途 | 安装 |
|------|------|------|------|
| **mkdocs** | latest | 文档生成 | `pip install mkdocs` |
| **mkdocs-material** | latest | 文档主题 | `pip install mkdocs-material` |

**开发依赖安装**:
```bash
pip install -r requirements-dev.txt
```

**requirements-dev.txt内容**:
```
pytest>=7.0
pytest-cov>=4.0
flake8>=6.0
black>=23.0
mypy>=1.0
mkdocs>=1.5
mkdocs-material>=9.0
```

---

## 系统依赖

### 操作系统要求

| 系统 | 版本 | 支持状态 | 说明 |
|------|------|---------|------|
| **Windows** | 10/11 | ✅ 完全支持 | 推荐使用PowerShell 7+ |
| **macOS** | 11+ | ✅ 完全支持 | 需要Xcode Command Line Tools |
| **Linux** | Ubuntu 20.04+ | ✅ 完全支持 | 其他发行版需测试 |

### 系统工具

| 工具 | 版本 | 用途 | 必需性 | 安装 |
|------|------|------|--------|------|
| **Git** | >= 2.30 | 版本控制 | ✅ 必需 | [git-scm.com](https://git-scm.com/) |
| **tmux** | >= 3.0 | 终端复用 (并行执行) | 🔷 可选 | `apt install tmux` / `brew install tmux` |

---

## 可选服务依赖

### OpenClaw (24/7任务调度)

**状态**: Phase 6待集成

**依赖**:
- Node.js >= 16
- npm >= 8

**安装方式**:
```bash
# 安装OpenClaw
npm install -g openclaw

# 配置
openclaw init

# 启动
openclaw start
```

**用途**: 实现24/7后台任务调度和多Worker并行执行

**必需性**: 🔷 可选（并行执行功能需要）

### draw.io MCP Server

**状态**: Phase 7待集成

**依赖**:
- Node.js >= 16
- draw.io Desktop或Web版本

**安装方式**:
```bash
# 安装MCP server
npm install -g @drawio/mcp-server

# 配置
drawio-mcp configure

# 启动
drawio-mcp start
```

**用途**: 自动生成架构图、流程图、UML图

**必需性**: 🔷 可选（可视化功能需要）

---

## 依赖关系图

```
双脑Ralph系统 v3.0
│
├─ 核心运行时
│  ├─ Python >= 3.8 (必需)
│  ├─ pyperclip (必需)
│  └─ colorama (推荐)
│
├─ 内部模块
│  ├─ .janus/core/
│  │  ├─ hippocampus.py
│  │  ├─ router.py
│  │  ├─ thinkbank.py
│  │  └─ cache_manager.py
│  │
│  └─ .ralph/tools/
│     ├─ tools_manager.py
│     ├─ memory_integrator.py
│     ├─ claude_mem_enhanced.py
│     └─ session_hooks.py
│
├─ MCP工具 (内置)
│  ├─ pencil MCP
│  ├─ web-search-prime
│  ├─ web-reader
│  ├─ zread
│  └─ zai-mcp-server
│
├─ 可选增强
│  ├─ jieba (中文分词)
│  ├─ sentence-transformers (向量搜索)
│  ├─ OpenClaw (并行执行)
│  └─ draw.io MCP (可视化)
│
└─ 开发工具
   ├─ pytest (测试)
   ├─ flake8 (检查)
   ├─ black (格式化)
   └─ mkdocs (文档)
```

---

## 依赖检查脚本

### check_dependencies.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""依赖检查脚本"""

import sys
import importlib

def check_dependency(module_name, optional=False):
    """检查依赖是否安装"""
    try:
        importlib.import_module(module_name)
        status = "✓"
        color = "\033[92m"  # 绿色
    except ImportError:
        if optional:
            status = "○"
            color = "\033[93m"  # 黄色
        else:
            status = "✗"
            color = "\033[91m"  # 红色

    reset = "\033[0m"
    opt_text = " (可选)" if optional else ""
    print(f"{color}{status}{reset} {module_name}{opt_text}")

    return status == "✓" if not optional else True

def main():
    print("="*60)
    print("双脑Ralph系统 v3.0 - 依赖检查")
    print("="*60)

    print("\n核心依赖:")
    core_ok = True
    core_ok &= check_dependency("json")
    core_ok &= check_dependency("pathlib")
    core_ok &= check_dependency("re")
    core_ok &= check_dependency("pyperclip")

    print("\n推荐依赖:")
    check_dependency("colorama", optional=True)

    print("\n可选增强:")
    check_dependency("jieba", optional=True)
    check_dependency("pytest", optional=True)
    check_dependency("flake8", optional=True)

    print("\n内部模块:")
    sys.path.insert(0, ".janus")
    check_dependency("core.hippocampus", optional=True)
    check_dependency("core.router", optional=True)

    sys.path.insert(0, ".ralph/tools")
    check_dependency("tools_manager", optional=True)
    check_dependency("memory_integrator", optional=True)

    print("\n" + "="*60)
    if core_ok:
        print("✓ 核心依赖满足，系统可以运行")
    else:
        print("✗ 核心依赖缺失，请安装必需的包")
        print("\n安装命令:")
        print("  pip install pyperclip colorama")
    print("="*60)

    return 0 if core_ok else 1

if __name__ == "__main__":
    sys.exit(main())
```

**使用方式**:
```bash
python .ralph/scripts/check_dependencies.py
```

---

## 依赖安装指南

### 最小安装 (核心功能)

```bash
# 1. 克隆仓库
git clone <repository-url>
cd system-max

# 2. 安装Python依赖
pip install pyperclip colorama

# 3. 验证安装
python .ralph/scripts/check_dependencies.py

# 4. 运行测试
python brain_v3.py "测试任务"
```

### 完整安装 (所有功能)

```bash
# 1. 克隆仓库
git clone <repository-url>
cd system-max

# 2. 安装所有依赖
pip install -r requirements.txt
pip install -r requirements-enhanced.txt
pip install -r requirements-dev.txt

# 3. 安装可选工具
# OpenClaw (并行执行)
npm install -g openclaw

# draw.io MCP (可视化)
npm install -g @drawio/mcp-server

# 4. 验证安装
python .ralph/scripts/check_dependencies.py

# 5. 运行完整测试
pytest tests/ -v --cov
```

---

## 依赖更新策略

### 版本锁定

**生产环境**: 使用精确版本号
```
pyperclip==1.8.2
colorama==0.4.6
```

**开发环境**: 使用最低版本要求
```
pyperclip>=1.8.2
colorama>=0.4.6
```

### 更新命令

```bash
# 检查过时的包
pip list --outdated

# 更新单个包
pip install --upgrade pyperclip

# 更新所有包
pip install --upgrade -r requirements.txt
```

### 兼容性测试

每次更新依赖后运行：
```bash
# 1. 运行测试套件
pytest tests/ -v

# 2. 检查代码质量
flake8 .

# 3. 类型检查
mypy .

# 4. 集成测试
python .ralph/tools/test_phase3.py
python .ralph/tools/test_dealer_v3.py
```

---

## 依赖问题排查

### 常见问题

#### 1. ImportError: No module named 'xxx'

**原因**: 依赖包未安装
**解决**:
```bash
pip install xxx
```

#### 2. ModuleNotFoundError: No module named '.janus'

**原因**: Python路径未正确设置
**解决**:
```python
import sys
sys.path.insert(0, ".janus")
```

#### 3. pyperclip.PyperclipException

**原因**: 剪贴板访问权限问题（Linux）
**解决**:
```bash
# Ubuntu/Debian
sudo apt-get install xclip

# Fedora
sudo dnf install xclip
```

#### 4. colorama不工作（Windows）

**原因**: 终端不支持ANSI颜色
**解决**:
```python
from colorama import init
init(autoreset=True)
```

---

## 依赖维护清单

### 定期检查 (每月)

- [ ] 检查依赖包更新
- [ ] 测试兼容性
- [ ] 更新requirements.txt
- [ ] 更新文档

### 重大更新 (每季度)

- [ ] Python版本升级测试
- [ ] 依赖大版本升级
- [ ] 性能基准测试
- [ ] 文档全面更新

### 安全审计 (每半年)

- [ ] 安全漏洞扫描
- [ ] 依赖许可证审查
- [ ] 过时包清理
- [ ] 供应链安全检查

---

## 总结

双脑Ralph系统v3.0的依赖设计遵循以下原则：

1. **最小化核心依赖** - 仅pyperclip为必需第三方包
2. **渐进式增强** - 高级功能依赖可选
3. **标准库优先** - 尽量使用Python标准库
4. **清晰文档** - 每个依赖说明用途和必需性
5. **自动检查** - 提供依赖检查脚本

这确保了系统易于安装、维护和扩展。

---

**维护说明**:
- 添加新依赖时更新本文档
- 更新依赖版本后测试兼容性
- 定期审查依赖必要性
- 保持requirements.txt同步

**最后更新**: 2026-02-11
**版本**: v3.0.0-alpha
