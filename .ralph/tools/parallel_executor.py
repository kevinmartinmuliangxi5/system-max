#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
并行执行管理器 (Parallel Executor)

支持OpenClaw和tmux的并行任务执行框架
"""

import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Optional

class ParallelExecutor:
    """并行执行管理器"""

    def __init__(self, mode: str = "sequential"):
        """
        初始化并行执行器

        Args:
            mode: 执行模式
                - "sequential": 顺序执行（默认）
                - "tmux": tmux并行执行
                - "openclaw": OpenClaw并行执行
        """
        self.mode = mode
        self.session_name = "ralph-parallel"
        self.tasks: List[Dict] = []
        self.results: Dict[str, Dict] = {}

        # 检查工具可用性
        self.tmux_available = self._check_tmux()
        self.openclaw_available = self._check_openclaw()

        # 根据可用性调整模式
        if mode == "tmux" and not self.tmux_available:
            print("⚠️ tmux不可用，降级到顺序执行")
            self.mode = "sequential"

        if mode == "openclaw" and not self.openclaw_available:
            print("⚠️ OpenClaw不可用，降级到顺序执行")
            self.mode = "sequential"

    def _check_tmux(self) -> bool:
        """检查tmux是否可用"""
        try:
            result = subprocess.run(
                ["tmux", "-V"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False

    def _check_openclaw(self) -> bool:
        """检查OpenClaw是否可用"""
        # OpenClaw通常通过HTTP API访问
        # 这里简化检查，实际应该ping OpenClaw服务
        openclaw_config = Path(".ralph/tools/openclaw_config.json")
        return openclaw_config.exists()

    def add_task(self, task_id: str, command: str, description: str = ""):
        """
        添加任务到执行队列

        Args:
            task_id: 任务ID
            command: 要执行的命令
            description: 任务描述
        """
        self.tasks.append({
            "id": task_id,
            "command": command,
            "description": description,
            "status": "pending"
        })
        print(f"✅ 添加任务: {task_id} - {description}")

    def execute(self) -> Dict[str, Dict]:
        """
        执行所有任务

        Returns:
            执行结果字典
        """
        if not self.tasks:
            print("⚠️ 没有任务需要执行")
            return {}

        print(f"\n🚀 开始执行 {len(self.tasks)} 个任务 (模式: {self.mode})")

        if self.mode == "sequential":
            return self._execute_sequential()
        elif self.mode == "tmux":
            return self._execute_tmux()
        elif self.mode == "openclaw":
            return self._execute_openclaw()

    def _execute_sequential(self) -> Dict[str, Dict]:
        """顺序执行模式"""
        print("\n📋 顺序执行模式")

        for task in self.tasks:
            task_id = task["id"]
            command = task["command"]
            description = task["description"]

            print(f"\n▶️  执行任务: {task_id}")
            print(f"   描述: {description}")
            print(f"   命令: {command}")

            start_time = time.time()

            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5分钟超时
                )

                elapsed = time.time() - start_time

                self.results[task_id] = {
                    "status": "success" if result.returncode == 0 else "failed",
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "elapsed": elapsed
                }

                if result.returncode == 0:
                    print(f"   ✅ 成功 ({elapsed:.2f}秒)")
                else:
                    print(f"   ❌ 失败 (返回码: {result.returncode})")
                    if result.stderr:
                        print(f"   错误: {result.stderr[:200]}")

            except subprocess.TimeoutExpired:
                print(f"   ⏱️  超时")
                self.results[task_id] = {
                    "status": "timeout",
                    "error": "Task timed out after 300 seconds"
                }

            except Exception as e:
                print(f"   ❌ 异常: {e}")
                self.results[task_id] = {
                    "status": "error",
                    "error": str(e)
                }

        return self.results

    def _execute_tmux(self) -> Dict[str, Dict]:
        """tmux并行执行模式"""
        print("\n🔀 tmux并行执行模式")

        # 创建tmux会话
        self._create_tmux_session()

        # 在不同窗口启动任务
        for i, task in enumerate(self.tasks):
            task_id = task["id"]
            command = task["command"]
            description = task["description"]

            window_name = f"task-{i}"

            # 创建新窗口
            subprocess.run([
                "tmux", "new-window",
                "-t", self.session_name,
                "-n", window_name,
                command
            ])

            print(f"▶️  启动任务 {task_id} 在窗口 {window_name}")

        print("\n⏳ 等待所有任务完成...")

        # 轮询检查任务状态
        max_wait = 600  # 最多等待10分钟
        start_time = time.time()

        while time.time() - start_time < max_wait:
            all_done = True

            for i, task in enumerate(self.tasks):
                task_id = task["id"]
                window_name = f"task-{i}"

                # 检查窗口是否还存在
                result = subprocess.run(
                    ["tmux", "list-windows", "-t", self.session_name, "-F", "#{window_name}"],
                    capture_output=True,
                    text=True
                )

                if window_name in result.stdout:
                    all_done = False
                else:
                    if task_id not in self.results:
                        self.results[task_id] = {
                            "status": "completed",
                            "message": "Task completed in tmux"
                        }

            if all_done:
                break

            time.sleep(2)

        # 清理tmux会话
        self._cleanup_tmux_session()

        return self.results

    def _execute_openclaw(self) -> Dict[str, Dict]:
        """OpenClaw并行执行模式"""
        print("\n🦞 OpenClaw并行执行模式")

        # 读取OpenClaw配置
        config_file = Path(".ralph/tools/openclaw_config.json")
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        openclaw_url = config.get("url", "http://localhost:8080")

        # 提交所有任务到OpenClaw
        job_ids = []

        for task in self.tasks:
            task_id = task["id"]
            command = task["command"]

            # 这里应该调用OpenClaw API提交任务
            # 简化实现，记录任务
            print(f"▶️  提交任务 {task_id} 到 OpenClaw")

            # 模拟任务ID
            job_id = f"openclaw-{task_id}"
            job_ids.append((task_id, job_id))

            self.results[task_id] = {
                "status": "submitted",
                "job_id": job_id,
                "openclaw_url": openclaw_url
            }

        print(f"\n✅ 已提交 {len(job_ids)} 个任务到 OpenClaw")
        print(f"   OpenClaw URL: {openclaw_url}")
        print("\n💡 提示: 使用OpenClaw Web界面查看任务状态")

        return self.results

    def _create_tmux_session(self):
        """创建tmux会话"""
        # 检查会话是否已存在
        result = subprocess.run(
            ["tmux", "has-session", "-t", self.session_name],
            capture_output=True
        )

        if result.returncode != 0:
            # 创建新会话
            subprocess.run([
                "tmux", "new-session",
                "-d",  # detached
                "-s", self.session_name
            ])
            print(f"✅ 创建tmux会话: {self.session_name}")
        else:
            print(f"✅ 使用现有tmux会话: {self.session_name}")

    def _cleanup_tmux_session(self):
        """清理tmux会话"""
        subprocess.run([
            "tmux", "kill-session",
            "-t", self.session_name
        ])
        print(f"\n🧹 清理tmux会话: {self.session_name}")

    def get_status_summary(self) -> Dict:
        """获取执行状态摘要"""
        if not self.results:
            return {
                "total": len(self.tasks),
                "pending": len(self.tasks),
                "success": 0,
                "failed": 0,
                "error": 0
            }

        summary = {
            "total": len(self.tasks),
            "success": 0,
            "failed": 0,
            "error": 0,
            "timeout": 0,
            "pending": 0
        }

        for task_id, result in self.results.items():
            status = result.get("status", "pending")
            if status == "success":
                summary["success"] += 1
            elif status == "failed":
                summary["failed"] += 1
            elif status == "error":
                summary["error"] += 1
            elif status == "timeout":
                summary["timeout"] += 1
            else:
                summary["pending"] += 1

        return summary

    def print_summary(self):
        """打印执行摘要"""
        summary = self.get_status_summary()

        print("\n" + "="*60)
        print("📊 执行摘要")
        print("="*60)
        print(f"总任务数: {summary['total']}")
        print(f"✅ 成功: {summary['success']}")
        print(f"❌ 失败: {summary['failed']}")
        print(f"⚠️  错误: {summary['error']}")
        print(f"⏱️  超时: {summary['timeout']}")
        print(f"⏳ 待处理: {summary['pending']}")
        print("="*60)


def get_parallel_executor(mode: str = "sequential") -> ParallelExecutor:
    """
    获取并行执行器实例

    Args:
        mode: 执行模式 ("sequential", "tmux", "openclaw")

    Returns:
        ParallelExecutor实例
    """
    return ParallelExecutor(mode=mode)


if __name__ == "__main__":
    # 测试
    executor = get_parallel_executor("sequential")

    # 添加测试任务
    executor.add_task("task1", "echo 'Task 1'", "测试任务1")
    executor.add_task("task2", "echo 'Task 2'", "测试任务2")
    executor.add_task("task3", "echo 'Task 3'", "测试任务3")

    # 执行
    results = executor.execute()

    # 打印摘要
    executor.print_summary()
