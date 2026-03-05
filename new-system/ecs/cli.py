"""
ECS - 命令行接口
提供交互式和批处理模式
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

from . import (
    ECSCoordinator,
    ECSQueryBuilder,
    ECSConfig,
    load_config,
    easy_collaborate
)
from .roles import get_all_roles, list_role_combinations, recommend_roles_for_task
from .utils import (
    format_emergence_report,
    validate_api_key,
    validate_task_description,
    estimate_collaboration_cost,
    get_timestamp
)


# ============================================================
# 交互式模式
# ============================================================

def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("ECS - 多Agent真涌现系统 (交互式模式)")
    print("=" * 60)

    # 1. 输入任务
    print("\n请输入您的任务描述（输入 'quit' 退出）:")
    task = input("> ").strip()

    if task.lower() in ['quit', 'exit', 'q']:
        print("再见！")
        return

    # 验证任务
    valid, error = validate_task_description(task)
    if not valid:
        print(f"\n错误: {error}")
        return

    # 2. 选择Agent数量
    print("\n选择Agent数量 (3-10，默认5):")
    agent_input = input("> ").strip()
    agent_count = int(agent_input) if agent_input.isdigit() else 5
    agent_count = max(3, min(10, agent_count))

    # 3. 选择讨论轮次
    print("\n选择讨论轮次 (2-7，默认3):")
    rounds_input = input("> ").strip()
    max_rounds = int(rounds_input) if rounds_input.isdigit() else 3
    max_rounds = max(2, min(7, max_rounds))

    # 4. 选择涌现阈值
    print("\n选择涌现阈值 (0.5-0.9，默认0.7):")
    threshold_input = input("> ").strip()
    try:
        threshold = float(threshold_input) if threshold_input else 0.7
        threshold = max(0.5, min(0.9, threshold))
    except ValueError:
        threshold = 0.7

    # 5. 成本估算
    print("\n=== 成本估算 ===")
    cost_estimate = estimate_collaboration_cost(
        agent_count=agent_count,
        rounds=max_rounds,
        model="claude-sonnet-4-20250514"
    )
    print(f"预计调用次数: {cost_estimate['total_calls']}")
    print(f"预计输入tokens: {cost_estimate['total_input_tokens']:,}")
    print(f"预计输出tokens: {cost_estimate['total_output_tokens']:,}")
    print(f"预计成本 (无缓存): ${cost_estimate['cost_no_cache']:.4f}")
    print(f"预计成本 (有缓存): ${cost_estimate['cost_with_cache']:.4f}")
    print(f"缓存节省: {cost_estimate['savings_percent']:.1f}%")

    # 6. 确认
    print("\n是否继续？(y/n):")
    confirm = input("> ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return

    # 7. 执行协作
    print("\n=== 开始协作 ===")
    print(f"任务: {task[:100]}...")
    print(f"配置: {agent_count}个Agent, {max_rounds}轮, 阈值{threshold}")
    print()

    try:
        result = easy_collaborate(
            task=task,
            agents=agent_count,
            rounds=max_rounds,
            threshold=threshold,
            verbose=True
        )

        # 8. 显示结果
        print("\n" + "=" * 60)
        print("=== 协作完成 ===")
        print("=" * 60)
        print(format_emergence_report(result.emergence_report))
        print("\n=== 解决方案 ===")
        print(result.solution[:1000])
        if len(result.solution) > 1000:
            print("...")
        print(f"\n耗时: {result.total_time:.1f}秒")

    except Exception as e:
        print(f"\n错误: {e}")
        logging.exception("协作失败")


# ============================================================
# 命令行模式
# ============================================================

def command_mode(args):
    """命令行模式"""
    # 加载配置
    config = load_config(args.config)

    # 应用命令行参数
    if args.verbose:
        config.verbose = True

    # 执行协作
    print(f"任务: {args.task}")
    print(f"Agent数量: {args.agents}")
    print(f"讨论轮次: {args.rounds}")

    result = easy_collaborate(
        task=args.task,
        agents=args.agents,
        rounds=args.rounds,
        threshold=args.threshold,
        output=args.output,
        verbose=args.verbose
    )

    # 显示结果
    print("\n" + format_emergence_report(result.emergence_report))


# ============================================================
# 列出角色
# ============================================================

def list_roles():
    """列出所有可用角色"""
    roles = get_all_roles()

    print("=" * 60)
    print("可用角色列表")
    print("=" * 60)

    for role_id, role_name in roles.items():
        print(f"\n[{role_id}] {role_name}")


# ============================================================
# 列出角色组合
# ============================================================

def list_combinations():
    """列出所有角色组合"""
    combinations = list_role_combinations()

    print("=" * 60)
    print("角色组合列表")
    print("=" * 60)

    for combo_id, combo_name in combinations.items():
        print(f"\n[{combo_id}] {combo_name}")


# ============================================================
# 推荐角色
# ============================================================

def recommend_roles(task: str):
    """为任务推荐角色"""
    recommended = recommend_roles_for_task(task, num_agents=7)

    print("=" * 60)
    print("角色推荐")
    print("=" * 60)
    print(f"\n任务: {task}")
    print(f"\n推荐的Agent组合:")

    roles = get_all_roles()
    for i, role_id in enumerate(recommended, 1):
        role_name = roles.get(role_id, role_id)
        print(f"  {i}. {role_id}: {role_name}")


# ============================================================
# 验证配置
# ============================================================

def validate_config_file(config_path: str):
    """验证配置文件"""
    try:
        config = load_config(config_path)
        errors = config.validate()

        if errors:
            print("配置验证失败:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("配置验证通过！")
            print(f"\n配置摘要:")
            print(f"  LLM提供商: {config.llm.provider}")
            print(f"  模型: {config.llm.model}")
            print(f"  Agent数量: {config.agents.count}")
            print(f"  讨论轮次: {config.collaboration.max_rounds}")
            print(f"  涌现阈值: {config.emergence.emergence_threshold}")
            return True

    except Exception as e:
        print(f"配置文件错误: {e}")
        return False


# ============================================================
# 主函数
# ============================================================

def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="ECS - 多Agent真涌现系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式模式
  ecs-cli

  # 快速协作
  ecs-cli --task "设计一个API接口"

  # 指定参数
  ecs-cli --task "优化数据库查询" --agents 5 --rounds 3

  # 保存结果
  ecs-cli --task "设计用户系统" --output result.json

  # 列出角色
  ecs-cli --list-roles

  # 推荐角色
  ecs-cli --recommend "设计一个加密货币交易所"

  # 验证配置
  ecs-cli --validate-config config.yaml
        """
    )

    parser.add_argument(
        "--task", "-t",
        help="任务描述"
    )

    parser.add_argument(
        "--agents", "-a",
        type=int,
        default=5,
        help="Agent数量 (默认5)"
    )

    parser.add_argument(
        "--rounds", "-r",
        type=int,
        default=3,
        help="讨论轮次 (默认3)"
    )

    parser.add_argument(
        "--threshold", "-th",
        type=float,
        default=0.7,
        help="涌现阈值 (默认0.7)"
    )

    parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )

    parser.add_argument(
        "--config", "-c",
        help="配置文件路径"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )

    parser.add_argument(
        "--list-roles",
        action="store_true",
        help="列出所有可用角色"
    )

    parser.add_argument(
        "--list-combinations",
        action="store_true",
        help="列出所有角色组合"
    )

    parser.add_argument(
        "--recommend",
        metavar="TASK",
        help="为任务推荐角色"
    )

    parser.add_argument(
        "--validate-config",
        metavar="CONFIG",
        help="验证配置文件"
    )

    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互式模式"
    )

    args = parser.parse_args()

    # 处理特殊命令
    if args.list_roles:
        list_roles()
        return

    if args.list_combinations:
        list_combinations()
        return

    if args.recommend:
        recommend_roles(args.recommend)
        return

    if args.validate_config:
        validate_config_file(args.validate_config)
        return

    # 交互式模式
    if args.interactive or not args.task:
        interactive_mode()
        return

    # 命令行模式
    command_mode(args)


if __name__ == "__main__":
    main()
