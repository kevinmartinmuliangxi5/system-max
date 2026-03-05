"""
CMS Industry Templates - 内容管理系统行业模板
===============================================

包含内容管理系统专用的 5 个完整页面模板：

模板列表:
    1. ArticleEditor - 文章编辑器（富文本、预览、发布）
    2. MediaLibrary - 媒体库（上传、分类、搜索）
    3. ContentList - 内容列表（状态、操作、批量）
    4. CategoryManager - 分类管理（树形、拖拽排序）
    5. SEOPanel - SEO 设置（标题、描述、关键词）

推荐主题:
    - default_light: 适合日间使用的 CMS
    - midnight_blue: 适合夜间使用的 CMS
    - corporate_gray: 适合企业级 CMS

使用方式:
    from ui_library.industries.cms import (
        ArticleEditor,
        MediaLibrary,
        ContentList,
        CategoryManager,
        SEOPanel,
    )
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import pandas as pd
from datetime import datetime
from pathlib import Path


# ============================================================================
# 枚举定义
# ============================================================================

class ContentStatus(Enum):
    """内容状态"""
    DRAFT = "draft"               # 草稿
    PENDING_REVIEW = "pending"    # 待审核
    PUBLISHED = "published"       # 已发布
    ARCHIVED = "archived"         # 已归档
    SCHEDULED = "scheduled"       # 定时发布


class ContentType(Enum):
    """内容类型"""
    ARTICLE = "article"           # 文章
    PAGE = "page"                 # 页面
    POST = "post"                 # 帖子
    NEWS = "news"                 # 新闻
    PRODUCT = "product"           # 产品


class MediaType(Enum):
    """媒体类型"""
    IMAGE = "image"               # 图片
    VIDEO = "video"               # 视频
    AUDIO = "audio"               # 音频
    DOCUMENT = "document"         # 文档
    OTHER = "other"               # 其他


class EditorMode(Enum):
    """编辑器模式"""
    WRITE = "write"               # 编辑模式
    PREVIEW = "preview"           # 预览模式
    SPLIT = "split"               # 分屏模式


# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class Article:
    """
    文章定义

    Attributes:
        id: 文章ID
        title: 标题
        slug: URL 别名
        content: 内容
        excerpt: 摘要
        author: 作者
        category_id: 分类ID
        tags: 标签
        featured_image: 特色图片
        status: 状态
        published_at: 发布时间
        created_at: 创建时间
        updated_at: 更新时间
        seo_title: SEO 标题
        seo_description: SEO 描述
        seo_keywords: SEO 关键词
    """
    id: str
    title: str
    slug: str
    content: str
    excerpt: str
    author: str
    category_id: Optional[str]
    tags: List[str]
    featured_image: Optional[str]
    status: ContentStatus
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "excerpt": self.excerpt,
            "author": self.author,
            "category_id": self.category_id,
            "tags": self.tags,
            "featured_image": self.featured_image,
            "status": self.status.value,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "seo_title": self.seo_title,
            "seo_description": self.seo_description,
            "seo_keywords": self.seo_keywords,
        }


@dataclass
class MediaFile:
    """
    媒体文件定义

    Attributes:
        id: 文件ID
        filename: 文件名
        url: 访问URL
        type: 媒体类型
        size: 文件大小（字节）
        dimensions: 尺寸 (width, height) 用于图片
        alt_text: 替代文本
        category_id: 分类ID
        tags: 标签
        uploaded_at: 上传时间
        uploader: 上传者
    """
    id: str
    filename: str
    url: str
    type: MediaType
    size: int
    dimensions: Optional[Tuple[int, int]]
    alt_text: str
    category_id: Optional[str]
    tags: List[str]
    uploaded_at: datetime
    uploader: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "filename": self.filename,
            "url": self.url,
            "type": self.type.value,
            "size": self.size,
            "dimensions": self.dimensions,
            "alt_text": self.alt_text,
            "category_id": self.category_id,
            "tags": self.tags,
            "uploaded_at": self.uploaded_at.isoformat(),
            "uploader": self.uploader,
        }


@dataclass
class Category:
    """
    分类定义

    Attributes:
        id: 分类ID
        name: 分类名称
        slug: URL 别名
        parent_id: 父分类ID
        description: 描述
        icon: 图标
        color: 颜色
        order: 排序
        post_count: 文章数量
    """
    id: str
    name: str
    slug: str
    parent_id: Optional[str]
    description: str
    icon: Optional[str]
    color: Optional[str]
    order: int
    post_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "parent_id": self.parent_id,
            "description": self.description,
            "icon": self.icon,
            "color": self.color,
            "order": self.order,
            "post_count": self.post_count,
        }


@dataclass
class SEOSettings:
    """
    SEO 设置定义

    Attributes:
        title: 页面标题
        description: 页面描述
        keywords: 关键词
        og_title: Open Graph 标题
        og_description: Open Graph 描述
        og_image: Open Graph 图片
        canonical_url: 规范URL
        noindex: 是否禁止索引
        priority: 优先级
    """
    title: str
    description: str
    keywords: List[str]
    og_title: Optional[str]
    og_description: Optional[str]
    og_image: Optional[str]
    canonical_url: Optional[str]
    noindex: bool
    priority: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "og_title": self.og_title,
            "og_description": self.og_description,
            "og_image": self.og_image,
            "canonical_url": self.canonical_url,
            "noindex": self.noindex,
            "priority": self.priority,
        }


# ============================================================================
# 1. ArticleEditor - 文章编辑器模板
# ============================================================================

class ArticleEditor:
    """
    文章编辑器模板

    功能: 富文本编辑、实时预览、发布管理

    推荐主题: default_light, midnight_blue

    特性:
        - Markdown 编辑
        - 实时预览
        - 自动保存
        - 版本历史
        - 发布设置
        - SEO 配置
    """

    def __init__(self):
        """初始化文章编辑器"""
        self._articles = {}
        self._drafts = {}

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
文章编辑器 - Streamlit 实现
============================

功能: 富文本编辑、实时预览、发布管理
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import json


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="文章编辑器",
    page_icon="✍️",
    layout="wide"
)


# ============================================================================
# 状态管理
# ============================================================================

if "editor_mode" not in st.session_state:
    st.session_state.editor_mode = "write"  # write, preview, split

if "article_content" not in st.session_state:
    st.session_state.article_content = ""

if "article_title" not in st.session_state:
    st.session_state.article_title = ""

if "article_autosave" not in st.session_state:
    st.session_state.article_autosave = True

if "article_revisions" not in st.session_state:
    st.session_state.article_revisions = []


# ============================================================================
# 顶部操作栏
# ============================================================================

st.title("✍️ 文章编辑器")

# 工具栏
col_toolbar1, col_toolbar2, col_toolbar3, col_toolbar4 = st.columns(4)

with col_toolbar1:
    mode = st.radio(
        "编辑模式",
        ["✏️ 编辑", "👁️ 预览", "⬛ 分屏"],
        horizontal=True,
        index=["write", "preview", "split"].index(st.session_state.editor_mode)
    )
    mode_map = {"✏️ 编辑": "write", "👁️ 预览": "preview", "⬛ 分屏": "split"}
    new_mode = mode_map[mode]
    if new_mode != st.session_state.editor_mode:
        st.session_state.editor_mode = new_mode

with col_toolbar2:
    autosave = st.checkbox("自动保存", value=st.session_state.article_autosave)
    st.session_state.article_autosave = autosave
    if autosave:
        st.caption("💾 每30秒自动保存")

with col_toolbar3:
    st.metric("字数", f"{len(st.session_state.article_content):,}")

with col_toolbar4:
    if st.button("📜 版本历史", use_container_width=True):
        st.info("版本历史功能开发中")

st.divider()


# ============================================================================
# 分屏预览模式
# ============================================================================

if st.session_state.editor_mode == "split":
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📝 编辑区")

        # 标题输入
        title = st.text_input(
            "文章标题",
            value=st.session_state.article_title,
            placeholder="输入引人注目的标题..."
        )
        st.session_state.article_title = title

        st.divider()

        # 内容编辑
        content = st.text_area(
            "文章内容",
            value=st.session_state.article_content,
            height=500,
            placeholder="支持 Markdown 语法，在这里开始写作...",
            label_visibility="collapsed"
        )
        st.session_state.article_content = content

    with col_right:
        st.subheader("👁️ 预览区")

        if title:
            st.markdown(f"# {title}")

        if content:
            st.markdown(content)
        else:
            st.info("👈 在左侧编辑内容，这里会实时显示预览")

elif st.session_state.editor_mode == "write":
    st.subheader("📝 编辑区")

    # 标题输入
    title = st.text_input(
        "文章标题",
        value=st.session_state.article_title,
        placeholder="输入引人注目的标题..."
    )
    st.session_state.article_title = title

    st.divider()

    # Markdown 工具栏
    col_md1, col_md2, col_md3, col_md4, col_md5 = st.columns(5)

    with col_md1:
        if st.button("**B**", help="粗体"):
            if st.session_state.article_content:
                st.session_state.article_content += "**粗体**"
                st.rerun()

    with col_md2:
        if st.button("*I*", help="斜体"):
            if st.session_state.article_content:
                st.session_state.article_content += "*斜体*"
                st.rerun()

    with col_md3:
        if st.button("# H1", help="一级标题"):
            if st.session_state.article_content:
                st.session_state.article_content += "\n# 一级标题\n"
                st.rerun()

    with col_md4:
        if st.button("> 引用", help="引用块"):
            if st.session_state.article_content:
                st.session_state.article_content += "\n> 引用内容\n"
                st.rerun()

    with col_md5:
        if st.button("- 列表", help="列表"):
        if st.session_state.article_content:
            st.session_state.article_content += "\n- 列表项\n"
            st.rerun()

    st.divider()

    # 内容编辑
    content = st.text_area(
        "文章内容",
        value=st.session_state.article_content,
        height=600,
        placeholder="支持 Markdown 语法...",
        label_visibility="collapsed"
    )
    st.session_state.article_content = content

elif st.session_state.editor_mode == "preview":
    st.subheader("👁️ 预览区")

    if st.session_state.article_title:
        st.markdown(f"# {st.session_state.article_title}")
        st.divider()

    if st.session_state.article_content:
        st.markdown(st.session_state.article_content)
    else:
        st.info("👈 切换到编辑模式开始写作")


# ============================================================================
# 侧边栏 - 发布设置
# ============================================================================

st.sidebar.title("⚙️ 发布设置")

# 文章状态
st.sidebar.subheader("📋 文章状态")

status_options = {
    "draft": "草稿",
    "pending": "待审核",
    "published": "已发布",
    "scheduled": "定时发布",
}

status = st.sidebar.selectbox(
    "当前状态",
    list(status_options.keys()),
    format_func=lambda x: status_options[x],
    index=0
)

if status == "scheduled":
    pub_date = st.sidebar.date_input("发布日期", value=datetime.now().date())
    pub_time = st.sidebar.time_input("发布时间", value=datetime.now().time())

# 分类选择
st.sidebar.divider()
st.sidebar.subheader("📂 分类")

categories = ["技术", "生活", "旅行", "美食", "科技"]
selected_category = st.sidebar.selectbox("选择分类", categories)

# 标签输入
st.sidebar.divider()
st.sidebar.subheader("🏷️ 标签")

tags = st.sidebar.text_input("标签（逗号分隔）", placeholder="Python, 教程, 新手")

if tags:
    tag_list = [t.strip() for t in tags.split(",")]
    for tag in tag_list:
        st.sidebar.caption(f"#{tag}")

# 特色图片
st.sidebar.divider()
st.sidebar.subheader("🖼️ 特色图片")

uploaded_file = st.sidebar.file_uploader(
    "上传封面图",
    type=["png", "jpg", "jpeg"],
    help="推荐尺寸: 1200x630"
)

if uploaded_file:
    st.sidebar.image(uploaded_file, use_container_width=True)
    st.sidebar.success("图片已上传")

# 摘要
st.sidebar.divider()
st.sidebar.subheader("📝 摘要")

excerpt = st.sidebar.text_area(
    "文章摘要",
    placeholder="简短描述文章内容，用于搜索结果展示...",
    height=100
)

# SEO 设置
st.sidebar.divider()
st.sidebar.subheader("🔍 SEO 设置")

seo_title = st.sidebar.text_input("SEO 标题", placeholder="留空则使用文章标题")
seo_desc = st.sidebar.text_area("SEO 描述", height=80)
seo_keywords = st.sidebar.text_input("SEO 关键词", placeholder="关键词1, 关键词2")

# 发布按钮
st.sidebar.divider()

col_pub1, col_pub2 = st.columns(2)

with col_pub1:
    if st.button("💾 保存草稿", use_container_width=True):
        # 保存草稿
        draft_data = {
            "title": st.session_state.article_title,
            "content": st.session_state.article_content,
            "status": "draft",
            "saved_at": datetime.now().isoformat()
        }
        st.session_state.article_revisions.append(draft_data)
        st.success("✅ 草稿已保存")

with col_pub2:
    if st.button("🚀 发布文章", use_container_width=True, type="primary"):
        if st.session_state.article_title and st.session_state.article_content:
            # 发布文章
            st.success(f"✅ 文章 '{st.session_state.article_title}' 已发布！")
        else:
            st.error("❌ 请填写标题和内容")


# ============================================================================
# 底部统计
# ============================================================================

st.divider()

st.caption("💡 提示：支持 Markdown 语法，可以使用 **粗体**、*斜体*、# 标题 等格式")
'''


# ============================================================================
# 2. MediaLibrary - 媒体库模板
# ============================================================================

class MediaLibrary:
    """
    媒体库模板

    功能: 文件上传、分类管理、搜索筛选

    推荐主题: default_light, midnight_blue

    特性:
        - 拖拽上传
        - 媒体分类
        - 批量操作
        - 搜索过滤
        - 图片预览
        - 文件管理
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
媒体库 - Streamlit 实现
========================

