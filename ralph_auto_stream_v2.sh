#!/bin/bash
# Ralph Auto Mode with Real-time Streaming + Interrupt V2
# 使用直接文件读取方式实现真正的流式输出

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Ralph Auto Stream Mode V2 - 真正的流式输出               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "💡 模式说明："
echo "  • Worker自动连续迭代"
echo "  • 真正的实时流式输出（像终端一样）"
echo "  • 每轮结束后5秒倒计时"
echo "  • 倒计时期间按 Ctrl+C 可打断"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================
# 1. 配置智普API（使用 GLM-4.7 模型映射）
# ============================================
echo "📡 配置智普API..."

if [ -f ".janus/config.json" ]; then
    ZHIPU_KEY=$(cat .janus/config.json | grep '"ZHIPU_API_KEY"' | cut -d'"' -f4)

    if [ -n "$ZHIPU_KEY" ] && [ "$ZHIPU_KEY" != "" ]; then
        export ANTHROPIC_API_KEY="$ZHIPU_KEY"
        echo "  ✅ API Key loaded"
    else
        echo "  ⚠️  ZHIPU_API_KEY not found in .janus/config.json"
        read -p "  请输入智普API Key: " ZHIPU_KEY
        export ANTHROPIC_API_KEY="$ZHIPU_KEY"
    fi

    # 读取模型映射配置
    BASE_URL=$(cat .janus/config.json | grep '"ANTHROPIC_BASE_URL"' | cut -d'"' -f4)
    OPUS_MODEL=$(cat .janus/config.json | grep '"ANTHROPIC_DEFAULT_OPUS_MODEL"' | cut -d'"' -f4)
    SONNET_MODEL=$(cat .janus/config.json | grep '"ANTHROPIC_DEFAULT_SONNET_MODEL"' | cut -d'"' -f4)
    HAIKU_MODEL=$(cat .janus/config.json | grep '"ANTHROPIC_DEFAULT_HAIKU_MODEL"' | cut -d'"' -f4)
else
    echo "  ⚠️  .janus/config.json not found"
    read -p "  请输入智普API Key: " ZHIPU_KEY
    export ANTHROPIC_API_KEY="$ZHIPU_KEY"

    BASE_URL="https://open.bigmodel.cn/api/anthropic"
    OPUS_MODEL="glm-4.7"
    SONNET_MODEL="glm-4.7"
    HAIKU_MODEL="glm-4.5-air"
fi

# 配置 API Endpoint 和模型映射（GLM Coding Plan 推荐方式）
export ANTHROPIC_BASE_URL="${BASE_URL:-https://open.bigmodel.cn/api/anthropic}"
export ANTHROPIC_DEFAULT_OPUS_MODEL="${OPUS_MODEL:-glm-4.7}"
export ANTHROPIC_DEFAULT_SONNET_MODEL="${SONNET_MODEL:-glm-4.7}"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="${HAIKU_MODEL:-glm-4.5-air}"

# 设置超时和禁用非必要流量
export API_TIMEOUT_MS="300000"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

# 关键：禁用沙盒模式，允许完全文件访问
export CLAUDE_DISABLE_SANDBOX=1

echo "  ✅ API Endpoint: $ANTHROPIC_BASE_URL"
echo "  ✅ Sonnet Model: $ANTHROPIC_DEFAULT_SONNET_MODEL"
echo ""

# ============================================
# 2. 检查蓝图
# ============================================
if [ ! -f ".janus/project_state.json" ]; then
    echo "❌ 错误：蓝图文件不存在"
    echo "  请先在Brain终端生成任务蓝图"
    exit 1
fi

TASK_COUNT=$(cat .janus/project_state.json | grep -c "task_name" || echo "0")
echo "📋 蓝图文件: .janus/project_state.json"
echo "  任务数量: $TASK_COUNT"
echo ""

# ============================================
# 3. 初始化
# ============================================
loop_count=0
max_loops=50
user_feedback_file=".ralph/user_feedback.txt"
mkdir -p .ralph/logs

rm -f "$user_feedback_file"

echo "🚀 启动Ralph循环（Ctrl+C 随时打断）"
echo ""

# ============================================
# 4. 信号处理（捕获Ctrl+C）
# ============================================
interrupted=false

handle_interrupt() {
    interrupted=true
    echo ""
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏸️  检测到中断 (Ctrl+C)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "请选择操作："
    echo "  c / continue   → 继续当前循环"
    echo "  f / feedback   → 提供反馈意见（下一轮应用）"
    echo "  s / status     → 查看状态"
    echo "  q / quit       → 退出Ralph"
    echo ""

    while true; do
        read -p "👉 您的指令: " user_command

        case "$user_command" in
            c|continue)
                echo "  ✅ 继续..."
                interrupted=false
                return 0
                ;;

            f|feedback)
                echo ""
                echo "💬 输入反馈（输入'END'结束）："
                > "$user_feedback_file"

                while true; do
                    read -p "  " feedback_line
                    if [ "$feedback_line" = "END" ]; then
                        break
                    fi
                    echo "$feedback_line" >> "$user_feedback_file"
                done

                echo ""
                echo "  ✅ 反馈已保存，下一轮应用"
                interrupted=false
                return 0
                ;;

            s|status)
                echo ""
                echo "📊 当前状态："
                echo "  循环次数: $loop_count"
                echo "  最大循环: $max_loops"
                git status -s 2>/dev/null | head -10 || echo "  无Git仓库"
                echo ""
                ;;

            q|quit)
                echo ""
                echo "👋 退出Ralph"
                exit 0
                ;;

            *)
                echo "  ❌ 无效命令"
                ;;
        esac
    done
}

