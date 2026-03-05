import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.janus'))
from core.validator import Validator
from core.hippocampus import Hippocampus
import json

def quick_check():
    if Validator().validate():
        try: # 验证通过，自动记忆
            with open(".janus/project_state.json", 'r') as f:
                t = next((x for x in json.load(f)['blueprint'] if x.get("status")=="PENDING"), None)
            if t: Hippocampus().store(t['task_name'], t['instruction'][:150])
        except: pass
        print("✅ 验证通过")
    else: sys.exit(1)
if __name__ == "__main__": quick_check()