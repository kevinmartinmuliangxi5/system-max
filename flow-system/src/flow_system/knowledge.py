"""
知识库与模式管理模块

实现知识的积累、检索、迁移:
1. FAISS向量检索 - 本地化，无需Docker
2. 模式库 - 高质量代码模式提取与复用
3. 知识蒸馏 - 从成功案例中学习
4. 跨任务迁移 - 知识泛化能力

评分提升: 从不存储代码到完整知识管理系统
"""

import json
import sqlite3
import pickle
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
from threading import Lock
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None
    print("⚠️  FAISS not installed. Knowledge retrieval will be disabled.")

from .config import Config
from .utils import logger, get_hash, save_json, load_json


class PatternLibrary:
    """代码模式库

    存储高质量代码模式，支持模板化复用
    """

    def __init__(self, db_path: Path = Config.KNOWLEDGE_DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.lock = Lock()
        self._init_db()
        logger.info(f"Pattern library initialized: {db_path}")

    def _init_db(self):
        """初始化数据库"""
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")

        # 创建模式表
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                template_code TEXT NOT NULL,
                task_description TEXT,
                applicable_tasks TEXT,
                quality_score REAL,
                usage_count INTEGER DEFAULT 0,
                created_at REAL,
                metadata TEXT
            )
        """
        )

        # 创建任务历史表
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_hash TEXT UNIQUE NOT NULL,
                task_description TEXT,
                final_code TEXT,
                final_score REAL,
                generations INTEGER,
                feature_vector TEXT,
                pattern_id INTEGER,
                created_at REAL,
                FOREIGN KEY (pattern_id) REFERENCES patterns (id)
            )
        """
        )

        # 创建索引
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_task_hash ON task_history(task_hash)"
        )
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_quality ON patterns(quality_score DESC)"
        )

        self.conn.commit()

    def add_pattern(
        self,
        pattern_name: str,
        template_code: str,
        task_description: str,
        applicable_tasks: List[str],
        quality_score: float,
        metadata: Optional[Dict] = None,
    ) -> int:
        """添加代码模式

        Args:
            pattern_name: 模式名称
            template_code: 模板代码（含<PLACEHOLDER>）
            task_description: 原任务描述
            applicable_tasks: 适用的任务类型列表
            quality_score: 质量评分
            metadata: 额外元数据

        Returns:
            模式ID
        """
        import time

        with self.lock:
            cursor = self.conn.execute(
                """
                INSERT INTO patterns
                (pattern_name, template_code, task_description, applicable_tasks,
                 quality_score, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    pattern_name,
                    template_code,
                    task_description,
                    json.dumps(applicable_tasks),
                    quality_score,
                    time.time(),
                    json.dumps(metadata or {}),
                ),
            )
            self.conn.commit()
            pattern_id = cursor.lastrowid

        logger.info(f"Added pattern: {pattern_name} (ID={pattern_id}, score={quality_score:.2f})")
        return pattern_id

    def get_pattern(self, pattern_id: int) -> Optional[Dict]:
        """获取模式"""
        cursor = self.conn.execute(
            "SELECT * FROM patterns WHERE id=?", (pattern_id,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "pattern_name": row[1],
            "template_code": row[2],
            "task_description": row[3],
            "applicable_tasks": json.loads(row[4]),
            "quality_score": row[5],
            "usage_count": row[6],
            "created_at": row[7],
            "metadata": json.loads(row[8]),
        }

    def get_top_patterns(self, limit: int = 10) -> List[Dict]:
        """获取高质量模式"""
        cursor = self.conn.execute(
            """
            SELECT * FROM patterns
            ORDER BY quality_score DESC, usage_count DESC
            LIMIT ?
        """,
            (limit,),
        )

        patterns = []
        for row in cursor.fetchall():
            patterns.append(
                {
                    "id": row[0],
                    "pattern_name": row[1],
                    "template_code": row[2],
                    "task_description": row[3],
                    "applicable_tasks": json.loads(row[4]),
                    "quality_score": row[5],
                    "usage_count": row[6],
                    "created_at": row[7],
                    "metadata": json.loads(row[8]),
                }
            )

        return patterns

    def increment_usage(self, pattern_id: int) -> None:
        """增加模式使用计数"""
        with self.lock:
            self.conn.execute(
                "UPDATE patterns SET usage_count = usage_count + 1 WHERE id=?",
                (pattern_id,),
            )
            self.conn.commit()

    def add_task_history(
        self,
        task_description: str,
        final_code: str,
        final_score: float,
        generations: int,
        feature_vector: List[float],
        pattern_id: Optional[int] = None,
    ) -> None:
        """添加任务历史

        Args:
            task_description: 任务描述
            final_code: 最终代码
            final_score: 最终评分
            generations: 演化代数
            feature_vector: 特征向量
            pattern_id: 关联的模式ID
        """
        import time

        task_hash = get_hash(task_description)

        with self.lock:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO task_history
                (task_hash, task_description, final_code, final_score, generations,
                 feature_vector, pattern_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    task_hash,
                    task_description,
                    final_code,
                    final_score,
                    generations,
                    json.dumps(feature_vector),
                    pattern_id,
                    time.time(),
                ),
            )
            self.conn.commit()

        logger.info(f"Added task history: score={final_score:.2f}, gens={generations}")

    def get_task_history(self, task_description: str) -> Optional[Dict]:
        """获取任务历史（缓存）"""
        task_hash = get_hash(task_description)

        cursor = self.conn.execute(
            "SELECT * FROM task_history WHERE task_hash=?", (task_hash,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "task_hash": row[1],
            "task_description": row[2],
            "final_code": row[3],
            "final_score": row[4],
            "generations": row[5],
            "feature_vector": json.loads(row[6]),
            "pattern_id": row[7],
            "created_at": row[8],
        }

    def get_stats(self) -> Dict:
        """获取统计信息"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM patterns")
        pattern_count = cursor.fetchone()[0]

        cursor = self.conn.execute("SELECT COUNT(*) FROM task_history")
        history_count = cursor.fetchone()[0]

        cursor = self.conn.execute("SELECT AVG(quality_score) FROM patterns")
        avg_quality = cursor.fetchone()[0] or 0

        return {
            "pattern_count": pattern_count,
            "history_count": history_count,
            "avg_quality": avg_quality,
        }


