"""
测试GLM Coding Plan连接

验证OpenAI协议接入是否正常工作
"""

import sys
import io
from pathlib import Path

# 修复Windows控制台编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_openai_client():
    """测试OpenAI客户端初始化"""
    print("测试1: OpenAI客户端初始化...")

    try:
        from openai import OpenAI
        from flow_system.config import Config

        client = OpenAI(
            api_key=Config.API_KEY or "sk-test",  # 使用测试密钥
            base_url=Config.BASE_URL
        )

        print(f"  ✓ 客户端创建成功")
        print(f"    - Base URL: {Config.BASE_URL}")
        print(f"    - 模型: {Config.MODEL_NAME}")
        return True

    except Exception as e:
        print(f"  ✗ 客户端创建失败: {e}")
        return False


def test_llm_engine_init():
    """测试LLM引擎初始化"""
    print("\n测试2: LLM引擎初始化...")

    try:
        from flow_system.llm_engine import LLMEngine

        engine = LLMEngine()

        print(f"  ✓ LLM引擎初始化成功")
        print(f"    - 缓存: {'启用' if engine.cache else '禁用'}")
        print(f"    - 线程池: {engine.executor._max_workers} workers")
        return True

    except Exception as e:
        print(f"  ✗ LLM引擎初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_validation():
    """测试配置验证"""
    print("\n测试3: 配置验证...")

    from flow_system.config import Config

    print(f"  模型配置:")
    print(f"    - MODEL_NAME: {Config.MODEL_NAME}")
    print(f"    - BASE_URL: {Config.BASE_URL}")
    print(f"    - EMBEDDING_MODEL: {Config.EMBEDDING_MODEL}")

    if Config.API_KEY:
        print(f"    - API_KEY: {'*' * 20}{Config.API_KEY[-8:]}")
    else:
        print(f"    ⚠️  API_KEY: 未配置")

    print(f"\n  端点验证:")
    if "coding/paas/v4" in Config.BASE_URL:
        print(f"    ✓ 使用GLM Coding Plan专属端点")
    else:
        print(f"    ⚠️  未使用GLM Coding Plan专属端点")
        print(f"    当前端点: {Config.BASE_URL}")
        print(f"    应该是: https://open.bigmodel.cn/api/coding/paas/v4")

    return True


async def test_api_call():
    """测试实际API调用（需要有效API密钥）"""
    print("\n测试4: API调用测试...")

    from flow_system.config import Config
    from flow_system.llm_engine import LLMEngine

    if not Config.API_KEY or Config.API_KEY == "your_api_key_here":
        print("  ⚠️  跳过: 未配置有效的API密钥")
        print("  请在 .env 文件中配置 ZHIPUAI_API_KEY")
        return False

    try:
        engine = LLMEngine()

        print("  正在调用API...")
        result = await engine.generate(
            prompt="Say 'Hello from GLM Coding Plan!'",
            sys_prompt="You are a helpful assistant.",
            temp=0.7,
            max_tokens=50
        )

        if result:
            print(f"  ✓ API调用成功!")
            print(f"    响应: {result[:100]}...")
            return True
        else:
            print(f"  ✗ API返回为空")
            return False

    except Exception as e:
        print(f"  ✗ API调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("GLM Coding Plan 连接测试")
    print("=" * 60)
    print()

    results = []

    # 基础测试（不需要API密钥）
    results.append(test_openai_client())
    results.append(test_llm_engine_init())
    results.append(test_config_validation())

    # API调用测试（需要API密钥）
    print("\n" + "=" * 60)
    print("API调用测试（需要有效API密钥）")
    print("=" * 60)

    import asyncio
    api_result = asyncio.run(test_api_call())
    results.append(api_result)

    # 总结
    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)

    if passed >= 3:  # 前3个基础测试都通过
        print(f"✅ 基础配置正确! ({passed}/{total} 测试通过)")
        print()

        if not api_result:
            print("⚠️  API调用测试未通过，请检查:")
            print("  1. 是否已订阅 GLM Coding Plan 套餐")
            print("  2. .env 文件中的 ZHIPUAI_API_KEY 是否正确")
            print("  3. 网络连接是否正常")
            print()
            print("配置指南: GLM_CODING_PLAN_SETUP.md")
        else:
            print("🎉 所有测试通过! 系统已就绪!")
            print()
            print("开始使用:")
            print("  python run.py")

        return True
    else:
        print(f"❌ 配置有问题! ({passed}/{total} 测试通过)")
        print()
        print("请检查配置，参考: GLM_CODING_PLAN_SETUP.md")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
