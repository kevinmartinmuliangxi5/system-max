"""
记忆集成器 - 融合Hippocampus和claude-mem的双记忆系统
"""
import json
import os
from typing import List, Dict, Optional, Any
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from .janus.core.hippocampus import Hippocampus
except:
    # 如果相对导入失败，尝试绝对导入
    try:
        from core.hippocampus import Hippocampus
    except:
        print("警告: 无法导入Hippocampus，将使用模拟实现")

        class Hippocampus:
            def retrieve(self, query, top_k=5):
                return []

# 导入增强版claude-mem
try:
    from claude_mem_enhanced import ClaudeMem
    CLAUDE_MEM_AVAILABLE = True
except ImportError:
    print("警告: 无法导入claude-mem增强版，将使用模拟实现")
    CLAUDE_MEM_AVAILABLE = False

    class ClaudeMem:
        """claude-mem模拟器（降级实现）"""

        def __init__(self, storage_dir: str = ".ralph/memories"):
            self.storage_dir = storage_dir
            self.sessions = []
            os.makedirs(storage_dir, exist_ok=True)

        def search(self, query: str, top_k: int = 5, obs_type: str = None) -> List[Dict]:
            return []

        def store_session(self, session_data: Dict, auto_compress: bool = True) -> str:
            session_id = f"sess-{len(self.sessions):04d}"
            self.sessions.append({"id": session_id, "data": session_data})
            return session_id

        def compress_session(self, session_id: str) -> List[Dict]:
            return []


