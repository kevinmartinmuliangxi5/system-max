"""
Education Industry Templates - 教育培训行业模板
=================================================

包含教育培训行业专用的 5 个完整页面模板：

模板列表:
    1. CourseCatalog - 课程目录（分类、搜索、推荐）
    2. LessonPlayer - 课程播放器（视频、笔记、进度）
    3. QuizSystem - 测验系统（题目、计时、评分）
    4. ProgressTracker - 学习进度（完成率、徽章、排行）
    5. DiscussionForum - 讨论区（问答、回复、点赞）

推荐主题:
    - ocean_blue: 适合教育平台主色调
    - spring_blossom: 适合温馨学习氛围
    - forest_green: 适合知识成长主题

使用方式:
    from ui_library.industries.education import (
        CourseCatalog,
        LessonPlayer,
        QuizSystem,
        ProgressTracker,
        DiscussionForum,
    )
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import pandas as pd
from datetime import datetime, timedelta


# ============================================================================
# 枚举定义
# ============================================================================

class CourseLevel(Enum):
    """课程难度"""
    BEGINNER = "beginner"       # 入门
    INTERMEDIATE = "intermediate"  # 中级
    ADVANCED = "advanced"       # 高级
    ALL = "all"                 # 全部


class CourseStatus(Enum):
    """课程状态"""
    DRAFT = "draft"             # 草稿
    PUBLISHED = "published"     # 已发布
    ARCHIVED = "archived"       # 已归档


class EnrollmentStatus(Enum):
    """报名状态"""
    NOT_ENROLLED = "not_enrolled"  # 未报名
    ENROLLED = "enrolled"          # 已报名
    IN_PROGRESS = "in_progress"    # 学习中
    COMPLETED = "completed"        # 已完成
    DROPPED = "dropped"            # 已退课


class QuestionType(Enum):
    """题目类型"""
    SINGLE_CHOICE = "single_choice"    # 单选题
    MULTIPLE_CHOICE = "multiple_choice"  # 多选题
    TRUE_FALSE = "true_false"        # 判断题
    FILL_BLANK = "fill_blank"        # 填空题
    ESSAY = "essay"                  # 简答题
    CODING = "coding"                # 编程题


class BadgeType(Enum):
    """徽章类型"""
    COMPLETION = "completion"    # 完成徽章
    ACHIEVEMENT = "achievement"  # 成就徽章
    STREAK = "streak"           # 连续学习
    MILESTONE = "milestone"     # 里程碑
    SPECIAL = "special"         # 特别徽章


class PostType(Enum):
    """帖子类型"""
    QUESTION = "question"       # 提问
    ANSWER = "answer"           # 回答
    DISCUSSION = "discussion"   # 讨论
    ANNOUNCEMENT = "announcement"  # 公告
    SHARE = "share"             # 分享


# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class Course:
    """
    课程定义

    Attributes:
        id: 课程ID
        title: 课程标题
        description: 课程描述
        instructor: 讲师
        level: 课程难度
        duration: 时长（分钟）
        price: 价格
        category: 分类
        tags: 标签
        thumbnail: 封面图
        status: 状态
    """
    id: str
    title: str
    description: str
        instructor: str
        level: CourseLevel
        duration: int  # 分钟
        price: float
        category: str
        tags: List[str] = field(default_factory=list)
        thumbnail: Optional[str] = None
        status: CourseStatus = CourseStatus.PUBLISHED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "instructor": self.instructor,
            "level": self.level.value,
            "duration": self.duration,
            "price": self.price,
            "category": self.category,
            "tags": self.tags,
            "thumbnail": self.thumbnail,
            "status": self.status.value,
        }


@dataclass
class Lesson:
    """
    课程课时定义

    Attributes:
        id: 课时ID
        course_id: 所属课程ID
        title: 标题
        description: 描述
        video_url: 视频URL
        duration: 时长（秒）
        order_no: 顺序号
        resources: 学习资源
    """
    id: str
    course_id: str
    title: str
    description: str
    video_url: str
    duration: int  # 秒
    order_no: int
    resources: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "video_url": self.video_url,
            "duration": self.duration,
            "order_no": self.order_no,
            "resources": self.resources,
        }


@dataclass
class Question:
    """
    题目定义

    Attributes:
        id: 题目ID
        quiz_id: 所属测验ID
        type: 题目类型
        content: 题目内容
        options: 选项列表
        correct_answer: 正确答案
        points: 分值
        explanation: 解析
    """
    id: str
    quiz_id: str
    type: QuestionType
    content: str
    options: List[str]
    correct_answer: Any
    points: int
    explanation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "type": self.type.value,
            "content": self.content,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "points": self.points,
            "explanation": self.explanation,
        }


@dataclass
class Quiz:
    """
    测验定义

    Attributes:
        id: 测验ID
        course_id: 所属课程ID
        title: 标题
        description: 描述
        duration: 时长限制（分钟）
        passing_score: 及格分
        attempts: 允许尝试次数
        questions: 题目列表
        shuffle_questions: 是否随机排序
    """
    id: str
    course_id: str
    title: str
    description: str
    duration: int  # 分钟
    passing_score: int
    attempts: int
    questions: List[Question]
    shuffle_questions: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "duration": self.duration,
            "passing_score": self.passing_score,
            "attempts": self.attempts,
            "questions": [q.to_dict() for q in self.questions],
            "shuffle_questions": self.shuffle_questions,
        }


@dataclass
class Badge:
    """
    徽章定义

    Attributes:
        id: 徽章ID
        name: 名称
        description: 描述
        icon: 图标
        type: 类型
        requirement: 获得条件
    """
    id: str
    name: str
    description: str
    icon: str
    type: BadgeType
    requirement: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "type": self.type.value,
            "requirement": self.requirement,
        }


@dataclass
class ForumPost:
    """
    论坛帖子定义

    Attributes:
        id: 帖子ID
        type: 帖子类型
        author: 作者
        title: 标题
        content: 内容
        course_id: 关联课程ID
        tags: 标签
        created_at: 创建时间
        likes: 点赞数
        replies: 回复数
        views: 浏览数
        is_solved: 是否已解决
    """
    id: str
    type: PostType
    author: str
    title: str
    content: str
    course_id: Optional[str]
    tags: List[str]
    created_at: datetime
    likes: int = 0
    replies: int = 0
    views: int = 0
    is_solved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "author": self.author,
            "title": self.title,
            "content": self.content,
            "course_id": self.course_id,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "likes": self.likes,
            "replies": self.replies,
            "views": self.views,
            "is_solved": self.is_solved,
        }


# ============================================================================
# 1. CourseCatalog - 课程目录模板
# ============================================================================

class CourseCatalog:
    """
    课程目录模板

    功能: 课程分类、搜索筛选、智能推荐

    推荐主题: ocean_blue, spring_blossom

    特性:
        - 多分类浏览
        - 关键词搜索
        - 难度筛选
        - 价格筛选
        - 个性化推荐
        - 课程对比
    """

    # 默认课程分类
    DEFAULT_CATEGORIES = [
        "编程开发",
        "产品设计",
        "数据分析",
        "人工智能",
        "数字营销",
        "职场技能",
        "语言学习",
        "兴趣艺术"
    ]

    def __init__(self, courses: Optional[List[Course]] = None):
        """
        初始化课程目录

        Args:
            courses: 课程列表
        """
        self.courses = courses or self._get_default_courses()
        self._categories = self.DEFAULT_CATEGORIES

    def _get_default_courses(self) -> List[Course]:
        """获取默认课程列表"""
        return [
            Course(
                id="python_101",
                title="Python 零基础入门",
                description="从零开始学习 Python 编程，适合编程新手",
                instructor="张老师",
                level=CourseLevel.BEGINNER,
                duration=1200,
                price=199.00,
                category="编程开发",
                tags=["Python", "编程", "入门"]
            ),
            Course(
                id="web_design",
                title="UI/UX 设计实战",
                description="学习现代网页设计原理和实践技巧",
                instructor="李老师",
                level=CourseLevel.INTERMEDIATE,
                duration=900,
                price=299.00,
                category="产品设计",
                tags=["UI", "UX", "设计", "Figma"]
            ),
            Course(
                id="data_analysis",
                title="数据分析与可视化",
                description="使用 Python 进行数据分析和可视化展示",
                instructor="王老师",
                level=CourseLevel.INTERMEDIATE,
                duration=1500,
                price=399.00,
                category="数据分析",
                tags=["数据分析", "Python", "可视化"]
            ),
            Course(
                id="ai_basics",
                title="人工智能基础概论",
                description="了解 AI 的基本原理和应用场景",
                instructor="赵老师",
                level=CourseLevel.BEGINNER,
                duration=800,
                price=0.00,  # 免费课程
                category="人工智能",
                tags=["AI", "机器学习", "入门"]
            ),
        ]

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
课程目录 - Streamlit 实现
==========================

功能: 课程分类、搜索筛选、智能推荐
"""

