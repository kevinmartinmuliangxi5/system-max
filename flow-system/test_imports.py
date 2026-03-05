"""
导入测试脚本

验证所有模块是否可以正确导入
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

def test_imports():
    """测试所有导入"""
    errors = []

    # 测试基础模块
    try:
        from flow_system.config import Config, AdaptiveConfig
        print("✓ config.py")
    except Exception as e:
        errors.append(f"config.py: {e}")
        print(f"✗ config.py: {e}")

    try:
        from flow_system.utils import logger, timeit, get_cache_key
        print("✓ utils.py")
    except Exception as e:
        errors.append(f"utils.py: {e}")
        print(f"✗ utils.py: {e}")

    # 测试LLM引擎
    try:
        from flow_system.llm_engine import LLMEngine, SQLiteCache
        print("✓ llm_engine.py")
    except Exception as e:
        errors.append(f"llm_engine.py: {e}")
        print(f"✗ llm_engine.py: {e}")

    # 测试沙箱
    try:
        from flow_system.sandbox import Sandbox, CodeExecutor, FeatureExtractor
        print("✓ sandbox.py")
    except Exception as e:
        errors.append(f"sandbox.py: {e}")
        print(f"✗ sandbox.py: {e}")

    # 测试涌现检测
    try:
        from flow_system.emergence import (
            EmergenceDetector,
            TakensEmbedding,
            LyapunovCalculator,
            EffectiveInformation,
            DownwardCausation,
        )
        print("✓ emergence.py")
    except Exception as e:
        errors.append(f"emergence.py: {e}")
        print(f"✗ emergence.py: {e}")

    # 测试知识库
    try:
        from flow_system.knowledge import (
            KnowledgeManager,
            PatternLibrary,
            FAISSRetriever,
        )
        print("✓ knowledge.py")
    except Exception as e:
        errors.append(f"knowledge.py: {e}")
        print(f"✗ knowledge.py: {e}")

    # 测试演化引擎
    try:
        from flow_system.evolution_engine import (
            EvolutionEngine,
            Individual,
            Population,
        )
        print("✓ evolution_engine.py")
    except Exception as e:
        errors.append(f"evolution_engine.py: {e}")
        print(f"✗ evolution_engine.py: {e}")

    # 测试主程序
    try:
        from flow_system.main import main, run_ui, run_cli
        print("✓ main.py")
    except Exception as e:
        errors.append(f"main.py: {e}")
        print(f"✗ main.py: {e}")

    # 测试包导入
    try:
        import flow_system
        print(f"✓ flow_system package (version: {flow_system.__version__})")
    except Exception as e:
        errors.append(f"flow_system package: {e}")
        print(f"✗ flow_system package: {e}")

    # 总结
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ {len(errors)} 个模块导入失败:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ 所有模块导入成功!")
        return True


def test_config_validation():
    """测试配置验证"""
    print("\n" + "=" * 60)
    print("测试配置验证...")

    try:
        from flow_system.config import Config

        # 不验证API_KEY（可能未设置）
        print(f"  BASE_DIR: {Config.BASE_DIR}")
        print(f"  DATA_DIR: {Config.DATA_DIR}")
        print(f"  MODEL: {Config.MODEL_NAME}")
        print(f"  PLATFORM: {Config.PLATFORM}")
        print(f"  CPU_COUNT: {Config.CPU_COUNT}")
        print(f"  POPULATION_SIZE: {Config.POPULATION_SIZE}")
        print(f"  MAX_GENERATIONS: {Config.MAX_GENERATIONS}")
        print("✓ 配置加载成功")
        return True

    except Exception as e:
        print(f"✗ 配置验证失败: {e}")
        return False


def test_directory_structure():
    """测试目录结构"""
    print("\n" + "=" * 60)
    print("测试目录结构...")

    base = Path(__file__).parent
    required_dirs = [
        base / "src" / "flow_system",
        base / "data",
        base / "logs",
        base / "checkpoints",
    ]

    all_ok = True
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"  ✓ {dir_path.relative_to(base)}")
        else:
            print(f"  ✗ {dir_path.relative_to(base)} (不存在)")
            all_ok = False

    # 检查.gitkeep文件
    gitkeep_files = [
        base / "data" / ".gitkeep",
        base / "logs" / ".gitkeep",
        base / "checkpoints" / ".gitkeep",
        base / "data" / "faiss_index" / ".gitkeep",
    ]

    for file_path in gitkeep_files:
        if file_path.exists():
            print(f"  ✓ {file_path.relative_to(base)}")
        else:
            print(f"  ✗ {file_path.relative_to(base)} (不存在)")
            all_ok = False

    if all_ok:
        print("✓ 目录结构完整")
    else:
        print("⚠️  部分目录或文件缺失")

    return all_ok


if __name__ == "__main__":
    print("FlowSystem 导入测试")
    print("=" * 60)

    success = True

    # 1. 测试导入
    if not test_imports():
        success = False

    # 2. 测试配置
    if not test_config_validation():
        success = False

    # 3. 测试目录
    if not test_directory_structure():
        success = False

    # 最终结果
    print("\n" + "=" * 60)
    if success:
        print("✅ 所有测试通过! 系统准备就绪.")
        print("\n下一步:")
        print("  1. 安装依赖: pip install -r requirements.txt")
        print("  2. 配置API密钥: 编辑 .env 文件")
        print("  3. 运行系统: python run.py")
    else:
        print("❌ 部分测试失败，请检查错误信息")

    sys.exit(0 if success else 1)
