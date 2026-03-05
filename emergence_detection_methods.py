"""
多Agent系统涌现检测方法集合
================================

本模块实现了用于检测和量化多Agent系统中"真涌现"现象的计算指标和算法。

核心指标包括：
1. 观点多样性（Viewpoint Diversity）
2. 共识收敛程度（Consensus Level）
3. 创新突破检测（Innovation Detection）
4. 社会选择和投票算法
5. 观点动力学建模

作者：System Max Research Team
日期：2025
"""

import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import warnings

warnings.filterwarnings('ignore')

# 可选依赖
try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    nx = None

try:
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    PCA = None
    TSNE = None


# ============================================================================
# 1. 观点多样性（Viewpoint Diversity）量化方法
# ============================================================================

@dataclass
class DiversityMetrics:
    """多样性指标容器"""
    entropy: float  # 熵基多样性
    variance: float  # 方差基多样性
    dispersion: float  # 离散度
    polarization: float  # 极化程度
    cluster_count: int  # 观点聚类数量
    effective_diversity: float  # 有效多样性


class ViewpointDiversity:
    """
    观点多样性量化器

    理论基础：
    - Shannon熵：衡量观点分布的不确定性
    - Simpson指数：衡量观点的均匀性
    - 极化指数：衡量观点向两极发展的程度
    - 空间离散度：衡量观点在高维空间的分散程度
    """

    def __init__(self, viewpoint_dim: int = 1):
        """
        初始化多样性分析器

        Args:
            viewpoint_dim: 观点空间的维度（1为标量观点，>1为向量观点）
        """
        self.viewpoint_dim = viewpoint_dim

    def calculate_entropy_diversity(self, opinions: np.ndarray,
                                    bins: int = 50) -> float:
        """
        计算基于Shannon熵的多样性

        对于连续观点空间，先离散化再计算熵：
        H = -Σ p_i * log(p_i)

        Args:
            opinions: 形状为(n_agents,)或(n_agents, dim)的观点数组
            bins: 离散化的箱数

        Returns:
            归一化的熵值（0-1之间）
        """
        if opinions.ndim == 1:
            opinions = opinions.reshape(-1, 1)

        # 对每个维度分别计算熵
        entropies = []
        for d in range(opinions.shape[1]):
            hist, _ = np.histogram(opinions[:, d], bins=bins, density=False)
            # 归一化为概率分布
            hist = hist / np.sum(hist)
            # 避免零概率
            hist = hist[hist > 0]
            entropy = -np.sum(hist * np.log(hist))
            # 归一化：最大熵为log(bins)
            normalized_entropy = entropy / np.log(bins)
            entropies.append(normalized_entropy)

        return np.mean(entropies)

    def calculate_simpson_diversity(self, opinions: np.ndarray,
                                    bins: int = 50) -> float:
        """
        计算基于Simpson指数的多样性

        D = 1 - Σ p_i²
        其中p_i是第i个观点的概率

        Args:
            opinions: 观点数组
            bins: 离散化的箱数

        Returns:
            Simpson多样性指数（0-1之间）
        """
        if opinions.ndim == 1:
            opinions = opinions.reshape(-1, 1)

        simpson_indices = []
        for d in range(opinions.shape[1]):
            hist, _ = np.histogram(opinions[:, d], bins=bins, density=False)
            hist = hist / np.sum(hist)
            simpson = 1 - np.sum(hist ** 2)
            simpson_indices.append(simpson)

        return np.mean(simpson_indices)

    def calculate_polarization(self, opinions: np.ndarray) -> float:
        """
        计算观点极化程度

        极化定义为：
        P = Var[opinions] / (max_possible_variance)

        当观点集中在两端时极化度高，集中在中间时极化度低

        Args:
            opinions: 形状为(n_agents,)的观点数组（标量）

        Returns:
            极化程度（0-1之间）
        """
        if opinions.ndim > 1:
            # 对多维情况，取第一主成分
            pca = PCA(n_components=1)
            opinions_1d = pca.fit_transform(opinions).flatten()
        else:
            opinions_1d = opinions

        variance = np.var(opinions_1d)
        # 假设观点范围在[0,1]，最大方差为0.25
        max_variance = 0.25
        polarization = variance / max_variance

        return min(polarization, 1.0)

    def calculate_dispersion(self, opinions: np.ndarray) -> float:
        """
        计算观点在高维空间的离散度

        使用平均成对距离：
        D = (2/(n*(n-1))) * Σ||opinions[i] - opinions[j]||

        Args:
            opinions: 形状为(n_agents, dim)的观点数组

        Returns:
            归一化的离散度（0-1之间）
        """
        if opinions.ndim == 1:
            opinions = opinions.reshape(-1, 1)

        n = opinions.shape[0]
        if n < 2:
            return 0.0

        # 计算所有成对距离
        pairwise_distances = pdist(opinions, metric='euclidean')
        avg_distance = np.mean(pairwise_distances)

        # 归一化：假设每个维度的范围是[0,1]
        max_distance = np.sqrt(opinions.shape[1])
        normalized_dispersion = avg_distance / max_distance

        return min(normalized_dispersion, 1.0)

    def count_opinion_clusters(self, opinions: np.ndarray,
                               threshold: float = 0.1) -> int:
        """
        使用层次聚类识别观点簇的数量

        Args:
            opinions: 观点数组
            threshold: 聚类距离阈值

        Returns:
            观点簇的数量
        """
        if opinions.ndim == 1:
            opinions = opinions.reshape(-1, 1)

        n = opinions.shape[0]
        if n < 2:
            return 1

        # 计算距离矩阵
        distances = squareform(pdist(opinions, metric='euclidean'))

        # 层次聚类
        Z = linkage(distances, method='ward')

        # 根据阈值确定簇数
        max_distance = threshold * np.sqrt(opinions.shape[1])
        clusters = self._count_clusters_from_linkage(Z, max_distance)

        return clusters

    def _count_clusters_from_linkage(self, Z: np.ndarray,
                                     threshold: float) -> int:
        """从层次聚类结果中统计簇数"""
        n = len(Z) + 1
        clusters = n

        for row in Z:
            if row[2] > threshold:
                break
            clusters -= 1

        return max(clusters, 1)

    def calculate_effective_diversity(self, opinions: np.ndarray) -> float:
        """
        计算有效多样性（Effective Diversity）

        有效多样性定义为：
        D_eff = exp(H)
        其中H是Shannon熵

        这个指标衡量的是"有效"的不同观点数量

        Args:
            opinions: 观点数组

        Returns:
            有效多样性
        """
        entropy = self.calculate_entropy_diversity(opinions)
        # 使用以2为底的指数，使得最大值为bins数
        bins = 50
        effective_diversity = np.exp(entropy * np.log(bins))

        # 归一化到[0,1]
        return min(effective_diversity / bins, 1.0)

    def compute_all_metrics(self, opinions: np.ndarray) -> DiversityMetrics:
        """
        计算所有多样性指标

        Args:
            opinions: 观点数组，形状为(n_agents,)或(n_agents, dim)

        Returns:
            DiversityMetrics对象，包含所有多样性指标
        """
        return DiversityMetrics(
            entropy=self.calculate_entropy_diversity(opinions),
            variance=self.calculate_simpson_diversity(opinions),
            dispersion=self.calculate_dispersion(opinions),
            polarization=self.calculate_polarization(opinions),
            cluster_count=self.count_opinion_clusters(opinions),
            effective_diversity=self.calculate_effective_diversity(opinions)
        )


