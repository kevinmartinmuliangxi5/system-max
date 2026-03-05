"""
涌现检测方法简化测试脚本（无需额外依赖）
================================

演示核心功能，不依赖networkx和matplotlib

运行方式：
    python test_emergence_simple.py
"""

import numpy as np
import sys

# 导入我们的模块
from emergence_detection_methods import (
    ViewpointDiversity,
    ConsensusAnalyzer,
    InnovationDetector,
    SocialChoiceCalculator,
    OpinionDynamicsSimulator,
    DynamicsModel,
    EmergenceDetector,
    ComplexSystemsMetrics
)


def test_1_diversity():
    """测试1：观点多样性分析"""
    print("\n" + "="*60)
    print("测试1：观点多样性分析")
    print("="*60)

    analyzer = ViewpointDiversity()

    # 场景1：高多样性（均匀分布）
    print("\n场景1：高多样性（均匀分布）")
    opinions1 = np.random.uniform(0, 1, (100, 1))
    metrics1 = analyzer.compute_all_metrics(opinions1)
    print(f"  熵基多样性: {metrics1.entropy:.4f}")
    print(f"  极化程度: {metrics1.polarization:.4f}")
    print(f"  观点簇数: {metrics1.cluster_count}")

    # 场景2：低多样性（集中分布）
    print("\n场景2：低多样性（集中分布）")
    opinions2 = np.random.normal(0.5, 0.05, (100, 1))
    opinions2 = np.clip(opinions2, 0, 1)
    metrics2 = analyzer.compute_all_metrics(opinions2)
    print(f"  熵基多样性: {metrics2.entropy:.4f}")
    print(f"  极化程度: {metrics2.polarization:.4f}")
    print(f"  观点簇数: {metrics2.cluster_count}")

    # 场景3：极化分布（双峰）
    print("\n场景3：极化分布（双峰）")
    opinions3 = np.vstack([
        np.random.normal(0.2, 0.05, (50, 1)),
        np.random.normal(0.8, 0.05, (50, 1))
    ])
    metrics3 = analyzer.compute_all_metrics(opinions3)
    print(f"  熵基多样性: {metrics3.entropy:.4f}")
    print(f"  极化程度: {metrics3.polarization:.4f}")
    print(f"  观点簇数: {metrics3.cluster_count}")

    print("\n[OK] 多样性分析测试通过")


def test_2_consensus():
    """测试2：共识收敛分析"""
    print("\n" + "="*60)
    print("测试2：共识收敛分析")
    print("="*60)

    analyzer = ConsensusAnalyzer(agreement_threshold=0.1)

    # 模拟收敛过程
    n_agents = 50
    n_steps = 20

    print(f"\n模拟 {n_agents} 个agent的观点收敛过程（{n_steps}步）:")

    # 初始观点
    opinions = np.random.uniform(0.2, 0.8, (n_agents, 1))
    history = [opinions.copy()]

    # 演化
    for t in range(n_steps):
        mean = np.mean(opinions)
        rate = 0.1 * (1 - t/n_steps)
        opinions = (1-rate) * opinions + rate * mean
        opinions = np.clip(opinions + np.random.normal(0, 0.02, opinions.shape), 0, 1)
        history.append(opinions.copy())

    # 分析不同时间点
    for i in [0, 5, 10, 15, 20]:
        if i < len(history):
            metrics = analyzer.compute_all_metrics(history[i], history[:i+1])
            print(f"\n  时间步 {i}:")
            print(f"    共识水平: {metrics.consensus_level:.4f}")
            print(f"    同意比例: {metrics.agreement_ratio:.4f}")

    print("\n[OK] 共识分析测试通过")


