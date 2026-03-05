"""
Recommender Engine - 智能推荐引擎
==================================

增强版推荐引擎，基于多维度规则和用户偏好学习提供智能推荐。

核心功能:
    - recommend_components(): 根据场景推荐组件组合 (Top 3)
    - recommend_theme(): 根据行业和氛围推荐主题 (Top 3)
    - recommend_layout(): 根据用例和用户水平推荐布局
    - learn_from_feedback(): 从用户选择中学习偏好
    - get_recommendations(): 获取完整推荐方案

特性:
    - 多维度评分（行业匹配、框架兼容、复杂度适配、无障碍性）
    - 用户偏好学习（基于历史选择调整权重）
    - 规则引擎集成
    - Top-N 推荐（返回最佳3个选项）
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path

# 导入规则模块
from .rules import (
    RuleEngine,
    RuleWeights,
    RuleType,
    Mood,
    Complexity,
    UserLevel,
    TimeContext,
)

# 导入主题定义
from ..themes.definitions import (
    Theme,
    ThemeMode,
    ThemeCategory,
    THEME_REGISTRY,
    get_theme,
)

# 导入组件定义
from ..components.large import LARGE_COMPONENTS
from ..components.medium import MEDIUM_COMPONENTS


# ============================================================================
# 推荐结果数据类
# ============================================================================

@dataclass
class ComponentRecommendation:
    """组件推荐结果"""
    component_id: str
    component_name: str
    score: float
    reason: str
    category: str
    is_composable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component_id": self.component_id,
            "component_name": self.component_name,
            "score": self.score,
            "reason": self.reason,
            "category": self.category,
            "is_composable": self.is_composable,
        }


@dataclass
class ThemeRecommendation:
    """主题推荐结果"""
    theme_id: str
    theme_name: str
    score: float
    reason: str
    mode: str
    category: str
    preview_colors: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "theme_id": self.theme_id,
            "theme_name": self.theme_name,
            "score": self.score,
            "reason": self.reason,
            "mode": self.mode,
            "category": self.category,
            "preview_colors": self.preview_colors,
        }


@dataclass
class LayoutRecommendation:
    """布局推荐结果"""
    layout_id: str
    layout_name: str
    score: float
    reason: str
    component_count_range: Tuple[int, int]
    suggested_components: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layout_id": self.layout_id,
            "layout_name": self.layout_name,
            "score": self.score,
            "reason": self.reason,
            "component_count_range": self.component_count_range,
            "suggested_components": self.suggested_components,
        }


@dataclass
class RecommendationRequest:
    """推荐请求"""
    industry: str
    use_case: str
    framework: str = "streamlit"
    complexity: Complexity = Complexity.MODERATE
    mood: Optional[Mood] = None
    user_level: UserLevel = UserLevel.INTERMEDIATE
    require_accessibility: bool = False
    target_audience: Optional[str] = None
    custom_constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecommendationResult:
    """完整推荐结果"""
    components: List[ComponentRecommendation]
    themes: List[ThemeRecommendation]
    layouts: List[LayoutRecommendation]
    request: RecommendationRequest
    confidence_score: float
    alternatives: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "components": [c.to_dict() for c in self.components],
            "themes": [t.to_dict() for t in self.themes],
            "layouts": [l.to_dict() for l in self.layouts],
            "request": {
                "industry": self.request.industry,
                "use_case": self.request.use_case,
                "framework": self.request.framework,
                "complexity": self.request.complexity.value,
                "mood": self.request.mood.value if self.request.mood else None,
                "user_level": self.request.user_level.value,
                "require_accessibility": self.request.require_accessibility,
            },
            "confidence_score": self.confidence_score,
            "alternatives": self.alternatives,
        }


@dataclass
class UserFeedback:
    """用户反馈数据"""
    selected_recommendation: str
    recommendation_type: str  # "component", "theme", "layout"
    context: RecommendationRequest
    rating: Optional[int] = None  # 1-5
    alternative_selected: Optional[str] = None
    timestamp: str = ""


# ============================================================================
# 推荐引擎类
# ============================================================================

class RecommenderEngine:
    """
    智能推荐引擎

    基于规则引擎和用户偏好学习提供智能推荐
    """

    def __init__(
        self,
        weights: Optional[RuleWeights] = None,
        history_file: Optional[str] = None
    ):
        """
        初始化推荐引擎

        Args:
            weights: 规则权重配置
            history_file: 用户历史记录文件路径
        """
        self.rule_engine = RuleEngine(weights)
        self._history: List[UserFeedback] = []
        self._history_file = history_file
        self._selection_counts: Dict[str, int] = {}
        self._load_history()

    # ========================================================================
    # 组件推荐
    # ========================================================================

    def recommend_components(
        self,
        industry: str,
        use_case: str,
        complexity: Complexity = Complexity.MODERATE,
        framework: str = "streamlit",
        accessibility: bool = False,
        top_n: int = 3
    ) -> List[ComponentRecommendation]:
        """
        根据行业和用例推荐组件组合

        Args:
            industry: 行业ID (government, finance, healthcare, ecommerce, education, technology)
            use_case: 用例ID (data_visualization, user_management, content_consumption, etc.)
            complexity: 复杂度
            framework: 目标框架
            accessibility: 是否要求高无障碍性
            top_n: 返回前N个推荐

        Returns:
            组件推荐列表（Top N）
        """
        # 获取组件数量范围
        min_count, max_count = self.rule_engine.get_complexity_range(complexity)

        # 收集所有可用组件
        all_components = []

        # 添加大型组件
        for comp in LARGE_COMPONENTS:
            all_components.append({
                "id": comp.id,
                "name": comp.name,
                "category": comp.category.value,
                "is_composable": False,
            })

        # 添加中型可组合组件
        for comp in MEDIUM_COMPONENTS:
            all_components.append({
                "id": comp.id,
                "name": comp.name,
                "category": comp.category.value,
                "is_composable": getattr(comp, 'composable', True),
            })

        # 评分和筛选
        scored_components = []

        for comp in all_components:
            # 计算综合得分
            score = self.rule_engine.calculate_component_score(
                comp["id"],
                industry,
                framework,
                complexity,
                accessibility
            )

            # 应用无障碍筛选
            if accessibility:
                a11y_score = self.rule_engine.get_accessibility_score(comp["id"])
                if a11y_score < 0.7:
                    continue

            # 应用复杂度数量限制
            if complexity in [Complexity.MINIMAL, Complexity.SIMPLE]:
                # 简单场景优先选择中型组件
                if comp["is_composable"]:
                    score *= 1.1

            scored_components.append({
                **comp,
                "score": score,
            })

        # 按得分排序
        scored_components.sort(key=lambda x: x["score"], reverse=True)

        # 生成推荐结果
        recommendations = []

        # 获取预设组合
        combinations = self.rule_engine.get_component_combinations(industry)
        if combinations and len(combinations) > 0:
            # 使用行业预设组合
            for combo in combinations[:top_n]:
                for comp_id in combo:
                    comp_data = next((c for c in scored_components if c["id"] == comp_id), None)
                    if comp_data:
                        recommendations.append(ComponentRecommendation(
                            component_id=comp_data["id"],
                            component_name=comp_data["name"],
                            score=comp_data["score"],
                            reason=f"适合{industry}行业的{use_case}场景",
                            category=comp_data["category"],
                            is_composable=comp_data["is_composable"],
                        ))
        else:
            # 使用评分最高的组件
            for comp in scored_components[:top_n]:
                recommendations.append(ComponentRecommendation(
                    component_id=comp["id"],
                    component_name=comp["name"],
                    score=comp["score"],
                    reason=f"综合评分{comp['score']:.2f}，适合{industry}行业",
                    category=comp["category"],
                    is_composable=comp["is_composable"],
                ))

        # 记录选择频率
        for rec in recommendations:
            self._selection_counts[rec.component_id] = \
                self._selection_counts.get(rec.component_id, 0) + 1

        return recommendations

    # ========================================================================
    # 主题推荐
    # ========================================================================

    def recommend_theme(
        self,
        industry: str,
        mood: Mood,
        accessibility: bool = False,
        time_context: Optional[TimeContext] = None,
        top_n: int = 3
    ) -> List[ThemeRecommendation]:
        """
        根据行业和氛围推荐主题（Top 3）

        Args:
            industry: 行业ID
            mood: 氛围/情绪
            accessibility: 是否要求高无障碍性
            time_context: 时间情境
            top_n: 返回前N个推荐

        Returns:
            主题推荐列表（Top N）
        """
        recommendations = []
        scored_themes = []

        # 获取所有主题
        all_themes = list(THEME_REGISTRY.values())

        for theme in all_themes:
            score = 0.0
            reasons = []

            # 1. 氛围匹配得分
            mood_scores = self.rule_engine.get_mood_theme_scores(mood)
            mood_score = next((s for t, s in mood_scores if t == theme.id), 0.0)
            score += mood_score * 0.4
            if mood_score > 0.8:
                reasons.append(f"完美契合{mood.value}氛围")

            # 2. 行业适配得分
            industry_theme_map = {
                "government": ["corporate_gray", "default_dark", "midnight_blue"],
                "finance": ["corporate_gray", "ocean_blue", "midnight_blue"],
                "healthcare": ["cool_mint", "ocean_blue", "forest_green"],
                "ecommerce": ["sunset_orange", "berry_purple", "rose_gold"],
                "education": ["forest_green", "warm_earth", "spring_blossom"],
                "technology": ["tech_neon", "ocean_blue", "default_dark"],
            }

            if industry in industry_theme_map:
                if theme.id in industry_theme_map[industry]:
                    score += 0.3
                    reasons.append(f"适合{industry}行业")

            # 3. 无障碍性得分
            if accessibility:
                # 深色主题对比度通常更好
                if theme.mode == ThemeMode.DARK:
                    score += 0.15
                    reasons.append("高对比度，利于无障碍访问")
                else:
                    score += 0.05

            # 4. 时间情境加分
            if time_context:
                time_themes = self.rule_engine.get_time_based_themes(time_context)
                if theme.id in time_themes:
                    score += 0.15
                    reasons.append("符合当前时间情境")

            # 5. 历史选择加分（用户偏好学习）
            selection_count = self._selection_counts.get(f"theme_{theme.id}", 0)
            if selection_count > 0:
                score += min(selection_count * 0.02, 0.1)  # 最多加0.1

            scored_themes.append({
                "theme": theme,
                "score": score,
                "reasons": reasons,
            })

        # 按得分排序
        scored_themes.sort(key=lambda x: x["score"], reverse=True)

        # 生成推荐结果（Top N）
        for item in scored_themes[:top_n]:
            theme = item["theme"]
            recommendations.append(ThemeRecommendation(
                theme_id=theme.id,
                theme_name=theme.name,
                score=item["score"],
                reason="; ".join(item["reasons"]) if item["reasons"] else "综合推荐",
                mode=theme.mode.value,
                category=theme.category.value,
                preview_colors={
                    "primary": theme.colors.primary,
                    "background": theme.colors.background,
                    "surface": theme.colors.surface,
                    "text": theme.colors.text,
                }
            ))

        return recommendations

    # ========================================================================
    # 布局推荐
    # ========================================================================

    def recommend_layout(
        self,
        content_type: str,
        user_level: UserLevel = UserLevel.INTERMEDIATE,
        complexity: Optional[Complexity] = None,
        top_n: int = 3
    ) -> List[LayoutRecommendation]:
        """
        推荐布局模式

        Args:
            content_type: 内容类型/用例
            user_level: 用户水平
            complexity: 复杂度（可选）
            top_n: 返回前N个推荐

        Returns:
            布局推荐列表
        """
        recommendations = []

        # 获取用例对应的布局列表
        layout_scores = self.rule_engine.get_use_case_layouts(content_type)

        if not layout_scores:
            # 没有特定布局规则，返回通用推荐
            layout_scores = [
                ("dashboard_grid", 0.8),
                ("split_view", 0.7),
                ("card_grid", 0.6),
            ]

        # 根据用户水平过滤复杂度
        allowed_complexities = USER_LEVEL_LAYOUT_COMPLEXITY.get(user_level, [Complexity.MODERATE])

        for layout_id, base_score in layout_scores[:top_n]:
            # 确定布局复杂度
            layout_complexity = self._infer_layout_complexity(layout_id)
            complexity_obj = complexity or layout_complexity

            # 检查用户水平是否匹配
            if complexity_obj not in allowed_complexities:
                # 降低得分但不完全排除
                adjusted_score = base_score * 0.7
                reason = f"布局较复杂，建议提升熟练度后使用"
            else:
                adjusted_score = base_score
                reason = f"适合{user_level.value}水平用户"

            # 获取组件数量范围
            min_count, max_count = self.rule_engine.get_complexity_range(complexity_obj)

            # 获取建议组件
            suggested = self._get_layout_components(layout_id)

            recommendations.append(LayoutRecommendation(
                layout_id=layout_id,
                layout_name=self._get_layout_name(layout_id),
                score=adjusted_score,
                reason=reason,
                component_count_range=(min_count, max_count),
                suggested_components=suggested,
            ))

        return recommendations

    def _infer_layout_complexity(self, layout_id: str) -> Complexity:
        """推断布局的复杂度"""
        high_complexity = ["dashboard_grid", "workspace", "kanban_board"]
        medium_complexity = ["analytics_center", "split_view", "master_detail"]
        low_complexity = ["article_focus", "card_grid", "modal_focus"]

        if layout_id in high_complexity:
            return Complexity.COMPLEX
        elif layout_id in medium_complexity:
            return Complexity.MODERATE
        else:
            return Complexity.SIMPLE

    def _get_layout_name(self, layout_id: str) -> str:
        """获取布局显示名称"""
        names = {
            "dashboard_grid": "仪表板网格布局",
            "analytics_center": "数据分析中心",
            "report_layout": "报告布局",
            "master_detail": "主从布局",
            "data_table_center": "数据表格中心",
            "form_split": "表单分栏布局",
            "article_focus": "文章聚焦布局",
            "card_grid": "卡片网格布局",
            "timeline_vertical": "垂直时间线布局",
            "kanban_board": "看板布局",
            "list_split": "列表分栏布局",
            "workspace": "工作空间布局",
            "product_catalog": "商品目录布局",
            "checkout_flow": "结账流程布局",
            "landing_hero": "落地页焦点布局",
            "feed_center": "信息流中心",
            "profile_card": "个人资料卡布局",
            "chat_layout": "聊天布局",
            "form_wizard": "表单向导布局",
            "split_form": "分栏表单布局",
            "modal_focus": "模态聚焦布局",
            "settings_nav": "设置导航布局",
            "tabbed_settings": "标签设置布局",
            "toggle_split": "切换分栏布局",
        }
        return names.get(layout_id, layout_id)

    def _get_layout_components(self, layout_id: str) -> List[str]:
        """获取布局建议的组件"""
        mapping = {
            "dashboard_grid": ["dashboard", "metric_card", "chart_panel"],
            "data_table_center": ["data_table", "filter_bar"],
            "form_wizard": ["form_wizard", "alert_panel"],
            "kanban_board": ["kanban", "filter_bar"],
            "article_focus": ["data_list", "comment_section"],
            "product_catalog": ["data_list", "pricing_table"],
            "chat_layout": ["chatbot"],
        }
        return mapping.get(layout_id, [])

    # ========================================================================
    # 完整推荐
    # ========================================================================

    def get_recommendations(
        self,
        request: RecommendationRequest
    ) -> RecommendationResult:
        """
        获取完整推荐方案

        Args:
            request: 推荐请求

        Returns:
            完整推荐结果
        """
        # 推荐组件
        components = self.recommend_components(
            industry=request.industry,
            use_case=request.use_case,
            complexity=request.complexity,
            framework=request.framework,
            accessibility=request.require_accessibility,
        )

        # 推荐主题
        themes = []
        if request.mood:
            themes = self.recommend_theme(
                industry=request.industry,
                mood=request.mood,
                accessibility=request.require_accessibility,
            )

        # 推荐布局
        layouts = self.recommend_layout(
            content_type=request.use_case,
            user_level=request.user_level,
            complexity=request.complexity,
        )

        # 计算置信度
        confidence = self._calculate_confidence(components, themes, layouts)

        # 生成替代方案
        alternatives = self._generate_alternatives(request)

        return RecommendationResult(
            components=components,
            themes=themes,
            layouts=layouts,
            request=request,
            confidence_score=confidence,
            alternatives=alternatives,
        )

    def _calculate_confidence(
        self,
        components: List[ComponentRecommendation],
        themes: List[ThemeRecommendation],
        layouts: List[LayoutRecommendation]
    ) -> float:
        """计算推荐置信度"""
        scores = []

        if components:
            scores.append(components[0].score)

        if themes:
            scores.append(themes[0].score)

        if layouts:
            scores.append(layouts[0].score)

        return sum(scores) / len(scores) if scores else 0.0

    def _generate_alternatives(self, request: RecommendationRequest) -> List[str]:
        """生成替代方案建议"""
        alternatives = []

        if request.complexity != Complexity.MODERATE:
            alternatives.append(f"尝试{Complexity.MODERATE.value}复杂度以获得平衡体验")

        if not request.require_accessibility:
            alternatives.append("启用无障碍模式以获得更好的包容性")

        if request.mood is None:
            alternatives.append("指定氛围以获得更精准的主题推荐")

        return alternatives

    # ========================================================================
    # 用户偏好学习
    # ========================================================================

    def learn_from_feedback(self, feedback: UserFeedback):
        """
        从用户反馈中学习

        Args:
            feedback: 用户反馈数据
        """
        # 记录历史
        self._history.append(feedback)

        # 更新选择计数
        key = f"{feedback.recommendation_type}_{feedback.selected_recommendation}"
        self._selection_counts[key] = self._selection_counts.get(key, 0) + 1

        # 如果提供了评分，根据评分调整权重
        if feedback.rating is not None:
            # 高评分（4-5）：增强相关规则的权重
            if feedback.rating >= 4:
                self._positive_feedback_adjustment(feedback)
            # 低评分（1-2）：降低相关规则的权重
            elif feedback.rating <= 2:
                self._negative_feedback_adjustment(feedback)

        # 保存历史
        self._save_history()

    def _positive_feedback_adjustment(self, feedback: UserFeedback):
        """正面反馈调整"""
        delta = 0.05  # 增加权重

        if feedback.recommendation_type == "component":
            # 用户接受了组件推荐，增强行业和复杂度规则权重
            self.rule_engine.adjust_weights(RuleType.INDUSTRY_COMPONENT, delta)
            self.rule_engine.adjust_weights(RuleType.COMPLEXITY_COMPONENT, delta)

        elif feedback.recommendation_type == "theme":
            # 用户接受了主题推荐，增强氛围规则权重
            self.rule_engine.adjust_weights(RuleType.MOOD_THEME, delta)

        elif feedback.recommendation_type == "layout":
            # 用户接受了布局推荐，增强用例规则权重
            self.rule_engine.adjust_weights(RuleType.USE_CASE_LAYOUT, delta)

    def _negative_feedback_adjustment(self, feedback: UserFeedback):
        """负面反馈调整"""
        delta = -0.05  # 减少权重

        if feedback.recommendation_type == "component":
            self.rule_engine.adjust_weights(RuleType.INDUSTRY_COMPONENT, delta)
            self.rule_engine.adjust_weights(RuleType.COMPLEXITY_COMPONENT, delta)

        elif feedback.recommendation_type == "theme":
            self.rule_engine.adjust_weights(RuleType.MOOD_THEME, delta)

        elif feedback.recommendation_type == "layout":
            self.rule_engine.adjust_weights(RuleType.USE_CASE_LAYOUT, delta)

        # 如果用户选择了替代方案，增强替代方案相关规则
        if feedback.alternative_selected:
            # 这里可以进一步分析替代方案的特征
            pass

    # ========================================================================
    # 历史记录管理
    # ========================================================================

    def _load_history(self):
        """加载历史记录"""
        if not self._history_file:
            return

        try:
            history_path = Path(self._history_file)
            if history_path.exists():
                with open(history_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._history = [
                        UserFeedback(**item) for item in data.get("history", [])
                    ]
                    self._selection_counts = data.get("selection_counts", {})
        except Exception as e:
            print(f"加载历史记录失败: {e}")

    def _save_history(self):
        """保存历史记录"""
        if not self._history_file:
            return

        try:
            history_path = Path(self._history_file)
            history_path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "history": [
                    {
                        "selected_recommendation": f.selected_recommendation,
                        "recommendation_type": f.recommendation_type,
                        "context": {
                            "industry": f.context.industry,
                            "use_case": f.context.use_case,
                            "framework": f.context.framework,
                            "complexity": f.context.complexity.value,
                            "mood": f.context.mood.value if f.context.mood else None,
                            "user_level": f.context.user_level.value,
                            "require_accessibility": f.context.require_accessibility,
                        },
                        "rating": f.rating,
                        "alternative_selected": f.alternative_selected,
                        "timestamp": f.timestamp,
                    }
                    for f in self._history
                ],
                "selection_counts": self._selection_counts,
            }

            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"保存历史记录失败: {e}")

    def get_history(self) -> List[UserFeedback]:
        """获取历史记录"""
        return self._history.copy()

    def get_selection_stats(self) -> Dict[str, int]:
        """获取选择统计"""
        return self._selection_counts.copy()

    def clear_history(self):
        """清除历史记录"""
        self._history.clear()
        self._selection_counts.clear()


# ============================================================================
# 全局推荐引擎实例
# ============================================================================

_global_engine: Optional[RecommenderEngine] = None


def get_recommender_engine(
    history_file: Optional[str] = None
) -> RecommenderEngine:
    """
    获取全局推荐引擎（单例模式）

    Args:
        history_file: 历史记录文件路径

    Returns:
        RecommenderEngine 实例
    """
    global _global_engine
    if _global_engine is None:
        _global_engine = RecommenderEngine(history_file=history_file)
    return _global_engine


# ============================================================================
# 便捷函数
# ============================================================================

def recommend_components(
    industry: str,
    use_case: str,
    complexity: Complexity = Complexity.MODERATE,
    framework: str = "streamlit",
    accessibility: bool = False,
    top_n: int = 3
) -> List[ComponentRecommendation]:
    """
    推荐组件的便捷函数

    Args:
        industry: 行业ID
        use_case: 用例ID
        complexity: 复杂度
        framework: 框架
        accessibility: 无障碍要求
        top_n: 返回数量

    Returns:
        组件推荐列表
    """
    engine = get_recommender_engine()
    return engine.recommend_components(
        industry=industry,
        use_case=use_case,
        complexity=complexity,
        framework=framework,
        accessibility=accessibility,
        top_n=top_n,
    )


def recommend_theme(
    industry: str,
    mood: Mood,
    accessibility: bool = False,
    top_n: int = 3
) -> List[ThemeRecommendation]:
    """
    推荐主题的便捷函数

    Args:
        industry: 行业ID
        mood: 氛围
        accessibility: 无障碍要求
        top_n: 返回数量

    Returns:
        主题推荐列表
    """
    engine = get_recommender_engine()
    return engine.recommend_theme(
        industry=industry,
        mood=mood,
        accessibility=accessibility,
        top_n=top_n,
    )


def recommend_layout(
    content_type: str,
    user_level: UserLevel = UserLevel.INTERMEDIATE,
    top_n: int = 3
) -> List[LayoutRecommendation]:
    """
    推荐布局的便捷函数

    Args:
        content_type: 内容类型
        user_level: 用户水平
        top_n: 返回数量

    Returns:
        布局推荐列表
    """
    engine = get_recommender_engine()
    return engine.recommend_layout(
        content_type=content_type,
        user_level=user_level,
        top_n=top_n,
    )


# 用户水平-布局复杂度映射（用于便捷函数）
USER_LEVEL_LAYOUT_COMPLEXITY = {
    UserLevel.BEGINNER: [Complexity.MINIMAL, Complexity.SIMPLE],
    UserLevel.INTERMEDIATE: [Complexity.SIMPLE, Complexity.MODERATE, Complexity.COMPLEX],
    UserLevel.EXPERT: [Complexity.MODERATE, Complexity.COMPLEX, Complexity.ADVANCED],
}


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 推荐结果
    "ComponentRecommendation",
    "ThemeRecommendation",
    "LayoutRecommendation",
    "RecommendationRequest",
    "RecommendationResult",
    "UserFeedback",
    # 引擎
    "RecommenderEngine",
    "get_recommender_engine",
    # 便捷函数
    "recommend_components",
    "recommend_theme",
    "recommend_layout",
]
