# Ralph 系统启动指南

## 📋 当前状态检查

Ralph 命令未找到。以下是几种安装和启动方式：

---

## 🔧 方法 1：安装 Ralph CLI

```bash
# 1. 安装 Ralph（全局安装）
pip install ralph-cli

# 2. 验证安装
ralph --version

# 3. 在项目目录启动
cd D:\AI_Projects\system-max\1.mianshiAI
ralph --verbose
```

---

## 🔧 方法 2：使用 Claude Code 插件

```bash
# 在 Claude Code 中执行：

# 1. 安装官方 Ralph 插件
/plugin install ralph-loop@claude-plugins-official

# 2. 启动循环
/ralph-loop "修复HTML渲染、侧边栏颜色和标题颜色问题" --verbose
```

---

## 🔧 方法 3：手动 Ralph 模拟（临时方案）

由于 Ralph 系统未完全配置，我现在以 **Ralph 模式** 为您手动修复这三个问题：

## 📝 Ralph 模式修复方案

### 🔴 P0 - 紧急修复（必须完成）

#### 问题 1：HTML 渲染修复

**文件**：`app.py` 第 72-102 行

**当前问题**：`render_html()` 函数可能无法正确处理组件HTML

**修复方案**：
```python
def render_html(html: str, height: int = None):
    """渲染HTML组件 - Ralph修复版"""
    import re
    import streamlit.components.v1 as components

    # 清理HTML
    clean_html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    clean_html = clean_html.strip().lstrip()

    if not clean_html:
        return

    # 强制以<开头
    if not clean_html.startswith('<'):
        clean_html = f"<div>{clean_html}</div>"

    # 使用 iframe 渲染（最可靠）
    height = max(200, min(800, len(clean_html) // 3))
    components.html(clean_html, height=height, scrolling=False)
```

#### 问题 2：侧边栏米黄色背景

**文件**：`app.py` 第 201-205 行

**修复方案**：
```python
/* 侧边栏 - 米黄色背景 */
[data-testid="stSidebar"] {
    background: #FFF8E7 !important;
    border-right: 1px solid #E5E7EB !important;
}

/* 确保所有侧边栏子元素都透明 */
[data-testid="stSidebar"] * {
    background-color: transparent !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    background: transparent !important;
}
```

#### 问题 3：标题深蓝色背景

**文件**：`app.py` 在 `apply_moyu_theme()` 函数的CSS中添加

**修复方案**：
```css
/* 所有标题（h3-h6）深蓝色背景 - 全面覆盖 */
h3, h4, h5, h6,
.stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
.main h3, .main h4, .main h5, .main h6,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6,
[class*="ink-title"] h3,
[class*="ink-title"] h4,
[class*="ink-title"] h5,
[class*="ink-title"] h6 {
    background: #1E3A8A !important;
    color: #FFFFFF !important;
    padding: 0.5rem 1rem !important;
    border-radius: 6px !important;
    display: inline-block !important;
}
```

---

## 🎯 执行步骤

### 步骤 1：备份代码
```bash
cd D:\AI_Projects\system-max\1.mianshiAI
git add .
git commit -m "Backup before Ralph fixes" || echo "No git repo, skipping backup"
```

### 步骤 2：修改 app.py

#### 2.1 修复 render_html 函数
定位 `def render_html(html: str, height: int = None):` （约第72行）

替换函数体为上面提供的修复方案

#### 2.2 修复侧边栏颜色
在 `apply_moyu_theme()` 函数中找到侧边栏CSS

#### 2.3 添加标题深蓝色CSS
在 `apply_moyu_theme()` 函数的CSS中添加上面的标题样式

### 步骤 3：清除缓存
```bash
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
streamlit cache clear
```

### 步骤 4：重启应用
```bash
streamlit run app.py
```

---

## ✅ 验证清单

- [ ] HTML正确渲染，不显示原始代码
- [ ] 侧边栏背景为米黄色
- [ ] 所有h3-h6标题有深蓝色背景
- [ ] 主文字为黑色
- [ ] 字号已放大

---

## 🚀 自动化脚本

如果您希望我自动执行这些修复，请说：

**"Ralph模式：执行修复"** - 我将按照Ralph模式自动修复所有问题

或者您也可以手动修改，然后我帮您验证。

---

**您希望我现在以Ralph模式执行修复，还是您想先安装Ralph CLI？**