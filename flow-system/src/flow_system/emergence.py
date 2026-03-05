"""
真涌现检测模块

基于复杂系统理论的真涌现检测:
1. Takens嵌入定理 - 相空间重构
2. Lyapunov指数 - 吸引子检测
3. 信息论 - 有效信息(EI)度量
4. 向下因果 - 宏观约束检测

评分核心: 从伪涌现(聚类)到真涌现(动力学系统分析)
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from scipy.spatial.distance import pdist, squareform
from scipy.stats import entropy
from sklearn.neighbors import NearestNeighbors

from .config import Config
from .utils import logger


class TakensEmbedding:
    """Takens嵌入定理实现

    将时间序列重构为高维相空间轨迹
    """

    def __init__(self, dimension: int = 3, delay: int = 1):
        """
        Args:
            dimension: 嵌入维度
            delay: 时间延迟
        """
        self.dimension = dimension
        self.delay = delay
        logger.info(f"Takens embedding: dim={dimension}, delay={delay}")

    def embed(self, time_series: np.ndarray) -> np.ndarray:
        """嵌入时间序列到相空间

        Args:
            time_series: 1D时间序列 (n_steps, n_features)的某一特征

        Returns:
            嵌入后的相空间轨迹 (n_points, dimension)
        """
        if len(time_series) < self.dimension * self.delay:
            logger.warning("Time series too short for embedding")
            return np.array([])

        n_points = len(time_series) - (self.dimension - 1) * self.delay
        embedded = np.zeros((n_points, self.dimension))

        for i in range(self.dimension):
            start = i * self.delay
            end = start + n_points
            embedded[:, i] = time_series[start:end]

        return embedded

    def embed_multivariate(self, trajectory: np.ndarray) -> np.ndarray:
        """嵌入多维特征轨迹

        Args:
            trajectory: (n_steps, n_features) 特征演化轨迹

        Returns:
            嵌入后的相空间 (n_points, dimension * n_features)
        """
        if trajectory.ndim == 1:
            return self.embed(trajectory)

        n_features = trajectory.shape[1]
        embedded_list = []

        for feat_idx in range(n_features):
            embedded = self.embed(trajectory[:, feat_idx])
            if len(embedded) > 0:
                embedded_list.append(embedded)

        if not embedded_list:
            return np.array([])

        # 拼接所有特征的嵌入
        return np.hstack(embedded_list)


class LyapunovCalculator:
    """Lyapunov指数计算器

    用于检测系统是否收敛到吸引子（负指数）
    """

    def __init__(self, epsilon: float = 1e-3, max_iter: int = 50):
        """
        Args:
            epsilon: 初始扰动大小
            max_iter: 最大迭代次数
        """
        self.epsilon = epsilon
        self.max_iter = max_iter
        logger.info(f"Lyapunov calculator: epsilon={epsilon}, max_iter={max_iter}")

    def calculate(self, trajectory: np.ndarray) -> float:
        """计算最大Lyapunov指数

        Args:
            trajectory: 相空间轨迹 (n_points, n_dims)

        Returns:
            最大Lyapunov指数 (负数=收敛, 正数=发散, ~0=周期)
        """
        if len(trajectory) < 10:
            logger.warning("Trajectory too short for Lyapunov calculation")
            return 0.0

        n_points, n_dims = trajectory.shape
        max_iter = min(self.max_iter, n_points - 2)

        # 使用Rosenstein方法
        divergences = []

        for i in range(n_points - max_iter - 1):
            # 找到最近邻点
            current_point = trajectory[i]
            distances = np.linalg.norm(trajectory[i+1:] - current_point, axis=1)

            # 排除太近的点（时间上）
            valid_indices = np.where(np.arange(len(distances)) > 10)[0]
            if len(valid_indices) == 0:
                continue

            nearest_idx = valid_indices[np.argmin(distances[valid_indices])]
            nearest_idx += i + 1

            # 追踪发散
            local_divergences = []
            for j in range(1, max_iter):
                if i + j >= n_points or nearest_idx + j >= n_points:
                    break

                dist = np.linalg.norm(
                    trajectory[i + j] - trajectory[nearest_idx + j]
                )
                if dist > self.epsilon:
                    local_divergences.append(np.log(dist / self.epsilon))

            if local_divergences:
                divergences.extend(local_divergences)

        if not divergences:
            return 0.0

        # 线性拟合斜率即为Lyapunov指数
        x = np.arange(len(divergences))
        lyapunov = np.polyfit(x, divergences, 1)[0]

        logger.debug(f"Lyapunov exponent: {lyapunov:.4f}")
        return float(lyapunov)

    def is_attractor(self, lyapunov: float) -> bool:
        """判断是否收敛到吸引子

        Args:
            lyapunov: Lyapunov指数

        Returns:
            True if 收敛到吸引子（负指数）
        """
        threshold = Config.LYAPUNOV_THRESHOLD
        is_attr = lyapunov < threshold
        logger.debug(f"Attractor test: {lyapunov:.4f} < {threshold} = {is_attr}")
        return is_attr


class EffectiveInformation:
    """有效信息(EI)计算器

    量化宏观层级对微观层级的约束程度
    EI = H(macro) - H(micro|macro)
    """

    def __init__(self, n_bins: int = 10):
        """
        Args:
            n_bins: 离散化的bin数量
        """
        self.n_bins = n_bins
        logger.info(f"Effective Information calculator: n_bins={n_bins}")

    def calculate(
        self,
        micro_states: np.ndarray,
        macro_states: np.ndarray
    ) -> float:
        """计算有效信息

        Args:
            micro_states: 微观状态 (n_samples, n_features)
            macro_states: 宏观状态 (n_samples,) - 如聚类标签

        Returns:
            有效信息值 (0-1, 越大说明宏观约束越强)
        """
        if len(micro_states) != len(macro_states):
            logger.error("Micro and macro states length mismatch")
            return 0.0

        # 计算宏观熵 H(macro)
        macro_probs = self._get_probabilities(macro_states)
        h_macro = entropy(macro_probs)

        # 计算条件熵 H(micro|macro)
        h_micro_given_macro = 0.0
        unique_macros = np.unique(macro_states)

        for macro_val in unique_macros:
            # 获取该宏观状态下的微观状态
            mask = (macro_states == macro_val)
            micro_subset = micro_states[mask]

            if len(micro_subset) == 0:
                continue

            # 计算微观状态熵
            micro_discrete = self._discretize(micro_subset)
            micro_probs = self._get_probabilities(micro_discrete)
            h_micro = entropy(micro_probs)

            # 加权
            weight = np.sum(mask) / len(macro_states)
            h_micro_given_macro += weight * h_micro

        # 有效信息
        ei = h_macro - h_micro_given_macro
        ei_normalized = ei / (h_macro + 1e-10)  # 归一化到[0,1]

        logger.debug(f"Effective Information: {ei_normalized:.4f}")
        return max(0.0, min(1.0, ei_normalized))

    def _discretize(self, states: np.ndarray) -> np.ndarray:
        """将连续状态离散化"""
        if states.ndim == 1:
            states = states.reshape(-1, 1)

        discretized = np.zeros(len(states), dtype=int)

        for feat_idx in range(states.shape[1]):
            feat_values = states[:, feat_idx]
            bins = np.linspace(feat_values.min(), feat_values.max() + 1e-10, self.n_bins + 1)
            digitized = np.digitize(feat_values, bins) - 1
            digitized = np.clip(digitized, 0, self.n_bins - 1)

            # 组合多个特征的离散值
            discretized = discretized * self.n_bins + digitized

        return discretized

    def _get_probabilities(self, states: np.ndarray) -> np.ndarray:
        """计算状态概率分布"""
        unique, counts = np.unique(states, return_counts=True)
        probs = counts / len(states)
        return probs


class DownwardCausation:
    """向下因果检测器

    检测宏观层级对微观层级的约束作用
    """

    def __init__(self):
        self.ei_calculator = EffectiveInformation()
        logger.info("Downward causation detector initialized")

    def detect(
        self,
        trajectory: np.ndarray,
        macro_labels: Optional[np.ndarray] = None
    ) -> Tuple[bool, float, Dict[str, float]]:
        """检测向下因果

        Args:
            trajectory: 特征轨迹 (n_steps, n_features)
            macro_labels: 可选的宏观聚类标签

        Returns:
            (是否存在向下因果, 有效信息值, 详细指标)
        """
        if len(trajectory) < 5:
            return False, 0.0, {"ei": 0.0, "threshold": Config.EFFECTIVE_INFO_THRESHOLD}

        # 如果没有提供宏观标签，使用简单聚类
        if macro_labels is None:
            macro_labels = self._simple_clustering(trajectory)

        # 计算有效信息
        ei = self.ei_calculator.calculate(trajectory, macro_labels)

        # 计算额外指标
        metrics = {
            "ei": ei,
            "threshold": Config.EFFECTIVE_INFO_THRESHOLD,
            "n_macro_states": len(np.unique(macro_labels)),
            "trajectory_length": len(trajectory),
        }

        # 判断
        has_downward = ei > Config.EFFECTIVE_INFO_THRESHOLD

        logger.info(f"Downward causation: {has_downward}, EI={ei:.4f}")
        return has_downward, ei, metrics

    def _simple_clustering(self, trajectory: np.ndarray, k: int = 3) -> np.ndarray:
        """简单K近邻聚类"""
        if len(trajectory) < k:
            return np.zeros(len(trajectory), dtype=int)

        from sklearn.cluster import KMeans

        # 限制聚类数量
        k = min(k, len(trajectory))
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)

        try:
            labels = kmeans.fit_predict(trajectory)
            return labels
        except:
            return np.zeros(len(trajectory), dtype=int)


class EmergenceDetector:
    """真涌现检测器（统一接口）

    集成Takens嵌入、Lyapunov指数、有效信息、向下因果
    """

    def __init__(self):
        self.takens = TakensEmbedding(dimension=3, delay=1)
        self.lyapunov = LyapunovCalculator()
        self.downward = DownwardCausation()
        logger.info("Emergence detector initialized")

    def detect(
        self,
        feature_trajectory: List[List[float]],
        macro_labels: Optional[np.ndarray] = None
    ) -> Dict[str, any]:
        """检测真涌现

        Args:
            feature_trajectory: 特征演化轨迹 (代数, 特征维度)
            macro_labels: 可选的宏观标签

        Returns:
            检测结果字典
        """
        if len(feature_trajectory) < 5:
            logger.warning("Trajectory too short for emergence detection")
            return self._empty_result()

        # 转换为numpy数组
        trajectory = np.array(feature_trajectory)

        # === 1. 相空间重构 ===
        phase_space = self.takens.embed_multivariate(trajectory)

        if len(phase_space) == 0:
            logger.warning("Phase space embedding failed")
            return self._empty_result()

        # === 2. Lyapunov指数 ===
        lyapunov = self.lyapunov.calculate(phase_space)
        has_attractor = self.lyapunov.is_attractor(lyapunov)

        # === 3. 向下因果 ===
        has_downward, ei, dc_metrics = self.downward.detect(trajectory, macro_labels)

        # === 4. 真涌现判断 ===
        is_true_emergence = has_attractor and has_downward

        # === 5. 涌现强度 ===
        emergence_strength = self._calculate_strength(lyapunov, ei)

        result = {
            "is_true_emergence": is_true_emergence,
            "emergence_strength": emergence_strength,
            "has_attractor": has_attractor,
            "has_downward_causation": has_downward,
            "lyapunov_exponent": lyapunov,
            "effective_information": ei,
            "phase_space_shape": phase_space.shape,
            "trajectory_length": len(trajectory),
            "details": dc_metrics,
        }

        logger.info(
            f"Emergence detection: "
            f"true={is_true_emergence}, "
            f"strength={emergence_strength:.3f}, "
            f"lyapunov={lyapunov:.4f}, "
            f"EI={ei:.4f}"
        )

        return result

    def _calculate_strength(self, lyapunov: float, ei: float) -> float:
        """计算涌现强度 (0-1)

        综合Lyapunov指数和有效信息
        """
        # Lyapunov分量 (越负越好)
        lyap_strength = max(0, -lyapunov / abs(Config.LYAPUNOV_THRESHOLD))
        lyap_strength = min(lyap_strength, 1.0)

        # EI分量 (越高越好)
        ei_strength = ei / Config.EFFECTIVE_INFO_THRESHOLD
        ei_strength = min(ei_strength, 1.0)

        # 加权平均
        strength = 0.5 * lyap_strength + 0.5 * ei_strength
        return float(strength)

    def _empty_result(self) -> Dict[str, any]:
        """返回空结果"""
        return {
            "is_true_emergence": False,
            "emergence_strength": 0.0,
            "has_attractor": False,
            "has_downward_causation": False,
            "lyapunov_exponent": 0.0,
            "effective_information": 0.0,
            "phase_space_shape": (0, 0),
            "trajectory_length": 0,
            "details": {},
        }

    def analyze_trajectory(self, trajectory: List[List[float]]) -> Dict[str, any]:
        """分析轨迹特性（不判断涌现）

        返回轨迹的统计特性
        """
        if not trajectory:
            return {"error": "Empty trajectory"}

        trajectory = np.array(trajectory)

        # 基础统计
        mean_features = np.mean(trajectory, axis=0)
        std_features = np.std(trajectory, axis=0)

        # 趋势分析
        trends = []
        for feat_idx in range(trajectory.shape[1]):
            # 简单线性拟合
            x = np.arange(len(trajectory))
            slope = np.polyfit(x, trajectory[:, feat_idx], 1)[0]
            trends.append(float(slope))

        # 方差分析
        variance_ratio = np.var(trajectory, axis=0) / (np.mean(trajectory, axis=0) + 1e-10)

        return {
            "length": len(trajectory),
            "n_features": trajectory.shape[1],
            "mean_features": mean_features.tolist(),
            "std_features": std_features.tolist(),
            "trends": trends,
            "variance_ratio": variance_ratio.tolist(),
            "overall_variance": float(np.mean(np.var(trajectory, axis=0))),
        }
