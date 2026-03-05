#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Brain - 任务理解与蓝图生成模块

用户通过自然语言描述任务，Brain 通过对话理解需求，自动生成任务蓝图。

使用方法:
    python brain.py                    # 交互式对话
    python brain.py "实现用户登录功能"  # 单任务模式
"""

import os
import sys
import json
import re
from pathlib import Path

# UTF-8 输出支持
if sys.platform == "win32":
    try:
        import io
        if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except (AttributeError, ValueError):
        pass

class Brain:
    def __init__(self):
        self.state_file = Path('.janus/project_state.json')
        self.current_blueprint = self.load_blueprint()

    def print_header(self):
        print('''
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        🧠 Brain - 任务理解与蓝图生成                             ║
║                                                                  ║
║        说出你的需求，我来帮你分析和规划                           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        ''')

    def load_blueprint(self):
        """加载现有蓝图"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('blueprint', [])
            except:
                return []
        return []

    def save_blueprint(self, blueprint):
        """保存蓝图"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        data = {'blueprint': blueprint}

        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f'\n✅ 蓝图已保存到: {self.state_file}')

    def analyze_task(self, user_input):
        """分析用户输入，提取任务信息"""
        print(f'\n🤔 正在分析任务...')

        # 提取任务关键信息
        task_info = {
            'task_name': '',
            'instruction': user_input,
            'target_files': [],
            'status': 'PENDING'
        }

        # 尝试提取任务名称（简化版，实际应该用 LLM）
        # 这里提供一个模板，可以被 Claude Code 在实际使用时智能填充

        return task_info

    def ask_clarification(self, task_info):
        """询问澄清问题"""
        print('\n' + '='*70)
        print('📋 任务理解')
        print('='*70)

        # 1. 任务名称
        if not task_info['task_name']:
            print('\n请为这个任务起一个简短的名称：')
            print('  例如: "实现用户登录"、"优化数据库查询"、"修复内存泄漏"')
            task_name = input('\n任务名称: ').strip()

            if not task_name:
                # 尝试从描述中提取
                task_name = self.extract_task_name(task_info['instruction'])

            task_info['task_name'] = task_name

        # 2. 详细指令
        print(f'\n任务: {task_info["task_name"]}')
        print(f'描述: {task_info["instruction"]}')

        print('\n需要补充更详细的实现要求吗？(留空跳过)')
        more_detail = input('补充说明: ').strip()

        if more_detail:
            task_info['instruction'] = f"{task_info['instruction']}。{more_detail}"

        # 3. 目标文件
        print('\n这个任务涉及哪些文件？')
        print('  提示: 用逗号分隔，例如: auth.py, models/user.py')
        print('  如果是新建文件，直接输入期望的文件名')

        files_input = input('\n目标文件: ').strip()

        if files_input:
            files = [f.strip() for f in files_input.split(',') if f.strip()]
            task_info['target_files'] = files
        else:
            # 尝试智能推测
            task_info['target_files'] = self.guess_target_files(task_info)

        return task_info

    def extract_task_name(self, instruction):
        """从指令中提取任务名称"""
        # 简化版：取前几个词
        words = instruction[:30]

        # 移除标点
        words = re.sub(r'[，。！？、,.!?]', '', words)

        return words if words else "未命名任务"

    def guess_target_files(self, task_info):
        """智能推测目标文件"""
        instruction = task_info['instruction'].lower()
        task_name = task_info['task_name'].lower()

        files = []

        # 关键词匹配
        keywords_map = {
            ('登录', 'login', '认证', 'auth'): ['auth.py', 'models/user.py'],
            ('数据库', 'database', 'db', 'sql'): ['database.py', 'models.py'],
            ('api', '接口', 'endpoint'): ['api.py', 'routes.py'],
            ('测试', 'test'): ['test_main.py'],
            ('配置', 'config'): ['config.py', 'settings.py'],
        }

        for keywords, suggested_files in keywords_map.items():
            if any(kw in instruction or kw in task_name for kw in keywords):
                files.extend(suggested_files)
                break

        return files[:2] if files else []

    def confirm_task(self, task_info):
        """确认任务信息"""
        print('\n' + '='*70)
        print('✅ 任务确认')
        print('='*70)

        print(f'\n📌 任务名称: {task_info["task_name"]}')
        print(f'📝 实现要求: {task_info["instruction"]}')
        print(f'📁 目标文件: {", ".join(task_info["target_files"]) if task_info["target_files"] else "待定"}')
        print(f'⏱️ 状态: {task_info["status"]}')

        print('\n这个任务理解正确吗？')
        print('  1. 正确，添加到蓝图')
        print('  2. 需要修改')
        print('  3. 取消')

        choice = input('\n请选择 (1-3): ').strip()

        return choice

    def modify_task(self, task_info):
        """修改任务信息"""
        print('\n请选择要修改的项目：')
        print('  1. 任务名称')
        print('  2. 实现要求')
        print('  3. 目标文件')
        print('  4. 返回')

        choice = input('\n请选择 (1-4): ').strip()

        if choice == '1':
            task_name = input('新的任务名称: ').strip()
            if task_name:
                task_info['task_name'] = task_name

        elif choice == '2':
            instruction = input('新的实现要求: ').strip()
            if instruction:
                task_info['instruction'] = instruction

        elif choice == '3':
            files = input('目标文件（逗号分隔）: ').strip()
            if files:
                task_info['target_files'] = [f.strip() for f in files.split(',')]

        return task_info

    def add_task_to_blueprint(self, task_info):
        """将任务添加到蓝图"""
        self.current_blueprint.append(task_info)
        self.save_blueprint(self.current_blueprint)

        print(f'\n✨ 任务已添加到蓝图！')
        print(f'   当前蓝图共有 {len(self.current_blueprint)} 个任务')

    def show_blueprint(self):
        """显示当前蓝图"""
        if not self.current_blueprint:
            print('\n📋 当前蓝图为空')
            return

        print('\n' + '='*70)
        print('📋 当前任务蓝图')
        print('='*70)

        for i, task in enumerate(self.current_blueprint, 1):
            status = task.get('status', 'PENDING')
            status_icon = {
                'PENDING': '⏳',
                'IN_PROGRESS': '🔄',
                'COMPLETED': '✅',
                'BLOCKED': '🚫'
            }.get(status, '❓')

            print(f'\n{i}. {status_icon} [{status}] {task.get("task_name", "未命名")}')
            print(f'   📝 {task.get("instruction", "")[:60]}...' if len(task.get("instruction", "")) > 60 else f'   📝 {task.get("instruction", "")}')

            if task.get('target_files'):
                print(f'   📁 {", ".join(task["target_files"])}')

    def interactive_mode(self):
        """交互式对话模式"""
        self.print_header()

        print('\n👋 你好！我是 Brain，来帮你规划任务。')
        print('\n你可以：')
        print('  - 直接描述任务（例如："实现用户登录功能"）')
        print('  - 输入 "show" 查看当前蓝图')
        print('  - 输入 "deploy" 部署第一个任务')
        print('  - 输入 "quit" 退出')

        while True:
            print('\n' + '-'*70)
            user_input = input('\n💬 你: ').strip()

            if not user_input:
                continue

            if user_input.lower() == 'quit':
                print('\n👋 再见！')
                break

            elif user_input.lower() == 'show':
                self.show_blueprint()
                continue

            elif user_input.lower() == 'deploy':
                self.deploy_first_task()
                continue

            elif user_input.lower() == 'help':
                self.print_help()
                continue

            # 处理任务输入
            self.process_task_input(user_input)

    def process_task_input(self, user_input):
        """处理任务输入"""
        # 1. 分析任务
        task_info = self.analyze_task(user_input)

        # 2. 询问澄清问题
        task_info = self.ask_clarification(task_info)

        # 3. 确认任务
        while True:
            choice = self.confirm_task(task_info)

            if choice == '1':
                # 添加到蓝图
                self.add_task_to_blueprint(task_info)
                break

            elif choice == '2':
                # 修改任务
                task_info = self.modify_task(task_info)

            elif choice == '3':
                # 取消
                print('\n❌ 已取消')
                break

            else:
                print('\n⚠️ 无效选择，请重新输入')

    def deploy_first_task(self):
        """部署第一个 PENDING 任务"""
        pending_tasks = [t for t in self.current_blueprint if t.get('status') == 'PENDING']

        if not pending_tasks:
            print('\n⚠️ 没有待处理的任务')
            return

        first_task = pending_tasks[0]

        print('\n' + '='*70)
        print('🚀 准备部署任务')
        print('='*70)

        print(f'\n📌 任务: {first_task["task_name"]}')
        print(f'📝 要求: {first_task["instruction"]}')

        print('\n即将调用 Dealer 生成指令...')
        print('\n请选择 Dealer 版本：')
        print('  1. 增强版（推荐，包含完整上下文）')
        print('  2. 简化版（快速轻量）')

        choice = input('\n请选择 (1-2): ').strip()

        if choice == '1':
            self.call_dealer('enhanced')
        elif choice == '2':
            self.call_dealer('simple')
        else:
            print('\n⚠️ 无效选择')

    def call_dealer(self, version='enhanced'):
        """调用 Dealer"""
        print(f'\n🔄 正在调用 Dealer {version}版...\n')

        import subprocess

        dealer_script = 'dealer_enhanced.py' if version == 'enhanced' else 'dealer.py'

        if not os.path.exists(dealer_script):
            print(f'\n⚠️ 找不到 {dealer_script}')
            return

        try:
            result = subprocess.run(
                [sys.executable, dealer_script],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            print(result.stdout)

            if result.returncode == 0:
                print('\n✅ Dealer 已生成指令并复制到剪贴板！')
                print('\n下一步：')
                print('  1. 粘贴指令给 Claude Code（Ctrl+V / Cmd+V）')
                print('  2. Claude Code 将自动执行任务')
            else:
                print(f'\n❌ Dealer 执行失败: {result.stderr}')

        except Exception as e:
            print(f'\n❌ 调用 Dealer 出错: {e}')

    def print_help(self):
        """打印帮助信息"""
        print('\n' + '='*70)
        print('📚 使用帮助')
        print('='*70)

        print('\n🎯 工作流程：')
        print('  1. 用自然语言描述任务')
        print('  2. 回答 Brain 的澄清问题')
        print('  3. 确认任务信息')
        print('  4. 任务添加到蓝图')
        print('  5. 输入 "deploy" 部署任务')
        print('  6. 将生成的指令粘贴给 Claude Code')

        print('\n💡 命令：')
        print('  show   - 查看当前任务蓝图')
        print('  deploy - 部署第一个待处理任务')
        print('  help   - 显示此帮助')
        print('  quit   - 退出')

        print('\n📝 示例：')
        print('  你: 实现用户登录功能')
        print('  Brain: [询问澄清问题...]')
        print('  你: [回答问题]')
        print('  Brain: [确认任务并添加到蓝图]')
        print('  你: deploy')
        print('  Brain: [调用 Dealer 生成指令]')

    def single_task_mode(self, task_description):
        """单任务模式（命令行参数）"""
        self.print_header()

        print(f'\n💬 用户输入: {task_description}')

        self.process_task_input(task_description)

        print('\n✅ 任务已添加到蓝图')
        print(f'   当前蓝图: {len(self.current_blueprint)} 个任务')

        print('\n要立即部署吗？(y/n): ', end='')
        choice = input().strip().lower()

        if choice == 'y':
            self.deploy_first_task()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Brain - 任务理解与蓝图生成模块',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python brain.py                        # 交互式对话模式
  python brain.py "实现用户登录功能"       # 单任务模式

工作流程:
  1. 用自然语言描述任务
  2. Brain 通过问题理解需求
  3. 自动生成任务蓝图
  4. 调用 Dealer 部署任务
        '''
    )

    parser.add_argument(
        'task',
        nargs='?',
        help='任务描述（单任务模式）'
    )

    args = parser.parse_args()

    brain = Brain()

    try:
        if args.task:
            # 单任务模式
            brain.single_task_mode(args.task)
        else:
            # 交互式模式
            brain.interactive_mode()

    except KeyboardInterrupt:
        print('\n\n👋 再见！')
        sys.exit(0)

    except Exception as e:
        print(f'\n❌ 出错: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
