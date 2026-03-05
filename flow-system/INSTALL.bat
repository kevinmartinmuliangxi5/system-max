@echo off
REM FlowSystem 自动安装脚本（Windows版本）
REM 配置 GLM Coding Plan

echo ============================================
echo   FlowSystem 安装脚本
echo   配置 GLM Coding Plan
echo ============================================
echo.

REM 检查Python
echo [1/5] 检查Python版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python版本: %PYTHON_VERSION%
echo.

REM 安装依赖
echo [2/5] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✓ 依赖安装完成
echo.

REM 创建配置文件
echo [3/5] 配置API密钥...
if not exist .env (
    copy .env.example .env
    echo ✓ 已创建 .env 配置文件
    echo.
    echo ⚠️  请编辑 .env 文件，填入你的API密钥：
    echo.
    echo    ZHIPUAI_API_KEY=你的API密钥
    echo.
    pause
) else (
    echo ✓ .env 文件已存在
)
echo.

REM 运行导入测试
echo [4/5] 运行导入测试...
python test_imports.py
if errorlevel 1 (
    echo ❌ 导入测试失败
    pause
    exit /b 1
)
echo.

REM 运行功能测试
echo [5/5] 运行功能测试...
python test_simple.py
if errorlevel 1 (
    echo ⚠️  功能测试失败，请检查配置
)
echo.

REM 完成
echo ============================================
echo ✅ 安装完成!
echo ============================================
echo.
echo 下一步:
echo   1. 确保已订阅 GLM Coding Plan 套餐
echo   2. 编辑 .env 文件，填入你的API密钥
echo   3. 运行: python run.py
echo.
echo 详细配置指南: GLM_CODING_PLAN_SETUP.md
echo.
pause
