#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dealer v3.0 - 增强版指令生成器

集成功能:
- tools_manager: 工具管理和Superpowers规则
- memory_integrator: 双记忆系统检索
- Context Engineering: 结构化上下文注入
- Compound Engineering: 质量门控
"""

import json
import os
import sys
import pyperclip
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# UTF-8 输出支持
if sys.platform == "win32":
    import io
    if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 颜色支持
try:
    from colorama import init, Fore
    init(autoreset=True)
except:
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = ""

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.janus'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.ralph', 'tools'))

# 导入原有模块
from core.router import TaskRouter
from core.hippocampus import Hippocampus
from core.thinkbank import ThinkBank
from core.cache_manager import CacheManager

# 导入v3.0新模块
try:
    from tools_manager import get_tools_manager
    from memory_integrator import get_memory_integrator
    TOOLS_V3_AVAILABLE = True
except ImportError:
    print(Fore.YELLOW + "警告: 无法导入v3.0工具，将使用基础功能")
    TOOLS_V3_AVAILABLE = False


STATE_FILE = ".janus/project_state.json"
CONTEXT_DIR = Path(".ralph/context")
SUPERPOWERS_RULES_FILE = Path(".ralph/tools/superpowers_rules.md")


class DealerV3:
    """Dealer v3.0 - 增强版"""

    def __init__(self):
        """初始化Dealer v3"""
        # 原有组件
        self.router = TaskRouter()
        self.hippocampus = Hippocampus()
        self.thinkbank = ThinkBank()
        self.cache = CacheManager()

        # v3.0组件
        if TOOLS_V3_AVAILABLE:
            self.tools_manager = get_tools_manager()
            self.memory_integrator = get_memory_integrator()
            print(Fore.GREEN + "✓ 已加载v3.0增强功能")
        else:
            self.tools_manager = None
            self.memory_integrator = None
            print(Fore.YELLOW + "⚠ 使用基础Dealer功能")

    def detect_operation_type(self, instruction: str, files: List[str]) -> str:
        """
        检测操作类型

        Args:
            instruction: 任务指令
            files: 目标文件列表

        Returns:
            操作类型: CREATE, MODIFY, FIX, REFACTOR, OPTIMIZE
        """
        instr_lower = instruction.lower()
        files_exist = all(os.path.exists(f) for f in files if f)

        # 关键词匹配
        if any(kw in instr_lower for kw in ['新建', '创建', 'create', 'new', 'add']):
            if not files_exist:
                return "CREATE"

        if any(kw in instr_lower for kw in ['重构', 'refactor', '重写', 'rewrite']):
            return "REFACTOR"

        if any(kw in instr_lower for kw in ['修复', 'fix', 'bug', '调试', 'debug']):
            return "FIX"

        if any(kw in instr_lower for kw in ['优化', 'optimize', '改进', 'improve']):
            return "OPTIMIZE"

        return "MODIFY" if files_exist else "CREATE"

    def get_file_info(self, filepath: str) -> Dict:
        """
        获取文件信息

        Args:
            filepath: 文件路径

        Returns:
            文件信息字典
        """
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                lines = content.split('\n')
                return {
                    'exists': True,
                    'lines': len(lines),
                    'size': len(content),
                    'preview': '\n'.join(lines[:30])  # v3.0: 增加到30行
                }
            except:
                return {'exists': True, 'lines': 0, 'size': 0, 'error': 'read_failed'}

        return {'exists': False}

    def load_context_engineering(self) -> Dict[str, str]:
        """
        加载Context Engineering文档

        Returns:
            上下文文档字典
        """
        context_docs = {}

        if not CONTEXT_DIR.exists():
            return context_docs

        # 加载关键文档
        doc_files = {
            "project_info": "project-info.md",
            "architecture": "architecture.md",
            "coding_style": "coding-style.md"
        }

        for key, filename in doc_files.items():
            filepath = CONTEXT_DIR / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        context_docs[key] = f.read()
                except:
                    pass

        return context_docs

    def load_superpowers_rules(self) -> Optional[str]:
        """
        加载Superpowers规则

        Returns:
            规则文本
        """
        if not SUPERPOWERS_RULES_FILE.exists():
            return None

        try:
            with open(SUPERPOWERS_RULES_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return None

    def retrieve_dual_memory(self, query: str) -> Dict:
        """
        从双记忆系统检索

        Args:
            query: 查询字符串

        Returns:
            检索结果
        """
        if not self.memory_integrator:
            # 降级：仅使用Hippocampus
            hippo_results = self.hippocampus.retrieve(query)
            return {
                "source": "hippocampus_only",
                "hippocampus": hippo_results,
                "claude_mem": [],
                "merged": hippo_results
            }

        # 使用双记忆系统
        return self.memory_integrator.retrieve_combined(query, top_k=5)

    def format_memory_context(self, memory_results: Dict) -> str:
        """
        格式化记忆为上下文

        Args:
            memory_results: retrieve_dual_memory的结果

        Returns:
            格式化的Markdown文本
        """
        if not self.memory_integrator:
            # 降级：简单格式化Hippocampus
            hippo_results = memory_results.get("hippocampus", [])
            if not hippo_results:
                return "无相关历史经验。"

            context = []
            for i, insight in enumerate(hippo_results, 1):
                context.append(f"{i}. **{insight.get('p', '问题')}**")
                context.append(f"   {insight.get('s', '解决方案')}")
                if insight.get('w'):
                    context.append(f"   ⚠️ {insight['w']}")
                context.append("")

            return "\n".join(context)

        # 使用memory_integrator格式化
        return self.memory_integrator.format_for_context(memory_results)

    def check_quality_gates(self, op_type: str, task: Dict) -> List[str]:
        """
        检查Compound Engineering质量门控

        Args:
            op_type: 操作类型
            task: 任务信息

        Returns:
            质量检查项列表
        """
        if not self.tools_manager:
            return []

        # 获取质量门控配置
        config = self.tools_manager.config.get("tools", {}).get("compound_engineering", {})
        quality_gates = config.get("quality_gates", {})

        # 根据阶段返回检查项
        gates = {
            "CREATE": quality_gates.get("planning", []),
            "MODIFY": quality_gates.get("execution", []),
            "FIX": quality_gates.get("execution", []),
            "REFACTOR": quality_gates.get("review", []),
            "OPTIMIZE": quality_gates.get("review", [])
        }

        return gates.get(op_type, [])

    def should_trigger_skills(self, op_type: str) -> Dict[str, bool]:
        """
        判断是否应触发技能

        Args:
            op_type: 操作类型

        Returns:
            技能触发字典
        """
        if not self.tools_manager:
            return {}

        skills = {}

        # 代码审查
        context = {"action": "code_change"}
        skills["code_review"] = self.tools_manager.should_trigger_skill("code_review", context)

        # 测试
        if op_type in ["CREATE", "MODIFY"]:
            context = {"action": "new_feature"}
            skills["testing"] = self.tools_manager.should_trigger_skill("testing", context)

        # 调试
        if op_type == "FIX":
            context = {"action": "bug"}
            skills["debugging"] = self.tools_manager.should_trigger_skill("debugging", context)

        return skills

    def generate_instruction(self, task: Dict) -> str:
        """
        生成增强版指令

        Args:
            task: 任务信息

        Returns:
            完整指令文本
        """
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "🔨 Dealer v3.0 - 生成增强版指令")
        print(Fore.CYAN + "="*70 + "\n")

        # 1. 基础信息
        task_name = task.get('task_name', '未命名任务')
        instruction = task.get('instruction', '')
        files = task.get('target_files', [])

        print(Fore.YELLOW + f"📋 任务: {task_name}")
        print(Fore.WHITE + f"📝 指令: {instruction[:60]}...")

        # 2. 路由与角色
        category, role_prompt = self.router.route(task_name, instruction, files)
        print(Fore.MAGENTA + f"🎭 角色: {role_prompt}")

        # 3. 操作类型检测
        op_type = self.detect_operation_type(instruction, files)
        print(Fore.BLUE + f"📦 操作类型: {op_type}")

        # 4. 文件信息
        files_info = {f: self.get_file_info(f) for f in files}
        exists_count = sum(1 for info in files_info.values() if info.get('exists'))
        print(Fore.GREEN + f"📁 目标文件: {len(files)} 个 (存在: {exists_count})")

        # 5. 双记忆检索
        print(Fore.CYAN + "🧠 检索双记忆系统...")
        memory_results = self.retrieve_dual_memory(task_name)
        memory_context = self.format_memory_context(memory_results)

        # 6. Context Engineering
        print(Fore.CYAN + "📚 加载Context Engineering文档...")
        context_docs = self.load_context_engineering()

        # 7. Superpowers规则
        print(Fore.CYAN + "⚡ 加载Superpowers规则...")
        superpowers_rules = self.load_superpowers_rules()

        # 8. 质量门控
        quality_gates = self.check_quality_gates(op_type, task)

        # 9. 技能触发
        triggered_skills = self.should_trigger_skills(op_type)

        # 10. 思考库决策
        decisions = self.thinkbank.get_latest_context()

        print(Fore.GREEN + "✓ 上下文收集完成\n")
        print(Fore.CYAN + "="*70)
        print(Fore.CYAN + "📝 生成指令...")
        print(Fore.CYAN + "="*70 + "\n")

        # ========== 生成Prompt ==========

        prompt = f"""# 🎯 任务执行指令 (Dealer v3.0)