# ============================================================================
# 2. 共识收敛程度（Consensus Level）计算
# ============================================================================

@dataclass
class ConsensusMetrics:
    """共识指标容器"""
    consensus_level: float  # 总体共识水平
    convergence_rate: float  # 收敛速率
    agreement_ratio: float  # 同意比例
    cluster_separation: float  # 簇间分离度
    stability_index: float  # 稳定性指数


class ConsensusAnalyzer:
    """
    共识收敛分析器

    理论基础：
    - 标准差：衡量观点偏离均值的程度
    - 收敛速率：观点趋于一致的速度
    - 同意阈值：在可接受误差范围内达成一致的agent比例
    - 稳定性：共识状态的持续性
    """

    def __init__(self, agreement_threshold: float = 0.1):
        """
        初始化共识分析器

        Args:
            agreement_threshold: 判断达成共识的误差阈值
        """
        self.agreement_threshold = agreement_threshold

    def calculate_consensus_level(self, opinions: np.ndarray) -> float:
        """
        计算共识水平

        共识水平定义为：
        C = 1 - (std(opinions) / max_possible_std)

        完全共识时C=1，完全分散时C=0

        Args:
            opinions: 观点数组

        Returns:
            共识水平（0-1之间）
        """
        if opinions.ndim == 1:
            opinions = opinions.reshape(-1, 1)

        # 计算每个维度的标准差
        stds = np.std(opinions, axis=0)
        # 平均标准差
        avg_std = np.mean(stds)

        # 归一化：假设观点范围是[0,1]，最大标准差为0.5
        max_std = 0.5
        consensus_level = 1 - (avg_std / max_std)

        return max(0.0, min(consensus_level, 1.0))

    def calculate_convergence_rate(self, opinion_history: List[np.ndarray]) -> float:
        """
        计算收敛速率

        使用指数衰减拟合：
        ||x(t) - mean|| ≈ exp(-λ*t)

        其中λ是收敛速率

        Args:
            opinion_history: 时间序列的观点列表

        Returns:
            收敛速率λ
        """
        if len(opinion_history) < 2:
            return 0.0

        # 计算每个时间点的标准差
        stds = []
        for opinions in opinion_history:
            if opinions.ndim == 1:
                opinions = opinions.reshape(-1, 1)
            std = np.mean(np.std(opinions, axis=0))
            stds.append(std)

        stds = np.array(stds)

        # 如果已经收敛，返回高收敛率
        if stds[-1] < 1e-6:
            return 1.0

        # 拟合指数衰减：std(t) = a * exp(-λ*t) + c
        t = np.arange(len(stds))

        try:
            # 对数变换：log(std - c) = log(a) - λ*t
            # 假设c是最终稳态值
            c = stds[-1]
            if stds[0] > c:
                log_stds = np.log(stds - c + 1e-10)
                # 线性回归拟合
                slope, _ = np.polyfit(t, log_stds, 1)
                convergence_rate = -slope
            else:
                convergence_rate = 0.0
        except:
            convergence_rate = 0.0

        # 归一化：假设λ=1为快速收敛
        return min(convergence_rate, 1.0)

    def calculate_agreement_ratio(self, opinions: np.ndarray) -> float:
        """
        计算在阈值范围内达成一致的agent比例

        Args:
            opinions: 观点数组

        Returns:
            同意比例（0-1之间）
        """
        if opinions.ndim == 1:
            opinions = opinions.reshape(-1, 1)

        # 计算均值
        mean_opinion = np.mean(opinions, axis=0)

        # 计算每个agent与均值的距离
        distances = np.linalg.norm(opinions - mean_opinion, axis=1)

        # 统计在阈值内的比例
        agree_mask = distances <= self.agreement_threshold
        agreement_ratio = np.mean(agree_mask)

        return agreement_ratio

    def calculate_cluster_separation(self, opinions: np.ndarray) -> float:
        """
        计算观点簇间的分离度

        使用轮廓系数（Silhouette Coefficient）：
        S = (b - a) / max(a, b)
        其中a是簇内距离，b是簇间最近距离

        Args:
            opinions: 观点数组

        Returns:
            簇间分离度（-1到1之间，1表示完全分离）
        """
        if opinions.ndim == 1:
            opinions = opinions.reshape(-1, 1)

        n = opinions.shape[0]
        if n < 2:
            return 0.0

        # 计算距离矩阵
        distances = squareform(pdist(opinions, metric='euclidean'))

        # 使用简单的聚类（基于阈值）
        threshold = self.agreement_threshold * 2
        clusters = self._simple_cluster(opinions, threshold)

        if len(np.unique(clusters)) == 1:
            return 0.0  # 只有一个簇

        # 计算轮廓系数
        silhouette_scores = []
        for i in range(n):
            a = self._intra_cluster_distance(i, clusters, distances)
            b = self._inter_cluster_distance(i, clusters, distances)

            if len(np.unique(clusters)) == 1:
                silhouette = 0
            else:
                silhouette = (b - a) / max(a, b) if max(a, b) > 0 else 0

            silhouette_scores.append(silhouette)

        return np.mean(silhouette_scores)

    def _simple_cluster(self, opinions: np.ndarray,
                       threshold: float) -> np.ndarray:
        """简单的距离阈值聚类"""
        n = opinions.shape[0]
        clusters = np.arange(n)

        for i in range(n):
            for j in range(i+1, n):
                dist = np.linalg.norm(opinions[i] - opinions[j])
                if dist < threshold:
                    # 合并簇
                    clusters[j] = min(clusters[i], clusters[j])
                    # 更新所有具有相同簇标签的节点
                    same_cluster = np.where(clusters == clusters[j])[0]
                    clusters[same_cluster] = min(clusters[i], clusters[j])

        return clusters

    def _intra_cluster_distance(self, i: int, clusters: np.ndarray,
                               distances: np.ndarray) -> float:
        """计算节点i的簇内平均距离"""
        cluster_id = clusters[i]
        cluster_members = np.where(clusters == cluster_id)[0]

        if len(cluster_members) == 1:
            return 0.0

        mask = np.zeros(len(distances), dtype=bool)
        mask[cluster_members] = True
        mask[i] = False

        return np.mean(distances[i][mask]) if np.any(mask) else 0.0

    def _inter_cluster_distance(self, i: int, clusters: np.ndarray,
                               distances: np.ndarray) -> float:
        """计算节点i到最近其他簇的平均距离"""
        cluster_id = clusters[i]
        other_clusters = np.unique(clusters[clusters != cluster_id])

        if len(other_clusters) == 0:
            return 0.0

        min_distances = []
        for other_id in other_clusters:
            other_members = np.where(clusters == other_id)[0]
            min_dist = np.min(distances[i][other_members])
            min_distances.append(min_dist)

        return np.mean(min_distances)

    def calculate_stability_index(self, opinion_history: List[np.ndarray],
                                 window: int = 10) -> float:
        """
        计算共识稳定性指数

        稳定性定义为最近时间窗口内共识水平的变化率

        Args:
            opinion_history: 时间序列的观点列表
            window: 时间窗口大小

        Returns:
            稳定性指数（0-1之间，1表示完全稳定）
        """
        if len(opinion_history) < window:
            window = len(opinion_history)

        if window < 2:
            return 0.0

        # 计算窗口内的共识水平
        recent_history = opinion_history[-window:]
        consensus_levels = [self.calculate_consensus_level(op)
                           for op in recent_history]

        # 计算变化率（标准差）
        stability = 1.0 - np.std(consensus_levels)

        return max(0.0, min(stability, 1.0))

    def compute_all_metrics(self, opinions: np.ndarray,
                           opinion_history: Optional[List[np.ndarray]] = None
                           ) -> ConsensusMetrics:
        """
        计算所有共识指标

        Args:
            opinions: 当前观点数组
            opinion_history: 时间序列的观点列表（可选）

        Returns:
            ConsensusMetrics对象
        """
        convergence_rate = 0.0
        stability_index = 0.0

        if opinion_history is not None and len(opinion_history) > 1:
            convergence_rate = self.calculate_convergence_rate(opinion_history)
            stability_index = self.calculate_stability_index(opinion_history)

        return ConsensusMetrics(
            consensus_level=self.calculate_consensus_level(opinions),
            convergence_rate=convergence_rate,
            agreement_ratio=self.calculate_agreement_ratio(opinions),
            cluster_separation=self.calculate_cluster_separation(opinions),
            stability_index=stability_index
        )


