#!/bin/bash
# Ralph Auto Stream Mode - 修复版（使用正确的流式方法）
# 基于原始 ralph_loop.sh 的流式输出实现

# ============================================
# 0. 切换到正确的工作目录
# ============================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 读取project_state.json获取工作目录
if [ -f "$SCRIPT_DIR/.janus/project_state.json" ]; then
    BASE_PATH=$(cat "$SCRIPT_DIR/.janus/project_state.json" | grep '"base_path"' | cut -d'"' -f4 | sed 's/\\\\/\//g')
    if [ -n "$BASE_PATH" ] && [ -d "$BASE_PATH" ]; then
        cd "$BASE_PATH" || {
            echo "⚠️  无法切换到工作目录: $BASE_PATH"
            echo "使用当前目录继续..."
        }
        echo "📂 工作目录: $(pwd)"
    fi
fi

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Ralph Auto Stream Mode - 真正的流式输出（修复版）        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "💡 模式说明："
echo "  • Worker自动连续迭代"
echo "  • 真正的实时流式输出（逐字显示）"
echo "  • 每轮结束后5秒倒计时"
echo "  • 最少迭代2轮以验证结果"
echo ""
echo "🎮 交互控制："
echo "  • 随时按 Ctrl+C 打断循环"
echo "  • 可以提供反馈纠错（选择 f）"
echo "  • 可以查看当前状态（选择 s）"
echo "  • 可以继续执行（选择 c）"
echo "  • 可以退出Ralph（选择 q）"
echo ""
echo "💬 实时纠错示例："
echo "  1. 发现Worker理解错了 → Ctrl+C"
echo "  2. 选择 f (feedback)"
echo "  3. 输入反馈（如：不要删除代码，只是隐藏）"
echo "  4. 输入 END 结束"
echo "  5. Worker下一轮会看到你的反馈并调整"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================
# 1. 配置智普API（使用主目录路径）
# ============================================
echo "📡 配置智普API..."

CONFIG_FILE="$SCRIPT_DIR/.janus/config.json"

if [ -f "$CONFIG_FILE" ]; then
    ZHIPU_KEY=$(cat "$CONFIG_FILE" | grep '"ZHIPU_API_KEY"' | cut -d'"' -f4)

    if [ -n "$ZHIPU_KEY" ] && [ "$ZHIPU_KEY" != "" ]; then
        export ANTHROPIC_API_KEY="$ZHIPU_KEY"
        export ANTHROPIC_AUTH_TOKEN="$ZHIPU_KEY"
        echo "  ✅ API Key loaded"
    else
        echo "  ⚠️  ZHIPU_API_KEY not found"
        read -p "  请输入智普API Key: " ZHIPU_KEY
        export ANTHROPIC_API_KEY="$ZHIPU_KEY"
        export ANTHROPIC_AUTH_TOKEN="$ZHIPU_KEY"
    fi

    BASE_URL=$(cat "$CONFIG_FILE" | grep '"ANTHROPIC_BASE_URL"' | cut -d'"' -f4)
    OPUS_MODEL=$(cat "$CONFIG_FILE" | grep '"ANTHROPIC_DEFAULT_OPUS_MODEL"' | cut -d'"' -f4)
    SONNET_MODEL=$(cat "$CONFIG_FILE" | grep '"ANTHROPIC_DEFAULT_SONNET_MODEL"' | cut -d'"' -f4)
    HAIKU_MODEL=$(cat "$CONFIG_FILE" | grep '"ANTHROPIC_DEFAULT_HAIKU_MODEL"' | cut -d'"' -f4)
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
# 2. 检查依赖
# ============================================
echo "🔍 检查依赖..."

if ! command -v jq &> /dev/null; then
    echo "  ❌ 错误：需要安装 jq 来解析流式输出"
    echo "  请安装 jq: https://stedolan.github.io/jq/download/"
    exit 1
fi

if ! command -v stdbuf &> /dev/null; then
    echo "  ⚠️  警告：stdbuf 不可用，流式输出可能有延迟"
    USE_STDBUF=false
else
    USE_STDBUF=true
fi

echo "  ✅ 依赖检查完成"
echo ""

# ============================================
# 3. 检查蓝图
# ============================================
# 使用主目录路径（蓝图文件在主目录，不在工作目录）
PROJECT_STATE_FILE="$SCRIPT_DIR/.janus/project_state.json"
INSTRUCTION_FILE="$SCRIPT_DIR/.ralph/current_instruction.txt"
USER_FEEDBACK_FILE="$SCRIPT_DIR/.ralph/user_feedback.txt"
LOG_DIR="$SCRIPT_DIR/.ralph/logs"

