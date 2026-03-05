#!/bin/bash
# Ralph Auto-Iterative Mode with Manual Interrupt
# 自动迭代模式 + 随时可打断纠偏

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Ralph Auto Mode - 自动迭代可打断                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "💡 模式说明："
echo "  • Worker自动连续迭代（无需输入c）"
echo "  • 每轮结束后倒计时5秒"
echo "  • 倒计时期间按任意键可打断"
echo "  • 打断后进入交互模式，可提供反馈"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================
# 1. 配置智普API
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
interrupt_flag=".ralph/interrupt_flag"
rm -f "$user_feedback_file"
rm -f "$interrupt_flag"

# ============================================
# 3. 帮助函数
# ============================================

# 倒计时函数（可打断）
countdown_with_interrupt() {
    local seconds=$1
    local interrupted=false

    echo ""
    echo "⏱️  自动继续倒计时: ${seconds}秒（按任意键打断）"

    # 保存终端设置
    old_tty_settings=$(stty -g)

    # 设置为非阻塞输入
    stty -echo -icanon time 0 min 0

    for ((i=seconds; i>0; i--)); do
        printf "\r  ⏱️  %d秒后自动继续...（按任意键打断）   " $i

        # 检查是否有按键
        read -t 1 -n 1 key
        if [ $? -eq 0 ]; then
            interrupted=true
            break
        fi
    done

    # 恢复终端设置
    stty $old_tty_settings

    printf "\r%50s\r" " "  # 清除倒计时行

    if [ "$interrupted" = true ]; then
        return 1  # 被打断
    else
        return 0  # 自动继续
    fi
}

# 交互菜单
show_interrupt_menu() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏸️  已打断 - 请选择操作"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "可用命令："
    echo "  c / continue   → 立即继续下一轮"
    echo "  f / feedback   → 提供反馈意见"
    echo "  d / diff       → 查看代码差异"
    echo "  v / view       → 查看完整输出"
    echo "  a / auto       → 恢复自动模式"
    echo "  q / quit       → 退出Ralph"
    echo ""

    while true; do
        read -p "👉 您的指令: " user_command

        case "$user_command" in
            c|continue)
                echo "  ✅ 继续下一轮..."
                echo ""
                return 0
                ;;

            f|feedback)
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "💬 输入您的反馈（输入'END'结束）："
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo ""

                > "$user_feedback_file"

                while true; do
                    read -p "  " feedback_line
                    if [ "$feedback_line" = "END" ]; then
                        break
                    fi
                    echo "$feedback_line" >> "$user_feedback_file"
                done

                echo ""
                echo "  ✅ 反馈已保存，继续下一轮..."
                echo ""
                return 0
                ;;

            d|diff)
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                git diff 2>/dev/null || echo "  (无git仓库或无变更)"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo ""
                ;;

            v|view)
                if [ -f ".ralph/loop_${loop_count}_output.txt" ]; then
                    echo ""
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    cat ".ralph/loop_${loop_count}_output.txt"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo ""
                fi
                ;;

            a|auto)
                echo "  ✅ 恢复自动模式..."
                echo ""
                return 0
                ;;

            q|quit)
                echo ""
                echo "👋 退出Ralph"
                exit 0
                ;;

            *)
                echo "  ❌ 无效命令，请重试"
                ;;
        esac
    done
}

# ============================================
# 4. 主循环（自动迭代+可打断）
# ============================================
while [ $loop_count -lt $max_loops ]; do
    loop_count=$((loop_count + 1))

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔄 Loop $loop_count"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # ----------------------------------------
    # Step 1: 生成指令
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
        echo "💬 应用用户反馈..."
        echo ""
        cat "$user_feedback_file" >> .ralph/current_instruction.txt
        rm -f "$user_feedback_file"
    fi

    # ----------------------------------------
    # Step 4: 执行Worker
    # ----------------------------------------
    echo "🤖 Worker执行中（智普API）..."
    echo ""

    instruction=$(cat .ralph/current_instruction.txt)
    result=$(echo "$instruction" | claude 2>&1)

    echo "$result" > .ralph/loop_${loop_count}_output.txt

    # 显示简要输出（前30行）
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📤 Worker输出（前30行）："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$result" | head -30
    echo ""
    echo "  💾 完整输出: .ralph/loop_${loop_count}_output.txt"
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
    # Step 6: 显示变更
    # ----------------------------------------
    echo "📁 本轮变更："
    git status -s 2>/dev/null | head -10 || echo "  (无变更)"
    echo ""

    # ----------------------------------------
    # Step 7: 自动继续倒计时（可打断）
    # ----------------------------------------
    countdown_with_interrupt 5

    if [ $? -eq 1 ]; then
        # 被打断，进入交互模式
        show_interrupt_menu
    else
        # 自动继续
        echo "  ✅ 自动继续下一轮..."
        echo ""
    fi
done

# ============================================
# 5. 完成总结
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎊 Ralph Auto Mode 完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 统计："
echo "  总循环次数: $loop_count"
echo "  输出日志: .ralph/loop_*.txt"
echo ""
