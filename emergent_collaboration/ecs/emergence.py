"""
ECS - 涌现检测模块

基于信息论、观点动力学和社会选择理论的涌现检测系统
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from scipy.stats import entropy
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json

from .viewpoint import Viewpoint, ViewpointSpace, Message


class EmergenceType(Enum):
    """涌现类型"""
    AGGREGATION = "aggregation"      # 聚合涌现：简单观点聚合
    COORDINATION = "coordination"    # 协调涌现：角色分工协作
    SYNERGY = "synergy"              # 协同涌现：深度观点整合
    INNOVATION = "innovation"        # 创新涌现：突破性洞察
    META_EMERGENCE = "meta_emergence" # 元涌现：范式转移


class SystemPhase(Enum):
    """系统阶段"""
    EXPLORATION = "exploration"       # 探索阶段：观点发散
    DEBATE = "debate"                # 辩论阶段：观点碰撞
    CONVERGENCE = "convergence"      # 收敛阶段：寻求共识
    CONSENSUS = "consensus"          # 共识阶段：达成一致
    STAGNATION = "stagnation"        # 停滞阶段：无进展


@dataclass
class EmergenceMetrics:
    """涌现指标"""
    # 多样性指标
    diversity: float = 0.0            # 观点多样性（Shannon熵）
    dispersion: float = 0.0          # 观点离散度
    polarization: float = 0.0         # 观点极化程度
    cluster_count: int = 0           # 观点簇数量

    # 整合指标
    integration: float = 0.0         # 观点整合度
    connectivity: float = 0.0        # 连接密度
    citation_density: float = 0.0    # 引用密度

    # 共识指标
    consensus: float = 0.0           # 共识水平
    convergence_rate: float = 0.0    # 收敛速率
    agreement_ratio: float = 0.0     # 同意比例

    # 创新指标
    novelty: float = 0.0             # 新颖度
    breakthrough: float = 0.0         # 突破性得分
    paradigm_shift: float = 0.0      # 范式转移程度

    # 综合指标
    emergence_score: float = 0.0     # 综合涌现得分
    synergy_score: float = 0.0       # 协同得分
    collective_intelligence: float = 0.0  # 集体智能

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'diversity': self.diversity,
            'dispersion': self.dispersion,
            'polarization': self.polarization,
            'cluster_count': self.cluster_count,
            'integration': self.integration,
            'connectivity': self.connectivity,
            'citation_density': self.citation_density,
            'consensus': self.consensus,
            'convergence_rate': self.convergence_rate,
            'agreement_ratio': self.agreement_ratio,
            'novelty': self.novelty,
            'breakthrough': self.breakthrough,
            'paradigm_shift': self.paradigm_shift,
            'emergence_score': self.emergence_score,
            'synergy_score': self.synergy_score,
            'collective_intelligence': self.collective_intelligence
        }


@dataclass
class EmergenceReport:
    """涌现检测报告"""
    emergence_type: EmergenceType
    system_phase: SystemPhase
    metrics: EmergenceMetrics

    # 详细分析
    diversity_analysis: Dict[str, Any] = None
    consensus_analysis: Dict[str, Any] = None
    innovation_analysis: Dict[str, Any] = None
    network_analysis: Dict[str, Any] = None

    # 时间信息
    timestamp: str = ""
    round_num: int = 0

    # 建议
    recommendations: List[str] = None

    def __post_init__(self):
        if self.diversity_analysis is None:
            self.diversity_analysis = {}
        if self.consensus_analysis is None:
            self.consensus_analysis = {}
        if self.innovation_analysis is None:
            self.innovation_analysis = {}
        if self.network_analysis is None:
            self.network_analysis = {}
        if self.recommendations is None:
            self.recommendations = []

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'emergence_type': self.emergence_type.value,
            'system_phase': self.system_phase.value,
            'metrics': self.metrics.to_dict(),
            'diversity_analysis': self.diversity_analysis,
            'consensus_analysis': self.consensus_analysis,
            'innovation_analysis': self.innovation_analysis,
            'network_analysis': self.network_analysis,
            'timestamp': self.timestamp,
            'round_num': self.round_num,
            'recommendations': self.recommendations
        }

    def to_json(self) -> str:
        """转换为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class EmergenceDetector:
    """涌现检测器

    基于信息论、观点动力学和社会选择理论的多维度涌现检测
    """

    def __init__(self,
                 diversity_threshold: float = 0.5,
                 consensus_threshold: float = 0.7,
                 novelty_threshold: float = 0.6):
        """
        初始化涌现检测器

        Args:
            diversity_threshold: 多样性阈值
            consensus_threshold: 共识阈值
            novelty_threshold: 新颖度阈值
        """
        self.diversity_threshold = diversity_threshold
        self.consensus_threshold = consensus_threshold
        self.novelty_threshold = novelty_threshold

        # 历史追踪
        self.history = []
        self.initial_viewpoints = None
        self.previous_metrics = None

    def detect(self,
              viewpoint_space: ViewpointSpace,
              round_num: int = 0) -> EmergenceReport:
        """
        执行完整的涌现检测

        Args:
            viewpoint_space: 观点空间
            round_num: 当前轮次

        Returns:
            涌现检测报告
        """
        # 获取当前所有观点
        current_viewpoints = viewpoint_space.get_all_viewpoints()

        # 如果是初始轮次，保存初始观点
        if round_num == 0:
            self.initial_viewpoints = current_viewpoints

        # 计算各类指标
        metrics = self._calculate_all_metrics(viewpoint_space, current_viewpoints)

        # 检测涌现类型
        emergence_type = self._classify_emergence(metrics)

        # 检测系统阶段
        system_phase = self._classify_phase(metrics, round_num)

        # 详细分析
        diversity_analysis = self._analyze_diversity(current_viewpoints)
        consensus_analysis = self._analyze_consensus(viewpoint_space, current_viewpoints)
        innovation_analysis = self._analyze_innovation(current_viewpoints)
        network_analysis = self._analyze_network(viewpoint_space)

        # 生成建议
        recommendations = self._generate_recommendations(
            emergence_type, system_phase, metrics
        )

        # 创建报告
        report = EmergenceReport(
            emergence_type=emergence_type,
            system_phase=system_phase,
            metrics=metrics,
            diversity_analysis=diversity_analysis,
            consensus_analysis=consensus_analysis,
            innovation_analysis=innovation_analysis,
            network_analysis=network_analysis,
            round_num=round_num,
            recommendations=recommendations
        )

        # 保存到历史
        self.history.append(report)
        self.previous_metrics = metrics

        return report

    def _calculate_all_metrics(self,
                               viewpoint_space: ViewpointSpace,
                               current_viewpoints: List[Viewpoint]) -> EmergenceMetrics:
        """计算所有指标"""
        if not current_viewpoints:
            return EmergenceMetrics()

        # 多样性指标
        diversity = self._calculate_diversity(current_viewpoints)
        dispersion = self._calculate_dispersion(current_viewpoints)
        polarization = self._calculate_polarization(current_viewpoints)
        cluster_count = self._calculate_cluster_count(current_viewpoints)

        # 整合指标
        integration = self._calculate_integration(viewpoint_space)
        connectivity = self._calculate_connectivity(viewpoint_space)
        citation_density = self._calculate_citation_density(viewpoint_space)

        # 共识指标
        consensus = self._calculate_consensus(current_viewpoints)
        convergence_rate = self._calculate_convergence_rate(current_viewpoints)
        agreement_ratio = self._calculate_agreement_ratio(current_viewpoints)

        # 创新指标
        novelty = self._calculate_novelty(current_viewpoints)
        breakthrough = self._calculate_breakthrough(current_viewpoints)
        paradigm_shift = self._calculate_paradigm_shift(current_viewpoints)

        # 综合指标
        emergence_score = self._calculate_emergence_score(
            diversity, consensus, novelty
        )
        synergy_score = self._calculate_synergy_score(
            diversity, integration, novelty
        )
        collective_intelligence = self._calculate_collective_intelligence(
            consensus, integration, innovation_score=breakthrough
        )

        return EmergenceMetrics(
            diversity=diversity,
            dispersion=dispersion,
            polarization=polarization,
            cluster_count=cluster_count,
            integration=integration,
            connectivity=connectivity,
            citation_density=citation_density,
            consensus=consensus,
            convergence_rate=convergence_rate,
            agreement_ratio=agreement_ratio,
            novelty=novelty,
            breakthrough=breakthrough,
            paradigm_shift=paradigm_shift,
            emergence_score=emergence_score,
            synergy_score=synergy_score,
            collective_intelligence=collective_intelligence
        )

    # === 多样性指标 ===

    def _calculate_diversity(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算观点多样性（Shannon熵）

        基于观点向量的分布计算熵值
        """
        if len(viewpoints) < 2:
            return 0.0

        # 获取所有观点向量
        vectors = np.array([vp.get_vector_representation() for vp in viewpoints])

        # 对每个维度计算熵
        entropies = []
        for dim in range(vectors.shape[1]):
            values = vectors[:, dim]

            # 离散化到bin
            bins = min(10, len(values))
            hist, _ = np.histogram(values, bins=bins, density=True)

            # 移除零值
            hist = hist[hist > 0]
            if len(hist) > 0:
                ent = entropy(hist)
                entropies.append(ent)

        # 平均熵（归一化）
        if entropies:
            max_entropy = np.log(min(10, len(viewpoints)))
            avg_entropy = np.mean(entropies)
            return min(avg_entropy / max_entropy, 1.0) if max_entropy > 0 else 0.0

        return 0.0

    def _calculate_dispersion(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算观点离散度（平均成对距离）

        值越高表示观点越分散
        """
        if len(viewpoints) < 2:
            return 0.0

        # 计算成对距离
        distances = []
        for i, vp1 in enumerate(viewpoints):
            for j, vp2 in enumerate(viewpoints):
                if i < j:
                    distances.append(vp1.distance_to(vp2))

        if distances:
            return float(np.mean(distances))
        return 0.0

    def _calculate_polarization(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算观点极化程度

        检测是否存在两极分化
        """
        if len(viewpoints) < 3:
            return 0.0

        # 使用K-means聚类（k=2）
        vectors = np.array([vp.get_vector_representation() for vp in viewpoints])

        try:
            kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
            labels = kmeans.fit_predict(vectors)

            # 计算簇间距离与簇内距离的比值
            if len(set(labels)) < 2:
                return 0.0

            # 簇中心
            centers = kmeans.cluster_centers_

            # 簇间距离
            inter_cluster_dist = np.linalg.norm(centers[0] - centers[1])

            # 簇内距离
            intra_cluster_dists = []
            for label in set(labels):
                cluster_vectors = vectors[labels == label]
                if len(cluster_vectors) > 1:
                    intra_dist = np.mean(pdist(cluster_vectors))
                    intra_cluster_dists.append(intra_dist)

            if intra_cluster_dists:
                avg_intra = np.mean(intra_cluster_dists)
                # 极化度 = 簇间 / 簇内
                if avg_intra > 0:
                    return min(inter_cluster_dist / avg_intra, 1.0)

        except Exception:
            pass

        return 0.0

    def _calculate_cluster_count(self, viewpoints: List[Viewpoint]) -> int:
        """
        计算观点簇数量

        使用轮廓系数确定最优聚类数
        """
        if len(viewpoints) < 3:
            return len(viewpoints)

        vectors = np.array([vp.get_vector_representation() for vp in viewpoints])

        best_score = -1
        best_n = 1

        # 尝试2到min(6, n_viewpoints)个簇
        max_clusters = min(6, len(viewpoints))
        for n in range(2, max_clusters + 1):
            try:
                kmeans = KMeans(n_clusters=n, random_state=42, n_init=10)
                labels = kmeans.fit_predict(vectors)

                if len(set(labels)) < 2:
                    continue

                score = silhouette_score(vectors, labels)
                if score > best_score:
                    best_score = score
                    best_n = n
            except Exception:
                continue

        return best_n

    # === 整合指标 ===

    def _calculate_integration(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算观点整合度

        基于消息引用关系
        """
        messages = viewpoint_space.message_history
        if not messages:
            return 0.0

        # 计算有引用的消息比例
        referenced_count = sum(
            1 for msg in messages
            if msg.references and len(msg.references) > 0
        )

        return referenced_count / len(messages)

    def _calculate_connectivity(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算连接密度

        Agent之间的交互连接密度
        """
        messages = viewpoint_space.message_history
        if not messages:
            return 0.0

        # 统计交互对
        interactions = set()
        for msg in messages:
            if msg.reply_to:
                interactions.add(tuple(sorted([msg.agent_id, msg.reply_to])))
            for ref in msg.references:
                interactions.add(tuple(sorted([msg.agent_id, ref])))

        n_agents = len(viewpoint_space.viewpoints)
        if n_agents < 2:
            return 0.0

        # 可能的最大连接数
        max_connections = n_agents * (n_agents - 1) / 2

        if max_connections > 0:
            return len(interactions) / max_connections
        return 0.0

    def _calculate_citation_density(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算引用密度

        每个观点被引用的平均次数
        """
        messages = viewpoint_space.message_history
        if not messages:
            return 0.0

        # 统计每个观点被引用的次数
        citation_counts = {}
        for msg in messages:
            for ref in msg.references:
                citation_counts[ref] = citation_counts.get(ref, 0) + 1

        if citation_counts:
            return float(np.mean(list(citation_counts.values())))
        return 0.0

    # === 共识指标 ===

    def _calculate_consensus(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算共识水平

        基于观点相似度的一致性程度
        """
        if len(viewpoints) < 2:
            return 1.0

        # 计算成对相似度
        similarities = []
        for i, vp1 in enumerate(viewpoints):
            for j, vp2 in enumerate(viewpoints):
                if i < j:
                    similarities.append(vp1.similarity_to(vp2))

        if similarities:
            # 共识 = 平均相似度
            return float(np.mean(similarities))
        return 0.0

    def _calculate_convergence_rate(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算收敛速率

        基于观点方差的衰减
        """
        if len(viewpoints) < 2 or not self.previous_metrics:
            return 0.0

        # 与之前的多样性比较
        current_diversity = self._calculate_diversity(viewpoints)
        previous_diversity = self.previous_metrics.diversity

        if previous_diversity > 0:
            # 收敛速率 = 多样性减少的比例
            rate = (previous_diversity - current_diversity) / previous_diversity
            return max(0.0, rate)
        return 0.0

    def _calculate_agreement_ratio(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算同意比例

        相似度超过阈值的观点对比例
        """
        if len(viewpoints) < 2:
            return 1.0

        threshold = 0.7  # 相似度阈值
        agreement_count = 0
        total_pairs = 0

        for i, vp1 in enumerate(viewpoints):
            for j, vp2 in enumerate(viewpoints):
                if i < j:
                    total_pairs += 1
                    if vp1.similarity_to(vp2) > threshold:
                        agreement_count += 1

        if total_pairs > 0:
            return agreement_count / total_pairs
        return 0.0

    # === 创新指标 ===

    def _calculate_novelty(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算新颖度

        与初始观点的平均距离
        """
        if not self.initial_viewpoints or not viewpoints:
            return 0.0

        # 计算当前观点与初始观点的平均距离
        distances = []
        for current_vp in viewpoints:
            min_dist = float('inf')
            for initial_vp in self.initial_viewpoints:
                dist = current_vp.distance_to(initial_vp)
                if dist < min_dist:
                    min_dist = dist
            distances.append(min_dist)

        if distances:
            return float(np.mean(distances))
        return 0.0

    def _calculate_breakthrough(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算突破性得分

        结合新颖度和质量
        """
        if not viewpoints:
            return 0.0

        # 新颖度
        novelty = self._calculate_novelty(viewpoints)

        # 平均置信度
        avg_confidence = np.mean([vp.confidence for vp in viewpoints])

        # 综合得分
        return (novelty * 0.6 + avg_confidence * 0.4)

    def _calculate_paradigm_shift(self, viewpoints: List[Viewpoint]) -> float:
        """
        计算范式转移程度

        检测是否创造了新的概念簇
        """
        if not self.initial_viewpoints or len(viewpoints) < 3:
            return 0.0

        # 对初始观点聚类
        initial_vectors = np.array([
            vp.get_vector_representation() for vp in self.initial_viewpoints
        ])
        current_vectors = np.array([
            vp.get_vector_representation() for vp in viewpoints
        ])

        # 确定维度一致
        min_dim = min(initial_vectors.shape[1], current_vectors.shape[1])
        initial_vectors = initial_vectors[:, :min_dim]
        current_vectors = current_vectors[:, :min_dim]

        try:
            # 初始聚类
            kmeans_init = KMeans(n_clusters=2, random_state=42)
            init_labels = kmeans_init.fit_predict(initial_vectors)

            # 检查当前观点是否形成新簇
            kmeans_current = KMeans(n_clusters=3, random_state=42)
            current_labels = kmeans_current.fit_predict(current_vectors)

            # 如果有新的簇出现，说明有范式转移
            n_unique_clusters = len(set(current_labels))

            # 范式转移得分
            shift_score = min((n_unique_clusters - 2) / 3.0, 1.0)
            return shift_score

        except Exception:
            pass

        return 0.0

    # === 综合指标 ===

    def _calculate_emergence_score(self,
                                  diversity: float,
                                  consensus: float,
                                  novelty: float) -> float:
        """
        计算综合涌现得分

        权重：多样性0.3 + 共识0.3 + 新颖度0.4
        """
        return (diversity * 0.3 + consensus * 0.3 + novelty * 0.4)

    def _calculate_synergy_score(self,
                                diversity: float,
                                integration: float,
                                novelty: float) -> float:
        """
        计算协同得分

        协同 = 多样性 × 整合度 × 新颖性
        """
        return (diversity * integration * novelty) ** (1/3)

    def _calculate_collective_intelligence(self,
                                          consensus: float,
                                          integration: float,
                                          innovation_score: float) -> float:
        """
        计算集体智能

        集体智能 = 共识 × 整合 × 创新
        """
        return (consensus * integration * innovation_score) ** (1/3)

    # === 分类方法 ===

    def _classify_emergence(self, metrics: EmergenceMetrics) -> EmergenceType:
        """
        分类涌现类型

        基于多维指标判断涌现类型
        """
        div = metrics.diversity
        cons = metrics.consensus
        nov = metrics.novelty
        integ = metrics.integration

        # 判断阈值
        low_threshold = 0.3
        medium_threshold = 0.5
        high_threshold = 0.7

        # 元涌现：所有指标都很高
        if (div > high_threshold and
            cons > high_threshold and
            nov > high_threshold and
            integ > high_threshold):
            return EmergenceType.META_EMERGENCE

        # 创新涌现：高新颖度
        if nov > high_threshold and div > medium_threshold:
            return EmergenceType.INNOVATION

        # 协同涌现：高整合度和多样性
        if integ > high_threshold and div > medium_threshold:
            return EmergenceType.SYNERGY

        # 协调涌现：中等整合度
        if integ > medium_threshold and cons > medium_threshold:
            return EmergenceType.COORDINATION

        # 聚合涌现：低整合度
        if integ < low_threshold:
            return EmergenceType.AGGREGATION

        # 默认为协调涌现
        return EmergenceType.COORDINATION

    def _classify_phase(self, metrics: EmergenceMetrics, round_num: int) -> SystemPhase:
        """
        分类系统阶段

        基于多样性和共识判断当前阶段
        """
        div = metrics.diversity
        cons = metrics.consensus

        # 停滞：多样性和共识都很低
        if div < 0.3 and cons < 0.3:
            return SystemPhase.STAGNATION

        # 共识：高共识
        if cons > 0.8:
            return SystemPhase.CONSENSUS

        # 收敛：共识增加
        if self.previous_metrics and cons > self.previous_metrics.consensus:
            return SystemPhase.CONVERGENCE

        # 辩论：中等多样性和共识
        if 0.4 < div < 0.7 and 0.4 < cons < 0.7:
            return SystemPhase.DEBATE

        # 探索：高多样性
        if div > 0.6:
            return SystemPhase.EXPLORATION

        # 默认为探索
        return SystemPhase.EXPLORATION

    # === 详细分析 ===

    def _analyze_diversity(self, viewpoints: List[Viewpoint]) -> Dict[str, Any]:
        """详细多样性分析"""
        if not viewpoints:
            return {}

        return {
            'viewpoint_count': len(viewpoints),
            'unique_propositions': sum(len(vp.propositions) for vp in viewpoints),
            'avg_confidence': np.mean([vp.confidence for vp in viewpoints]),
            'sentiment_range': [
                min(vp.sentiment for vp in viewpoints),
                max(vp.sentiment for vp in viewpoints)
            ],
            'most_divergent_pair': self._find_most_divergent_pair(viewpoints)
        }

    def _analyze_consensus(self,
                          viewpoint_space: ViewpointSpace,
                          viewpoints: List[Viewpoint]) -> Dict[str, Any]:
        """详细共识分析"""
        return {
            'agreement_ratio': self._calculate_agreement_ratio(viewpoints),
            'consensus_trend': self._get_consensus_trend(),
            'key_agreements': self._extract_key_agreements(viewpoints),
            'remaining_disagreements': self._extract_disagreements(viewpoints)
        }

    def _analyze_innovation(self, viewpoints: List[Viewpoint]) -> Dict[str, Any]:
        """详细创新分析"""
        return {
            'novelty_level': 'high' if self._calculate_novelty(viewpoints) > 0.6 else 'medium' if self._calculate_novelty(viewpoints) > 0.3 else 'low',
            'breakthrough_potential': self._calculate_breakthrough(viewpoints),
            'new_concepts': self._extract_new_concepts(viewpoints),
            'creative_sparks': self._identify_creative_sparks(viewpoints)
        }

    def _analyze_network(self, viewpoint_space: ViewpointSpace) -> Dict[str, Any]:
        """详细网络分析"""
        messages = viewpoint_space.message_history

        # 构建交互网络
        interaction_matrix = self._build_interaction_matrix(messages)

        return {
            'total_interactions': len(messages),
            'most_active_agent': self._find_most_active_agent(messages),
            'network_density': self._calculate_network_density(interaction_matrix),
            'clustering_coefficient': self._calculate_clustering_coefficient(interaction_matrix)
        }

    # === 辅助方法 ===

    def _find_most_divergent_pair(self, viewpoints: List[Viewpoint]) -> Tuple[str, str]:
        """找出最分歧的观点对"""
        max_dist = 0
        pair = (None, None)

        for i, vp1 in enumerate(viewpoints):
            for j, vp2 in enumerate(viewpoints):
                if i < j:
                    dist = vp1.distance_to(vp2)
                    if dist > max_dist:
                        max_dist = dist
                        pair = (vp1.agent_id, vp2.agent_id)

        return pair

    def _get_consensus_trend(self) -> str:
        """获取共识趋势"""
        if len(self.history) < 2:
            return "unknown"

        recent = self.history[-1].metrics.consensus
        previous = self.history[-2].metrics.consensus

        if recent > previous + 0.1:
            return "increasing"
        elif recent < previous - 0.1:
            return "decreasing"
        else:
            return "stable"

    def _extract_key_agreements(self, viewpoints: List[Viewpoint]) -> List[str]:
        """提取关键共识点"""
        # 简化版：基于关键词匹配
        agreements = []

        # 收集所有主张
        all_props = []
        for vp in viewpoints:
            all_props.extend(vp.propositions)

        # 查找相似主张（简化版：关键词重叠）
        for i, prop1 in enumerate(all_props):
            matching_count = 0
            for j, prop2 in enumerate(all_props):
                if i != j:
                    words1 = set(prop1.split())
                    words2 = set(prop2.split())
                    overlap = len(words1 & words2) / max(len(words1 | words2), 1)
                    if overlap > 0.5:
                        matching_count += 1

            if matching_count >= len(all_props) / 2:
                agreements.append(prop1[:100])

        return agreements[:5]

    def _extract_disagreements(self, viewpoints: List[Viewpoint]) -> List[str]:
        """提取分歧点"""
        # 简化版：返回约束条件
        disagreements = []
        for vp in viewpoints:
            for constraint in vp.constraints[:3]:
                disagreements.append(f"{vp.agent_id}: {constraint[:100]}")
        return disagreements

    def _extract_new_concepts(self, viewpoints: List[Viewpoint]) -> List[str]:
        """提取新概念"""
        # 简化版：返回建议
        concepts = []
        for vp in viewpoints:
            for suggestion in vp.suggestions[:3]:
                concepts.append(suggestion[:100])
        return concepts

    def _identify_creative_sparks(self, viewpoints: List[Viewpoint]) -> List[str]:
        """识别创意火花"""
        sparks = []

        for vp in viewpoints:
            if vp.confidence > 0.7 and vp.novelty > 0.6:
                for prop in vp.propositions[:2]:
                    sparks.append(f"{vp.agent_id}: {prop[:100]}")

        return sparks

    def _build_interaction_matrix(self, messages: List[Message]) -> np.ndarray:
        """构建交互矩阵"""
        agent_ids = set(msg.agent_id for msg in messages)
        agent_ids.update(msg.reply_to for msg in messages if msg.reply_to)
        agent_ids.update(ref for msg in messages for ref in msg.references)

        agent_list = list(agent_ids)
        n = len(agent_list)
        matrix = np.zeros((n, n))

        for msg in messages:
            if msg.agent_id in agent_list:
                i = agent_list.index(msg.agent_id)

                if msg.reply_to and msg.reply_to in agent_list:
                    j = agent_list.index(msg.reply_to)
                    matrix[i][j] += 1

                for ref in msg.references:
                    if ref in agent_list:
                        j = agent_list.index(ref)
                        matrix[i][j] += 1

        return matrix

    def _find_most_active_agent(self, messages: List[Message]) -> str:
        """找出最活跃的Agent"""
        counts = {}
        for msg in messages:
            counts[msg.agent_id] = counts.get(msg.agent_id, 0) + 1

        if counts:
            return max(counts, key=counts.get)
        return "none"

    def _calculate_network_density(self, matrix: np.ndarray) -> float:
        """计算网络密度"""
        n = matrix.shape[0]
        if n < 2:
            return 0.0

        total_edges = np.sum(matrix > 0)
        max_edges = n * (n - 1)

        if max_edges > 0:
            return total_edges / max_edges
        return 0.0

    def _calculate_clustering_coefficient(self, matrix: np.ndarray) -> float:
        """计算聚类系数（简化版）"""
        try:
            import networkx as nx
            G = nx.from_numpy_array(matrix)
            return nx.average_clustering(G)
        except Exception:
            return 0.0

    def _generate_recommendations(self,
                                  emergence_type: EmergenceType,
                                  system_phase: SystemPhase,
                                  metrics: EmergenceMetrics) -> List[str]:
        """生成建议"""
        recommendations = []

        # 基于阶段建议
        if system_phase == SystemPhase.EXPLORATION:
            recommendations.append("当前处于探索阶段，鼓励更多观点发散")
            if metrics.diversity < 0.5:
                recommendations.append("多样性不足，建议引入更多不同视角")

        elif system_phase == SystemPhase.DEBATE:
            recommendations.append("当前处于辩论阶段，促进观点碰撞")
            recommendations.append("注意保持建设性的讨论氛围")

        elif system_phase == SystemPhase.CONVERGENCE:
            recommendations.append("当前处于收敛阶段，开始整合观点")
            if metrics.integration < 0.5:
                recommendations.append("整合度不足，建议加强观点连接")

        elif system_phase == SystemPhase.CONSENSUS:
            recommendations.append("已达成高度共识，可以开始方案细化")

        elif system_phase == SystemPhase.STAGNATION:
            recommendations.append("⚠️ 系统停滞，建议：")
            recommendations.append("1. 引入新的角色或视角")
            recommendations.append("2. 重新定义问题")
            recommendations.append("3. 调整讨论规则")

        # 基于涌现类型建议
        if emergence_type == EmergenceType.META_EMERGENCE:
            recommendations.append("✨ 已检测到元涌现！这是最高级别的集体智能")
        elif emergence_type == EmergenceType.INNOVATION:
            recommendations.append("💡 检测到创新涌现，记录突破性洞察")
        elif emergence_type == EmergenceType.SYNERGY:
            recommendations.append("🔗 检测到协同涌现，观点整合良好")

        return recommendations


# 辅助函数
def create_emergence_report_from_data(data: Dict[str, Any]) -> EmergenceReport:
    """从数据字典创建涌现报告"""
    metrics_data = data.get('metrics', {})
    metrics = EmergenceMetrics(
        diversity=metrics_data.get('diversity', 0.0),
        dispersion=metrics_data.get('dispersion', 0.0),
        polarization=metrics_data.get('polarization', 0.0),
        cluster_count=metrics_data.get('cluster_count', 0),
        integration=metrics_data.get('integration', 0.0),
        connectivity=metrics_data.get('connectivity', 0.0),
        citation_density=metrics_data.get('citation_density', 0.0),
        consensus=metrics_data.get('consensus', 0.0),
        convergence_rate=metrics_data.get('convergence_rate', 0.0),
        agreement_ratio=metrics_data.get('agreement_ratio', 0.0),
        novelty=metrics_data.get('novelty', 0.0),
        breakthrough=metrics_data.get('breakthrough', 0.0),
        paradigm_shift=metrics_data.get('paradigm_shift', 0.0),
        emergence_score=metrics_data.get('emergence_score', 0.0),
        synergy_score=metrics_data.get('synergy_score', 0.0),
        collective_intelligence=metrics_data.get('collective_intelligence', 0.0)
    )

    return EmergenceReport(
        emergence_type=EmergenceType(data.get('emergence_type', 'coordination')),
        system_phase=SystemPhase(data.get('system_phase', 'exploration')),
        metrics=metrics,
        diversity_analysis=data.get('diversity_analysis', {}),
        consensus_analysis=data.get('consensus_analysis', {}),
        innovation_analysis=data.get('innovation_analysis', {}),
        network_analysis=data.get('network_analysis', {}),
        timestamp=data.get('timestamp', ''),
        round_num=data.get('round_num', 0),
        recommendations=data.get('recommendations', [])
    )


__all__ = [
    'EmergenceType',
    'SystemPhase',
    'EmergenceMetrics',
    'EmergenceReport',
    'EmergenceDetector',
    'create_emergence_report_from_data',
]