import streamlit as st
import pandas as pd
from datetime import datetime


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="课程目录",
    page_icon="📚",
    layout="wide"
)


# ============================================================================
# 模拟课程数据
# ============================================================================

@st.cache_data
def get_courses():
    """获取课程列表"""
    courses = [
        {
            "id": "python_101",
            "title": "Python 零基础入门",
            "description": "从零开始学习 Python 编程，适合编程新手",
            "instructor": "张老师",
            "level": "beginner",
            "duration": 1200,
            "price": 199.00,
            "category": "编程开发",
            "tags": ["Python", "编程", "入门"],
            "enrollment": 12580,
            "rating": 4.8,
            "thumbnail": "🐍"
        },
        {
            "id": "web_design",
            "title": "UI/UX 设计实战",
            "description": "学习现代网页设计原理和实践技巧",
            "instructor": "李老师",
            "level": "intermediate",
            "duration": 900,
            "price": 299.00,
            "category": "产品设计",
            "tags": ["UI", "UX", "设计", "Figma"],
            "enrollment": 8420,
            "rating": 4.9,
            "thumbnail": "🎨"
        },
        {
            "id": "data_analysis",
            "title": "数据分析与可视化",
            "description": "使用 Python 进行数据分析和可视化展示",
            "instructor": "王老师",
            "level": "intermediate",
            "duration": 1500,
            "price": 399.00,
            "category": "数据分析",
            "tags": ["数据分析", "Python", "可视化"],
            "enrollment": 6750,
            "rating": 4.7,
            "thumbnail": "📊"
        },
        {
            "id": "ai_basics",
            "title": "人工智能基础概论",
            "description": "了解 AI 的基本原理和应用场景",
            "instructor": "赵老师",
            "level": "beginner",
            "duration": 800,
            "price": 0.00,
            "category": "人工智能",
            "tags": ["AI", "机器学习", "入门"],
            "enrollment": 25680,
            "rating": 4.6,
            "thumbnail": "🤖"
        },
        {
            "id": "digital_marketing",
            title="数字营销全攻略",
            "description="掌握现代数字营销的核心策略和工具",
            "instructor": "刘老师",
            "level": "beginner",
            "duration": 1000,
            "price": 249.00,
            "category": "数字营销",
            "tags": ["营销", "SEO", "社交媒体"],
            "enrollment": 5120,
            "rating": 4.5,
            "thumbnail": "📱"
        },
        {
            "id": "react_advanced",
            title="React 高级进阶",
            description="深入理解 React 原理和高级模式",
            "instructor": "陈老师",
            "level": "advanced",
            "duration": 1800,
            "price": 499.00,
            "category": "编程开发",
            "tags": ["React", "JavaScript", "前端"],
            "enrollment": 3200,
            "rating": 4.9,
            "thumbnail": "⚛️"
        },
    ]
    return courses


@st.cache_data
def get_categories():
    """获取课程分类"""
    return [
        "全部",
        "编程开发",
        "产品设计",
        "数据分析",
        "人工智能",
        "数字营销",
        "职场技能",
        "语言学习",
        "兴趣艺术"
    ]


# ============================================================================
# 状态管理
# ============================================================================

if "catalog_filters" not in st.session_state:
    st.session_state.catalog_filters = {
        "category": "全部",
        "level": "all",
        "price_range": "all",
        "search": "",
        "tags": []
    }

if "enrolled_courses" not in st.session_state:
    st.session_state.enrolled_courses = []

if "cart_courses" not in st.session_state:
    st.session_state.cart_courses = []


# ============================================================================
# 侧边栏 - 筛选控制
# ============================================================================

st.sidebar.title("🔍 课程筛选")

# 搜索
search = st.sidebar.text_input(
    "搜索课程",
    value=st.session_state.catalog_filters["search"],
    placeholder="输入关键词..."
)

if search != st.session_state.catalog_filters["search"]:
    st.session_state.catalog_filters["search"] = search
    st.rerun()

st.sidebar.divider()

# 分类筛选
st.sidebar.subheader("📂 课程分类")
categories = get_categories()

selected_category = st.sidebar.selectbox(
    "选择分类",
    categories,
    index=categories.index(st.session_state.catalog_filters["category"])
)

if selected_category != st.session_state.catalog_filters["category"]:
    st.session_state.catalog_filters["category"] = selected_category
    st.rerun()

# 难度筛选
st.sidebar.subheader("📊 课程难度")
level_options = ["全部", "入门", "中级", "高级"]
level_map = {"全部": "all", "入门": "beginner", "中级": "intermediate", "高级": "advanced"}

selected_level = st.sidebar.selectbox(
    "选择难度",
    level_options,
    index=0
)

st.session_state.catalog_filters["level"] = level_map[selected_level]

# 价格筛选
st.sidebar.subheader("💰 价格范围")
price_options = ["全部", "免费", "¥200以下", "¥200-500", "¥500以上"]
selected_price = st.sidebar.selectbox("选择价格", price_options)

st.session_state.catalog_filters["price_range"] = selected_price

st.sidebar.divider()

# 已选课程
st.sidebar.subheader(f"🛒 购物车 ({len(st.session_state.cart_courses)})")

if st.session_state.cart_courses:
    for course_id in st.session_state.cart_courses:
        all_courses = get_courses()
        course = next((c for c in all_courses if c["id"] == course_id), None)
        if course:
            with st.sidebar.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f'{course["thumbnail"]} {course["title"][:20]}...')
                with col2:
                    if st.button("×", key=f'remove_cart_{course_id}'):
                        st.session_state.cart_courses.remove(course_id)
                        st.rerun()
else:
    st.sidebar.caption("购物车为空")

if st.session_state.cart_courses:
    total = sum(
        next((c["price"] for c in get_courses() if c["id"] == cid), 0)
        for cid in st.session_state.cart_courses
    )
    st.sidebar.metric("总计", f"¥{total:.2f}")

    if st.sidebar.button("去结算", use_container_width=True, type="primary"):
        st.info("💳 结算功能开发中...")


# ============================================================================
# 主界面
# ============================================================================

st.title("📚 课程目录")

# 推荐课程
st.subheader("🔥 热门推荐")

all_courses = get_courses()
# 按报名数排序
recommended = sorted(all_courses, key=lambda x: x["enrollment"], reverse=True)[:4]

rec_cols = st.columns(4)

