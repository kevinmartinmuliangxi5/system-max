#!/bin/bash
# Ralph v3.2 停止脚本

set -e

RALPH_DIR=".ralph"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}停止Ralph v3.2...${NC}"

# 停止Worker
if [[ -f "$RALPH_DIR/.worker.pid" ]]; then
    WORKER_PID=$(cat "$RALPH_DIR/.worker.pid")
    if ps -p "$WORKER_PID" > /dev/null 2>&1; then
        echo "停止Worker (PID: $WORKER_PID)..."
        kill "$WORKER_PID" 2>/dev/null || true
        sleep 2
        if ps -p "$WORKER_PID" > /dev/null 2>&1; then
            echo "强制停止Worker..."
            kill -9 "$WORKER_PID" 2>/dev/null || true
        fi
        echo -e "${GREEN}✓ Worker已停止${NC}"
    else
        echo -e "${YELLOW}Worker未运行${NC}"
    fi
    rm -f "$RALPH_DIR/.worker.pid"
else
    echo -e "${YELLOW}未找到Worker PID文件${NC}"
fi

# 停止Reviewer
if [[ -f "$RALPH_DIR/.reviewer.pid" ]]; then
    REVIEWER_PID=$(cat "$RALPH_DIR/.reviewer.pid")
    if ps -p "$REVIEWER_PID" > /dev/null 2>&1; then
        echo "停止Reviewer (PID: $REVIEWER_PID)..."
        kill "$REVIEWER_PID" 2>/dev/null || true
        sleep 2
        if ps -p "$REVIEWER_PID" > /dev/null 2>&1; then
            echo "强制停止Reviewer..."
            kill -9 "$REVIEWER_PID" 2>/dev/null || true
        fi
        echo -e "${GREEN}✓ Reviewer已停止${NC}"
    else
        echo -e "${YELLOW}Reviewer未运行${NC}"
    fi
    rm -f "$RALPH_DIR/.reviewer.pid"
else
    echo -e "${YELLOW}未找到Reviewer PID文件${NC}"
fi

echo ""
echo -e "${GREEN}✓ Ralph v3.2已完全停止${NC}"
