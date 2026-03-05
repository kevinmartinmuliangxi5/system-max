"""
涌现检测方法测试和演示脚本
================================

本脚本提供了完整的示例代码，演示如何使用涌现检测方法。
包括：
1. 基础功能测试
2. 观点动力学模拟
3. 涌现检测案例分析
4. 可视化演示

运行方式：
    python test_emergence_detection.py
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
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


# ============================================================================
# 测试1：观点多样性分析
# ============================================================================

def test_diversity_analysis():
    """测试观点多样性指标"""
    print("\n" + "="*60)
    print("测试1：观点多样性分析")
    print("="*60)

    # 创建不同分布的观点
    scenarios = {
        "高多样性（均匀分布）": np.random.uniform(0, 1, (100, 1)),
        "低多样性（集中分布）": np.random.normal(0.5, 0.05, (100, 1)),
        "双峰分布（极化）": np.concatenate([
            np.random.normal(0.2, 0.05, (50, 1)),
            np.random.normal(0.8, 0.05, (50, 1))
        ]),
        "多峰分布（碎片化）": np.concatenate([
            np.random.normal(0.15, 0.03, (25, 1)),
            np.random.normal(0.4, 0.03, (25, 1)),
            np.random.normal(0.65, 0.03, (25, 1)),
            np.random.normal(0.9, 0.03, (25, 1))
        ])
    }

    diversity_analyzer = ViewpointDiversity()

    for name, opinions in scenarios.items():
        opinions = np.clip(opinions, 0, 1)
        metrics = diversity_analyzer.compute_all_metrics(opinions)

        print(f"\n场景：{name}")
        print(f"  - 熵基多样性: {metrics.entropy:.4f}")
        print(f"  - Simpson指数: {metrics.variance:.4f}")
        print(f"  - 离散度: {metrics.dispersion:.4f}")
        print(f"  - 极化程度: {metrics.polarization:.4f}")
        print(f"  - 观点簇数: {metrics.cluster_count}")
        print(f"  - 有效多样性: {metrics.effective_diversity:.4f}")


# ============================================================================
# 测试2：共识收敛分析
# ============================================================================

def test_consensus_analysis():
    """测试共识收敛指标"""
    print("\n" + "="*60)
    print("测试2：共识收敛分析")
    print("="*60)

    # 模拟观点收敛过程
    n_steps = 30
    n_agents = 50

    # 初始：随机观点
    initial_opinions = np.random.uniform(0.2, 0.8, (n_agents, 1))

    # 模拟收敛：逐步向均值靠拢
    opinion_history = []
    current_opinions = initial_opinions.copy()

    for t in range(n_steps):
        # 添加噪声和收敛趋势
        noise = np.random.normal(0, 0.05, (n_agents, 1))
        convergence_rate = 0.1 * (1 - t/n_steps)  # 收敛率递减
        mean_opinion = np.mean(current_opinions)

        current_opinions = (1 - convergence_rate) * current_opinions + \
                          convergence_rate * mean_opinion + noise
        current_opinions = np.clip(current_opinions, 0, 1)

        opinion_history.append(current_opinions.copy())

    # 分析共识
    consensus_analyzer = ConsensusAnalyzer(agreement_threshold=0.15)

    print("\n共识演化：")
    for i in [0, n_steps//4, n_steps//2, 3*n_steps//4, n_steps-1]:
        metrics = consensus_analyzer.compute_all_metrics(
            opinion_history[i],
            opinion_history[:i+1]
        )
        print(f"\n  时间步 {i}:")
        print(f"    - 共识水平: {metrics.consensus_level:.4f}")
        print(f"    - 收敛速率: {metrics.convergence_rate:.4f}")
        print(f"    - 同意比例: {metrics.agreement_ratio:.4f}")
        print(f"    - 簇间分离度: {metrics.cluster_separation:.4f}")
        print(f"    - 稳定性指数: {metrics.stability_index:.4f}")


# ============================================================================
# 测试3：创新检测
# ============================================================================

def test_innovation_detection():
    """测试创新突破检测"""
    print("\n" + "="*60)
    print("测试3：创新突破检测")
    print("="*60)

    # 现有观点（两个聚类）
    existing_opinions = np.vstack([
        np.random.normal(0.3, 0.05, (30, 1)),
        np.random.normal(0.7, 0.05, (30, 1))
    ])

    # 测试不同类型的新观点
    new_opinions = {
        "常规观点（簇内）": np.array([[0.32]]),
        "中间观点（簇间）": np.array([[0.5]]),
        "远距离观点（新颖）": np.array([[0.05]]),
        "突破性观点（新簇）": np.array([[0.95]])
    }

    innovation_detector = InnovationDetector(novelty_threshold=2.0)
    diversity = ViewpointDiversity()
    existing_clusters = diversity.count_opinion_clusters(existing_opinions)

    print(f"\n现有观点簇数: {existing_clusters}")
    print("\n新观点分析：")

    for name, new_opinion in new_opinions.items():
        novelty = innovation_detector.calculate_novelty_score(
            new_opinion, existing_opinions
        )

        is_breakthrough, breakthrough_score = innovation_detector.detect_breakthrough(
            new_opinion, existing_opinions, existing_clusters
        )

        print(f"\n  {name}:")
        print(f"    - 新颖度: {novelty:.4f}")
        print(f"    - 是否突破: {is_breakthrough}")
        print(f"    - 突破得分: {breakthrough_score:.4f}")


# ============================================================================
# 测试4：社会选择算法
# ============================================================================

def test_social_choice():
    """测试社会选择算法"""
    print("\n" + "="*60)
    print("测试4：社会选择算法对比")
    print("="*60)

    # 创建偏好矩阵（10个投票者，4个选项）
    np.random.seed(42)
    preferences = np.array([
        [1, 2, 3, 4],  # 投票者1
        [1, 3, 2, 4],  # 投票者2
        [2, 1, 3, 4],  # 投票者3
        [4, 3, 2, 1],  # 投票者4
        [3, 2, 1, 4],  # 投票者5
        [1, 2, 4, 3],  # 投票者6
        [2, 3, 1, 4],  # 投票者7
        [3, 1, 2, 4],  # 投票者8
        [4, 2, 3, 1],  # 投票者9
        [1, 4, 2, 3],  # 投票者10
    ])

    calculator = SocialChoiceCalculator()

    print("\n投票规则对比：")
    print(f"{'规则':<20} {'获胜者':<10} {'共识得分':<15} {'社会福利':<15}")
    print("-" * 60)

    methods = [
        ("多数规则", calculator.majority_rule),
        ("孔多塞", calculator.condorcet_rule),
        ("博达计数", calculator.borda_count),
        ("批准投票", lambda p: calculator.approval_voting(p, threshold=0.6)),
    ]

    for name, method in methods:
        result = method(preferences)
        print(f"{name:<20} {result.winner:<10} {result.consensus_score:<15.4f} "
              f"{result.social_welfare:<15.4f}")


# ============================================================================
# 测试5：观点动力学模拟
# ============================================================================

def test_opinion_dynamics():
    """测试观点动力学模型"""
    print("\n" + "="*60)
    print("测试5：观点动力学模拟")
    print("="*60)

    n_agents = 50
    n_steps = 50

    # 初始观点
    initial_opinions = np.random.uniform(0.2, 0.8, (n_agents, 1))

    # 创建网络
    network = nx.watts_strogatz_graph(n_agents, k=4, p=0.1)

    # 初始化模拟器
    simulator = OpinionDynamicsSimulator(n_agents, opinion_dim=1)

    # 测试不同模型
    models = [
        ("DeGroot模型", DynamicsModel.DEGROOT, {}),
        ("有界置信模型", DynamicsModel.HEGSELMANN_KRAUSE,
         {"confidence_threshold": 0.15})
    ]

    for model_name, model_type, params in models:
        print(f"\n{model_name}:")

        if model_type == DynamicsModel.DEGROOT:
            # 构建影响矩阵
            adj_matrix = nx.adjacency_matrix(network).toarray()
            influence_matrix = adj_matrix / (adj_matrix.sum(axis=1, keepdims=True) + 1e-10)
            influence_matrix = np.nan_to_num(influence_matrix, nan=0.0)

            final_opinions, history = simulator.degroot_model(
                initial_opinions, influence_matrix, n_steps=n_steps
            )
        else:
            final_opinions, history = simulator.hegelmann_krause_model(
                initial_opinions, **params, n_steps=n_steps
            )

        # 分析结果
        initial_std = np.std(initial_opinions)
        final_std = np.std(final_opinions)
        n_clusters = ViewpointDiversity().count_opinion_clusters(final_opinions)

        print(f"  - 初始标准差: {initial_std:.4f}")
        print(f"  - 最终标准差: {final_std:.4f}")
        print(f"  - 收敛程度: {(1 - final_std/0.5):.4f}")
        print(f"  - 最终簇数: {n_clusters}")


# ============================================================================
# 测试6：完整涌现检测流程
# ============================================================================

def test_full_emergence_detection():
    """完整的涌现检测流程"""
    print("\n" + "="*60)
    print("测试6：完整涌现检测流程")
    print("="*60)

    # 设置
    n_agents = 50
    n_steps = 30
    np.random.seed(123)

    # 初始观点（三个簇）
    initial_opinions = np.vstack([
        np.random.normal(0.2, 0.05, (15, 1)),
        np.random.normal(0.5, 0.05, (20, 1)),
        np.random.normal(0.8, 0.05, (15, 1))
    ])
    initial_opinions = np.clip(initial_opinions, 0, 1)

    # 创建网络
    network = nx.watts_strogatz_graph(n_agents, k=6, p=0.2)

    # 初始化检测器
    detector = EmergenceDetector(n_agents=n_agents, opinion_dim=1)

    # 模拟并检测
    print("\n开始模拟...")
    reports = detector.simulate_and_detect(
        initial_opinions=initial_opinions,
        network=network,
        model=DynamicsModel.DEGROOT,
        n_steps=n_steps,
        detection_interval=3
    )

    # 分析结果
    print(f"\n完成！共检测 {len(reports)} 个时间点")
    print("\n涌现演化总结：")

    # 统计各阶段出现次数
    phases = [r.phase for r in reports]
    emergence_types = [r.emergence_type for r in reports]

    phase_counts = {p: phases.count(p) for p in set(phases)}
    type_counts = {t: emergence_types.count(t) for t in set(emergence_types)}

    print("\n阶段分布:")
    for phase, count in phase_counts.items():
        print(f"  - {phase}: {count} 次")

    print("\n涌现类型分布:")
    for etype, count in type_counts.items():
        print(f"  - {etype}: {count} 次")

    # 找出关键涌现时刻
    print("\n关键涌现时刻（涌现强度 > 0.5）:")
    for i, report in enumerate(reports):
        if report.emergence_strength > 0.5:
            print(f"  时间 {i*3}: 类型={report.emergence_type}, "
                  f"阶段={report.phase}, 强度={report.emergence_strength:.4f}")

    # 检测相变点
    all_opinions = [initial_opinions]  # 简化版本
    transitions = ComplexSystemsMetrics.detect_phase_transition(all_opinions)
    if transitions:
        print(f"\n检测到 {len(transitions)} 个相变点")
    else:
        print("\n未检测到明显相变点")

    # 可视化
    print("\n生成可视化...")
    try:
        detector.visualize_emergence(
            reports,
            save_path="emergence_demo.png"
        )
        print("可视化已保存到 emergence_demo.png")
    except Exception as e:
        print(f"可视化失败: {e}")


# ============================================================================
# 测试7：复杂系统指标
# ============================================================================

def test_complex_systems_metrics():
    """测试复杂系统相关指标"""
    print("\n" + "="*60)
    print("测试7：复杂系统指标")
    print("="*60)

    # 生成模拟数据（包含相变）
    n_steps = 100
    n_agents = 50

    opinion_history = []
    current = np.random.uniform(0.3, 0.4, (n_agents, 1))

    # 阶段1：探索
    for t in range(30):
        current = current + np.random.normal(0, 0.02, current.shape)
        current = np.clip(current, 0, 1)
        opinion_history.append(current.copy())

    # 阶段2：相变（快速变化）
    for t in range(10):
        current = current + np.random.normal(0.05, 0.05, current.shape)
        current = np.clip(current, 0, 1)
        opinion_history.append(current.copy())

    # 阶段3：稳定
    for t in range(60):
        current = current + np.random.normal(0, 0.005, current.shape)
        current = np.clip(current, 0, 1)
        opinion_history.append(current.copy())

    # 计算指标
    criticality = ComplexSystemsMetrics.calculate_criticality_indicator(
        opinion_history, window=20
    )

    transitions = ComplexSystemsMetrics.detect_phase_transition(
        opinion_history, threshold=0.3
    )

    print(f"\n临界性指标: {criticality:.4f}")
    print(f"检测到的相变点: {transitions}")

    # 计算迁移熵（简化示例）
    if len(opinion_history) > 10:
        # 使用第一个agent的观点作为示例
        source = opinion_history[-20:][:, 0, 0]  # 源序列
        target = opinion_history[-20:][:, 1, 0]  # 目标序列

        te = ComplexSystemsMetrics.calculate_transfer_entropy(source, target)
        print(f"\n迁移熵（agent 0 -> agent 1）: {te:.4f}")

    # 计算因果涌现（微观到宏观）
    micro_states = np.array([np.mean(op) for op in opinion_history[-20:]])
    # 宏观状态：二值化（高/低）
    macro_states = (micro_states > np.median(micro_states)).astype(int)

    ce = ComplexSystemsMetrics.calculate_causal_emergence(
        micro_states, macro_states
    )
    print(f"因果涌现（微观->宏观）: {ce:.4f}")
    if ce > 0:
        print("  -> 宏观尺度具有更强的因果效力！")


# ============================================================================
# 测试8：多维度观点空间
# ============================================================================

def test_multidimensional_opinions():
    """测试高维观点空间"""
    print("\n" + "="*60)
    print("测试8：多维度观点空间")
    print("="*60)

    n_agents = 100
    opinion_dim = 5

    # 生成高维观点（带相关性）
    mean = np.zeros(opinion_dim)
    cov = np.eye(opinion_dim) * 0.1

    # 三个簇
    opinions = np.vstack([
        np.random.multivariate_normal(mean + np.array([0.2]*opinion_dim), cov, 30),
        np.random.multivariate_normal(mean + np.array([0.5]*opinion_dim), cov, 40),
        np.random.multivariate_normal(mean + np.array([0.8]*opinion_dim), cov, 30)
    ])
    opinions = np.clip(opinions, 0, 1)

    # 分析
    diversity = ViewpointDiversity(viewpoint_dim=opinion_dim)
    diversity_metrics = diversity.compute_all_metrics(opinions)

    print(f"\n{opinion_dim}维观点空间的多样性分析:")
    print(f"  - 熵基多样性: {diversity_metrics.entropy:.4f}")
    print(f"  - 空间离散度: {diversity_metrics.dispersion:.4f}")
    print(f"  - 观点簇数: {diversity_metrics.cluster_count}")

    # PCA降维可视化
    pca = PCA(n_components=2)
    opinions_2d = pca.fit_transform(opinions)

    print(f"\nPCA分析:")
    print(f"  - 第一主成分解释方差: {pca.explained_variance_ratio_[0]:.4f}")
    print(f"  - 第二主成分解释方差: {pca.explained_variance_ratio_[1]:.4f}")
    print(f"  - 累计解释方差: {sum(pca.explained_variance_ratio_):.4f}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """运行所有测试"""
    print("\n" + "="*70)
    print(" " * 15 + "涌现检测方法测试套件")
    print("="*70)

    tests = [
        ("观点多样性分析", test_diversity_analysis),
        ("共识收敛分析", test_consensus_analysis),
        ("创新检测", test_innovation_detection),
        ("社会选择算法", test_social_choice),
        ("观点动力学模拟", test_opinion_dynamics),
        ("完整涌现检测", test_full_emergence_detection),
        ("复杂系统指标", test_complex_systems_metrics),
        ("多维度观点空间", test_multidimensional_opinions),
    ]

    print("\n可用测试:")
    for i, (name, _) in enumerate(tests, 1):
        print(f"  {i}. {name}")

    print("\n选择测试 (1-8, 或 'all' 运行全部):")
    choice = input("> ").strip()

    if choice.lower() == 'all':
        for name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"\n测试 '{name}' 失败: {e}")
                import traceback
                traceback.print_exc()
    elif choice.isdigit() and 1 <= int(choice) <= len(tests):
        name, test_func = tests[int(choice) - 1]
        try:
            test_func()
        except Exception as e:
            print(f"\n测试失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("无效选择！")

    print("\n" + "="*70)
    print("测试完成！")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
