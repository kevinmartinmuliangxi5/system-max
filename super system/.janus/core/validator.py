import subprocess, os, sys, io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Validator:
    def validate(self):
        print("🛡️ 快速验证...")
        passed = True
        # 1. Python 语法
        py = [f for f in os.listdir('.') if f.endswith('.py')]
        if py and subprocess.run(f"python -m py_compile {' '.join(py)}", shell=True).returncode != 0: passed = False
        # 2. 单元测试
        tests = [f for f in py if f.startswith('test_')]
        if tests and subprocess.run(f"python -m unittest {' '.join([t[:-3] for t in tests])}", shell=True).returncode != 0: passed = False
        return passed