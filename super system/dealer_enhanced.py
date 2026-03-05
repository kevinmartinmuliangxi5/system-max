import json, os, sys, pyperclip, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.janus'))
from core.router import TaskRouter
from core.hippocampus import Hippocampus
from core.thinkbank import ThinkBank
from core.cache_manager import CacheManager

if sys.platform == "win32":
    import io; sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
try: from colorama import init, Fore; init(autoreset=True)
except: pass

STATE_FILE = ".janus/project_state.json"

def detect_operation_type(instruction, files):
    """检测操作类型"""
    instr_lower = instruction.lower()

    # 检查文件是否存在
    files_exist = all(os.path.exists(f) for f in files if f)

    if any(kw in instr_lower for kw in ['新建', '创建', 'create', 'new', 'add']):
        if not files_exist:
            return "CREATE"

    if any(kw in instr_lower for kw in ['重构', 'refactor', '重写', 'rewrite']):
        return "REFACTOR"

    if any(kw in instr_lower for kw in ['修复', 'fix', 'bug', '调试', 'debug']):
        return "FIX"

    if any(kw in instr_lower for kw in ['优化', 'optimize', '改进', 'improve']):
        return "OPTIMIZE"

    if files_exist:
        return "MODIFY"
    else:
        return "CREATE"

def get_file_content(filepath):
    """读取文件内容"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 统计行数
            lines = content.split('\n')
            return {
                'exists': True,
                'lines': len(lines),
                'size': len(content),
                'preview': '\n'.join(lines[:20]) if len(lines) > 20 else content
            }
        except:
            return {'exists': True, 'lines': 0, 'size': 0, 'error': 'read_failed'}
    return {'exists': False}

def get_project_structure():
    """获取项目结构"""
    structure = []

    # 只列出重要目录和文件
    important_items = [
        '.janus/',
        'dealer.py',
        'quick_check.py',
        'setup.py',
        'README.md'
    ]

    for item in important_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                structure.append(f"📁 {item}")
            else:
                structure.append(f"📄 {item}")

    return "\n".join(structure) if structure else "未检测到标准项目结构"

def parse_brain(content):
    ThinkBank().store(content)
    match = re.search(r'```json(.*?)```', content, re.DOTALL)
    if match: return json.loads(match.group(1))
    try: return json.loads(content)
    except: return None

def deal():
    if not os.path.exists(STATE_FILE): print(Fore.RED+"❌ 蓝图缺失"); return

    # 1. 读取并解析
    with open(STATE_FILE, "r", encoding="utf-8") as f: raw = f.read()

    if "<thinking>" in raw or "```json" in raw:
        data = parse_brain(raw)
        if data:
            CacheManager().set("last_blueprint", raw)
            with open(STATE_FILE, "w", encoding="utf-8") as fw:
                json.dump(data, fw, indent=2, ensure_ascii=False)
    else:
        try: data = json.loads(raw)
        except: data = None

    if not data: print(Fore.RED+"❌ 数据不可用"); return

    tasks = data.get("blueprint", [])
    target = next((t for t in tasks if t.get("status") == "PENDING"), None)
    if not target: print(Fore.GREEN+"🎉 任务清空"); return

    # 2. 路由与上下文
    router = TaskRouter()
    cat, role_prompt = router.route(target['task_name'], target['instruction'], target.get('target_files', []))

    # 3. 海马体检索
    hippo = Hippocampus()
    insights = hippo.retrieve(target['task_name'])

    # 4. 思考库
    decisions = ThinkBank().get_latest_context()

    # 5. 检测操作类型
    files = target.get('target_files', [])
    op_type = detect_operation_type(target['instruction'], files)

    # 6. 读取文件内容
    files_info = {}
    for f in files:
        files_info[f] = get_file_content(f)

    # 7. 获取项目结构
    project_structure = get_project_structure()

    # 8. 生成增强版 prompt
    prompt = f"""# 任务概览

**角色**: {role_prompt}
**任务**: {target['task_name']}
**操作类型**: {op_type}

---

## 📋 任务详情

### 目标
{target['instruction']}