# ============================================================================
# 3. 创新突破检测（Innovation Detection）
# ============================================================================

@dataclass
class InnovationMetrics:
    """创新指标容器"""
    novelty_score: float  # 新颖度得分
    breakthrough_flag: bool  # 是否为突破性创新
    creativity_index: float  # 创造力指数
    paradigm_shift: float  # 范式转移程度
    innovation_entropy: float  # 创新熵


class InnovationDetector:
    """
    创新突破检测器

    理论基础：
    - 新颖度：与现有观点的距离
    - 突破性：创造新的观点聚类
    - 创造力：组合不同观点的能力
    - 范式转移：根本性改变观点分布
    """

    def __init__(self, novelty_threshold: float = 2.0,
                 breakthrough_threshold: float = 0.3):
        """
        初始化创新检测器

        Args:
            novelty_threshold: 新颖度阈值（标准差倍数）
            breakthrough_threshold: 突破性阈值
        """
        self.novelty_threshold = novelty_threshold
        self.breakthrough_threshold = breakthrough_threshold
        self.historical_opinions = []

    def calculate_novelty_score(self, new_opinion: np.ndarray,
                               existing_opinions: np.ndarray) -> float:
        """
        计算新观点的新颖度

        新颖度定义为到最近现有观点的距离（以标准差归一化）

        Args:
            new_opinion: 新观点，形状为(dim,)或(1, dim)
            existing_opinions: 现有观点集合，形状为(n, dim)

        Returns:
            新颖度得分（0-∞，越大越新颖）
        """
        if new_opinion.ndim == 1:
            new_opinion = new_opinion.reshape(1, -1)
        if existing_opinions.ndim == 1:
            existing_opinions = existing_opinions.reshape(-1, 1)

        # 计算到所有现有观点的距离
        distances = np.linalg.norm(existing_opinions - new_opinion, axis=1)

        # 最小距离
        min_distance = np.min(distances)

        # 用标准差归一化
        std = np.std(distances) if len(distances) > 1 else 1.0
        novelty_score = min_distance / (std + 1e-10)

        return novelty_score

    def detect_breakthrough(self, new_opinion: np.ndarray,
                          existing_opinions: np.ndarray,
                          existing_clusters: int) -> Tuple[bool, float]:
        """
        检测是否为突破性创新

        突破性创新定义为：
        1. 创造新的观点聚类
        2. 显著增加观点空间的覆盖

        Args:
            new_opinion: 新观点
            existing_opinions: 现有观点集合
            existing_clusters: 现有的观点簇数

        Returns:
            (是否突破, 突破程度)
        """
        # 添加新观点后的聚类数
        all_opinions = np.vstack([existing_opinions, new_opinion.reshape(1, -1)])

        diversity = ViewpointDiversity()
        new_clusters = diversity.count_opinion_clusters(all_opinions)

        # 检查是否增加了簇数
        cluster_increase = new_clusters > existing_clusters

        # 计算突破程度
        novelty = self.calculate_novelty_score(new_opinion, existing_opinions)
        breakthrough_score = (novelty / self.novelty_threshold *
                            (1 if cluster_increase else 0.5))

        is_breakthrough = (breakthrough_score > self.breakthrough_threshold
                          or cluster_increase)

        return is_breakthrough, breakthrough_score

    def calculate_creativity_index(self, opinions: np.ndarray,
                                  network: Optional['nx.Graph'] = None) -> float:
        """
        计算群体的创造力指数

        创造力定义为：
        1. 观点的多样性
        2. 观点组合的潜力（网络连接性）
        3. 跨界交流的程度

        Args:
            opinions: 观点数组
            network: agent间的交互网络（可选）

        Returns:
            创造力指数（0-1之间）
        """
        # 基础多样性
        diversity = ViewpointDiversity()
        div_metrics = diversity.compute_all_metrics(opinions)

        # 网络效应（如果有网络）
        network_effect = 1.0
        if network is not None and HAS_NETWORKX:
            # 计算网络的聚集系数（衡量局部连接性）
            clustering = nx.average_clustering(network)
            # 计算网络的小世界性（衡量全局可达性）
            try:
                avg_path_length = nx.average_shortest_path_length(network)
                # 归一化路径长度
                network_effect = clustering / (avg_path_length + 1)
            except:
                network_effect = clustering

        # 创造力 = 多样性 × 网络效应
        creativity = (div_metrics.entropy * div_metrics.dispersion *
                     network_effect)

        return min(creativity, 1.0)

    def calculate_paradigm_shift(self, before_opinions: np.ndarray,
                                after_opinions: np.ndarray) -> float:
        """
        计算范式转移程度

        范式转移定义为观点分布的显著变化，使用：
        1. 分布的Kolmogorov-Smirnov距离
        2. 主成分方向的变化
        3. 聚类结构的改变

        Args:
            before_opinions: 转移前的观点
            after_opinions: 转移后的观点

        Returns:
            范式转移程度（0-1之间）
        """
        # KS检验（每个维度）
        if before_opinions.ndim == 1:
            before_opinions = before_opinions.reshape(-1, 1)
        if after_opinions.ndim == 1:
            after_opinions = after_opinions.reshape(-1, 1)

        ks_distances = []
        for d in range(min(before_opinions.shape[1], after_opinions.shape[1])):
            ks_stat, _ = stats.ks_2samp(before_opinions[:, d],
                                        after_opinions[:, d])
            ks_distances.append(ks_stat)

        avg_ks = np.mean(ks_distances)

        # 主成分方向变化
        pca_before = PCA(n_components=1)
        pca_after = PCA(n_components=1)

        try:
            pc_before = pca_before.fit_transform(before_opinions)
            pc_after = pca_after.fit_transform(after_opinions)

            # 计算主方向的夹角
            direction_before = pca_before.components_[0]
            direction_after = pca_after.components_[0]

            cos_similarity = np.dot(direction_before, direction_after)
            angle_change = np.arccos(np.clip(cos_similarity, -1, 1)) / np.pi
        except:
            angle_change = 0.0

        # 聚类结构变化
        diversity = ViewpointDiversity()
        clusters_before = diversity.count_opinion_clusters(before_opinions)
        clusters_after = diversity.count_opinion_clusters(after_opinions)

        cluster_change = abs(clusters_after - clusters_before) / max(clusters_before, 1)

        # 综合范式转移度
        paradigm_shift = (avg_ks * 0.5 + angle_change * 0.3 +
                         cluster_change * 0.2)

        return min(paradigm_shift, 1.0)

    def calculate_innovation_entropy(self, opinion_history: List[np.ndarray]) -> float:
        """
        计算创新熵

        创新熵衡量观点演化过程中的新颖性累积

        Args:
            opinion_history: 时间序列的观点列表

        Returns:
            创新熵
        """
        if len(opinion_history) < 2:
            return 0.0

        novelty_scores = []
        for i in range(1, len(opinion_history)):
            # 计算相对于历史的新颖度
            historical = np.vstack(opinion_history[:i])
            current = opinion_history[i]

            # 对每个当前观点计算新颖度
            if current.ndim == 1:
                current = current.reshape(-1, 1)
            if historical.ndim == 1:
                historical = historical.reshape(-1, 1)

            for opinion in current:
                novelty = self.calculate_novelty_score(opinion, historical)
                novelty_scores.append(novelty)

        # 熵基累积
        if not novelty_scores:
            return 0.0

        # 归一化并计算熵
        novelty_scores = np.array(novelty_scores)
        novelty_scores = novelty_scores / (np.sum(novelty_scores) + 1e-10)

        innovation_entropy = -np.sum(novelty_scores * np.log(novelty_scores + 1e-10))

        return innovation_entropy

    def compute_all_metrics(self, opinions: np.ndarray,
                           opinion_history: Optional[List[np.ndarray]] = None,
                           network: Optional['nx.Graph'] = None
                           ) -> InnovationMetrics:
        """
        计算所有创新指标

        Args:
            opinions: 当前观点
            opinion_history: 历史观点序列（可选）
            network: 交互网络（可选）

        Returns:
            InnovationMetrics对象
        """
        # 计算平均新颖度
        if opinion_history and len(opinion_history) > 1:
            historical = np.vstack(opinion_history[:-1])
            current = opinion_history[-1]

            novelty_scores = []
            for i in range(current.shape[0]):
                opinion = current[i] if current.ndim > 1 else current
                novelty = self.calculate_novelty_score(opinion, historical)
                novelty_scores.append(novelty)

            avg_novelty = np.mean(novelty_scores)

            # 突破检测
            diversity = ViewpointDiversity()
            existing_clusters = diversity.count_opinion_clusters(historical)
            is_breakthrough, breakthrough_score = self.detect_breakthrough(
                current[0] if current.ndim > 1 else current,
                historical,
                existing_clusters
            )
        else:
            avg_novelty = 0.0
            is_breakthrough = False
            breakthrough_score = 0.0

        # 创造力指数
        creativity = self.calculate_creativity_index(opinions, network)

        # 范式转移
        paradigm_shift = 0.0
        innovation_entropy = 0.0

        if opinion_history and len(opinion_history) >= 2:
            paradigm_shift = self.calculate_paradigm_shift(
                opinion_history[0], opinions
            )
            innovation_entropy = self.calculate_innovation_entropy(opinion_history)

        return InnovationMetrics(
            novelty_score=avg_novelty,
            breakthrough_flag=is_breakthrough,
            creativity_index=creativity,
            paradigm_shift=paradigm_shift,
            innovation_entropy=innovation_entropy
        )


