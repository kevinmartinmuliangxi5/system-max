#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
并行Brain执行器

支持多个任务同时规划，提升Brain处理效率
"""

import sys
import json
from pathlib import Path
from typing import List, Dict

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from parallel_executor import get_parallel_executor


class ParallelBrain:
    """并行Brain规划器"""

    def __init__(self, mode: str = "sequential"):
        """
        初始化

        Args:
            mode: 执行模式 (sequential/tmux/openclaw)
        """
        self.executor = get_parallel_executor(mode)
        self.mode = mode

    def plan_tasks_parallel(self, tasks: List[str]) -> Dict:
        """
        并行规划多个任务

        Args:
            tasks: 任务描述列表

        Returns:
            规划结果
        """
        print(f"\n🧠 并行Brain模式: {len(tasks)}个任务")

        # 添加所有Brain任务
        for i, task in enumerate(tasks):
            task_id = f"brain-{i+1}"
            command = f'python brain_v3.py "{task}"'
            description = f"规划任务: {task[:50]}..."

            self.executor.add_task(task_id, command, description)

        # 执行
        results = self.executor.execute()

        # 打印摘要
        self.executor.print_summary()

        # 汇总蓝图
        blueprints = self._collect_blueprints(results)

        return {
            "mode": self.mode,
            "tasks": len(tasks),
            "results": results,
            "blueprints": blueprints
        }

    def _collect_blueprints(self, results: Dict) -> List[Dict]:
        """
        收集所有生成的蓝图

        Args:
            results: 执行结果

        Returns:
            蓝图列表
        """
        blueprints = []

        # 读取蓝图文件
        blueprint_file = Path(".janus/project_state.json")

        if blueprint_file.exists():
            with open(blueprint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                blueprints = data.get("blueprint", [])

        return blueprints


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="并行Brain规划器")
    parser.add_argument(
        "tasks",
        nargs="+",
        help="任务描述列表"
    )
    parser.add_argument(
        "--mode",
        choices=["sequential", "tmux", "openclaw"],
        default="sequential",
        help="执行模式"
    )

    args = parser.parse_args()

    # 创建并行Brain
    pbrain = ParallelBrain(mode=args.mode)

    # 并行规划
    result = pbrain.plan_tasks_parallel(args.tasks)

    print(f"\n✅ 并行规划完成")
    print(f"   生成蓝图数: {len(result['blueprints'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
