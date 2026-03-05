"""
快速启动脚本

用法:
    python run.py                           # 启动UI模式
    python run.py --task "你的任务"          # CLI模式
    python run.py --task "你的任务" -o out.py  # CLI模式并保存输出
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flow_system.main import main

if __name__ == "__main__":
    main()
