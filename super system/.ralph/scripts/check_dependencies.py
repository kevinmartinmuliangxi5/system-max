#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""依赖检查脚本"""

import sys
import io
import importlib

# UTF-8 输出支持
if sys.platform == "win32":
    if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
