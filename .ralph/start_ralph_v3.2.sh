#!/bin/bash
# Ralph v3.2 启动脚本
# 同时启动Worker和Reviewer两个独立进程

set -e

RALPH_DIR=".ralph"
LOG_DIR="$RALPH_DIR/logs"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}║        🚀 Ralph v3.2 - Worker + Reviewer 双进程架构               ║${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}║        Brain (Claude Pro)  → 规划                                 ║${NC}"
echo -e "${BLUE}║        Worker (GLM)        → 执行                                 ║${NC}"
echo -e "${BLUE}║        Reviewer (GLM)      → 审查                                 ║${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"

# 检查是否在Ralph项目目录
if [[ ! -f "$RALPH_DIR/PROMPT.md" ]]; then
    echo -e "${RED}错误：不在Ralph项目目录${NC}"
    echo ""
    echo "请先创建Ralph项目："
    echo "  ralph-setup my-project"
    echo "  cd my-project"
    echo ""
    exit 1
fi

# 检查依赖
check_dependencies() {
    local missing=()

    if ! command -v bash &> /dev/null; then
        missing+=("bash")
    fi

    if ! command -v jq &> /dev/null; then
        missing+=("jq")
    fi

    if ! command -v bc &> /dev/null; then
        missing+=("bc")
    fi

    if ! command -v claude &> /dev/null; then
        missing+=("claude (Claude Code CLI)")
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}缺少依赖：${missing[*]}${NC}"
        echo ""
        echo "请安装缺少的依赖"
        exit 1
    fi
}

echo ""
echo -e "${BLUE}检查依赖...${NC}"
check_dependencies
echo -e "${GREEN}✓ 依赖检查通过${NC}"

# 检查是否已有实例在运行
if [[ -f "$RALPH_DIR/.worker.pid" ]]; then
    WORKER_PID=$(cat "$RALPH_DIR/.worker.pid")
    if ps -p "$WORKER_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}警告：Worker已在运行 (PID: $WORKER_PID)${NC}"
        echo "是否停止现有实例？(y/n)"
        read -r answer
        if [[ "$answer" == "y" ]]; then
            kill "$WORKER_PID" 2>/dev/null || true
            rm -f "$RALPH_DIR/.worker.pid"
        else
            exit 0
        fi
    fi
fi

if [[ -f "$RALPH_DIR/.reviewer.pid" ]]; then
    REVIEWER_PID=$(cat "$RALPH_DIR/.reviewer.pid")
    if ps -p "$REVIEWER_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}警告：Reviewer已在运行 (PID: $REVIEWER_PID)${NC}"
        echo "是否停止现有实例？(y/n)"
        read -r answer
        if [[ "$answer" == "y" ]]; then
            kill "$REVIEWER_PID" 2>/dev/null || true
            rm -f "$RALPH_DIR/.reviewer.pid"
        else
            exit 0
        fi
    fi
fi

# 创建日志目录
mkdir -p "$LOG_DIR"

echo ""
echo -e "${BLUE}启动模式：${NC}"
echo "  1) 前台模式（推荐）- 使用tmux分屏显示"
echo "  2) 后台模式 - 两个进程后台运行"
echo ""
read -p "选择模式 (1/2，默认1): " mode
mode=${mode:-1}

if [[ "$mode" == "1" ]]; then
    # ============================================================
    # 前台模式：使用tmux分屏
    # ============================================================

    # 检查tmux
    if ! command -v tmux &> /dev/null; then
        echo -e "${YELLOW}tmux未安装，降级为后台模式${NC}"
        mode=2
    else
        echo ""
        echo -e "${BLUE}使用tmux分屏模式启动...${NC}"

        # 创建新的tmux会话
        SESSION_NAME="ralph-v32-$(date +%s)"

        # 创建新会话（第一个窗口给Worker）
        tmux new-session -d -s "$SESSION_NAME" -n "Worker"

        # 在第一个窗口启动Worker
        tmux send-keys -t "$SESSION_NAME:Worker" "bash $RALPH_DIR/worker_loop.sh" C-m

        # 创建第二个窗口给Reviewer
        tmux new-window -t "$SESSION_NAME" -n "Reviewer"
        tmux send-keys -t "$SESSION_NAME:Reviewer" "bash $RALPH_DIR/reviewer_loop.sh --live" C-m

        # 创建第三个窗口给状态监控
        tmux new-window -t "$SESSION_NAME" -n "Status"
        tmux send-keys -t "$SESSION_NAME:Status" "watch -n 5 'jq -s . $RALPH_DIR/worker_status.json $RALPH_DIR/reviewer_status.json 2>/dev/null || echo \"等待启动...\"'" C-m

        # 设置窗口布局（平铺）
        tmux select-layout -t "$SESSION_NAME:0" tiled

        echo ""
        echo -e "${GREEN}✓ Tmux会话创建成功：$SESSION_NAME${NC}"
        echo ""
        echo -e "${BLUE}控制：${NC}"
        echo "  - Ctrl+B, 然后 数字键 (0/1/2) : 切换窗口"
        echo "  - Ctrl+B, 然后 D : 分离会话（后台运行）"
        echo "  - Ctrl+C : 停止当前窗口进程"
        echo ""
        echo -e "${BLUE}重新连接：${NC}"
        echo "  tmux attach -t $SESSION_NAME"
        echo ""
        echo -e "${YELLOW}按Enter连接到会话...${NC}"
        read

        # 连接到会话
        tmux attach -session "$SESSION_NAME"

        exit 0
    fi
