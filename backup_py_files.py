#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python文件自动备份脚本

功能：
- 自动备份指定目录下的所有.py文件
- 在backup文件夹中创建带时间戳的备份
- 支持递归遍历子目录
- 完善的异常处理和日志记录
"""

import os
import shutil
import datetime
import logging
from pathlib import Path
from typing import List, Tuple


class PyFileBackup:
    """Python文件备份工具类"""

    def __init__(self, source_dir: str = ".", backup_dir: str = "backup"):
        """
        初始化备份工具

        Args:
            source_dir: 源目录路径，默认为当前目录
            backup_dir: 备份目录名称，默认为 'backup'
        """
        self.source_dir = Path(source_dir).resolve()
        self.backup_dir = self.source_dir / backup_dir
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # 配置日志
        self._setup_logging()

    def _setup_logging(self):
        """配置日志系统"""
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(f"backup_{self.timestamp}.log", encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def create_backup_directory(self) -> Path:
        """
        创建带时间戳的备份目录

        Returns:
            创建的备份目录路径

        Raises:
            OSError: 创建目录失败时抛出
        """
        timestamped_backup_dir = self.backup_dir / f"backup_{self.timestamp}"

        try:
            timestamped_backup_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"备份目录创建成功: {timestamped_backup_dir}")
            return timestamped_backup_dir
        except OSError as e:
            self.logger.error(f"创建备份目录失败: {e}")
            raise

    def find_py_files(self) -> List[Path]:
        """
        递归查找所有.py文件

        Returns:
            找到的所有.py文件路径列表
        """
        py_files = []

        try:
            # 使用rglob递归查找所有.py文件
            for py_file in self.source_dir.rglob("*.py"):
                # 排除backup目录中的文件
                if "backup" not in py_file.parts:
                    py_files.append(py_file)

            self.logger.info(f"找到 {len(py_files)} 个Python文件")
            return py_files

        except Exception as e:
            self.logger.error(f"查找Python文件时出错: {e}")
            return []

    def backup_file(self, file_path: Path, backup_root: Path) -> bool:
        """
        备份单个文件，保持目录结构

        Args:
            file_path: 源文件路径
            backup_root: 备份根目录

        Returns:
            备份是否成功
        """
        try:
            # 计算相对路径
            relative_path = file_path.relative_to(self.source_dir)

            # 构建目标路径
            dest_path = backup_root / relative_path

            # 创建目标目录
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # 复制文件
            shutil.copy2(file_path, dest_path)

            # 获取文件大小
            file_size = file_path.stat().st_size
            self.logger.info(
                f"备份成功: {relative_path} ({file_size} bytes)"
            )
            return True

        except Exception as e:
            self.logger.error(f"备份文件失败 {file_path}: {e}")
            return False

    def create_backup_summary(self, backup_root: Path,
                            success_count: int,
                            fail_count: int,
                            total_size: int):
        """
        创建备份摘要文件

        Args:
            backup_root: 备份根目录
            success_count: 成功备份的文件数
            fail_count: 失败的文件数
            total_size: 总文件大小（字节）
        """
        summary_file = backup_root / "backup_summary.txt"

        try:
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("Python文件备份摘要\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"备份时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"源目录: {self.source_dir}\n")
                f.write(f"备份目录: {backup_root}\n\n")
                f.write(f"成功备份: {success_count} 个文件\n")
                f.write(f"失败: {fail_count} 个文件\n")
                f.write(f"总大小: {total_size / 1024:.2f} KB ({total_size} bytes)\n")
                f.write("\n" + "=" * 60 + "\n")

            self.logger.info(f"备份摘要已保存到: {summary_file}")

        except Exception as e:
            self.logger.error(f"创建备份摘要失败: {e}")

    def run(self) -> Tuple[int, int]:
        """
        执行备份操作

        Returns:
            (成功数, 失败数) 元组
        """
        self.logger.info("=" * 60)
        self.logger.info("开始Python文件备份任务")
        self.logger.info("=" * 60)
        self.logger.info(f"源目录: {self.source_dir}")

        try:
            # 创建备份目录
            backup_root = self.create_backup_directory()

            # 查找所有.py文件
            py_files = self.find_py_files()

            if not py_files:
                self.logger.warning("未找到任何Python文件，备份终止")
                return (0, 0)

            # 执行备份
            success_count = 0
            fail_count = 0
            total_size = 0

            for py_file in py_files:
                if self.backup_file(py_file, backup_root):
                    success_count += 1
                    total_size += py_file.stat().st_size
                else:
                    fail_count += 1

            # 创建备份摘要
            self.create_backup_summary(backup_root, success_count, fail_count, total_size)

            # 输出结果
            self.logger.info("=" * 60)
            self.logger.info(f"备份完成！成功: {success_count}, 失败: {fail_count}")
            self.logger.info(f"总大小: {total_size / 1024:.2f} KB")
            self.logger.info(f"备份位置: {backup_root}")
            self.logger.info("=" * 60)

            return (success_count, fail_count)

        except Exception as e:
            self.logger.error(f"备份过程中发生错误: {e}")
            return (0, 0)


def main():
    """主函数"""
    import argparse

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description="自动备份指定目录下的所有.py文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python backup_py_files.py                          # 备份当前目录
  python backup_py_files.py -s /path/to/source       # 备份指定目录
  python backup_py_files.py -s . -b my_backup        # 自定义备份文件夹名称
        """
    )

    parser.add_argument(
        "-s", "--source",
        type=str,
        default=".",
        help="源目录路径（默认为当前目录）"
    )

    parser.add_argument(
        "-b", "--backup",
        type=str,
        default="backup",
        help="备份目录名称（默认为 'backup'）"
    )

    # 解析命令行参数
    args = parser.parse_args()

    try:
        # 创建备份工具实例并执行
        backup_tool = PyFileBackup(
            source_dir=args.source,
            backup_dir=args.backup
        )

        success, fail = backup_tool.run()

        # 根据结果设置退出码
        if fail > 0:
            exit(1)
        elif success == 0:
            exit(2)
        else:
            exit(0)

    except KeyboardInterrupt:
        print("\n\n备份被用户中断")
        exit(130)
    except Exception as e:
        print(f"\n发生未预期的错误: {e}")
        exit(1)


if __name__ == "__main__":
    main()