# ============================================================================
# 4. 社会选择理论和投票算法
# ============================================================================

class VotingRule(Enum):
    """投票规则类型"""
    MAJORITY = "majority"  # 简单多数
    CONDORCET = "condorcet"  # 孔多塞规则
    BORDA = "borda"  # 博达计数
    APPROVAL = "approval"  # 批准投票
    RANGE = "range"  # 范围投票
    MEDIAN = "median"  # 中位数规则


@dataclass
class VotingResult:
    """投票结果"""
    winner: int  # 获胜者索引
    consensus_score: float  # 共识得分
    participation_rate: float  # 参与率
    social_welfare: float  # 社会福利
    rule_used: VotingRule  # 使用的规则


class SocialChoiceCalculator:
    """
    社会选择计算器

    实现多种投票和共识算法：
    - 简单多数规则
    - 孔多塞赢家
    - 博达计数
    - 批准投票
    - 范围投票
    - 中位数规则
    """

    def __init__(self):
        """初始化社会选择计算器"""
        self.preference_history = []

    def majority_rule(self, preferences: np.ndarray) -> VotingResult:
        """
        简单多数规则

        选择获得最多第一偏好选择的选项

        Args:
            preferences: 偏好矩阵，形状为(n_voters, n_alternatives)
                        表示每个投票者对每个选项的排名（1为最高）

        Returns:
            VotingResult对象
        """
        # 统计第一偏好的票数
        first_choices = np.argmin(preferences, axis=1)
        vote_counts = np.bincount(first_choices)
        winner = int(np.argmax(vote_counts))

        # 共识得分：获胜者得票比例
        consensus_score = vote_counts[winner] / len(preferences)

        # 社会福利：平均排名
        welfare = np.mean(preferences[:, winner])

        return VotingResult(
            winner=winner,
            consensus_score=consensus_score,
            participation_rate=1.0,
            social_welfare=1.0 - (welfare - 1) / preferences.shape[1],
            rule_used=VotingRule.MAJORITY
        )

    def condorcet_rule(self, preferences: np.ndarray) -> VotingResult:
        """
        孔多塞规则

        孔多塞赢家是在两两比较中击败所有其他选项的候选者

        Args:
            preferences: 偏好矩阵

        Returns:
            VotingResult对象
        """
        n_alternatives = preferences.shape[1]

        # 两两比较矩阵
        comparison_matrix = np.zeros((n_alternatives, n_alternatives))

        for i in range(n_alternatives):
            for j in range(n_alternatives):
                if i != j:
                    # 统计偏好i超过j的投票者数量
                    votes_for_i = np.sum(preferences[:, i] < preferences[:, j])
                    comparison_matrix[i, j] = votes_for_i

        # 寻找孔多塞赢家
        winner = -1
        for i in range(n_alternatives):
            if all(comparison_matrix[i, j] > len(preferences) / 2
                   for j in range(n_alternatives) if i != j):
                winner = i
                break

        # 如果没有孔多塞赢家，使用Copeland规则
        if winner == -1:
            copeland_scores = np.sum(comparison_matrix > len(preferences) / 2, axis=1)
            winner = int(np.argmax(copeland_scores))

        # 共识得分：最小优势比例
        min_advantage = np.min(comparison_matrix[winner, :]) / len(preferences)
        consensus_score = max(0.5, min_advantage)

        return VotingResult(
            winner=winner,
            consensus_score=consensus_score,
            participation_rate=1.0,
            social_welfare=consensus_score,
            rule_used=VotingRule.CONDORCET
        )

    def borda_count(self, preferences: np.ndarray) -> VotingResult:
        """
        博达计数法

        每个选项根据排名获得积分，最高分获胜

        Args:
            preferences: 偏好矩阵

        Returns:
            VotingResult对象
        """
        n_alternatives = preferences.shape[1]

        # 博达分数：倒数排名的积分
        scores = np.sum(n_alternatives - preferences, axis=0)
        winner = int(np.argmax(scores))

        # 共识得分：归一化的得分差
        total_score = np.sum(scores)
        consensus_score = scores[winner] / total_score if total_score > 0 else 0

        return VotingResult(
            winner=winner,
            consensus_score=consensus_score,
            participation_rate=1.0,
            social_welfare=consensus_score,
            rule_used=VotingRule.BORDA
        )

    def approval_voting(self, preferences: np.ndarray,
                       threshold: float = 0.6) -> VotingResult:
        """
        批准投票

        投票者批准所有达到阈值的选项

        Args:
            preferences: 偏好矩阵（可以是0-1之间的满意度评分）
            threshold: 批准阈值

        Returns:
            VotingResult对象
        """
        # 如果是排名形式，转换为满意度
        if preferences.min() >= 1:
            satisfactions = 1.0 / preferences
        else:
            satisfactions = preferences

        # 计算批准数
        approvals = np.sum(satisfactions >= threshold, axis=0)
        winner = int(np.argmax(approvals))

        # 共识得分
        consensus_score = approvals[winner] / len(preferences)

        return VotingResult(
            winner=winner,
            consensus_score=consensus_score,
            participation_rate=1.0,
            social_welfare=consensus_score,
            rule_used=VotingRule.APPROVAL
        )

    def range_voting(self, utilities: np.ndarray) -> VotingResult:
        """
        范围投票

        投票者给每个选项评分，平均分最高者获胜

        Args:
            utilities: 效用矩阵，形状为(n_voters, n_alternatives)
                      表示每个投票者对每个选项的效用评分

        Returns:
            VotingResult对象
        """
        # 计算平均效用
        mean_utilities = np.mean(utilities, axis=0)
        winner = int(np.argmax(mean_utilities))

        # 共识得分：归一化的平均效用
        max_utility = np.max(utilities)
        consensus_score = mean_utilities[winner] / max_utility if max_utility > 0 else 0

        return VotingResult(
            winner=winner,
            consensus_score=consensus_score,
            participation_rate=1.0,
            social_welfare=consensus_score,
            rule_used=VotingRule.RANGE
        )

    def median_rule(self, opinions: np.ndarray) -> VotingResult:
        """
        中位数规则

        选择中位数观点作为社会选择

        适用于一维观点空间，具有良好的策略抗性

        Args:
            opinions: 观点数组，形状为(n_agents, n_alternatives)

        Returns:
            VotingResult对象
        """
        # 计算每个选项的中位数
        medians = np.median(opinions, axis=0)
        winner = int(np.argmax(medians))

        # 共识得分：中位数相对于最大值的比例
        consensus_score = medians[winner] / np.max(medians) if np.max(medians) > 0 else 0

        return VotingResult(
            winner=winner,
            consensus_score=consensus_score,
            participation_rate=1.0,
            social_welfare=consensus_score,
            rule_used=VotingRule.MEDIAN
        )

    def compute_consensus_curve(self, opinions_history: List[np.ndarray],
                               rule: VotingRule = VotingRule.MEDIAN) -> np.ndarray:
        """
        计算共识演化曲线

        Args:
            opinions_history: 时间序列的观点列表
            rule: 使用的投票规则

        Returns:
            共识水平的时间序列
        """
        consensus_levels = []

        for opinions in opinions_history:
            if opinions.ndim == 1:
                opinions = opinions.reshape(-1, 1)

            if rule == VotingRule.MEDIAN:
                # 使用标准差作为共识的逆指标
                consensus = 1.0 - np.std(opinions) / 0.5
            elif rule == VotingRule.MAJORITY:
                # 将连续观点离散化
                bins = np.linspace(0, 1, 6)
                discretized = np.digitize(opinions.flatten(), bins)
                first_choices = np.bincount(discretized)
                consensus = np.max(first_choices) / len(discretized)
            else:
                # 默认使用标准差
                consensus = 1.0 - np.std(opinions) / 0.5

            consensus_levels.append(max(0.0, min(consensus, 1.0)))

        return np.array(consensus_levels)