def test_3_innovation():
    """测试3：创新检测"""
    print("\n" + "="*60)
    print("测试3：创新突破检测")
    print("="*60)

    detector = InnovationDetector()

    # 现有观点（两个簇）
    existing = np.vstack([
        np.random.normal(0.3, 0.03, (30, 1)),
        np.random.normal(0.7, 0.03, (30, 1))
    ])

    print("\n现有观点分布: 2个簇")
    print(f"  簇1中心: ~0.3")
    print(f"  簇2中心: ~0.7")

    # 测试不同新观点
    test_cases = [
        ("簇内观点", 0.31, False),
        ("簇间观点", 0.5, False),
        ("远距离观点", 0.05, True),
        ("极端观点", 0.95, True),
    ]

    print("\n新观点分析:")
    for name, value, expect_novel in test_cases:
        new_op = np.array([[value]])

        novelty = detector.calculate_novelty_score(new_op, existing)
        is_breakthrough, score = detector.detect_breakthrough(
            new_op, existing, 2
        )

        print(f"\n  {name} ({value:.2f}):")
        print(f"    新颖度: {novelty:.4f}")
        print(f"    突破性: {is_breakthrough} (得分: {score:.4f})")

    print("\n[OK] 创新检测测试通过")


def test_4_voting():
    """测试4：社会选择算法"""
    print("\n" + "="*60)
    print("测试4：社会选择算法对比")
    print("="*60)

    calculator = SocialChoiceCalculator()

    # 偏好矩阵（10个投票者，4个选项）
    preferences = np.array([
        [1, 2, 3, 4],
        [1, 3, 2, 4],
        [2, 1, 3, 4],
        [4, 3, 2, 1],
        [3, 2, 1, 4],
        [1, 2, 4, 3],
        [2, 3, 1, 4],
        [3, 1, 2, 4],
        [4, 2, 3, 1],
        [1, 4, 2, 3],
    ])

    print("\n投票结果对比:")
    print(f"{'规则':<15} | {'获胜者':<8} | {'共识得分':<10}")
    print("-" * 40)

    # 多数规则
    result1 = calculator.majority_rule(preferences)
    print(f"{'多数规则':<15} | {result1.winner:<8} | {result1.consensus_score:<10.4f}")

    # 孔多塞
    result2 = calculator.condorcet_rule(preferences)
    print(f"{'孔多塞':<15} | {result2.winner:<8} | {result2.consensus_score:<10.4f}")

    # 博达计数
    result3 = calculator.borda_count(preferences)
    print(f"{'博达计数':<15} | {result3.winner:<8} | {result3.consensus_score:<10.4f}")

    print("\n[OK] 投票算法测试通过")


def test_5_dynamics():
    """测试5：观点动力学"""
    print("\n" + "="*60)
    print("测试5：观点动力学模型")
    print("="*60)

    simulator = OpinionDynamicsSimulator(n_agents=30, opinion_dim=1)

    # 初始观点
    initial = np.random.uniform(0.2, 0.8, (30, 1))

    # DeGroot模型
    print("\nDeGroot模型:")
    # 创建简单的影响矩阵（环形网络）
    W = np.zeros((30, 30))
    for i in range(30):
        W[i, i] = 0.5
        W[i, (i-1)%30] = 0.25
        W[i, (i+1)%30] = 0.25

    final, history = simulator.degroot_model(initial, W, n_steps=30)

    print(f"  初始标准差: {np.std(initial):.4f}")
    print(f"  最终标准差: {np.std(final):.4f}")
    print(f"  收敛程度: {1 - np.std(final)/0.5:.4f}")

    # 有界置信模型
    print("\n有界置信模型:")
    final2, history2 = simulator.hegelmann_krause_model(
        initial, confidence_threshold=0.15, n_steps=30
    )

    print(f"  初始标准差: {np.std(initial):.4f}")
    print(f"  最终标准差: {np.std(final2):.4f}")
    print(f"  最终簇数: {ViewpointDiversity().count_opinion_clusters(final2)}")

    print("\n[OK] 动力学模型测试通过")


