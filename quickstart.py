"""
涌现检测方法 - 快速开始指南
================================

这是一个简化的入门示例，展示如何使用涌现检测工具包。
"""

import numpy as np
from emergence_detection_methods import (
    ViewpointDiversity,
    ConsensusAnalyzer,
    EmergenceDetector
)


def example_1_basic_diversity():
    """示例1：基础多样性分析"""
    print("\n" + "="*60)
    print("示例1：分析观点多样性")
    print("="*60)

    # 创建分析器
    analyzer = ViewpointDiversity()

    # 生成一些观点数据
    opinions = np.random.uniform(0, 1, (100, 1))

    # 计算多样性指标
    metrics = analyzer.compute_all_metrics(opinions)

    print("\n结果：")
    print(f"  熵基多样性: {metrics.entropy:.4f} (0=低, 1=高)")
    print(f"  极化程度: {metrics.polarization:.4f} (0=低, 1=高)")
    print(f"  观点簇数: {metrics.cluster_count}")


def example_2_consensus_tracking():
    """示例2：追踪共识形成过程"""
    print("\n" + "="*60)
    print("示例2：追踪共识形成")
    print("="*60)

    # 创建分析器
    analyzer = ConsensusAnalyzer()

    # 模拟观点收敛
    n_agents = 30
    opinions = np.random.uniform(0.3, 0.7, (n_agents, 1))

    print("\n共识演化：")
    for step in range(5):
        # 计算当前共识
        metrics = analyzer.compute_all_metrics(opinions)
        print(f"  步骤 {step}: 共识={metrics.consensus_level:.2f}, "
              f"同意率={metrics.agreement_ratio:.2f}")

        # 模拟观点更新（向均值靠拢）
        mean = np.mean(opinions)
        opinions = 0.7 * opinions + 0.3 * mean
        opinions += np.random.normal(0, 0.02, opinions.shape)
        opinions = np.clip(opinions, 0, 1)


def example_3_emergence_detection():
    """示例3：完整涌现检测"""
    print("\n" + "="*60)
    print("示例3：涌现检测")
    print("="*60)

    # 创建检测器
    detector = EmergenceDetector(n_agents=40, opinion_dim=1)

    # 创建初始观点（三个簇）
    initial = np.vstack([
        np.random.normal(0.25, 0.05, (15, 1)),
        np.random.normal(0.5, 0.05, (10, 1)),
        np.random.normal(0.75, 0.05, (15, 1))
    ])
    initial = np.clip(initial, 0, 1)

    # 创建简单的影响矩阵（环形网络）
    n = 40
    W = np.zeros((n, n))
    for i in range(n):
        W[i, i] = 0.5
        W[i, (i-1) % n] = 0.25
        W[i, (i+1) % n] = 0.25

    # 模拟并检测
    print("\n开始模拟...")
    current = initial.copy()

    for step in range(10):
        # DeGroot更新
        current = W @ current
        current = np.clip(current, 0, 1)

        # 检测涌现
        report = detector.detect_emergence(current, update_history=False)

        if step % 3 == 0:
            print(f"\n  步骤 {step}:")
            print(f"    阶段: {report.phase}")
            print(f"    类型: {report.emergence_type}")
            print(f"    强度: {report.emergence_strength:.3f}")
            print(f"    共识: {report.consensus.consensus_level:.3f}")
            print(f"    多样性: {report.diversity.entropy:.3f}")

    print("\n  检测完成！")


def example_4_compare_scenarios():
    """示例4：对比不同场景"""
    print("\n" + "="*60)
    print("示例4：对比不同场景")
    print("="*60)

    analyzer = ViewpointDiversity()

    scenarios = {
        "高多样性": np.random.uniform(0, 1, (100, 1)),
        "低多样性": np.clip(np.random.normal(0.5, 0.1, (100, 1)), 0, 1),
        "极化": np.vstack([
            np.random.normal(0.2, 0.05, (50, 1)),
            np.random.normal(0.8, 0.05, (50, 1))
        ])
    }

    print("\n场景对比：")
    print(f"{'场景':<12} {'熵':<8} {'极化':<8} {'簇数':<6}")
    print("-" * 40)

    for name, opinions in scenarios.items():
        opinions = np.clip(opinions, 0, 1)
        m = analyzer.compute_all_metrics(opinions)
        print(f"{name:<12} {m.entropy:<8.3f} {m.polarization:<8.3f} {m.cluster_count:<6}")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print(" " * 15 + "涌现检测 - 快速开始")
    print("="*60)

    examples = [
        ("基础多样性分析", example_1_basic_diversity),
        ("共识追踪", example_2_consensus_tracking),
        ("涌现检测", example_3_emergence_detection),
        ("场景对比", example_4_compare_scenarios),
    ]

    print("\n可用示例：")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n选择示例 (1-4) 或 'all' 运行全部：")
    choice = input("> ").strip()

    if choice.lower() == 'all':
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\n[错误] {name}: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        name, func = examples[int(choice) - 1]
        try:
            func()
        except Exception as e:
            print(f"\n[错误] {e}")
    else:
        print("无效选择")

    print("\n" + "="*60)
    print("示例运行完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
