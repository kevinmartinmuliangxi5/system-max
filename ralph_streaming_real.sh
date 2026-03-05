#!/bin/bash
# Ralph Real Streaming Mode - 真正的实时流式输出
# 使用 --print --output-format=stream-json 实现真正的流式效果

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Ralph Real Streaming - 真正的实时流式输出                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "💡 模式说明："
echo "  • 使用 Claude Code 的流式 JSON 输出"
echo "  • 真正的逐字实时显示"
echo "  • 每轮结束后5秒倒计时"
echo "  • 倒计时期间按 Ctrl+C 可打断"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================
# 1. 配置智普API
# ============================================
echo "📡 配置智普API..."

if [ -f ".janus/config.json" ]; then
    ZHIPU_KEY=$(cat .janus/config.json | grep '"ZHIPU_API_KEY"' | cut -d'"' -f4)

    if [ -n "$ZHIPU_KEY" ] && [ "$ZHIPU_KEY" != "" ]; then
        export ANTHROPIC_API_KEY="$ZHIPU_KEY"
        echo "  ✅ API Key loaded"
    else
        echo "  ⚠️  ZHIPU_API_KEY not found"
        read -p "  请输入智普API Key: " ZHIPU_KEY
        export ANTHROPIC_API_KEY="$ZHIPU_KEY"
    fi

    BASE_URL=$(cat .janus/config.json | grep '"ANTHROPIC_BASE_URL"' | cut -d'"' -f4)
    OPUS_MODEL=$(cat .janus/config.json | grep '"ANTHROPIC_DEFAULT_OPUS_MODEL"' | cut -d'"' -f4)
    SONNET_MODEL=$(cat .janus/config.json | grep '"ANTHROPIC_DEFAULT_SONNET_MODEL"' | cut -d'"' -f4)
    HAIKU_MODEL=$(cat .janus/config.json | grep '"ANTHROPIC_DEFAULT_HAIKU_MODEL"' | cut -d'"' -f4)
else
    ZHIPU_KEY=""
    BASE_URL="https://open.bigmodel.cn/api/anthropic"
    OPUS_MODEL="glm-4.7"
    SONNET_MODEL="glm-4.7"
    HAIKU_MODEL="glm-4.5-air"
fi

export ANTHROPIC_BASE_URL="${BASE_URL:-https://open.bigmodel.cn/api/anthropic}"
export ANTHROPIC_DEFAULT_OPUS_MODEL="${OPUS_MODEL:-glm-4.7}"
export ANTHROPIC_DEFAULT_SONNET_MODEL="${SONNET_MODEL:-glm-4.7}"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="${HAIKU_MODEL:-glm-4.5-air}"

export API_TIMEOUT_MS="300000"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
export CLAUDE_DISABLE_SANDBOX=1

echo "  ✅ API Endpoint: $ANTHROPIC_BASE_URL"
echo "  ✅ Sonnet Model: $ANTHROPIC_DEFAULT_SONNET_MODEL"
echo ""

# ============================================
# 2. 检查蓝图
# ============================================
if [ ! -f ".janus/project_state.json" ]; then
    echo "❌ 错误：蓝图文件不存在"
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
# 4. 信号处理
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
    echo "  f / feedback   → 提供反馈意见"
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
                echo "  ✅ 反馈已保存"
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
# 5. Python 流式处理脚本
# ============================================
cat > .ralph/stream_processor.py << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
"""流式输出处理器 - 从 stream-json 提取文本并实时显示"""
import sys
import json
import time

def process_stream():
    """处理流式 JSON 输出"""
    full_text = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            data = json.loads(line)

            # 处理不同类型的消息
            if data.get('type') == 'content_block_delta':
                # 获取增量文本
                delta = data.get('delta', {})
                if delta.get('type') == 'text_delta':
                    text = delta.get('text', '')
                    # 实时输出
                    print(text, end='', flush=True)
                    full_text.append(text)

            elif data.get('type') == 'message_start':
                # 消息开始
                pass

            elif data.get('type') == 'message_stop':
                # 消息结束
                print()  # 换行
                break

        except json.JSONDecodeError:
            # 不是 JSON，可能是普通文本
            print(line)
            full_text.append(line)

    # 保存完整文本到文件
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w', encoding='utf-8') as f:
            f.write(''.join(full_text))

    return ''.join(full_text)

if __name__ == '__main__':
    text = process_stream()
    # 返回是否包含完成信号
    if '<promise>' in text and 'COMPLETE' in text and '</promise>' in text:
        sys.exit(0)  # 完成
    else:
        sys.exit(1)  # 未完成
PYTHON_SCRIPT

chmod +x .ralph/stream_processor.py

# ============================================
# 6. 主循环
# ============================================
while [ $loop_count -lt $max_loops ]; do
    loop_count=$((loop_count + 1))

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔄 Loop $loop_count / $max_loops"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # 生成指令
    echo "📝 生成执行指令..."
    py dealer_enhanced.py --ralph-mode > /dev/null 2>&1

    if [ ! -f ".ralph/current_instruction.txt" ]; then
        echo "❌ 错误：指令生成失败"
        break
    fi

    echo "  ✅ 指令已生成"

    current_task=$(cat .janus/project_state.json | grep -m1 '"task_name"' | cut -d'"' -f4 2>/dev/null || echo "未知任务")
    echo "  📋 任务: $current_task"
    echo ""

    # 检查用户反馈
    if [ -f "$user_feedback_file" ]; then
        echo "💬 检测到用户反馈，整合到指令中..."
        echo "" >> .ralph/current_instruction.txt
        echo "## 用户反馈（必须优先处理）：" >> .ralph/current_instruction.txt
        cat "$user_feedback_file" >> .ralph/current_instruction.txt
        rm -f "$user_feedback_file"
        echo ""
    fi

    # 执行 Worker（真正的流式输出）
    echo "🤖 Worker执行中（智普API）- 实时流式输出："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    log_file=".ralph/logs/loop_${loop_count}.log"

    # 关键：使用 --print 模式 + --output-format=stream-json + Python 处理器
    cat .ralph/current_instruction.txt | \
        claude --print \
               --dangerously-skip-permissions \
               --output-format=stream-json \
               --include-partial-messages \
               2>&1 | \
        python .ralph/stream_processor.py "$log_file"

    worker_exit_code=$?

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  💾 日志已保存: $log_file"
    echo ""

    # 检查完成信号
    if [ $worker_exit_code -eq 0 ]; then
        echo "🎉 检测到完成信号！"
        echo ""
        break
    fi

    # 显示变更
    echo "📁 本轮变更："
    git status -s 2>/dev/null | head -10 || echo "  (无Git或无变更)"
    echo ""

    # 倒计时
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
# 7. 完成总结
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎊 Ralph Real Streaming 完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 统计："
echo "  总循环次数: $loop_count"
echo "  日志目录: .ralph/logs/"
echo ""
