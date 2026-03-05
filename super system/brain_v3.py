#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Brain v3.0 - 增强版任务理解与蓝图生成模块

集成功能:
- Compound Engineering方法论
- SpecKit规格驱动开发
- draw.io MCP可视化
- Context Engineering上下文管理
- 双记忆系统检索
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

# UTF-8 输出支持
if sys.platform == "win32":
    try:
        import io
        if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except (AttributeError, ValueError):
        pass

# 导入工具管理器
sys.path.append(str(Path(__file__).parent))
try:
    from .ralph.tools.tools_manager import get_tools_manager
    from .ralph.tools.memory_integrator import get_memory_integrator
except:
    try:
        sys.path.append(str(Path(__file__).parent / ".ralph" / "tools"))
        from tools_manager import get_tools_manager
        from memory_integrator import get_memory_integrator
    except:
        print("警告: 无法导入工具管理器，将使用基础功能")
        get_tools_manager = None
        get_memory_integrator = None


class CompoundEngineeringAgent:
    """Compound Engineering 代理模拟器"""

    def __init__(self):
        self.agents = {
            "req_dev": self._req_dev_agent,
            "brainstorm": self._brainstorm_agent,
            "design_review": self._design_review_agent
        }

    def _req_dev_agent(self, user_input: str) -> Dict:
        """需求分析代理"""
        return {
            "agent": "req_dev",
            "questions": [
                "这个功能的主要用户是谁？",
                "成功的标准是什么？",
                "有哪些边界情况需要考虑？",
                "依赖哪些外部系统？"
            ],
            "requirements": {
                "functional": [],
                "non_functional": [],
                "constraints": []
            }
        }

    def _brainstorm_agent(self, requirements: Dict) -> Dict:
        """头脑风暴代理"""
        return {
            "agent": "brainstorm",
            "design_options": [],
            "trade_offs": [],
            "recommendations": []
        }

    def _design_review_agent(self, design: Dict) -> Dict:
        """设计审查代理"""
        return {
            "agent": "design_review",
            "issues": [],
            "suggestions": [],
            "approved": False
        }

    def invoke(self, agent_name: str, *args, **kwargs) -> Dict:
        """调用指定代理"""
        if agent_name in self.agents:
            return self.agents[agent_name](*args, **kwargs)
        return {}


class SpecKitGenerator:
    """SpecKit规格生成器模拟"""

    def generate_spec(self, task_info: Dict) -> str:
        """生成规格文档"""
        spec = f"""# {task_info['task_name']} - 功能规格

## 概述
{task_info['instruction']}

## 输入
- 待定义

## 输出
- 待定义

## 业务规则
1. 待定义

## 技术约束
- 待定义

## 测试用例
- [ ] 正常情况测试
- [ ] 边界情况测试
- [ ] 错误处理测试

## 验收标准
- [ ] 功能完整实现
- [ ] 测试全部通过
- [ ] 代码审查通过
"""
        return spec