# ============================================================================
# 5. 观点动力学建模（Opinion Dynamics）
# ============================================================================

class DynamicsModel(Enum):
    """观点动力学模型类型"""
    DEGROOT = "degroot"  # DeGroot模型
    FRIEDKIN_JOHNSEN = "friedkin_johnsen"  # Friedkin-Johnsen模型
    HEGSELMANN_KRAUSE = "hegelmann_krause"  # Hegselmann-Krause模型
    BOUNDED_CONFIDENCE = "bounded_confidence"  # 有界置信模型
    VICSEK = "vicsek"  # Vicsek模型


class OpinionDynamicsSimulator:
    """
    观点动力学模拟器

    实现多种经典的观点动力学模型：
    - DeGroot模型：基于信任加权的观点更新
    - Friedkin-Johnsen模型：考虑固有偏见的观点更新
    - Hegselmann-Krause模型：有界置信的agent聚类
    - Vicsek模型：群体对齐行为
    """

    def __init__(self, n_agents: int, opinion_dim: int = 1):
        """
        初始化模拟器

        Args:
            n_agents: agent数量
            opinion_dim: 观点空间维度
        """
        self.n_agents = n_agents
        self.opinion_dim = opinion_dim
        self.opinion_history = []

    def degroot_model(self, initial_opinions: np.ndarray,
                     influence_matrix: np.ndarray,
                     n_steps: int = 100) -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        DeGroot模型

        观点更新规则：
        x(t+1) = W * x(t)

        其中W是影响矩阵（行随机矩阵）

        Args:
            initial_opinions: 初始观点，形状为(n_agents, dim)
            influence_matrix: 影响矩阵W，形状为(n_agents, n_agents)
            n_steps: 模拟步数

        Returns:
            (最终观点, 观点历史)
        """
        opinions = initial_opinions.copy()
        history = [opinions.copy()]

        for _ in range(n_steps):
            opinions = influence_matrix @ opinions
            history.append(opinions.copy())

            # 检查收敛
            if np.std(opinions) < 1e-6:
                break

        return opinions, history

    def friedkin_johnsen_model(self, initial_opinions: np.ndarray,
                              influence_matrix: np.ndarray,
                              stubbornness: np.ndarray,
                              n_steps: int = 100) -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        Friedkin-Johnsen模型

        观点更新规则：
        x(t+1) = A * W * x(t) + (I - A) * x(0)

        其中A是对角矩阵，对角线元素是agent的开放性(1-stubbornness)

        Args:
            initial_opinions: 初始观点
            influence_matrix: 影响矩阵W
            stubbornness: 固执程度，形状为(n_agents,)，0为完全开放，1为完全固执
            n_steps: 模拟步数

        Returns:
            (最终观点, 观点历史)
        """
        opinions = initial_opinions.copy()
        history = [opinions.copy()]

        # 开放性矩阵
        openness = 1.0 - stubbornness
        A = np.diag(openness)

        for _ in range(n_steps):
            opinions = A @ (influence_matrix @ opinions) + (np.diag(1 - openness) @ initial_opinions)
            history.append(opinions.copy())

            if np.std(opinions - history[-2]) < 1e-6:
                break

        return opinions, history

    def hegelmann_krause_model(self, initial_opinions: np.ndarray,
                              confidence_threshold: float = 0.2,
                              n_steps: int = 100) -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        Hegselmann-Krause有界置信模型

        观点更新规则：
        x_i(t+1) = (1/|N_i(t)|) * Σ_{j in N_i(t)} x_j(t)

        其中N_i(t) = {j: |x_i(t) - x_j(t)| <= ε}

        Args:
            initial_opinions: 初始观点
            confidence_threshold: 置信阈值ε
            n_steps: 模拟步数

        Returns:
            (最终观点, 观点历史)
        """
        opinions = initial_opinions.copy()
        history = [opinions.copy()]

        for _ in range(n_steps):
            new_opinions = opinions.copy()

            for i in range(self.n_agents):
                # 找到置信范围内的邻居
                distances = np.linalg.norm(opinions - opinions[i], axis=1)
                neighbors = np.where(distances <= confidence_threshold)[0]

                # 更新观点
                if len(neighbors) > 0:
                    new_opinions[i] = np.mean(opinions[neighbors], axis=0)

            opinions = new_opinions
            history.append(opinions.copy())

            if np.std(opinions - history[-2]) < 1e-6:
                break

        return opinions, history

    def vicsek_model(self, initial_positions: np.ndarray,
                    initial_velocities: np.ndarray,
                    interaction_radius: float = 0.1,
                    noise_level: float = 0.0,
                    n_steps: int = 100,
                    dt: float = 0.01) -> Tuple[np.ndarray, np.ndarray, List[np.ndarray]]:
        """
        Vicsek模型（简化版观点对齐）

        速度更新规则：
        v_i(t+1) = normalize(Σ_{j in N_i(t)} v_j(t)) + noise

        用于模拟群体行为的同步和对齐

        Args:
            initial_positions: 初始位置
            initial_velocities: 初始速度（作为观点）
            interaction_radius: 交互半径
            noise_level: 噪声水平
            n_steps: 模拟步数
            dt: 时间步长

        Returns:
            (最终位置, 最终速度, 速度历史)
        """
        positions = initial_positions.copy()
        velocities = initial_velocities.copy()
        history = [velocities.copy()]

        for _ in range(n_steps):
            new_velocities = velocities.copy()

            for i in range(self.n_agents):
                # 找到交互半径内的邻居
                distances = np.linalg.norm(positions - positions[i], axis=1)
                neighbors = np.where(distances <= interaction_radius)[0]

                # 计算平均速度方向
                if len(neighbors) > 0:
                    avg_velocity = np.mean(velocities[neighbors], axis=0)
                    # 归一化
                    norm = np.linalg.norm(avg_velocity)
                    if norm > 0:
                        avg_velocity = avg_velocity / norm

                    # 添加噪声
                    noise = np.random.randn(*avg_velocity.shape) * noise_level
                    new_velocities[i] = avg_velocity + noise

                    # 归一化速度
                    norm = np.linalg.norm(new_velocities[i])
                    if norm > 0:
                        new_velocities[i] = new_velocities[i] / norm

            # 更新位置
            positions = positions + velocities * dt
            velocities = new_velocities
            history.append(velocities.copy())

        return positions, velocities, history

    def simulate_network_dynamics(self, initial_opinions: np.ndarray,
                                 network: Optional['nx.Graph'] = None,
                                 influence_matrix: Optional[np.ndarray] = None,
                                 model: DynamicsModel = DynamicsModel.DEGROOT,
                                 **kwargs) -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        在网络上模拟观点动力学

        Args:
            initial_opinions: 初始观点
            network: agent间的交互网络（可选，需要networkx）
            influence_matrix: 直接提供影响矩阵（可选）
            model: 使用的动力学模型
            **kwargs: 模型特定参数

        Returns:
            (最终观点, 观点历史)
        """
        n = self.n_agents

        # 构建影响矩阵
        if influence_matrix is not None:
            adj_matrix = influence_matrix
        elif network is not None and HAS_NETWORKX:
            adj_matrix = nx.adjacency_matrix(network).toarray()
        else:
            raise ValueError("必须提供network或influence_matrix")

        # 归一化为行随机矩阵
        influence_matrix = adj_matrix / (adj_matrix.sum(axis=1, keepdims=True) + 1e-10)
        influence_matrix = np.nan_to_num(influence_matrix, nan=0.0)

        if model == DynamicsModel.DEGROOT:
            return self.degroot_model(initial_opinions, influence_matrix, **kwargs)
        elif model == DynamicsModel.FRIEDKIN_JOHNSEN:
            stubbornness = kwargs.get('stubbornness', np.zeros(n))
            return self.friedkin_johnsen_model(initial_opinions, influence_matrix,
                                             stubbornness, **kwargs)
        else:
            # 默认使用DeGroot模型
            return self.degroot_model(initial_opinions, influence_matrix, **kwargs)