if [ ! -f "$PROJECT_STATE_FILE" ]; then
    echo "❌ 错误：蓝图文件不存在"
    echo "   期望位置: $PROJECT_STATE_FILE"
    exit 1
fi

# 创建日志目录
mkdir -p "$LOG_DIR"

TASK_COUNT=$(cat "$PROJECT_STATE_FILE" | grep -c "task_name" || echo "0")
echo "📋 蓝图文件: $PROJECT_STATE_FILE"
echo "  任务数量: $TASK_COUNT"
echo ""

# ============================================
# 4. 初始化
# ============================================
loop_count=0
max_loops=50
min_loops=2

rm -f "$USER_FEEDBACK_FILE"

echo "🚀 启动Ralph循环（Ctrl+C 随时打断）"
echo ""

# ============================================
# 5. 信号处理
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
                > "$USER_FEEDBACK_FILE"
                while true; do
                    read -p "  " feedback_line
                    if [ "$feedback_line" = "END" ]; then
                        break
                    fi
                    echo "$feedback_line" >> "$USER_FEEDBACK_FILE"
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
# 6. jq 过滤器（提取流式文本）
# ============================================
# 实用版过滤器：显示文本、工具标记和结果摘要
# ============================================
# 改进版：尝试显示更多工具调用详情
jq_filter='
    if .type == "stream_event" then
        # 显示文本内容
        if .event.type == "content_block_delta" and .event.delta.type == "text_delta" then
            .event.delta.text
        # 显示工具调用标记
        elif .event.type == "content_block_start" and .event.content_block.type == "tool_use" then
            "\n\n⚡ [" + .event.content_block.name + "]\n"
        # 空行分隔
        elif .event.type == "content_block_stop" then
            ""
        else
            empty
        end
    elif .type == "user" and .message.role == "user" then
        # 显示工具调用结果
        if .message.content[0].type == "tool_result" then
            result = .message.content[0].content
            # 显示错误
            if .message.content[0].is_error == true then
                "❌ " + (result | split("\n")[0]) + "\n"
            else
                # 尝试显示有用信息
                if result | test("^[A-Z]") then
                    # 结果首行是大写，可能是命令输出
                    "📊 " + (result | split("\n")[0]) + "\n"
                elif result | test("^\\{") then
                    # JSON输出
                    "✅ 完成\n"
                elif result | length > 100 then
                    # 长输出，只显示前100字符
                    "✅ " + (result[:100] | tostring) + "...\n"
                else
                    # 短输出
                    "✅ " + result + "\n"
                end
            end
        else
            empty
        end
    else
        empty
    end
'


