"""
ECS - 使用示例
演示如何使用EmergentCollaboration System
"""

import asyncio
from ecs import (
    ECSCoordinator,
    easy_collaborate,
    ECSQueryBuilder,
    ECSConfig,
    quick
)


# ============================================================
# 示例1：最简单的使用方式
# ============================================================

def example1_basic():
    """最简单的使用方式"""
    print("=" * 60)
    print("示例1：最简单的使用方式")
    print("=" * 60)

    result = easy_collaborate(
        task="设计一个可持续的城市自行车共享系统",
        agents=5,
        rounds=3,
        verbose=True
    )

    print(f"\n涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")
    print(f"涌现类型: {result.emergence_report.emergence_type.value}")
    print(f"协同度: {result.emergence_report.metrics.synergy:.2f}")


# ============================================================
# 示例2：使用查询构建器
# ============================================================

def example2_query_builder():
    """使用查询构建器"""
    print("\n" + "=" * 60)
    print("示例2：使用查询构建器")
    print("=" * 60)

    result = (ECSQueryBuilder()
        .with_task("开发一个在线教育平台的核心功能")
        .with_agents(7)
        .with_rounds(4)
        .with_threshold(0.8)
        .with_output("education_platform_result.json")
        .verbose(True)
        .execute())

    print("\n✓ 已保存结果到 education_platform_result.json")
    print(f"涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")


# ============================================================
# 示例3：使用自定义配置
# ============================================================

def example3_custom_config():
    """使用自定义配置"""
    print("\n" + "=" * 60)
    print("示例3：使用自定义配置")
    print("=" * 60)

    # 创建自定义配置
    config = ECSConfig()
    config.agents.count = 6
    config.collaboration.max_rounds = 4
    config.emergence.emergence_threshold = 0.8
    config.verbose = True
    # 启用迹发沟通
    config.collaboration.stigmergy_enabled = True
    # 启用动态温度调整
    config.collaboration.temperature_dynamic = True

    # 创建协调器
    coordinator = ECSCoordinator(config)

    # 执行协作
    result = coordinator.collaborate(
        task="设计一个智能家居控制系统",
        agent_count=6,
        max_rounds=4
    )

    print(f"\n涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")


# ============================================================
# 示例4：探索角色信息
# ============================================================

def example4_explore_roles():
    """探索可用角色"""
    print("\n" + "=" * 60)
    print("示例4：探索可用角色")
    print("=" * 60)

    coordinator = ECSCoordinator()

    # 列出所有角色
    roles = coordinator.get_available_roles()
    print(f"\n可用角色共 {len(roles)} 个:")
    for role_id, role_name in roles.items():
        details = coordinator.get_role_details(role_id)
        print(f"\n【{role_id}】{role_name}")
        print(f"  描述: {details['description']}")
        print(f"  思维风格: {details['thinking_style']}")
        print(f"  专业领域: {', '.join(details['expertise'][:3])}")


# ============================================================
# 示例5：为任务推荐角色
# ============================================================

def example5_recommend_roles():
    """为任务推荐角色"""
    print("\n" + "=" * 60)
    print("示例5：为任务推荐角色")
    print("=" * 60)

    coordinator = ECSCoordinator()

    task = "设计一个加密货币交易所的架构"
    recommended = coordinator.recommend_roles_for_task(task, num_agents=7)

    print(f"\n任务: {task}")
    print(f"\n推荐的Agent组合:")
    roles = coordinator.get_available_roles()
    for i, role_id in enumerate(recommended, 1):
        role_name = roles.get(role_id, role_id)
        print(f"  {i}. {role_id}: {role_name}")


# ============================================================
# 示例6：使用预定义角色组合
# ============================================================

def example6_role_combinations():
    """使用预定义角色组合"""
    print("\n" + "=" * 60)
    print("示例6：使用预定义角色组合")
    print("=" * 60)

    from ecs.roles import ROLE_COMBINATIONS

    print("\n可用角色组合:")
    combinations = ECSCoordinator().list_role_combinations()
    for combo_id, combo_name in combinations.items():
        combo_info = ROLE_COMBINATIONS[combo_id]
        print(f"\n【{combo_id}】{combo_name}")
        print(f"  描述: {combo_info['description']}")
        print(f"  角色: {', '.join(combo_info['roles'])}")
        print(f"  理想规模: {combo_info['ideal_size']}个Agent")

    # 使用特定组合
    print("\n\n使用'product_design'组合执行任务:")
    result = easy_collaborate(
        task="设计一款面向Z世代的社交应用",
        roles=ROLE_COMBINATIONS['product_design']['roles']
    )

    print(f"\n涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")


# ============================================================
# 示例7：批量处理多个任务
# ============================================================

def example7_batch_processing():
    """批量处理多个任务"""
    print("\n" + "=" * 60)
    print("示例7：批量处理多个任务")
    print("=" * 60)

    tasks = [
        "设计一个企业内部知识管理系统",
        "优化移动应用的电池寿命",
        "创建一个用户反馈收集系统"
    ]

    results = []
    for i, task in enumerate(tasks, 1):
        print(f"\n处理任务 {i}/{len(tasks)}: {task[:50]}...")
        result = easy_collaborate(task, agents=5, rounds=2, verbose=False)
        results.append(result)
        print(f"  涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")
        print(f"  协同度: {result.emergence_report.metrics.synergy:.2f}")

    # 总结
    avg_emergence = sum(
        r.emergence_report.metrics.emergence_score
        for r in results
    ) / len(results)

    avg_synergy = sum(
        r.emergence_report.metrics.synergy
        for r in results
    ) / len(results)

    print(f"\n平均涌现强度: {avg_emergence:.2f}")
    print(f"平均协同度: {avg_synergy:.2f}")


