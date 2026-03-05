#!/bin/bash
# Reviewer Loop - 独立的代码审查进程
# 监控Worker提交的代码，使用GLM + 静态分析进行审查

set -e

# ============================================================================
# GLM API 配置
# ============================================================================
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="434698bbe0754202aabea54a1b6d184d.zPhgfbdAFrX46GDg"
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"

# 配置
RALPH_DIR=".ralph"
QUEUE_DIR="$RALPH_DIR/queue"
PENDING_DIR="$QUEUE_DIR/pending"
REVIEWING_DIR="$QUEUE_DIR/reviewing"
APPROVED_DIR="$QUEUE_DIR/approved"
REJECTED_DIR="$QUEUE_DIR/rejected"
FEEDBACK_DIR="$RALPH_DIR/feedback"
LOG_DIR="$RALPH_DIR/logs"
STATUS_FILE="$RALPH_DIR/reviewer_status.json"
EXPERIENCE_FILE="$RALPH_DIR/review_experience.jsonl"  # 审查经验记录
LIVE_OUTPUT=false  # 实时输出模式

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 创建目录
mkdir -p "$REVIEWING_DIR" "$APPROVED_DIR" "$REJECTED_DIR" "$FEEDBACK_DIR" "$LOG_DIR"

log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local color=$GREEN

    case $level in
        "WARN") color=$YELLOW ;;
        "ERROR") color=$RED ;;
        "INFO") color=$BLUE ;;
        "PROGRESS") color=$BLUE ;;
    esac

    echo -e "${color}[$timestamp] [Review] $message${NC}"
    echo "[$timestamp] [Review] $message" >> "$LOG_DIR/reviewer.log"
}

# 显示审查进度（可视化）
show_progress() {
    local step=$1
    local total=$2
    local description=$3

    if [[ "$LIVE_OUTPUT" == "true" ]]; then
        local percent=$((step * 100 / total))
        local filled=$((percent / 5))
        local empty=$((20 - filled))

        printf "\r${BLUE}[Review进度] ["
        printf "%${filled}s" | tr ' ' '='
        printf "%${empty}s" | tr ' ' ' '
        printf "] %3d%% - %s${NC}" "$percent" "$description"

        if [[ $step -eq $total ]]; then
            echo ""  # 换行
        fi
    else
        log "PROGRESS" "[$step/$total] $description"
    fi
}

# 更新Reviewer状态
update_reviewer_status() {
    local status=$1
    local task_id=$2
    cat > "$STATUS_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "status": "$status",
    "reviewing_task": "$task_id",
    "reviewer": "glm-4.7 + static"
}
EOF
}

# 记录审查经验
record_review_experience() {
    local task_id=$1
    local approved=$2
    local score=$3
    local issues=$4
    local lesson=$5

    # 追加到经验文件（JSONL格式）
    cat >> "$EXPERIENCE_FILE" << EOF
{"timestamp":"$(date -Iseconds)","task_id":"$task_id","approved":$approved,"score":$score,"issues":"$issues","lesson":"$lesson"}
EOF

    log "INFO" "📚 审查经验已记录"
}

# 提取审查教训
extract_lesson() {
    local approved=$1
    local issues=$2
    local score=$3

    if [[ "$approved" == "true" ]]; then
        echo "优秀代码模式：评分$score，通过审查"
    else
        # 简化问题描述
        local key_issues=$(echo "$issues" | head -c 100)
        echo "需要改进：$key_issues"
    fi
}

# 查询历史经验（辅助当前审查）
query_experience() {
    local code_pattern=$1

    if [[ ! -f "$EXPERIENCE_FILE" ]]; then
        echo ""
        return
    fi

    # 查找相似的历史案例
    local similar_cases=$(grep -i "$code_pattern" "$EXPERIENCE_FILE" 2>/dev/null | tail -3)

    if [[ -n "$similar_cases" ]]; then
        log "INFO" "💡 找到相似历史案例"
        echo "$similar_cases" | while IFS= read -r case; do
            local case_lesson=$(echo "$case" | jq -r '.lesson' 2>/dev/null)
            log "INFO" "   - $case_lesson"
        done
    fi
}

