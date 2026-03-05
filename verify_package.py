#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
双脑Ralph系统 v3.0 部署包验证脚本
Dual-Brain Ralph System v3.0 Package Verification Script

用法 / Usage:
    python verify_package.py [目标目录]

默认检查当前目录下的 "super system" 文件夹
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

# 设置Windows终端编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 颜色输出 (ANSI)
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

# 必需的文件清单
REQUIRED_FILES = {
    'root': [
        'brain_v3.py',
        'dealer_v3.py',
        'brain.py',
        'setup.py',
        'requirements.txt',
        'README.md',
        'DEPLOYMENT.md',
        'QUICK_START_V3.md',
    ],
    '.janus': [
        'core/__init__.py',
        'core/hippocampus.py',
        'core/router.py',
        'core/router_v2.py',
        'core/thinkbank.py',
        'core/validator.py',
        'core/cache_manager.py',
        'config.json',
        'ui_templates.py',
        'knowledge/index.json',
        'knowledge/python_web.json',
    ],
    '.janus/ui_library': [
        '__init__.py',
        'config.py',
        'components/__init__.py',
        'themes/__init__.py',
        'patterns/__init__.py',
    ],
    '.ralph': [
        'tools/tools_manager.py',
        'tools/memory_integrator.py',
        'tools/claude_mem_enhanced.py',
        'tools/config.json',
        'context/project-info.md',
        'context/architecture.md',
        'context/coding-style.md',
        'PROMPT_V3.md',
    ],
    '.ralph/tools': [
        'tools_manager.py',
        'memory_integrator.py',
        'claude_mem_enhanced.py',
        'drawio_mcp_client.py',
        'session_hooks.py',
        'parallel_brain.py',
        'parallel_executor.py',
        'config.json',
        'superpowers_rules.md',
    ],
}

# 排除的文件/目录
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.pyc',
    '.git',
]

def print_header(text: str):
    """打印标题"""
    print(f"\n{Colors.BLUE}{'='*50}{Colors.NC}")
    print(f"{Colors.BLUE}{text}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}\n")

def print_success(text: str):
    """打印成功消息"""
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")

def print_error(text: str):
    """打印错误消息"""
    print(f"{Colors.RED}✗ {text}{Colors.NC}")

def print_warning(text: str):
    """打印警告消息"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.NC}")

def check_file(base_path: Path, relative_path: str) -> bool:
    """检查文件是否存在"""
    file_path = base_path / relative_path
    return file_path.is_file()

def check_dir(base_path: Path, relative_path: str) -> bool:
    """检查目录是否存在"""
    dir_path = base_path / relative_path
    return dir_path.is_dir()

def verify_package(target_dir: str) -> Tuple[int, int, List[str]]:
    """
    验证部署包

    返回: (通过数量, 失败数量, 缺失文件列表)
    """
    base_path = Path(target_dir)

    if not base_path.exists():
        print_error(f"目录不存在: {target_dir}")
        return 0, 0, []

    passed = 0
    failed = 0
    missing_files = []

    print_header("验证部署包结构")

    # 检查根目录文件
    print(f"{Colors.YELLOW}检查根目录文件...{Colors.NC}")
    for file_path in REQUIRED_FILES['root']:
        if check_file(base_path, file_path):
            print_success(f"  {file_path}")
            passed += 1
        else:
            print_error(f"  {file_path} (缺失)")
            failed += 1
            missing_files.append(file_path)

    # 检查.janus目录
    print(f"\n{Colors.YELLOW}检查.janus目录...{Colors.NC}")
    if check_dir(base_path, '.janus'):
        print_success("  .janus/ 目录存在")
        for file_path in REQUIRED_FILES['.janus']:
            if check_file(base_path, '.janus/' + file_path):
                print_success(f"  .janus/{file_path}")
                passed += 1
            else:
                print_warning(f"  .janus/{file_path} (可选)")
    else:
        print_error("  .janus/ 目录缺失")
        failed += 1
        missing_files.append('.janus/')

    # 检查.janus/ui_library
    print(f"\n{Colors.YELLOW}检查.janus/ui_library目录...{Colors.NC}")
    if check_dir(base_path, '.janus/ui_library'):
        print_success("  .janus/ui_library/ 目录存在")
        for file_path in REQUIRED_FILES['.janus/ui_library']:
            if check_file(base_path, '.janus/ui_library/' + file_path):
                print_success(f"  .janus/ui_library/{file_path}")
                passed += 1
            else:
                print_warning(f"  .janus/ui_library/{file_path} (可选)")
    else:
        print_warning("  .janus/ui_library/ 目录不存在 (可选)")

    # 检查.ralph目录
    print(f"\n{Colors.YELLOW}检查.ralph目录...{Colors.NC}")
    if check_dir(base_path, '.ralph'):
        print_success("  .ralph/ 目录存在")
        for file_path in REQUIRED_FILES['.ralph']:
            if check_file(base_path, '.ralph/' + file_path):
                print_success(f"  .ralph/{file_path}")
                passed += 1
            else:
                print_warning(f"  .ralph/{file_path} (可选)")

        # 检查tools子目录
        if check_dir(base_path, '.ralph/tools'):
            print_success("  .ralph/tools/ 目录存在")
            for file_path in REQUIRED_FILES['.ralph/tools']:
                if check_file(base_path, '.ralph/tools/' + file_path):
                    print_success(f"  .ralph/tools/{file_path}")
                    passed += 1
                else:
                    print_warning(f"  .ralph/tools/{file_path} (可选)")
    else:
        print_error("  .ralph/ 目录缺失")
        failed += 1
        missing_files.append('.ralph/')

    # 检查是否有不需要的文件
    print(f"\n{Colors.YELLOW}检查排除项...{Colors.NC}")

    pycache_count = 0
    for pycache in base_path.rglob('__pycache__'):
        if pycache.is_dir():
            pycache_count += 1

    if pycache_count > 0:
        print_warning(f"  发现 {pycache_count} 个 __pycache__ 目录 (应删除)")
        failed += pycache_count
    else:
        print_success("  未发现 __pycache__ 目录")

    # 统计文件数量
    print(f"\n{Colors.YELLOW}文件统计...{Colors.NC}")
    py_files = list(base_path.rglob('*.py'))
    md_files = list(base_path.rglob('*.md'))
    json_files = list(base_path.rglob('*.json'))

    print(f"  Python文件: {len(py_files)}")
    print(f"  文档文件: {len(md_files)}")
    print(f"  配置文件: {len(json_files)}")

    return passed, failed, missing_files

def main():
    """主函数"""
    # 获取目标目录
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = "super system"

    print_header("双脑Ralph系统 v3.0 部署包验证")
    print(f"目标目录: {target_dir}\n")

    passed, failed, missing = verify_package(target_dir)

    # 打印总结
    print_header("验证结果")

    total = passed + failed
    if total > 0:
        pass_rate = (passed / total) * 100
        print(f"通过: {passed}/{total} ({pass_rate:.1f}%)")
        print(f"失败: {failed}/{total}")

    if failed == 0:
        print(f"\n{Colors.GREEN}✓ 部署包验证通过！{Colors.NC}")
        print(f"{Colors.GREEN}✓ Package verification passed!{Colors.NC}")
        return 0
    else:
        print(f"\n{Colors.RED}✗ 发现 {failed} 个问题{Colors.NC}")
        if missing:
            print(f"\n{Colors.RED}缺失的关键文件:{Colors.NC}")
            for f in missing:
                print(f"  - {f}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
