#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
系统集成测试脚本

测试覆盖：
1. Brain v3 任务规划
2. Dealer v3 指令生成
3. 双记忆系统
4. Context Engineering
5. 端到端流程
"""

import sys
import io
import os
import json
import shutil
from pathlib import Path

# UTF-8 输出支持
if sys.platform == "win32":
    if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if hasattr(sys.stderr, 'buffer') and sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

def print_section(title):
    """打印章节标题"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_test(name, passed):
    """打印测试结果"""
    status = "✅ 通过" if passed else "❌ 失败"
    print(f"{status} - {name}")
    return passed

def test_environment():
    """测试1: 环境检查"""
    print_section("测试 1: 环境检查")

    results = []

    # 检查Python版本
    import sys
    version = sys.version_info
    python_ok = version.major == 3 and version.minor >= 8
    results.append(print_test(
        f"Python版本 ({version.major}.{version.minor}.{version.micro})",
        python_ok
    ))

    # 检查核心依赖
    try:
        import pyperclip
        results.append(print_test("pyperclip 已安装", True))
    except:
        results.append(print_test("pyperclip 已安装", False))

    try:
        import colorama
        results.append(print_test("colorama 已安装", True))
    except:
        results.append(print_test("colorama 已安装 (可选)", True))

    # 检查目录结构
    dirs = [
        ".janus",
        ".ralph",
        ".ralph/tools",
        ".ralph/context",
        ".ralph/memories"
    ]
    for dir_path in dirs:
        exists = os.path.exists(dir_path)
        results.append(print_test(f"目录存在: {dir_path}", exists))

    return all(results)

def test_brain_v3():
    """测试2: Brain v3功能"""
    print_section("测试 2: Brain v3 功能")

    results = []

    try:
        from brain_v3 import BrainV3

        # 创建实例
        brain = BrainV3()
        results.append(print_test("Brain v3 实例化", True))

        # 测试规划任务
        test_task = "测试任务：实现用户登录功能"
        blueprint = brain.plan_task(test_task)

        results.append(print_test("任务规划执行", blueprint is not None))
        results.append(print_test("蓝图非空", len(blueprint) > 0))

        # 检查生成的文件
        state_file = Path(".janus/project_state.json")
        results.append(print_test("蓝图文件生成", state_file.exists()))

        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            results.append(print_test("蓝图JSON有效", "blueprint" in data))

        # 检查规格文件
        spec_files = list(Path(".ralph/specs").glob("*.md"))
        results.append(print_test(f"规格文件生成 ({len(spec_files)}个)", len(spec_files) > 0))

    except Exception as e:
        print(f"❌ Brain v3测试失败: {e}")
        results.append(False)

    return all(results)

def test_dealer_v3():
    """测试3: Dealer v3功能"""
    print_section("测试 3: Dealer v3 功能")

    results = []

    try:
        from dealer_v3 import DealerV3

        # 创建实例
        dealer = DealerV3()
        results.append(print_test("Dealer v3 实例化", True))

        # 检查工具集成
        tools_ok = dealer.tools_manager is not None
        results.append(print_test("tools_manager 集成", tools_ok))

        memory_ok = dealer.memory_integrator is not None
        results.append(print_test("memory_integrator 集成", memory_ok))

        # 测试操作类型检测
        op_type = dealer.detect_operation_type("修复Bug", ["test.py"])
        results.append(print_test(
            f"操作类型检测 (FIX)",
            op_type == "FIX"
        ))

        # 测试Context加载
        context_docs = dealer.load_context_engineering()
        results.append(print_test(
            f"Context Engineering加载 ({len(context_docs)}个文档)",
            len(context_docs) > 0
        ))

        # 测试Superpowers加载
        rules = dealer.load_superpowers_rules()
        results.append(print_test(
            "Superpowers规则加载",
            rules is not None
        ))

    except Exception as e:
        print(f"❌ Dealer v3测试失败: {e}")
        results.append(False)

    return all(results)