for col, course in zip(rec_cols, recommended):
    with col:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;'>
            <div style='font-size: 48px;'>{course['thumbnail']}</div>
            <h4 style='margin: 10px 0;'>{course['title']}</h4>
            <p style='color: gray; font-size: 12px;'>{course['instructor']}</p>
            <p style='color: #f56c6c; font-weight: bold;'>{'免费' if course['price'] == 0 else f'¥{course[\"price\"]:.0f}'}</p>
        </div>
        """, unsafe_allow_html=True)

        if course["id"] not in st.session_state.enrolled_courses:
            if course["id"] not in st.session_state.cart_courses:
                if st.button("加入购物车", key=f'add_rec_{course["id"]}', use_container_width=True):
                    st.session_state.cart_courses.append(course["id"])
                    st.success(f"已添加: {course['title']}")
                    st.rerun()
            else:
                st.button("已在购物车", disabled=True, use_container_width=True)
        else:
            st.button("已购买", disabled=True, use_container_width=True)

st.divider()


# ============================================================================
# 课程列表
# ============================================================================

st.subheader("📖 所有课程")

# 应用筛选
filters = st.session_state.catalog_filters

filtered_courses = all_courses.copy()

# 分类筛选
if filters["category"] != "全部":
    filtered_courses = [c for c in filtered_courses if c["category"] == filters["category"]]

# 难度筛选
if filters["level"] != "all":
    filtered_courses = [c for c in filtered_courses if c["level"] == filters["level"]]

# 价格筛选
if filters["price_range"] == "免费":
    filtered_courses = [c for c in filtered_courses if c["price"] == 0]
elif filters["price_range"] == "¥200以下":
    filtered_courses = [c for c in filtered_courses if 0 < c["price"] < 200]
elif filters["price_range"] == "¥200-500":
    filtered_courses = [c for c in filtered_courses if 200 <= c["price"] <= 500]
elif filters["price_range"] == "¥500以上":
    filtered_courses = [c for c in filtered_courses if c["price"] > 500]

# 搜索筛选
if filters["search"]:
    search_lower = filters["search"].lower()
    filtered_courses = [
        c for c in filtered_courses
        if search_lower in c["title"].lower() or
           search_lower in c["description"].lower() or
           any(search_lower in tag.lower() for tag in c["tags"])
    ]

# 显示统计
st.caption(f"找到 {len(filtered_courses)} 门课程")

# 渲染课程卡片
for course in filtered_courses:
    with st.container():
        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown(f"<div style='font-size: 64px; text-align: center;'>{course['thumbnail']}</div>", unsafe_allow_html=True)

        with col2:
            # 课程标题和标签
            col_title, col_price = st.columns([4, 1])

            with col_title:
                st.markdown(f"### {course['title']}")

                # 标签
                tag_cols = st.columns(len(course['tags']))
                for tag_col, tag in zip(tag_cols, course['tags']):
                    with tag_col:
                        st.caption(f"#{tag}")

            with col_price:
                if course["price"] == 0:
                    st.markdown("<div style='color: #67c23a; font-weight: bold; font-size: 20px;'>免费</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='color: #f56c6c; font-weight: bold; font-size: 20px;'>¥{course['price']:.0f}</div>", unsafe_allow_html=True)

            # 课程信息
            col_info1, col_info2, col_info3 = st.columns(3)

            with col_info1:
                st.write(f"👨‍🏫 {course['instructor']}")

            with col_info2:
                level_icons = {"beginner": "🌱", "intermediate": "🌿", "advanced": "🌳"}
                st.write(f"{level_icons.get(course['level'], '📚')} {course['level'].title()}")

            with col_info3:
                hours = course['duration'] // 60
                st.write(f"⏱️ {hours} 小时")

            # 统计信息
            col_stats1, col_stats2, col_stats3 = st.columns(3)

            with col_stats1:
                st.metric("", f"{course['enrollment']:,}", label_visibility="collapsed", help="报名人数")

            with col_stats2:
                st.metric("", f"⭐ {course['rating']}", label_visibility="collapsed", help="评分")

            with col_stats3:
                st.metric("", f"{course['category']}", label_visibility="collapsed", help="分类")

            # 课程描述
            st.caption(course['description'])

            # 操作按钮
            col_btn1, col_btn2, col_btn3 = st.columns(3)

            with col_btn1:
                if st.button(f'📖 查看详情', key=f'detail_{course["id"]}', use_container_width=True):
                    st.info(f"正在加载: {course['title']}")

            with col_btn2:
                if course["id"] not in st.session_state.cart_courses:
                    if st.button(f'🛒 加入购物车', key=f'cart_{course["id"]}', use_container_width=True):
                        st.session_state.cart_courses.append(course["id"])
                        st.success("已添加到购物车")
                        st.rerun()
                else:
                    st.button('已在购物车', disabled=True, use_container_width=True)

            with col_btn3:
                if st.button(f'❤️ 收藏', key=f'fav_{course["id"]}', use_container_width=True):
                    st.success("已收藏")

        st.divider()


# ============================================================================
# 空状态
# ============================================================================

if not filtered_courses:
    st.info("🔍 没有找到符合条件的课程，请尝试调整筛选条件")
'''

    def get_sample_data(self) -> Dict[str, Any]:
        """获取示例数据结构"""
        return {
            "courses": [c.to_dict() for c in self.courses],
            "categories": self._categories,
            "sample_filters": {
                "category": "编程开发",
                "level": "beginner",
                "price_range": "0-200"
            }
        }


# ============================================================================
# 2. LessonPlayer - 课程播放器模板
# ============================================================================

class LessonPlayer:
    """
    课程播放器模板

    功能: 视频播放、笔记记录、进度跟踪

    推荐主题: ocean_blue, spring_blossom

    特性:
        - 视频播放
        - 课程大纲
        - 学习笔记
        - 进度保存
        - 问答互动
        - 资源下载
    """

    def __init__(self, course: Optional[Course] = None):
        """初始化播放器"""
        self.course = course
        self._lessons = self._get_default_lessons()

    def _get_default_lessons(self) -> List[Lesson]:
        """获取默认课时列表"""
        return [
            Lesson(
                id="lesson_1",
                course_id="python_101",
                title="第1课: Python 简介",
                description="了解 Python 的历史和应用场景",
                video_url="https://example.com/video1.mp4",
                duration=600,
                order_no=1
            ),
            Lesson(
                id="lesson_2",
                course_id="python_101",
                title="第2课: 环境搭建",
                description="安装 Python 和配置开发环境",
                video_url="https://example.com/video2.mp4",
                duration=900,
                order_no=2
            ),
            Lesson(
                id="lesson_3",
                course_id="python_101",
                title="第3课: 基础语法",
                description="学习 Python 基础语法和数据类型",
                video_url="https://example.com/video3.mp4",
                duration=1200,
                order_no=3
            ),
        ]

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
课程播放器 - Streamlit 实现
============================

功能: 视频播放、笔记记录、进度跟踪
"""

import streamlit as st
from datetime import timedelta


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="课程播放器",
    page_icon="🎬",
    layout="wide"
)


# ============================================================================
# 模拟课程数据
# ============================================================================

@st.cache_data
def get_course():
    """获取当前课程"""
    return {
        "id": "python_101",
        "title": "Python 零基础入门",
        "instructor": "张老师",
        "total_duration": 7200,
        "total_lessons": 20
    }