功能: 文件上传、分类管理、搜索筛选
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="媒体库",
    page_icon="🖼️",
    layout="wide"
)


# ============================================================================
# 模拟媒体数据
# ============================================================================

@st.cache_data
def get_media_files():
    """获取媒体文件列表"""
    return [
        {
            "id": "img_001",
            "filename": "hero-banner.jpg",
            "type": "image",
            "size": 256000,
            "dimensions": (1920, 630),
            "url": "/media/hero-banner.jpg",
            "alt": "首页横幅图",
            "category": "banner",
            "uploaded_at": datetime(2024, 1, 15, 10, 30),
            "uploader": "管理员"
        },
        {
            "id": "img_002",
            "filename": "product-1.png",
            "type": "image",
            "size": 128000,
            "dimensions": (800, 600),
            "url": "/media/product-1.png",
            "alt": "产品图1",
            "category": "product",
            "uploaded_at": datetime(2024, 1, 14, 15, 45),
            "uploader": "编辑"
        },
        {
            "id": "img_003",
            "filename": "team-photo.jpg",
            "type": "image",
            "size": 512000,
            "dimensions": (1600, 900),
            "url": "/media/team-photo.jpg",
            "alt": "团队合影",
            "category": "team",
            "uploaded_at": datetime(2024, 1, 12, 9, 0),
            "uploader": "管理员"
        },
        {
            "id": "video_001",
            "filename": "intro-video.mp4",
            "type": "video",
            "size": 25600000,
            "dimensions": None,
            "url": "/media/intro-video.mp4",
            "alt": "产品介绍视频",
            "category": "video",
            "uploaded_at": datetime(2024, 1, 10, 14, 20),
            "uploader": "内容组"
        },
    ]


