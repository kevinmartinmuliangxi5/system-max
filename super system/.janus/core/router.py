class TaskRouter:
    STRATEGIES = {
        "frontend": {
            "role": "前端架构师 (Vue/React)",
            "exts": [".html", ".css", ".js", ".vue", ".jsx", ".tsx"],
            "keywords": ["界面", "页面", "前端", "ui", "ux", "布局", "样式", "组件"]
        },
        "backend": {
            "role": "后端架构师 (Python/Go)",
            "exts": [".py", ".go", ".java", ".sql", ".c", ".cpp"],
            "keywords": ["数据库", "api", "接口", "服务", "后端", "查询", "server", "database"]
        },
        "test": {
            "role": "测试工程师",
            "exts": [".test.py", "_test.py", ".spec.js", ".test.js"],
            "keywords": ["测试", "test", "单元", "集成", "验证", "unittest", "pytest", "检查"]
        },
        "debug": {
            "role": "调试专家",
            "exts": [],
            "keywords": ["修复", "bug", "错误", "崩溃", "异常", "fix", "repair", "debug", "solve", "问题"]
        },
        "devops": {
            "role": "SRE运维专家",
            "exts": [".sh", ".yaml", ".yml", ".dockerfile", ".tf"],
            "keywords": ["部署", "运维", "容器", "监控", "ci/cd", "docker", "kubernetes", "k8s"]
        },
        "data": {
            "role": "数据科学家",
            "exts": [".ipynb", ".csv", ".json"],
            "keywords": ["数据", "分析", "模型", "训练", "预测", "machine learning", "ml", "ai"]
        }
    }

    def route(self, name, instr, files):
        """
        智能路由任务到合适的角色

        优先级:
        1. 关键词匹配（任务名称和指令）
        2. 文件扩展名匹配
        3. 默认通用角色
        """
        text = (name + " " + instr).lower()

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