## 📋 任务概览

**角色**: {role_prompt}
**任务名称**: {task_name}
**操作类型**: {op_type}
**任务类别**: {category}

---

## 📝 任务详情

### 目标
{instruction}

### 目标文件
"""

        # 文件列表
        for f, info in files_info.items():
            if info.get('exists'):
                prompt += f"\n- `{f}` (✓ 已存在, {info.get('lines', 0)} 行)"
            else:
                prompt += f"\n- `{f}` (✗ 需要创建)"

        # 当前文件内容
        prompt += "\n\n---\n\n## 📁 当前文件内容\n"

        for f, info in files_info.items():
            if info.get('exists') and not info.get('error'):
                prompt += f"\n### {f}\n\n```python\n{info.get('preview', '')}\n```\n"
                if info.get('lines', 0) > 30:
                    prompt += f"\n*（显示前 30 行，共 {info['lines']} 行）*\n"
            elif info.get('exists') and info.get('error'):
                prompt += f"\n### {f}\n\n⚠️ 文件存在但读取失败\n"
            else:
                prompt += f"\n### {f}\n\n📝 文件不存在，需要创建\n"

        # Context Engineering - 项目信息
        if context_docs.get("project_info"):
            prompt += "\n---\n\n## 🏗️ 项目信息 (Context Engineering)\n\n"
            # 只显示关键部分
            project_info = context_docs["project_info"]
            # 提取技术栈部分
            if "## 技术栈" in project_info:
                tech_stack_start = project_info.find("## 技术栈")
                tech_stack_end = project_info.find("\n## ", tech_stack_start + 1)
                if tech_stack_end > tech_stack_start:
                    prompt += project_info[tech_stack_start:tech_stack_end]
                else:
                    prompt += project_info[tech_stack_start:tech_stack_start+500]

        # Context Engineering - 编码规范
        if context_docs.get("coding_style"):
            prompt += "\n---\n\n## 📐 编码规范 (Context Engineering)\n\n"
            coding_style = context_docs["coding_style"]
            # 提取Python规范部分
            if "### Python代码规范" in coding_style:
                python_start = coding_style.find("### Python代码规范")
                python_end = coding_style.find("\n## ", python_start + 1)
                if python_end > python_start:
                    prompt += coding_style[python_start:python_end]
                else:
                    prompt += coding_style[python_start:python_start+800]

        # 双记忆系统检索结果
        prompt += "\n---\n\n## 💡 相关经验 (双记忆系统)\n\n"
        prompt += memory_context

        # 思考库决策
        if decisions:
            prompt += f"\n---\n\n## 🧠 项目决策 (思考库)\n\n{decisions}\n"

        # Superpowers Bright-Line Rules
        if superpowers_rules:
            prompt += "\n---\n\n## ⚡ Superpowers质量纪律\n\n"
            # 提取Bright-Line Rules部分
            if "## Bright-Line Rules" in superpowers_rules:
                rules_start = superpowers_rules.find("## Bright-Line Rules")
                rules_end = superpowers_rules.find("\n## ", rules_start + 1)
                if rules_end > rules_start:
                    prompt += superpowers_rules[rules_start:rules_end]
                else:
                    prompt += superpowers_rules[rules_start:rules_start+600]
            else:
                prompt += superpowers_rules[:500]

        # 质量门控
        if quality_gates:
            prompt += "\n---\n\n## 🚦 质量门控 (Compound Engineering)\n\n"
            prompt += "请确保通过以下质量检查:\n\n"
            for gate in quality_gates:
                prompt += f"- [ ] {gate}\n"

        # 成功标准（根据操作类型）
        prompt += "\n---\n\n## ✅ 成功标准\n\n"

        if op_type == "CREATE":
            prompt += """1. ✓ 创建所有目标文件，使用正确的文件路径
