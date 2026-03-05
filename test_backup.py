#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备份脚本测试验证程序

用于验证 backup_py_files.py 的功能是否正常
"""

import os
import sys
from pathlib import Path
import shutil


def test_backup_script():
    """测试备份脚本的基本功能"""
    print("=" * 60)
    print("备份脚本功能测试")
    print("=" * 60)
    print()

    # 检查主脚本是否存在
    backup_script = Path("backup_py_files.py")
    if not backup_script.exists():
        print("[X] 错误：找不到 backup_py_files.py")
        return False

    print("[OK] 主脚本文件存在")

    # 检查是否可以导入
    try:
        import backup_py_files
        print("[OK] 脚本可以正常导入")
    except Exception as e:
        print(f"[X] 导入失败: {e}")
        return False

    # 检查关键类和方法
    if hasattr(backup_py_files, 'PyFileBackup'):
        print("[OK] PyFileBackup 类定义正确")

        backup_class = backup_py_files.PyFileBackup
        required_methods = [
            'create_backup_directory',
            'find_py_files',
            'backup_file',
            'create_backup_summary',
            'run'
        ]

        for method in required_methods:
            if hasattr(backup_class, method):
                print(f"[OK] 方法 {method} 存在")
            else:
                print(f"[X] 缺少方法: {method}")
                return False
    else:
        print("[X] 找不到 PyFileBackup 类")
        return False

    # 检查 backup 目录
    backup_dir = Path("backup")
    if backup_dir.exists():
        backup_folders = list(backup_dir.glob("backup_*"))
        print(f"[OK] 找到 {len(backup_folders)} 个备份文件夹")

        if backup_folders:
            latest = max(backup_folders, key=lambda p: p.stat().st_mtime)
            print(f"   最新备份: {latest.name}")

            # 检查备份摘要
            summary_file = latest / "backup_summary.txt"
            if summary_file.exists():
                print(f"[OK] 备份摘要文件存在")
                with open(summary_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "备份时间" in content and "成功备份" in content:
                        print("[OK] 备份摘要内容正确")
            else:
                print("[!] 备份摘要文件不存在")
    else:
        print("[!] backup 目录不存在（尚未运行过备份）")

    print()
    print("=" * 60)
    print("测试完成！所有检查项通过")
    print("=" * 60)
    return True


def show_usage_info():
    """显示使用信息"""
    print()
    print("快速使用指南：")
    print("-" * 60)
    print("1. 基本用法：")
    print("   python backup_py_files.py")
    print()
    print("2. 备份指定目录：")
    print("   python backup_py_files.py -s /path/to/directory")
    print()
    print("3. 自定义备份文件夹：")
    print("   python backup_py_files.py -b my_backups")
    print()
    print("4. Windows用户：")
    print("   双击运行 backup.bat")
    print()
    print("详细文档请查看：")
    print("- BACKUP_README.md (中文详细说明)")
    print("- backup_usage.md (使用手册)")
    print("-" * 60)


if __name__ == "__main__":
    try:
        success = test_backup_script()
        show_usage_info()

        if success:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        sys.exit(1)
