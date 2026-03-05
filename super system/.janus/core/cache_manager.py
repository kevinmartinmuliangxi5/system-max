import json, os, hashlib
from datetime import datetime

class CacheManager:
    def __init__(self):
        self.cache_dir = ".janus/cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, key):
        p = os.path.join(self.cache_dir, f"{self.get_hash(key)}.json")
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f: return json.load(f)["content"]
            except: pass
        return None

    def set(self, key, content):
        p = os.path.join(self.cache_dir, f"{self.get_hash(key)}.json")
        with open(p, 'w', encoding='utf-8') as f:
            json.dump({"content": content, "ts": datetime.now().isoformat()}, f)