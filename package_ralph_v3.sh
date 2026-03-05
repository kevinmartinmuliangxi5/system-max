#!/bin/bash
# ========================================
# 双脑Ralph系统 v3.0 打包脚本
# Dual-Brain Ralph System v3.0 Package Script
# ========================================
#
# 此脚本将系统打包为可分发的部署包
# This script packages the system for distribution
#
# 使用方法 / Usage:
#   bash package_ralph_v3.sh
#
# ========================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SOURCE_DIR="."
PACKAGE_NAME="ralph-v3.0"
TARGET_DIR="super system"
VERSION="v3.0.0-alpha"
DATE=$(date +%Y-%m-%d)

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}双脑Ralph系统 v3.0 打包工具${NC}"
echo -e "${BLUE}Dual-Brain Ralph System v3.0 Packager${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# ========================================
# 1. 清理旧文件
# ========================================
echo -e "${YELLOW}[1/7] 清理旧文件...${NC}"
rm -rf "${TARGET_DIR}"
rm -f "${PACKAGE_NAME}.tar.gz" "${PACKAGE_NAME}.zip"
echo -e "${GREEN}✓ 清理完成${NC}"
echo ""

# ========================================
# 2. 创建目录结构
# ========================================
echo -e "${YELLOW}[2/7] 创建目录结构...${NC}"
mkdir -p "${TARGET_DIR}"
mkdir -p "${TARGET_DIR}/.janus/core"
mkdir -p "${TARGET_DIR}/.janus/knowledge"
mkdir -p "${TARGET_DIR}/.janus/ui_library"
mkdir -p "${TARGET_DIR}/.ralph/tools"
mkdir -p "${TARGET_DIR}/.ralph/context/modules"
mkdir -p "${TARGET_DIR}/.ralph/diagrams"
mkdir -p "${TARGET_DIR}/.ralph/specs"
mkdir -p "${TARGET_DIR}/.ralph/memories"
mkdir -p "${TARGET_DIR}/.ralph/logs"
mkdir -p "${TARGET_DIR}/.ralph/docs/generated"
mkdir -p "${TARGET_DIR}/.ralph/scripts"
echo -e "${GREEN}✓ 目录结构创建完成${NC}"
echo ""

# ========================================
# 3. 复制核心Python模块
# ========================================
echo -e "${YELLOW}[3/7] 复制核心Python模块...${NC}"

# 核心模块
cp brain_v3.py "${TARGET_DIR}/"
cp brain.py "${TARGET_DIR}/"
cp dealer_v3.py "${TARGET_DIR}/"
cp dealer_enhanced.py "${TARGET_DIR}/"
cp setup.py "${TARGET_DIR}/"
cp quickstart.py "${TARGET_DIR}/"
cp quick_test.sh "${TARGET_DIR}/"

echo -e "${GREEN}✓ 核心模块复制完成${NC}"
echo ""

# ========================================
# 4. 复制.janus目录
# ========================================
echo -e "${YELLOW}[4/7] 复制.janus核心记忆系统...${NC}"