# ============================================================================
# 状态管理
# ============================================================================

if "media_category" not in st.session_state:
    st.session_state.media_category = "all"

if "media_type" not in st.session_state:
    st.session_state.media_type = "all"

if "media_search" not in st.session_state:
    st.session_state.media_search = ""

if "selected_media" not in st.session_state:
    st.session_state.selected_media = []


# ============================================================================
# 主界面
# ============================================================================

st.title("🖼️ 媒体库")

# ============================================================================
# 上传区域
# ============================================================================

st.subheader("📤 上传媒体")

with st.container():
    # 拖拽上传区域
    st.markdown("""
    <div style='border: 2px dashed #ccc; padding: 40px; text-align: center; border-radius: 8px;'>
        <div style='font-size: 48px;'>📁</div>
        <p>拖拽文件到这里上传</p>
        <p style='color: #999;'>或</p>
    </div>
    """, unsafe_allow_html=True)

    # 文件选择
    uploaded_files = st.file_uploader(
        "选择文件",
        type=["png", "jpg", "jpeg", "gif", "mp4", "pdf", "doc", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        for file in uploaded_files:
            st.success(f"✅ 已上传: {file.name}")

    # 上传选项
    col_upload1, col_upload2, col_upload3 = st.columns(3)

    with col_upload1:
        # 分类选择
        categories = ["", "banner", "product", "team", "video", "document", "other"]
        category = st.selectbox("选择分类", categories)

    with col_upload2:
        # 批量命名
        batch_name = st.text_input("批量命名前缀", placeholder="img-")

    with col_upload3:
        # 图片压缩
        compress = st.checkbox("上传后压缩", value=True)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("📤 上传所有文件", use_container_width=True):
            st.info("正在上传...")

    with col_btn2:
        if st.button("取消", use_container_width=True):
            st.info("已取消上传")

st.divider()


# ============================================================================
# 筛选和搜索
# ============================================================================

st.subheader("🔍 筛选和搜索")

col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)

with col_filter1:
    type_filter = st.selectbox(
        "媒体类型",
        ["全部", "图片", "视频", "音频", "文档"]
    )

with col_filter2:
    category_filter = st.selectbox(
        "分类",
        ["全部", "banner", "product", "team", "video", "document"]
    )

with col_filter3:
    date_filter = st.selectbox(
        "上传时间",
        ["全部", "今天", "本周", "本月", "更早"]
    )

with col_filter4:
    search = st.text_input("🔍 搜索文件", placeholder="输入文件名...")

st.divider()


# ============================================================================
# 媒体网格显示
# ============================================================================

st.subheader("📚 媒体文件")

media_files = get_media_files()

# 应用筛选
filtered_files = media_files.copy()

if type_filter != "全部":
    type_map = {"图片": "image", "视频": "video", "音频": "audio", "文档": "document"}
    filtered_files = [f for f in filtered_files if f["type"] == type_map.get(type_filter)]

if category_filter != "全部":
    filtered_files = [f for f in filtered_files if f.get("category") == category_filter]

if search:
    search_lower = search.lower()
    filtered_files = [
        f for f in filtered_files
        if search_lower in f["filename"].lower() or
        search_lower in f.get("alt", "").lower()
    ]

# 显示统计
st.caption(f"找到 {len(filtered_files)} 个文件")

# 网格显示（每行4个）
if filtered_files:
    grid_cols = st.columns(4)

    for i, media in enumerate(filtered_files):
        col = grid_cols[i % 4]

        with col:
            # 媒体卡片
            is_selected = media["id"] in st.session_state.selected_media

            border_color = "#007bff" if is_selected else "#e0e0e0"

            if media["type"] == "image":
                # 显示图片
                st.markdown(f"""
                <div style='border: 2px solid {border_color}; border-radius: 8px; padding: 10px; text-align: center;'>
                    <div style='background: #f5f5f5; height: 120px; display: flex; align-items: center; justify-content: center; border-radius: 4px;'>
                        <span style='font-size: 32px;'>🖼️</span>
                    </div>
                    <p style='margin: 8px 0 4px 0; font-size: 12px;'>{media['filename'][:20]}...</p>
                </div>
                """, unsafe_allow_html=True)

            else:
                # 显示文件图标
                type_icons = {"video": "🎬", "audio": "🎵", "document": "📄"}
                icon = type_icons.get(media["type"], "📁")

                st.markdown(f"""
                <div style='border: 2px solid {border_color}; border-radius: 8px; padding: 20px; text-align: center;'>
                    <div style='font-size: 48px;'>{icon}</div>
                    <p style='margin: 8px 0 4px 0; font-size: 12px;'>{media['filename'][:20]}...</p>
                </div>
                """, unsafe_allow_html=True)

            # 选择按钮
            if not is_selected:
                if st.button(f'选择', key=f'select_{media["id"]}', use_container_width=True):
                    st.session_state.selected_media.append(media["id"])
                    st.rerun()
            else:
                if st.button(f'✓ 已选', key=f'selected_{media["id"]}', use_container_width=True):
                    st.session_state.selected_media.remove(media["id"])
                    st.rerun()

            # 详情
            with st.expander("详情", expanded=False):
                col_det1, col_det2 = st.columns(2)

                with col_det1:
                    st.caption(f"大小: {media['size'] / 1024:.1f} KB")
                    if media["dimensions"]:
                        st.caption(f"尺寸: {media['dimensions'][0]}x{media['dimensions'][1]}")

                with col_det2:
                    st.caption(f"上传: {media['uploader']}")
                    st.caption(f"日期: {media['uploaded_at'].strftime('%Y-%m-%d')}")

                if st.button(f'❌ 删除', key=f'delete_{media["id"]}', use_container_width=True):
                    st.warning(f"准备删除: {media['filename']}")
else:
    st.info("📁 没有找到符合条件的媒体文件")


# ============================================================================
# 批量操作
# ============================================================================

if st.session_state.selected_media:
    st.divider()

    st.subheader(f"🔧 批量操作 ({len(st.session_state.selected_media)} 项)")

    col_batch1, col_batch2, col_batch3 = st.columns(3)

    with col_batch1:
        if st.button("📥 下载选中", use_container_width=True):
            st.info(f"下载 {len(st.session_state.selected_media)} 个文件")

    with col_batch2:
        new_category = st.selectbox("移动到分类", ["", "banner", "product", "team", "other"])
        if st.button("移动", use_container_width=True):
            st.success("文件已移动")

    with col_batch3:
        if st.button("🗑️ 删除选中", use_container_width=True):
            st.warning(f"删除 {len(st.session_state.selected_media)} 个文件")


# ============================================================================
# 存储空间统计
# ============================================================================

st.divider()

st.subheader("💾 存储空间")

total_space = 5 * 1024 * 1024 * 1024  # 5GB
used_space = sum(f["size"] for f in media_files)
free_space = total_space - used_space

col_storage1, col_storage2 = st.columns(2)

with col_storage1:
    st.metric("已使用", f"{used_space / 1024 / 1024:.2f} GB")

with col_storage2:
    st.metric("可用空间", f"{free_space / 1024 / 1024:.2f} GB")

st.progress(used_space / total_space)
st.caption(f"{used_space / total_space * 100:.1f}% 已使用")
'''


# ============================================================================
# 3. ContentList - 内容列表模板
# ============================================================================

class ContentList:
    """
    内容列表模板

    功能: 内容浏览、状态筛选、批量操作

    推荐主题: default_light, midnight_blue

    特性:
        - 列表/网格视图
        - 状态筛选
        - 批量编辑
        - 快速操作
        - 发布管理
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
内容列表 - Streamlit 实现
==========================

功能: 内容浏览、状态筛选、批量操作
"""

import streamlit as st
import pandas as pd
from datetime import datetime


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="内容列表",
    page_icon="📋",
    layout="wide"
)


# ============================================================================
# 模拟内容数据
# ============================================================================

@st.cache_data
def get_content_list():
    """获取内容列表"""
    return [
        {
            "id": "art_001",
            "title": "Python 入门教程完整版",
            "type": "article",
            "status": "published",
            "author": "张三",
            "category": "技术",
            "views": 15280,
            "created_at": datetime(2024, 1, 10, 9, 30),
            "updated_at": datetime(2024, 1, 15, 14, 20),
        },
        {
            "id": "art_002",
            "title": "2024年学习计划",
            "type": "page",
            "status": "draft",
            "author": "李四",
            "category": "生活",
            "views": 0,
            "created_at": datetime(2024, 1, 12, 10, 15),
            "updated_at": datetime(2024, 1, 12, 10, 15),
        },
        {
            "id": "art_003",
            "title": "新产品发布通知",
            "type": "news",
            "status": "published",
            "author": "管理员",
            "category": "公告",
            "views": 8960,
            "created_at": datetime(2024, 1, 14, 16, 0),
            "updated_at": datetime(2024, 1, 14, 16, 0),
        },
        {
            "id": "art_004",
            "title": "如何高效学习编程？",
            "type": "article",
            "status": "published",
            "author": "王五",
            "category": "技术",
            "views": 12560,
            "created_at": datetime(2024, 1, 8, 8, 0),
            "updated_at": datetime(2024, 1, 8, 8, 0),
        },
    ]


# ============================================================================
# 状态管理
# ============================================================================

if "content_view" not in st.session_state:
    st.session_state.content_view = "list"  # list, grid

if "content_filter_status" not in st.session_state:
    st.session_state.content_filter_status = "all"

if "content_selected" not in st.session_state:
    st.session_state.content_selected = []


# ============================================================================
# 主界面
# ============================================================================

st.title("📋 内容列表")

# ============================================================================
# 操作栏
# ============================================================================

col_op1, col_op2, col_op3, col_op4, col_op5 = st.columns(5)

with col_op1:
    view = st.radio(
        "视图",
        ["📋 列表", "⊞ 网格"],
        horizontal=True,
        index=["list", "grid"].index(st.session_state.content_view)
    )
    st.session_state.content_view = {"📋 列表": "list", "⊞ 网格": "grid"}[view]

with col_op2:
    status_filter = st.selectbox(
        "状态筛选",
        ["全部", "已发布", "草稿", "待审核", "已归档"],
        index=0
    )

with col_op3:
    type_filter = st.selectbox(
        "类型",
        ["全部", "文章", "页面", "新闻", "产品"]
    )

with col_op4:
    sort_by = st.selectbox(
        "排序",
        ["最新", "最热", "标题"]
    )

with col_op5:
    if st.button("➕ 新建内容", use_container_width=True, type="primary"):
        st.info("跳转到编辑器")

st.divider()


# ============================================================================
# 统计卡片
# ============================================================================

all_content = get_content_list()

stat_cols = st.columns(5)

with stat_cols[0]:
    st.metric("全部", f"{len(all_content)}")

with stat_cols[1]:
    published_count = sum(1 for c in all_content if c["status"] == "published")
    st.metric("已发布", published_count)

with stat_cols[2]:
    draft_count = sum(1 for c in all_content if c["status"] == "draft")
    st.metric("草稿", draft_count)

with stat_cols[3]:
    total_views = sum(c["views"] for c in all_content)
    st.metric("总浏览", f"{total_views:,}")

with stat_cols[4]:
    st.metric("今日新增", "2")

st.divider()


# ============================================================================
# 内容列表
# ============================================================================

st.subheader("📄 内容列表")

# 应用筛选
filtered_content = all_content.copy()

if status_filter != "全部":
    status_map = {"已发布": "published", "草稿": "draft", "待审核": "pending", "已归档": "archived"}
    filtered_content = [c for c in filtered_content if c["status"] == status_map.get(status_filter)]

if type_filter != "全部":
    filtered_content = [c for c in filtered_content if c["type"] == type_filter]

# 显示内容
if not filtered_content:
    st.info("🔍 没有找到符合条件的内容")
else:
    if st.session_state.content_view == "list":
        # 列表视图
        for content in filtered_content:
            with st.container():
                # 状态图标
                status_icons = {
                    "published": "🟢",
                    "draft": "🟡",
                    "pending": "🟠",
                    "archived": "⚪"
                }
                status_icon = status_icons.get(content["status"], "📄")

                # 选择框
                selected = content["id"] in st.session_state.content_selected

                col_list1, col_list2 = st.columns([1, 5])

                with col_list1:
                    if st.checkbox("", value=selected, key=f'check_{content["id"]}'):
                        if content["id"] not in st.session_state.content_selected:
                            st.session_state.content_selected.append(content["id"])
                        else:
                            st.session_state.content_selected.remove(content["id"])
                        st.rerun()

                with col_list2:
                    # 内容信息
                    col_content1, col_content2, col_content3, col_content4 = st.columns([3, 2, 2, 3])

                    with col_content1:
                        st.markdown(f"### {status_icon} {content['title']}")

                    with col_content2:
                        st.caption(f"👤 {content['author']}")
                        st.caption(f"📂 {content['category']}")

                    with col_content3:
                        st.caption(f"👁️ {content['views']:,}")
                        st.caption(f"📅 {content['created_at'].strftime('%Y-%m-%d')}")

                    with col_content4:
                        # 快速操作
                        if st.button(f'✏️ 编辑', key=f'edit_{content["id"]}', use_container_width=True):
                            st.info(f"编辑: {content['title']}")

                st.divider()

    else:
        # 网格视图
        grid_cols = st.columns(3)

        for i, content in enumerate(filtered_content):
            col = grid_cols[i % 3]

            with col:
                status_icons = {
                    "published": "🟢",
                    "draft": "🟡",
                    "pending": "🟠",
                    "archived": "⚪"
                }
                status_icon = status_icons.get(content["status"], "📄")

                st.markdown(f"""
                <div style='border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; height: 150px;'>
                    <h4>{status_icon} {content['title'][:30]}...</h4>
                    <p style='color: #666; font-size: 12px;'>{content['author']} · {content['category']}</p>
                    <p style='color: #999; font-size: 12px;'>{content['created_at'].strftime('%Y-%m-%d')}</p>
                    <p style='color: #999; font-size: 12px;'>👁️ {content['views']:,} 浏览</p>
                </div>
                """, unsafe_allow_html=True)


# ============================================================================
# 批量操作
# ============================================================================

if st.session_state.content_selected:
    st.divider()

    st.subheader(f"🔧 批量操作 ({len(st.session_state.content_selected)} 项)")

    col_batch1, col_batch2, col_batch3 = st.columns(3)

    with col_batch1:
        batch_status = st.selectbox("批量更改状态", ["", "草稿", "已发布", "已归档"])
        if st.button("应用", use_container_width=True):
            st.success(f"已更改 {len(st.session_state.content_selected)} 个内容的状态")

    with col_batch2:
        batch_category = st.selectbox("批量更改分类", ["", "技术", "生活", "公告"])
        if st.button("应用", use_container_width=True):
            st.success("分类已更新")

    with col_batch3:
        if st.button("🗑️ 删除", use_container_width=True):
            st.warning(f"准备删除 {len(st.session_state.content_selected)} 个内容")
            st.session_state.content_selected = []
            st.rerun()
'''


# ============================================================================
# 4. CategoryManager - 分类管理模板
# ============================================================================

class CategoryManager:
    """
    分类管理模板

    功能: 树形结构、拖拽排序、层级管理

    推荐主题: default_light, midnight_blue

    特性:
        - 树形显示
        - 添加/编辑/删除
        - 拖拽排序
        - 层级管理
        - 文章数量统计
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
分类管理 - Streamlit 实现
=========================

功能: 树形结构、拖拽排序、层级管理
"""

import streamlit as st
from datetime import datetime


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="分类管理",
    page_icon="🗂️",
    layout="wide"
)


