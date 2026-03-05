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

def detect_mode(instruction):
    """自动判断任务复杂度"""
    if "#deep" in instruction: return "deep"
    if "#simple" in instruction: return "simple"
    # 关键词触发深度模式
    complex_words = ["设计", "架构", "重构", "分析", "新建", "初始化"]
    if any(w in instruction for w in complex_words): return "deep"
    return "simple"

def parse_brain(content):
    ThinkBank().store(content) # 自动存思考
    # 提取 JSON
    match = re.search(r'```json(.*?)```', content, re.DOTALL)
    if match: return json.loads(match.group(1))
    try: return json.loads(content)
    except: return None

def deal():
    if not os.path.exists(STATE_FILE): print(Fore.RED+"❌ 蓝图缺失"); return

    # 1. 尝试读取并解析
    with open(STATE_FILE, "r", encoding="utf-8") as f: raw = f.read()

    # 如果是 Brain 的原始输出，进行解析和缓存
    if "<thinking>" in raw or "```json" in raw:
        data = parse_brain(raw)
        if data:
            CacheManager().set("last_blueprint", raw) # 缓存原始输出
            with open(STATE_FILE, "w", encoding="utf-8") as fw:
                json.dump(data, fw, indent=2, ensure_ascii=False)
    else:
        try: data = json.loads(raw)
        except: data = None

    if not data: print(Fore.RED+"❌ 数据不可用"); return

    tasks = data.get("blueprint", [])
    target = next((t for t in tasks if t.get("status") == "PENDING"), None)
    if not target: print(Fore.GREEN+"🎉 任务清空"); return

    # 2. 路由与上下文 (只给 Worker 最需要的)
    router = TaskRouter()
    cat, role_prompt = router.route(target['task_name'], target['instruction'], target.get('target_files', []))

    # 海马体 (历史经验)
    hippo = Hippocampus()
    insights = hippo.retrieve(target['task_name'])
    insight_txt = "\n".join([f"- {i['s'][:100]}" for i in insights])

    # 思考库 (最近决策)
    decisions = ThinkBank().get_latest_context()

    prompt = f"""
{role_prompt}

【任务】{target['task_name']}
【指令】{target['instruction']}
【文件】{", ".join(target.get('target_files', []))}

【项目背景】
{decisions if decisions else "无。"}

【避坑指南】
{insight_txt if insight_txt else "无。"}

【执行协议】
1. 代码必须包裹在 Markdown 块中。
2. 严禁省略代码 (如 // ...rest)。
"""
    pyperclip.copy(prompt)
    print(Fore.CYAN + "-"*40)
    print(Fore.YELLOW + f"🚀 提取任务: {target['task_name']}")
    print(Fore.MAGENTA + f"🎭 模式: {cat.upper()}")
    print(Fore.GREEN + "\n✅ 极简指令已复制")
    print(Fore.CYAN + "-"*40)

if __name__ == "__main__": deal()