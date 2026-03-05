#!/bin/bash
# 测试流式输出是否工作

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试1: 使用 Claude Pro API（应该有流式输出）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "请用一句话介绍 Python 编程语言" | claude --dangerously-skip-permissions
echo ""
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试2: 使用智普 API（可能没有流式输出）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 加载智普 API 配置
if [ -f ".janus/config.json" ]; then
    ZHIPU_KEY=$(cat .janus/config.json | grep '"ZHIPU_API_KEY"' | cut -d'"' -f4)
    export ANTHROPIC_API_KEY="$ZHIPU_KEY"
    export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
    export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"

    echo "请用一句话介绍 Python 编程语言" | claude --dangerously-skip-permissions
else
    echo "⚠️ 配置文件不存在"
fi

echo ""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "观察结果："
echo "  如果测试1有逐字输出，测试2没有 → 智普API不支持流式"
echo "  如果两者都没有逐字输出 → 终端或Claude Code配置问题"
echo "  如果两者都有逐字输出 → 说明Ralph脚本需要优化"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