trap handle_interrupt SIGINT

# ============================================
# 5. 主循环
# ============================================
while [ $loop_count -lt $max_loops ]; do
    loop_count=$((loop_count + 1))

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔄 Loop $loop_count / $max_loops"
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

    # 显示当前任务
    current_task=$(cat .janus/project_state.json | grep -m1 '"task_name"' | cut -d'"' -f4 2>/dev/null || echo "未知任务")
    echo "  📋 任务: $current_task"
    echo ""

    # ----------------------------------------
    # Step 2: 检查用户反馈
    # ----------------------------------------
    if [ -f "$user_feedback_file" ]; then
        echo "💬 检测到用户反馈，整合到指令中..."
        echo "" >> .ralph/current_instruction.txt
        echo "## 用户反馈（必须优先处理）：" >> .ralph/current_instruction.txt
        cat "$user_feedback_file" >> .ralph/current_instruction.txt
        rm -f "$user_feedback_file"
        echo ""
    fi

    # ----------------------------------------
    # Step 3: 执行Worker（真正的流式输出）
    # ----------------------------------------
    echo "🤖 Worker执行中（智普API）- 实时流式输出："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    log_file=".ralph/logs/loop_${loop_count}.log"

    # 方案1: 创建临时脚本让 Claude 直接执行
    temp_script=".ralph/temp_instruction_${loop_count}.sh"
    echo "#!/bin/bash" > "$temp_script"
    echo "cat <<'INSTRUCTION_EOF'" >> "$temp_script"
    cat .ralph/current_instruction.txt >> "$temp_script"
    echo "" >> "$temp_script"
    echo "INSTRUCTION_EOF" >> "$temp_script"
    chmod +x "$temp_script"

    # 使用 script 命令创建伪终端（如果可用）
    # 或直接运行 claude 命令让它以交互模式显示
    if command -v script &> /dev/null; then
        # Unix/Mac: 使用 script -q
        if [[ "$OSTYPE" == "darwin"* ]]; then
            bash "$temp_script" | script -q /dev/null claude --dangerously-skip-permissions 2>&1 | tee "$log_file"
        else
            # Linux: script -c
            script -q -c "bash \"$temp_script\" | claude --dangerously-skip-permissions" /dev/null 2>&1 | tee "$log_file"
        fi
    else
        # Windows or no script: 直接运行
        bash "$temp_script" | claude --dangerously-skip-permissions 2>&1 | tee "$log_file"
    fi

    worker_exit_code=${PIPESTATUS[1]}
    rm -f "$temp_script"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  💾 日志已保存: $log_file"
    echo ""

    # ----------------------------------------
    # Step 4: 检查完成信号（更严格的检查）
    # ----------------------------------------
    if grep -q "<promise>.*COMPLETE.*</promise>" "$log_file"; then
        echo "🎉 检测到完成信号！"
        echo ""
        break
    fi

    # 检查是否明确说明无需修改（也视为完成）
    if grep -qi "无需进行任何代码修改" "$log_file" || grep -qi "无需修改" "$log_file"; then
        echo "💡 Worker 报告无需修改 - 任务可能已完成"
        echo "  请检查日志确认: $log_file"
        echo ""
        echo "是否退出循环? (y/n)"
        read -t 10 -p "👉 " confirm_exit
        if [ "$confirm_exit" = "y" ]; then
            echo "✅ 手动确认退出"
            break
        fi
    fi

    # ----------------------------------------
    # Step 5: 显示变更
    # ----------------------------------------
    echo "📁 本轮变更："
    git status -s 2>/dev/null | head -10 || echo "  (无Git或无变更)"
    echo ""

    # ----------------------------------------
    # Step 6: 倒计时（可被Ctrl+C打断）
    # ----------------------------------------
    echo "⏱️  5秒后自动继续...（按 Ctrl+C 打断）"

    for i in {5..1}; do
        if [ "$interrupted" = true ]; then
            handle_interrupt
            break
        fi

        printf "\r  ⏱️  %d秒...   " $i
        sleep 1
    done

    if [ "$interrupted" = false ]; then
        printf "\r%30s\r" " "
        echo "  ✅ 自动继续下一轮..."
        echo ""
    fi

    interrupted=false
done

# ============================================
# 6. 完成总结
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎊 Ralph Auto Stream 完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 统计："
echo "  总循环次数: $loop_count"
echo "  日志目录: .ralph/logs/"
echo ""
echo "📁 查看所有日志："
echo "  ls -lh .ralph/logs/loop_*.log"
echo ""