@st.cache_data
def get_lessons():
    """获取课程课时列表"""
    return [
        {
            "id": "lesson_1",
            "title": "第1课: Python 简介",
            "description": "了解 Python 的历史和应用场景",
            "duration": 600,
            "order_no": 1,
            "completed": True
        },
        {
            "id": "lesson_2",
            "title": "第2课: 环境搭建",
            "description": "安装 Python 和配置开发环境",
            "duration": 900,
            "order_no": 2,
            "completed": True
        },
        {
            "id": "lesson_3",
            "title": "第3课: 基础语法",
            "description": "学习 Python 基础语法和数据类型",
            "duration": 1200,
            "order_no": 3,
            "completed": False
        },
        {
            "id": "lesson_4",
            "title": "第4课: 控制流程",
            "description": "if 语句和循环结构",
            "duration": 1500,
            "order_no": 4,
            "completed": False
        },
        {
            "id": "lesson_5",
            "title": "第5课: 函数入门",
            "description": "定义和调用函数",
            "duration": 1800,
            "order_no": 5,
            "completed": False
        },
    ]


# ============================================================================
# 状态管理
# ============================================================================

if "current_lesson" not in st.session_state:
    st.session_state.current_lesson = "lesson_3"

if "lesson_progress" not in st.session_state:
    st.session_state.lesson_progress = {
        "lesson_1": 100,
        "lesson_2": 100,
        "lesson_3": 0,
        "lesson_4": 0,
        "lesson_5": 0
    }

if "lesson_notes" not in st.session_state:
    st.session_state.lesson_notes = {}

if "video_position" not in st.session_state:
    st.session_state.video_position = 0


# ============================================================================
# 获取数据
# ============================================================================

course = get_course()
lessons = get_lessons()
current_lesson = next((l for l in lessons if l["id"] == st.session_state.current_lesson), lessons[0])


# ============================================================================
# 主界面布局
# ============================================================================

# 顶部信息栏
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.title(f"🎬 {course['title']}")

with col2:
    # 总体进度
    completed_count = sum(1 for l in lessons if l.get("completed", False))
    total_progress = completed_count / len(lessons) * 100
    st.metric("学习进度", f"{completed_count}/{len(lessons)} 课", delta=f"{total_progress:.0f}%")

with col3:
    st.metric("总时长", f"{course['total_duration'] // 60} 小时")


# ============================================================================
# 主内容区 - 三栏布局
# ============================================================================

col_main, col_sidebar, col_notes = st.columns([3, 2, 2])


# ============================================================================
# 左侧 - 视频播放区
# ============================================================================

with col_main:
    st.subheader(f"📺 {current_lesson['title']}")

    # 视频播放器占位
    st.markdown(f"""
    <div style='background: #000; border-radius: 8px; height: 400px; display: flex; align-items: center; justify-content: center; color: #fff;'>
        <div style='text-align: center;'>
            <div style='font-size: 64px;'>▶️</div>
            <p>视频播放器</p>
            <p style='color: #888;'>{current_lesson['title']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 播放控制
    col_play1, col_play2, col_play3, col_play4 = st.columns(4)

    with col_play1:
        if st.button("⏮️ 上一课"):
            current_index = current_lesson["order_no"] - 1
            if current_index > 0:
                prev_lesson = next((l for l in lessons if l["order_no"] == current_index), None)
                if prev_lesson:
                    st.session_state.current_lesson = prev_lesson["id"]
                    st.rerun()

    with col_play2:
        if st.button("⏸️ 暂停/播放"):
            st.info("播放/暂停")

    with col_play3:
        if st.button("⏭️ 下一课"):
            current_index = current_lesson["order_no"] + 1
            next_lesson_obj = next((l for l in lessons if l["order_no"] == current_index), None)
            if next_lesson_obj:
                # 标记当前课程为完成
                st.session_state.lesson_progress[st.session_state.current_lesson] = 100
                st.session_state.current_lesson = next_lesson_obj["id"]
                st.rerun()

    with col_play4:
        if st.button("✅ 标记完成"):
            st.session_state.lesson_progress[st.session_state.current_lesson] = 100
            st.success("已标记为完成")

    # 进度条
    current_progress = st.session_state.lesson_progress.get(st.session_state.current_lesson, 0)
    st.progress(current_progress / 100)
    st.caption(f"观看进度: {current_progress}%")

    # 课时描述
    st.divider()
    st.markdown("### 📝 课程说明")
    st.write(current_lesson['description'])

    # 课时资源
    st.markdown("### 📎 课件资源")

    resources = [
        {"name": "课程PPT", "type": "ppt", "size": "2.5MB"},
        {"name": "示例代码", "type": "code", "size": "15KB"},
        {"name": "练习题", "type": "pdf", "size": "500KB"},
    ]

    for res in resources:
        with st.container():
            col_res1, col_res2 = st.columns([4, 1])

            with col_res1:
                st.write(f"📄 {res['name']}")

            with col_res2:
                if st.button("⬇️", key=f'download_{res["name"]}', use_container_width=True):
                    st.success(f"下载中: {res['name']}")


# ============================================================================
# 中间 - 课程大纲
# ============================================================================

with col_sidebar:
    st.subheader("📚 课程大纲")

    # 展开所有课时
    for lesson in lessons:
        is_current = lesson["id"] == st.session_state.current_lesson
        is_completed = lesson.get("completed", False)
        progress = st.session_state.lesson_progress.get(lesson["id"], 0)

        # 状态图标
        if is_completed:
            status_icon = "✅"
        elif progress > 0:
            status_icon = "⏳"
        else:
            status_icon = "⭕"

        with st.expander(
            f"{status_icon} {lesson['title']}",
            expanded=is_current
        ):
            st.caption(f"⏱️ {lesson['duration'] // 60} 分钟")

            if is_current:
                st.info("👈 正在学习")

                # 进度控制
                new_progress = st.slider(
                    "调整进度",
                    0, 100,
                    int(progress),
                    key=f'progress_{lesson["id"]}'
                )
                if new_progress != progress:
                    st.session_state.lesson_progress[lesson["id"]] = new_progress
                    st.rerun()

            else:
                if st.button(f'开始学习', key=f'start_{lesson["id"]}', use_container_width=True):
                    st.session_state.current_lesson = lesson["id"]
                    st.rerun()


# ============================================================================
# 右侧 - 笔记区
# ============================================================================

with col_notes:
    st.subheader("📝 学习笔记")

    # 当前课时笔记
    current_notes = st.session_state.lesson_notes.get(
        st.session_state.current_lesson,
        ""
    )

    # 笔记输入
    notes = st.text_area(
        "记录笔记",
        value=current_notes,
        height=200,
        key="lesson_notes_input",
        help="在这里记录学习要点、疑问和心得"
    )

    # 保存笔记
    if st.button("💾 保存笔记", use_container_width=True):
        st.session_state.lesson_notes[st.session_state.current_lesson] = notes
        st.success("笔记已保存")

    st.divider()

    # 历史笔记
    st.markdown("### 📖 我的笔记")

    note_lessons = [
        (k, v) for k, v in st.session_state.lesson_notes.items() if v
    ]

    if note_lessons:
        for lesson_id, note_text in note_lessons:
            lesson_title = next((l["title"] for l in lessons if l["id"] == lesson_id), lesson_id)

            with st.expander(f"📌 {lesson_title}"):
                st.write(note_text[:100] + "..." if len(note_text) > 100 else note_text)

                if st.button(f'编辑', key=f'edit_note_{lesson_id}'):
                    st.session_state.lesson_notes[st.session_state.current_lesson] = note_text
                    st.rerun()
    else:
        st.caption("还没有笔记，开始记录吧！")


# ============================================================================
# 底部 - 互动问答
# ============================================================================

st.divider()

st.subheader("💬 课间问答")

# 提问输入
question = st.text_input("提出你的问题", key="lesson_question")

if st.button("❓ 提交问题", use_container_width=True):
    st.success("问题已提交，讲师和同学会看到")

# 模拟问答列表
qa_list = [
    {
        "user": "同学A",
        "question": "Python 中列表和元组有什么区别？",
        "answer": "列表是可变的，元组是不可变的。",
        "time": "10分钟前"
    },
    {
        "user": "同学B",
        "question": "如何安装第三方库？",
        "answer": "使用 pip install 命令安装。",
        "time": "30分钟前"
    },
]

for qa in qa_list:
    with st.container():
        col_qa1, col_qa2 = st.columns([4, 1])

        with col_qa1:
            st.markdown(f"**❓ {qa['user']}**")
            st.write(qa['question'])

            if qa.get('answer'):
                st.markdown(f"**💡 讲师回复:**")
                st.info(qa['answer'])

        with col_qa2:
            st.caption(qa['time'])

        st.divider()
'''


# ============================================================================
# 3. QuizSystem - 测验系统模板
# ============================================================================

class QuizSystem:
    """
    测验系统模板

    功能: 题目展示、计时答题、自动评分

    推荐主题: ocean_blue, forest_green

    特性:
        - 多种题型支持
        - 计时功能
        - 自动评分
        - 答案解析
        - 成绩统计
        - 错题回顾
    """

    def __init__(self, quiz: Optional[Quiz] = None):
        """初始化测验系统"""
        self.quiz = quiz or self._get_default_quiz()

    def _get_default_quiz(self) -> Quiz:
        """获取默认测验"""
        return Quiz(
            id="python_basics_quiz",
            course_id="python_101",
            title="Python 基础测验",
            description="测试 Python 基础知识掌握情况",
            duration=30,
            passing_score=60,
            attempts=3,
            questions=[
                Question(
                    id="q1",
                    quiz_id="python_basics_quiz",
                    type=QuestionType.SINGLE_CHOICE,
                    content="Python 中哪个关键字用于定义函数？",
                    options=["def", "function", "define", "func"],
                    correct_answer="def",
                    points=10,
                    explanation="def 是 Python 中定义函数的关键字"
                ),
                Question(
                    id="q2",
                    quiz_id="python_basics_quiz",
                    type=QuestionType.TRUE_FALSE,
                    content="Python 是一种编译型语言",
                    options=["正确", "错误"],
                    correct_answer="错误",
                    points=10,
                    explanation="Python 是解释型语言"
                ),
                Question(
                    id="q3",
                    quiz_id="python_basics_quiz",
                    type=QuestionType.MULTIPLE_CHOICE,
                    content="以下哪些是 Python 的基本数据类型？（多选）",
                    options=["int", "str", "list", "var"],
                    correct_answer=["int", "str", "list"],
                    points=20,
                    explanation="int, str, list 都是 Python 的基本数据类型，var 不是"
                ),
            ]
        )

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
测验系统 - Streamlit 实现
========================

功能: 题目展示、计时答题、自动评分
"""

import streamlit as st
import time


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="测验系统",
    page_icon="📝",
    layout="center"
)