# ============================================
# 7. 主循环
# ============================================
while [ $loop_count -lt $max_loops ]; do
    loop_count=$((loop_count + 1))

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔄 Loop $loop_count / $max_loops"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # 生成指令（从主目录运行dealer）
    echo "📝 生成执行指令..."
    (cd "$SCRIPT_DIR" && py dealer_enhanced.py --ralph-mode > /dev/null 2>&1)

    if [ ! -f "$INSTRUCTION_FILE" ]; then
        echo "❌ 错误：指令生成失败"
        break
    fi

    # 自动追加完成信号要求和中文强制协议
    # 检查是否已经添加过
    if ! grep -q "绝对要求：中文输出" "$INSTRUCTION_FILE"; then
        # 在指令开头插入中文强制要求
        TEMP_FILE=$(mktemp)
        echo "# ⚠️⚠️⚠️ 中文输出强制要求 ⚠️⚠️⚠️" > "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo "**你必须使用中文输出所有内容！**" >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo "错误的示例（禁止）：" >> "$TEMP_FILE"
        echo "  - \"I will create the file...\"" >> "$TEMP_FILE"
        echo "  - \"Let me check the file...\"" >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo "正确的示例（必须）：" >> "$TEMP_FILE"
        echo "  - \"我将创建文件...\"" >> "$TEMP_FILE"
        echo "  - \"让我检查文件...\"" >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo "## 📋 任务" >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"

        # 追加原指令内容
        cat "$INSTRUCTION_FILE" >> "$TEMP_FILE"

        # 追加末尾的完成信号要求
        echo "" >> "$TEMP_FILE"
        echo "---" >> "$TEMP_FILE"
        echo "## ⚠️️⚠️⚠️ 绝对要求：中文输出 + 完成信号 ⚠️⚠️⚠️" >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo "### 🚫 禁止英文输出 🚫" >> "$TEMP_FILE"
        echo "你输出的**所有文字必须是中文**，包括但不限于：" >> "$TEMP_FILE"
        echo "- ✅ 思考过程 → 中文" >> "$TEMP_FILE"
        echo "- ✅ 工具调用说明 → 中文" >> "$TEMP_FILE"
        echo "- ✅ 完成总结 → 中文" >> "$TEMP_FILE"
        echo "- ❌ 禁止英文输出（代码关键字、变量名、函数名除外）" >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo "### 📝 完成信号（必须输出）" >> "$TEMP_FILE"
        echo "**任务完成后，必须按以下格式输出：**" >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo '```xml' >> "$TEMP_FILE"
        echo '<learning>' >> "$TEMP_FILE"
        echo "  <problem>用一句话描述本次任务</problem>" >> "$TEMP_FILE"
        echo "  <solution>用1-3句话描述解决方案</solution>" >> "$TEMP_FILE"
        echo '  <pitfalls>（可选）注意事项</pitfalls>' >> "$TEMP_FILE"
        echo "</learning>" >> "$TEMP_FILE"
        echo '```' >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo '```xml' >> "$TEMP_FILE"
        echo "<promise>COMPLETE</promise>" >> "$TEMP_FILE"
        echo '```' >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo "**⚠️ 警告：没有完成信号，系统将永远循环！**" >> "$TEMP_FILE"
        echo "" >> "$TEMP_FILE"
        echo "**每次循环开始时，请先用中文确认：**" >> "$TEMP_FILE"
        echo '"我已理解任务：[任务名称]，我将用中文输出所有内容。"' >> "$TEMP_FILE"

        # 替换原文件
        mv "$TEMP_FILE" "$INSTRUCTION_FILE"
    fi

    echo "  ✅ 指令已生成"

    current_task=$(cat "$PROJECT_STATE_FILE" | grep -m1 '"task_name"' | cut -d'"' -f4 2>/dev/null || echo "未知任务")
    echo "  📋 任务: $current_task"
    echo ""

    # 检查用户反馈
    if [ -f "$USER_FEEDBACK_FILE" ]; then
        echo "💬 检测到用户反馈，整合到指令中..."
        echo "" >> "$INSTRUCTION_FILE"
        echo "## 用户反馈（必须优先处理）：" >> "$INSTRUCTION_FILE"
        cat "$USER_FEEDBACK_FILE" >> "$INSTRUCTION_FILE"
        rm -f "$USER_FEEDBACK_FILE"
        echo ""
    fi

    # 执行 Worker（真正的流式输出）
    echo "🤖 Worker执行中（智普API）- 实时流式输出："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    log_file="$LOG_DIR/loop_${loop_count}.log"
    stream_file="$LOG_DIR/loop_${loop_count}_stream.log"

    # 关键：使用正确的流式输出方法（基于原始 ralph_loop.sh）
    # 1. --output-format stream-json（流式JSON格式）
    # 2. --include-partial-messages（包含部分消息）
    # 3. --verbose（详细输出）
    # 4. jq 解析流式 JSON
    # 5. stdbuf 禁用缓冲

    set -o pipefail

    if [ "$USE_STDBUF" = true ]; then
        # 有 stdbuf：完整的流式管道
        cat "$INSTRUCTION_FILE" | \
            stdbuf -oL claude \
                --dangerously-skip-permissions \
                --output-format stream-json \
                --verbose \
                --include-partial-messages \
                2>&1 | \
            stdbuf -oL tee "$stream_file" | \
            stdbuf -oL jq --unbuffered -j "$jq_filter" 2>/dev/null | \
            tee "$log_file"
    else
        # 没有 stdbuf：简化的流式管道
        cat "$INSTRUCTION_FILE" | \
            claude \
                --dangerously-skip-permissions \
                --output-format stream-json \
                --verbose \
                --include-partial-messages \
                2>&1 | \
            tee "$stream_file" | \
            jq --unbuffered -j "$jq_filter" 2>/dev/null | \
            tee "$log_file"
    fi

    pipe_status=("${PIPESTATUS[@]}")
    set +o pipefail

    worker_exit_code=${pipe_status[0]}

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  💾 日志已保存: $log_file"
    echo "  💾 原始流: $stream_file"
    echo ""

    # 检查完成信号
    if grep -q "<promise>.*COMPLETE.*</promise>" "$log_file" 2>/dev/null || \
       grep -q "<promise>.*COMPLETE.*</promise>" "$stream_file" 2>/dev/null; then

        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📚 提取并存储执行经验..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""

        # 使用Python提取<learning>标签并存储到Hippocampus
        python3 << PYTHON_EXTRACT
