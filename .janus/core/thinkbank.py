import json, os, re, hashlib
from datetime import datetime

class ThinkBank:
    def __init__(self):
        self.bank_dir = ".janus/thinking"
        os.makedirs(self.bank_dir, exist_ok=True)
        self.index_file = os.path.join(self.bank_dir, "index.json")
        self.index = json.load(open(self.index_file, 'r', encoding='utf-8')) if os.path.exists(self.index_file) else []

    def store(self, content):
        # 提取思考内容
        match = re.search(r'<thinking>(.*?)</thinking>', content, re.DOTALL)
        if not match: return
        thought = match.group(1).strip()

        # 智能压缩：只提取决策句
        decisions = re.findall(r'(?:选择|采用|使用|避免|架构|方案|定为).*?[，。]', thought)
        summary = " ".join(decisions)[:300] # 限制长度，省Token

        tid = hashlib.md5(thought.encode()).hexdigest()[:8]

        # 存全量 (备查)
        with open(os.path.join(self.bank_dir, f"{tid}.txt"), 'w', encoding='utf-8') as f: f.write(thought)

        # 存摘要 (使用)
        self.index.append({"id": tid, "time": datetime.now().isoformat(), "summary": summary if summary else thought[:50]+"..."})
        with open(self.index_file, 'w', encoding='utf-8') as f: json.dump(self.index[-50:], f, indent=2)

    def get_latest_context(self):
        # 只返回最近 3 条决策摘要，极简 Context
        return "\n".join([f"• {i['summary']}" for i in self.index[-3:]])