# ============================================================================
# 状态管理
# ============================================================================

if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = "intro"  # intro, taking, result

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_time_remaining" not in st.session_state:
    st.session_state.quiz_time_remaining = 30 * 60  # 30分钟


# ============================================================================
# 测验数据
# ============================================================================

@st.cache_data
def get_quiz():
    """获取测验"""
    return {
        "id": "python_basics_quiz",
        "title": "Python 基础知识测验",
        "description": "测试你对 Python 基础的掌握程度",
        "duration": 30,  # 分钟
        "passing_score": 60,
        "total_points": 100,
        "questions": [
            {
                "id": "q1",
                "type": "single_choice",
                "content": "Python 中哪个关键字用于定义函数？",
                "options": ["def", "function", "define", "func"],
                "correct": "def",
                "points": 10
            },
            {
                "id": "q2",
                "type": "true_false",
                "content": "Python 是一种编译型语言",
                "options": ["正确", "错误"],
                "correct": "错误",
                "points": 10
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "content": "以下哪些是 Python 的基本数据类型？（多选）",
                "options": ["int", "str", "list", "var"],
                "correct": ["int", "str", "list"],
                "points": 20
            },
            {
                "id": "q4",
                "type": "fill_blank",
                "content": "Python 中用于输出内容的函数是 ____",
                "correct": "print",
                "points": 10
            },
            {
                "id": "q5",
                "type": "single_choice",
                "content": "以下哪个不是 Python 的数据类型？",
                "options": ["int", "str", "char", "list"],
                "correct": "char",
                "points": 10
            },
        ]
    }


# ============================================================================
# 测验介绍页
# ============================================================================

if st.session_state.quiz_state == "intro":
    st.title("📝 Python 基础知识测验")

    quiz = get_quiz()

    # 测验信息
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("题目数量", f"{len(quiz['questions'])} 题")

    with col2:
        st.metric("测验时长", f"{quiz['duration']} 分钟")

    with col3:
        st.metric("及格分数", f"{quiz['passing_score']} 分")

    st.divider()

    st.markdown("### 📋 测验说明")

    st.markdown(f"""
    **{quiz['description']}**

    - ⏱️ 时间限制: {quiz['duration']} 分钟
    - ✅ 及格分数: {quiz['passing_score']} 分
    - 🔄 尝试次数: 3 次
    """)

    st.markdown("---")
    st.markdown("### 📊 题目分布")

    question_types = {}
    for q in quiz['questions']:
        qtype = q['type']
        question_types[qtype] = question_types.get(qtype, 0) + 1

    type_cols = st.columns(len(question_types))
    for col, (qtype, count) in zip(type_cols, question_types.items()):
        with col:
            st.metric(qtype.replace('_', ' ').title(), f"{count} 题")

    st.divider()

    # 开始按钮
    if st.button("🚀 开始测验", use_container_width=True, type="primary", size="large"):
        st.session_state.quiz_state = "taking"
        st.session_state.quiz_start_time = time.time()
        st.rerun()


# ============================================================================
# 答题页
# ============================================================================

elif st.session_state.quiz_state == "taking":
    quiz = get_quiz()

    # 顶部计时器
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.title("📝 正在答题...")

    with col2:
        # 倒计时
        if st.session_state.quiz_time_remaining > 0:
            minutes = st.session_state.quiz_time_remaining // 60
            seconds = st.session_state.quiz_time_remaining % 60
            st.metric("⏱️ 剩余时间", f"{minutes:02d}:{seconds:02d}")

            # 自动倒计时
            time.sleep(1)
            st.session_state.quiz_time_remaining -= 1
            st.rerun()
        else:
            st.session_state.quiz_state = "result"
            st.rerun()

    with col3:
        progress = (len(st.session_state.quiz_answers) / len(quiz['questions'])) * 100
        st.metric("进度", f"{len(st.session_state.quiz_answers)}/{len(quiz['questions'])}", delta=f"{progress:.0f}%")

    st.divider()

    # 答题区域
    for i, question in enumerate(quiz['questions']):
        qid = question['id']

        # 跳过已答题目
        if qid in st.session_state.quiz_answers:
            continue

        st.markdown(f"### 题目 {i + 1}")

        # 题目内容
        if question['type'] == 'single_choice':
            answer = st.radio(
                question['content'],
                question['options'],
                key=f"q_{qid}",
                index=None
            )
            if answer:
                st.session_state.quiz_answers[qid] = answer

        elif question['type'] == 'true_false':
            answer = st.radio(
                question['content'],
                question['options'],
                key=f"q_{qid}",
                index=None
            )
            if answer:
                st.session_state.quiz_answers[qid] = answer

        elif question['type'] == 'multiple_choice':
            answer = st.multiselect(
                question['content'],
                question['options'],
                key=f"q_{qid}"
            )
            if st.button('确认答案', key=f'confirm_{qid}'):
                st.session_state.quiz_answers[qid] = answer
                st.rerun()

        elif question['type'] == 'fill_blank':
            answer = st.text_input(
                question['content'],
                key=f"q_{qid}"
            )
            if answer and st.button('提交', key=f'submit_{qid}'):
                st.session_state.quiz_answers[qid] = answer
                st.rerun()

        st.divider()

    # 提交按钮
    answered_count = len(st.session_state.quiz_answers)
    if answered_count == len(quiz['questions']):
        if st.button("✅ 提交答卷", use_container_width=True, type="primary"):
            st.session_state.quiz_state = "result"
            st.rerun()
    else:
        st.info(f"还有 {len(quiz['questions']) - answered_count} 道题目未完成")

    # 暂停/退出
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⏸️ 暂停计时", use_container_width=True):
            st.info("计时已暂停")

    with col2:
        if st.button("🚪 退出测验", use_container_width=True):
            if st.session_state.get("quiz_paused_time"):
                # 恢复之前的状态
                pass
            st.session_state.quiz_state = "intro"
            st.rerun()


