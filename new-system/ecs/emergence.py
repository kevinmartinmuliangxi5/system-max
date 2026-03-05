"""
ECS - 涌现检测系统
基于信息论、复杂网络和观点动力学
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math

from .core.viewpoint import ViewpointSpace, DiscussionHistory, SystemPhase, EmergenceType


# ============================================================
# 涌现指标数据类
# ============================================================

@dataclass
class EmergenceMetrics:
    """涌现指标"""
    diversity: float = 0.0       # 多样性（Shannon熵）
    consensus: float = 0.0       # 共识度（相似度均值）
    novelty: float = 0.0         # 新颖度（语义距离）
    integration: float = 0.0     # 整合度（连接密度）
    synergy: float = 0.0         # 协同度（PID核心）
    dispersion: float = 0.0      # 观点离散度
    polarization: float = 0.0    # 极化程度
    connectivity: float = 0.0    # 连接密度
    emergence_score: float = 0.0 # 综合涌现强度

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "diversity": self.diversity,
            "consensus": self.consensus,
            "novelty": self.novelty,
            "integration": self.integration,
            "synergy": self.synergy,
            "dispersion": self.dispersion,
            "polarization": self.polarization,
            "connectivity": self.connectivity,
            "emergence_score": self.emergence_score
        }


@dataclass
class EmergenceReport:
    """涌现报告"""
    emergence_type: EmergenceType
    system_phase: SystemPhase
    metrics: EmergenceMetrics
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    description: str = ""
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "emergence_type": self.emergence_type.value,
            "system_phase": self.system_phase.value,
            "metrics": self.metrics.to_dict(),
            "timestamp": self.timestamp,
            "description": self.description,
            "insights": self.insights,
            "recommendations": self.recommendations
        }


# ============================================================
# 涌现检测器
# ============================================================

class EmergenceDetector:
    """
    涌现检测器

    基于多维度指标检测和分析涌现现象
    """

    def __init__(
        self,
        diversity_weight: float = 0.3,
        consensus_weight: float = 0.3,
        novelty_weight: float = 0.4,
        emergence_threshold: float = 0.7
    ):
        """
        初始化涌现检测器

        Args:
            diversity_weight: 多样性权重
            consensus_weight: 共识权重
            novelty_weight: 新颖度权重
            emergence_threshold: 涌现阈值
        """
        self.diversity_weight = diversity_weight
        self.consensus_weight = consensus_weight
        self.novelty_weight = novelty_weight
        self.emergence_threshold = emergence_threshold

        # 历史基线（用于计算新颖度）
        self._baseline_viewpoints: List[str] = []
        self._history: List[EmergenceReport] = []

    # ========================================================
    # 核心检测方法
    # ========================================================

    def detect(
        self,
        viewpoint_space: ViewpointSpace,
        round_num: int = 0,
        initial_viewpoints: List[str] = None
    ) -> EmergenceReport:
        """
        执行涌现检测

        Args:
            viewpoint_space: 观点空间
            round_num: 当前轮次
            initial_viewpoints: 初始观点（用于计算新颖度）

        Returns:
            涌现报告
        """
        # 1. 计算多维度指标
        metrics = self._calculate_all_metrics(viewpoint_space, initial_viewpoints)

        # 2. 计算综合涌现强度
        metrics.emergence_score = self._calculate_emergence_score(metrics)

        # 3. 分类涌现类型
        emergence_type = self._classify_emergence(metrics)

        # 4. 识别系统阶段
        system_phase = self._identify_phase(metrics)

        # 5. 生成洞察和建议
        description, insights, recommendations = self._generate_report_content(
            emergence_type, system_phase, metrics
        )

        # 6. 创建报告
        report = EmergenceReport(
            emergence_type=emergence_type,
            system_phase=system_phase,
            metrics=metrics,
            description=description,
            insights=insights,
            recommendations=recommendations
        )

        # 7. 更新历史
        self._history.append(report)

        return report

    # ========================================================
    # 指标计算
    # ========================================================

    def _calculate_all_metrics(
        self,
        viewpoint_space: ViewpointSpace,
        initial_viewpoints: List[str] = None
    ) -> EmergenceMetrics:
        """计算所有指标"""
        metrics = EmergenceMetrics()

        # 多样性：基于Shannon熵
        metrics.diversity = self._calculate_diversity(viewpoint_space)

        # 共识度：基于平均相似度
        metrics.consensus = self._calculate_consensus(viewpoint_space)

        # 新颖度：与初始观点的距离
        metrics.novelty = self._calculate_novelty(
            viewpoint_space, initial_viewpoints
        )

        # 整合度：基于观点连接密度
        metrics.integration = self._calculate_integration(viewpoint_space)

        # 协同度：PID核心指标
        metrics.synergy = self._calculate_synergy(
            metrics.diversity, metrics.integration, metrics.novelty
        )

        # 离散度
        metrics.dispersion = self._calculate_dispersion(viewpoint_space)

        # 极化度
        metrics.polarization = self._calculate_polarization(viewpoint_space)

        # 连接密度
        metrics.connectivity = self._calculate_connectivity(viewpoint_space)

        return metrics

    def _calculate_diversity(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算多样性（基于Shannon熵）

        多样性衡量观点的丰富程度和差异性
        """
        viewpoints = viewpoint_space.get_all_viewpoints()
        if len(viewpoints) < 2:
            return 0.0

        # 使用成对距离的分布计算熵
        distances = viewpoint_space.calculate_pairwise_distances()
        upper_tri = distances[np.triu_indices_from(distances, k=1)]

        if len(upper_tri) == 0:
            return 0.0

        # 计算距离的分布
        hist, _ = np.histogram(upper_tri, bins=20, range=(0, 1))
        prob = hist / len(upper_tri)
        prob = prob[prob > 0]

        # Shannon熵
        entropy = -np.sum(prob * np.log2(prob))

        # 归一化到0-1
        max_entropy = np.log2(20)
        return float(entropy / max_entropy)

    def _calculate_consensus(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算共识度

        共识度衡量群体观点的一致性程度
        """
        return viewpoint_space.get_consensus()

    def _calculate_novelty(
        self,
        viewpoint_space: ViewpointSpace,
        initial_viewpoints: List[str] = None
    ) -> float:
        """
        计算新颖度

        新颖度衡量当前观点相对于初始观点的创新程度
        """
        current_viewpoints = viewpoint_space.get_all_viewpoints()
        if not current_viewpoints:
            return 0.0

        if initial_viewpoints is None or len(initial_viewpoints) == 0:
            # 如果没有初始观点，使用历史基线
            if self._baseline_viewpoints:
                initial_viewpoints = self._baseline_viewpoints
            else:
                return 0.5  # 默认中等新颖度

        # 计算当前观点与初始观点的平均距离
        from .viewpoint import calculate_text_similarity

        distances = []
        for current_vp in current_viewpoints:
            max_distance = 0.0
            for init_vp in initial_viewpoints:
                # 距离 = 1 - 相似度
                distance = 1.0 - calculate_text_similarity(
                    current_vp.content, init_vp
                )
                max_distance = max(max_distance, distance)
            distances.append(max_distance)

        return float(np.mean(distances)) if distances else 0.0

    def _calculate_integration(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算整合度

        整合度衡量观点之间的关联程度
        """
        return viewpoint_space.get_connectivity()

    def _calculate_synergy(
        self,
        diversity: float,
        integration: float,
        novelty: float
    ) -> float:
        """
        计算协同度（PID核心）

        协同度是真涌现的核心指标，衡量协作产生的额外价值
        使用几何平均数：只有当三者都较高时，协同度才高
        """
        if diversity <= 0 or integration <= 0 or novelty <= 0:
            return 0.0

        # 几何平均数
        synergy = (diversity * integration * novelty) ** (1/3)
        return float(synergy)

    def _calculate_dispersion(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算观点离散度

        离散度衡量观点在空间中的分布程度
        """
        viewpoints = viewpoint_space.get_all_viewpoints()
        if len(viewpoints) < 2:
            return 0.0

        distances = viewpoint_space.calculate_pairwise_distances()
        upper_tri = distances[np.triu_indices_from(distances, k=1)]

        if len(upper_tri) == 0:
            return 0.0

        # 使用标准差作为离散度
        return float(np.std(upper_tri))

    def _calculate_polarization(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算极化度

        极化度衡量观点分裂成对立阵营的程度
        """
        return viewpoint_space.get_polarization()

    def _calculate_connectivity(self, viewpoint_space: ViewpointSpace) -> float:
        """
        计算连接密度

        连接密度衡量观点之间的连接紧密程度
        """
        return viewpoint_space.get_connectivity()

    # ========================================================
    # 涌现强度计算
    # ========================================================

    def _calculate_emergence_score(self, metrics: EmergenceMetrics) -> float:
        """
        计算综合涌现强度

        涌现强度 = 多样性权重 × 多样性
                 + 共识权重 × 共识度
                 + 新颖度权重 × 新颖度

        注意：这是一个加权和，而协同度（synergy）是乘积关系
        """
        score = (
            self.diversity_weight * metrics.diversity +
            self.consensus_weight * metrics.consensus +
            self.novelty_weight * metrics.novelty
        )
        return float(score)

    # ========================================================
    # 涌现类型分类
    # ========================================================

    def _classify_emergence(self, metrics: EmergenceMetrics) -> EmergenceType:
        """
        分类涌现类型

        基于多维度指标的组合进行分类
        """
        synergy = metrics.synergy
        novelty = metrics.novelty
        integration = metrics.integration
        diversity = metrics.diversity
        consensus = metrics.consensus

        # 元涌现：范式转移级别
        if synergy > 0.9 and novelty > 0.85:
            return EmergenceType.META_EMERGENCE

        # 创新涌现：突破性洞察
        if novelty > 0.8 and synergy > 0.7:
            return EmergenceType.INNOVATION

        # 协同涌现：深度观点整合
        if integration > 0.7 and synergy > 0.6:
            return EmergenceType.SYNERGY

        # 协调涌现：角色分工协作
        if diversity > 0.5 and consensus > 0.5 and integration > 0.4:
            return EmergenceType.COORDINATION

        # 聚合涌现：观点简单聚合
        return EmergenceType.AGGREGATION

    # ========================================================
    # 系统阶段识别
    # ========================================================

    def _identify_phase(self, metrics: EmergenceMetrics) -> SystemPhase:
        """
        识别系统所处阶段

        基于多样性和共识度的组合
        """
        diversity = metrics.diversity
        consensus = metrics.consensus

        # 停滞期：低多样性，低共识
        if diversity < 0.3 and consensus < 0.5:
            return SystemPhase.STAGNATION

        # 探索期：高多样性，低共识
        if diversity > 0.6 and consensus < 0.5:
            return SystemPhase.EXPLORATION

        # 辩论期：中等多样性，中等共识
        if 0.4 < diversity < 0.7 and 0.4 < consensus < 0.7:
            return SystemPhase.DEBATE

        # 收敛期：低多样性，高共识
        if diversity < 0.5 and consensus > 0.6:
            return SystemPhase.CONVERGENCE

        # 共识期：高共识
        if consensus > 0.75:
            return SystemPhase.CONSENSUS

        # 默认辩论期
        return SystemPhase.DEBATE

    # ========================================================
    # 报告生成
    # ========================================================

    def _generate_report_content(
        self,
        emergence_type: EmergenceType,
        system_phase: SystemPhase,
        metrics: EmergenceMetrics
    ) -> Tuple[str, List[str], List[str]]:
        """生成报告内容"""
        # 描述
        description = self._get_emergence_description(emergence_type, system_phase)

        # 洞察
        insights = self._generate_insights(emergence_type, system_phase, metrics)

        # 建议
        recommendations = self._generate_recommendations(
            emergence_type, system_phase, metrics
        )

        return description, insights, recommendations

    def _get_emergence_description(
        self,
        emergence_type: EmergenceType,
        system_phase: SystemPhase
    ) -> str:
        """获取涌现描述"""
        type_desc = {
            EmergenceType.AGGREGATION: "聚合涌现 - 观点简单聚合，尚未产生深度协作",
            EmergenceType.COORDINATION: "协调涌现 - 角色分工明确，开始有效协作",
            EmergenceType.SYNERGY: "协同涌现 - 深度观点整合，产生协同效应",
            EmergenceType.INNOVATION: "创新涌现 - 产生突破性洞察和创造性解决方案",
            EmergenceType.META_EMERGENCE: "元涌现 - 范式转移级别的涌现，超越原有框架"
        }

        phase_desc = {
            SystemPhase.EXPLORATION: "探索期 - 团队正在探索多种可能性",
            SystemPhase.DEBATE: "辩论期 - 观点碰撞，深度讨论中",
            SystemPhase.CONVERGENCE: "收敛期 - 观点趋向一致",
            SystemPhase.CONSENSUS: "共识期 - 达成高度共识",
            SystemPhase.STAGNATION: "停滞期 - 需要引入新视角打破僵局"
        }

        return f"{type_desc.get(emergence_type, '')}\n{phase_desc.get(system_phase, '')}"

    def _generate_insights(
        self,
        emergence_type: EmergenceType,
        system_phase: SystemPhase,
        metrics: EmergenceMetrics
    ) -> List[str]:
        """生成洞察"""
        insights = []

        # 基于涌现类型的洞察
        if emergence_type == EmergenceType.AGGREGATION:
            insights.append("当前主要是观点的简单聚合，尚未产生深度协作")
            insights.append("建议增加讨论轮次，促进观点深度碰撞")
        elif emergence_type == EmergenceType.COORDINATION:
            insights.append("角色分工明确，协作开始进入正轨")
            insights.append("不同视角正在被有效整合")
        elif emergence_type == EmergenceType.SYNERGY:
            insights.append("检测到深度观点整合，产生协同效应")
            insights.append("团队智慧开始超越个体之和")
        elif emergence_type == EmergenceType.INNOVATION:
            insights.append("发现突破性洞察！产生了创新性解决方案")
            insights.append("这是真涌现的典型特征")
        elif emergence_type == EmergenceType.META_EMERGENCE:
            insights.append("检测到范式转移级别的涌现！")
            insights.append("这是最高层次的真涌现，超越了原有框架")

        # 基于指标的洞察
        if metrics.synergy > 0.7:
            insights.append(f"协同度极高({metrics.synergy:.2f})，表明产生了真涌现")
        if metrics.novelty > 0.7:
            insights.append(f"新颖度高({metrics.novelty:.2f})，发现了突破性想法")
        if metrics.polarization > 0.6:
            insights.append(f"警告：极化度较高({metrics.polarization:.2f})，观点可能分裂")

        return insights

    def _generate_recommendations(
        self,
        emergence_type: EmergenceType,
        system_phase: SystemPhase,
        metrics: EmergenceMetrics
    ) -> List[str]:
        """生成建议"""
        recommendations = []

        # 基于系统阶段的建议
        if system_phase == SystemPhase.EXPLORATION:
            recommendations.append("继续探索，鼓励更多样化的观点")
        elif system_phase == SystemPhase.DEBATE:
            recommendations.append("促进深度讨论，鼓励观点碰撞")
        elif system_phase == SystemPhase.CONVERGENCE:
            recommendations.append("准备形成共识，整合最终方案")
        elif system_phase == SystemPhase.CONSENSUS:
            recommendations.append("达成共识，可以开始执行阶段")
        elif system_phase == SystemPhase.STAGNATION:
            recommendations.append("警告：进入停滞期")
            recommendations.append("建议引入新视角或新角色打破僵局")

        # 基于指标的建议
        if metrics.diversity < 0.3:
            recommendations.append("多样性不足，建议增加更多不同视角")
        if metrics.consensus < 0.4 and system_phase != SystemPhase.EXPLORATION:
            recommendations.append("共识度较低，需要继续讨论")
        if metrics.integration < 0.4:
            recommendations.append("整合度不足，观点之间缺乏有效连接")
        if metrics.polarization > 0.6:
            recommendations.append("极化度高，需要调解对立观点")

        # 基于涌现类型的建议
        if emergence_type == EmergenceType.AGGREGATION:
            recommendations.append("增加讨论深度，追求协同涌现")
        elif emergence_type in [EmergenceType.SYNERGY, EmergenceType.INNOVATION]:
            recommendations.append("真涌现已产生，可以准备输出结果")

        return recommendations

    # ========================================================
    # 历史管理
    # ========================================================

    def set_baseline(self, viewpoints: List[str]):
        """设置基线观点（用于计算新颖度）"""
        self._baseline_viewpoints = viewpoints

    def get_history(self) -> List[EmergenceReport]:
        """获取历史报告"""
        return self._history

    def get_trend(self) -> Dict[str, Any]:
        """获取涌现趋势"""
        if len(self._history) < 2:
            return {"trend": "insufficient_data"}

        recent = self._history[-5:]  # 最近5个报告

        emergence_scores = [r.metrics.emergence_score for r in recent]
        synergy_scores = [r.metrics.synergy for r in recent]

        # 计算趋势
        if len(emergence_scores) >= 2:
            score_change = emergence_scores[-1] - emergence_scores[0]
            synergy_change = synergy_scores[-1] - synergy_scores[0]

            return {
                "trend": "improving" if score_change > 0.1 else "stable" if abs(score_change) < 0.1 else "declining",
                "emergence_score_change": float(score_change),
                "synergy_change": float(synergy_change),
                "latest_emergence_type": recent[-1].emergence_type.value,
                "latest_phase": recent[-1].system_phase.value
            }

        return {"trend": "insufficient_data"}

    # ========================================================
    # 关键词检测（辅助方法）
    # ========================================================

    @staticmethod
    def detect_emergence_keywords(content: str) -> List[str]:
        """
        检测内容中的涌现关键词

        Args:
            content: 要检测的内容

        Returns:
            匹配的关键词列表
        """
        keywords = [
            "新想法", "突然想到", "更好的方案", "结合",
            "创新", "改进", "优化", "综合", "突破",
            "换个角度", "重新考虑", "发现", "启发",
            "insight", "breakthrough", "novel", "innovative",
            "realize", "aha", "epiphany", "组合", "融合"
        ]

        matched = []
        content_lower = content.lower()
        for keyword in keywords:
            if keyword.lower() in content_lower:
                matched.append(keyword)

        return matched


# ============================================================
# 工厂函数
# ============================================================

def create_emergence_detector(
    diversity_weight: float = 0.3,
    consensus_weight: float = 0.3,
    novelty_weight: float = 0.4,
    emergence_threshold: float = 0.7
) -> EmergenceDetector:
    """创建涌现检测器"""
    return EmergenceDetector(
        diversity_weight=diversity_weight,
        consensus_weight=consensus_weight,
        novelty_weight=novelty_weight,
        emergence_threshold=emergence_threshold
    )


# 导出
__all__ = [
    "EmergenceType",
    "SystemPhase",
    "EmergenceMetrics",
    "EmergenceReport",
    "EmergenceDetector",
    "create_emergence_detector"
]
