#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
记忆模块测试脚本
验证三层记忆系统的基本功能
"""

import sys
import os
from pathlib import Path

# 设置UTF-8输出
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from ecs.memory import MemoryManager, MemoryConfig


def test_working_memory():
    """测试工作记忆"""
    print("\n=== 测试工作记忆 ===")
    manager = MemoryManager()

    # 添加消息
    manager.add_message({"role": "user", "content": "Hello"})
    manager.add_message({"role": "assistant", "content": "Hi there!"})

    # 设置上下文
    manager.set_context("session_id", "test_001")
    manager.set_context("user_name", "Alice")

    # 获取消息
    messages = manager.get_recent_messages(10)
    print(f"消息数量: {len(messages)}")
    print(f"最近消息: {messages[-1]}")

    # 获取上下文
    session_id = manager.get_context("session_id")
    print(f"Session ID: {session_id}")

    # 统计
    stats = manager.get_stats()
    print(f"工作记忆项: {stats['working_memory_count']}")


def test_episodic_memory():
    """测试情景记忆"""
    print("\n=== 测试情景记忆 ===")
    manager = MemoryManager()

    # 保存协作经验
    manager.save_collaboration_experience(
        task="编写一个快速排序算法",
        config={"language": "python", "style": "recursive"},
        result={"code": "def quicksort..."},
        emergence_score=0.85
    )

    manager.save_collaboration_experience(
        task="实现二分查找",
        config={"language": "python", "style": "iterative"},
        result={"code": "def binary_search..."},
        emergence_score=0.75
    )

    # 推荐配置
    config = manager.recommend_config("编写排序算法")
    print(f"推荐配置: {config}")

    # 相似经验
    similar = manager.get_similar_experiences("排序", top_k=2)
    print(f"相似经验数量: {len(similar)}")
    if similar:
        print(f"最相似任务: {similar[0]['task']}")

    # 统计
    stats = manager.get_stats()
    print(f"情景记忆项: {stats['episodic_memory_count']}")


def test_semantic_memory():
    """测试语义记忆"""
    print("\n=== 测试语义记忆 ===")
    manager = MemoryManager()

    # 触发成功模式保存 (emergence_score > 0.8)
    manager.save_collaboration_experience(
        task="设计REST API",
        config={"framework": "fastapi", "auth": "jwt"},
        result={"endpoints": 10, "tests": "passing"},
        emergence_score=0.92
    )

    # 获取成功模式
    patterns = manager.get_success_patterns()
    print(f"成功模式数量: {len(patterns)}")
    if patterns:
        print(f"最新模式: {patterns[-1].get('pattern_name', 'N/A')}")

    # 统计
    stats = manager.get_stats()
    print(f"语义记忆项: {stats['semantic_memory_count']}")


def test_session_cleanup():
    """测试会话清理"""
    print("\n=== 测试会话清理 ===")
    manager = MemoryManager()

    # 添加工作记忆
    manager.add_message({"role": "user", "content": "Temporary"})

    stats_before = manager.get_stats()
    print(f"清理前工作记忆: {stats_before['working_memory_count']}")

    # 清理会话
    manager.cleanup_session()

    stats_after = manager.get_stats()
    print(f"清理后工作记忆: {stats_after['working_memory_count']}")
    print(f"长期记忆保留: {stats_after['episodic_memory_count']} 情景, {stats_after['semantic_memory_count']} 模式")


if __name__ == "__main__":
    print("=" * 50)
    print("ECS 记忆系统测试")
    print("=" * 50)

    try:
        test_working_memory()
        test_episodic_memory()
        test_semantic_memory()
        test_session_cleanup()

        print("\n" + "=" * 50)
        print("[OK] 所有测试通过")
        print("=" * 50)

    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
