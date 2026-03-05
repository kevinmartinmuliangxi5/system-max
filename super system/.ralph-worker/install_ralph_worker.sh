#!/bin/bash
#
# install_ralph_worker.sh
#
# Ralph Worker 安装脚本
# Ralph Worker Installation Script
#
# 此脚本将 Ralph Worker 安装到用户的 ~/.ralph/ 目录
# This script installs Ralph Worker to the user's ~/.ralph/ directory
#
# 版本 (Version): 1.0.0
# 最后更新 (Last Updated): 2026-02-11
#

set -e

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
    echo "  Ralph Worker 安装脚本"
    echo "  Ralph Worker Installation Script"
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

# 检测操作系统 (Detect OS)
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        OS="unknown"
    fi
    print_info "检测到操作系统: $OS"
}

# 检查依赖 (Check dependencies)
check_dependencies() {
    print_info "检查依赖..."

    # 检查 bash
    if ! command -v bash &> /dev/null; then
        print_error "未找到 bash。请先安装 bash。"
        exit 1
    fi

    # 检查必要命令
    local required_commands=("mkdir" "cp" "chmod" "grep" "sed")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            print_error "未找到必要命令: $cmd"
            exit 1
        fi
    done

    print_success "依赖检查通过"
}

# 备份现有文件 (Backup existing files)
backup_existing_files() {
    if [[ -d "$RALPH_HOME" ]]; then
        # 检查是否有需要备份的文件
        local files_to_backup=()

        if [[ -f "$RALPH_HOME/ralph_loop.sh" ]]; then
            files_to_backup+=("ralph_loop.sh")
        fi

        if [[ -d "$RALPH_HOME/lib" ]]; then
            files_to_backup+=("lib")
        fi

        if [[ ${#files_to_backup[@]} -gt 0 ]]; then
            local backup_dir="${RALPH_HOME}/backup_$(date +%Y%m%d_%H%M%S)"
            mkdir -p "$backup_dir"

            for file in "${files_to_backup[@]}"; do
                print_info "备份现有文件: $file"
                cp -r "$RALPH_HOME/$file" "$backup_dir/"
            done

            print_success "已备份到: $backup_dir"
        else
            print_info "未找到需要备份的现有文件"
        fi
    fi
}

# 创建目录 (Create directories)
create_directories() {
    print_info "创建目录结构..."

    mkdir -p "$RALPH_HOME"
    mkdir -p "$RALPH_HOME/lib"

    print_success "目录创建完成"
}

# 安装 ralph_loop.sh (Install ralph_loop.sh)
install_ralph_loop() {
    print_info "安装 ralph_loop.sh..."

    if [[ -f "$SCRIPT_DIR/ralph_loop.sh" ]]; then
        cp "$SCRIPT_DIR/ralph_loop.sh" "$RALPH_HOME/"
        chmod +x "$RALPH_HOME/ralph_loop.sh"
        print_success "ralph_loop.sh 安装完成"
    else
        print_error "未找到 ralph_loop.sh 文件"
        exit 1
    fi
}

# 安装 lib 目录 (Install lib directory)
install_lib() {
    print_info "安装 lib 目录..."

    if [[ -d "$SCRIPT_DIR/lib" ]]; then
        # 复制所有 lib 文件
        for file in "$SCRIPT_DIR"/lib/*.sh; do
            if [[ -f "$file" ]]; then
                cp "$file" "$RALPH_HOME/lib/"
                chmod +x "$RALPH_HOME/lib/$(basename "$file")"
            fi
        done
        print_success "lib 目录安装完成"
    else
        print_error "未找到 lib 目录"
        exit 1
    fi
}

# 创建配置文件 (Create configuration)
create_config() {
    print_info "创建配置..."

    # 创建 .ralphrc 配置文件（如果不存在）
    if [[ ! -f "$RALPH_HOME/.ralphrc" ]]; then
        cat > "$RALPH_HOME/.ralphrc" << 'EOF'
# Ralph Worker 配置文件
# Ralph Worker Configuration File

# Worker 模式设置 (Worker mode settings)
RALPH_WORKER_MODE="auto"

# API 设置 (API settings)
RALPH_API_MODEL="sonnet"
RALPH_API_TIMEOUT=300

# 日志设置 (Logging settings)
RALPH_LOG_ENABLED=true
RALPH_LOG_LEVEL="info"

# 任务循环设置 (Task loop settings)
RALPH_LOOP_ENABLED=true
RALPH_LOOP_INTERVAL=5
EOF
        print_success "配置文件创建完成"
    else
        print_info "配置文件已存在，跳过创建"
    fi
}

# 验证安装 (Verify installation)
verify_installation() {
    print_info "验证安装..."

    local errors=0

    # 检查 ralph_loop.sh
    if [[ -f "$RALPH_HOME/ralph_loop.sh" && -x "$RALPH_HOME/ralph_loop.sh" ]]; then
        print_success "ralph_loop.sh 已正确安装"
    else
        print_error "ralph_loop.sh 安装失败"
        ((errors++))
    fi

    # 检查 lib 目录
    if [[ -d "$RALPH_HOME/lib" ]]; then
        local lib_files=(
            "circuit_breaker.sh"
            "date_utils.sh"
            "enable_core.sh"
            "response_analyzer.sh"
            "task_sources.sh"
            "timeout_utils.sh"
            "wizard_utils.sh"
        )

        local missing_files=0
        for file in "${lib_files[@]}"; do
            if [[ -f "$RALPH_HOME/lib/$file" ]]; then
                print_success "  - lib/$file"
            else
                print_error "  - lib/$file 缺失"
                ((missing_files++))
            fi
        done

        if [[ $missing_files -eq 0 ]]; then
            print_success "lib 目录完整"
        else
            print_error "lib 目录缺少 $missing_files 个文件"
            ((errors++))
        fi
    else
        print_error "lib 目录不存在"
        ((errors++))
    fi

    if [[ $errors -eq 0 ]]; then
        print_success "安装验证通过"
        return 0
    else
        print_error "安装验证失败，发现 $errors 个错误"
        return 1
    fi
}

# 打印使用说明 (Print usage instructions)
print_usage() {
    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}  Ralph Worker 安装完成！${NC}"
    echo -e "${GREEN}  Ralph Worker Installation Complete!${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    echo -e "${CYAN}使用方法 (Usage):${NC}"
    echo ""
    echo "  1. 运行 Worker (Run Worker):"
    echo "     bash ~/.ralph/ralph_loop.sh"
    echo ""
    echo "  2. 使用 Dealer v3 生成任务指令:"
    echo "     python dealer_v3.py"
    echo ""
    echo "  3. Worker 会自动读取并执行任务"
    echo "     Worker will automatically read and execute tasks"
    echo ""
    echo -e "${CYAN}目录结构 (Directory Structure):${NC}"
    echo "  ~/.ralph/"
    echo "    ├── ralph_loop.sh    # Worker 主脚本"
    echo "    ├── lib/             # 辅助函数库"
    echo "    │   ├── circuit_breaker.sh"
    echo "    │   ├── date_utils.sh"
    echo "    │   ├── enable_core.sh"
    echo "    │   ├── response_analyzer.sh"
    echo "    │   ├── task_sources.sh"
    echo "    │   ├── timeout_utils.sh"
    echo "    │   └── wizard_utils.sh"
    echo "    └── .ralphrc         # 配置文件"
    echo ""
    echo -e "${CYAN}Brain-Dealer-Worker 工作流:${NC}"
    echo "  Brain (brain_v3.py) → Dealer (dealer_v3.py) → Worker (ralph_loop.sh)"
    echo ""
    echo "  1. Brain: 规划任务和子任务"
    echo "  2. Dealer: 生成详细的执行指令"
    echo "  3. Worker: 自动循环执行任务"
    echo ""
    echo -e "${YELLOW}提示 (Tips):${NC}"
    echo "  - 将 ~/.ralph 添加到 PATH 以便全局访问"
    echo "  - 编辑 ~/.ralph/.ralphrc 自定义配置"
    echo "  - 查看 WORKER.md 了解更多详情"
    echo ""
}

# 主函数 (Main function)
main() {
    print_header

    print_info "开始安装 Ralph Worker..."
    echo ""

    # 检测操作系统
    detect_os
    echo ""

    # 检查依赖
    check_dependencies
    echo ""

    # 备份现有文件
    backup_existing_files
    echo ""

    # 创建目录
    create_directories
    echo ""

    # 安装文件
    install_ralph_loop
    echo ""

    install_lib
    echo ""

    # 创建配置
    create_config
    echo ""

    # 验证安装
    if verify_installation; then
        echo ""
        print_usage
        exit 0
    else
        echo ""
        print_error "安装过程中出现错误"
        exit 1
    fi
}

# 运行主函数 (Run main function)
main "$@"
