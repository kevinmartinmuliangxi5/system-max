#!/bin/bash
# 双脑+Ralph系统统一启动入口

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          双脑+Ralph自动开发系统                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 检测当前状态
if [ -f ".janus/project_state.json" ]; then
    # 有蓝图 → 提供选项
    echo "📋 检测到蓝图文件"
    echo ""

    # 显示任务
    py << 'PYTHON_PREVIEW'
import json
try:
    data = json.load(open('.janus/project_state.json', 'r', encoding='utf-8'))
    tasks = data.get('blueprint', [])
    pending = [t for t in tasks if t.get('status') == 'PENDING']
    completed = [t for t in tasks if t.get('status') == 'COMPLETED']

    print(f"待执行: {len(pending)} 个任务")
    print(f"已完成: {len(completed)} 个任务")
    print("")

    if pending:
        print("待执行任务:")
        for i, t in enumerate(pending[:3], 1):
            print(f"  {i}. {t.get('task_name', '未知')}")
        if len(pending) > 3:
            print(f"  ... 还有 {len(pending) - 3} 个")
except Exception as e:
    print(f"(无法解析蓝图: {str(e)})")
PYTHON_PREVIEW

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "请选择操作:"
    echo "  1. 启动Ralph自动执行（推荐）"
    echo "  2. 与Brain重新规划任务"
    echo "  3. 查看蓝图详情"
    echo "  4. 清除蓝图重新开始"
    echo "  q. 退出"
    echo ""

    read -p "👉 您的选择: " choice

    case "$choice" in
        1)
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🚀 启动Ralph自动执行..."
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            bash ralph_auto_stream_fixed.sh
            ;;
        2)
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📝 请在Brain终端与Claude重新规划任务"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "规划完成后再运行: bash start.sh"
            echo ""
            ;;
        3)
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📄 蓝图详情"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            cat .janus/project_state.json
            echo ""
            ;;
        4)
            echo ""
            read -p "⚠️  确认清除蓝图？(y/n): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                mv .janus/project_state.json .janus/project_state.json.bak 2>/dev/null
                echo "✅ 蓝图已清除（备份到 project_state.json.bak）"
            else
                echo "已取消"
            fi
            echo ""
            ;;
        q|Q)
            echo ""
            echo "👋 再见"
            echo ""
            ;;
        *)
            echo ""
            echo "❌ 无效选择"
            echo ""
            ;;
    esac

else
    # 无蓝图 → 提示先规划
    echo "📝 尚未规划任务"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "双脑系统工作流程:"
    echo ""
    echo "  阶段1: 与Brain规划 (Brain终端)"
    echo "    ↓"
    echo "    描述需求 → Brain分析 → 生成蓝图"
    echo "    ↓"
    echo "  阶段2: Ralph自动执行 (当前终端)"
    echo "    ↓"
    echo "    bash start.sh → 启动Ralph"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📌 下一步:"
    echo "  1. 在Brain终端与Claude描述你的需求"
    echo "  2. Brain会生成蓝图文件 (.janus/project_state.json)"
    echo "  3. 然后在此终端运行: bash start.sh"
    echo ""
    echo "💡 示例需求:"
    echo '  "帮我实现一个用户登录功能"'
    echo '  "优化首页加载性能"'
    echo '  "修复XXX功能的bug"'
    echo ""
fi