2. ✓ 实现所有必需的功能和方法
3. ✓ 添加完整的文档字符串和必要注释
4. ✓ 代码符合Python规范和项目规范
5. ✓ 处理错误情况和边界条件
6. ✓ 代码可直接运行，无语法错误
"""
        elif op_type == "FIX":
            prompt += """1. ✓ 准确定位并修复bug
2. ✓ 添加注释说明修复内容和原因
3. ✓ 确保不引入新的问题
4. ✓ 保持代码风格一致
5. ✓ 添加预防性检查（如有必要）
6. ✓ 验证修复后功能正常
"""
        elif op_type == "REFACTOR":
            prompt += """1. ✓ 保持功能完全不变
2. ✓ 显著提升代码可读性和可维护性
3. ✓ 遵循SOLID设计原则
4. ✓ 更新所有相关注释和文档
5. ✓ 确保向后兼容性
6. ✓ 重构后代码更简洁清晰
"""
        elif op_type == "OPTIMIZE":
            prompt += """1. ✓ 实现明确的性能优化目标
2. ✓ 保持功能完全正确
3. ✓ 添加性能改进说明和基准对比
4. ✓ 避免过度优化和复杂化
5. ✓ 保持代码可维护性
6. ✓ 测试验证性能提升
"""
        else:  # MODIFY
            prompt += """1. ✓ 正确实现所有修改需求
