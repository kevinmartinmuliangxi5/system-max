#!/bin/bash
# FlowSystem 自动安装脚本（适用于GLM Coding Plan配置）

set -e  # 遇到错误立即退出

echo "============================================"
echo "  FlowSystem 安装脚本"
echo "  配置 GLM Coding Plan"
echo "============================================"
echo ""

# 检查Python版本
echo "[1/5] 检查Python版本..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python版本: $PYTHON_VERSION"
echo ""

# 安装依赖
echo "[2/5] 安装依赖包..."
pip3 install -r requirements.txt
echo "✓ 依赖安装完成"
echo ""

# 创建配置文件
echo "[3/5] 配置API密钥..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ 已创建 .env 配置文件"
    echo ""
    echo "⚠️  请编辑 .env 文件，填入你的API密钥："
    echo ""
    echo "   ZHIPUAI_API_KEY=你的API密钥"
    echo ""
    read -p "按回车键继续..."
else
    echo "✓ .env 文件已存在"
fi
echo ""

# 运行导入测试
echo "[4/5] 运行导入测试..."
python3 test_imports.py
echo ""

# 运行功能测试
echo "[5/5] 运行功能测试..."
python3 test_simple.py
echo ""

# 完成
echo "============================================"
echo "✅ 安装完成!"
echo "============================================"
echo ""
echo "下一步:"
echo "  1. 确保已订阅 GLM Coding Plan 套餐"
echo "  2. 编辑 .env 文件，填入你的API密钥"
echo "  3. 运行: python3 run.py"
echo ""
echo "详细配置指南: GLM_CODING_PLAN_SETUP.md"
echo ""
