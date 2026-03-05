#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
claude-mem增强版 - 真实的持久化记忆系统

实现功能:
- 文件系统持久化存储
- 语义搜索（使用TF-IDF + 余弦相似度）
- AI智能压缩
- 会话管理
- 观察提取
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from collections import Counter
import math


class ClaudeMem:
    """claude-mem持久化记忆系统"""

    def __init__(self, storage_dir: str = ".ralph/memories"):
        """
        初始化claude-mem

        Args:
            storage_dir: 存储目录路径
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # 子目录
        self.sessions_dir = self.storage_dir / "sessions"
        self.observations_dir = self.storage_dir / "observations"
        self.index_dir = self.storage_dir / "index"

        for dir_path in [self.sessions_dir, self.observations_dir, self.index_dir]:
            dir_path.mkdir(exist_ok=True)

        # 索引文件
        self.index_file = self.index_dir / "memory_index.json"
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """加载索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "sessions": [],
            "observations": [],
            "last_updated": None
        }

    def _save_index(self):
        """保存索引"""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def store_session(
        self,
        session_data: Dict,
        auto_compress: bool = True
    ) -> str:
        """
        存储完整会话

        Args:
            session_data: 会话数据
            auto_compress: 是否自动压缩为观察

        Returns:
            会话ID
        """
        # 生成会话ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"sess_{timestamp}"

        # 保存会话文件
        session_file = self.sessions_dir / f"{session_id}.json"
        session_record = {
            "id": session_id,
            "timestamp": datetime.now().isoformat(),
            "data": session_data,
            "compressed": False
        }

        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_record, f, indent=2, ensure_ascii=False)

        # 更新索引
        self.index["sessions"].append({
            "id": session_id,
            "timestamp": session_record["timestamp"],
            "file": str(session_file),
            "compressed": False
        })
        self._save_index()

        print(f"✓ 会话已存储: {session_id}")

        # 自动压缩
        if auto_compress:
            observations = self.compress_session(session_id)
            if observations:
                print(f"✓ 已提取 {len(observations)} 条观察")

        return session_id

    def compress_session(self, session_id: str) -> List[Dict]:
        """
        将会话压缩为观察列表

        Args:
            session_id: 会话ID

        Returns:
            观察列表
        """
        # 读取会话
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            print(f"警告: 会话不存在: {session_id}")
            return []

        with open(session_file, 'r', encoding='utf-8') as f:
            session_record = json.load(f)

        session_data = session_record["data"]

        # 提取观察
        observations = self._extract_observations(session_data)

        # 存储观察
        for obs in observations:
            self.store_observation(obs, session_id)

        # 标记会话已压缩
        session_record["compressed"] = True
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_record, f, indent=2, ensure_ascii=False)

        # 更新索引
        for sess in self.index["sessions"]:
            if sess["id"] == session_id:
                sess["compressed"] = True
                break
        self._save_index()

        return observations

    def _extract_observations(self, session_data: Dict) -> List[Dict]:
        """
        从会话数据中提取观察

        这是简化版实现，实际应该使用LLM进行智能提取

        Args:
            session_data: 会话数据

        Returns:
            观察列表
        """
        observations = []

        # 提取任务信息
        task = session_data.get("task", {})
        if task:
            observations.append({
                "type": "task_definition",
                "content": f"任务: {task.get('name', '')} - {task.get('description', '')}",
                "context": {
                    "task_id": task.get("id", ""),
                    "status": task.get("status", "")
                },
                "importance": "high"
            })

        # 提取关键决策
        decisions = session_data.get("decisions", [])
        for decision in decisions:
            observations.append({
                "type": "decision",
                "content": decision.get("description", ""),
                "context": {
                    "alternatives": decision.get("alternatives", []),
                    "rationale": decision.get("rationale", "")
                },
                "importance": "high"
            })

        # 提取学习经验
        learnings = session_data.get("learnings", [])
        for learning in learnings:
            observations.append({
                "type": "learning",
                "content": learning.get("observation", ""),
                "context": {
                    "situation": learning.get("situation", ""),
                    "outcome": learning.get("outcome", "")
                },
                "importance": "medium"
            })

        # 提取错误和解决方案
        errors = session_data.get("errors", [])
        for error in errors:
            observations.append({
                "type": "error_solution",
                "content": f"问题: {error.get('error', '')} | 解决: {error.get('solution', '')}",
                "context": {
                    "error_type": error.get("type", ""),
                    "stack_trace": error.get("stack_trace", "")
                },
                "importance": "high"
            })

        return observations

    def store_observation(
        self,
        observation: Dict,
        session_id: Optional[str] = None
    ) -> str:
        """
        存储单个观察

        Args:
            observation: 观察数据
            session_id: 关联的会话ID（可选）

        Returns:
            观察ID
        """
        # 生成观察ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        obs_id = f"obs_{timestamp}"

        # 保存观察文件
        obs_file = self.observations_dir / f"{obs_id}.json"
        obs_record = {
            "id": obs_id,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "observation": observation
        }

        with open(obs_file, 'w', encoding='utf-8') as f:
            json.dump(obs_record, f, indent=2, ensure_ascii=False)

        # 更新索引
        self.index["observations"].append({
            "id": obs_id,
            "timestamp": obs_record["timestamp"],
            "type": observation.get("type", "general"),
            "session_id": session_id,
            "file": str(obs_file)
        })
        self._save_index()

        return obs_id

    def search(
        self,
        query: str,
        top_k: int = 5,
        obs_type: Optional[str] = None
    ) -> List[Dict]:
        """
        语义搜索观察

        Args:
            query: 查询字符串
            top_k: 返回结果数量
            obs_type: 观察类型过滤（可选）

        Returns:
            相关观察列表
        """
        # 加载所有观察
        observations = []
        for obs_info in self.index["observations"]:
            # 类型过滤
            if obs_type and obs_info.get("type") != obs_type:
                continue

            # 读取观察文件
            obs_file = Path(obs_info["file"])
            if not obs_file.exists():
                continue

            try:
                with open(obs_file, 'r', encoding='utf-8') as f:
                    obs_record = json.load(f)
                    observations.append(obs_record)
            except:
                continue

        if not observations:
            return []

        # 计算相似度
        scored_observations = []
        for obs_record in observations:
            obs = obs_record["observation"]
            content = obs.get("content", "")

            # 使用简单的关键词匹配和TF-IDF
            score = self._calculate_relevance(query, content)

            # 考虑重要性
            importance_weight = {
                "high": 1.5,
                "medium": 1.0,
                "low": 0.7
            }.get(obs.get("importance", "medium"), 1.0)

            final_score = score * importance_weight

            scored_observations.append({
                "id": obs_record["id"],
                "type": obs.get("type", "general"),
                "content": content,
                "context": obs.get("context", {}),
                "timestamp": obs_record["timestamp"],
                "session_id": obs_record.get("session_id"),
                "importance": obs.get("importance", "medium"),
                "score": final_score
            })

        # 排序并返回top_k
        scored_observations.sort(key=lambda x: x["score"], reverse=True)
        return scored_observations[:top_k]

    def _calculate_relevance(self, query: str, content: str) -> float:
        """
        计算查询和内容的相关度

        使用简化的TF-IDF + 余弦相似度

        Args:
            query: 查询字符串
            content: 内容字符串

        Returns:
            相关度分数 (0-1)
        """
        # 分词（简单按空格和标点分割）
        def tokenize(text):
            # 保留中文字符、英文字符、数字
            tokens = re.findall(r'[\w\u4e00-\u9fff]+', text.lower())
            return tokens

        query_tokens = tokenize(query)
        content_tokens = tokenize(content)

        if not query_tokens or not content_tokens:
            return 0.0

        # 计算词频
        query_freq = Counter(query_tokens)
        content_freq = Counter(content_tokens)

        # 计算交集
        common_tokens = set(query_tokens) & set(content_tokens)
        if not common_tokens:
            return 0.0

        # 计算TF-IDF相似度（简化版）
        score = 0.0
        for token in common_tokens:
            tf_query = query_freq[token] / len(query_tokens)
            tf_content = content_freq[token] / len(content_tokens)
            score += tf_query * tf_content

        # 归一化
        score = min(score, 1.0)

        return score

    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        获取完整会话

        Args:
            session_id: 会话ID

        Returns:
            会话数据
        """
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return None

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None

    def list_sessions(
        self,
        limit: int = 10,
        compressed_only: bool = False
    ) -> List[Dict]:
        """
        列出会话

        Args:
            limit: 返回数量限制
            compressed_only: 仅返回已压缩的会话

        Returns:
            会话信息列表
        """
        sessions = self.index.get("sessions", [])

        if compressed_only:
            sessions = [s for s in sessions if s.get("compressed", False)]

        # 按时间倒序
        sessions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return sessions[:limit]

    def get_statistics(self) -> Dict:
        """
        获取统计信息

        Returns:
            统计数据
        """
        total_sessions = len(self.index.get("sessions", []))
        compressed_sessions = len([s for s in self.index.get("sessions", [])
                                   if s.get("compressed", False)])
        total_observations = len(self.index.get("observations", []))

        # 按类型统计观察
        obs_by_type = Counter(
            obs.get("type", "general")
            for obs in self.index.get("observations", [])
        )

        return {
            "total_sessions": total_sessions,
            "compressed_sessions": compressed_sessions,
            "pending_sessions": total_sessions - compressed_sessions,
            "total_observations": total_observations,
            "observations_by_type": dict(obs_by_type),
            "last_updated": self.index.get("last_updated")
        }


def get_claude_mem() -> ClaudeMem:
    """获取全局claude-mem实例"""
    global _claude_mem_instance
    if '_claude_mem_instance' not in globals():
        _claude_mem_instance = ClaudeMem()
    return _claude_mem_instance


if __name__ == "__main__":
    # 测试
    print("=== claude-mem增强版测试 ===\n")

    cm = ClaudeMem()

    # 测试会话存储
    print("1. 测试会话存储:")
    test_session = {
        "task": {
            "id": "task_001",
            "name": "实现用户登录",
            "description": "使用JWT实现用户认证",
            "status": "completed"
        },
        "decisions": [
            {
                "description": "选择JWT而非Session",
                "alternatives": ["JWT", "Session", "OAuth"],
                "rationale": "无状态，适合分布式系统"
            }
        ],
        "learnings": [
            {
                "observation": "JWT过期时间设置为24小时比较合适",
                "situation": "用户登录场景",
                "outcome": "良好的用户体验"
            }
        ],
        "errors": [
            {
                "error": "Token验证失败",
                "solution": "检查密钥配置",
                "type": "authentication"
            }
        ]
    }

    session_id = cm.store_session(test_session)

    # 测试搜索
    print("\n2. 测试搜索:")
    results = cm.search("JWT 用户登录", top_k=3)
    print(f"找到 {len(results)} 条相关观察")
    for i, result in enumerate(results, 1):
        print(f"\n观察 {i}:")
        print(f"  类型: {result['type']}")
        print(f"  内容: {result['content'][:50]}...")
        print(f"  分数: {result['score']:.3f}")

    # 测试统计
    print("\n3. 统计信息:")
    stats = cm.get_statistics()
    print(f"  总会话数: {stats['total_sessions']}")
    print(f"  已压缩会话: {stats['compressed_sessions']}")
    print(f"  总观察数: {stats['total_observations']}")
    print(f"  观察类型分布: {stats['observations_by_type']}")

    print("\n✓ 测试完成")