# ============================================================================
# 模拟分类数据（树形结构）
# ============================================================================

@st.cache_data
def get_categories():
    """获取分类列表（树形结构）"""
    return [
        {
            "id": "cat_1",
            "name": "技术",
            "slug": "tech",
            "parent_id": None,
            "description": "技术相关文章",
            "icon": "💻",
            "color": "#007bff",
            "order": 1,
            "post_count": 45,
            "children": [
                {
                    "id": "cat_1_1",
                    "name": "编程",
                    "slug": "programming",
                    "parent_id": "cat_1",
                    "description": "编程语言和开发",
                    "icon": "👨‍💻",
                    "color": "#0056b3",
                    "order": 1,
                    "post_count": 28,
                    "children": []
                },
                {
                    "id": "cat_1_2",
                    "name": "数据库",
                    "slug": "database",
                    "parent_id": "cat_1",
                    "description": "数据库技术",
                    "icon": "🗄️",
                    "color": "#0056b3",
                    "order": 2,
                    "post_count": 17,
                    "children": [
                        {
                            "id": "cat_1_2_1",
                            "name": "MySQL",
                            "slug": "mysql",
                            "parent_id": "cat_1_2",
                            "description": "MySQL 数据库",
                            "icon": "🐬",
                            "color": "#004085",
                            "order": 1,
                            "post_count": 10,
                            "children": []
                        },
                        {
                            "id": "cat_1_2_2",
                            "name": "PostgreSQL",
                            "slug": "postgresql",
                            "parent_id": "cat_1_2",
                            "description": "PostgreSQL 数据库",
                            "icon": "🐘",
                            "color": "#004085",
                            "order": 2,
                            "post_count": 7,
                            "children": []
                        },
                    ]
                },
            ]
        },
        {
            "id": "cat_2",
            "name": "生活",
            "slug": "life",
            "parent_id": None,
            "description": "生活随笔",
            "icon": "🌟",
            "color": "#28a745",
            "order": 2,
            "post_count": 32,
            "children": [
                {
                    "id": "cat_2_1",
                    "name": "旅行",
                    "slug": "travel",
                    "parent_id": "cat_2",
                    "description": "旅行见闻",
                    "icon": "✈️",
                    "color": "#1e7e34",
                    "order": 1,
                    "post_count": 18,
                    "children": []
                },
                {
                    "id": "cat_2_2",
                    "name": "美食",
                    "slug": "food",
                    "parent_id": "cat_2",
                    "description": "美食分享",
                    "icon": "🍜",
                    "color": "#1e7e34",
                    "order": 2,
                    "post_count": 14,
                    "children": []
                },
            ]
        },
        {
            "id": "cat_3",
            "name": "公告",
            "slug": "announcement",
            "parent_id": None,
            "description": "网站公告",
            "icon": "📢",
            "color": "#ffc107",
            "order": 3,
            "post_count": 8,
            "children": []
        },
    ]


