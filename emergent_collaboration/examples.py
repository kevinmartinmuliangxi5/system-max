"""
ECS - 使用示例

演示如何使用EmergentCollaboration System
"""

import asyncio
from emergent_collaboration import (
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


# ============================================================
# 示例3：使用自定义配置
# ============================================================

def example3_custom_config():
    """使用自定义配置"""
    print("\n" " + "=" * 60)
    print("示例3：使用自定义配置")
    print("=" * 60)

    # 创建自定义配置
    config = ECSConfig()
    config.agents.count = 6
    config.collaboration.max_rounds = 4
    config.emergence.emergence_threshold = 0.8
    config.verbose = True

    # 创建协调器
    coordinator = ECSCoordinator(config)

    # 执行协作
    result = coordinator.collaborate(
        task="设计一个智能家居控制系统",
        agent_count=6,
        max_rounds=4,
        emergence_threshold=0.8
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
        print(f"  {details['description']}")
        print(f"  思维风格: {details['thinking_style']}")


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
    for i, role_id in enumerate(recommended, 1):
        role_name = coordinator.get_available_roles()[role_id]
        print(f"  {i}. {role_id}: {role_name}")


# ============================================================
# 示例6：使用预定义角色组合
# ============================================================

def example6_role_combinations():
    """使用预定义角色组合"""
    print("\n" + "=" * 60)
    print("示例6：使用预定义角色组合")
    print("=" * 60)

    from emergent_collaboration import ROLE_COMBINATIONS

    print("\n可用角色组合:")
    for combo_id, combo_info in ROLE_COMBINATIONS.items():
        print(f"\n【{combo_id}】{combo_info['name']}")
        print(f"  描述: {combo_info['description']}")
        print(f"  角色: {', '.join(combo_info['roles'])}")

    # 使用特定组合
    print("\n\n使用'product_design'组合执行任务:")
    config = ECSConfig()
    config.agents.selection_strategy = "diverse"
    config.agents.custom_roles = ROLE_COMBINATIONS['product_design']['roles'][:5]

    coordinator = ECSCoordinator(config)
    result = coordinator.collaborate(
        task="设计一款面向Z世代的社交应用",
        verbose=True
    )


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

    # 总结
    avg_emergence = sum(
        r.emergence_report.metrics.emergence_score
        for r in results
    ) / len(results)

    print(f"\n平均涌现强度: {avg_emergence:.2f}")


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

    print(f"\n详细指标:")
    print(f"  观点离散度: {metrics.dispersion:.3f}")
    print(f"  极化程度: {metrics.polarization:.3f}")
    print(f"  连接密度: {metrics.connectivity:.2f}")

    # 涌现类型解释
    emergence_type_descriptions = {
        "aggregation": "聚合涌现 - 观点简单聚合",
        "coordination": "协调涌现 - 角色分工协作",
        "synergy": "协同涌现 - 深度观点整合",
        "innovation": "创新涌现 - 突破性洞察",
        "meta_emergence": "元涌现 - 范式转移"
    }

    print(f"\n涌现类型说明:")
    print(f"  {emergence_type_descriptions[report.emergence_type.value]}")


# ============================================================
# 示例9：异步使用
# ============================================================

async def example9_async():
#     """异步使用示例"""
#     print("\n" + "=" * 60)
#     print("示例9：异步使用")
#     print("=" * 60)
#
#     coordinator = ECSCoordinator()
#
#     # 并发执行多个任务
#     tasks = [
#         "设计API接口规范",
#         "定义数据模型",
#         "规划测试策略"
#     ]
#
#     results = await asyncio.gather(*[
#         coordinator.collaborate(task, verbose=False)
#         for task in tasks
#     ])
#
#     for result in results:
#         print(f"任务完成: {result.solution[:50]}...")


# ============================================================
# 示例10：导出和比较结果
# ============================================================

def example10_export_compare():
    """导出和比较结果"""
    print("\n" + "=" * 60)
    print("示例10：导出和比较结果")
    print("=" * 60)

    # 同一任务，不同配置
    configs = [
        {"agents": 3, "rounds": 2, "threshold": 0.6},
        {"agents": 5, "rounds": 3, "threshold": 0.7},
        {"agents": 7, "rounds": 4, "threshold": 0.8},
    ]

    results = []
    for i, config_override in enumerate(configs, 1):
        print(f"\n配置 {i}: {config_override}")
        result = easy_collaborate(
            task="设计一个用户友好的文件管理界面",
            verbose=False,
            **config_override
        )

        results.append(result)

        # 保存结果
        output_file = f"result_config{i}.json"
        from emergent_collaboration import ECSConfig
        config = ECSConfig()
        coordinator = ECSCoordinator(config)
        coordinator.export_result(result, output_file)

        print(f"  涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")
        print(f"  已保存到: {output_file}")

    # 比较
    print(f"\n=== 配置比较 ===")
    for i, result in enumerate(results, 1):
        print(f"\n配置{i}:")
        print(f"  涌现强度: {result.emergence_report.metrics.emergence_score:.2f}")
        print(f"  轮次: {result.rounds_completed}")
        print(f"  耗时: {result.total_time:.1f}秒")


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
        # ("示例9：异步使用", example9_async),
        ("示例10：导出比较", example10_export_compare),
    ]

    print("\n" + "=" * 60)
    print("ECS - 使用示例集合")
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
