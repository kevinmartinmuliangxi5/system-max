"""
情景记忆 - 存储具体的事件和经历

类似人类的情景记忆，记录每次完整的协作过程。
特点：
- 时间序列：按时间顺序存储历史事件
- 可追溯：每个事件都有唯一ID和时间戳
- 相似检索：支持基于任务相似度的历史查询
- 持久化：自动保存到磁盘，重启后可恢复
"""

import numpy as np
from typing import List, Dict, Any, Optional, Union, Set
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib
from threading import Lock

from .base import (
    BaseMemory, MemoryConfig, MemoryType, MemoryEntry, MemoryQuery
)


class EpisodicMemory(BaseMemory):
    """
    情景记忆 - 存储具体的事件和经历

    情景记忆是系统的中期记忆，用于：
    - 记录每次完整的协作过程（任务、配置、结果）
    - 保留历史事件的详细记录
    - 支持基于相似度的历史查询
    - 提供最佳配置推荐

    特性：
    - 持久化存储：每个情景保存为独立JSON文件
    - 容量管理：超过最大数量时自动淘汰最旧记录
    - 相似度检索：基于任务关键词匹配历史情景
    - 时间索引：支持按时间范围查询
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        super().__init__(config, MemoryType.EPISODIC)
        self.storage_path = self.config.get_episodic_path()
        self._lock = Lock()
        self.episodes: List[Dict[str, Any]] = []
        self._load_episodes()

    def save(self, data: Union[Dict[str, Any], MemoryEntry]) -> bool:
        """
        保存一个情景（一次完整的协作）

        Args:
            data: 情景数据，格式：
                - {'task': str, 'config': dict, 'result': dict, 'emergence_score': float}
                - MemoryEntry实例

        Returns:
            bool: 保存是否成功
        """
        try:
            with self._lock:
                if isinstance(data, MemoryEntry):
                    episode = data.to_dict()
                else:
                    task = data.get('task', '')
                    config = data.get('config', {})
                    result = data.get('result', {})
                    emergence_score = data.get('emergence_score', 0.0)
                    metadata = data.get('metadata', {})

                    episode = {
                        "id": self._generate_id(),
                        "timestamp": self._now(),
                        "task": task,
                        "config": config,
                        "result": result,
                        "emergence_score": emergence_score,
                        "task_embedding": self._encode_task(task),
                        "metadata": metadata
                    }

                self.episodes.append(episode)
                self._save_episode(episode)

                # 容量管理：超过最大数量时淘汰最旧的
                max_episodes = self.config.episodic_max_episodes
                if len(self.episodes) > max_episodes:
                    removed = self.episodes.pop(0)
                    self._delete_episode(removed['id'])

                return True

        except (OSError, IOError) as e:
            print(f"[警告] 情景记忆文件操作失败: {e}")
            return False
        except Exception as e:
            print(f"[警告] 保存情景失败: {e}")
            return False

    def load(self, query: Union[Dict[str, Any], MemoryQuery]) -> List[Dict[str, Any]]:
        """
        加载情景

        Args:
            query: 查询条件，支持：
                - {'type': 'similar', 'task': str, 'top_k': int} - 查找相似情景
                - {'type': 'best_configs', 'task': str} - 获取最佳配置
                - {'type': 'by_id', 'id': str} - 按ID查询
                - {'type': 'by_time_range', 'start': str, 'end': str} - 按时间范围
                - {'type': 'all'} - 获取所有情景

        Returns:
            List[Dict]: 查询结果
        """
        with self._lock:
            query_type = query.get('type', 'all') if isinstance(query, dict) else query.query_type

            if query_type == 'similar':
                task = query.get('task') if isinstance(query, dict) else query.filters.get('task')
                top_k = query.get('top_k', query.get('limit', 3)) if isinstance(query, dict) else query.limit
                return self.find_similar_episodes(task, top_k)

            elif query_type == 'best_configs':
                task = query.get('task') if isinstance(query, dict) else query.filters.get('task')
                configs = self.get_best_configs(task)
                return [{'config': c} for c in configs]

            elif query_type == 'by_id':
                episode_id = query.get('id') if isinstance(query, dict) else query.filters.get('id')
                episode = self.get_episode(episode_id)
                return [episode] if episode else []

            elif query_type == 'by_time_range':
                start = query.get('start') if isinstance(query, dict) else query.filters.get('start')
                end = query.get('end') if isinstance(query, dict) else query.filters.get('end')
                return self.get_episodes_by_time_range(start, end)

            else:
                return self.episodes.copy()

    def clear(self) -> None:
        """清空所有情景"""
        with self._lock:
            self.episodes.clear()
            for file in self.storage_path.glob("*.json"):
                file.unlink()

    def count(self) -> int:
        """返回情景数量"""
        with self._lock:
            return len(self.episodes)

    # ==================== 内部方法 ====================

    def _encode_task(self, task: str) -> List[float]:
        """
        编码任务为向量

        注意：这里使用简单的hash编码作为占位符
        阶段三将替换为sentence-transformers的向量嵌入

        Args:
            task: 任务描述文本

        Returns:
            List[float]: 任务向量表示
        """
        # 使用稳定的hash算法，确保跨运行一致性
        hash_obj = hashlib.md5(task.encode('utf-8'))
        hash_val = int(hash_obj.hexdigest(), 16) % 10000
        return [hash_val / 10000.0]

    def _save_episode(self, episode: Dict[str, Any]) -> None:
        """
        保存情景到文件

        Args:
            episode: 情景数据
        """
        file_path = self.storage_path / f"{episode['id']}.json"
        episode_copy = episode.copy()

        # 确保数据可JSON序列化
        if 'task_embedding' in episode_copy:
            embedding = episode_copy['task_embedding']
            if isinstance(embedding, np.ndarray):
                episode_copy['task_embedding'] = embedding.tolist()
            elif not isinstance(embedding, list):
                episode_copy['task_embedding'] = list(embedding)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(episode_copy, f, ensure_ascii=False, indent=2)

    def _delete_episode(self, episode_id: str) -> None:
        """
        删除情景文件

        Args:
            episode_id: 情景ID
        """
        file_path = self.storage_path / f"{episode_id}.json"
        if file_path.exists():
            file_path.unlink()

    def _load_episodes(self) -> None:
        """从文件加载所有情景"""
        self.episodes = []
        if not self.storage_path.exists():
            self.storage_path.mkdir(parents=True, exist_ok=True)
            return

        for file in sorted(self.storage_path.glob("*.json")):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    episode = json.load(f)
                    # 恢复为numpy数组（兼容性处理）
                    if 'task_embedding' in episode:
                        episode['task_embedding'] = list(episode['task_embedding'])
                    self.episodes.append(episode)
            except json.JSONDecodeError as e:
                print(f"[警告] JSON解析失败 {file.name}: {e}")
            except Exception as e:
                print(f"[警告] 加载情景失败 {file.name}: {e}")

    # ==================== 公开方法 ====================

    def find_similar_episodes(self, task: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        查找相似的历史情景

        注意：这里使用简单的关键词匹配作为占位符
        阶段三将替换为向量相似度检索

        Args:
            task: 当前任务描述
            top_k: 返回最相似的k个情景

        Returns:
            List[Dict]: 相似情景列表
        """
        with self._lock:
            if not self.episodes:
                return []

            # 简化版本：基于关键词匹配
            task_words = set(task.lower().split())
            scored_episodes = []

            for ep in self.episodes:
                ep_words = set(ep.get('task', '').lower().split())
                overlap = len(task_words & ep_words)
                if overlap > 0:
                    scored_episodes.append((ep, overlap))

            scored_episodes.sort(key=lambda x: x[1], reverse=True)
            return [ep for ep, _ in scored_episodes[:top_k]]

    def get_best_configs(self, task: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        获取针对相似任务的最佳配置

        Args:
            task: 当前任务描述
            top_k: 返回前k个最佳配置

        Returns:
            List[Dict]: 最佳配置列表
        """
        similar = self.find_similar_episodes(task, top_k=10)
        # 按涌现分数排序
        similar.sort(key=lambda ep: ep.get('emergence_score', 0), reverse=True)
        return [ep.get('config', {}) for ep in similar[:top_k]]

    def get_episode(self, episode_id: str) -> Optional[Dict[str, Any]]:
        """
        获取指定情景

        Args:
            episode_id: 情景ID

        Returns:
            Optional[Dict]: 情景数据，不存在则返回None
        """
        with self._lock:
            for ep in self.episodes:
                if ep['id'] == episode_id:
                    return ep.copy()
            return None

    def get_episodes_by_time_range(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        按时间范围获取情景

        Args:
            start: 起始时间（ISO格式）
            end: 结束时间（ISO格式）

        Returns:
            List[Dict]: 时间范围内的情景列表
        """
        with self._lock:
            if not start and not end:
                return self.episodes.copy()

            result = []
            for ep in self.episodes:
                ep_time = ep.get('timestamp', '')
                if start and ep_time < start:
                    continue
                if end and ep_time > end:
                    continue
                result.append(ep.copy())

            return result

    def cleanup_old_episodes(self, retention_days: Optional[int] = None) -> int:
        """
        清理过期的情景记录

        Args:
            retention_days: 保留天数，默认使用配置值

        Returns:
            int: 清理的情景数量
        """
        retention_days = retention_days or self.config.episodic_retention_days
        cutoff_time = (datetime.now() - timedelta(days=retention_days)).isoformat()

        with self._lock:
            to_remove = [
                ep for ep in self.episodes
                if ep.get('timestamp', '') < cutoff_time
            ]

            for ep in to_remove:
                self.episodes.remove(ep)
                self._delete_episode(ep['id'])

            return len(to_remove)