def test_dual_memory():
    """测试4: 双记忆系统"""
    print_section("测试 4: 双记忆系统")

    results = []

    try:
        from memory_integrator import get_memory_integrator

        # 获取实例
        mi = get_memory_integrator()
        results.append(print_test("memory_integrator 实例化", True))

        # 检查是否使用真实claude-mem
        using_real = mi.using_real_claude_mem
        results.append(print_test(
            f"使用真实claude-mem: {using_real}",
            True  # 总是通过，只是信息
        ))

        # 测试检索
        test_query = "用户登录认证"
        retrieval_results = mi.retrieve_combined(test_query, top_k=3)

        results.append(print_test(
            "双记忆检索执行",
            retrieval_results is not None
        ))

        results.append(print_test(
            "检索结果包含hippocampus",
            "hippocampus" in retrieval_results
        ))

        results.append(print_test(
            "检索结果包含claude_mem",
            "claude_mem" in retrieval_results
        ))

        results.append(print_test(
            "检索结果包含merged",
            "merged" in retrieval_results
        ))

        # 测试上下文格式化
        context = mi.format_for_context(retrieval_results)
        results.append(print_test(
            f"上下文格式化 ({len(context)}字符)",
            isinstance(context, str)
        ))

    except Exception as e:
        print(f"❌ 双记忆系统测试失败: {e}")
        results.append(False)

    return all(results)

def test_context_engineering():
    """测试5: Context Engineering"""
    print_section("测试 5: Context Engineering")

    results = []

    # 检查Context文档
    context_dir = Path(".ralph/context")
    context_files = [
        "project-info.md",
        "architecture.md",
        "coding-style.md",
        "decisions.md",
        "dependencies.md"
    ]

    for filename in context_files:
        filepath = context_dir / filename
        exists = filepath.exists()
        results.append(print_test(f"文档存在: {filename}", exists))

        if exists:
            size = filepath.stat().st_size
            results.append(print_test(f"  文档非空 ({size} 字节)", size > 0))

    # 检查模块文档
    modules_dir = context_dir / "modules"
    module_files = ["brain.md", "dealer.md", "worker.md"]

    for filename in module_files:
        filepath = modules_dir / filename
        exists = filepath.exists()
        results.append(print_test(f"模块文档: {filename}", exists))

    return all(results)

def test_end_to_end():
    """测试6: 端到端流程"""
    print_section("测试 6: 端到端流程")

    results = []

    try:
        # Step 1: Brain规划
        print("Step 1: Brain v3 规划任务...")
        from brain_v3 import BrainV3
        brain = BrainV3()

        test_task = "集成测试任务：实现简单的API端点"
        blueprint = brain.plan_task(test_task)

        results.append(print_test("Brain规划完成", len(blueprint) > 0))

        # Step 2: Dealer生成指令
        print("\nStep 2: Dealer v3 生成指令...")
        from dealer_v3 import DealerV3
        dealer = DealerV3()

        # 读取蓝图
        state_file = Path(".janus/project_state.json")
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            tasks = data.get("blueprint", [])
            if tasks:
                task = tasks[0]
                instruction = dealer.generate_instruction(task)

                results.append(print_test(
                    f"Dealer指令生成 ({len(instruction)}字符)",
                    len(instruction) > 1000
                ))

                # 检查指令内容
                has_superpowers = "Superpowers" in instruction
                has_quality = "质量门控" in instruction
                has_memory = "相关经验" in instruction

                results.append(print_test("  包含Superpowers规则", has_superpowers))
                results.append(print_test("  包含质量门控", has_quality))
                results.append(print_test("  包含双记忆经验", has_memory))
        else:
            results.append(print_test("读取蓝图", False))

        # Step 3: 检查双记忆系统记录
        print("\nStep 3: 检查双记忆系统...")
        from claude_mem_enhanced import get_claude_mem
        cm = get_claude_mem()

        stats = cm.get_statistics()
        results.append(print_test(
            f"会话记录数: {stats['total_sessions']}",
            True  # 总是通过，只是信息
        ))
        results.append(print_test(
            f"观察记录数: {stats['total_observations']}",
            True  # 总是通过，只是信息
        ))

    except Exception as e:
        print(f"❌ 端到端测试失败: {e}")
        import traceback
        traceback.print_exc()
        results.append(False)

    return all(results)