def render_category_tree(categories, level=0):
    """递归渲染分类树"""
    for cat in categories:
        indent = "　　" * level

        # 分类项
        col1, col2, col3, col4, col5 = st.columns([4, 2, 1, 1, 1])

        with col1:
            st.markdown(f"{indent}{cat['icon']} **{cat['name']}**")
            st.caption(cat['description'])

        with col2:
            st.metric("", f"{cat['post_count']} 篇", label_visibility="collapsed")

        with col3:
            if st.button("✏️", key=f'edit_{cat["id"]}', use_container_width=True):
                st.info(f"编辑分类: {cat['name']}")

        with col4:
            if cat["parent_id"] and st.button("⬆️", key=f'move_up_{cat["id"]}', use_container_width=True):
                st.success(f"上移: {cat['name']}")

            if cat["parent_id"] and st.button("⬇️", key=f'move_down_{cat["id"]}', use_container_width=True):
                st.success(f"下移: {cat['name']}")

        with col5:
            if st.button("🗑️", key=f'delete_{cat["id"]}', use_container_width=True):
                st.warning(f"删除分类: {cat['name']}")

        # 递归渲染子分类
        if cat.get("children"):
            render_category_tree(cat["children"], level + 1)


# ============================================================================
# 主界面
# ============================================================================

