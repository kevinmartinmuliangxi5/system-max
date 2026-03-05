#!/bin/bash
#
# verify_worker_package.sh
#
# Ralph Worker 包完整性验证脚本
# Ralph Worker Package Integrity Verification Script
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

# 统计变量 (Statistics)
total_checks=0
passed_checks=0
failed_checks=0
warnings=0

# 打印函数 (Print functions)
print_header() {
    echo -e "${CYAN}"
    echo "=============================================="
    echo "  Ralph Worker 包完整性验证"
    echo "  Ralph Worker Package Verification"
    echo "=============================================="
    echo -e "${NC}"
}

print_section() {
    echo ""
    echo -e "${BLUE}▶ $1${NC}"
    echo "----------------------------------------------"
}

print_success() {
    echo -e "${GREEN}  ✓ $1${NC}"
    ((passed_checks++))
    ((total_checks++))
}

print_fail() {
    echo -e "${RED}  ✗ $1${NC}"
    ((failed_checks++))
    ((total_checks++))
}

print_warning() {
    echo -e "${YELLOW}  ⚠ $1${NC}"
    ((warnings++))
}

print_info() {
    echo -e "${BLUE}  ℹ $1${NC}"
}

# 检查文件存在 (Check file existence)
check_file() {
    local file="$1"
    local description="$2"

    if [[ -f "$file" ]]; then
        local size=$(wc -c < "$file" 2>/dev/null || echo "0")
        print_success "$description ($size bytes)"
        return 0
    else
        print_fail "$description - 文件不存在"
        return 1
    fi
}

# 检查目录存在 (Check directory existence)
check_dir() {
    local dir="$1"
    local description="$2"

    if [[ -d "$dir" ]]; then
        local count=$(find "$dir" -type f 2>/dev/null | wc -l)
        print_success "$description ($count files)"
        return 0
    else
        print_fail "$description - 目录不存在"
        return 1
    fi
}

# 检查脚本可执行 (Check script executable)
check_executable() {
    local file="$1"
    local description="$2"

    if [[ -x "$file" ]]; then
        print_success "$description 可执行"
        return 0
    else
        print_warning "$description 不可执行"
        return 1
    fi
}

# 检查文件大小 (Check file size)
check_file_size() {
    local file="$1"
    local min_size="$2"
    local description="$3"

    if [[ -f "$file" ]]; then
        local size=$(wc -c < "$file" 2>/dev/null || echo "0")
        if [[ $size -ge $min_size ]]; then
            print_success "$description (size: $size bytes, min: $min_size)"
            return 0
        else
            print_fail "$description - 文件过小 (size: $size, min: $min_size)"
            return 1
        fi
    else
        print_fail "$description - 文件不存在"
        return 1
    fi
}

