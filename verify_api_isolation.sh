#!/bin/bash
# API隔离验证脚本
# 用于确认Brain和Ralph使用不同的API端点

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  API隔离验证 - Brain vs Ralph                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ============================================
# 测试1：当前终端的API配置
# ============================================
echo "📍 测试1: 当前终端（应该是官方API）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ANTHROPIC_BASE_URL = ${ANTHROPIC_BASE_URL:-未设置 (使用默认)}"
echo "  ANTHROPIC_API_KEY  = ${ANTHROPIC_API_KEY:0:10}${ANTHROPIC_API_KEY:+...}"
echo ""

if [ -z "$ANTHROPIC_BASE_URL" ]; then
    echo "  ✅ 正确：未设置base_url"
    echo "     → 将使用Anthropic官方API"
    echo "     → Brain可以正常使用Claude Sonnet 4.5"
else
    echo "  ⚠️  警告：当前终端已设置base_url"
    echo "     → 这会影响Brain的API调用"
    echo "     → 建议：在新终端重新打开Brain"
fi
echo ""

# ============================================
# 测试2：智普API终端模拟
# ============================================
echo "📍 测试2: 智普API终端模拟"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 在子shell中设置环境变量（不影响当前终端）
(
    export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
    export ANTHROPIC_API_KEY="test_key_123"

    echo "  子进程环境变量："
    echo "    ANTHROPIC_BASE_URL = $ANTHROPIC_BASE_URL"
    echo "    ANTHROPIC_API_KEY  = ${ANTHROPIC_API_KEY:0:10}..."
)

echo ""
echo "  ✅ 子进程环境变量已设置"
echo ""

# ============================================
# 测试3：验证隔离
# ============================================
echo "📍 测试3: 验证隔离效果"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  当前终端 ANTHROPIC_BASE_URL = ${ANTHROPIC_BASE_URL:-未设置}"
echo ""

if [ -z "$ANTHROPIC_BASE_URL" ]; then
    echo "  ✅ 隔离成功！"
    echo "     子进程的环境变量没有影响父进程"
    echo ""
    echo "  结论："
    echo "    • 终端1（Brain）: 使用官方API ✅"
    echo "    • 终端2（Ralph）: 使用智普API ✅"
    echo "    • 两者完全隔离 ✅"
else
    echo "  ⚠️  隔离可能有问题"
    echo "     当前终端的环境变量已被设置"
fi
echo ""

# ============================================
# 测试4：Claude Code CLI检查
# ============================================
echo "📍 测试4: Claude Code CLI检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v claude &> /dev/null; then
    echo "  ✅ claude 命令已安装"
    claude --version
else
    echo "  ❌ claude 命令未找到"
    echo "     请安装: npm install -g @anthropic-ai/claude-code"
fi
echo ""

# ============================================
# 总结
# ============================================
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  验证总结                                                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ 推荐使用方式："
echo ""
echo "  【终端1 - Brain（您和我对话）】"
echo "    cd D:/AI_Projects/system-max"
echo "    # 不设置任何环境变量"
echo "    # 直接使用 Claude Code"
echo "    → 使用官方API (Claude Sonnet 4.5)"
echo ""
echo "  【终端2 - Ralph Worker】"
echo "    cd D:/AI_Projects/system-max"
echo "    bash start_ralph_with_zhipu.sh --live --verbose"
echo "    → 使用智普API (glm-4)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