2. ✓ 保持代码整体一致性
3. ✓ 更新所有相关注释和文档
4. ✓ 不破坏任何现有功能
5. ✓ 处理所有边界情况
6. ✓ 代码可直接运行测试
"""

        # 技能自动触发提示
        if triggered_skills:
            prompt += "\n---\n\n## 🎯 自动触发的技能\n\n"
            prompt += "根据Superpowers配置，以下技能将自动触发:\n\n"
            for skill, should_trigger in triggered_skills.items():
                if should_trigger:
                    prompt += f"- ✓ **{skill}**: 任务完成后自动执行\n"

        # 执行协议
        prompt += """
---

## 🚀 执行协议

### 代码规范
1. **所有代码必须包裹在正确的 Markdown 代码块中**（使用 ```python）
2. **🚫 严禁省略代码**（不允许使用 `// ...rest`、`# ... 其余代码`或任何省略符号）
3. **必须提供完整的文件内容**（如需修改文件，提供从头到尾的完整代码）
4. **保持原有的缩进和代码风格**（与现有代码保持一致）
5. **添加必要的中文注释**（解释关键逻辑和复杂算法）

### 操作步骤
1. 📖 **仔细阅读** - 理解当前文件内容和项目上下文
2. 💡 **吸收经验** - 学习相关历史经验和决策
3. 📐 **规划方案** - 设计实现方案和代码结构
4. ⚙️ **实现代码** - 编写完整的、可运行的代码
5. ✅ **自我检查** - 对照成功标准和质量纪律

### 输出要求
1. **📝 实现思路** - 简要说明你的设计思路和关键决策
2. **💻 完整代码** - 提供所有文件的完整代码（不省略）
3. **💬 关键解释** - 解释重要的技术决策和权衡
4. **🧪 测试说明** - 说明如何测试和验证功能

---

## 📌 开始执行

