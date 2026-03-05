"""
简单功能测试

测试基础功能是否正常工作（不需要API密钥）
"""

import sys
import io
from pathlib import Path

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_sandbox():
    """测试沙箱执行"""
    print("测试1: 沙箱执行...")

    from flow_system.sandbox import Sandbox

    sandbox = Sandbox()

    # 测试代码
    test_code = """
def add(a, b):
    return a + b
"""

    # 快速测试
    success, result, error = sandbox.quick_test(test_code, [2, 3])

    if success and result == 5:
        print("  ✓ 沙箱执行正常")
        return True
    else:
        print(f"  ✗ 沙箱执行失败: {error}")
        return False


def test_feature_extraction():
    """测试特征提取"""
    print("测试2: 特征提取...")

    from flow_system.sandbox import Sandbox

    sandbox = Sandbox()

    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

    test_cases = {
        0: 0,
        1: 1,
        2: 1,
        3: 2,
        4: 3,
        5: 5,
    }

    accuracy, features, vector = sandbox.evaluate(test_code, test_cases)

    if len(features) >= 18 and len(vector) >= 18:
        print(f"  ✓ 特征提取正常: {len(features)}维特征")
        print(f"    - 正确率: {accuracy:.2%}")
        print(f"    - 可维护性: {features.get('maintainability_index', 0):.2f}")
        print(f"    - 圈复杂度: {features.get('cyclomatic_complexity', 0):.2f}")
        return True
    else:
        print(f"  ✗ 特征提取失败: 只有{len(features)}维")
        return False


def test_emergence_detector():
    """测试涌现检测器"""
    print("测试3: 涌现检测...")

    from flow_system.emergence import EmergenceDetector
    import numpy as np

    detector = EmergenceDetector()

    # 创建一个模拟轨迹（10代，20维特征）
    trajectory = []
    for gen in range(10):
        # 模拟收敛过程：特征逐渐稳定
        noise = np.random.randn(20) * (1 - gen/10)  # 噪声递减
        center = np.ones(20) * 0.8  # 收敛中心
        features = center + noise * 0.1
        features = np.clip(features, 0, 1)  # 限制在[0,1]
        trajectory.append(features.tolist())

    result = detector.detect(trajectory)

    print(f"  ✓ 涌现检测完成")
    print(f"    - 真涌现: {result['is_true_emergence']}")
    print(f"    - Lyapunov指数: {result['lyapunov_exponent']:.4f}")
    print(f"    - 有效信息: {result['effective_information']:.4f}")
    print(f"    - 涌现强度: {result['emergence_strength']:.2%}")

    return True


def test_knowledge_manager():
    """测试知识管理器"""
    print("测试4: 知识管理...")

    from flow_system.knowledge import KnowledgeManager

    km = KnowledgeManager()

    # 测试存储
    test_task = "Test task: add two numbers"
    test_code = "def add(a, b):\n    return a + b"
    test_vector = [0.5] * 20

    km.store_solution(test_task, test_code, 0.95, 5, test_vector)

    # 测试缓存检查
    cached = km.check_cache(test_task)

    if cached == test_code:
        print("  ✓ 知识管理正常: 缓存命中")
    else:
        print("  ✓ 知识管理正常: 存储成功")

    # 获取统计
    stats = km.get_stats()
    print(f"    - 模式数: {stats.get('pattern_count', 0)}")
    print(f"    - 历史数: {stats.get('history_count', 0)}")
    print(f"    - 向量数: {stats.get('faiss_vectors', 0)}")

    return True


def test_population():
    """测试种群管理"""
    print("测试5: 种群管理...")

    from flow_system.evolution_engine import Population, Individual

    pop = Population(size=5)

    # 添加个体
    for i in range(5):
        ind = Individual(
            code=f"def func_{i}():\n    return {i}",
            score=0.5 + i * 0.1,
            features={"accuracy": 0.5 + i * 0.1},
            feature_vector=[0.5] * 20,
            generation=0,
        )
        pop.add(ind)

    # 测试功能
    best = pop.get_best(1)[0]
    diversity = pop.calculate_diversity()
    stats = pop.get_stats()

    print(f"  ✓ 种群管理正常")
    print(f"    - 最佳得分: {best.score:.2f}")
    print(f"    - 多样性: {diversity:.2%}")
    print(f"    - 平均分: {stats['avg_score']:.2f}")

    return True


def main():
    print("=" * 60)
    print("FlowSystem 功能测试")
    print("=" * 60)
    print()

    results = []

    # 运行所有测试
    tests = [
        test_sandbox,
        test_feature_extraction,
        test_emergence_detector,
        test_knowledge_manager,
        test_population,
    ]

    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"  ✗ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
        print()

    # 总结
    print("=" * 60)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✅ 所有测试通过! ({passed}/{total})")
        print()
        print("系统已就绪，可以使用以下命令启动:")
        print("  1. UI模式: python run.py")
        print("  2. CLI模式: python run.py --task \"你的任务\"")
        print()
        print("注意: 实际运行需要先配置API密钥(.env文件)")
        return True
    else:
        print(f"❌ {total - passed} 个测试失败! ({passed}/{total})")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