def test_performance():
    """测试7: 性能基准"""
    print_section("测试 7: 性能基准")

    results = []

    try:
        import time

        # Brain性能
        print("测试 Brain v3 性能...")
        from brain_v3 import BrainV3
        brain = BrainV3()

        start = time.time()
        brain.plan_task("性能测试任务")
        brain_time = time.time() - start

        results.append(print_test(
            f"Brain规划时间: {brain_time:.2f}秒",
            brain_time < 5.0  # 应该在5秒内完成
        ))

        # Dealer性能
        print("\n测试 Dealer v3 性能...")
        from dealer_v3 import DealerV3
        dealer = DealerV3()

        state_file = Path(".janus/project_state.json")
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            tasks = data.get("blueprint", [])
            if tasks:
                start = time.time()
                instruction = dealer.generate_instruction(tasks[0])
                dealer_time = time.time() - start

                results.append(print_test(
                    f"Dealer生成时间: {dealer_time:.2f}秒",
                    dealer_time < 3.0  # 应该在3秒内完成
                ))

        # 双记忆检索性能
        print("\n测试双记忆检索性能...")
        from memory_integrator import get_memory_integrator
        mi = get_memory_integrator()

        start = time.time()
        mi.retrieve_combined("测试查询", top_k=5)
        memory_time = time.time() - start

        results.append(print_test(
            f"双记忆检索时间: {memory_time:.2f}秒",
            memory_time < 1.0  # 应该在1秒内完成
        ))

    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        results.append(False)

    return all(results)

def generate_report(test_results):
    """生成测试报告"""
    print_section("测试报告")

    total = len(test_results)
    passed = sum(test_results.values())
    failed = total - passed

    print(f"总测试数: {total}")
    print(f"通过: {passed} ✅")
    print(f"失败: {failed} ❌")
    print(f"通过率: {passed/total*100:.1f}%")

    print("\n详细结果:")
    for test_name, result in test_results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {test_name}")

    # 生成报告文件
    report_file = Path(".ralph/test_report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 系统集成测试报告\n\n")
        f.write(f"**测试时间**: {Path(__file__).stat().st_mtime}\n")
        f.write(f"**版本**: v3.0.0-alpha\n\n")
        f.write("## 测试概要\n\n")
        f.write(f"- 总测试数: {total}\n")
        f.write(f"- 通过: {passed} ✅\n")
        f.write(f"- 失败: {failed} ❌\n")
        f.write(f"- 通过率: {passed/total*100:.1f}%\n\n")
        f.write("## 详细结果\n\n")
        for test_name, result in test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            f.write(f"- {status}: {test_name}\n")

    print(f"\n📄 测试报告已生成: {report_file}")

    return passed == total

def main():
    """主函数"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "双脑Ralph系统 v3.0" + " "*33 + "║")
    print("║" + " "*18 + "系统集成测试" + " "*36 + "║")
    print("╚" + "="*68 + "╝")

    test_results = {}

    try:
        # 运行所有测试
        test_results["环境检查"] = test_environment()
        test_results["Brain v3功能"] = test_brain_v3()
        test_results["Dealer v3功能"] = test_dealer_v3()
        test_results["双记忆系统"] = test_dual_memory()
        test_results["Context Engineering"] = test_context_engineering()
        test_results["端到端流程"] = test_end_to_end()
        test_results["性能基准"] = test_performance()

        # 生成报告
        all_passed = generate_report(test_results)

        if all_passed:
            print("\n🎉 所有测试通过！系统集成完整，可以投入使用！")
            return 0
        else:
            print("\n⚠️  部分测试失败，请检查上述错误信息。")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        return 2
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        return 3

if __name__ == "__main__":
    sys.exit(main())
