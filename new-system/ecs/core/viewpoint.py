"""
ECS - Viewpoint和Message数据结构
支持观点空间、相似度计算、涌现检测
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from datetime import datetime
import json
import re


# ============================================================
# 枚举类型
# ============================================================

class EmergenceType(Enum):
    """涌现类型"""
    AGGREGATION = "aggregation"      # 聚合涌现：观点简单聚合
    COORDINATION = "coordination"     # 协调涌现：角色分工协作
    SYNERGY = "synergy"              # 协同涌现：深度观点整合
    INNOVATION = "innovation"         # 创新涌现：突破性洞察
    META_EMERGENCE = "meta_emergence" # 元涌现：范式转移


class SystemPhase(Enum):
    """系统阶段"""
    EXPLORATION = "exploration"   # 探索期：高多样性，低共识
    DEBATE = "debate"            # 辩论期：观点碰撞
    CONVERGENCE = "convergence"  # 收敛期：走向共识
    CONSENSUS = "consensus"      # 共识期：高度一致
    STAGNATION = "stagnation"    # 停滞期：低多样性，低共识


class MessageType(Enum):
    """消息类型"""
    SENSE = "sense"       # 感知阶段输出
    DISCUSS = "discuss"   # 讨论阶段发言
    ACT = "act"          # 行动阶段输出
    REFLECT = "reflect"   # 反思阶段输出
    SYSTEM = "system"     # 系统消息


# ============================================================
# Viewpoint - 观点数据结构
# ============================================================

@dataclass
class Viewpoint:
    """
    观点数据结构

    一个观点包含：
    - 命题（Claims）：提出的论点
    - 证据（Evidences）：支持论点的证据
    - 约束（Constraints）：识别的约束条件
    - 建议（Suggestions）：提出的建议
    - 置信度（Confidence）：对观点的信心
    """

    agent_id: str
    content: str                    # 观点完整内容
    propositions: List[str] = field(default_factory=list)   # 命题
    evidences: List[str] = field(default_factory=list)      # 证据
    constraints: List[str] = field(default_factory=list)    # 约束
    suggestions: List[str] = field(default_factory=list)    # 建议
    confidence: float = 0.5          # 置信度 0-1
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    phase: str = "discuss"           # 所属阶段
    embedding: Optional[np.ndarray] = None  # 向量嵌入（延迟计算）

    def extract_propositions(self) -> List[str]:
        """从内容中提取命题"""
        # 简单实现：按句子分割
        sentences = re.split(r'[。！？.!?]', self.content)
        # 过滤掉空句子和太短的句子
        propositions = [s.strip() for s in sentences if len(s.strip()) > 10]
        self.propositions = propositions
        return propositions

    def extract_evidences(self) -> List[str]:
        """从内容中提取证据"""
        # 查找包含"因为"、"根据"、"证据显示"等关键词的句子
        evidence_keywords = ['因为', '由于', '根据', '证据', '研究', '数据', 'because', 'according', 'evidence']
        evidences = []
        sentences = re.split(r'[。！？.!?]', self.content)
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in evidence_keywords):
                evidences.append(sentence.strip())
        self.evidences = evidences
        return evidences

    def extract_constraints(self) -> List[str]:
        """从内容中提取约束条件"""
        # 查找包含"限制"、"约束"、"必须"、"不能"等关键词的句子
        constraint_keywords = ['限制', '约束', '必须', '不能', '禁止', '要求',
                              'limit', 'constraint', 'must', 'cannot', 'require']
        constraints = []
        sentences = re.split(r'[。！？.!?]', self.content)
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in constraint_keywords):
                constraints.append(sentence.strip())
        self.constraints = constraints
        return constraints

    def extract_suggestions(self) -> List[str]:
        """从内容中提取建议"""
        # 查找包含"建议"、"推荐"、"应该"、"可以"等关键词的句子
        suggestion_keywords = ['建议', '推荐', '应该', '可以', '考虑',
                              'suggest', 'recommend', 'should', 'consider']
        suggestions = []
        sentences = re.split(r'[。！？.!?]', self.content)
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in suggestion_keywords):
                suggestions.append(sentence.strip())
        self.suggestions = suggestions
        return suggestions

    def get_embedding(self, model=None) -> np.ndarray:
        """获取观点的向量嵌入"""
        if self.embedding is None:
            # 简单实现：使用词频向量
            # 实际应用中应使用专业的嵌入模型
            words = self.content.lower().split()
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            # 转换为向量
            self.embedding = np.array(list(word_freq.values()))
        return self.embedding

    def similarity_to(self, other: 'Viewpoint') -> float:
        """
        计算与另一个观点的余弦相似度

        Args:
            other: 另一个Viewpoint对象

        Returns:
            相似度值 0-1
        """
        # 使用简单的词袋模型计算相似度
        words1 = set(self.content.lower().split())
        words2 = set(other.content.lower().split())

        if not words1 or not words2:
            return 0.0

        # Jaccard相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def distance_to(self, other: 'Viewpoint') -> float:
        """
        计算与另一个观点的距离

        Args:
            other: 另一个Viewpoint对象

        Returns:
            距离值 0-1
        """
        return 1.0 - self.similarity_to(other)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "agent_id": self.agent_id,
            "content": self.content,
            "propositions": self.propositions,
            "evidences": self.evidences,
            "constraints": self.constraints,
            "suggestions": self.suggestions,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "phase": self.phase
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Viewpoint':
        """从字典创建Viewpoint"""
        return cls(**data)

    def __repr__(self) -> str:
        return f"Viewpoint(agent={self.agent_id}, confidence={self.confidence:.2f})"


# ============================================================
# Message - 消息数据结构
# ============================================================

@dataclass
class Message:
    """
    消息数据结构

    记录讨论过程中的每条消息
    """

    message_id: str
    agent_id: str
    content: str
    message_type: MessageType
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    round_num: int = 0
    references: List[str] = field(default_factory=list)  # 引用的其他消息ID
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "message_id": self.message_id,
            "agent_id": self.agent_id,
            "content": self.content,
            "message_type": self.message_type.value,
            "timestamp": self.timestamp,
            "round_num": self.round_num,
            "references": self.references,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        """从字典创建Message"""
        data['message_type'] = MessageType(data['message_type'])
        return cls(**data)

    def __repr__(self) -> str:
        return f"Message({self.agent_id}, {self.message_type.value}, round={self.round_num})"


# ============================================================
# ViewpointSpace - 观点空间
# ============================================================

class ViewpointSpace:
    """
    观点空间

    管理所有观点及其相互关系
    """

    def __init__(self):
        self.viewpoints: Dict[str, Viewpoint] = {}
        self.messages: List[Message] = []
        self._similarity_matrix: Optional[np.ndarray] = None
        self._distance_matrix: Optional[np.ndarray] = None

    def add_viewpoint(self, viewpoint: Viewpoint):
        """添加观点"""
        self.viewpoints[viewpoint.agent_id] = viewpoint
        # 清除缓存的矩阵
        self._similarity_matrix = None
        self._distance_matrix = None

    def add_message(self, message: Message):
        """添加消息"""
        self.messages.append(message)

    def get_viewpoint(self, agent_id: str) -> Optional[Viewpoint]:
        """获取特定Agent的观点"""
        return self.viewpoints.get(agent_id)

    def get_all_viewpoints(self) -> List[Viewpoint]:
        """获取所有观点"""
        return list(self.viewpoints.values())

    def get_recent_messages(self, limit: int = 10) -> List[Message]:
        """获取最近的消息"""
        return self.messages[-limit:] if self.messages else []

    def calculate_pairwise_similarities(self) -> np.ndarray:
        """
        计算所有观点之间的成对相似度矩阵

        Returns:
            相似度矩阵 (n x n)
        """
        if self._similarity_matrix is not None:
            return self._similarity_matrix

        viewpoints = self.get_all_viewpoints()
        n = len(viewpoints)
        self._similarity_matrix = np.zeros((n, n))

        for i, vp1 in enumerate(viewpoints):
            for j, vp2 in enumerate(viewpoints):
                self._similarity_matrix[i][j] = vp1.similarity_to(vp2)

        return self._similarity_matrix

    def calculate_pairwise_distances(self) -> np.ndarray:
        """
        计算所有观点之间的成对距离矩阵

        Returns:
            距离矩阵 (n x n)
        """
        if self._distance_matrix is not None:
            return self._distance_matrix

        similarities = self.calculate_pairwise_similarities()
        self._distance_matrix = 1.0 - similarities
        return self._distance_matrix

    def get_clustering_info(self) -> Dict:
        """
        获取聚类信息

        Returns:
            包含聚类统计信息的字典
        """
        distance_matrix = self.calculate_pairwise_distances()
        n = distance_matrix.shape[0]

        # 计算平均距离
        avg_distance = np.sum(distance_matrix) / (n * (n - 1)) if n > 1 else 0

        # 计算最大距离
        max_distance = np.max(distance_matrix) if n > 0 else 0

        # 计算最小距离
        min_distance = np.min(distance_matrix[distance_matrix > 0]) if np.any(distance_matrix > 0) else 0

        # 简单的聚类：基于距离阈值
        threshold = avg_distance * 0.5
        clusters = []
        assigned = set()

        for i, vp in enumerate(self.get_all_viewpoints()):
            if vp.agent_id in assigned:
                continue
            # 找到所有距离小于阈值的观点
            cluster = [vp.agent_id]
            for j, other_vp in enumerate(self.get_all_viewpoints()):
                if i != j and distance_matrix[i][j] < threshold:
                    cluster.append(other_vp.agent_id)
                    assigned.add(other_vp.agent_id)
            clusters.append(cluster)

        return {
            "num_clusters": len(clusters),
            "clusters": clusters,
            "avg_distance": float(avg_distance),
            "max_distance": float(max_distance),
            "min_distance": float(min_distance)
        }

    def get_diversity(self) -> float:
        """
        计算观点空间的多样性（基于Shannon熵）

        Returns:
            多样性值 0-1
        """
        if len(self.viewpoints) < 2:
            return 0.0

        # 使用成对距离的分布计算熵
        distances = self.calculate_pairwise_distances()
        # 获取上三角（不包括对角线）
        upper_tri = distances[np.triu_indices_from(distances, k=1)]

        if len(upper_tri) == 0:
            return 0.0

        # 计算距离的分布
        hist, _ = np.histogram(upper_tri, bins=10, range=(0, 1))
        prob = hist / len(upper_tri)
        prob = prob[prob > 0]  # 移除零概率

        # Shannon熵
        entropy = -np.sum(prob * np.log2(prob))

        # 归一化到0-1
        max_entropy = np.log2(10)  # 最多10个bin
        return entropy / max_entropy

    def get_consensus(self) -> float:
        """
        计算观点空间的共识度

        Returns:
            共识度值 0-1
        """
        if len(self.viewpoints) < 2:
            return 1.0

        similarities = self.calculate_pairwise_similarities()
        # 获取上三角（不包括对角线）
        upper_tri = similarities[np.triu_indices_from(similarities, k=1)]

        if len(upper_tri) == 0:
            return 1.0

        # 平均相似度作为共识度
        return float(np.mean(upper_tri))

    def get_polarization(self) -> float:
        """
        计算观点极化程度

        极化是指观点分裂成对立阵营的程度

        Returns:
            极化度值 0-1
        """
        clustering_info = self.get_clustering_info()
        num_clusters = clustering_info["num_clusters"]

        if num_clusters <= 1:
            return 0.0

        # 极化度与聚类数成正比，但需要考虑聚类大小
        n = len(self.viewpoints)
        max_polarization = min(num_clusters / n, 1.0)

        # 计算聚类间距离
        clusters = clustering_info["clusters"]
        if len(clusters) < 2:
            return 0.0

        inter_cluster_distances = []
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # 计算两个聚类之间的平均距离
                for agent1 in clusters[i]:
                    for agent2 in clusters[j]:
                        vp1 = self.get_viewpoint(agent1)
                        vp2 = self.get_viewpoint(agent2)
                        if vp1 and vp2:
                            inter_cluster_distances.append(vp1.distance_to(vp2))

        if not inter_cluster_distances:
            return max_polarization

        avg_inter_distance = np.mean(inter_cluster_distances)
        return float(avg_inter_distance * max_polarization)

    def get_connectivity(self) -> float:
        """
        计算观点空间的连接密度

        Returns:
            连接密度值 0-1
        """
        if len(self.viewpoints) < 2:
            return 0.0

        similarities = self.calculate_pairwise_similarities()
        threshold = 0.5  # 相似度阈值

        # 计算高于阈值的连接数
        n = similarities.shape[0]
        total_possible = n * (n - 1) / 2
        actual_connections = np.sum(similarities > threshold) / 2  # 除以2因为矩阵对称

        return actual_connections / total_possible if total_possible > 0 else 0.0

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "viewpoints": {k: v.to_dict() for k, v in self.viewpoints.items()},
            "messages": [m.to_dict() for m in self.messages],
            "diversity": self.get_diversity(),
            "consensus": self.get_consensus(),
            "polarization": self.get_polarization(),
            "connectivity": self.get_connectivity()
        }


# ============================================================
# DiscussionHistory - 讨论历史
# ============================================================

class DiscussionHistory:
    """
    讨论历史管理

    提供对讨论历史的访问和分析
    """

    def __init__(self):
        self.messages: List[Message] = []
        self.viewpoint_space = ViewpointSpace()

    def add_message(self, message: Message):
        """添加消息"""
        self.messages.append(message)
        self.viewpoint_space.add_message(message)

    def add_viewpoint(self, viewpoint: Viewpoint):
        """添加观点"""
        self.viewpoint_space.add_viewpoint(viewpoint)

    def get_recent(self, limit: int = 10) -> List[Message]:
        """获取最近的消息"""
        return self.messages[-limit:] if self.messages else []

    def get_by_agent(self, agent_id: str) -> List[Message]:
        """获取特定Agent的消息"""
        return [m for m in self.messages if m.agent_id == agent_id]

    def get_by_round(self, round_num: int) -> List[Message]:
        """获取特定轮次的消息"""
        return [m for m in self.messages if m.round_num == round_num]

    def get_by_type(self, message_type: MessageType) -> List[Message]:
        """获取特定类型的消息"""
        return [m for m in self.messages if m.message_type == message_type]

    def get_thread(self, message_id: str) -> List[Message]:
        """获取消息线程（包含所有引用的消息）"""
        thread = []
        target = None

        # 找到目标消息
        for msg in self.messages:
            if msg.message_id == message_id:
                target = msg
                break

        if target is None:
            return []

        # 递归查找引用
        def collect_references(msg: Message, collected: List[Message]):
            for ref_id in msg.references:
                for ref_msg in self.messages:
                    if ref_msg.message_id == ref_id:
                        collect_references(ref_msg, collected)
                        collected.append(ref_msg)
            collected.append(msg)

        collect_references(target, thread)
        return thread

    def get_emergence_moments(self, keywords: List[str] = None) -> List[Message]:
        """
        获取涌现时刻（包含涌现关键词的消息）

        Args:
            keywords: 涌现关键词列表，默认使用内置列表

        Returns:
            包含涌现关键词的消息列表
        """
        if keywords is None:
            keywords = [
                "新想法", "突然想到", "更好的方案", "结合",
                "创新", "改进", "优化", "综合", "突破",
                "换个角度", "重新考虑", "发现", "启发",
                "insight", "breakthrough", "novel", "innovative",
                "realize", "aha", "epiphany"
            ]

        emergence_moments = []
        for msg in self.messages:
            content_lower = msg.content.lower()
            if any(keyword.lower() in content_lower for keyword in keywords):
                emergence_moments.append(msg)

        return emergence_moments

    def get_statistics(self) -> Dict:
        """获取讨论统计信息"""
        if not self.messages:
            return {
                "total_messages": 0,
                "agents_count": 0,
                "rounds_count": 0,
                "avg_message_length": 0,
                "type_distribution": {},
                "agent_activity": {}
            }

        agents = set(m.agent_id for m in self.messages)
        rounds = set(m.round_num for m in self.messages)

        # 消息类型分布
        type_dist = {}
        for msg in self.messages:
            msg_type = msg.message_type.value
            type_dist[msg_type] = type_dist.get(msg_type, 0) + 1

        # Agent活跃度
        agent_activity = {}
        for agent in agents:
            agent_activity[agent] = len([m for m in self.messages if m.agent_id == agent])

        # 平均消息长度
        avg_length = np.mean([len(m.content) for m in self.messages])

        return {
            "total_messages": len(self.messages),
            "agents_count": len(agents),
            "rounds_count": len(rounds),
            "avg_message_length": float(avg_length),
            "type_distribution": type_dist,
            "agent_activity": agent_activity,
            "emergence_moments": len(self.get_emergence_moments())
        }

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "messages": [m.to_dict() for m in self.messages],
            "viewpoint_space": self.viewpoint_space.to_dict(),
            "statistics": self.get_statistics()
        }


# ============================================================
# 辅助函数
# ============================================================

def create_viewpoint(
    agent_id: str,
    content: str,
    confidence: float = 0.5,
    phase: str = "discuss"
) -> Viewpoint:
    """创建Viewpoint实例"""
    viewpoint = Viewpoint(
        agent_id=agent_id,
        content=content,
        confidence=confidence,
        phase=phase
    )
    # 自动提取组件
    viewpoint.extract_propositions()
    viewpoint.extract_evidences()
    viewpoint.extract_constraints()
    viewpoint.extract_suggestions()
    return viewpoint


def create_message(
    agent_id: str,
    content: str,
    message_type: MessageType,
    round_num: int = 0,
    references: List[str] = None
) -> Message:
    """创建Message实例"""
    import uuid
    return Message(
        message_id=str(uuid.uuid4()),
        agent_id=agent_id,
        content=content,
        message_type=message_type,
        round_num=round_num,
        references=references or []
    )


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    计算两段文本的相似度

    Args:
        text1: 第一段文本
        text2: 第二段文本

    Returns:
        相似度值 0-1
    """
    # 使用简单的词袋模型
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0