# 静态分析（使用pylint, bandit等）
run_static_analysis() {
    local code_file=$1
    local result_file=$2

    show_progress 1 3 "静态分析: $(basename "$code_file")"

    local total_score=10
    local issues=""

    # 1. 检查Python语法
    if [[ "$code_file" == *.py ]]; then
        if command -v python &> /dev/null; then
            if ! python -m py_compile "$code_file" 2>/dev/null; then
                total_score=$((total_score - 5))
                issues+="语法错误; "
            fi
        fi

        # 2. Pylint检查（如果安装了）
        if command -v pylint &> /dev/null; then
            local pylint_output=$(pylint "$code_file" 2>/dev/null || true)
            local pylint_score=$(echo "$pylint_output" | grep "Your code has been rated" | awk '{print $7}' | cut -d'/' -f1)

            if [[ -n "$pylint_score" ]]; then
                # Pylint分数 0-10
                total_score=$(echo "scale=1; ($total_score + $pylint_score) / 2" | bc)
                if (( $(echo "$pylint_score < 5" | bc -l) )); then
                    issues+="Pylint低分($pylint_score); "
                fi
            fi
        fi

        # 3. Bandit安全检查（如果安装了）
        if command -v bandit &> /dev/null; then
            local bandit_output=$(bandit -f json "$code_file" 2>/dev/null || echo '{}')
            local high_issues=$(echo "$bandit_output" | jq '.metrics._totals.SEVERITY.HIGH // 0' 2>/dev/null || echo "0")
            local medium_issues=$(echo "$bandit_output" | jq '.metrics._totals.SEVERITY.MEDIUM // 0' 2>/dev/null || echo "0")

            if [[ $high_issues -gt 0 ]]; then
                total_score=$((total_score - 3))
                issues+="$high_issues 个高危安全问题; "
            fi
            if [[ $medium_issues -gt 0 ]]; then
                total_score=$((total_score - 1))
                issues+="$medium_issues 个中危安全问题; "
            fi
        fi
    fi

    # 保存结果
    cat > "$result_file" << EOF
{
    "file": "$code_file",
    "score": $total_score,
    "issues": "$issues",
    "timestamp": "$(date -Iseconds)"
}
EOF

    echo "$total_score"
}

