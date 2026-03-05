#!/bin/bash
# 快速验证脚本 - 测试所有配置是否正确

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Ralph + 双脑系统 - 快速验证                               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

test_count=0
pass_count=0

# 测试函数
run_test() {
    local test_name="$1"
    local test_command="$2"

    test_count=$((test_count + 1))
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "测试 $test_count: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if eval "$test_command"; then
        echo "  ✅ 通过"
        pass_count=$((pass_count + 1))
    else
        echo "  ❌ 失败"
    fi
    echo ""
}

# ============================================
# 测试1: 文件结构
# ============================================
run_test "双脑系统文件结构" '
    [ -f ".janus/core/hippocampus.py" ] && \
    [ -f "dealer_enhanced.py" ] && \
    [ -f "brain.py" ]
'

# ============================================
# 测试2: Ralph文件
# ============================================
run_test "Ralph文件存在" '
    [ -f ".ralphrc" ] && \
    [ -f "$HOME/.ralph/ralph_loop.sh" ]
'

# ============================================
# 测试3: 新增脚本
# ============================================
run_test "新增脚本文件" '
    [ -f "start_ralph_with_zhipu.sh" ] && \
    [ -f "ralph_interactive.sh" ] && \
    [ -f "monitor_ralph.sh" ]
'

# ============================================
# 测试4: Python依赖
# ============================================
run_test "Python和依赖" '
    py --version > /dev/null 2>&1 && \
    import jieba "import jieba" > /dev/null 2>&1
'

# ============================================
# 测试5: Claude Code CLI
# ============================================
run_test "Claude Code CLI" '
    command -v claude > /dev/null 2>&1
'

# ============================================
# 测试6: Git
# ============================================
run_test "Git可用性" '
    git --version > /dev/null 2>&1
'

# ============================================
# 测试7: 智普API配置
# ============================================
run_test "智普API配置" '
    [ -f ".janus/config.json" ] && \
    grep -q "ZHIPU_API_KEY" .janus/config.json
'

# ============================================
# 测试8: API隔离验证
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 8: API隔离验证"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 当前终端应该没有设置ANTHROPIC_BASE_URL
if [ -z "$ANTHROPIC_BASE_URL" ]; then
    echo "  ✅ 当前终端未设置智普端点（正确）"
    echo "     → Brain将使用Claude Pro API"
    pass_count=$((pass_count + 1))
else
    echo "  ⚠️  当前终端已设置智普端点"
    echo "     → 这会影响Brain的API调用"
    echo "     → 建议：重新打开终端"
fi
test_count=$((test_count + 1))
echo ""

# ============================================
# 测试9: 脚本权限
# ============================================
run_test "脚本可执行权限" '
    chmod +x start_ralph_with_zhipu.sh && \
    chmod +x ralph_interactive.sh && \
    chmod +x monitor_ralph.sh && \
    chmod +x verify_api_isolation.sh && \
    chmod +x quick_test.sh
'

# ============================================
# 测试10: 蓝图文件（可选）
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 10: 任务蓝图文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_count=$((test_count + 1))

if [ -f ".janus/project_state.json" ]; then
    task_count=$(cat .janus/project_state.json | grep -c "task_name" || echo "0")
    echo "  ✅ 蓝图文件存在"
    echo "     任务数量: $task_count"
    pass_count=$((pass_count + 1))
else
    echo "  ⚠️  蓝图文件不存在（需要Brain生成）"
    echo "     这不是错误，使用前需要先和Brain对话生成蓝图"
fi
echo ""

# ============================================
# 总结
# ============================================
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  验证结果                                                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "  通过: $pass_count / $test_count"
echo ""

if [ $pass_count -eq $test_count ]; then
    echo "  🎉 所有测试通过！系统已就绪"
    echo ""
    echo "  下一步："
    echo "    1. 在当前终端和Brain对话生成任务蓝图"
    echo "    2. 新开终端运行: bash ralph_interactive.sh"
    echo ""
elif [ $pass_count -ge $((test_count - 2)) ]; then
    echo "  ⚠️  大部分测试通过，可以开始使用"
    echo ""
    echo "  建议修复失败的测试项"
    echo ""
else
    echo "  ❌ 多个测试失败，请检查配置"
    echo ""
    echo "  常见问题："
    echo "    • Claude Code未安装: npm install -g @anthropic-ai/claude-code"
    echo "    • jieba未安装: pip install jieba"
    echo "    • 智普API Key未配置: 编辑 .janus/config.json"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