# 主验证函数 (Main verification)
main() {
    print_header

    # 获取脚本目录 (Get script directory)
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # ========================================
    # 1. 检查 .ralph-worker 目录
    # ========================================
    print_section "1. Worker 目录结构检查"

    check_dir "$SCRIPT_DIR/.ralph-worker" ".ralph-worker 目录"

    if [[ -d "$SCRIPT_DIR/.ralph-worker" ]]; then
        WORKER_DIR="$SCRIPT_DIR/.ralph-worker"

        # 检查核心文件
        echo ""
        print_info "检查核心文件..."
        check_file "$WORKER_DIR/ralph_loop.sh" "ralph_loop.sh (Worker 主脚本)"
        check_file "$WORKER_DIR/install_ralph_worker.sh" "install_ralph_worker.sh (安装脚本)"
        check_file "$WORKER_DIR/verify_install.sh" "verify_install.sh (验证脚本)"

        # 检查 lib 目录
        echo ""
        print_info "检查 lib/ 目录..."
        check_dir "$WORKER_DIR/lib" "lib/ (辅助函数库)"

        if [[ -d "$WORKER_DIR/lib" ]]; then
            # 检查所有必需的库文件
            check_file "$WORKER_DIR/lib/circuit_breaker.sh" "circuit_breaker.sh (熔断器)"
            check_file "$WORKER_DIR/lib/response_analyzer.sh" "response_analyzer.sh (响应分析器)"
            check_file "$WORKER_DIR/lib/date_utils.sh" "date_utils.sh (日期工具)"
            check_file "$WORKER_DIR/lib/timeout_utils.sh" "timeout_utils.sh (超时工具)"
            check_file "$WORKER_DIR/lib/task_sources.sh" "task_sources.sh (任务源)"
            check_file "$WORKER_DIR/lib/enable_core.sh" "enable_core.sh (核心启用)"
            check_file "$WORKER_DIR/lib/wizard_utils.sh" "wizard_utils.sh (向导工具)"
        fi
    fi

    # ========================================
    # 2. 检查核心 Python 模块
    # ========================================
    print_section "2. 核心 Python 模块检查"

    check_file "$SCRIPT_DIR/brain_v3.py" "brain_v3.py (增强版任务规划)"
    check_file "$SCRIPT_DIR/dealer_v3.py" "dealer_v3.py (增强版指令生成)"
    check_file "$SCRIPT_DIR/brain.py" "brain.py (基础版任务规划)"
    check_file "$SCRIPT_DIR/dealer_enhanced.py" "dealer_enhanced.py (增强指令生成)"
    check_file "$SCRIPT_DIR/setup.py" "setup.py (安装脚本)"
    check_file "$SCRIPT_DIR/quickstart.py" "quickstart.py (快速测试)"

    # ========================================
    # 3. 检查 .janus 记忆系统
    # ========================================
    print_section "3. .janus 核心记忆系统检查"

    check_dir "$SCRIPT_DIR/.janus" ".janus/ 目录"
    check_dir "$SCRIPT_DIR/.janus/core" ".janus/core/ (核心模块)"
    check_dir "$SCRIPT_DIR/.janus/knowledge" ".janus/knowledge/ (知识库)"
    check_dir "$SCRIPT_DIR/.janus/ui_library" ".janus/ui_library/ (UI库)"

    if [[ -d "$SCRIPT_DIR/.janus/core" ]]; then
        echo ""
        print_info "检查核心模块..."
        check_file "$SCRIPT_DIR/.janus/core/hippocampus.py" "hippocampus.py (海马体)"
        check_file "$SCRIPT_DIR/.janus/core/router.py" "router.py (路由器)"
        check_file "$SCRIPT_DIR/.janus/core/thinkbank.py" "thinkbank.py (思考库)"
        check_file "$SCRIPT_DIR/.janus/core/validator.py" "validator.py (验证器)"
        check_file "$SCRIPT_DIR/.janus/core/cache_manager.py" "cache_manager.py (缓存管理)"
    fi

    # ========================================
    # 4. 检查 .ralph 工具层
    # ========================================
    print_section "4. .ralph 工具集成层检查"

    check_dir "$SCRIPT_DIR/.ralph" ".ralph/ 目录"
    check_dir "$SCRIPT_DIR/.ralph/tools" ".ralph/tools/ (工具集成)"
    check_dir "$SCRIPT_DIR/.ralph/context" ".ralph/context/ (Context Engineering)"
    check_dir "$SCRIPT_DIR/.ralph/diagrams" ".ralph/diagrams/ (流程图)"
    check_dir "$SCRIPT_DIR/.ralph/specs" ".ralph/specs/ (规格文档)"
    check_dir "$SCRIPT_DIR/.ralph/memories" ".ralph/memories/ (记忆存储)"
    check_dir "$SCRIPT_DIR/.ralph/scripts" ".ralph/scripts/ (脚本)"

    if [[ -d "$SCRIPT_DIR/.ralph/tools" ]]; then
        echo ""
        print_info "检查工具文件..."
        check_file "$SCRIPT_DIR/.ralph/tools/tools_manager.py" "tools_manager.py (工具管理器)"
        check_file "$SCRIPT_DIR/.ralph/tools/memory_integrator.py" "memory_integrator.py (记忆集成)"
        check_file "$SCRIPT_DIR/.ralph/tools/claude_mem_enhanced.py" "claude_mem_enhanced.py (记忆增强)"
        check_file "$SCRIPT_DIR/.ralph/tools/parallel_executor.py" "parallel_executor.py (并行执行)"
        check_file "$SCRIPT_DIR/.ralph/tools/session_hooks.py" "session_hooks.py (会话钩子)"
        check_file "$SCRIPT_DIR/.ralph/tools/config.json" "config.json (工具配置)"
    fi

    # ========================================
    # 5. 检查文档完整性
    # ========================================
    print_section "5. 文档完整性检查"

    check_file "$SCRIPT_DIR/README.md" "README.md (系统概述)"
    check_file "$SCRIPT_DIR/README_V3.md" "README_V3.md (v3版本说明)"
    check_file "$SCRIPT_DIR/DEPLOYMENT.md" "DEPLOYMENT.md (部署指南)"
    check_file "$SCRIPT_DIR/WORKER.md" "WORKER.md (Worker指南)"
    check_file "$SCRIPT_DIR/INSTALL.md" "INSTALL.md (安装说明)"
    check_file "$SCRIPT_DIR/QUICK_START_V3.md" "QUICK_START_V3.md (快速入门)"
    check_file "$SCRIPT_DIR/INTEGRATION_COMPLETE_SUMMARY.md" "INTEGRATION_COMPLETE_SUMMARY.md (集成总结)"
    check_file "$SCRIPT_DIR/PACKAGE_MANIFEST.md" "PACKAGE_MANIFEST.md (打包清单)"

    if [[ -d "$SCRIPT_DIR/.ralph/context" ]]; then
        echo ""
        print_info "检查 Context Engineering 文档..."
        check_file "$SCRIPT_DIR/.ralph/context/project-info.md" "project-info.md"
        check_file "$SCRIPT_DIR/.ralph/context/architecture.md" "architecture.md"
        check_file "$SCRIPT_DIR/.ralph/context/coding-style.md" "coding-style.md"
        check_file "$SCRIPT_DIR/.ralph/context/decisions.md" "decisions.md"
        check_file "$SCRIPT_DIR/.ralph/context/dependencies.md" "dependencies.md"
    fi

    # ========================================
    # 6. 检查配置文件
    # ========================================
    print_section "6. 配置文件检查"

    check_file "$SCRIPT_DIR/requirements.txt" "requirements.txt (Python依赖)"

    if [[ -d "$SCRIPT_DIR/.janus" ]]; then
        check_file "$SCRIPT_DIR/.janus/config.json" ".janus/config.json (Janus配置)" || \
            print_info ".janus/config.json 不存在 (需要首次运行时生成)"
    fi

    if [[ -d "$SCRIPT_DIR/.janus" ]]; then
        check_file "$SCRIPT_DIR/.janus/config.template.json" ".janus/config.template.json (配置模板)"
    fi

    # ========================================
    # 7. 检查文件大小合理性
    # ========================================
    print_section "7. 文件大小合理性检查"

    # ralph_loop.sh 应该较大 (约 60KB+)
    check_file_size "$SCRIPT_DIR/.ralph-worker/ralph_loop.sh" 60000 "ralph_loop.sh 大小"

    # install_ralph_worker.sh 应该合理大小 (约 8KB+)
    check_file_size "$SCRIPT_DIR/.ralph-worker/install_ralph_worker.sh" 8000 "install_ralph_worker.sh 大小"

    # brain_v3.py 应该合理大小 (约 15KB+)
    check_file_size "$SCRIPT_DIR/brain_v3.py" 15000 "brain_v3.py 大小"

    # dealer_v3.py 应该合理大小 (约 20KB+)
    check_file_size "$SCRIPT_DIR/dealer_v3.py" 20000 "dealer_v3.py 大小"

    # ========================================
    # 8. 语法检查
    # ========================================
    print_section "8. Shell 脚本语法检查"

    if command -v bash &> /dev/null; then
        if [[ -f "$SCRIPT_DIR/.ralph-worker/ralph_loop.sh" ]]; then
            if bash -n "$SCRIPT_DIR/.ralph-worker/ralph_loop.sh" 2>/dev/null; then
                print_success "ralph_loop.sh 语法正确"
            else
                print_fail "ralph_loop.sh 语法错误"
            fi
        fi

        if [[ -f "$SCRIPT_DIR/.ralph-worker/install_ralph_worker.sh" ]]; then
            if bash -n "$SCRIPT_DIR/.ralph-worker/install_ralph_worker.sh" 2>/dev/null; then
                print_success "install_ralph_worker.sh 语法正确"
            else
                print_fail "install_ralph_worker.sh 语法错误"
            fi
        fi

        # 检查 lib 中的脚本
        if [[ -d "$SCRIPT_DIR/.ralph-worker/lib" ]]; then
            local lib_errors=0
            for script in "$SCRIPT_DIR/.ralph-worker/lib"/*.sh; do
                if [[ -f "$script" ]]; then
                    if ! bash -n "$script" 2>/dev/null; then
                        ((lib_errors++))
                        print_fail "$(basename "$script") 语法错误"
                    fi
                fi
            done
            if [[ $lib_errors -eq 0 ]]; then
                print_success "所有 lib/ 脚本语法正确"
            fi
        fi
    else
        print_warning "bash 不可用，跳过语法检查"
    fi

    # ========================================
    # 9. Python 导入检查
    # ========================================
    print_section "9. Python 模块导入检查"

    if command -v python &> /dev/null || command -v python3 &> /dev/null; then
        local py_cmd=$(command -v python &> /dev/null && echo "python" || echo "python3")

        # 检查 brain_v3.py
        if [[ -f "$SCRIPT_DIR/brain_v3.py" ]]; then
            if $py_cmd -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); import brain_v3" 2>/dev/null; then
                print_success "brain_v3.py 可导入"
            else
                print_warning "brain_v3.py 导入检查失败 (可能缺少依赖)"
            fi
        fi

        # 检查 dealer_v3.py
        if [[ -f "$SCRIPT_DIR/dealer_v3.py" ]]; then
            if $py_cmd -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); import dealer_v3" 2>/dev/null; then
                print_success "dealer_v3.py 可导入"
            else
                print_warning "dealer_v3.py 导入检查失败 (可能缺少依赖)"
            fi
        fi
    else
        print_warning "Python 不可用，跳过导入检查"
    fi

    # ========================================
    # 10. 安装脚本功能测试
    # ========================================
    print_section "10. 安装脚本功能检查"

    if [[ -f "$SCRIPT_DIR/.ralph-worker/install_ralph_worker.sh" ]]; then
        # 检查脚本是否包含必要函数
        local install_script="$SCRIPT_DIR/.ralph-worker/install_ralph_worker.sh"

        if grep -q "detect_os" "$install_script"; then
            print_success "包含 OS 检测功能"
        else
            print_fail "缺少 OS 检测功能"
        fi

        if grep -q "check_dependencies" "$install_script"; then
            print_success "包含依赖检查功能"
        else
            print_fail "缺少依赖检查功能"
        fi

        if grep -q "backup_existing_files" "$install_script"; then
            print_success "包含备份功能"
        else
            print_fail "缺少备份功能"
        fi

        if grep -q "verify_installation" "$install_script"; then
            print_success "包含验证功能"
        else
            print_fail "缺少验证功能"
        fi
    fi

    # ========================================
    # 11. DEPLOYMENT.md 完整性检查
    # ========================================
    print_section "11. DEPLOYMENT.md Worker 安装指南检查"

    if [[ -f "$SCRIPT_DIR/DEPLOYMENT.md" ]]; then
        local deploy_doc="$SCRIPT_DIR/DEPLOYMENT.md"

        if grep -q ".ralph-worker" "$deploy_doc"; then
            print_success "DEPLOYMENT.md 包含 .ralph-worker 说明"
        else
            print_fail "DEPLOYMENT.md 缺少 .ralph-worker 说明"
        fi

        if grep -q "install_ralph_worker" "$deploy_doc"; then
            print_success "DEPLOYMENT.md 包含安装脚本说明"
        else
            print_fail "DEPLOYMENT.md 缺少安装脚本说明"
        fi

        if grep -q "Brain-Dealer-Worker" "$deploy_doc"; then
            print_success "DEPLOYMENT.md 包含完整工作流说明"
        else
            print_fail "DEPLOYMENT.md 缺少工作流说明"
        fi

        if grep -q "ralph_loop.sh" "$deploy_doc"; then
            print_success "DEPLOYMENT.md 包含 ralph_loop.sh 使用说明"
        else
            print_fail "DEPLOYMENT.md 缺少 ralph_loop.sh 说明"
        fi
    fi

    # ========================================
    # 12. 文件统计
    # ========================================
    print_section "12. 包文件统计"

    local py_count=$(find "$SCRIPT_DIR" -name "*.py" -type f 2>/dev/null | wc -l)
    local sh_count=$(find "$SCRIPT_DIR" -name "*.sh" -type f 2>/dev/null | wc -l)
    local md_count=$(find "$SCRIPT_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
    local json_count=$(find "$SCRIPT_DIR" -name "*.json" -type f 2>/dev/null | wc -l)

    print_info "Python 文件: $py_count"
    print_info "Shell 脚本: $sh_count"
    print_info "Markdown 文档: $md_count"
    print_info "JSON 配置: $json_count"

    local total_size=$(du -sb "$SCRIPT_DIR" 2>/dev/null | awk '{print $1}' || echo "0")
    print_info "总大小: $total_size bytes (~$((total_size / 1024)) KB)"

    # ========================================
    # 生成报告
    # ========================================
    print_section "验证报告"

    echo ""
    echo -e "${CYAN}检查统计:${NC}"
    echo -e "  总检查项: $total_checks"
    echo -e "${GREEN}  通过: $passed_checks${NC}"
    echo -e "${RED}  失败: $failed_checks${NC}"
    echo -e "${YELLOW}  警告: $warnings${NC}"

    local pass_rate=0
    if [[ $total_checks -gt 0 ]]; then
        pass_rate=$((passed_checks * 100 / total_checks))
    fi

    echo ""
    echo -e "  通过率: ${pass_rate}%"

    if [[ $failed_checks -eq 0 ]]; then
        echo ""
        echo -e "${GREEN}==============================================${NC}"
        echo -e "${GREEN}  ✅ 验证通过！Worker 包完整！${NC}"
        echo -e "${GREEN}==============================================${NC}"
        return 0
    else
        echo ""
        echo -e "${RED}==============================================${NC}"
        echo -e "${RED}  ❌ 验证失败，发现 $failed_checks 个问题${NC}"
        echo -e "${RED}==============================================${NC}"
        return 1
    fi
}

# 运行主函数 (Run main)
main "$@"