class MemoryIntegrator:
    """双记忆系统集成器"""

    def __init__(
        self,
        hippocampus: Optional[Hippocampus] = None,
        claude_mem: Optional[ClaudeMem] = None,
        config: Optional[Dict] = None
    ):
        """
        初始化记忆集成器

        Args:
            hippocampus: 海马体实例（核心经验库）
            claude_mem: claude-mem实例（会话记忆）
            config: 配置字典
        """
        self.hippocampus = hippocampus or Hippocampus()
        self.claude_mem = claude_mem or ClaudeMem()
        self.config = config or self._load_default_config()

        # 标记是否使用真实claude-mem
        self.using_real_claude_mem = CLAUDE_MEM_AVAILABLE

    def _load_default_config(self) -> Dict:
        """加载默认配置"""
        return {
            "hippocampus_weight": 0.6,  # 核心经验权重更高
            "claude_mem_weight": 0.4,    # 完整历史权重稍低
            "top_k": 5,
            "merge_strategy": "weighted"  # weighted or interleave
        }

    def retrieve_combined(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> Dict[str, List[Dict]]:
        """
        从双记忆系统检索相关内容

        Args:
            query: 查询字符串
            top_k: 返回结果数量

        Returns:
            包含两个系统检索结果的字典
        """
        top_k = top_k or self.config["top_k"]

        # 并行检索两个系统
        hippo_results = self._retrieve_from_hippocampus(query, top_k)
        claudemem_results = self._retrieve_from_claudemem(query, top_k)

        return {
            "hippocampus": hippo_results,
            "claude_mem": claudemem_results,
            "merged": self._merge_results(hippo_results, claudemem_results)
        }

    def _retrieve_from_hippocampus(self, query: str, top_k: int) -> List[Dict]:
        """从Hippocampus检索"""
        try:
            results = self.hippocampus.retrieve(query, top_k=top_k)

            # 格式化结果
            formatted = []
            for item in results:
                if isinstance(item, dict):
                    formatted.append({
                        "source": "hippocampus",
                        "type": "core_experience",
                        "problem": item.get("problem", ""),
                        "solution": item.get("solution", ""),
                        "pitfalls": item.get("pitfalls", ""),
                        "score": item.get("score", 0.0)
                    })

            return formatted
        except Exception as e:
            print(f"警告: Hippocampus检索失败: {e}")
            return []

    def _retrieve_from_claudemem(self, query: str, top_k: int) -> List[Dict]:
        """从claude-mem检索"""
        try:
            results = self.claude_mem.search(query, top_k=top_k)

            # 格式化结果
            formatted = []
            for item in results:
                if isinstance(item, dict):
                    formatted.append({
                        "source": "claude_mem",
                        "type": item.get("type", "observation"),
                        "content": item.get("content", ""),
                        "context": item.get("context", ""),
                        "timestamp": item.get("timestamp", ""),
                        "score": item.get("score", 0.0)
                    })

            return formatted
        except Exception as e:
            print(f"警告: claude-mem检索失败: {e}")
            return []

    def _merge_results(
        self,
        hippo_results: List[Dict],
        claudemem_results: List[Dict]
    ) -> List[Dict]:
        """
        合并两个系统的检索结果

        Args:
            hippo_results: Hippocampus结果
            claudemem_results: claude-mem结果

        Returns:
            合并后的结果列表
        """
        strategy = self.config.get("merge_strategy", "weighted")

        if strategy == "weighted":
            return self._merge_weighted(hippo_results, claudemem_results)
        elif strategy == "interleave":
            return self._merge_interleave(hippo_results, claudemem_results)
        else:
            # 默认简单合并
            return hippo_results + claudemem_results

    def _merge_weighted(
        self,
        hippo_results: List[Dict],
        claudemem_results: List[Dict]
    ) -> List[Dict]:
        """加权合并策略"""
        hippo_weight = self.config["hippocampus_weight"]
        claudemem_weight = self.config["claude_mem_weight"]

        # 调整分数
        for item in hippo_results:
            item["weighted_score"] = item.get("score", 0) * hippo_weight

        for item in claudemem_results:
            item["weighted_score"] = item.get("score", 0) * claudemem_weight

        # 合并并排序
        all_results = hippo_results + claudemem_results
        all_results.sort(key=lambda x: x.get("weighted_score", 0), reverse=True)

        return all_results[:self.config["top_k"]]

    def _merge_interleave(
        self,
        hippo_results: List[Dict],
        claudemem_results: List[Dict]
    ) -> List[Dict]:
        """交叉合并策略（保证两个系统结果都出现）"""
        merged = []
        max_len = max(len(hippo_results), len(claudemem_results))

        for i in range(max_len):
            if i < len(hippo_results):
                merged.append(hippo_results[i])
            if i < len(claudemem_results):
                merged.append(claudemem_results[i])

        return merged[:self.config["top_k"]]

    def format_for_context(self, results: Dict[str, List[Dict]]) -> str:
        """
        将检索结果格式化为可注入上下文的文本

        Args:
            results: retrieve_combined的返回结果

        Returns:
            格式化的上下文字符串
        """
        context = []

        # 核心经验部分
        hippo_results = results.get("hippocampus", [])
        if hippo_results:
            context.append("## 核心经验 (来自Hippocampus)")
            context.append("")
            for i, item in enumerate(hippo_results, 1):
                context.append(f"### 经验 {i}")
                context.append(f"**问题**: {item.get('problem', 'N/A')}")
                context.append(f"**解决方案**: {item.get('solution', 'N/A')}")
                if item.get('pitfalls'):
                    context.append(f"**注意事项**: {item['pitfalls']}")
                context.append("")

        # 完整历史部分
        claudemem_results = results.get("claude_mem", [])
        if claudemem_results:
            context.append("## 完整历史上下文 (来自claude-mem)")
            context.append("")
            for i, item in enumerate(claudemem_results, 1):
                context.append(f"### 记录 {i}")
                context.append(f"**类型**: {item.get('type', 'N/A')}")
                context.append(f"**内容**: {item.get('content', 'N/A')}")
                if item.get('context'):
                    context.append(f"**上下文**: {item['context']}")
                context.append("")

        return "\n".join(context)

    def store_learning(self, learning_data: Dict) -> None:
        """
        存储学习标签数据到Hippocampus

        Args:
            learning_data: 包含problem, solution, pitfalls的字典
        """
        try:
            # 存储到Hippocampus
            key = learning_data.get("problem", "unnamed_task")
            value = {
                "solution": learning_data.get("solution", ""),
                "pitfalls": learning_data.get("pitfalls", "")
            }
            self.hippocampus.store(key, value)
            print(f"✓ 学习经验已存入Hippocampus: {key}")
        except Exception as e:
            print(f"警告: 存储学习经验失败: {e}")

    def store_session(self, session_data: Dict) -> str:
        """
        存储完整会话到claude-mem

        Args:
            session_data: 会话数据

        Returns:
            会话ID
        """
        try:
            session_id = self.claude_mem.store_session(session_data)
            print(f"✓ 会话已存入claude-mem: {session_id}")
            return session_id
        except Exception as e:
            print(f"警告: 存储会话失败: {e}")
            return ""


# 全局实例
_memory_integrator = None


def get_memory_integrator() -> MemoryIntegrator:
    """获取全局记忆集成器实例"""
    global _memory_integrator
    if _memory_integrator is None:
        _memory_integrator = MemoryIntegrator()
    return _memory_integrator


if __name__ == "__main__":
    # 测试
    integrator = MemoryIntegrator()

    print("测试双记忆系统检索:")
    results = integrator.retrieve_combined("用户登录功能")

    print(f"\nHippocampus结果: {len(results['hippocampus'])}条")
    print(f"claude-mem结果: {len(results['claude_mem'])}条")
    print(f"合并结果: {len(results['merged'])}条")

    print("\n格式化的上下文:")
    context = integrator.format_for_context(results)
    print(context[:500] if len(context) > 500 else context)