# ============================================================================
# 6. 涌现检测综合分析器
# ============================================================================

@dataclass
class EmergenceReport:
    """涌现检测报告"""
    # 多样性指标
    diversity: DiversityMetrics

    # 共识指标
    consensus: ConsensusMetrics

    # 创新指标
    innovation: InnovationMetrics

    # 综合涌现指标
    emergence_strength: float  # 涌现强度
    emergence_type: str  # 涌现类型
    phase: str  # 系统所处阶段

    # 涌现特征
    has_consensus: bool
    has_polarization: bool
    has_innovation: bool
    has_fragmentation: bool


class EmergenceDetector:
    """
    涌现检测综合分析器

    整合所有指标，检测多Agent系统中的涌现现象
    """

    def __init__(self, n_agents: int, opinion_dim: int = 1):
        """
        初始化涌现检测器

        Args:
            n_agents: agent数量
            opinion_dim: 观点维度
        """
        self.n_agents = n_agents
        self.opinion_dim = opinion_dim

        # 子分析器
        self.diversity_analyzer = ViewpointDiversity(opinion_dim)
        self.consensus_analyzer = ConsensusAnalyzer()
        self.innovation_detector = InnovationDetector()
        self.social_choice = SocialChoiceCalculator()
        self.dynamics_simulator = OpinionDynamicsSimulator(n_agents, opinion_dim)

        # 历史数据
        self.opinion_history = []
        self.baseline_diversity = None

    def detect_emergence(self, current_opinions: np.ndarray,
                        network: Optional['nx.Graph'] = None,
                        update_history: bool = True) -> EmergenceReport:
        """
        检测涌现现象

        Args:
            current_opinions: 当前观点
            network: 交互网络（可选）
            update_history: 是否更新历史记录

        Returns:
            EmergenceReport对象
        """
        if update_history:
            self.opinion_history.append(current_opinions.copy())

        # 计算各类指标
        diversity = self.diversity_analyzer.compute_all_metrics(current_opinions)

        opinion_hist = self.opinion_history if len(self.opinion_history) > 1 else None
        consensus = self.consensus_analyzer.compute_all_metrics(current_opinions, opinion_hist)

        innovation = self.innovation_detector.compute_all_metrics(
            current_opinions, opinion_hist, network
        )

        # 分析涌现类型
        emergence_type, phase = self._classify_emergence(diversity, consensus, innovation)

        # 计算涌现强度
        emergence_strength = self._calculate_emergence_strength(
            diversity, consensus, innovation
        )

        # 检测涌现特征
        features = self._detect_emergence_features(diversity, consensus, innovation)

        return EmergenceReport(
            diversity=diversity,
            consensus=consensus,
            innovation=innovation,
            emergence_strength=emergence_strength,
            emergence_type=emergence_type,
            phase=phase,
            **features
        )

    def _classify_emergence(self, diversity: DiversityMetrics,
                           consensus: ConsensusMetrics,
                           innovation: InnovationMetrics) -> Tuple[str, str]:
        """
        分类涌现类型和系统阶段
        """
        # 定义阈值
        HIGH_CONSENSUS = 0.8
        HIGH_DIVERSITY = 0.6
        HIGH_POLARIZATION = 0.5

        # 判断阶段
        if consensus.consensus_level > HIGH_CONSENSUS:
            if consensus.agreement_ratio > 0.9:
                phase = "unified"  # 统一阶段
            else:
                phase = "converging"  # 收敛阶段
        elif diversity.polarization > HIGH_POLARIZATION:
            phase = "polarized"  # 极化阶段
        elif diversity.cluster_count > 2:
            phase = "fragmented"  # 碎片化阶段
        elif innovation.breakthrough_flag:
            phase = "innovative"  # 创新阶段
        else:
            phase = "exploring"  # 探索阶段

        # 判断涌现类型
        if innovation.breakthrough_flag:
            emergence_type = "creative_emergence"  # 创造性涌现
        elif consensus.convergence_rate > 0.5 and consensus.consensus_level > HIGH_CONSENSUS:
            emergence_type = "consensus_emergence"  # 共识涌现
        elif diversity.polarization > HIGH_POLARIZATION:
            emergence_type = "polarization_emergence"  # 极化涌现
        elif diversity.cluster_count > 3 and diversity.dispersion > HIGH_DIVERSITY:
            emergence_type = "diversity_emergence"  # 多样性涌现
        else:
            emergence_type = "weak_emergence"  # 弱涌现

        return emergence_type, phase

    def _calculate_emergence_strength(self, diversity: DiversityMetrics,
                                     consensus: ConsensusMetrics,
                                     innovation: InnovationMetrics) -> float:
        """
        计算涌现强度

        涌现强度综合了多样性、共识和创新等多个维度
        """
        # 各维度得分
        diversity_score = diversity.entropy * diversity.dispersion
        consensus_score = consensus.consensus_level * consensus.stability_index
        innovation_score = innovation.creativity_index * (1.0 if innovation.breakthrough_flag else 0.5)

        # 非线性组合（涌现往往是非线性的）
        emergence_strength = (
            0.3 * diversity_score +
            0.3 * consensus_score +
            0.4 * innovation_score
        )

        # 考虑交互效应
        interaction_effect = diversity_score * consensus_score * innovation_score
        emergence_strength += 0.5 * interaction_effect

        return min(emergence_strength, 1.0)

    def _detect_emergence_features(self, diversity: DiversityMetrics,
                                  consensus: ConsensusMetrics,
                                  innovation: InnovationMetrics) -> Dict:
        """
        检测具体的涌现特征
        """
        return {
            'has_consensus': consensus.consensus_level > 0.8,
            'has_polarization': diversity.polarization > 0.5,
            'has_innovation': innovation.breakthrough_flag or innovation.novelty_score > 2.0,
            'has_fragmentation': diversity.cluster_count > 3
        }

    def simulate_and_detect(self, initial_opinions: np.ndarray,
                           network: Optional['nx.Graph'] = None,
                           influence_matrix: Optional[np.ndarray] = None,
                           model: DynamicsModel = DynamicsModel.DEGROOT,
                           n_steps: int = 100,
                           detection_interval: int = 5) -> List[EmergenceReport]:
        """
        模拟观点演化并持续检测涌现

        Args:
            initial_opinions: 初始观点
            network: 交互网络
            model: 动力学模型
            n_steps: 模拟步数
            detection_interval: 检测间隔

        Returns:
            涌现报告列表
        """
        # 模拟动力学
        final_opinions, history = self.dynamics_simulator.simulate_network_dynamics(
            initial_opinions, network, influence_matrix, model, n_steps=n_steps
        )

        # 定期检测涌现
        reports = []
        for i, opinions in enumerate(history[::detection_interval]):
            report = self.detect_emergence(opinions, network, update_history=False)
            reports.append(report)

        return reports

    def visualize_emergence(self, reports: List[EmergenceReport],
                          save_path: Optional[str] = None):
        """
        可视化涌现过程（需要matplotlib）

        Args:
            reports: 涌现报告列表
            save_path: 保存路径（可选）
        """
        try:
            import matplotlib.pyplot as plt

            fig, axes = plt.subplots(2, 2, figsize=(12, 10))

            # 提取时间序列数据
            times = range(len(reports))

            # 1. 多样性演化
            axes[0, 0].plot(times, [r.diversity.entropy for r in reports],
                          label='Entropy', marker='o')
            axes[0, 0].plot(times, [r.diversity.dispersion for r in reports],
                          label='Dispersion', marker='s')
            axes[0, 0].set_xlabel('Time')
            axes[0, 0].set_ylabel('Diversity')
            axes[0, 0].set_title('Diversity Evolution')
            axes[0, 0].legend()
            axes[0, 0].grid(True)

            # 2. 共识演化
            axes[0, 1].plot(times, [r.consensus.consensus_level for r in reports],
                          label='Consensus Level', marker='o')
            axes[0, 1].plot(times, [r.consensus.agreement_ratio for r in reports],
                          label='Agreement Ratio', marker='s')
            axes[0, 1].set_xlabel('Time')
            axes[0, 1].set_ylabel('Consensus')
            axes[0, 1].set_title('Consensus Evolution')
            axes[0, 1].legend()
            axes[0, 1].grid(True)

            # 3. 创新演化
            axes[1, 0].plot(times, [r.innovation.novelty_score for r in reports],
                          label='Novelty', marker='o')
            axes[1, 0].plot(times, [r.innovation.creativity_index for r in reports],
                          label='Creativity', marker='s')
            axes[1, 0].set_xlabel('Time')
            axes[1, 0].set_ylabel('Innovation')
            axes[1, 0].set_title('Innovation Evolution')
            axes[1, 0].legend()
            axes[1, 0].grid(True)

            # 4. 涌现强度
            axes[1, 1].plot(times, [r.emergence_strength for r in reports],
                          label='Emergence Strength', marker='o', linewidth=2)
            phases = [r.phase for r in reports]
            unique_phases = list(set(phases))
            colors = plt.cm.tab10(np.linspace(0, 1, len(unique_phases)))

            for i, phase in enumerate(unique_phases):
                phase_times = [t for t, p in zip(times, phases) if p == phase]
                phase_strengths = [reports[t].emergence_strength for t in phase_times]
                axes[1, 1].scatter(phase_times, phase_strengths,
                                  label=phase, color=colors[i], s=100, alpha=0.3)

            axes[1, 1].set_xlabel('Time')
            axes[1, 1].set_ylabel('Emergence Strength')
            axes[1, 1].set_title('Emergence Detection')
            axes[1, 1].legend()
            axes[1, 1].grid(True)

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')

            plt.show()

        except ImportError:
            print("Matplotlib not available. Skipping visualization.")


