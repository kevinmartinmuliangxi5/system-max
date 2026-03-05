"""
ECS - 命令行接口

提供CLI命令
"""

import sys
import asyncio
import argparse
from pathlib import Path
from typing import Optional

from . import ECSCoordinator, ECSConfig, easy_collaborate
from .utils import (
    validate_api_key, format_emergence_report,
    parse_task_input, format_duration
)


def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        description="ECS - 多Agent无领导小组讨论真涌现系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础使用
  python -m ecs "设计一个智能客服系统"

  # 指定Agent数量
  python -m ecs "产品规划" --agents 7

  # 自定义配置
  python -m ecs "技术选型" --config my_config.yaml

  # 输出到文件
  python -m ecs "复杂任务" --output result.json

  # 详细模式
  python -m ecs "创新项目" --verbose

  # 列出可用角色
  python -m ecs --list-roles

  # 创建配置文件
  python -m ecs --init-config
        """
    )

    # 主要参数
    parser.add_argument(
        'task',
        nargs='?',
        help='任务描述（如果不提供则进入交互模式）'
    )

    # 配置选项
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='配置文件路径（YAML或JSON格式）'
    )
    parser.add_argument(
        '--agents', '-a',
        type=int,
        default=5,
        help='Agent数量（默认：5）'
    )
    parser.add_argument(
        '--rounds', '-r',
        type=int,
        default=3,
        help='最大讨论轮数（默认：3）'
    )
    parser.add_argument(
        '--threshold', '-t',
        type=float,
        default=0.7,
        help='涌现阈值（0-1，默认：0.7）'
    )

    # 输出选项
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='输出文件路径（支持.json和.md格式）'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'markdown', 'both'],
        default='json',
        help='输出格式（默认：json）'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='安静模式，只输出最终结果'
    )

    # 实用选项
    parser.add_argument(
        '--list-roles',
        action='store_true',
        help='列出所有可用角色'
    )
    parser.add_argument(
        '--init-config',
        action='store_true',
        help='创建默认配置文件'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='验证配置文件'
    )

    # 调试选项
    parser.add_argument(
        '--debug',
        action='store_true',
        help='调试模式'
    )

    return parser


def list_roles():
    """列出所有可用角色"""
    print("\n" + "=" * 60)
    print("可用角色列表")
    print("=" * 60 + "\n")

    # 创建临时协调器以获取角色信息
    coordinator = ECSCoordinator()
    roles = coordinator.get_available_roles()

    for role_id, role_name in roles.items():
        details = coordinator.get_role_details(role_id)
        if details:
            print(f"【{role_id}】{role_name}")
            print(f"  描述: {details['description']}")
            print(f"  思维风格: {details['thinking_style']}")
            if details['focus_areas']:
                print(f"  关注点: {', '.join(details['focus_areas'][:3])}")
            print(f"  专业领域:")
            for exp in details['expertise']:
                print(f"    - {exp['domain']}: {', '.join(exp['skills'][:3])}")
            print()

    print("=" * 60)


def init_config(output_path: str = "config.yaml"):
    """创建默认配置文件"""
    from .config import create_default_config

    try:
        create_default_config(output_path)
        print(f"✓ 默认配置文件已创建: {output_path}")
        print(f"\n你可以编辑此文件来自定义系统行为")
    except Exception as e:
        print(f"✗ 创建配置文件失败: {e}")
        sys.exit(1)


def validate_config_file(config_path: str):
    """验证配置文件"""
    try:
        config = ECSConfig.from_file(config_path)
        is_valid, errors = config.validate()

        if is_valid:
            print(f"✓ 配置文件有效: {config_path}")
            print(f"\n配置摘要:")
            print(f"  Agent数量: {config.agents.count}")
            print(f"  最大轮数: {config.collaboration.max_rounds}")
            print(f"  涌现阈值: {config.emergence.emergence_threshold}")
            print(f"  收敛阈值: {config.collaboration.convergence_threshold}")
        else:
            print(f"✗ 配置文件存在错误:")
            for error in errors:
                print(f"  • {error}")
            sys.exit(1)

    except FileNotFoundError:
        print(f"✗ 配置文件不存在: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 解析配置文件失败: {e}")
        sys.exit(1)


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 60)
    print("ECS - 多Agent无领导小组讨论系统")
    print("=" * 60)
    print("\n输入你的任务描述（输入'quit'退出）:")

    # 验证API密钥
    is_valid, message = validate_api_key()
    if not is_valid:
        print(f"\n⚠️  {message}")
        print("\n请设置ANTHROPIC_API_KEY环境变量")
        sys.exit(1)

    while True:
        try:
            task = input("\n> ").strip()

            if not task:
                continue

            if task.lower() in ['quit', 'exit', 'q', '退出']:
                print("\n再见！")
                break

            # 执行协作
            print(f"\n正在处理任务: {task[:50]}...")
            result = easy_collaborate(task, verbose=True)

            print(f"\n{'='*60}")
            print("最终方案:")
            print("="*60)
            print(result.solution)

            print(f"\n{'='*60}")
            print("涌现分析:")
            print("="*60)
            print(format_emergence_report(result.emergence_report))

            if result.emergence_report.metrics.emergence_score > 0.7:
                print("\n✨ 检测到真涌现！")

        except KeyboardInterrupt:
            print("\n\n中断执行")
            break
        except Exception as e:
            print(f"\n✗ 执行失败: {e}")
            if "api_key" in str(e).lower() or "401" in str(e):
                print("\n请检查ANTHROPIC_API_KEY是否正确设置")
            continue


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()

    # 处理特殊命令
    if args.list_roles:
        list_roles()
        return

    if args.init_config:
        init_config()
        return

    if args.validate:
        if not args.config:
            print("✗ 请使用--config参数指定配置文件")
            sys.exit(1)
        validate_config_file(args.config)
        return

    # 加载配置
    config = None
    if args.config:
        try:
            config = ECSConfig.from_file(args.config)
        except Exception as e:
            print(f"✗ 加载配置文件失败: {e}")
            sys.exit(1)
    else:
        config = ECSConfig()

    # 更新配置（命令行参数优先级更高）
    if args.verbose:
        config.verbose = True

    # 验证API密钥
    if not args.debug:
        is_valid, message = validate_api_key()
        if not is_valid:
            print(f"✗ {message}")
            print("\n请设置ANTHROPIC_API_KEY环境变量")
            print("\n在Linux/Mac上:")
            print("  export ANTHROPIC_API_KEY='your-key-here'")
            print("\n在Windows上:")
            print("  set ANTHROPIC_API_KEY=your-key-here")
            sys.exit(1)

    # 如果没有任务，进入交互模式
    if not args.task:
        interactive_mode()
        return

    # 执行协作任务
    try:
        task = parse_task_input(args.task)

        if args.verbose:
            print(f"\n任务: {task}")
            print(f"Agent数量: {args.agents}")
            print(f"最大轮数: {args.rounds}")
            print(f"涌现阈值: {args.threshold}")
            print()

        # 创建协调器并执行
        coordinator = ECSCoordinator(config)

        start_time = asyncio.get_event_loop().time()
        result = coordinator.collaborate(
            task,
            agent_count=args.agents,
            max_rounds=args.rounds,
            emergence_threshold=args.threshold,
            verbose=args.verbose and not args.quiet
        )

        # 输出结果
        if args.quiet:
            # 安静模式：只输出方案
            print(result.solution)
        else:
            # 正常输出
            print(f"\n{'='*60}")
            print("最终方案")
            print("="*60)
            print(result.solution)

            print(f"\n{'='*60}")
            print("涌现分析")
            print("="*60)
            print(format_emergence_report(result.emergence_report))

            if result.total_time > 0:
                print(f"\n总耗时: {format_duration(result.total_time)}")
            print(f"完成轮数: {result.rounds_completed}")
            print(f"总消息数: {result.total_messages}")

            # 涌现评价
            score = result.emergence_report.metrics.emergence_score
            if score > 0.8:
                print("\n✨✨✨ 优秀！检测到高质量真涌现！")
            elif score > 0.7:
                print("\n✨ 检测到真涌现！")
            elif score > 0.5:
                print("\n⚠️  检测到部分涌现")
            else:
                print("\n⚠️  涌现程度较低")

        # 导出结果
        if args.output:
            try:
                coordinator.export_result(result, args.output)
                print(f"\n✓ 结果已保存到: {args.output}")
            except Exception as e:
                print(f"\n⚠️  保存结果失败: {e}")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ 执行失败: {e}")

        if args.debug:
            import traceback
            traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()