st.title("🗂️ 分类管理")

# ============================================================================
# 添加新分类
# ============================================================================

st.subheader("➕ 添加新分类")

with st.expander("展开表单", expanded=True):
    col_form1, col_form2 = st.columns(2)

    with col_form1:
        new_name = st.text_input("分类名称*", placeholder="例如: 技术")
        new_slug = st.text_input("URL 别名", placeholder="例如: tech")

    with col_form2:
        parent_cat = st.selectbox(
            "父分类",
            ["(无)"] + [c["name"] for c in get_categories() if c["parent_id"] is None]
        )
        icon = st.selectbox("图标", ["💻", "🌟", "🌈", "📢", "✈️", "🍜"], index=0)
        color = st.color_picker("主题颜色", "#007bff")

    description = st.text_area("描述", height=80, placeholder="分类描述...")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("➕ 添加分类", use_container_width=True, type="primary"):
            if new_name:
                st.success(f"✅ 分类 '{new_name}' 已添加")
            else:
                st.error("请填写分类名称")

    with col_btn2:
        if st.button("取消", use_container_width=True):
            st.rerun()

st.divider()


# ============================================================================
# 分类列表
# ============================================================================

st.subheader("📊 分类列表")

categories = get_categories()

# 切换显示方式
display_mode = st.radio(
    "显示方式",
    ["📋 树形视图", "📊 列表视图"],
    horizontal=True
)