class DrawioMCPSimulator:
    """draw.io MCP 模拟器"""

    def create_flowchart(self, title: str, phases: List[Dict]) -> str:
        """生成流程图（模拟）"""
        diagram = f"# {title} 流程图\n\n"
        for i, phase in enumerate(phases, 1):
            diagram += f"{i}. {phase.get('task_name', '未命名阶段')}\n"
            diagram += f"   ↓\n"
        diagram += "完成\n"
        return diagram

    def save_diagram(self, diagram: str, filepath: str):
        """保存图表"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(diagram)
        print(f"✓ 流程图已保存: {filepath}")


class BrainV3:
    """Brain v3.0 - 增强版"""

    def __init__(self):
        self.state_file = Path('.janus/project_state.json')
        self.spec_dir = Path('.ralph/specs')
        self.diagram_dir = Path('.ralph/diagrams')
        self.context_dir = Path('.ralph/context')

        # 创建必要的目录
        self.spec_dir.mkdir(parents=True, exist_ok=True)
        self.diagram_dir.mkdir(parents=True, exist_ok=True)

        # 加载工具
        self.tools_manager = get_tools_manager() if get_tools_manager else None
        self.memory_integrator = get_memory_integrator() if get_memory_integrator else None

        # 集成的工具
        self.ce_agent = CompoundEngineeringAgent()
        self.speckit = SpecKitGenerator()
        self.drawio = DrawioMCPSimulator()

        self.current_blueprint = self.load_blueprint()

    def print_header(self):
        print('''
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        🧠 Brain v3.0 - 增强版任务规划系统                        ║
║                                                                  ║
║        集成功能:                                                  ║
║        • Compound Engineering 方法论                              ║
║        • SpecKit 规格驱动开发                                     ║
║        • draw.io 可视化生成                                       ║
║        • 双记忆系统检索                                           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        ''')

    def load_blueprint(self) -> List[Dict]:
        """加载现有蓝图"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('blueprint', [])
            except:
                return []
        return []

    def save_blueprint(self, blueprint: List[Dict]):
        """保存蓝图"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        data = {'blueprint': blueprint}

        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f'\n✅ 蓝图已保存到: {self.state_file}')

    def analyze_with_ce(self, user_input: str) -> Dict:
        """
        使用Compound Engineering的req-dev代理分析需求

        Args:
            user_input: 用户输入的需求描述

        Returns:
            需求分析结果
        """
        print('\n🤖 [Compound Engineering] 调用req-dev代理分析需求...')

        # 调用CE的req-dev代理
        analysis = self.ce_agent.invoke("req_dev", user_input)

        print('\n📊 需求分析结果:')
        for question in analysis.get('questions', []):
            print(f'   ❓ {question}')

        return analysis

    def generate_spec(self, task_info: Dict) -> str:
        """
        使用SpecKit生成规格文档

        Args:
            task_info: 任务信息

        Returns:
            规格文档内容
        """
        print('\n📝 [SpecKit] 生成规格文档...')

        spec = self.speckit.generate_spec(task_info)

        # 保存规格文档
        spec_file = self.spec_dir / f"{task_info['task_name']}.md"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec)

        print(f'✓ 规格文档已生成: {spec_file}')

        return spec

    def decompose_to_phases(self, task_info: Dict) -> List[Dict]:
        """
        分解任务为多个Phase

        Args:
            task_info: 任务信息

        Returns:
            Phase列表
        """
        print('\n🔨 分解任务为多个Phase...')

        # 简化版分解逻辑
        # 实际应该使用LLM智能分解
        phases = [
            {
                "task_name": f"{task_info['task_name']} - Phase 1: 核心功能实现",
                "instruction": task_info['instruction'],
                "target_files": task_info.get('target_files', []),
                "status": "PENDING"
            }
        ]

        print(f'✓ 已分解为 {len(phases)} 个Phase')
        for i, phase in enumerate(phases, 1):
            print(f'   Phase {i}: {phase["task_name"]}')

        return phases

    def generate_flowchart(self, blueprint: List[Dict]) -> str:
        """
        使用draw.io MCP生成流程图

        Args:
            blueprint: 任务蓝图

        Returns:
            流程图文件路径
        """
        print('\n📊 [draw.io MCP] 生成任务流程图...')

        # 生成流程图
        flowchart = self.drawio.create_flowchart(
            title="任务执行流程",
            phases=blueprint
        )

        # 保存流程图
        diagram_file = self.diagram_dir / "task-flow.txt"
        self.drawio.save_diagram(flowchart, str(diagram_file))

        return str(diagram_file)

    def retrieve_relevant_experience(self, task_name: str) -> Optional[str]:
        """
        从双记忆系统检索相关经验

        Args:
            task_name: 任务名称

        Returns:
            格式化的经验上下文
        """
        if not self.memory_integrator:
            return None

        print('\n🧠 从双记忆系统检索相关经验...')

        try:
            results = self.memory_integrator.retrieve_combined(task_name, top_k=3)
            context = self.memory_integrator.format_for_context(results)

            hippo_count = len(results.get('hippocampus', []))
            claudemem_count = len(results.get('claude_mem', []))

            print(f'✓ 找到相关经验:')
            print(f'   - Hippocampus: {hippo_count}条')
            print(f'   - claude-mem: {claudemem_count}条')

            return context if context.strip() else None
        except Exception as e:
            print(f'⚠ 经验检索失败: {e}')
            return None

    def review_phase_output(self, phase: Dict, output_files: List[str]) -> bool:
        """
        Phase间审查产出质量

        Args:
            phase: Phase信息
            output_files: 产出文件列表

        Returns:
            是否通过审查
        """
        print(f'\n🔍 审查 Phase 产出质量...')
        print(f'   Phase: {phase["task_name"]}')
        print(f'   产出文件: {len(output_files)}个')

        # 检查清单
        checks = {
            "文件完整性": self._check_files_complete(phase, output_files),
            "代码质量": self._check_code_quality(output_files),
            "接口一致性": self._check_interface_consistency(output_files)
        }

        print('\n审查结果:')
        all_passed = True
        for check_name, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f'   {status} {check_name}')
            if not passed:
                all_passed = False

        return all_passed

    def _check_files_complete(self, phase: Dict, output_files: List[str]) -> bool:
        """检查文件是否齐全"""
        target_files = phase.get('target_files', [])
        if not target_files:
            return True  # 没有指定目标文件

        # 检查是否都已创建
        for target in target_files:
            if target not in output_files:
                print(f'     ⚠ 缺少文件: {target}')
                return False

        return True

    def _check_code_quality(self, output_files: List[str]) -> bool:
        """检查代码质量（简化版）"""
        # 这里应该调用Superpowers的code-review
        # 简化版只做基础检查
        return True

    def _check_interface_consistency(self, output_files: List[str]) -> bool:
        """检查接口一致性"""
        # 简化版
        return True

    def plan_task(self, user_input: str) -> List[Dict]:
        """
        完整的任务规划流程

        Args:
            user_input: 用户输入

        Returns:
            生成的蓝图
        """
        print('\n' + '='*70)
        print('🚀 开始任务规划流程')
        print('='*70)

        # Step 1: 使用CE的req-dev分析需求
        ce_analysis = self.analyze_with_ce(user_input)

        # Step 2: 构建任务信息
        task_info = {
            'task_name': self._extract_task_name(user_input),
            'instruction': user_input,
            'target_files': [],
            'ce_analysis': ce_analysis,
            'status': 'PENDING'
        }

        print(f'\n📋 任务名称: {task_info["task_name"]}')

        # Step 3: 使用SpecKit生成规格
        spec = self.generate_spec(task_info)
        task_info['spec_file'] = str(self.spec_dir / f"{task_info['task_name']}.md")

        # Step 4: 分解为多个Phase
        phases = self.decompose_to_phases(task_info)

        # Step 5: 生成流程图
        flowchart_file = self.generate_flowchart(phases)

        # Step 6: 检索相关经验
        experience_context = self.retrieve_relevant_experience(task_info['task_name'])
        if experience_context:
            task_info['relevant_experience'] = experience_context

        # Step 7: 保存蓝图
        self.save_blueprint(phases)

        print('\n' + '='*70)
        print('✅ 任务规划完成')
        print('='*70)
        print(f'\n📁 生成的文件:')
        print(f'   - 蓝图: {self.state_file}')
        print(f'   - 规格: {task_info.get("spec_file", "N/A")}')
        print(f'   - 流程图: {flowchart_file}')

        return phases

    def _extract_task_name(self, user_input: str) -> str:
        """从用户输入提取任务名称"""
        # 简化版：取前20个字符
        name = user_input[:20]
        if len(user_input) > 20:
            name += "..."
        return name

    def interactive_mode(self):
        """交互式模式"""
        self.print_header()

        print('\n请描述你想要完成的任务：')
        print('（输入 "quit" 或 "exit" 退出）\n')

        while True:
            try:
                user_input = input('💬 你: ').strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print('\n👋 再见！')
                    break

                # 规划任务
                blueprint = self.plan_task(user_input)

                print('\n' + '='*70)
                print('🎯 下一步操作:')
                print('='*70)
                print('\n1. 运行 Dealer 生成详细指令:')
                print('   python dealer_enhanced.py')
                print('\n2. 或者直接让 Worker 执行:')
                print('   [启动 Ralph 自动执行]')
                print('\n' + '='*70)

                break  # 规划完一个任务后退出

            except KeyboardInterrupt:
                print('\n\n👋 再见！')
                break
            except Exception as e:
                print(f'\n❌ 错误: {e}')
                import traceback
                traceback.print_exc()


def main():
    """主函数"""
    brain = BrainV3()

    # 检查命令行参数
    if len(sys.argv) > 1:
        # 单任务模式
        user_input = ' '.join(sys.argv[1:])
        brain.plan_task(user_input)
    else:
        # 交互式模式
        brain.interactive_mode()


if __name__ == '__main__':
    main()
