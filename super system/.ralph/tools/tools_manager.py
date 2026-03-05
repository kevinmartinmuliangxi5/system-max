"""
工具管理器 - 统一管理所有集成的工具
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any


class ToolsManager:
    """管理双脑系统集成的所有工具"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.json")

        self.config_path = config_path
        self.config = self._load_config()
        self.enabled_tools = self._get_enabled_tools()

    def _load_config(self) -> Dict:
        """加载工具配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告: 配置文件未找到: {self.config_path}")
            return {"tools": {}}

    def _get_enabled_tools(self) -> List[str]:
        """获取所有启用的工具"""
        enabled = []
        for tool_name, tool_config in self.config.get("tools", {}).items():
            if tool_config.get("enabled", False):
                enabled.append(tool_name)
        return enabled

    def is_tool_enabled(self, tool_name: str) -> bool:
        """检查工具是否启用"""
        return tool_name in self.enabled_tools

    def get_tool_config(self, tool_name: str) -> Optional[Dict]:
        """获取工具配置"""
        return self.config.get("tools", {}).get(tool_name)

    def should_trigger_skill(self, skill_name: str, context: Dict) -> bool:
        """
        判断是否应该触发某个技能

        Args:
            skill_name: 技能名称（如 'code_review', 'testing'）
            context: 上下文信息
                - action: 当前动作（如 'code_change', 'new_feature'）
                - keywords: 关键词列表
                - files: 涉及的文件列表

        Returns:
            是否应该触发
        """
        if not self.is_tool_enabled("superpowers"):
            return False

        sp_config = self.get_tool_config("superpowers")
        skills = sp_config.get("skills", {})

        if skill_name not in skills:
            return False

        skill_config = skills[skill_name]
        if not skill_config.get("enabled", False):
            return False

        # 检查触发条件
        trigger_on = skill_config.get("trigger_on", [])
        action = context.get("action", "")

        return action in trigger_on

    def should_trigger_frontend_design(self, context: Dict) -> bool:
        """判断是否应该触发前端设计技能"""
        if not self.is_tool_enabled("frontend_design"):
            return False

        fd_config = self.get_tool_config("frontend_design")

        # 检查关键词
        keywords = fd_config.get("keywords", [])
        task_desc = context.get("description", "").lower()

        for keyword in keywords:
            if keyword in task_desc:
                return True

        # 检查文件模式
        file_patterns = fd_config.get("file_patterns", [])
        files = context.get("files", [])

        for file in files:
            for pattern in file_patterns:
                if file.endswith(pattern.replace("*", "")):
                    return True

        return False

    def get_compound_engineering_agent(self, task_type: str) -> Optional[str]:
        """
        根据任务类型获取对应的CE代理

        Args:
            task_type: 任务类型（如 'requirement', 'design', 'code', 'test'）

        Returns:
            代理名称（如 'req_dev', 'brainstorm'）
        """
        if not self.is_tool_enabled("compound_engineering"):
            return None

        ce_config = self.get_tool_config("compound_engineering")
        agents = ce_config.get("agents", {})

        # 任务类型到代理的映射
        type_to_agent = {
            "requirement": "req_dev",
            "requirements": "req_dev",
            "design": "brainstorm",
            "architecture": "brainstorm",
            "code": "code_gen",
            "implementation": "code_gen",
            "test": "test_gen",
            "testing": "test_gen",
            "review": "code_review",
            "documentation": "doc_gen",
            "docs": "doc_gen"
        }

        agent_name = type_to_agent.get(task_type.lower())

        if agent_name and agent_name in agents:
            if agents[agent_name].get("enabled", False):
                return agent_name

        return None

    def get_memory_search_config(self) -> Dict:
        """获取记忆搜索配置"""
        if not self.is_tool_enabled("claude_mem"):
            return {
                "semantic_weight": 0.7,
                "keyword_weight": 0.3,
                "top_k": 5
            }

        cm_config = self.get_tool_config("claude_mem")
        return cm_config.get("search", {
            "semantic_weight": 0.7,
            "keyword_weight": 0.3,
            "top_k": 5
        })

    def should_generate_diagram(self, diagram_type: str) -> bool:
        """判断是否应该生成图表"""
        if not self.is_tool_enabled("drawio_mcp"):
            return False

        dio_config = self.get_tool_config("drawio_mcp")
        auto_gen = dio_config.get("auto_generate", {})

        type_mapping = {
            "task": "task_flow",
            "flow": "task_flow",
            "architecture": "architecture",
            "arch": "architecture",
            "decision": "decision_tree",
            "debug": "decision_tree"
        }

        key = type_mapping.get(diagram_type.lower(), diagram_type)
        return auto_gen.get(key, False)

    def get_diagram_output_dir(self) -> str:
        """获取图表输出目录"""
        if not self.is_tool_enabled("drawio_mcp"):
            return ".ralph/diagrams"

        dio_config = self.get_tool_config("drawio_mcp")
        return dio_config.get("output_dir", ".ralph/diagrams")

    def get_bright_line_rules(self) -> Dict:
        """获取Superpowers的Bright-Line规则"""
        if not self.is_tool_enabled("superpowers"):
            return {}

        sp_config = self.get_tool_config("superpowers")
        return sp_config.get("bright_line_rules", {})

    def validate_quality_gate(self, phase: str, checks: List[str]) -> bool:
        """
        验证质量门禁

        Args:
            phase: 阶段（'planning', 'execution', 'review'）
            checks: 已完成的检查项

        Returns:
            是否通过质量门禁
        """
        if not self.is_tool_enabled("compound_engineering"):
            return True

        ce_config = self.get_tool_config("compound_engineering")
        quality_gates = ce_config.get("quality_gates", {})

        required_checks = quality_gates.get(phase, [])

        for required in required_checks:
            if required not in checks:
                return False

        return True

    def get_tools_for_layer(self, layer: str) -> List[str]:
        """
        获取某个层级应该使用的工具

        Args:
            layer: 层级名称（'brain', 'memory', 'dealer', 'worker'）

        Returns:
            工具名称列表
        """
        integration = self.config.get("integration_layers", {})
        layer_config = integration.get(layer, {})
        return layer_config.get("tools", [])

    def get_spec_validation_config(self) -> Dict:
        """获取规格验证配置"""
        if not self.is_tool_enabled("speckit"):
            return {"auto_validate": False, "strict_mode": False}

        sk_config = self.get_tool_config("speckit")
        return sk_config.get("validation", {
            "auto_validate": True,
            "strict_mode": True
        })


# 全局实例
tools_manager = ToolsManager()


def get_tools_manager() -> ToolsManager:
    """获取工具管理器实例"""
    return tools_manager


if __name__ == "__main__":
    # 测试
    tm = ToolsManager()

    print("启用的工具:")
    for tool in tm.enabled_tools:
        print(f"  ✓ {tool}")

    print("\nBrain层工具:")
    for tool in tm.get_tools_for_layer("brain"):
        print(f"  - {tool}")

    print("\n测试技能触发:")
    context = {
        "action": "code_change",
        "description": "修改登录页面UI",
        "files": ["login.jsx"]
    }

    if tm.should_trigger_skill("code_review", context):
        print("  ✓ 应该触发 code_review")

    if tm.should_trigger_frontend_design(context):
        print("  ✓ 应该触发 frontend_design")