# ============================================================================
# 7. 复杂系统理论联系
# ============================================================================

class ComplexSystemsMetrics:
    """
    复杂系统理论相关指标

    包括：
    - 临界性指标
    - 相变检测
    - 信息流
    - 因果涌现
    """

    @staticmethod
    def calculate_criticality_indicator(opinion_history: List[np.ndarray],
                                       window: int = 10) -> float:
        """
        计算临界性指标

        临界性特征：
        1. 雪崩效应（小扰动大影响）
        2. 幂律分布
        3. 1/f噪声

        使用方差变化的波动性来近似

        Args:
            opinion_history: 观点历史
            window: 时间窗口

        Returns:
            临界性指标（0-1之间）
        """
        if len(opinion_history) < window:
            return 0.0

        # 计算每个时间点的方差
        variances = [np.var(op) for op in opinion_history]
        variances = np.array(variances)

        # 计算波动性的方差
        volatility = np.std(variances[-window:])

        # 归一化
        max_volatility = np.std(variances) if len(variances) > 1 else 1.0
        criticality = volatility / (max_volatility + 1e-10)

        return min(criticality, 1.0)

    @staticmethod
    def detect_phase_transition(opinion_history: List[np.ndarray],
                               threshold: float = 0.3) -> List[int]:
        """
        检测相变点

        相变特征：多样性或共识水平的突然变化

        Args:
            opinion_history: 观点历史
            threshold: 变化阈值

        Returns:
            相变点索引列表
        """
        if len(opinion_history) < 3:
            return []

        # 计算多样性时间序列
        diversity_analyzer = ViewpointDiversity()
        diversity_series = [diversity_analyzer.calculate_entropy_diversity(op)
                           for op in opinion_history]

        # 计算差分
        diffs = np.abs(np.diff(diversity_series))

        # 检测突变点
        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs)

        transition_points = []
        for i, diff in enumerate(diffs):
            if diff > mean_diff + threshold * std_diff:
                transition_points.append(i + 1)

        return transition_points

    @staticmethod
    def calculate_transfer_entropy(source: np.ndarray,
                                  target: np.ndarray,
                                  bins: int = 10) -> float:
        """
        计算迁移熵（Transfer Entropy）

        迁移熵衡量时间序列之间的信息流：
        TE_{X->Y} = H(Y_{t+1}|Y_t) - H(Y_{t+1}|Y_t, X_t)

        Args:
            source: 源时间序列
            target: 目标时间序列
            bins: 离散化的箱数

        Returns:
            迁移熵值
        """
        if len(source) < 3 or len(target) < 3:
            return 0.0

        # 离散化
        source_disc = np.digitize(source, np.linspace(0, 1, bins))
        target_disc = np.digitize(target, np.linspace(0, 1, bins))

        # 计算条件熵
        def conditional_entropy(x, y_given):
            """计算H(x|y_given)"""
            # 联合分布
            unique_y = np.unique(y_given)
            ce = 0.0
            for y in unique_y:
                mask = y_given == y
                x_given_y = x[mask]
                if len(x_given_y) > 0:
                    # 条件分布
                    counts = np.bincount(x_given_y, minlength=bins)
                    probs = counts / np.sum(counts)
                    probs = probs[probs > 0]
                    ce -= np.sum(probs * np.log(probs)) * np.mean(mask)
            return ce

        # H(Y_{t+1}|Y_t)
        ce1 = conditional_entropy(target_disc[1:], target_disc[:-1])

        # H(Y_{t+1}|Y_t, X_t)
        joint_condition = np.vstack([target_disc[:-1], source_disc[:-1]]).T
        # 将联合条件转换为单一标签
        joint_labels = target_disc[:-1] * bins + source_disc[:-1]
        ce2 = conditional_entropy(target_disc[1:], joint_labels)

        # 迁移熵
        transfer_entropy = ce1 - ce2

        return max(0, transfer_entropy)

    @staticmethod
    def calculate_causal_emergence(micro_states: np.ndarray,
                                  macro_states: np.ndarray,
                                  bins: int = 10) -> float:
        """
        计算因果涌现（Causal Emergence）

        因果涌现 = EI(macro) - EI(micro)
        其中EI是有效信息（Effective Information）

        Args:
            micro_states: 微观状态序列
            macro_states: 宏观状态序列
            bins: 离散化箱数

        Returns:
            因果涌现值（正值表示宏观涌现）
        """
        def effective_information(states):
            """计算有效信息"""
            if len(states) < 2:
                return 0.0

            # 离散化（确保索引从0开始）
            disc = np.digitize(states, np.linspace(0, 1, bins + 1)) - 1
            disc = np.clip(disc, 0, bins - 1)  # 确保在有效范围内

            # 状态转移矩阵
            n_states = bins
            T = np.zeros((n_states, n_states))

            for i in range(len(disc) - 1):
                T[disc[i], disc[i+1]] += 1

            # 归一化
            row_sums = T.sum(axis=1, keepdims=True)
            T = np.divide(T, row_sums, out=np.zeros_like(T), where=row_sums>0)

            # 均匀分布作为输入分布
            uniform_dist = np.ones(n_states) / n_states

            # 计算有效信息
            ei = 0.0
            for i in range(n_states):
                for j in range(n_states):
                    if T[i, j] > 0 and uniform_dist[i] > 0:
                        ei += uniform_dist[i] * T[i, j] * np.log2(T[i, j] / uniform_dist[j] + 1e-10)

            return ei

        ei_micro = effective_information(micro_states)
        ei_macro = effective_information(macro_states)

        causal_emergence = ei_macro - ei_micro

        return causal_emergence