fi

if [[ "$mode" == "2" ]]; then
    # ============================================================
    # 后台模式：两个独立后台进程
    # ============================================================

    echo ""
    echo -e "${BLUE}后台模式启动...${NC}"

    # 启动Reviewer（先启动，监控队列）
    echo -e "${BLUE}启动Reviewer...${NC}"
    nohup bash "$RALPH_DIR/reviewer_loop.sh" > "$LOG_DIR/reviewer_console.log" 2>&1 &
    REVIEWER_PID=$!
    echo "$REVIEWER_PID" > "$RALPH_DIR/.reviewer.pid"
    echo -e "${GREEN}✓ Reviewer已启动 (PID: $REVIEWER_PID)${NC}"

    sleep 2

    # 启动Worker
    echo -e "${BLUE}启动Worker...${NC}"
    nohup bash "$RALPH_DIR/worker_loop.sh" > "$LOG_DIR/worker_console.log" 2>&1 &
    WORKER_PID=$!
    echo "$WORKER_PID" > "$RALPH_DIR/.worker.pid"
    echo -e "${GREEN}✓ Worker已启动 (PID: $WORKER_PID)${NC}"

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Ralph v3.2 已成功启动！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}进程信息：${NC}"
    echo "  Worker PID:   $WORKER_PID"
    echo "  Reviewer PID: $REVIEWER_PID"
    echo ""
    echo -e "${BLUE}日志文件：${NC}"
    echo "  Worker:   $LOG_DIR/worker_console.log"
    echo "  Reviewer: $LOG_DIR/reviewer_console.log"
    echo ""
    echo -e "${BLUE}状态文件：${NC}"
    echo "  Worker:   $RALPH_DIR/worker_status.json"
    echo "  Reviewer: $RALPH_DIR/reviewer_status.json"
    echo ""
    echo -e "${BLUE}监控命令：${NC}"
    echo "  # 实时查看Worker输出"
    echo "  tail -f $LOG_DIR/worker_console.log"
    echo ""
    echo "  # 实时查看Reviewer输出"
    echo "  tail -f $LOG_DIR/reviewer_console.log"
    echo ""
    echo "  # 查看状态"
    echo "  jq -s . $RALPH_DIR/worker_status.json $RALPH_DIR/reviewer_status.json"
    echo ""
    echo -e "${BLUE}停止命令：${NC}"
    echo "  # 停止Worker"
    echo "  kill $WORKER_PID"
    echo ""
    echo "  # 停止Reviewer"
    echo "  kill $REVIEWER_PID"
    echo ""
    echo "  # 或使用停止脚本"
    echo "  bash $RALPH_DIR/stop_ralph_v3.2.sh"
    echo ""

    # 等待几秒，确认启动成功
    sleep 3

    # 检查进程是否还在运行
    if ! ps -p "$WORKER_PID" > /dev/null 2>&1; then
        echo -e "${RED}✗ Worker启动失败，查看日志：${NC}"
        echo "  tail -50 $LOG_DIR/worker_console.log"
        exit 1
    fi

    if ! ps -p "$REVIEWER_PID" > /dev/null 2>&1; then
        echo -e "${RED}✗ Reviewer启动失败，查看日志：${NC}"
        echo "  tail -50 $LOG_DIR/reviewer_console.log"
        exit 1
    fi

    echo -e "${GREEN}✓ 所有进程运行正常${NC}"
    echo ""
fi
