#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
draw.io MCP客户端

与draw.io MCP服务器交互，生成真实的流程图和架构图
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List


class DrawioMCPClient:
    """draw.io MCP客户端"""

    def __init__(self):
        """初始化客户端"""
        self.config_file = Path(".ralph/tools/config.json")
        self.enabled = self._check_enabled()
        self.diagrams_dir = Path(".ralph/diagrams")
        self.diagrams_dir.mkdir(exist_ok=True)

        if self.enabled:
            self.mcp_available = self._check_mcp_server()
        else:
            self.mcp_available = False

    def _check_enabled(self) -> bool:
        """检查是否启用draw.io MCP"""
        if not self.config_file.exists():
            return False

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get("tools", {}).get("drawio_mcp", {}).get("enabled", False)
        except:
            return False

    def _check_mcp_server(self) -> bool:
        """检查MCP服务器是否可用"""
        try:
            # 尝试调用MCP服务器
            # 这里简化实现，实际应该调用真实的MCP API
            result = subprocess.run(
                ["mcp", "list-servers"],
                capture_output=True,
                text=True,
                timeout=2
            )

            # 检查是否有draw.io服务器
            if "draw.io" in result.stdout or "drawio" in result.stdout:
                return True

        except:
            pass

        return False

    def create_flowchart(
        self,
        title: str,
        nodes: List[Dict],
        edges: List[Dict],
        output_format: str = "xml"
    ) -> Optional[str]:
        """
        创建流程图

        Args:
            title: 图表标题
            nodes: 节点列表，每个节点包含 id, label, type
            edges: 边列表，每个边包含 from, to, label
            output_format: 输出格式 (xml, png, svg)

        Returns:
            生成的文件路径
        """
        if not self.enabled:
            print("⚠️ draw.io MCP未启用，生成文本版本")
            return self._create_text_flowchart(title, nodes, edges)

        if not self.mcp_available:
            print("⚠️ draw.io MCP服务器不可用，生成文本版本")
            return self._create_text_flowchart(title, nodes, edges)

        # 调用真实的MCP服务器
        return self._create_real_flowchart(title, nodes, edges, output_format)

    def _create_text_flowchart(
        self,
        title: str,
        nodes: List[Dict],
        edges: List[Dict]
    ) -> str:
        """
        创建文本版流程图（降级方案）

        Args:
            title: 标题
            nodes: 节点列表
            edges: 边列表

        Returns:
            文件路径
        """
        output_file = self.diagrams_dir / f"{title}.txt"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write("## 流程图结构\n\n")

            # 写入节点
            f.write("### 节点\n\n")
            for node in nodes:
                node_id = node.get("id", "")
                label = node.get("label", "")
                node_type = node.get("type", "process")
                f.write(f"- [{node_id}] {label} ({node_type})\n")

            # 写入连接
            f.write("\n### 连接\n\n")
            for edge in edges:
                from_node = edge.get("from", "")
                to_node = edge.get("to", "")
                label = edge.get("label", "")
                if label:
                    f.write(f"- {from_node} → {to_node} ({label})\n")
                else:
                    f.write(f"- {from_node} → {to_node}\n")

            # ASCII艺术图（简单版）
            f.write("\n### ASCII流程图\n\n")
            f.write("```\n")
            for i, node in enumerate(nodes):
                label = node.get("label", "")
                f.write(f"[{label}]\n")
                if i < len(nodes) - 1:
                    f.write("  ↓\n")
            f.write("```\n")

        print(f"✅ 文本流程图已生成: {output_file}")
        return str(output_file)

    def _create_real_flowchart(
        self,
        title: str,
        nodes: List[Dict],
        edges: List[Dict],
        output_format: str
    ) -> str:
        """
        使用真实MCP服务器创建流程图

        Args:
            title: 标题
            nodes: 节点列表
            edges: 边列表
            output_format: 输出格式

        Returns:
            文件路径
        """
        # 构建MCP请求
        mcp_request = {
            "tool": "drawio",
            "action": "create_flowchart",
            "params": {
                "title": title,
                "nodes": nodes,
                "edges": edges,
                "format": output_format
            }
        }

        # 调用MCP服务器
        try:
            result = subprocess.run(
                ["mcp", "call", json.dumps(mcp_request)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                response = json.loads(result.stdout)
                output_file = response.get("file_path")

                if output_file:
                    print(f"✅ draw.io流程图已生成: {output_file}")
                    return output_file

        except Exception as e:
            print(f"❌ MCP调用失败: {e}")

        # 降级到文本版本
        return self._create_text_flowchart(title, nodes, edges)

    def create_architecture_diagram(
        self,
        title: str,
        components: List[Dict],
        connections: List[Dict],
        output_format: str = "xml"
    ) -> Optional[str]:
        """
        创建架构图

        Args:
            title: 图表标题
            components: 组件列表
            connections: 连接列表
            output_format: 输出格式

        Returns:
            生成的文件路径
        """
        if not self.enabled or not self.mcp_available:
            return self._create_text_architecture(title, components, connections)

        return self._create_real_architecture(title, components, connections, output_format)

    def _create_text_architecture(
        self,
        title: str,
        components: List[Dict],
        connections: List[Dict]
    ) -> str:
        """创建文本版架构图"""
        output_file = self.diagrams_dir / f"{title}-architecture.txt"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {title} - 系统架构\n\n")

            # 写入组件
            f.write("## 组件\n\n")
            for comp in components:
                comp_id = comp.get("id", "")
                name = comp.get("name", "")
                comp_type = comp.get("type", "service")
                description = comp.get("description", "")

                f.write(f"### {name}\n\n")
                f.write(f"- ID: {comp_id}\n")
                f.write(f"- 类型: {comp_type}\n")
                if description:
                    f.write(f"- 说明: {description}\n")
                f.write("\n")

            # 写入连接
            f.write("## 连接关系\n\n")
            for conn in connections:
                from_comp = conn.get("from", "")
                to_comp = conn.get("to", "")
                conn_type = conn.get("type", "uses")

                f.write(f"- {from_comp} --[{conn_type}]--> {to_comp}\n")

        print(f"✅ 文本架构图已生成: {output_file}")
        return str(output_file)

    def _create_real_architecture(
        self,
        title: str,
        components: List[Dict],
        connections: List[Dict],
        output_format: str
    ) -> str:
        """使用真实MCP创建架构图"""
        mcp_request = {
            "tool": "drawio",
            "action": "create_architecture",
            "params": {
                "title": title,
                "components": components,
                "connections": connections,
                "format": output_format
            }
        }

        try:
            result = subprocess.run(
                ["mcp", "call", json.dumps(mcp_request)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                response = json.loads(result.stdout)
                output_file = response.get("file_path")

                if output_file:
                    print(f"✅ draw.io架构图已生成: {output_file}")
                    return output_file

        except Exception as e:
            print(f"❌ MCP调用失败: {e}")

        return self._create_text_architecture(title, components, connections)

    def export_diagram(
        self,
        source_file: str,
        output_format: str = "png"
    ) -> Optional[str]:
        """
        导出图表为不同格式

        Args:
            source_file: 源文件路径（.drawio或.xml）
            output_format: 目标格式 (png, svg, pdf)

        Returns:
            导出的文件路径
        """
        if not self.mcp_available:
            print("⚠️ draw.io MCP不可用，无法导出")
            return None

        try:
            mcp_request = {
                "tool": "drawio",
                "action": "export",
                "params": {
                    "source": source_file,
                    "format": output_format
                }
            }

            result = subprocess.run(
                ["mcp", "call", json.dumps(mcp_request)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                response = json.loads(result.stdout)
                output_file = response.get("file_path")

                if output_file:
                    print(f"✅ 图表已导出: {output_file}")
                    return output_file

        except Exception as e:
            print(f"❌ 导出失败: {e}")

        return None


def get_drawio_client() -> DrawioMCPClient:
    """
    获取draw.io MCP客户端实例

    Returns:
        DrawioMCPClient实例
    """
    return DrawioMCPClient()


if __name__ == "__main__":
    # 测试
    client = get_drawio_client()

    # 测试流程图
    nodes = [
        {"id": "start", "label": "开始", "type": "start"},
        {"id": "task1", "label": "任务1", "type": "process"},
        {"id": "task2", "label": "任务2", "type": "process"},
        {"id": "end", "label": "结束", "type": "end"}
    ]

    edges = [
        {"from": "start", "to": "task1"},
        {"from": "task1", "to": "task2"},
        {"from": "task2", "to": "end"}
    ]

    result = client.create_flowchart("测试流程", nodes, edges)
    print(f"生成的文件: {result}")
