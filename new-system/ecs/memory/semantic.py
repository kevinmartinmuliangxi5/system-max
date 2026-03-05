"""
语义记忆 - 存储抽象的知识和模式

类似人类的语义记忆，存储成功的模式、最佳实践等。
特点：
- 抽象知识：从具体经验中提取的通用模式
- 使用统计：记录模式使用频率和效果
- 增量学习：随时间积累和完善知识
- 分类管理：支持按类型组织模式
"""

from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import json
from threading import Lock
from datetime import datetime
import hashlib

from .base import (
    BaseMemory, MemoryConfig, MemoryType, MemoryEntry, MemoryQuery
)


class SemanticMemory(BaseMemory):
    """
    语义记忆 - 存储抽象的知识和模式

    语义记忆是系统的长期记忆，用于：
    - 存储从成功协作中提取的抽象模式
    - 保留最佳实践和经验规则
    - 维护模式的使用统计和效果评估
    - 支持模式的增量学习和更新

    特性：
    - 持久化存储：所有模式保存在单一JSON文件
    - 使用追踪：记录每个模式的使用次数和最后更新时间
    - 自动清理：低频使用的模式可被自动淘汰
    - 分类管理：支持按前缀命名约定组织模式
    """

    # 模式分类前缀
    PREFIX_SUCCESS = "success_pattern_"
    PREFIX_BEST_PRACTICE = "best_practice_"
    PREFIX_RULE = "rule_"
    PREFIX_TEMPLATE = "template_"

    def __init__(self, config: Optional[MemoryConfig] = None):
        super().__init__(config, MemoryType.SEMANTIC)
        self.storage_path = self.config.get_semantic_path()
        self._lock = Lock()
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self._load_patterns()

    def save(self, data: Union[Dict[str, Any], MemoryEntry]) -> bool:
        """
        保存或更新模式

        Args:
            data: 模式数据，格式：
                - {'pattern_name': str, 'pattern_data': dict}
                - MemoryEntry实例

        Returns:
            bool: 保存是否成功
        """
        try:
            with self._lock:
                if isinstance(data, MemoryEntry):
                    pattern_dict = data.to_dict()
                    pattern_name = pattern_dict.get('pattern_name')
                    pattern_data = pattern_dict.get('content', {})
                else:
                    pattern_name = data.get('pattern_name')
                    pattern_data = data.get('pattern_data', {})

                if not pattern_name:
                    return False

                # 获取现有模式或创建新模式
                existing = self.patterns.get(pattern_name, {})
                usage_count = existing.get('usage_count', 0) + 1

                # 合并数据，保留使用统计
                self.patterns[pattern_name] = {
                    **pattern_data,
                    'usage_count': usage_count,
                    'created_at': existing.get('created_at', self._now()),
                    'updated_at': self._now(),
                }

                self._save_patterns()
                return True

        except (OSError, IOError) as e:
            print(f"[警告] 语义记忆文件操作失败: {e}")
            return False
        except Exception as e:
            print(f"[警告] 保存模式失败: {e}")
            return False

    def load(self, query: Union[Dict[str, Any], MemoryQuery]) -> List[Dict[str, Any]]:
        """
        加载模式

        Args:
            query: 查询条件，支持：
                - {'type': 'pattern', 'name': str} - 获取指定模式
                - {'type': 'all'} - 获取所有模式
                - {'type': 'success'} - 获取成功模式
                - {'type': 'by_prefix', 'prefix': str} - 按前缀查询
                - {'type': 'by_category', 'category': str} - 按分类查询

        Returns:
            List[Dict]: 查询结果
        """
        with self._lock:
            query_type = query.get('type', 'all') if isinstance(query, dict) else query.query_type

            if query_type == 'pattern':
                name = query.get('name') if isinstance(query, dict) else query.filters.get('name')
                pattern = self.get_pattern(name)
                return [{**pattern, 'pattern_name': name}] if pattern else []

            elif query_type == 'success':
                return self._get_patterns_by_prefix(self.PREFIX_SUCCESS)

            elif query_type == 'by_prefix':
                prefix = query.get('prefix') if isinstance(query, dict) else query.filters.get('prefix')
                return self._get_patterns_by_prefix(prefix)

            elif query_type == 'by_category':
                category = query.get('category') if isinstance(query, dict) else query.filters.get('category')
                return self._get_patterns_by_category(category)

            else:
                # 返回所有模式
                return [
                    {**data, 'pattern_name': name}
                    for name, data in self.patterns.items()
                ]

    def clear(self) -> None:
        """清空所有模式"""
        with self._lock:
            self.patterns.clear()
            self._save_patterns()

    def count(self) -> int:
        """返回模式数量"""
        with self._lock:
            return len(self.patterns)

    # ==================== 便捷方法 ====================

    def save_pattern(
        self,
        pattern_name: str,
        pattern_data: Dict[str, Any]
    ) -> bool:
        """
        保存模式

        Args:
            pattern_name: 模式名称
            pattern_data: 模式数据

        Returns:
            bool: 是否保存成功
        """
        return self.save({
            'pattern_name': pattern_name,
            'pattern_data': pattern_data
        })

    def save_success_pattern(
        self,
        task: str,
        config: Dict[str, Any],
        emergence_score: float
    ) -> str:
        """
        保存成功模式（自动生成名称）

        Args:
            task: 任务描述
            config: 配置
            emergence_score: 涌现分数

        Returns:
            str: 生成的模式名称
        """
        # 基于任务生成稳定的模式名
        hash_val = hashlib.md5(task.encode()).hexdigest()[:8]
        pattern_name = f"{self.PREFIX_SUCCESS}{hash_val}"

        self.save_pattern(pattern_name, {
            'task': task,
            'config': config,
            'emergence_score': emergence_score,
            'category': self._infer_category(task)
        })

        return pattern_name

    def get_pattern(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """
        获取指定模式

        Args:
            pattern_name: 模式名称

        Returns:
            Optional[Dict]: 模式数据，不存在返回None
        """
        with self._lock:
            pattern = self.patterns.get(pattern_name)
            return pattern.copy() if pattern else None

    def get_all_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有模式

        Returns:
            Dict[str, Dict]: 所有模式的浅拷贝
        """
        with self._lock:
            return self.patterns.copy()

    def delete_pattern(self, pattern_name: str) -> bool:
        """
        删除模式

        Args:
            pattern_name: 模式名称

        Returns:
            bool: 是否删除成功
        """
        with self._lock:
            if pattern_name in self.patterns:
                del self.patterns[pattern_name]
                self._save_patterns()
                return True
            return False

    def get_success_patterns(self) -> List[Dict[str, Any]]:
        """
        获取所有成功模式

        Returns:
            List[Dict]: 成功模式列表
        """
        return self.load({'type': 'success'})

    def get_patterns_by_usage(self, min_usage: int = 1) -> List[Dict[str, Any]]:
        """
        获取满足最小使用次数的模式

        Args:
            min_usage: 最小使用次数

        Returns:
            List[Dict]: 符合条件的模式列表
        """
        with self._lock:
            return [
                {**data, 'pattern_name': name}
                for name, data in self.patterns.items()
                if data.get('usage_count', 0) >= min_usage
            ]

    def cleanup_low_usage_patterns(self, min_count: Optional[int] = None) -> int:
        """
        清理低频使用的模式

        Args:
            min_count: 最小使用次数，默认使用配置值

        Returns:
            int: 清理的模式数量
        """
        min_count = min_count or self.config.semantic_min_usage_count

        with self._lock:
            to_remove = [
                name for name, data in self.patterns.items()
                if data.get('usage_count', 0) < min_count
            ]

            for name in to_remove:
                del self.patterns[name]

            if to_remove:
                self._save_patterns()

            return len(to_remove)

    # ==================== 内部方法 ====================

    def _load_patterns(self) -> None:
        """从文件加载模式"""
        file_path = self.storage_path / "patterns.json"
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.patterns = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[警告] 语义记忆JSON解析失败: {e}")
                self.patterns = {}
            except Exception as e:
                print(f"[警告] 加载语义记忆失败: {e}")
                self.patterns = {}

    def _save_patterns(self) -> None:
        """保存模式到文件"""
        file_path = self.storage_path / "patterns.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)

    def _get_patterns_by_prefix(self, prefix: str) -> List[Dict[str, Any]]:
        """按前缀获取模式"""
        return [
            {**data, 'pattern_name': name}
            for name, data in self.patterns.items()
            if name.startswith(prefix)
        ]

    def _get_patterns_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按分类获取模式"""
        return [
            {**data, 'pattern_name': name}
            for name, data in self.patterns.items()
            if data.get('category') == category
        ]

    def _infer_category(self, task: str) -> str:
        """
        从任务描述推断分类

        Args:
            task: 任务描述

        Returns:
            str: 推断的分类
        """
        task_lower = task.lower()

        # 简单的关键词匹配分类
        category_keywords = {
            'code': ['code', '编程', '实现', '开发'],
            'design': ['design', '设计', '架构'],
            'analysis': ['analysis', '分析', '研究'],
            'optimization': ['optimization', '优化', '改进'],
            'debug': ['debug', '调试', '修复', 'bug'],
        }

        for category, keywords in category_keywords.items():
            if any(kw in task_lower for kw in keywords):
                return category

        return 'general'