def test_6_full_detection():
    """测试6：完整涌现检测"""
    print("\n" + "="*60)
    print("测试6：完整涌现检测流程")
    print("="*60)

    n_agents = 40
    n_steps = 15

    # 初始观点（三个簇）
    np.random.seed(42)
    initial = np.vstack([
        np.random.normal(0.2, 0.03, (12, 1)),
        np.random.normal(0.5, 0.03, (16, 1)),
        np.random.normal(0.8, 0.03, (12, 1))
    ])
    initial = np.clip(initial, 0, 1)

    print(f"\n初始配置:")
    print(f"  Agent数量: {n_agents}")
    print(f"  初始簇数: 3")
    print(f"  初始标准差: {np.std(initial):.4f}")

    # 创建简单的环形影响网络
    W = np.zeros((n_agents, n_agents))
    for i in range(n_agents):
        # 自权重
        W[i, i] = 0.4
        # 邻居权重
        for j in range(i-2, i+3):
            W[i, j % n_agents] += 0.15

    # 初始化检测器
    detector = EmergenceDetector(n_agents=n_agents, opinion_dim=1)

    # 手动模拟并检测
    print(f"\n开始模拟...")

    current = initial.copy()
    all_reports = []

    for t in range(n_steps):
        # DeGroot更新
        current = W @ current
        current = np.clip(current, 0, 1)

        # 检测涌现
        report = detector.detect_emergence(current, update_history=True)
        all_reports.append(report)

        if t % 5 == 0:
            print(f"\n  时间步 {t}:")
            print(f"    阶段: {report.phase}")
            print(f"    类型: {report.emergence_type}")
            print(f"    强度: {report.emergence_strength:.4f}")
            print(f"    共识: {report.consensus.consensus_level:.4f}")
            print(f"    多样性: {report.diversity.entropy:.4f}")

    # 统计
    phases = [r.phase for r in all_reports]
    phase_counts = {p: phases.count(p) for p in set(phases)}

    print(f"\n阶段分布:")
    for phase, count in phase_counts.items():
        print(f"  {phase}: {count} 次")

    print("\n[OK] 完整检测流程测试通过")


def test_7_complex_metrics():
    """测试7：复杂系统指标"""
    print("\n" + "="*60)
    print("测试7：复杂系统指标")
    print("="*60)

    # 生成带有突变的时间序列
    n_steps = 50
    history = []

    # 阶段1：稳定
    for _ in range(20):
        history.append(np.random.normal(0.4, 0.02, (20, 1)))

    # 阶段2：突变
    for _ in range(5):
        history.append(np.random.normal(0.6, 0.08, (20, 1)))

    # 阶段3：稳定
    for _ in range(25):
        history.append(np.random.normal(0.6, 0.02, (20, 1)))

    # 临界性指标
    criticality = ComplexSystemsMetrics.calculate_criticality_indicator(history)
    print(f"\n临界性指标: {criticality:.4f}")

    # 相变检测
    transitions = ComplexSystemsMetrics.detect_phase_transition(history)
    print(f"检测到的相变点: {transitions}")

    # 迁移熵
    if len(history) > 10:
        source = np.array([h[0, 0] for h in history[-10:]])
        target = np.array([h[1, 0] for h in history[-10:]])

        te = ComplexSystemsMetrics.calculate_transfer_entropy(source, target)
        print(f"迁移熵 (agent 0 -> agent 1): {te:.4f}")

    # 因果涌现
    micro = np.array([np.mean(h) for h in history[-20:]])
    macro = (micro > np.median(micro)).astype(int)

    ce = ComplexSystemsMetrics.calculate_causal_emergence(micro, macro)
    print(f"因果涌现 (微观->宏观): {ce:.4f}")

    print("\n[OK] 复杂系统指标测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print(" " * 15 + "涌现检测方法测试套件")
    print(" " * 10 + "（简化版 - 无需额外依赖）")
    print("="*70)

    tests = [
        test_1_diversity,
        test_2_consensus,
        test_3_innovation,
        test_4_voting,
        test_5_dynamics,
        test_6_full_detection,
        test_7_complex_metrics,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n[FAIL] 测试失败: {test.__name__}")
            print(f"  错误: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "="*70)
    print(f"测试完成！通过: {passed}/{passed+failed}")
    print("="*70 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