# ============================================================
# 示例8：分析涌现报告
# ============================================================

def example8_analyze_emergence():
    """分析涌现报告"""
    print("\n" + "=" * 60)
    print("示例8：分析涌现报告")
    print("=" * 60)

    result = easy_collaborate(
        task="评估并改进现有的产品设计",
        agents=6,
        rounds=3,
        verbose=False
    )

    report = result.emergence_report

    print("\n=== 涌现分析 ===")
    print(f"涌现类型: {report.emergence_type.value}")
    print(f"系统阶段: {report.system_phase.value}")

    metrics = report.metrics
    print(f"\n核心指标:")
    print(f"  涌现强度: {metrics.emergence_score:.2f}")
    print(f"  多样性: {metrics.diversity:.2f}")
    print(f"  共识度: {metrics.consensus:.2f}")
    print(f"  新颖度: {metrics.novelty:.2f}")
    print(f"  整合度: {metrics.integration:.2f}")
    print(f"  协同度: {metrics.synergy:.2f}")

    print(f"\n详细指标:")
    print(f"  观点离散度: {metrics.dispersion:.3f}")
    print(f"  极化程度: {metrics.polarization:.3f}")
    print(f"  连接密度: {metrics.connectivity:.2f}")

    # 涌现类型解释
    from ecs.utils import get_emergence_type_description
    emergence_desc = get_emergence_type_description(report.emergence_type.value)

    print(f"\n涌现类型说明:")
    print(f"  {emergence_desc}")

    # 系统阶段解释
    from ecs.utils import get_system_phase_description
    phase_desc = get_system_phase_description(report.system_phase.value)

    print(f"\n系统阶段说明:")
    print(f"  {phase_desc}")

    # 洞察和建议
    if report.insights:
        print(f"\n关键洞察:")
        for insight in report.insights:
            print(f"  - {insight}")

    if report.recommendations:
        print(f"\n建议:")
        for rec in report.recommendations:
            print(f"  - {rec}")


# ============================================================
# 示例9：成本估算
# ============================================================

def example9_cost_estimation():
    """成本估算"""
    print("\n" + "=" * 60)
    print("示例9：成本估算")
    print("=" * 60)

    from ecs.utils import estimate_collaboration_cost

    scenarios = [
        ("简单任务", 3, 2),
        ("中等任务", 5, 3),
        ("复杂任务", 7, 5),
    ]

    print("\n成本估算（使用Claude Sonnet 4）:\n")
    print(f"{'场景':<12} {'Agent数':<8} {'轮次':<6} {'无缓存':<12} {'有缓存':<12} {'节省':<8}")
    print("-" * 60)

    for name, agents, rounds in scenarios:
        estimate = estimate_collaboration_cost(
            agent_count=agents,
            rounds=rounds
        )

        print(f"{name:<12} {agents:<8} {rounds:<6} "
              f"${estimate['cost_no_cache']:<11.4f} "
              f"${estimate['cost_with_cache']:<11.4f} "
              f"{estimate['savings_percent']:.1f}%")


# ============================================================
# 示例10：SPAR循环详细演示
# ============================================================

def example10_spar_cycle():
    """SPAR循环详细演示"""
    print("\n" + "=" * 60)
    print("示例10：SPAR循环详细演示")
    print("=" * 60)

    # 创建启用SPAR循环所有阶段的配置
    config = ECSConfig()
    config.collaboration.enable_sense_phase = True
    config.collaboration.enable_discuss_phase = True
    config.collaboration.enable_act_phase = True
    config.collaboration.enable_reflect_phase = True
    config.collaboration.stigmergy_enabled = True  # 启用迹发沟通
    config.collaboration.temperature_dynamic = True  # 启用动态温度
    config.verbose = True

    coordinator = ECSCoordinator(config)

    result = coordinator.collaborate(
        task="设计一个可扩展的微服务架构",
        agent_count=5,
        max_rounds=3
    )

    print("\n=== SPAR循环完成 ===")
    print(f"Sense阶段: 已执行（感知任务和环境）")
    print(f"Discuss阶段: {result.rounds_completed}轮讨论")
    print(f"Act阶段: 已执行（生成解决方案）")
    print(f"Reflect阶段: 已执行（反思和评估）")
    print(f"\n最终涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有示例"""
    examples = [
        ("示例1：最简单的使用方式", example1_basic),
        ("示例2：查询构建器", example2_query_builder),
        ("示例3：自定义配置", example3_custom_config),
        ("示例4：探索角色", example4_explore_roles),
        ("示例5：推荐角色", example5_recommend_roles),
        ("示例6：角色组合", example6_role_combinations),
        ("示例7：批量处理", example7_batch_processing),
        ("示例8：分析涌现", example8_analyze_emergence),
        ("示例9：成本估算", example9_cost_estimation),
        ("示例10：SPAR循环", example10_spar_cycle),
    ]

    print("\n" + "=" * 60)
    print("ECS - 使用示例集合")
    print("版本 2.0 Enhanced")
    print("=" * 60)
    print("\n选择要运行的示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n  0. 运行所有示例")
    print("  q. 退出")

    try:
        choice = input("\n请选择 (0-10, 或q): ").strip()
    except KeyboardInterrupt:
        print("\n\n退出")
        return

    if choice.lower() == 'q':
        return

    if choice == '0':
        # 运行所有示例
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\n✗ {name} 执行失败: {e}")
    else:
        # 运行选定的示例
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                name, func = examples[idx]
                func()
            else:
                print("无效选择")
        except ValueError:
            print("无效输入")
        except Exception as e:
            print(f"\n✗ 执行失败: {e}")


if __name__ == "__main__":
    main()
