"""
Recommender - 智能推荐引擎模块
==============================

基于用户需求和上下文，智能推荐最合适的UI组件、主题和布局。

子模块:
    - rules: 推荐规则矩阵定义
    - engine: 增强版智能推荐引擎

推荐依据:
    - 行业匹配度
    - 框架兼容性
    - 使用频率
    - 用户评分
    - 组件相似度
    - 氛围匹配
    - 复杂度适配
    - 无障碍性
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# 原有推荐策略枚举（向后兼容）
# ============================================================================

class RecommendationStrategy(Enum):
    """推荐策略"""
    BALANCED = "balanced"           # 均衡策略
    INDUSTRY_FOCUSED = "industry"   # 行业优先
    PERFORMANCE = "performance"     # 性能优先
    POPULARITY = "popularity"       # 热度优先
    CUSTOM = "custom"               # 自定义权重


# ============================================================================
# 原有推荐结果数据类（向后兼容）
# ============================================================================

@dataclass
class RecommendationResult:
    """
    推荐结果（原有版本，向后兼容）

    Attributes:
        component_id: 组件ID
        component_name: 组件名称
        score: 推荐得分 (0-1)
        reasons: 推荐理由列表
        match_details: 匹配详情
    """
    component_id: str
    component_name: str
    score: float
    reasons: List[str] = field(default_factory=list)
    match_details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "component_id": self.component_id,
            "component_name": self.component_name,
            "score": round(self.score, 3),
            "reasons": self.reasons,
            "match_details": self.match_details,
        }


@dataclass
class RecommendationRequest:
    """
    推荐请求（原有版本，向后兼容）

    Attributes:
        framework: 前端框架
        industry: 行业类型
        category: 组件分类
        keywords: 关键词列表
        strategy: 推荐策略
        max_results: 最大结果数
        threshold: 推荐阈值
    """
    framework: str = "react"
    industry: str = "general"
    category: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    strategy: RecommendationStrategy = RecommendationStrategy.BALANCED
    max_results: int = 10
    threshold: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "framework": self.framework,
            "industry": self.industry,
            "category": self.category,
            "keywords": self.keywords,
            "strategy": self.strategy.value,
            "max_results": self.max_results,
            "threshold": self.threshold,
        }


# ============================================================================
# 原有推荐引擎（向后兼容）
# ============================================================================

class RecommenderEngine:
    """
    UI组件推荐引擎（原有版本，向后兼容）

    基于多维度评分，智能推荐最合适的组件
    """

    # 默认权重配置
    DEFAULT_WEIGHTS = {
        RecommendationStrategy.BALANCED: {
            "industry_match": 0.4,
            "framework_compatibility": 0.3,
            "usage_frequency": 0.2,
            "user_rating": 0.1,
        },
        RecommendationStrategy.INDUSTRY_FOCUSED: {
            "industry_match": 0.6,
            "framework_compatibility": 0.2,
            "usage_frequency": 0.1,
            "user_rating": 0.1,
        },
        RecommendationStrategy.PERFORMANCE: {
            "industry_match": 0.2,
            "framework_compatibility": 0.5,
            "usage_frequency": 0.2,
            "user_rating": 0.1,
        },
        RecommendationStrategy.POPULARITY: {
            "industry_match": 0.2,
            "framework_compatibility": 0.2,
            "usage_frequency": 0.5,
            "user_rating": 0.1,
        },
    }

    def __init__(self):
        self._component_db: Dict[str, Dict[str, Any]] = {}
        self._initialize_component_db()

    def _initialize_component_db(self):
        """初始化组件数据库"""
        self._component_db = {
            # === Form Components ===
            "input": {
                "id": "input",
                "name": "输入框",
                "category": "form",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "healthcare", "finance", "ecommerce", "education", "manufacturing"],
                "usage_frequency": 0.95,
                "user_rating": 4.5,
                "tags": ["input", "form", "text"],
            },
            "select": {
                "id": "select",
                "name": "下拉选择器",
                "category": "form",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "healthcare", "finance", "ecommerce", "education", "manufacturing"],
                "usage_frequency": 0.85,
                "user_rating": 4.3,
                "tags": ["select", "dropdown", "choice"],
            },
            "datepicker": {
                "id": "datepicker",
                "name": "日期选择器",
                "category": "form",
                "frameworks": ["react", "vue"],
                "industries": ["general", "healthcare", "finance", "ecommerce"],
                "usage_frequency": 0.75,
                "user_rating": 4.2,
                "tags": ["date", "picker", "calendar"],
            },
            "autocomplete": {
                "id": "autocomplete",
                "name": "自动完成",
                "category": "form",
                "frameworks": ["react", "vue"],
                "industries": ["general", "ecommerce", "healthcare"],
                "usage_frequency": 0.65,
                "user_rating": 4.4,
                "tags": ["autocomplete", "suggest", "input"],
            },
            # === Data Components ===
            "table": {
                "id": "table",
                "name": "表格",
                "category": "data",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "finance", "manufacturing"],
                "usage_frequency": 0.90,
                "user_rating": 4.4,
                "tags": ["table", "grid", "data"],
            },
            "chart": {
                "id": "chart",
                "name": "图表",
                "category": "data",
                "frameworks": ["react", "vue"],
                "industries": ["finance", "healthcare", "manufacturing"],
                "usage_frequency": 0.70,
                "user_rating": 4.6,
                "tags": ["chart", "graph", "visualization"],
            },
            "card": {
                "id": "card",
                "name": "卡片",
                "category": "data",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "ecommerce", "education"],
                "usage_frequency": 0.85,
                "user_rating": 4.5,
                "tags": ["card", "container", "content"],
            },
            # === Navigation Components ===
            "menu": {
                "id": "menu",
                "name": "菜单",
                "category": "navigation",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "ecommerce", "education"],
                "usage_frequency": 0.95,
                "user_rating": 4.3,
                "tags": ["menu", "nav", "links"],
            },
            "breadcrumb": {
                "id": "breadcrumb",
                "name": "面包屑",
                "category": "navigation",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "ecommerce", "education"],
                "usage_frequency": 0.60,
                "user_rating": 4.1,
                "tags": ["breadcrumb", "nav", "path"],
            },
            "tabs": {
                "id": "tabs",
                "name": "标签页",
                "category": "navigation",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "healthcare", "education"],
                "usage_frequency": 0.80,
                "user_rating": 4.4,
                "tags": ["tabs", "switch", "panel"],
            },
            # === Feedback Components ===
            "modal": {
                "id": "modal",
                "name": "模态对话框",
                "category": "feedback",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "healthcare", "finance", "ecommerce"],
                "usage_frequency": 0.85,
                "user_rating": 4.2,
                "tags": ["modal", "dialog", "popup"],
            },
            "toast": {
                "id": "toast",
                "name": "消息提示",
                "category": "feedback",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "ecommerce", "finance"],
                "usage_frequency": 0.90,
                "user_rating": 4.5,
                "tags": ["toast", "notification", "alert"],
            },
            "loading": {
                "id": "loading",
                "name": "加载状态",
                "category": "feedback",
                "frameworks": ["react", "vue", "vanilla"],
                "industries": ["general", "healthcare", "finance"],
                "usage_frequency": 0.95,
                "user_rating": 4.3,
                "tags": ["loading", "spinner", "skeleton"],
            },
        }

    def recommend(
        self,
        request: RecommendationRequest
    ) -> List[RecommendationResult]:
        """
        生成推荐结果

        Args:
            request: 推荐请求

        Returns:
            推荐结果列表（按得分降序）
        """
        # 获取权重配置
        weights = self._get_weights(request.strategy)

        # 计算每个组件的得分
        results = []
        for component_id, component_data in self._component_db.items():
            # 过滤条件
            if request.category and component_data["category"] != request.category:
                continue

            if request.framework not in component_data["frameworks"]:
                continue

            # 计算得分
            score, details = self._calculate_score(component_data, request, weights)

            # 过滤低分结果
            if score < request.threshold:
                continue

            # 生成推荐理由
            reasons = self._generate_reasons(component_data, details, request)

            results.append(RecommendationResult(
                component_id=component_id,
                component_name=component_data["name"],
                score=score,
                reasons=reasons,
                match_details=details,
            ))

        # 按得分排序并限制结果数量
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:request.max_results]

    def _get_weights(self, strategy: RecommendationStrategy) -> Dict[str, float]:
        """获取策略权重"""
        if strategy == RecommendationStrategy.CUSTOM:
            return self.DEFAULT_WEIGHTS[RecommendationStrategy.BALANCED]
        return self.DEFAULT_WEIGHTS.get(
            strategy,
            self.DEFAULT_WEIGHTS[RecommendationStrategy.BALANCED]
        )

    def _calculate_score(
        self,
        component: Dict[str, Any],
        request: RecommendationRequest,
        weights: Dict[str, float]
    ) -> Tuple[float, Dict[str, Any]]:
        """计算组件推荐得分"""
        scores = {}
        details = {}

        # 1. 行业匹配度
        industry_match = 1.0 if request.industry in component["industries"] else 0.3
        scores["industry_match"] = industry_match * weights["industry_match"]
        details["industry_match"] = industry_match

        # 2. 框架兼容性
        framework_match = 1.0 if request.framework in component["frameworks"] else 0.0
        scores["framework_compatibility"] = framework_match * weights["framework_compatibility"]
        details["framework_compatibility"] = framework_match

        # 3. 使用频率
        usage_score = component["usage_frequency"]
        scores["usage_frequency"] = usage_score * weights["usage_frequency"]
        details["usage_frequency"] = usage_score

        # 4. 用户评分
        rating_score = component["user_rating"] / 5.0
        scores["user_rating"] = rating_score * weights["user_rating"]
        details["user_rating"] = rating_score

        # 5. 关键词匹配（额外加分）
        keyword_bonus = 0.0
        if request.keywords:
            matches = sum(
                1 for kw in request.keywords
                if kw.lower() in str(component.get("tags", [])).lower()
            )
            keyword_bonus = (matches / len(request.keywords)) * 0.1
        details["keyword_bonus"] = keyword_bonus

        # 总分
        total_score = sum(scores.values()) + keyword_bonus

        return min(total_score, 1.0), details

    def _generate_reasons(
        self,
        component: Dict[str, Any],
        details: Dict[str, Any],
        request: RecommendationRequest
    ) -> List[str]:
        """生成推荐理由"""
        reasons = []

        if details.get("industry_match", 0) >= 0.8:
            reasons.append(f"与 {request.industry} 行业高度匹配")

        if details.get("framework_compatibility", 0) >= 0.8:
            reasons.append(f"完美支持 {request.framework} 框架")

        if details.get("usage_frequency", 0) >= 0.8:
            reasons.append("使用频率高，社区验证充分")

        if details.get("user_rating", 0) >= 0.85:
            reasons.append(f"用户评分 {component['user_rating']} 分，口碑良好")

        if details.get("keyword_bonus", 0) > 0:
            reasons.append("与搜索关键词高度相关")

        return reasons

    def get_component(self, component_id: str) -> Optional[Dict[str, Any]]:
        """获取组件详情"""
        return self._component_db.get(component_id)

    def list_components(
        self,
        category: Optional[str] = None,
        framework: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """列出组件"""
        results = []
        for component in self._component_db.values():
            if category and component["category"] != category:
                continue
            if framework and framework not in component["frameworks"]:
                continue
            results.append(component)
        return results


# ============================================================================
# 全局引擎实例（原有版本，向后兼容）
# ============================================================================

_default_engine: Optional[RecommenderEngine] = None


def get_recommender_engine() -> RecommenderEngine:
    """
    获取全局推荐引擎（单例模式，原有版本，向后兼容）

    Returns:
        RecommenderEngine 实例
    """
    global _default_engine
    if _default_engine is None:
        _default_engine = RecommenderEngine()
    return _default_engine


# ============================================================================
# 便捷函数（原有版本，向后兼容）
# ============================================================================

def recommend(
    framework: str = "react",
    industry: str = "general",
    category: Optional[str] = None,
    keywords: List[str] = None,
    strategy: RecommendationStrategy = RecommendationStrategy.BALANCED,
    max_results: int = 10
) -> List[RecommendationResult]:
    """
    推荐组件的便捷函数

    Args:
        framework: 前端框架
        industry: 行业类型
        category: 组件分类
        keywords: 关键词列表
        strategy: 推荐策略
        max_results: 最大结果数

    Returns:
        推荐结果列表
    """
    request = RecommendationRequest(
        framework=framework,
        industry=industry,
        category=category,
        keywords=keywords or [],
        strategy=strategy,
        max_results=max_results,
    )
    engine = get_recommender_engine()
    return engine.recommend(request)


def search_components(
    keyword: str,
    framework: str = "react"
) -> List[Dict[str, Any]]:
    """
    搜索组件的便捷函数

    Args:
        keyword: 搜索关键词
        framework: 前端框架

    Returns:
        匹配的组件列表
    """
    engine = get_recommender_engine()
    all_components = engine.list_components(framework=framework)

    keyword_lower = keyword.lower()
    results = []
    for component in all_components:
        if (keyword_lower in component["name"].lower() or
            keyword_lower in component["id"].lower() or
            any(keyword_lower in tag.lower() for tag in component.get("tags", []))):
            results.append(component)
    return results


# ============================================================================
# 导入新模块
# ============================================================================

# 导入规则模块
from .rules import (
    # 规则类型
    RuleType,
    Mood,
    Complexity,
    UserLevel,
    TimeContext,
    # 规则权重
    RuleWeights,
    # 规则引擎
    RuleEngine,
    # 规则矩阵常量
    INDUSTRY_COMPONENT_MATRIX,
    USE_CASE_LAYOUT_RULES,
    MOOD_THEME_MAPPING,
    COMPLEXITY_COMPONENT_RULES,
    COMPLEXITY_COMPONENT_PREFERENCE,
    ACCESSIBILITY_SCORES,
    ACCESSIBILITY_THRESHOLDS,
    FRAMEWORK_COMPATIBILITY,
    USER_LEVEL_LAYOUT_COMPLEXITY,
    COMPONENT_COMBINATIONS,
    TIME_THEME_MAPPING,
)

# 导入增强引擎模块
from .engine import (
    # 推荐结果数据类
    ComponentRecommendation,
    ThemeRecommendation,
    LayoutRecommendation,
    RecommendationRequest as EnhancedRecommendationRequest,
    RecommendationResult as EnhancedRecommendationResult,
    UserFeedback,
    # 增强引擎类
    RecommenderEngine as EnhancedRecommenderEngine,
    get_recommender_engine as get_enhanced_recommender_engine,
    # 便捷函数
    recommend_components,
    recommend_theme,
    recommend_layout,
)


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # ===== 原有导出（向后兼容） =====
    # 枚举
    "RecommendationStrategy",
    # 数据类
    "RecommendationResult",
    "RecommendationRequest",
    # 引擎
    "RecommenderEngine",
    "get_recommender_engine",
    # 便捷函数
    "recommend",
    "search_components",

    # ===== 新增：规则模块 =====
    # 规则类型
    "RuleType",
    "Mood",
    "Complexity",
    "UserLevel",
    "TimeContext",
    # 规则权重
    "RuleWeights",
    # 规则引擎
    "RuleEngine",
    # 规则矩阵常量
    "INDUSTRY_COMPONENT_MATRIX",
    "USE_CASE_LAYOUT_RULES",
    "MOOD_THEME_MAPPING",
    "COMPLEXITY_COMPONENT_RULES",
    "COMPLEXITY_COMPONENT_PREFERENCE",
    "ACCESSIBILITY_SCORES",
    "ACCESSIBILITY_THRESHOLDS",
    "FRAMEWORK_COMPATIBILITY",
    "USER_LEVEL_LAYOUT_COMPLEXITY",
    "COMPONENT_COMBINATIONS",
    "TIME_THEME_MAPPING",

    # ===== 新增：增强引擎模块 =====
    # 推荐结果数据类
    "ComponentRecommendation",
    "ThemeRecommendation",
    "LayoutRecommendation",
    "EnhancedRecommendationRequest",
    "EnhancedRecommendationResult",
    "UserFeedback",
    # 增强引擎类
    "EnhancedRecommenderEngine",
    "get_enhanced_recommender_engine",
    # 便捷函数
    "recommend_components",
    "recommend_theme",
    "recommend_layout",
]