# ============================================================================
# 使用示例
# ============================================================================

def example_usage():
    """
    涌现检测方法使用示例
    """
    print("=" * 60)
    print("多Agent涌现检测方法示例")
    print("=" * 60)

    # 1. 创建示例数据
    n_agents = 50
    n_steps = 20

    # 初始观点（正态分布）
    np.random.seed(42)
    initial_opinions = np.random.normal(0.5, 0.2, (n_agents, 1))
    initial_opinions = np.clip(initial_opinions, 0, 1)

    # 创建简单影响矩阵（环形网络）
    influence_matrix = np.zeros((n_agents, n_agents))
    for i in range(n_agents):
        influence_matrix[i, i] = 0.5
        influence_matrix[i, (i-1) % n_agents] = 0.25
        influence_matrix[i, (i+1) % n_agents] = 0.25

    print(f"\n系统配置：")
    print(f"  - Agent数量: {n_agents}")
    print(f"  - 初始观点范围: [{initial_opinions.min():.3f}, {initial_opinions.max():.3f}]")
    print(f"  - 网络类型: 环形网络（每个agent连接2个邻居）")

    # 2. 初始化检测器
    detector = EmergenceDetector(n_agents=n_agents, opinion_dim=1)

    # 3. 模拟观点演化并检测涌现
    print(f"\n开始模拟观点动力学...")
    reports = detector.simulate_and_detect(
        initial_opinions=initial_opinions,
        influence_matrix=influence_matrix,
        model=DynamicsModel.DEGROOT,
        n_steps=n_steps,
        detection_interval=2
    )

    # 4. 分析结果
    print(f"\n涌现检测结果：")
    print(f"  - 检测次数: {len(reports)}")

    for i, report in enumerate(reports[::len(reports)//5]):  # 显示部分结果
        print(f"\n  时间点 {i*2}:")
        print(f"    - 阶段: {report.phase}")
        print(f"    - 涌现类型: {report.emergence_type}")
        print(f"    - 涌现强度: {report.emergence_strength:.3f}")
        print(f"    - 多样性(熵): {report.diversity.entropy:.3f}")
        print(f"    - 共识水平: {report.consensus.consensus_level:.3f}")
        print(f"    - 创造力指数: {report.innovation.creativity_index:.3f}")

    # 5. 统计涌现阶段
    phases = [r.phase for r in reports]
    phase_counts = {p: phases.count(p) for p in set(phases)}
    print(f"\n阶段分布: {phase_counts}")

    # 6. 计算复杂系统指标
    print(f"\n复杂系统指标:")
    opinion_history = [initial_opinions] * n_steps  # 简化的历史

    criticality = ComplexSystemsMetrics.calculate_criticality_indicator(opinion_history)
    print(f"  - 临界性指标: {criticality:.3f}")

    transitions = ComplexSystemsMetrics.detect_phase_transition(opinion_history)
    print(f"  - 检测到的相变点: {transitions}")

    # 7. 尝试可视化
    print(f"\n尝试可视化涌现过程...")
    detector.visualize_emergence(reports, save_path="emergence_evolution.png")

    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)

    return detector, reports


if __name__ == "__main__":
    # 运行示例
    detector, reports = example_usage()
