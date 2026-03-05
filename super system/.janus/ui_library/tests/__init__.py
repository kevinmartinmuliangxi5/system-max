"""
UI Library Tests - 测试模块
============================

单元测试和集成测试套件。

测试文件:
    - test_components.py: 组件测试
    - test_themes.py: 主题测试
    - test_recommender.py: 推荐引擎测试
    - test_composition.py: 组合系统测试
    - test_adapters.py: 适配器测试
    - test_docs.py: 文档生成器测试

运行测试:
    pytest tests/
    pytest tests/test_components.py -v
    pytest -k "test_theme" -v
"""

import sys
import os

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
