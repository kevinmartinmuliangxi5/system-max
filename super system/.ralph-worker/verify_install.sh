#!/bin/bash
#
# verify_install.sh - Ralph Worker 安装验证脚本
# Verify the Ralph Worker installation
#
# 此脚本验证 Ralph Worker 的安装是否正确
# This script verifies that Ralph Worker is correctly installed
#

# 颜色定义 (Color definitions)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印函数 (Print functions)
print_header() {
    echo -e "${CYAN}"
    echo "============================================"
    echo "  Ralph Worker 安装验证"
    echo "  Ralph Worker Installation Verification"
    echo "============================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 获取脚本所在目录 (Get script directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 目标目录 (Target directory)
RALPH_HOME="${HOME}/.ralph"

# 验证计数器 (Verification counters)
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# 执行检查 (Perform check)
perform_check() {
    local check_name="$1"
    local check_command="$2"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    echo -n "检查: $check_name ... "

    if eval "$check_command" > /dev/null 2>&1; then
        print_success "通过"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        print_error "失败"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# 主验证流程 (Main verification process)
main() {
    print_header
    echo ""

    print_info "验证 Ralph Worker 安装..."
    echo ""

    # 1. 检查 .ralph-worker 目录
    echo -e "${YELLOW}【部署包验证】${NC}"
    perform_check ".ralph-worker 目录存在" "[ -d '$SCRIPT_DIR' ]"
    perform_check "install_ralph_worker.sh 存在" "[ -f '$SCRIPT_DIR/install_ralph_worker.sh' ]"
    perform_check "ralph_loop.sh 存在" "[ -f '$SCRIPT_DIR/ralph_loop.sh' ]"
    perform_check "lib/ 目录存在" "[ -d '$SCRIPT_DIR/lib' ]"
    echo ""

    # 2. 检查 lib 文件
    echo -e "${YELLOW}【lib 文件验证】${NC}"
    local lib_files=(
        "circuit_breaker.sh"
        "date_utils.sh"
        "enable_core.sh"
        "response_analyzer.sh"
        "task_sources.sh"
        "timeout_utils.sh"
        "wizard_utils.sh"
    )

    for file in "${lib_files[@]}"; do
        perform_check "lib/$file 存在" "[ -f '$SCRIPT_DIR/lib/$file' ]"
    done
    echo ""

    # 3. 检查已安装的 Worker (如果存在)
    echo -e "${YELLOW}【已安装 Worker 验证】${NC}"

    if [ -d "$RALPH_HOME" ]; then
        perform_check "~/.ralph/ 目录存在" "[ -d '$RALPH_HOME' ]"

        if [ -f "$RALPH_HOME/ralph_loop.sh" ]; then
            perform_check "~/.ralph/ralph_loop.sh 已安装" "[ -f '$RALPH_HOME/ralph_loop.sh' ]"
            perform_check "ralph_loop.sh 可执行" "[ -x '$RALPH_HOME/ralph_loop.sh' ]"
        else
            print_info "~/.ralph/ralph_loop.sh 未安装 (正常，如需安装请运行 install_ralph_worker.sh)"
            TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
        fi

        if [ -d "$RALPH_HOME/lib" ]; then
            perform_check "~/.ralph/lib/ 目录存在" "[ -d '$RALPH_HOME/lib' ]"

            local installed_lib_count=0
            for file in "${lib_files[@]}"; do
                if [ -f "$RALPH_HOME/lib/$file" ]; then
                    installed_lib_count=$((installed_lib_count + 1))
                fi
            done

            perform_check "~/.ralph/lib/ 文件完整 ($installed_lib_count/${#lib_files[@]})" "[ $installed_lib_count -eq ${#lib_files[@]} ]"
        else
            print_info "~/.ralph/lib/ 未安装 (正常，如需安装请运行 install_ralph_worker.sh)"
            TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
        fi

        if [ -f "$RALPH_HOME/.ralphrc" ]; then
            perform_check "~/.ralph/.ralphrc 配置存在" "[ -f '$RALPH_HOME/.ralphrc' ]"
        else
            print_info "~/.ralph/.ralphrc 不存在 (会在首次运行时创建)"
            TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
        fi
    else
        print_info "~/.ralph/ 目录不存在 (Worker 尚未安装)"
        TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    fi
    echo ""

    # 4. 检查文档
    echo -e "${YELLOW}【文档验证】${NC}"
    local super_system_dir="$(dirname "$SCRIPT_DIR")"
    perform_check "DEPLOYMENT.md 存在" "[ -f '$super_system_dir/DEPLOYMENT.md' ]"
    perform_check "WORKER.md 存在" "[ -f '$super_system_dir/WORKER.md' ]"
    echo ""

    # 5. 检查脚本语法
    echo -e "${YELLOW}【脚本语法验证】${NC}"
    perform_check "install_ralph_worker.sh 语法正确" "bash -n '$SCRIPT_DIR/install_ralph_worker.sh'"
    perform_check "ralph_loop.sh 语法正确" "bash -n '$SCRIPT_DIR/ralph_loop.sh'"

    for file in "${lib_files[@]}"; do
        perform_check "lib/$file 语法正确" "bash -n '$SCRIPT_DIR/lib/$file'"
    done
    echo ""

    # 打印总结 (Print summary)
    echo -e "${CYAN}============================================${NC}"
    echo -e "${CYAN}验证总结${NC}"
    echo -e "${CYAN}============================================${NC}"
    echo -e "总检查数: $TOTAL_CHECKS"
    echo -e "${GREEN}通过: $PASSED_CHECKS${NC}"
    echo -e "${RED}失败: $FAILED_CHECKS${NC}"
    echo ""

    if [ $FAILED_CHECKS -eq 0 ]; then
        print_success "所有检查通过！Ralph Worker 部署包完整。"
        echo ""
        echo -e "${BLUE}下一步操作:${NC}"
        echo "  1. 安装 Worker: bash $SCRIPT_DIR/install_ralph_worker.sh"
        echo "  2. 查看 WORKER.md 了解详细用法"
        echo "  3. 启动 Worker: bash ~/.ralph/ralph_loop.sh"
        echo ""
        return 0
    else
        print_error "发现 $FAILED_CHECKS 个问题，请检查部署包完整性。"
        return 1
    fi
}

# 运行主函数 (Run main function)
main "$@"