if display_mode == "📋 树形视图":
    # 树形视图
    st.caption("💡 提示：可以展开/折叠子分类")

    for root_cat in categories:
        if root_cat["parent_id"] is None:
            with st.expander(f"📁 **{root_cat['name']}** ({root_cat['post_count']} 篇)", expanded=True):
                # 根分类信息
                col_root1, col_root2 = st.columns(3)

                with col_root1:
                    st.write(f"📝 {root_cat['description']}")

                with col_root2:
                    st.info(f"🆔 {root_cat['post_count']} 篇文章")

                # 子分类
                if root_cat.get("children"):
                    render_category_tree(root_cat["children"], level=1)

else:
    # 列表视图（扁平）
    def flatten_categories(cats):
        """扁平化分类列表"""
        result = []
        for cat in cats:
            result.append(cat)
            if cat.get("children"):
                result.extend(flatten_categories(cat["children"]))
        return result

    flat_categories = flatten_categories(categories)

    # 表格显示
    for cat in flat_categories:
        col_item1, col_item2, col_item3, col_item4, col_item5 = st.columns([3, 2, 2, 2, 1])

        with col_item1:
            level = "└─ " * (2 if cat["parent_id"] else 0)
            st.write(f"{level}{cat['icon']} {cat['name']}")

        with col_item2:
            st.write(cat['slug'])

        with col_item3:
            st.write(f"{cat['post_count']} 篇")

        with col_item4:
            if st.button(f'✏️', key=f'list_edit_{cat["id"]}', use_container_width=True):
                st.info(f"编辑: {cat['name']}")

        with col_item5:
            if st.button(f'🗑️', key=f'list_delete_{cat["id"]}', use_container_width=True):
                st.warning(f"删除: {cat['name']}")

        st.divider()


# ============================================================================
# 统计信息
# ============================================================================

st.divider()

st.subheader("📊 分类统计")

total_categories = len(flatten_categories(categories))

col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.metric("总分类数", total_categories)

with col_stat2:
    max_cat = max(categories, key=lambda x: x["post_count"])
    st.metric("最多文章", f"{max_cat['name']} ({max_cat['post_count']} 篇)")

with col_stat3:
    leaf_cats = sum(1 for c in flatten_categories(categories) if not c.get("children"))
    st.metric("叶子分类", leaf_cats)
'''


# ============================================================================
# 5. SEOPanel - SEO 设置模板
# ============================================================================

class SEOPanel:
    """
    SEO 设置面板模板

    功能: 标题设置、元数据配置、站点地图

    推荐主题: midnight_blue, default_light

    特性:
        - SEO 标题
        - 元描述
        - 关键词管理
        - Open Graph
        - 结构化数据
        - 站点地图
    """

    def render_streamlit(self) -> str:
        """生成 Streamlit 代码"""
        return '''"""
SEO 设置 - Streamlit 实现
========================

功能: 标题设置、元数据配置、站点地图
"""

import streamlit as st


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="SEO 设置",
    page_icon="🔍",
    layout="wide"
)


# ============================================================================
# 主界面
# ============================================================================

st.title("🔍 SEO 设置中心")


# ============================================================================
# 全局 SEO 设置
# ============================================================================

st.subheader("🌐 全局 SEO 设置")

tab1, tab2, tab3 = st.tabs(["站点信息", "结构化数据", "站点地图"])


# ============================================================================
# 站点信息
# ============================================================================

with tab1:
    # 站点标题
    st.markdown("### 📝 站点标题")

    site_title = st.text_input(
        "站点标题",
        value="我的网站",
        help="显示在浏览器标签栏的标题"
    )

    st.caption("💡 建议：包含站点名称，控制在 60 字符以内")

    st.divider()

    # 站点描述
    st.markdown("### 📄 站点描述")

    site_description = st.text_area(
        "站点描述",
        value="一个专注于技术分享的博客网站",
        height=100,
        help="显示在搜索结果中的描述，建议控制在 160 字符以内"
    )

    st.divider()

    # 站点关键词
    st.markdown("### 🏷️ 全局关键词")

    global_keywords = st.text_input(
        "关键词（逗号分隔）",
        value="Python, 编程, 教程, 博客, 技术",
        help="5-8 个核心关键词，用逗号分隔"
    )

    st.divider()

    # 网站图标
    st.markdown("### 🖼️ 网站图标")

    col_fav1, col_fav2 = st.columns(2)

    with col_fav1:
        favicon_upload = st.file_uploader(
            "上传 Favicon",
            type=["png", "ico"],
            help="推荐尺寸: 32x32 或 16x16"
        )

    with col_fav2:
        logo_upload = st.file_uploader(
            "上传 Logo",
            type=["png", "jpg", "svg"],
            help="推荐尺寸: 200x50"
        )

    st.divider()

    # 社交媒体
    st.markdown("### 📱 社交媒体链接")

    social_links = {
        "facebook": "",
        "twitter": "",
        "instagram": "",
        "linkedin": "",
        "github": ""
    }

    for platform, placeholder in social_links.items():
        url = st.text_input(f"{platform.capitalize()} URL", placeholder=f"https://{platform}.com/yourpage")
        social_links[platform] = url