import re
import sys
import os

# 添加.janus到路径
sys.path.insert(0, os.path.join(os.getcwd(), '.janus'))

try:
    from core.hippocampus import Hippocampus
except ImportError:
    print("  ⚠️  无法导入Hippocampus模块")
    sys.exit(0)

# 读取日志文件
log_content = ''
log_file = '$log_file'
stream_file = '$stream_file'

if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        log_content += f.read()

if os.path.exists(stream_file):
    with open(stream_file, 'r', encoding='utf-8', errors='ignore') as f:
        log_content += f.read()

# 提取<learning>标签内容
learning_match = re.search(r'<learning>(.*?)</learning>', log_content, re.DOTALL | re.IGNORECASE)

if learning_match:
    learning_content = learning_match.group(1)

    # 提取problem, solution, pitfalls
    problem_match = re.search(r'<problem>(.*?)</problem>', learning_content, re.DOTALL | re.IGNORECASE)
    solution_match = re.search(r'<solution>(.*?)</solution>', learning_content, re.DOTALL | re.IGNORECASE)
    pitfalls_match = re.search(r'<pitfalls>(.*?)</pitfalls>', learning_content, re.DOTALL | re.IGNORECASE)

    if problem_match and solution_match:
        problem = problem_match.group(1).strip()
        solution = solution_match.group(1).strip()

        # 添加坑点信息（如果有）
        if pitfalls_match:
            pitfalls = pitfalls_match.group(1).strip()
            if pitfalls:
                solution += "\n\n⚠️ 注意事项: " + pitfalls

        # 存储到Hippocampus
        try:
            hippo = Hippocampus()
            hippo.store(problem, solution)

            print("  ✅ 经验已存入海马体（Hippocampus）")
            print("")
            print(f"  📌 问题: {problem[:80]}{'...' if len(problem) > 80 else ''}")
            print(f"  📌 方案: {solution[:100]}{'...' if len(solution) > 100 else ''}")
            print(f"  📊 海马体当前记忆数: {len(hippo.mem)} 条")
            print("")
        except Exception as e:
            print(f"  ⚠️  存储失败: {e}")
            print("")
    else:
        print("  ⚠️  Worker未输出完整的 <problem> 和 <solution> 标签")
        print("     （经验未能存储，但任务已完成）")
        print("")
else:
    print("  ⚠️  未找到 <learning> 标签")
    print("     Worker可能没有遵守经验学习协议")
    print("     （经验未能存储，但任务已完成）")
    print("")
PYTHON_EXTRACT

        # 如果还没达到最少轮数，询问是否确认完成
        if [ $loop_count -lt $min_loops ]; then
            echo "💡 检测到完成信号，但只迭代了 $loop_count 轮"
            echo "  建议至少迭代 $min_loops 轮以验证结果"
            echo ""
            read -t 10 -p "是否确认任务已完成并退出？(y/n): " confirm_exit
            if [ "$confirm_exit" = "y" ] || [ "$confirm_exit" = "Y" ]; then
                echo "🎉 用户确认完成！"
                echo ""
                break
            else
                echo "  ✅ 继续迭代..."
                echo ""
            fi
        else
            echo "🎉 检测到完成信号！"
            echo ""
            break
        fi
    fi

    # 显示变更
    echo "📁 本轮变更："

    # 尝试从主目录检测git变更
    if cd "$SCRIPT_DIR" && git status -s &>/dev/null; then
        # 有git仓库
        git status -s 2>/dev/null | head -10
        cd - > /dev/null
    else
        # 无git仓库，尝试检测创建/修改的文件
        cd - > /dev/null
        echo "  (无Git仓库 - 变更未检测)"
    fi
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
# 8. 完成总结
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎊 Ralph Auto Stream 完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 统计："
echo "  总循环次数: $loop_count"
echo "  日志目录: .ralph/logs/"
echo ""