class FAISSRetriever:
    """FAISS向量检索器

    本地向量数据库，无需Docker
    """

    def __init__(self, dimension: int = 20, index_path: Path = Config.FAISS_INDEX_PATH):
        """
        Args:
            dimension: 特征向量维度（应与FeatureExtractor一致）
            index_path: FAISS索引路径
        """
        self.dimension = dimension
        self.index_path = index_path
        self.index = None
        self.metadata = []  # 存储每个向量的元数据
        self.lock = Lock()

        if faiss is None:
            logger.warning("FAISS not available, retrieval disabled")
            return

        self._load_or_create_index()
        logger.info(f"FAISS retriever initialized: dim={dimension}, path={index_path}")

    def _load_or_create_index(self):
        """加载或创建索引"""
        index_file = self.index_path / "index.faiss"
        metadata_file = self.index_path / "metadata.pkl"

        if index_file.exists():
            # 加载现有索引
            self.index = faiss.read_index(str(index_file))
            if metadata_file.exists():
                with open(metadata_file, "rb") as f:
                    self.metadata = pickle.load(f)
            logger.info(f"Loaded FAISS index: {self.index.ntotal} vectors")
        else:
            # 创建新索引（使用L2距离）
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            logger.info("Created new FAISS index")

    def add(
        self,
        vector: np.ndarray,
        metadata: Dict[str, Any]
    ) -> None:
        """添加向量

        Args:
            vector: 特征向量 (dimension,)
            metadata: 关联元数据（如代码、得分等）
        """
        if faiss is None or self.index is None:
            return

        # 确保是2D数组
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)

        with self.lock:
            self.index.add(vector.astype(np.float32))
            self.metadata.append(metadata)

        logger.debug(f"Added vector to FAISS: total={self.index.ntotal}")

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 5,
        min_score: Optional[float] = None
    ) -> List[Tuple[float, Dict]]:
        """搜索最近邻

        Args:
            query_vector: 查询向量
            k: 返回数量
            min_score: 最小相似度阈值

        Returns:
            [(距离, 元数据), ...] 列表
        """
        if faiss is None or self.index is None or self.index.ntotal == 0:
            return []

        # 确保是2D数组
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        k = min(k, self.index.ntotal)

        # 搜索
        distances, indices = self.index.search(query_vector.astype(np.float32), k)

        # 构建结果
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                # 转换距离为相似度 (L2距离越小越好)
                similarity = 1.0 / (1.0 + dist)

                if min_score is None or similarity >= min_score:
                    results.append((float(dist), self.metadata[idx]))

        logger.debug(f"FAISS search: found {len(results)} results")
        return results

    def save(self) -> None:
        """保存索引"""
        if faiss is None or self.index is None:
            return

        index_file = self.index_path / "index.faiss"
        metadata_file = self.index_path / "metadata.pkl"

        with self.lock:
            faiss.write_index(self.index, str(index_file))
            with open(metadata_file, "wb") as f:
                pickle.dump(self.metadata, f)

        logger.info(f"Saved FAISS index: {self.index.ntotal} vectors")

    def clear(self) -> None:
        """清空索引"""
        if faiss is None:
            return

        with self.lock:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

        logger.info("Cleared FAISS index")