# ============================================================================
# 结果页
# ============================================================================

elif st.session_state.quiz_state == "result":
    quiz = get_quiz()

    st.title("🎯 测验结果")

    # 计算分数
    total_score = 0
    correct_count = 0
    results = []

    for question in quiz['questions']:
        qid = question['id']
        user_answer = st.session_state.quiz_answers.get(qid)
        correct_answer = question['correct']

        # 判断是否正确
        if question['type'] == 'multiple_choice':
            is_correct = (
                isinstance(user_answer, list) and
                set(user_answer) == set(correct_answer)
            )
        else:
            is_correct = user_answer == correct_answer

        if is_correct:
            total_score += question['points']
            correct_count += 1

        results.append({
            "question": question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    # 显示分数
    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:
        st.metric("总得分", f"{total_score} / {quiz['total_points']}")

    with score_col2:
        st.metric("正确率", f"{correct_count}/{len(quiz['questions'])}")

    with score_col3:
        is_pass = total_score >= quiz['passing_score']
        if is_pass:
            st.success("✅ 恭喜！你通过了测验")
        else:
            st.error("❌ 很遗憾，未达到及格分数")

    st.divider()

    # 详细结果
    st.markdown("### 📊 答题详情")

    for i, result in enumerate(results, 1):
        question = result['question']
        is_correct = result['is_correct']

        if is_correct:
            st.markdown(f"✅ **第 {i} 题** (正确)")
        else:
            st.markdown(f"❌ **第 {i} 题** (错误)")

        st.write(question['content'])

        col_ans1, col_ans2 = st.columns(2)

        with col_ans1:
            st.write(f"你的答案: **{result['user_answer']}**")

        with col_ans2:
            st.write(f"正确答案: **{result['correct_answer']}**")

        if not is_correct:
            st.info(f"💡 解析: {question.get('explanation', '暂无解析')}")

        st.divider()

    # 操作按钮
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("🔄 再测一次", use_container_width=True):
            st.session_state.quiz_state = "intro"
            st.session_state.quiz_answers = {}
            st.session_state.quiz_time_remaining = 30 * 60
            st.rerun()

    with col_btn2:
        if st.button("📥 导出结果", use_container_width=True):
            st.success("结果导出中...")

    with col_btn3:
        if st.button("🔙 返回课程", use_container_width=True):
            st.info("返回课程页面")
'''


# ============================================================================
# 4. ProgressTracker - 学习进度模板
# ============================================================================

class ProgressTracker:
    """
    学习进度跟踪模板

    功能: 完成率统计、徽章系统、排行榜

    推荐主题: forest_green, spring_blossom

    特性:
        - 课程进度
        - 学习时长统计
        - 成就徽章
        - 学习排行榜
        - 连续学习打卡
    """

    def __init__(self):
        """初始化进度跟踪器"""
        self._badges = self._get_default_badges()

    def _get_default_badges(self) -> List[Badge]:
        """获取默认徽章列表"""
        return [
            Badge(
                id="first_course",
                name="初出茅庐",
                description="完成第一门课程",
                icon="🌱",
                type=BadgeType.MILESTONE,
                requirement="完成任意一门课程"
            ),
            Badge(
                id="week_streak",
                name="持之以恒",
                description="连续学习7天",
                icon="🔥",
                type=BadgeType.STREAK,
                requirement="连续7天有学习记录"
            ),
            Badge(
                id="quiz_master",
                name="测验达人",
                description="测验得分超过90分",
                icon="🏆",
                type=BadgeType.ACHIEVEMENT,
                requirement="任意测验得分90分以上"
            ),
        ]

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
学习进度跟踪 - Streamlit 实现
================================

功能: 完成率统计、徽章系统、排行榜
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="学习进度",
    page_icon="📈",
    layout="wide"
)


# ============================================================================
# 模拟数据
# ============================================================================

@st.cache_data
def get_user_progress():
    """获取用户学习进度"""
    return {
        "total_courses": 12,
        "completed_courses": 3,
        "in_progress_courses": 5,
        "total_hours": 156,
        "this_week_hours": 12,
        "last_learn_date": datetime.now() - timedelta(hours=2),
        "streak_days": 7,
        "quiz_count": 15,
        "quiz_avg_score": 85.5
    }


@st.cache_data
def get_course_progress():
    """获取课程进度详情"""
    return [
        {
            "title": "Python 零基础入门",
            "category": "编程开发",
            "progress": 100,
            "status": "completed",
            "last_study": datetime.now() - timedelta(days=5)
        },
        {
            "title": "数据分析与可视化",
            "category": "数据分析",
            "progress": 65,
            "status": "in_progress",
            "last_study": datetime.now() - timedelta(hours=2)
        },
        {
            "title": "UI/UX 设计实战",
            "category": "产品设计",
            "progress": 30,
            "status": "in_progress",
            "last_study": datetime.now() - timedelta(days=1)
        },
        {
            "title": "人工智能基础",
            "category": "人工智能",
            "progress": 0,
            "status": "not_started",
            "last_study": None
        },
    ]


@st.cache_data
def get_badges():
    """获取徽章列表"""
    return [
        {
            "id": "first_lesson",
            "name": "初学者",
            "icon": "🌱",
            "earned": True,
            "earned_date": datetime.now() - timedelta(days=30)
        },
        {
            "id": "week_streak",
            "name": "坚持不懈",
            "icon": "🔥",
            "earned": True,
            "earned_date": datetime.now() - timedelta(days=1)
        },
        {
            "id": "first_course",
            "name": "初出茅庐",
            "icon": "🎓",
            "earned": True,
            "earned_date": datetime.now() - timedelta(days=15)
        },
        {
            "id": "perfect_quiz",
            "name": "满分状元",
            "icon": "💯",
            "earned": False,
            "earned_date": None
        },
        {
            "id": "month_study",
            "name": "月度学霸",
            "icon": "📚",
            "earned": False,
            "earned_date": None
        },
    ]


@st.cache_data
def get_leaderboard():
    """获取排行榜"""
    return [
        {"rank": 1, "name": "学习之星", "points": 5280, "courses": 12},
        {"rank": 2, "name": "知识探索者", "points": 4950, "courses": 11},
        {"rank": 3, "name": "编程爱好者", "points": 4520, "courses": 10},
        {"rank": 4, "name": "数据分析师", "points": 4280, "courses": 9},
        {"rank": 5, "name": "设计大师", "points": 3960, "courses": 8},
        {"rank": 6, "name": "我", "points": 3240, "courses": 6},
    ]


# ============================================================================
# 主界面
# ============================================================================

st.title("📈 我的学习进度")


# ============================================================================
# 总体统计卡片
# ============================================================================

progress = get_user_progress()

stat_cols = st.columns(5)

with stat_cols[0]:
    st.metric("已完课程", f"{progress['completed_courses']} 门")

with stat_cols[1]:
    st.metric("学习中", f"{progress['in_progress_courses']} 门")

with stat_cols[2]:
    st.metric("学习时长", f"{progress['total_hours']} 小时")

with stat_cols[3]:
    st.metric("本周学习", f"{progress['this_week_hours']} 小时")

with stat_cols[4]:
    streak_icon = "🔥" if progress['streak_days'] >= 7 else "📍"
    st.metric(streak_icon, f"{progress['streak_days']} 天", help="连续学习天数")


# ============================================================================
# 学习目标
# ============================================================================

st.divider()

st.subheader("🎯 学习目标")

col_goal1, col_goal2 = st.columns(2)

with col_goal1:
    st.markdown("#### 年度学习目标")
    target_courses = 10
    completed = progress['completed_courses']
    goal_progress = completed / target_courses * 100

    st.write(f"完成 {target_courses} 门课程")
    st.progress(completed / target_courses)
    st.caption(f"已完成 {completed}/{target_courses} 门 ({goal_progress:.0f}%)")

with col_goal2:
    st.markdown("#### 学习时长目标")
    target_hours = 200
    current_hours = progress['total_hours']
    hours_progress = current_hours / target_hours * 100

    st.write(f"学习 {target_hours} 小时")
    st.progress(current_hours / target_hours)
    st.caption(f"已完成 {current_hours}/{target_hours} 小时 ({hours_progress:.0f}%)")


# ============================================================================
# 课程进度详情
# ============================================================================

st.divider()

st.subheader("📚 课程进度")

course_progress = get_course_progress()

for course in course_progress:
    with st.container():
        # 状态图标
        if course['status'] == 'completed':
            status_icon = "✅"
            status_text = "已完成"
            status_color = "green"
        elif course['status'] == 'in_progress':
            status_icon = "⏳"
            status_text = "学习中"
            status_color = "blue"
        else:
            status_icon = "⭕"
            status_text = "未开始"
            status_color = "gray"

        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.markdown(f"### {status_icon} {course['title']}")
            st.caption(f"📂 {course['category']}")

        with col2:
            st.write(f"{status_text}")
            st.progress(course['progress'] / 100)

        with col3:
            st.metric("", f"{course['progress']}%", label_visibility="collapsed")

        # 最近学习时间
        if course['last_study']:
            days_ago = (datetime.now() - course['last_study']).days
            if days_ago == 0:
                last_study = "今天"
            elif days_ago == 1:
                last_study = "昨天"
            else:
                last_study = f"{days_ago} 天前"
            st.caption(f"最后学习: {last_study}")

        st.divider()


# ============================================================================
# 徽章系统
# ============================================================================

st.divider()

st.subheader("🏆 成就徽章")

badges = get_badges()

# 统计
earned_count = sum(1 for b in badges if b['earned'])
total_count = len(badges)

st.caption(f"已获得 {earned_count}/{total_count} 个徽章")

# 徽章网格展示
badge_cols = st.columns(5)

for i, badge in enumerate(badges):
    with badge_cols[i % 5]:
        if badge['earned']:
            st.markdown(f"""
            <div style='text-align: center; padding: 10px; background: #f0f9ff; border-radius: 8px; border: 2px solid #007bff;'>
                <div style='font-size: 32px;'>{badge['icon']}</div>
                <p style='margin: 5px 0; font-weight: bold;'>{badge['name']}</p>
                <p style='color: #007bff; font-size: 12px;'>✓ 已获得</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: center; padding: 10px; background: #f5f5f5; border-radius: 8px; opacity: 0.5;'>
                <div style='font-size: 32px;'>🔒</div>
                <p style='margin: 5px 0; color: #999;'>{badge['name']}</p>
                <p style='color: #999; font-size: 12px;'>未解锁</p>
            </div>
            """, unsafe_allow_html=True)


# ============================================================================
# 学习排行榜
# ============================================================================

st.divider()

st.subheader("🏅 学习排行榜")

leaderboard = get_leaderboard()

# 前三名特殊显示
top_3 = leaderboard[:3]

col_rank1, col_rank2, col_rank3 = st.columns(3)

with col_rank1:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ffd700, #ffed4e); border-radius: 8px;'>
        <div style='font-size: 48px;'>🥇</div>
        <h3>{top_3[0]['name']}</h3>
        <p>{top_3[0]['points']} 积分</p>
    </div>
    """, unsafe_allow_html=True)

with col_rank2:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #c0c0c0, #e8e8e8); border-radius: 8px;'>
        <div style='font-size: 48px;'>🥈</div>
        <h3>{top_3[1]['name']}</h3>
        <p>{top_3[1]['points']} 积分</p>
    </div>
    """, unsafe_allow_html=True)

with col_rank3:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #cd7f32, #e8a87c); border-radius: 8px;'>
        <div style='font-size: 48px;'>🥉</div>
        <h3>{top_3[2]['name']}</h3>
        <p>{top_3[2]['points']} 积分</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 其余排名
for entry in leaderboard[3:]:
    col_entry1, col_entry2, col_entry3 = st.columns([1, 4, 2])

    with col_entry1:
        st.write(f"**#{entry['rank']}**")

    with col_entry2:
        st.write(entry['name'])

    with col_entry3:
        st.write(f"{entry['points']} 积分")


# ============================================================================
# 本周学习统计
# ============================================================================

st.divider()

st.subheader("📊 本周学习统计")

# 模拟每日学习时长
daily_hours = [1.5, 2.0, 0.5, 3.0, 2.5, 1.0, 2.0]
days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

import plotly.express as px

df_weekly = pd.DataFrame({
    "day": days,
    "hours": daily_hours
})

fig = px.bar(df_weekly, x="day", y="hours", title="每日学习时长（小时）")
fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))

st.plotly_chart(fig, use_container_width=True)

# 统计
col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    total_week_hours = sum(daily_hours)
    st.metric("本周总时长", f"{total_week_hours:.1f} 小时")

with col_stat2:
    avg_daily = sum(daily_hours) / len(daily_hours)
    st.metric("日均学习", f"{avg_daily:.1f} 小时")

with col_stat3:
    max_day = days[daily_hours.index(max(daily_hours))]
    st.metric("最活跃日", max_day)
'''


# ============================================================================
# 5. DiscussionForum - 讨论区模板
# ============================================================================

class DiscussionForum:
    """
    讨论区模板

    功能: 问答互动、回复评论、点赞点赞

    推荐主题: ocean_blue, spring_blossom

    特性:
        - 发帖提问
        - 回复评论
        - 点赞功能
        - 最佳答案
        - 热门话题
        - 搜索筛选
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
讨论区 - Streamlit 实现
=======================

功能: 问答互动、回复评论、点赞功能
"""

import streamlit as st
from datetime import datetime


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="讨论区",
    page_icon="💬",
    layout="wide"
)


# ============================================================================
# 状态管理
# ============================================================================

if "forum_posts" not in st.session_state:
    st.session_state.forum_posts = [
        {
            "id": "post_1",
            "type": "question",
            "author": "同学A",
            "title": "Python 中列表推导式怎么用？",
            "content": "我想了解列表推导式的用法，有没有简单的例子？",
            "course": "Python 零基础入门",
            "tags": ["Python", "列表推导式"],
            "created_at": datetime.now() - timedelta(hours=2),
            "likes": 15,
            "replies": 3,
            "views": 128,
            "is_solved": True
        },
        {
            "id": "post_2",
            "type": "discussion",
            "author": "同学B",
            "title": "分享我的学习笔记",
            "content": "这是我整理的 Python 学习笔记，希望对大家有帮助...",
            "course": None,
            "tags": ["学习笔记", "Python"],
            "created_at": datetime.now() - timedelta(hours=5),
            "likes": 32,
            "replies": 8,
            "views": 256,
            "is_solved": False
        },
        {
            "id": "post_3",
            "type": "question",
            "author": "同学C",
            "title": "安装第三方库失败怎么办？",
            "content": "我用 pip install 安装包的时候报错，显示权限不足...",
            "course": None,
            "tags": ["安装", "pip", "错误"],
            "created_at": datetime.now() - timedelta(hours=8),
            "likes": 8,
            "replies": 2,
            "views": 89,
            "is_solved": False
        },
    ]

if "post_replies" not in st.session_state:
    st.session_state.post_replies = {
        "post_1": [
            {
                "id": "reply_1",
                "author": "助教小张",
                "content": "列表推导式是 Python 的特色功能，可以快速创建列表。",
                "is_best_answer": True,
                "created_at": datetime.now() - timedelta(hours=1),
                "likes": 25
            },
            {
                "id": "reply_2",
                "author": "同学D",
                "content": "我也想学习这个！",
                "is_best_answer": False,
                "created_at": datetime.now() - timedelta(minutes=30),
                "likes": 2
            },
        ]
    }


# ============================================================================
# 主界面
# ============================================================================

st.title("💬 课程讨论区")


# ============================================================================
# 顶部操作栏
# ============================================================================

with st.container():
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    with col1:
        search = st.text_input("🔍 搜索话题", placeholder="输入关键词...")

    with col2:
        post_type = st.selectbox(
            "帖子类型",
            ["全部", "提问", "讨论", "分享", "公告"]
        )

    with col3:
        sort_by = st.selectbox(
            "排序方式",
            ["最新", "热门", "待解决"]
        )

    with col4:
        if st.button("➕ 发布新帖", use_container_width=True, type="primary"):
            st.session_state.show_new_post_form = True
            st.rerun()


# ============================================================================
# 新帖表单
# ============================================================================

if st.session_state.get("show_new_post_form", False):
    st.subheader("✍️ 发布新帖")

    with st.form("new_post_form"):
        title = st.text_input("标题*", placeholder="简明扼要地描述问题或话题")

        post_type_select = st.radio(
            "帖子类型",
            ["❓ 提问", "💬 讨论", "📢 分享", "📢 公告"],
            horizontal=True
        )

        course = st.selectbox(
            "关联课程（可选）",
            ["", "Python 零基础入门", "数据分析与可视化", "UI/UX 设计实战"]
        )

        tags = st.text_input("标签（逗号分隔）", placeholder="Python, 列表")

        content = st.text_area(
            "内容*",
            height=200,
            placeholder="详细描述你的问题或分享内容..."
        )

        col_submit, col_cancel = st.columns(2)

        with col_submit:
            submitted = st.form_submit_button("📤 发布", use_container_width=True)

        with col_cancel:
            if st.form_submit_button("取消", use_container_width=True):
                st.session_state.show_new_post_form = False
                st.rerun()

    if submitted:
        if title and content:
            # 创建新帖
            new_post = {
                "id": f"post_{len(st.session_state.forum_posts) + 1}",
                "type": post_type_select.split()[1],
                "author": "我",
                "title": title,
                "content": content,
                "course": course if course else None,
                "tags": [t.strip() for t in tags.split(",") if tags],
                "created_at": datetime.now(),
                "likes": 0,
                "replies": 0,
                "views": 0,
                "is_solved": False
            }
            st.session_state.forum_posts.insert(0, new_post)
            st.session_state.show_new_post_form = False
            st.success("✅ 帖子发布成功！")
            st.rerun()
        else:
            st.error("请填写标题和内容")

    st.divider()


# ============================================================================
# 帖子列表
# ============================================================================

st.subheader("📋 话题列表")

# 应用筛选和排序
filtered_posts = st.session_state.forum_posts.copy()

if post_type != "全部":
    filtered_posts = [p for p in filtered_posts if p["type"] == post_type]

if search:
    search_lower = search.lower()
    filtered_posts = [
        p for p in filtered_posts
        if search_lower in p["title"].lower() or
           search_lower in p["content"].lower() or
           any(search_lower in tag.lower() for tag in p["tags"])
    ]

if sort_by == "最新":
    filtered_posts.sort(key=lambda x: x["created_at"], reverse=True)
elif sort_by == "热门":
    filtered_posts.sort(key=lambda x: x["likes"], reverse=True)
elif sort_by == "待解决":
    filtered_posts = [p for p in filtered_posts if p["type"] == "question" and not p["is_solved"]]

# 显示帖子
for post in filtered_posts:
    with st.container():
        # 帖子头部
        col_header1, col_header2 = st.columns([4, 1])

        with col_header1:
            # 类型图标
            type_icons = {"question": "❓", "discussion": "💬", "share": "📢", "announcement": "📢"}
            type_icon = type_icons.get(post["type"], "📄")

            # 已解决标识
            solved_badge = "✅ 已解决" if post.get("is_solved") else ""
            if post["type"] == "question" and not post.get("is_solved"):
                solved_badge = "🔴 待解决"

            st.markdown(f"### {type_icon} {post['title']} {solved_badge}")

        with col_header2:
            # 状态标识
            if post.get("is_solved"):
                st.success("✅")

        # 帖子元信息
        col_meta1, col_meta2, col_meta3 = st.columns(3)

        with col_meta1:
            st.caption(f"👤 {post['author']}")

        with col_meta2:
            time_diff = datetime.now() - post["created_at"]
            if time_diff.days > 0:
                time_str = f"{time_diff.days}天前"
            elif time_diff.seconds >= 3600:
                hours = time_diff.seconds // 3600
                time_str = f"{hours}小时前"
            else:
                minutes = time_diff.seconds // 60
                time_str = f"{minutes}分钟前"
            st.caption(f"🕐 {time_str}")

        with col_meta3:
            if post.get("course"):
                st.caption(f"📚 {post['course']}")

        # 标签
        if post["tags"]:
            tag_cols = st.columns(len(post["tags"]))
            for tag_col, tag in zip(tag_cols, post["tags"]):
                with tag_col:
                    st.caption(f"#{tag}")

        # 帖子内容
        with st.expander("查看内容"):
            st.write(post["content"])

        # 互动数据
        col互动1, col互动2, col互动3 = st.columns(3)

        with col互动1:
            st.button(f'👍 {post["likes"]}', key=f'like_{post["id"]}', help="点赞")

        with col互动2:
            st.button(f'💬 {post["replies"]}', key=f'reply_{post["id"]}', help="回复")

        with col互动3:
            st.button(f'👁️ {post["views"]}', key=f'view_{post["id"]}', help="浏览")

        st.divider()


# ============================================================================
# 帖子详情（展开时显示）
# ============================================================================

# 这里可以添加查看回复、添加回复等功能
# 在实际应用中，点击帖子会进入详情页
'''


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "CourseLevel",
    "CourseStatus",
    "EnrollmentStatus",
    "QuestionType",
    "BadgeType",
    "PostType",
    # 数据类
    "Course",
    "Lesson",
    "Question",
    "Quiz",
    "Badge",
    "ForumPost",
    # 模板类
    "CourseCatalog",
    "LessonPlayer",
    "QuizSystem",
    "ProgressTracker",
    "DiscussionForum",
]
