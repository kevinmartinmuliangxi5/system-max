"""
ECS - 观点模块

定义观点、消息、反馈等核心数据结构
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from enum import Enum
import numpy as np
import json


class MessageType(Enum):
    """消息类型"""
    INITIAL_ANALYSIS = "initial_analysis"  # 初始分析
    DISCUSSION = "discussion"              # 讨论
    SYNTHESIS = "synthesis"                # 综合
    FEEDBACK = "feedback"                  # 反馈
    PROPOSAL = "proposal"                  # 提案
    QUESTION = "question"                  # 问题
    CHALLENGE = "challenge"                # 挑战
    SUPPORT = "support"                    # 支持


@dataclass
class Viewpoint:
    """观点数据结构"""
    agent_id: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 观点组成部分
    propositions: List[str] = field(default_factory=list)    # 主张
    evidences: List[str] = field(default_factory=list)        # 证据
    constraints: List[str] = field(default_factory=list)      # 约束
    suggestions: List[str] = field(default_factory=list)      # 建议

    # 情感倾向
    sentiment: float = 0.5          # 情感倾向（0-1，0消极，1积极）
    confidence: float = 0.5         # 置信度（0-1）

    # 观点向量（用于计算相似度）
    embedding: Optional[np.ndarray] = None

    def __post_init__(self):
        """解析content提取组成部分"""
        if not self.propositions:
            self._extract_components()

    def _extract_components(self):
        """从content中提取组成部分"""
        # 简化版：基于关键词提取
        lines = self.content.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 识别主张
            if any(kw in line for kw in ['认为', '建议', '应该', '必须', '核心是']):
                if len(line) < 200:  # 避免过长段落
                    self.propositions.append(line)

            # 识别证据
            elif any(kw in line for kw in ['根据', '数据表明', '研究显示', '经验证明']):
                self.evidences.append(line)

            # 识别约束
            elif any(kw in line for kw in ['但是', '然而', '限制', '困难', '挑战']):
                self.constraints.append(line)

            # 识别建议
            elif any(kw in line for kw in ['可以', '建议', '推荐', '方案', '方法']):
                self.suggestions.append(line)

    def get_vector_representation(self, vocab_size: int = 1000) -> np.ndarray:
        """
        获取观点的向量表示（简化版词袋模型）

        Args:
            vocab_size: 词汇表大小

        Returns:
            向量表示
        """
        # 简化版：基于字符的哈希向量化
        vector = np.zeros(vocab_size)

        # 对content进行分词
        words = self.content.split()

        for word in words:
            # 简单的哈希函数
            idx = hash(word) % vocab_size
            vector[idx] += 1

        # 归一化
        if np.sum(vector) > 0:
            vector = vector / np.sum(vector)

        return vector

    def similarity_to(self, other: 'Viewpoint') -> float:
        """
        计算与另一个观点的相似度

        Args:
            other: 另一个观点

        Returns:
            相似度（0-1）
        """
        vec1 = self.embedding or self.get_vector_representation()
        vec2 = other.embedding or other.get_vector_representation()

        # 确保维度一致
        if vec1.shape[0] != vec2.shape[0]:
            min_dim = min(vec1.shape[0], vec2.shape[0])
            vec1 = vec1[:min_dim]
            vec2 = vec2[:min_dim]

        # 余弦相似度
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def distance_to(self, other: 'Viewpoint') -> float:
        """
        计算与另一个观点的距离

        Args:
            other: 另一个观点

        Returns:
            距离（0-1，0相同，1完全不同）
        """
        return 1.0 - self.similarity_to(other)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'agent_id': self.agent_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata,
            'propositions': self.propositions,
            'evidences': self.evidences,
            'constraints': self.constraints,
            'suggestions': self.suggestions,
            'sentiment': self.sentiment,
            'confidence': self.confidence
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Viewpoint':
        """从字典创建"""
        return cls(
            agent_id=data['agent_id'],
            content=data['content'],
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
            metadata=data.get('metadata', {}),
            propositions=data.get('propositions', []),
            evidences=data.get('evidences', []),
            constraints=data.get('constraints', []),
            suggestions=data.get('suggestions', []),
            sentiment=data.get('sentiment', 0.5),
            confidence=data.get('confidence', 0.5)
        )


@dataclass
class Message:
    """消息数据结构"""
    message_id: str
    agent_id: str
    content: str
    message_type: MessageType
    timestamp: datetime = field(default_factory=datetime.now)

    # 消息关系
    reply_to: Optional[str] = None      # 回复的消息ID
    references: List[str] = field(default_factory=list)  # 引用的观点

    # 附加信息
    round_num: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'message_id': self.message_id,
            'agent_id': self.agent_id,
            'content': self.content,
            'message_type': self.message_type.value,
            'timestamp': self.timestamp.isoformat(),
            'reply_to': self.reply_to,
            'references': self.references,
            'round_num': self.round_num,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """从字典创建"""
        return cls(
            message_id=data['message_id'],
            agent_id=data['agent_id'],
            content=data['content'],
            message_type=MessageType(data['message_type']),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
            reply_to=data.get('reply_to'),
            references=data.get('references', []),
            round_num=data.get('round_num', 0),
            metadata=data.get('metadata', {})
        )


@dataclass
class Feedback:
    """反馈数据结构"""
    feedback_id: str
    agent_id: str
    target_agent_id: str     # 反馈目标Agent
    content: str
    feedback_type: str       # positive/negative/suggestion

    # 评分
    quality_score: float = 0.0      # 质量评分（0-1）
    relevance_score: float = 0.0    # 相关性评分（0-1）
    novelty_score: float = 0.0      # 新颖性评分（0-1）

    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'feedback_id': self.feedback_id,
            'agent_id': self.agent_id,
            'target_agent_id': self.target_agent_id,
            'content': self.content,
            'feedback_type': self.feedback_type,
            'quality_score': self.quality_score,
            'relevance_score': self.relevance_score,
            'novelty_score': self.novelty_score,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class Solution:
    """解决方案数据结构"""
    content: str
    source_agents: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    # 方案组成部分
    problem_statement: str = ""
    proposed_solution: str = ""
    implementation_plan: List[str] = field(default_factory=list)
    risk_assessment: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)

    # 方案质量
    quality_score: float = 0.0
    consensus_score: float = 0.0
    innovation_score: float = 0.0

    # 追踪信息
    iteration_count: int = 0
    feedback_incorporated: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'content': self.content,
            'source_agents': self.source_agents,
            'timestamp': self.timestamp.isoformat(),
            'problem_statement': self.problem_statement,
            'proposed_solution': self.proposed_solution,
            'implementation_plan': self.implementation_plan,
            'risk_assessment': self.risk_assessment,
            'success_criteria': self.success_criteria,
            'quality_score': self.quality_score,
            'consensus_score': self.consensus_score,
            'innovation_score': self.innovation_score,
            'iteration_count': self.iteration_count,
            'feedback_incorporated': self.feedback_incorporated
        }


@dataclass
class DiscussionRound:
    """一轮讨论的数据"""
    round_num: int
    messages: List[Message] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    # 轮次统计
    participation_count: Dict[str, int] = field(default_factory=dict)
    topic_shifts: int = 0
    consensus_level: float = 0.0

    def add_message(self, message: Message):
        """添加消息"""
        self.messages.append(message)

        # 更新参与统计
        agent_id = message.agent_id
        self.participation_count[agent_id] = self.participation_count.get(agent_id, 0) + 1

    def finish(self):
        """结束本轮讨论"""
        self.end_time = datetime.now()

    def get_duration(self) -> float:
        """获取持续时间（秒）"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'round_num': self.round_num,
            'messages': [m.to_dict() for m in self.messages],
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'participation_count': self.participation_count,
            'topic_shifts': self.topic_shifts,
            'consensus_level': self.consensus_level
        }


