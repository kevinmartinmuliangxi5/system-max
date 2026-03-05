#!/bin/bash
# Ralph实时监控面板
# 用于Windows Terminal第3面板

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Ralph Real-time Monitor - 实时监控                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 清屏函数
clear_screen() {
    printf "\033c"
}

# 主循环
while true; do
    clear_screen

    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  Ralph Monitor - $(date '+%H:%M:%S')                       "
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    # ============================================
    # 1. 状态信息
    # ============================================
    if [ -f ".ralph/status.json" ]; then
        echo "📊 状态信息"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        status=$(cat .ralph/status.json | grep -o '"status": *"[^"]*"' | cut -d'"' -f4)
        loop_count=$(cat .ralph/status.json | grep -o '"loop_count": *[0-9]*' | grep -o '[0-9]*')
        calls_made=$(cat .ralph/status.json | grep -o '"calls_made_this_hour": *[0-9]*' | grep -o '[0-9]*')
        max_calls=$(cat .ralph/status.json | grep -o '"max_calls_per_hour": *[0-9]*' | grep -o '[0-9]*')

        echo "  状态: $status"
        echo "  循环次数: $loop_count"
        echo "  API调用: $calls_made / $max_calls"
        echo ""
    fi

    # ============================================
    # 2. 当前任务
    # ============================================
    if [ -f ".janus/project_state.json" ]; then
        echo "📋 当前任务"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        # 提取第一个PENDING任务
        task_name=$(cat .janus/project_state.json | grep -A3 '"status": *"PENDING"' | grep '"task_name"' | head -1 | cut -d'"' -f4)

        if [ -n "$task_name" ]; then
            echo "  → $task_name"
        else
            echo "  → 所有任务已完成或无任务"
        fi
        echo ""
    fi

    # ============================================
    # 3. 最近日志（最后10行）
    # ============================================
    if [ -f ".ralph/live.log" ]; then
        echo "📜 最近日志 (最后10行)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        tail -10 .ralph/live.log | sed 's/^/  /'
        echo ""
    fi

    # ============================================
    # 4. 文件变更
    # ============================================
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo "📁 文件变更"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        git status -s 2>/dev/null | head -10 | sed 's/^/  /' || echo "  无变更"
        echo ""
    fi

    # ============================================
    # 5. 成本估算（如果有）
    # ============================================
    if [ -f ".ralph/cost_tracking.json" ]; then
        echo "💰 成本跟踪"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        total_cost=$(cat .ralph/cost_tracking.json | grep -o '"total_cost_usd": *[0-9.]*' | grep -o '[0-9.]*')
        echo "  累计成本: \$$total_cost (约 ¥$(echo "$total_cost * 7" | bc))"
        echo ""
    fi

    # ============================================
    # 6. 熔断器状态
    # ============================================
    if [ -f ".ralph/.circuit_breaker_state" ]; then
        echo "🔌 熔断器状态"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        cat .ralph/.circuit_breaker_state | sed 's/^/  /'
        echo ""
    fi

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏱️  刷新中... (Ctrl+C 退出)"

    # 每2秒刷新
    sleep 2
done