# ============================================================================
# 结构化数据
# ============================================================================

with tab2:
    st.markdown("### 📊 结构化数据类型")

    # Schema.org 类型选择
    schema_types = {
        "Article": "文章",
        "Blog": "博客",
        "Organization": "组织",
        "Person": "人物",
        "WebSite": "网站"
    }

    selected_schema = st.selectbox(
        "选择 Schema 类型",
        list(schema_types.keys()),
        format_func=lambda x: schema_types[x]
    )

    st.divider()

    # 结构化数据配置
    st.markdown(f"### {schema_types[selected_schema]} 结构化数据")

    if selected_schema == "Article":
        st.markdown("""
        <style>
        .schema-example {
            background: #f5f5f5;
            padding: 15px;
            border-left: 4px solid #007bff;
            border-radius: 4px;
        }
        </style>
        <div class='schema-example'>
        <pre>
&lt;script type="application/ld+json"&gt;
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "文章标题",
  "author": {
    "@type": "Person",
    "name": "作者名称"
  },
  "datePublished": "2024-01-15",
  "description": "文章描述"
}
&lt;/script&gt;
        </pre>
        </div>
        """, unsafe_allow_html=True)

        st.caption("💡 复制代码到 &lt;head&gt; 部分")

    elif selected_schema == "Organization":
        st.markdown("""
        <style>
        .schema-example {
            background: #f5f5f5;
            padding: 15px;
            border-left: 4px solid #007bff;
            border-radius: 4px;
        }
        </style>
        <div class='schema-example'>
        <pre>
&lt;script type="application/ld+json"&gt;
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "网站名称",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://facebook.com/yourpage",
    "https://twitter.com/yourhandle"
  ]
}
&lt;/script&gt;
        </pre>
        </div>
        """, unsafe_allow_html=True)

        st.caption("💡 复制代码到 &lt;head&gt; 部分")


# ============================================================================
# 站点地图
# ============================================================================

with tab3:
    st.markdown("### 🗺️ 站点地图")

    sitemap_format = st.radio(
        "格式",
        ["XML", "TXT"],
        horizontal=True
    )

    if sitemap_format == "XML":
        st.markdown("""
        <style>
        .sitemap-example {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 4px;
        }
        </style>
        <div class='sitemap-example'>
        <pre>
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"&gt;
  &lt;url&gt;
    &lt;loc&gt;https://example.com/&lt;/loc&gt;
    &lt;lastmod&gt;2024-01-15&lt;/lastmod&gt;
    &lt;changefreq&gt;weekly&lt;/changefreq&gt;
    &lt;priority&gt;1.0&lt;/priority&gt;
  &lt;/url&gt;
  &lt;url&gt;
    &lt;loc&gt;https://example.com/article1&lt;/loc&gt;
    &lt;lastmod&gt;2024-01-14&lt;/lastmod&gt;
    &lt;changefreq&gt;weekly&lt;/changefreq&gt;
    &lt;priority&gt;0.8&lt;/priority&gt;
  &lt;/url&gt;
&lt;/urlset&gt;
        </pre>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
        .sitemap-example {
            background: #_s f5f5;
            padding: 15px;
            border-radius: 4px;
        }
        </style>
        <div class='sitemap-example'>
        <pre>
https://example.com/
https://example.com/article1
https://example.com/category/tech
        </pre>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# 生成按钮
# ============================================================================

st.divider()

st.subheader("🚀 生成配置")

col_gen1, col_gen2 = st.columns(2)

with col_gen1:
    if st.button("📋 生成 robots.txt", use_container_width=True):
        st.info("robots.txt 已生成")

with col_gen2:
    if st.button("🗺️ 生成 sitemap.xml", use_container_width=True):
        st.info("sitemap.xml 已生成")


# ============================================================================
# SEO 检查
# ============================================================================

st.divider()

st.subheader("🔍 SEO 检查")

st.markdown("### 快速检查项")

check_items = [
    {"name": "站点标题已设置", "status": True},
    {"name": "站点描述已设置", "status": True},
    {"name": "关键词已配置", "status": False},
    {"name": "Favicon 已上传", "status": False},
    {"name": "结构化数据已添加", "status": True},
    {"name": "站点地图已生成", "status": True},
]

for item in check_items:
    status_icon = "✅" if item["status"] else "⭕"
    st.markdown(f"{status_icon} {item['name']}")

# SEO 得分
passed_count = sum(1 for item in check_items if item["status"])
total_count = len(check_items)
seo_score = (passed_count / total_count) * 100

st.metric("SEO 得分", f"{seo_score:.0f}%", delta=f"{passed_count}/{total_count} 项通过")

if seo_score == 100:
    st.success("🎉 完美！所有 SEO 检查项都已通过")
elif seo_score >= 80:
    st.info("👍 SEO 设置良好，还有提升空间")
elif seo_score >= 60:
    st.warning("⚠️ SEO 设置一般，建议完善")
else:
    st.error("❌ SEO 设置较差，请尽快完善")
'''


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 枚举
    "ContentStatus",
    "ContentType",
    "MediaType",
    "EditorMode",
    # 数据类
    "Article",
    "MediaFile",
    "Category",
    "SEOSettings",
    # 模板类
    "ArticleEditor",
    "MediaLibrary",
    "ContentList",
    "CategoryManager",
    "SEOPanel",
]