### 目标文件
"""

    for f, info in files_info.items():
        if info.get('exists'):
            prompt += f"\n- `{f}` (已存在, {info.get('lines', 0)} 行)\n"
        else:
            prompt += f"\n- `{f}` (需要创建)\n"

    # 文件内容
    prompt += "\n---\n\n## 📁 当前文件内容\n"

    for f, info in files_info.items():
        if info.get('exists') and not info.get('error'):
            prompt += f"\n### {f}\n\n```python\n{info.get('preview', '')}\n```\n"
            if info.get('lines', 0) > 20:
                prompt += f"\n*（仅显示前 20 行，共 {info['lines']} 行）*\n"
        elif info.get('exists') and info.get('error'):
            prompt += f"\n### {f}\n\n⚠️ 文件存在但读取失败\n"
        else:
            prompt += f"\n### {f}\n\n📝 文件不存在，需要创建\n"

    # 项目结构
    prompt += f"""
---

## 🗂️ 项目结构

```
{project_structure}
```

---

## 💡 相关经验（来自海马体）

"""

    if insights:
        for i, insight in enumerate(insights, 1):
            prompt += f"{i}. **{insight['p']}**\n   {insight['s']}\n\n"
    else:
        prompt += "无相关历史经验。\n"

    # 项目背景
    prompt += f"""
---

## 🧠 项目决策（来自思考库）

{decisions if decisions else "无历史决策记录。"}

---

## ✅ 成功标准

请确保完成以下要求：

"""

    # 根据操作类型生成不同的成功标准
    if op_type == "CREATE":
        prompt += """1. 创建所有目标文件，使用正确的文件路径
2. 实现所有必需的功能和方法
3. 添加适当的文档字符串和注释
4. 代码符合 Python/项目规范
5. 处理可能的错误情况
"""
    elif op_type == "FIX":
        prompt += """1. 准确定位并修复 bug
2. 添加注释说明修复内容
3. 确保不引入新的问题
4. 保持代码风格一致
5. 如有可能，添加预防性检查
"""
    elif op_type == "REFACTOR":
        prompt += """1. 保持功能不变
2. 提升代码可读性和可维护性
3. 遵循设计原则（SOLID 等）
4. 更新相关注释和文档
5. 确保向后兼容
"""
    elif op_type == "OPTIMIZE":
        prompt += """1. 实现性能优化目标
2. 保持功能正确性
3. 添加性能改进说明
4. 避免过度优化
5. 考虑可维护性
"""
    else:  # MODIFY
        prompt += """1. 正确实现修改需求
2. 保持代码一致性
3. 更新相关注释
4. 不破坏现有功能
5. 处理边界情况
"""

    prompt += """
---

## 🚀 执行协议

### 代码规范
1. 所有代码必须包裹在正确的 Markdown 代码块中（使用 ```python）
2. **严禁省略代码**（禁止使用 `// ...rest` 或 `# ... 其余代码`）
3. 如需修改文件，提供完整的文件内容
4. 保持原有的缩进和代码风格

### 操作步骤
1. 仔细阅读当前文件内容（如有）
2. 理解任务需求和相关经验
3. 规划修改方案
4. 实现所有修改
5. 自我检查代码质量

### 输出要求
1. 说明你的实现思路
2. 提供完整的代码
3. 解释关键决策
4. 说明如何测试验证

---

## 📌 开始执行

请按照以上要求完成任务。
"""

    # 检查是否为Ralph模式
    ralph_mode = '--ralph-mode' in sys.argv

    if ralph_mode:
        # Ralph模式：写入文件
        os.makedirs('.ralph', exist_ok=True)
        with open('.ralph/current_instruction.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(Fore.GREEN + "✅ 指令已生成到 .ralph/current_instruction.txt")
    else:
        # 正常模式：复制到剪贴板
        pyperclip.copy(prompt)
        print(Fore.GREEN + "\n✅ 增强指令已复制到剪贴板")

    print(Fore.CYAN + "-"*60)
    print(Fore.YELLOW + f"🚀 提取任务: {target['task_name']}")
    print(Fore.MAGENTA + f"🎭 角色: {role_prompt}")
    print(Fore.BLUE + f"📦 操作类型: {op_type}")
    print(Fore.CYAN + f"📁 目标文件: {len(files)} 个")

    for f, info in files_info.items():
        status = "✓ 存在" if info.get('exists') else "✗ 需创建"
        print(Fore.WHITE + f"   - {f} {status}")

    print(Fore.CYAN + "-"*60)

    if not ralph_mode:
        print(f"\n💡 提示: 相比原版增加了:")
        print("  ✓ 文件当前内容")
        print("  ✓ 项目结构信息")
        print("  ✓ 操作类型检测")
        print("  ✓ 明确的成功标准")
        print("  ✓ 详细的执行协议")

    # 返回生成的指令（供ralph_interactive.sh使用）
    return prompt

if __name__ == "__main__": deal()
