"""
Industries - 行业模板模块
=========================

提供针对不同行业的定制化UI组件和模板。

支持行业:
    - general/: 通用组件
    - healthcare/: 医疗健康行业
    - finance/: 金融服务行业
    - ecommerce/: 电子商务行业
    - education/: 教育培训行业
    - manufacturing/: 制造业

每个行业模板包含:
    - 行业专用组件
    - 预定义颜色方案
    - 特定交互模式
    - 最佳实践指南
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# 行业类型枚举
# ============================================================================

class IndustryType(Enum):
    """行业类型枚举"""
    GENERAL = "general"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    ECOMMERCE = "ecommerce"
    EDUCATION = "education"
    MANUFACTURING = "manufacturing"


# ============================================================================
# 行业模板数据类
# ============================================================================

@dataclass
class IndustryColorScheme:
    """行业配色方案"""
    primary: str
    secondary: str
    accent: str
    description: str = ""

    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "accent": self.accent,
            "description": self.description,
        }


@dataclass
class IndustryComponent:
    """行业专用组件"""
    id: str
    name: str
    description: str
    category: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "tags": self.tags,
        }


@dataclass
class IndustryBestPractice:
    """行业最佳实践"""
    title: str
    description: str
    examples: List[str] = field(default_factory=list)
    anti_patterns: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "title": self.title,
            "description": self.description,
            "examples": self.examples,
            "anti_patterns": self.anti_patterns,
        }


@dataclass
class IndustryTemplate:
    """
    行业模板定义

    Attributes:
        industry_type: 行业类型
        name: 行业名称
        description: 行业描述
        color_scheme: 配色方案
        specific_components: 行业专用组件
        best_practices: 最佳实践
        typography: 字体配置
        layout_preferences: 布局偏好
        accessibility_requirements: 可访问性要求
    """
    industry_type: IndustryType
    name: str
    description: str
    color_scheme: IndustryColorScheme
    specific_components: List[IndustryComponent] = field(default_factory=list)
    best_practices: List[IndustryBestPractice] = field(default_factory=list)
    typography: Dict[str, str] = field(default_factory=dict)
    layout_preferences: Dict[str, Any] = field(default_factory=dict)
    accessibility_requirements: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "industry_type": self.industry_type.value,
            "name": self.name,
            "description": self.description,
            "color_scheme": self.color_scheme.to_dict(),
            "specific_components": [c.to_dict() for c in self.specific_components],
            "best_practices": [bp.to_dict() for bp in self.best_practices],
            "typography": self.typography,
            "layout_preferences": self.layout_preferences,
            "accessibility_requirements": self.accessibility_requirements,
        }


# ============================================================================
# 行业模板管理器
# ============================================================================

class IndustryManager:
    """行业模板管理器"""

    def __init__(self):
        self._templates: Dict[IndustryType, IndustryTemplate] = {}
        self._register_default_templates()

    def _register_default_templates(self):
        """注册默认行业模板"""

        # === General ===
        general = IndustryTemplate(
            industry_type=IndustryType.GENERAL,
            name="通用",
            description="适用于大多数场景的通用模板",
            color_scheme=IndustryColorScheme(
                primary="#007bff",
                secondary="#6c757d",
                accent="#28a745",
                description="蓝色系，专业且通用",
            ),
            typography={
                "font_family": "system-ui, -apple-system, sans-serif",
                "font_size": "16px",
                "line_height": "1.5",
            },
            layout_preferences={
                "container_max_width": "1200px",
                "spacing_unit": "8px",
                "border_radius": "4px",
            },
        )
        self.register(general)

        # === Healthcare ===
        healthcare = IndustryTemplate(
            industry_type=IndustryType.HEALTHCARE,
            name="医疗健康",
            description="医疗行业专用模板，强调清晰度和专业性",
            color_scheme=IndustryColorScheme(
                primary="#17a2b8",
                secondary="#138496",
                accent="#0d6efd",
                description="青色系，冷静且专业",
            ),
            specific_components=[
                IndustryComponent(
                    id="patient_form",
                    name="患者信息表单",
                    description="收集患者基本信息和病史",
                    category="form",
                    tags=["表单", "患者", "医疗"],
                ),
                IndustryComponent(
                    id="medical_chart",
                    name="医疗图表",
                    description="展示患者生命体征和医疗数据",
                    category="data",
                    tags=["图表", "数据", "生命体征"],
                ),
                IndustryComponent(
                    id="appointment_scheduler",
                    name="预约排期器",
                    description="管理医生预约时间表",
                    category="form",
                    tags=["预约", "日历", "时间"],
                ),
            ],
            best_practices=[
                IndustryBestPractice(
                    title="清晰的数据展示",
                    description="医疗数据需要清晰准确，避免歧义",
                    examples=["使用大字体显示关键数值", "使用颜色区分状态"],
                    anti_patterns=["使用模糊的图标", "信息过度拥挤"],
                ),
                IndustryBestPractice(
                    title="紧急操作突出",
                    description="紧急操作需要醒目且易于访问",
                    examples=["使用红色表示紧急", "固定在页面顶部"],
                    anti_patterns=["隐藏在菜单中", "与其他操作样式一致"],
                ),
            ],
            typography={
                "font_family": "Helvetica Neue, Arial, sans-serif",
                "font_size": "16px",
                "line_height": "1.6",
            },
            layout_preferences={
                "container_max_width": "1400px",
                "spacing_unit": "8px",
                "border_radius": "6px",
            },
            accessibility_requirements=[
                "符合 WCAG 2.1 AA 级标准",
                "支持屏幕阅读器",
                "键盘完全可操作",
                "色盲友好的配色",
            ],
        )
        self.register(healthcare)

        # === Finance ===
        finance = IndustryTemplate(
            industry_type=IndustryType.FINANCE,
            name="金融服务",
            description="金融行业模板，强调数据可视化和安全性",
            color_scheme=IndustryColorScheme(
                primary="#28a745",
                secondary="#20c997",
                accent="#007bff",
                description="绿色系，象征增长和稳定",
            ),
            specific_components=[
                IndustryComponent(
                    id="account_summary",
                    name="账户概览",
                    description="显示账户余额和关键指标",
                    category="data",
                    tags=["数据", "账户", "金融"],
                ),
                IndustryComponent(
                    id="transaction_table",
                    name="交易明细表",
                    description="展示交易历史记录",
                    category="data",
                    tags=["表格", "交易", "历史"],
                ),
                IndustryComponent(
                    id="risk_indicator",
                    name="风险指示器",
                    description="可视化展示投资风险等级",
                    category="feedback",
                    tags=["风险", "指示器", "可视化"],
                ),
            ],
            best_practices=[
                IndustryBestPractice(
                    title="数据精度",
                    description="金融数据必须精确显示",
                    examples=["使用等宽数字字体", "对齐小数点"],
                    anti_patterns=["四舍五入过度", "使用科学计数法"],
                ),
                IndustryBestPractice(
                    title="安全提示",
                    description="敏感操作需要明确提示",
                    examples=["二次确认", "显示最后几位账号"],
                    anti_patterns=["无确认直接操作", "完整显示账号"],
                ),
            ],
            typography={
                "font_family": "Roboto, monospace",
                "font_size": "14px",
                "line_height": "1.5",
            },
            accessibility_requirements=[
                "符合 WCAG 2.1 AAA 级标准",
                "高对比度模式",
                "减少动画（ vestibular disorder 友好）",
            ],
        )
        self.register(finance)

        # === E-commerce ===
        ecommerce = IndustryTemplate(
            industry_type=IndustryType.ECOMMERCE,
            name="电子商务",
            description="电商行业模板，强调转化率和用户体验",
            color_scheme=IndustryColorScheme(
                primary="#fd7e14",
                secondary="#dc3545",
                accent="#ffc107",
                description="橙红色系，激发购买欲望",
            ),
            specific_components=[
                IndustryComponent(
                    id="product_card",
                    name="商品卡片",
                    description="展示商品信息和价格",
                    category="media",
                    tags=["商品", "卡片", "价格"],
                ),
                IndustryComponent(
                    id="shopping_cart",
                    name="购物车",
                    description="管理待购商品",
                    category="data",
                    tags=["购物车", "商品", "结算"],
                ),
                IndustryComponent(
                    id="checkout_flow",
                    name="结算流程",
                    description="引导用户完成支付",
                    category="form",
                    tags=["结算", "支付", "表单"],
                ),
            ],
            best_practices=[
                IndustryBestPractice(
                    title="清晰的CTA",
                    description="购买按钮需要醒目",
                    examples=["使用对比色", "添加图标"],
                    anti_patterns=["使用灰色按钮", "位置不明显"],
                ),
                IndustryBestPractice(
                    title="减少摩擦",
                    description="简化购买流程",
                    examples=["保存用户信息", "进度指示"],
                    anti_patterns=["过多可选步骤", "不必要的信息收集"],
                ),
            ],
            typography={
                "font_family": "Inter, sans-serif",
                "font_size": "16px",
                "line_height": "1.4",
            },
            layout_preferences={
                "container_max_width": "1280px",
                "spacing_unit": "4px",
                "border_radius": "8px",
            },
        )
        self.register(ecommerce)

        # === Education ===
        education = IndustryTemplate(
            industry_type=IndustryType.EDUCATION,
            name="教育培训",
            description="教育行业模板，强调互动性和易用性",
            color_scheme=IndustryColorScheme(
                primary="#6610f2",
                secondary="#6f42c1",
                accent="#e83e8c",
                description="紫色系，激发创造力",
            ),
            specific_components=[
                IndustryComponent(
                    id="course_card",
                    name="课程卡片",
                    description="展示课程信息",
                    category="media",
                    tags=["课程", "卡片", "学习"],
                ),
                IndustryComponent(
                    id="quiz_interface",
                    name="测验界面",
                    description="互动问答组件",
                    category="form",
                    tags=["测验", "问答", "互动"],
                ),
                IndustryComponent(
                    id="progress_tracker",
                    name="进度追踪器",
                    description="显示学习进度",
                    category="feedback",
                    tags=["进度", "学习", "追踪"],
                ),
            ],
            best_practices=[
                IndustryBestPractice(
                    title="即时反馈",
                    description="学习需要及时反馈",
                    examples=["答题后立即显示结果", "进度条实时更新"],
                    anti_patterns=["延迟反馈", "无进度指示"],
                ),
                IndustryBestPractice(
                    title="鼓励机制",
                    description="使用正向激励",
                    examples=["成就徽章", "进度庆祝"],
                    anti_patterns=["仅显示错误", "惩罚性设计"],
                ),
            ],
            typography={
                "font_family": "Nunito, sans-serif",
                "font_size": "18px",
                "line_height": "1.6",
            },
            layout_preferences={
                "container_max_width": "1200px",
                "spacing_unit": "8px",
                "border_radius": "12px",
            },
        )
        self.register(education)

        # === Manufacturing ===
        manufacturing = IndustryTemplate(
            industry_type=IndustryType.MANUFACTURING,
            name="制造业",
            description="制造业模板，强调生产流程和数据监控",
            color_scheme=IndustryColorScheme(
                primary="#343a40",
                secondary="#495057",
                accent="#6c757d",
                description="灰色系，专业且稳重",
            ),
            specific_components=[
                IndustryComponent(
                    id="production_dashboard",
                    name="生产仪表盘",
                    description="监控生产指标",
                    category="data",
                    tags=["仪表盘", "生产", "监控"],
                ),
                IndustryComponent(
                    id="quality_control",
                    name="质量控制面板",
                    description="质量检验和报告",
                    category="form",
                    tags=["质量", "检验", "报告"],
                ),
                IndustryComponent(
                    id="inventory_table",
                    name="库存表格",
                    description="管理原材料和成品库存",
                    category="data",
                    tags=["库存", "表格", "管理"],
                ),
            ],
            best_practices=[
                IndustryBestPractice(
                    title="实时数据",
                    description="生产数据需要实时更新",
                    examples=["自动刷新", "WebSocket 连接"],
                    anti_patterns=["手动刷新", "延迟更新"],
                ),
                IndustryBestPractice(
                    title="警报系统",
                    description="异常情况需要立即通知",
                    examples=["声音提示", "闪烁警告"],
                    anti_patterns=["静默错误", "不明显的提示"],
                ),
            ],
            typography={
                "font_family": "Segoe UI, sans-serif",
                "font_size": "14px",
                "line_height": "1.5",
            },
            layout_preferences={
                "container_max_width": "1600px",
                "spacing_unit": "4px",
                "border_radius": "2px",
            },
            accessibility_requirements=[
                "符合 WCAG 2.1 AA 级标准",
                "支持暗色模式（车间环境）",
                "高对比度选项",
            ],
        )
        self.register(manufacturing)

    def register(self, template: IndustryTemplate):
        """
        注册行业模板

        Args:
            template: 行业模板实例
        """
        self._templates[template.industry_type] = template

    def get(self, industry_type: IndustryType) -> Optional[IndustryTemplate]:
        """
        获取行业模板

        Args:
            industry_type: 行业类型

        Returns:
            行业模板实例，不存在则返回 None
        """
        return self._templates.get(industry_type)

    def get_by_name(self, name: str) -> Optional[IndustryTemplate]:
        """
        按名称获取行业模板

        Args:
            name: 行业名称

        Returns:
            行业模板实例
        """
        for template in self._templates.values():
            if template.name == name or template.industry_type.value == name:
                return template
        return None

    def list_all(self) -> List[IndustryTemplate]:
        """列出所有行业模板"""
        return list(self._templates.values())

    def list_industries(self) -> List[str]:
        """列出所有支持的行业名称"""
        return [t.industry_type.value for t in self._templates.values()]


# ============================================================================
# 全局管理器实例
# ============================================================================

_default_manager: Optional[IndustryManager] = None


def get_industry_manager() -> IndustryManager:
    """
    获取全局行业模板管理器（单例模式）

    Returns:
        IndustryManager 实例
    """
    global _default_manager
    if _default_manager is None:
        _default_manager = IndustryManager()
    return _default_manager


# ============================================================================
# 便捷函数
# ============================================================================

def get_industry_template(industry_type: IndustryType) -> Optional[IndustryTemplate]:
    """获取行业模板"""
    return get_industry_manager().get(industry_type)


def get_industry_template_by_name(name: str) -> Optional[IndustryTemplate]:
    """按名称获取行业模板"""
    return get_industry_manager().get_by_name(name)


def list_industries() -> List[str]:
    """列出所有支持的行业"""
    return get_industry_manager().list_industries()


def get_industry_color_scheme(industry: str) -> Optional[IndustryColorScheme]:
    """
    获取行业配色方案

    Args:
        industry: 行业名称

    Returns:
        配色方案，不存在则返回 None
    """
    template = get_industry_template_by_name(industry)
    return template.color_scheme if template else None


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "IndustryType",
    # 数据类
    "IndustryColorScheme",
    "IndustryComponent",
    "IndustryBestPractice",
    "IndustryTemplate",
    # 管理器
    "IndustryManager",
    "get_industry_manager",
    # 便捷函数
    "get_industry_template",
    "get_industry_template_by_name",
    "list_industries",
    "get_industry_color_scheme",
]