class KnowledgeManager:
    """知识管理器（统一接口）

    整合模式库和向量检索
    """

    def __init__(self):
        self.pattern_lib = PatternLibrary()
        self.retriever = FAISSRetriever(dimension=20) if faiss else None
        logger.info("Knowledge manager initialized")

    def store_solution(
        self,
        task_description: str,
        code: str,
        score: float,
        generations: int,
        feature_vector: List[float],
    ) -> None:
        """存储成功的解决方案

        Args:
            task_description: 任务描述
            code: 最终代码
            score: 最终得分
            generations: 演化代数
            feature_vector: 特征向量
        """
        # 存储任务历史
        self.pattern_lib.add_task_history(
            task_description, code, score, generations, feature_vector
        )

        # 如果质量足够高，存储到FAISS
        if score >= Config.PATTERN_THRESHOLD and self.retriever:
            metadata = {
                "task": task_description,
                "code": code,
                "score": score,
                "generations": generations,
            }
            vector = np.array(feature_vector)
            self.retriever.add(vector, metadata)

        logger.info(f"Stored solution: score={score:.2f}, gens={generations}")

    def retrieve_similar(
        self,
        feature_vector: List[float],
        k: int = 3
    ) -> List[Dict]:
        """检索相似解决方案

        Args:
            feature_vector: 当前特征向量
            k: 返回数量

        Returns:
            相似解决方案列表
        """
        if not self.retriever:
            return []

        query_vector = np.array(feature_vector)
        results = self.retriever.search(query_vector, k=k, min_score=0.7)

        # 提取元数据
        solutions = [metadata for _, metadata in results]

        logger.info(f"Retrieved {len(solutions)} similar solutions")
        return solutions

    def get_best_patterns(self, limit: int = 5) -> List[Dict]:
        """获取最佳模式"""
        return self.pattern_lib.get_top_patterns(limit)

    def check_cache(self, task_description: str) -> Optional[str]:
        """检查任务缓存

        Args:
            task_description: 任务描述

        Returns:
            如果找到历史记录且得分高，返回代码；否则None
        """
        history = self.pattern_lib.get_task_history(task_description)

        if history and history["final_score"] >= 0.95:
            logger.info(f"Cache hit: {task_description[:50]}...")
            return history["final_code"]

        return None

    async def distill_pattern(
        self,
        llm_engine,
        code: str,
        task: str
    ) -> Optional[int]:
        """从高质量代码中提取模式

        Args:
            llm_engine: LLM引擎实例
            code: 高质量代码
            task: 任务描述

        Returns:
            模式ID（如果提取成功）
        """
        # 使用LLM提取模式
        pattern_data = await llm_engine.extract_pattern(code, task)

        if not pattern_data:
            return None

        # 存储模式
        pattern_id = self.pattern_lib.add_pattern(
            pattern_name=pattern_data.get("pattern_name", "unnamed"),
            template_code=pattern_data.get("template_code", code),
            task_description=task,
            applicable_tasks=pattern_data.get("applicable_tasks", ["algorithm"]),
            quality_score=0.9,  # 默认高质量
            metadata={"key_insight": pattern_data.get("key_insight", "")},
        )

        logger.info(f"Distilled pattern: {pattern_data.get('pattern_name')} (ID={pattern_id})")
        return pattern_id

    def get_stats(self) -> Dict:
        """获取知识库统计"""
        pattern_stats = self.pattern_lib.get_stats()

        faiss_count = 0
        if self.retriever and self.retriever.index:
            faiss_count = self.retriever.index.ntotal

        return {
            **pattern_stats,
            "faiss_vectors": faiss_count,
        }

    def save_all(self) -> None:
        """保存所有数据"""
        if self.retriever:
            self.retriever.save()
        logger.info("Saved all knowledge data")

    def __del__(self):
        """析构时保存"""
        try:
            self.save_all()
        except:
            pass