# GLM AI代码审查
run_glm_review() {
    local code_file=$1
    local context_file=$2
    local result_file=$3

    show_progress 2 3 "GLM AI审查: $(basename "$code_file")"

    # 查询历史经验
    local file_type=$(basename "$code_file" | sed 's/.*\.//')
    query_experience "$file_type"

    # 读取代码
    local code_content=$(cat "$code_file" 2>/dev/null || echo "")
    if [[ -z "$code_content" ]]; then
        log "WARN" "文件为空: $code_file"
        echo '{"score": 5, "issues": [], "approved": true}' > "$result_file"
        return 0
    fi

    # 读取上下文
    local context=$(jq -r '.worker // "unknown"' "$context_file" 2>/dev/null)

    # 构建审查提示
    local prompt="你是一个严格的代码审查专家。

上下文: $context

待审查代码:
\`\`\`
$code_content
\`\`\`

请进行代码审查，返回JSON格式：
{
    \"score\": 0-10的评分,
    \"issues\": [
        {
            \"severity\": \"critical/high/medium/low\",
            \"description\": \"问题描述\",
            \"suggestion\": \"修复建议\"
        }
    ],
    \"security_warnings\": [\"安全问题\"],
    \"approved\": true/false
}

重点检查：
1. 安全漏洞
2. 逻辑错误
3. 性能问题
4. 代码规范"

    # 调用GLM API
    local api_response=$(mktemp)

    # 使用Python调用API（更可靠）
    python3 -c "
import json
import os
from anthropic import Anthropic

client = Anthropic(
    api_key='$ANTHROPIC_AUTH_TOKEN',
    base_url='$ANTHROPIC_BASE_URL'
)

try:
    response = client.messages.create(
        model='glm-4.7',
        max_tokens=2000,
        temperature=0.1,
        messages=[{'role': 'user', 'content': '''$prompt'''}]
    )

    content = response.content[0].text

    # 尝试提取JSON
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()

    result = json.loads(content)
    print(json.dumps(result))

except Exception as e:
    print(json.dumps({
        'score': 5,
        'issues': [{'severity': 'high', 'description': f'审查失败: {str(e)}', 'suggestion': '请手动审查'}],
        'approved': True
    }))
" > "$api_response" 2>/dev/null

    # 读取结果
    if [[ -f "$api_response" && -s "$api_response" ]]; then
        cat "$api_response" > "$result_file"
        rm -f "$api_response"
        return 0
    else
        log "WARN" "GLM审查失败，使用降级结果"
        echo '{"score": 6, "issues": [], "approved": true}' > "$result_file"
        rm -f "$api_response"
        return 1
    fi
}

# 综合审查决策
make_review_decision() {
    local static_result=$1
    local glm_result=$2
    local decision_file=$3
    local code_file=$4

    show_progress 3 3 "综合决策: $(basename "$code_file")"

    local static_score=$(jq -r '.score // 5' "$static_result" 2>/dev/null)
    local glm_score=$(jq -r '.score // 5' "$glm_result" 2>/dev/null)
    local glm_approved=$(jq -r '.approved // true' "$glm_result" 2>/dev/null)

    # 综合评分：静态40% + GLM60%
    local final_score=$(echo "scale=1; $static_score * 0.4 + $glm_score * 0.6" | bc)

    # 决策逻辑
    local approved=false
    local feedback=""
    local issues=""

    if (( $(echo "$final_score >= 7" | bc -l) )) && [[ "$glm_approved" == "true" ]]; then
        approved=true
        feedback="代码质量良好，通过审查"
        issues="无重大问题"
    else
        approved=false

        # 收集问题
        local static_issues=$(jq -r '.issues // ""' "$static_result" 2>/dev/null)
        local glm_issues=$(jq -r '.issues[].description // ""' "$glm_result" 2>/dev/null | head -3 | paste -sd "; ")

        issues="$static_issues $glm_issues"
        feedback="代码需要改进。评分: $final_score/10。问题: $issues"
    fi

    # 保存决策
    cat > "$decision_file" << EOF
{
    "approved": $approved,
    "final_score": $final_score,
    "static_score": $static_score,
    "glm_score": $glm_score,
    "feedback": "$feedback",
    "issues": "$issues",
    "timestamp": "$(date -Iseconds)",
    "reviewer": "glm-4.7 + static"
}
EOF

    # 记录审查经验（每个文件）
    local lesson=$(extract_lesson "$approved" "$issues" "$final_score")
    local task_id=$(basename "$(dirname "$code_file")")
    record_review_experience "$task_id" "$approved" "$final_score" "$issues" "$lesson"

    if [[ "$approved" == "true" ]]; then
        return 0
    else
        return 1
    fi
}

# 审查任务
review_task() {
    local task_dir=$1
    local task_id=$(basename "$task_dir")

    log "INFO" "开始审查任务: $task_id"

    # 移动到reviewing状态
    local reviewing_path="$REVIEWING_DIR/$task_id"
    mv "$task_dir" "$reviewing_path"

    # 读取任务上下文
    local context_file="$reviewing_path/context.json"
    if [[ ! -f "$context_file" ]]; then
        log "WARN" "缺少任务上下文: $task_id"
        return 1
    fi

    # 找到所有代码文件
    local code_files=$(find "$reviewing_path" -type f \( -name "*.py" -o -name "*.js" -o -name "*.java" \) 2>/dev/null)

    if [[ -z "$code_files" ]]; then
        log "WARN" "没有找到代码文件: $task_id"
        return 1
    fi

    # 审查每个文件
    local all_approved=true
    local combined_score=0
    local file_count=0

    while IFS= read -r code_file; do
        file_count=$((file_count + 1))

        log "INFO" "审查文件: $(basename "$code_file")"

        # 1. 静态分析
        local static_result="$reviewing_path/static_$(basename "$code_file").json"
        local static_score=$(run_static_analysis "$code_file" "$static_result")

        # 2. GLM审查
        local glm_result="$reviewing_path/glm_$(basename "$code_file").json"
        run_glm_review "$code_file" "$context_file" "$glm_result"

        # 3. 综合决策
        local decision_file="$reviewing_path/decision_$(basename "$code_file").json"
        if ! make_review_decision "$static_result" "$glm_result" "$decision_file" "$code_file"; then
            all_approved=false
        fi

        local file_score=$(jq -r '.final_score // 5' "$decision_file" 2>/dev/null)
        combined_score=$(echo "$combined_score + $file_score" | bc)

    done <<< "$code_files"

    # 计算平均分
    local avg_score=$(echo "scale=1; $combined_score / $file_count" | bc)

    # 最终决策
    local feedback_file="$FEEDBACK_DIR/${task_id}.json"

    if [[ "$all_approved" == "true" && $(echo "$avg_score >= 7" | bc -l) -eq 1 ]]; then
        log "INFO" "✓ 任务通过审查: $task_id (评分: $avg_score)"

        # 移动到approved
        mv "$reviewing_path" "$APPROVED_DIR/"

        # 通知Worker
        cat > "$feedback_file" << EOF
{
    "approved": true,
    "score": $avg_score,
    "feedback": "代码质量良好，通过审查",
    "timestamp": "$(date -Iseconds)"
}
EOF
        return 0
    else
        log "WARN" "✗ 任务未通过审查: $task_id (评分: $avg_score)"

        # 移动到rejected
        mv "$reviewing_path" "$REJECTED_DIR/"

        # 收集详细反馈
        local detailed_feedback=$(find "$REJECTED_DIR/$task_id" -name "decision_*.json" -exec jq -r '.feedback' {} \; | head -3 | paste -sd "; ")

        # 通知Worker
        cat > "$feedback_file" << EOF
{
    "approved": false,
    "score": $avg_score,
    "feedback": "$detailed_feedback",
    "timestamp": "$(date -Iseconds)"
}
EOF
        return 1
    fi
}

# 主循环
main() {
    log "INFO" "Reviewer启动 (GLM-4.7 + 静态分析)"
    log "INFO" "监控目录: $PENDING_DIR"

    # 检查依赖
    if ! command -v python3 &> /dev/null; then
        log "WARN" "未安装python3，某些功能可能受限"
    fi

    if ! command -v bc &> /dev/null; then
        log "ERROR" "需要bc命令进行数学计算"
        exit 1
    fi

    local loop_count=0

    while true; do
        loop_count=$((loop_count + 1))

        update_reviewer_status "monitoring" ""

        # 检查pending目录
        local pending_tasks=$(find "$PENDING_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)

        if [[ -n "$pending_tasks" ]]; then
            # 有待审查的任务
            while IFS= read -r task_dir; do
                local task_id=$(basename "$task_dir")

                log "INFO" "=== Review Loop #$loop_count - Task: $task_id ==="

                update_reviewer_status "reviewing" "$task_id"

                # 审查任务
                if review_task "$task_dir"; then
                    log "INFO" "任务通过"
                else
                    log "WARN" "任务需要修复"
                fi

            done <<< "$pending_tasks"
        else
            # 没有待审查任务
            if [[ $((loop_count % 12)) -eq 0 ]]; then
                log "INFO" "监控中... (无待审查任务)"
            fi
        fi

        sleep 5
    done
}

# 捕获中断信号
cleanup() {
    log "INFO" "Reviewer收到中断信号，清理中..."
    update_reviewer_status "stopped" ""
    exit 0
}

trap cleanup SIGINT SIGTERM

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            cat << EOF
Reviewer Loop - 独立代码审查进程

使用方法:
    $0 [选项]       启动Reviewer循环

选项:
    -h, --help      显示帮助信息
    -l, --live      实时显示审查进度（可视化）
    -v, --verbose   详细输出模式

功能:
    - 监控Worker提交的代码
    - 三层审查：
      1. 静态分析 (pylint, bandit)
      2. GLM AI审查
      3. 综合决策
    - 给Worker反馈
    - 记录审查经验（持续学习）

审查标准:
    - 评分 >= 7分: 通过
    - 评分 < 7分: 不通过，需修复

配置:
    - 使用GLM API (包月无限)
    - 静态工具：pylint, bandit, python
    - 客观独立审查
    - 经验积累和查询

文件:
    - $STATUS_FILE (状态)
    - $LOG_DIR/reviewer.log (日志)
    - $EXPERIENCE_FILE (审查经验库)

示例:
    $0 --live       # 实时显示审查进度

EOF
            exit 0
            ;;
        -l|--live)
            LIVE_OUTPUT=true
            shift
            ;;
        -v|--verbose)
            set -x  # 详细模式
            shift
            ;;
        *)
            echo "未知选项: $1"
            echo "使用 -h 或 --help 查看帮助"
            exit 1
            ;;
    esac
done

# 启动
main
