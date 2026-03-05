#!/bin/bash
# Ralph专用启动脚本 - 使用智普API
# 不影响其他终端的Brain（Claude Pro API）

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Ralph Autonomous Loop - 智普API模式                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ============================================
# 1. 设置智普API配置（仅当前进程）
# ============================================
echo "📡 配置智普API..."

# 从配置文件读取智普API Key
if [ -f ".janus/config.json" ]; then
    ZHIPU_KEY=$(cat .janus/config.json | grep -o '"ZHIPU_API_KEY": *"[^"]*"' | cut -d'"' -f4)
    if [ -n "$ZHIPU_KEY" ]; then
        export ANTHROPIC_API_KEY="$ZHIPU_KEY"
        echo "  ✅ API Key loaded from .janus/config.json"
    else
        echo "  ⚠️  未找到 ZHIPU_API_KEY，请手动设置"
        read -p "  请输入智普API Key: " ZHIPU_KEY
        export ANTHROPIC_API_KEY="$ZHIPU_KEY"
    fi
else
    echo "  ⚠️  配置文件不存在"
    read -p "  请输入智普API Key: " ZHIPU_KEY
    export ANTHROPIC_API_KEY="$ZHIPU_KEY"
fi

# 设置智普API端点（关键！）
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"

# 可选：指定模型
export ANTHROPIC_MODEL="glm-4-plus"  # 或 glm-4

echo "  ✅ API Endpoint: $ANTHROPIC_BASE_URL"
echo "  ✅ Model: $ANTHROPIC_MODEL"
echo ""

# ============================================
# 2. 验证配置
# ============================================
echo "🧪 验证API配置..."
echo "  当前进程的环境变量："
echo "    ANTHROPIC_BASE_URL = $ANTHROPIC_BASE_URL"
echo "    ANTHROPIC_API_KEY  = ${ANTHROPIC_API_KEY:0:10}..."
echo ""

# ============================================
# 3. 检查蓝图文件
# ============================================
if [ -f ".janus/project_state.json" ]; then
    TASK_COUNT=$(cat .janus/project_state.json | grep -c "task_name")
    echo "📋 蓝图文件: .janus/project_state.json"
    echo "  任务数量: $TASK_COUNT"
else
    echo "❌ 错误: 蓝图文件不存在"
    echo "  请先在Brain终端生成任务蓝图"
    exit 1
fi
echo ""

# ============================================
# 4. 确认启动
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  重要提示："
echo "  1. 此终端将使用【智普API】运行Worker"
echo "  2. Brain终端仍使用【Claude Pro API】"
echo "  3. 两者完全隔离，互不影响"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "确认启动Ralph? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "取消启动"
    exit 0
fi

echo ""
echo "🚀 启动Ralph循环..."
echo ""

# ============================================
# 5. 启动Ralph（继承环境变量）
# ============================================
# 传递所有参数到 ralph_loop.sh
exec bash ~/.ralph/ralph_loop.sh "$@"