class ViewpointSpace:
    """观点空间 - 管理所有观点及其关系"""

    def __init__(self):
        self.viewpoints: Dict[str, Viewpoint] = {}
        self.message_history: List[Message] = []
        self.discussion_rounds: List[DiscussionRound] = []

    def add_viewpoint(self, viewpoint: Viewpoint):
        """添加观点"""
        self.viewpoints[viewpoint.agent_id] = viewpoint

    def get_viewpoint(self, agent_id: str) -> Optional[Viewpoint]:
        """获取观点"""
        return self.viewpoints.get(agent_id)

    def get_all_viewpoints(self) -> List[Viewpoint]:
        """获取所有观点"""
        return list(self.viewpoints.values())

    def calculate_pairwise_distances(self) -> np.ndarray:
        """
        计算观点间的成对距离矩阵

        Returns:
            距离矩阵（n x n，n为观点数量）
        """
        viewpoints = self.get_all_viewpoints()
        n = len(viewpoints)

        if n == 0:
            return np.array([])

        distance_matrix = np.zeros((n, n))

        for i, vp1 in enumerate(viewpoints):
            for j, vp2 in enumerate(viewpoints):
                if i < j:
                    distance = vp1.distance_to(vp2)
                    distance_matrix[i, j] = distance
                    distance_matrix[j, i] = distance

        return distance_matrix

    def get_average_distance(self) -> float:
        """获取平均观点距离"""
        distances = self.calculate_pairwise_distances()
        if distances.size == 0:
            return 0.0

        # 取上三角（不包括对角线）
        n = distances.shape[0]
        upper_tri = distances[np.triu_indices(n, k=1)]

        if len(upper_tri) == 0:
            return 0.0

        return float(np.mean(upper_tri))

    def get_clustering_info(self) -> Dict[str, Any]:
        """
        获取观点聚类信息

        Returns:
            聚类信息字典
        """
        from sklearn.cluster import KMeans
        from scipy.spatial.distance import pdist, squareform

        viewpoints = self.get_all_viewpoints()
        if len(viewpoints) < 2:
            return {'cluster_count': 1, 'silhouette_score': 0.0}

        # 获取距离矩阵
        distances = self.calculate_pairwise_distances()

        # 尝试不同的聚类数量
        best_score = -1
        best_n = 1

        for n_clusters in range(2, min(len(viewpoints), 6)):
            # K-means聚类
            vectors = np.array([vp.get_vector_representation() for vp in viewpoints])
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = kmeans.fit_predict(vectors)

            # 计算轮廓系数
            from sklearn.metrics import silhouette_score
            score = silhouette_score(vectors, labels)

            if score > best_score:
                best_score = score
                best_n = n_clusters

        return {
            'cluster_count': best_n,
            'silhouette_score': best_score
        }

    def add_message(self, message: Message):
        """添加消息到历史"""
        self.message_history.append(message)

    def start_discussion_round(self, round_num: int) -> DiscussionRound:
        """开始新一轮讨论"""
        round_obj = DiscussionRound(round_num=round_num)
        self.discussion_rounds.append(round_obj)
        return round_obj

    def finish_discussion_round(self, round_num: int):
        """结束讨论轮"""
        for round_obj in self.discussion_rounds:
            if round_obj.round_num == round_num:
                round_obj.finish()
                break

    def get_discussion_round(self, round_num: int) -> Optional[DiscussionRound]:
        """获取指定轮次的讨论"""
        for round_obj in self.discussion_rounds:
            if round_obj.round_num == round_num:
                return round_obj
        return None

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        viewpoints = self.get_all_viewpoints()

        return {
            'total_viewpoints': len(viewpoints),
            'total_messages': len(self.message_history),
            'discussion_rounds': len(self.discussion_rounds),
            'average_distance': self.get_average_distance(),
            'clustering_info': self.get_clustering_info(),
            'agent_participation': self._get_participation_stats()
        }

    def _get_participation_stats(self) -> Dict[str, int]:
        """获取参与统计"""
        stats = {}

        for message in self.message_history:
            agent_id = message.agent_id
            stats[agent_id] = stats.get(agent_id, 0) + 1

        return stats

    def export_to_json(self) -> str:
        """导出为JSON"""
        data = {
            'viewpoints': [vp.to_dict() for vp in self.get_all_viewpoints()],
            'messages': [msg.to_dict() for msg in self.message_history],
            'discussion_rounds': [round_obj.to_dict() for round_obj in self.discussion_rounds],
            'statistics': self.get_statistics()
        }

        return json.dumps(data, ensure_ascii=False, indent=2)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'viewpoints': {k: v.to_dict() for k, v in self.viewpoints.items()},
            'message_history': [m.to_dict() for m in self.message_history],
            'discussion_rounds': [r.to_dict() for r in self.discussion_rounds],
            'statistics': self.get_statistics()
        }