# 核心模块
cp -r .janus/core/* "${TARGET_DIR}/.janus/core/"
cp .janus/config.json "${TARGET_DIR}/.janus/"
cp .janus/ui_templates.py "${TARGET_DIR}/.janus/"
cp .janus/*.json "${TARGET_DIR}/.janus/" 2>/dev/null || true

# UI库
cp -r .janus/ui_library "${TARGET_DIR}/.janus/"

echo -e "${GREEN}✓ .janus目录复制完成${NC}"
echo ""

# ========================================
# 5. 复制.ralph目录
# ========================================
echo -e "${YELLOW}[5/7] 复制.ralph工具集成层...${NC}"

# 工具
cp -r .ralph/tools/* "${TARGET_DIR}/.ralph/tools/"

# Context Engineering
cp -r .ralph/context/* "${TARGET_DIR}/.ralph/context/"

# 配置文件
cp .ralph/*.md "${TARGET_DIR}/.ralph/" 2>/dev/null || true

# 文档
cp .ralph/docs/tools-integration-analysis.md "${TARGET_DIR}/.ralph/docs/" 2>/dev/null || true

echo -e "${GREEN}✓ .ralph目录复制完成${NC}"
echo ""

# ========================================
# 6. 复制文档
# ========================================
echo -e "${YELLOW}[6/7] 复制文档文件...${NC}"

# 文档文件
cp README.md "${TARGET_DIR}/" 2>/dev/null || echo "  [!] README.md not found"
cp README_V3.md "${TARGET_DIR}/"
cp QUICK_START_V3.md "${TARGET_DIR}/"
cp DEPLOYMENT.md "${TARGET_DIR}/"
cp INTEGRATION_COMPLETE_SUMMARY.md "${TARGET_DIR}/"

# 创建requirements.txt
cat > "${TARGET_DIR}/requirements.txt" << 'EOF'
# 双脑Ralph系统 v3.0 完整版依赖
# Dual-Brain Ralph System v3.0 Complete Dependencies
# 最后更新: 2026-02-11

# ====================
# 核心依赖 / Core Dependencies
# ====================

# 中文分词 / Chinese Word Segmentation
jieba>=0.42.1

# Claude API / Anthropic SDK
anthropic>=0.18.0

# 剪贴板操作 / Clipboard Operations (可选)
pyperclip>=1.8.2

# 颜色输出 / Terminal Colors
colorama>=0.4.6

# HTTP请求 / HTTP Requests
requests>=2.31.0

# ====================
# 可选依赖 / Optional Dependencies
# ====================

# 智谱AI API (可选) / Zhipu AI API (Optional)
# zhipuai>=4.0.0

# 向量数据库 (可选，用于claude-mem增强) / Vector DB (Optional)
# chromadb>=0.4.22
# faiss-cpu>=1.7.4

# 数据处理 (可选) / Data Processing (Optional)
# numpy>=1.24.0
# pandas>=2.0.0
EOF

# 创建示例配置模板
cat > "${TARGET_DIR}/.janus/config.template.json" << 'EOF'
{
  "ZHIPU_API_KEY": "your_api_key_here",
  "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7",
  "_comment": "请将your_api_key_here替换为您的实际API密钥"
}
EOF

echo -e "${GREEN}✓ 文档文件复制完成${NC}"
echo ""

# ========================================
# 7. 清理缓存文件
# ========================================
echo -e "${YELLOW}[7/7] 清理缓存文件...${NC}"
find "${TARGET_DIR}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "${TARGET_DIR}" -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✓ 缓存清理完成${NC}"
echo ""

# ========================================
# 创建打包清单
# ========================================
echo -e "${YELLOW}创建打包清单...${NC}"
cat > "${TARGET_DIR}/PACKAGE_MANIFEST.md" << EOF
# 双脑Ralph系统 v3.0 完整版 - 打包清单

**Dual-Brain Ralph System v3.0 Complete - Package Manifest**

版本: ${VERSION}
打包日期: ${DATE}

---

## 📦 包内容说明

本部署包包含双脑Ralph系统v3.0完整版的所有核心文件。

## 🚀 快速开始

1. 解压部署包
2. 运行: \`pip install -r requirements.txt\`
3. 验证: \`python .ralph/tools/tools_manager.py\`

## 📚 文档

- README.md - 系统使用说明
- DEPLOYMENT.md - 部署指南
- QUICK_START_V3.md - 快速上手指南

## 📋 文件统计

EOF

# 统计文件
PY_COUNT=$(find "${TARGET_DIR}" -name "*.py" -type f | wc -l)
MD_COUNT=$(find "${TARGET_DIR}" -name "*.md" -type f | wc -l)
JSON_COUNT=$(find "${TARGET_DIR}" -name "*.json" -type f | wc -l)

echo "- Python文件: ${PY_COUNT}" >> "${TARGET_DIR}/PACKAGE_MANIFEST.md"
echo "- 文档文件: ${MD_COUNT}" >> "${TARGET_DIR}/PACKAGE_MANIFEST.md"
echo "- 配置文件: ${JSON_COUNT}" >> "${TARGET_DIR}/PACKAGE_MANIFEST.md"

echo -e "${GREEN}✓ 打包清单创建完成${NC}"
echo ""

# ========================================
# 打包完成统计
# ========================================
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}打包完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}📦 部署包位置:${NC}"
echo -e "   ${TARGET_DIR}/"
echo ""
echo -e "${YELLOW}📊 文件统计:${NC}"
echo -e "   Python文件: ${PY_COUNT}"
echo -e "   文档文件: ${MD_COUNT}"
echo -e "   配置文件: ${JSON_COUNT}"
echo ""
echo -e "${YELLOW}🚀 后续步骤:${NC}"
echo -e "   1. cd \"${TARGET_DIR}\""
echo -e "   2. pip install -r requirements.txt"
echo -e "   3. python brain_v3.py \"测试任务\""
echo ""
echo -e "${GREEN}✅ 打包成功！${NC}"
echo ""
