"""
TaskRouter v2.0 - 增强版任务路由器
新增功能：
- 技术栈自动识别
- 知识库加载
- 智慧建议触发检测
"""

import os
import json
from pathlib import Path


class TaskRouterV2:
    """增强版任务路由器"""

    STRATEGIES = {
        "frontend": {
            "role": "前端架构师 (Vue/React)",
            "exts": [".html", ".css", ".js", ".vue", ".jsx", ".tsx"],
            "keywords": ["界面", "页面", "前端", "ui", "ux", "布局", "样式", "组件"],
            "tech_stacks": ["react", "vue", "angular", "svelte"]
        },
        "backend": {
            "role": "后端架构师 (Python/Go)",
            "exts": [".py", ".go", ".java", ".sql", ".c", ".cpp"],
            "keywords": ["数据库", "api", "接口", "服务", "后端", "查询", "server", "database"],
            "tech_stacks": ["fastapi", "flask", "django", "express", "spring"]
        },
        "streamlit": {
            "role": "Streamlit应用专家",
            "exts": [".py"],
            "keywords": ["streamlit", "st.", "页面", "仪表盘", "dashboard"],
            "tech_stacks": ["streamlit"]
        },
        "test": {
            "role": "测试工程师",
            "exts": [".test.py", "_test.py", ".spec.js", ".test.js"],
            "keywords": ["测试", "test", "单元", "集成", "验证", "unittest", "pytest", "检查"],
            "tech_stacks": ["pytest", "jest", "mocha"]
        },
        "debug": {
            "role": "调试专家",
            "exts": [],
            "keywords": ["修复", "bug", "错误", "崩溃", "异常", "fix", "repair", "debug", "solve", "问题"],
            "tech_stacks": []
        },
        "devops": {
            "role": "SRE运维专家",
            "exts": [".sh", ".yaml", ".yml", ".dockerfile", ".tf"],
            "keywords": ["部署", "运维", "容器", "监控", "ci/cd", "docker", "kubernetes", "k8s"],
            "tech_stacks": ["docker", "kubernetes", "terraform"]
        },
        "data": {
            "role": "数据科学家",
            "exts": [".ipynb", ".csv", ".json"],
            "keywords": ["数据", "分析", "模型", "训练", "预测", "machine learning", "ml", "ai"],
            "tech_stacks": ["pandas", "numpy", "tensorflow", "pytorch"]
        },
        "security": {
            "role": "安全工程师",
            "exts": [],
            "keywords": ["安全", "认证", "授权", "加密", "token", "jwt", "oauth", "密码", "登录"],
            "tech_stacks": ["jwt", "oauth", "bcrypt"]
        }
    }

    # 智慧建议触发词
    WISDOM_TRIGGERS = {
        "security": ["登录", "密码", "认证", "权限", "token", "session", "加密"],
        "performance": ["慢", "优化", "性能", "缓存", "加载", "速度"],
        "architecture": ["重构", "架构", "模块", "解耦", "分层", "设计"],
        "data": ["数据库", "存储", "查询", "SQL", "ORM", "数据"],
        "ui": ["界面", "页面", "样式", "布局", "组件", "交互"]
    }

    def __init__(self):
        self.knowledge_base = {}
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """加载知识库"""
        knowledge_dir = Path(__file__).parent.parent / "knowledge"
        if knowledge_dir.exists():
            for file in knowledge_dir.glob("*.json"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        tech_stack = data.get('tech_stack', file.stem)
                        self.knowledge_base[tech_stack.lower()] = data
                except Exception as e:
                    print(f"加载知识库失败 {file}: {e}")

    def route(self, name: str, instr: str, files: list = None) -> tuple:
        """
        智能路由任务到合适的角色

        返回: (category, role, tech_stack, knowledge)
        """
        files = files or []
        text = (name + " " + instr).lower()

        # 1. 检测技术栈
        tech_stack = self._detect_tech_stack(text, files)

        # 2. 匹配策略
        category, role = self._match_strategy(text, files)

        # 3. 加载相关知识
        knowledge = self._get_knowledge(tech_stack, category)

        return category, role, tech_stack, knowledge

    def _detect_tech_stack(self, text: str, files: list) -> str:
        """检测技术栈"""
        # Streamlit检测
        if "streamlit" in text or "st." in text:
            return "streamlit"

        # React检测
        if any(f.endswith(('.jsx', '.tsx')) for f in files) or "react" in text:
            return "react"

        # Vue检测
        if any(f.endswith('.vue') for f in files) or "vue" in text:
            return "vue"

        # FastAPI检测
        if "fastapi" in text or "@app.get" in text or "@app.post" in text:
            return "fastapi"

        # Flask检测
        if "flask" in text or "@app.route" in text:
            return "flask"

        # Django检测
        if "django" in text or "models.Model" in text:
            return "django"

        # Python Web通用
        if any(f.endswith('.py') for f in files):
            return "python"

        return "general"

    def _match_strategy(self, text: str, files: list) -> tuple:
        """匹配策略"""
        # 1. 优先匹配关键词
        for k, v in self.STRATEGIES.items():
            if any(kw in text for kw in v.get('keywords', [])):
                return k, v['role']

        # 2. 其次匹配文件扩展名
        for k, v in self.STRATEGIES.items():
            if files and any(e in f for f in files for e in v['exts']):
                return k, v['role']

        # 3. 默认通用
        return "general", "全栈工程师"

    def _get_knowledge(self, tech_stack: str, category: str) -> dict:
        """获取相关知识"""
        knowledge = {}

        # 获取技术栈知识
        if tech_stack in self.knowledge_base:
            knowledge['tech_stack'] = self.knowledge_base[tech_stack]

        # 获取安全知识（如果涉及安全）
        if category == "security" and "security" in self.knowledge_base:
            knowledge['security'] = self.knowledge_base['security']

        return knowledge

    def detect_wisdom_triggers(self, text: str) -> list:
        """检测需要提供智慧建议的领域"""
        text_lower = text.lower()
        triggered = []

        for category, keywords in self.WISDOM_TRIGGERS.items():
            if any(kw in text_lower for kw in keywords):
                triggered.append(category)

        return triggered

    def get_wisdom_suggestions(self, categories: list) -> dict:
        """获取智慧建议"""
        suggestions = {}

        wisdom_library = {
            "security": [
                {"title": "密码加密", "desc": "使用bcrypt加密密码，而非明文存储"},
                {"title": "登录限流", "desc": "添加登录限流，防止暴力破解"},
                {"title": "Token刷新", "desc": "实现Token刷新机制，提升安全性"},
                {"title": "二次验证", "desc": "对敏感操作添加二次验证"}
            ],
            "performance": [
                {"title": "数据缓存", "desc": "添加Redis缓存热点数据"},
                {"title": "分页加载", "desc": "实现分页加载，避免一次加载过多"},
                {"title": "懒加载", "desc": "使用懒加载优化首屏速度"},
                {"title": "索引优化", "desc": "添加数据库索引优化查询"}
            ],
            "architecture": [
                {"title": "分层架构", "desc": "采用分层架构，提升可维护性"},
                {"title": "依赖注入", "desc": "使用依赖注入，降低耦合度"},
                {"title": "公共抽取", "desc": "抽取公共逻辑到工具类"},
                {"title": "接口规范", "desc": "定义清晰的接口规范"}
            ],
            "data": [
                {"title": "使用ORM", "desc": "使用ORM而非原生SQL"},
                {"title": "事务处理", "desc": "添加事务处理保证数据一致性"},
                {"title": "批量操作", "desc": "对大量数据操作使用批量处理"},
                {"title": "数据验证", "desc": "添加数据验证防止脏数据"}
            ],
            "ui": [
                {"title": "组件化", "desc": "使用组件化开发提升复用性"},
                {"title": "加载状态", "desc": "添加加载状态提升用户体验"},
                {"title": "响应式", "desc": "实现响应式布局适配多端"},
                {"title": "错误边界", "desc": "添加错误边界处理异常"}
            ]
        }

        for category in categories:
            if category in wisdom_library:
                suggestions[category] = wisdom_library[category]

        return suggestions


# 保持向后兼容
class TaskRouter(TaskRouterV2):
    """向后兼容的别名"""

    def route(self, name, instr, files=None):
        """向后兼容的route方法，只返回category和role"""
        category, role, _, _ = super().route(name, instr, files)
        return category, role


# 测试代码
if __name__ == "__main__":
    router = TaskRouterV2()

    # 测试路由
    test_cases = [
        ("实现用户登录功能", "使用JWT认证，bcrypt加密密码", ["auth.py"]),
        ("优化首页加载速度", "减少API请求，添加缓存", ["app.py"]),
        ("添加Streamlit仪表盘", "展示数据分析结果", ["dashboard.py"]),
        ("修复数据库查询Bug", "解决SQL注入问题", ["database.py"]),
    ]

    for name, instr, files in test_cases:
        category, role, tech_stack, knowledge = router.route(name, instr, files)
        wisdom_triggers = router.detect_wisdom_triggers(name + " " + instr)

        print(f"\n任务: {name}")
        print(f"  类别: {category}")
        print(f"  角色: {role}")
        print(f"  技术栈: {tech_stack}")
        print(f"  智慧触发: {wisdom_triggers}")
        if knowledge:
            print(f"  知识库: {list(knowledge.keys())}")