请严格按照以上要求完成任务。记住：

- ⚠️ **禁止省略代码** - 这是最重要的规则
- ✅ **完整实现** - 不留TODO，不留占位符
- 🎯 **质量第一** - 代码质量比速度更重要
- 📚 **学习经验** - 充分利用历史经验避免重复错误

祝你顺利完成任务！🚀
"""

        return prompt

    def deal(self):
        """执行Dealer主流程"""
        print(Fore.CYAN + "\n╔" + "="*68 + "╗")
        print(Fore.CYAN + "║" + " "*20 + "Dealer v3.0" + " "*37 + "║")
        print(Fore.CYAN + "║" + " "*15 + "增强版指令生成器" + " "*36 + "║")
        print(Fore.CYAN + "╚" + "="*68 + "╝\n")

        # 1. 检查蓝图文件
        if not os.path.exists(STATE_FILE):
            print(Fore.RED + "❌ 蓝图文件不存在: " + STATE_FILE)
            print(Fore.YELLOW + "💡 请先运行 Brain 生成任务蓝图")
            return

        # 2. 读取蓝图
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            raw = f.read()

        # 3. 解析蓝图
        if "<thinking>" in raw or "```json" in raw:
            # Brain的输出需要解析
            data = self.parse_brain(raw)
            if data:
                self.cache.set("last_blueprint", raw)
                with open(STATE_FILE, "w", encoding="utf-8") as fw:
                    json.dump(data, fw, indent=2, ensure_ascii=False)
        else:
            try:
                data = json.loads(raw)
            except:
                data = None

        if not data:
            print(Fore.RED + "❌ 无法解析蓝图数据")
            return

        # 4. 获取待执行任务
        tasks = data.get("blueprint", [])
        target = next((t for t in tasks if t.get("status") == "PENDING"), None)

        if not target:
            print(Fore.GREEN + "🎉 所有任务已完成！")
            return

        # 5. 生成指令
        prompt = self.generate_instruction(target)

        # 6. 输出
        ralph_mode = '--ralph-mode' in sys.argv

        if ralph_mode:
            # Ralph模式：写入文件
            os.makedirs('.ralph', exist_ok=True)
            with open('.ralph/current_instruction.txt', 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(Fore.GREEN + "\n✅ 指令已生成到 .ralph/current_instruction.txt")
        else:
            # 正常模式：复制到剪贴板
            pyperclip.copy(prompt)
            print(Fore.GREEN + "\n✅ 增强指令已复制到剪贴板")

        # 7. 摘要
        print(Fore.CYAN + "\n" + "-"*70)
        print(Fore.YELLOW + f"🚀 提取任务: {target['task_name']}")

        files = target.get('target_files', [])
        print(Fore.CYAN + f"📁 目标文件: {len(files)} 个")

        for f in files:
            exists = os.path.exists(f)
            status = "✓ 存在" if exists else "✗ 需创建"
            color = Fore.GREEN if exists else Fore.YELLOW
            print(color + f"   - {f} {status}")

        print(Fore.CYAN + "-"*70)

        if not ralph_mode:
            print(Fore.GREEN + "\n💡 v3.0 增强功能:")
            print(Fore.WHITE + "  ✓ 双记忆系统 (Hippocampus + claude-mem)")
            print(Fore.WHITE + "  ✓ Context Engineering (项目上下文)")
            print(Fore.WHITE + "  ✓ Superpowers质量纪律")
            print(Fore.WHITE + "  ✓ Compound Engineering质量门控")
            print(Fore.WHITE + "  ✓ 技能自动触发提示")

        # 返回指令（供ralph_interactive.sh使用）
        return prompt

    def parse_brain(self, content: str) -> Optional[Dict]:
        """
        解析Brain的输出

        Args:
            content: Brain输出内容

        Returns:
            解析后的JSON数据
        """
        self.thinkbank.store(content)

        # 尝试提取JSON代码块
        match = re.search(r'```json(.*?)```', content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                pass

        # 尝试直接解析
        try:
            return json.loads(content)
        except:
            return None


def main():
    """主函数"""
    dealer = DealerV3()
    dealer.deal()


if __name__ == "__main__":
    main()
