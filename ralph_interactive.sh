#!/bin/bash
# Ralph Interactive Mode - 交互式自主开发
# 每次循环后暂停，允许人工审查和干预

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Ralph Interactive Mode - 交互式自主开发                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "💡 模式说明："
echo "  • Worker执行一轮后自动暂停"
echo "  • 您可以审查代码，提出修改意见"
echo "  • 输入指令控制下一步行动"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================
# 1. 配置智普API（同start_ralph_with_zhipu.sh）
# ============================================
echo "📡 配置智普API..."

if [ -f ".janus/config.json" ]; then
    ZHIPU_KEY=$(cat .janus/config.json | grep -o '"ZHIPU_API_KEY": *"[^"]*"' | cut -d'"' -f4)
    export ANTHROPIC_API_KEY="$ZHIPU_KEY"
fi

export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
export ANTHROPIC_MODEL="glm-4-plus"

echo "  ✅ API配置完成"
echo ""

# ============================================
# 2. 初始化状态
# ============================================
loop_count=0
max_loops=50
user_feedback_file=".ralph/user_feedback.txt"
rm -f "$user_feedback_file"  # 清空旧的反馈

# ============================================
# 3. 交互式循环
# ============================================
while [ $loop_count -lt $max_loops ]; do
    loop_count=$((loop_count + 1))

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔄 Loop $loop_count"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # ----------------------------------------
    # Step 1: 生成指令（Dealer）
    # ----------------------------------------
    echo "📝 生成执行指令..."
    py dealer_enhanced.py --ralph-mode > /dev/null 2>&1

    if [ ! -f ".ralph/current_instruction.txt" ]; then
        echo "❌ 错误：指令生成失败"
        break
    fi

    echo "  ✅ 指令已生成"
    echo ""

    # ----------------------------------------
    # Step 2: 显示当前任务
    # ----------------------------------------
    current_task=$(cat .janus/project_state.json | grep -m1 '"task_name"' | cut -d'"' -f4)
    echo "📋 当前任务: $current_task"
    echo ""

    # ----------------------------------------
    # Step 3: 检查用户反馈
    # ----------------------------------------
    if [ -f "$user_feedback_file" ]; then
        echo "💬 检测到用户反馈："
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        cat "$user_feedback_file"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""

        # 将反馈追加到指令中
        echo "" >> .ralph/current_instruction.txt
        echo "## 用户反馈（必须优先处理）：" >> .ralph/current_instruction.txt
        cat "$user_feedback_file" >> .ralph/current_instruction.txt

        # 清空反馈文件
        rm -f "$user_feedback_file"

        echo "  ✅ 用户反馈已整合到指令中"
        echo ""
    fi

    # ----------------------------------------
    # Step 4: 执行Worker（智普API）
    # ----------------------------------------
    echo "🤖 Worker执行中（智普API）..."
    echo "  (这可能需要10-30秒...)"
    echo ""

    # 调用claude命令执行任务
    instruction=$(cat .ralph/current_instruction.txt)

    # 执行并捕获输出
    result=$(echo "$instruction" | claude 2>&1)

    # 保存完整输出
    echo "$result" > .ralph/loop_${loop_count}_output.txt

    # 显示输出（前50行）
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📤 Worker输出（前50行）："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$result" | head -50
    echo ""
    echo "  完整输出已保存到: .ralph/loop_${loop_count}_output.txt"
    echo ""

    # ----------------------------------------
    # Step 5: 检查完成信号
    # ----------------------------------------
    if echo "$result" | grep -q "<promise>.*COMPLETE.*</promise>"; then
        echo "🎉 检测到完成信号！"
        echo ""
        break
    fi

    # ----------------------------------------
    # Step 6: 显示变更文件
    # ----------------------------------------
    echo "📁 本轮变更的文件："
    git status -s 2>/dev/null || echo "  (无git仓库)"
    echo ""

    # ----------------------------------------
    # Step 7: 交互式暂停
    # ----------------------------------------
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏸️  暂停 - 请审查Worker的工作"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "可用命令："
    echo "  c / continue   → 继续下一轮"
    echo "  f / feedback   → 提供反馈意见"
    echo "  d / diff       → 查看代码差异"
    echo "  v / view       → 查看完整输出"
    echo "  s / skip       → 跳过当前任务"
    echo "  q / quit       → 退出Ralph"
    echo ""

    while true; do
        read -p "👉 您的指令: " user_command

        case "$user_command" in
            c|continue)
                echo "  ✅ 继续下一轮..."
                echo ""
                break
                ;;

            f|feedback)
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "💬 输入您的反馈（输入'END'结束）："
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo ""

                > "$user_feedback_file"  # 清空文件

                while true; do
                    read -p "  " feedback_line
                    if [ "$feedback_line" = "END" ]; then
                        break
                    fi
                    echo "$feedback_line" >> "$user_feedback_file"
                done

                echo ""
                echo "  ✅ 反馈已保存，将在下一轮应用"
                echo "  ✅ 继续下一轮..."
                echo ""
                break
                ;;

            d|diff)
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                git diff 2>/dev/null || echo "  (无git仓库或无变更)"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo ""
                ;;

            v|view)
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                cat .ralph/loop_${loop_count}_output.txt
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo ""
                ;;

            s|skip)
                echo "  ⏭️  跳过当前任务..."
                # TODO: 实现跳过逻辑
                break
                ;;

            q|quit)
                echo ""
                echo "👋 退出Ralph Interactive Mode"
                exit 0
                ;;

            *)
                echo "  ❌ 无效命令，请重试"
                ;;
        esac
    done
done

# ============================================
# 4. 完成总结
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎊 Ralph Interactive Mode 完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 统计："
echo "  总循环次数: $loop_count"
echo "  输出日志: .ralph/loop_*.txt"
echo ""
