#!/bin/bash
# Worker Loop - 专注代码生成和执行
# 基于ralph_loop.sh修改，移除Review逻辑

set -e

# ============================================================================
# GLM API 配置
# ============================================================================
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="434698bbe0754202aabea54a1b6d184d.zPhgfbdAFrX46GDg"
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"

# 配置
RALPH_DIR=".ralph"
PROMPT_FILE="$RALPH_DIR/PROMPT.md"
QUEUE_DIR="$RALPH_DIR/queue"
PENDING_DIR="$QUEUE_DIR/pending"
APPROVED_DIR="$QUEUE_DIR/approved"
FEEDBACK_DIR="$RALPH_DIR/feedback"
LOG_DIR="$RALPH_DIR/logs"
STATUS_FILE="$RALPH_DIR/worker_status.json"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 创建目录
mkdir -p "$QUEUE_DIR" "$PENDING_DIR" "$APPROVED_DIR" "$FEEDBACK_DIR" "$LOG_DIR"

log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${GREEN}[$timestamp] [Worker] $message${NC}"
    echo "[$timestamp] [Worker] $message" >> "$LOG_DIR/worker.log"
}

# 更新Worker状态
update_worker_status() {
    local status=$1
    local task_id=$2
    cat > "$STATUS_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "status": "$status",
    "current_task": "$task_id",
    "worker": "glm-4.7"
}
EOF
}

# 执行Claude Code生成代码
execute_worker() {
    local task_id=$1
    local output_dir="$PENDING_DIR/$task_id"

    log "INFO" "开始执行任务: $task_id"
    mkdir -p "$output_dir"

    # 读取任务蓝图
    if [[ ! -f ".janus/project_state.json" ]]; then
        log "ERROR" "未找到任务蓝图"
        return 1
    fi

    # 调用Claude Code (使用GLM)
    log "INFO" "使用GLM-4.7生成代码..."

    # 执行代码生成
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local output_file="$LOG_DIR/worker_${timestamp}.log"

    if claude code < "$PROMPT_FILE" > "$output_file" 2>&1; then
        log "INFO" "代码生成完成"

        # 收集生成的文件
        collect_output_files "$output_dir"

        # 保存任务上下文
        cat > "$output_dir/context.json" << EOF
{
    "task_id": "$task_id",
    "timestamp": "$(date -Iseconds)",
    "worker": "glm-4.7",
    "output_file": "$output_file"
}
EOF

        log "INFO" "任务提交给Review: $output_dir"
        return 0
    else
        log "ERROR" "代码生成失败，查看日志: $output_file"
        return 1
    fi
}

# 收集输出文件
collect_output_files() {
    local output_dir=$1

    # 找到最近修改的文件
    if git status --short 2>/dev/null | grep -E "^\s*M\s+" > /dev/null; then
        log "INFO" "检测到文件变更"

        # 复制修改的文件到输出目录
        git status --short | grep -E "^\s*M\s+" | awk '{print $2}' | while read -r file; do
            local dest="$output_dir/$(basename "$file")"
            cp "$file" "$dest" 2>/dev/null || true
            log "INFO" "  收集文件: $file"
        done
    fi
}

# 等待Review反馈
wait_for_review() {
    local task_id=$1
    local feedback_file="$FEEDBACK_DIR/${task_id}.json"
    local max_wait=300  # 最多等待5分钟
    local waited=0

    log "INFO" "等待Review反馈..."

    while [[ $waited -lt $max_wait ]]; do
        if [[ -f "$feedback_file" ]]; then
            local approved=$(jq -r '.approved' "$feedback_file" 2>/dev/null)

            if [[ "$approved" == "true" ]]; then
                log "INFO" "✓ Review通过！"

                # 清理反馈文件
                rm -f "$feedback_file"
                return 0
            else
                log "WARN" "✗ Review不通过，需要修复"

                # 读取反馈意见
                local feedback=$(jq -r '.feedback' "$feedback_file" 2>/dev/null)
                log "INFO" "反馈: $feedback"

                # 清理反馈文件
                rm -f "$feedback_file"
                return 1
            fi
        fi

        sleep 5
        waited=$((waited + 5))
    done

    log "WARN" "等待Review超时"
    return 2
}

# 主循环
main() {
    log "INFO" "Worker启动 (使用GLM-4.7)"

    local loop_count=0

    while true; do
        loop_count=$((loop_count + 1))
        log "INFO" "=== Worker Loop #$loop_count ==="

        update_worker_status "ready" ""

        # 检查是否有新任务
        if [[ ! -f ".janus/project_state.json" ]]; then
            log "INFO" "等待Brain生成任务蓝图..."
            sleep 10
            continue
        fi

        # 生成任务ID
        local task_id="task_$(date +%s)"

        update_worker_status "working" "$task_id"

        # 执行任务
        if execute_worker "$task_id"; then
            update_worker_status "waiting_review" "$task_id"

            # 等待Review反馈
            if wait_for_review "$task_id"; then
                log "INFO" "任务完成！"

                # 移动到approved目录
                if [[ -d "$PENDING_DIR/$task_id" ]]; then
                    mv "$PENDING_DIR/$task_id" "$APPROVED_DIR/"
                fi

                # 清理蓝图（任务完成）
                rm -f ".janus/project_state.json"

                log "INFO" "等待下一个任务..."
                sleep 10
            else
                log "WARN" "需要修复，重新生成代码..."

                # 清理pending目录
                rm -rf "$PENDING_DIR/$task_id"

                # 短暂延迟后重试
                sleep 5
            fi
        else
            log "ERROR" "任务执行失败"
            update_worker_status "error" "$task_id"
            sleep 30
        fi
    done
}

# 捕获中断信号
cleanup() {
    log "INFO" "Worker收到中断信号，清理中..."
    update_worker_status "stopped" ""
    exit 0
}

trap cleanup SIGINT SIGTERM

# 检查帮助
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    cat << EOF
Worker Loop - 代码生成和执行

使用方法:
    $0              启动Worker循环

功能:
    - 读取Brain生成的任务蓝图
    - 使用GLM-4.7生成代码
    - 将代码提交给Review审查
    - 根据Review反馈修复或完成

配置:
    - 使用GLM API (包月无限)
    - 专注代码生成，不做审查
    - 通过文件队列与Review通信

状态文件:
    - $STATUS_FILE
    - $LOG_DIR/worker.log

EOF
    exit 0
fi

# 启动
main
