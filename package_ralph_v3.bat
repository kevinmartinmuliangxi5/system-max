@echo off
REM ========================================
REM 双脑Ralph系统 v3.0 打包脚本 (Windows)
REM Dual-Brain Ralph System v3.0 Package Script
REM ========================================
REM
REM 此脚本将系统打包为可分发的部署包
REM This script packages the system for distribution
REM
REM 使用方法 / Usage:
REM   package_ralph_v3.bat
REM
REM ========================================

setlocal enabledelayedexpansion

REM 配置
set "SOURCE_DIR=."
set "PACKAGE_NAME=ralph-v3.0"
set "TARGET_DIR=super system"
set "VERSION=v3.0.0-alpha"

REM 获取日期
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)

echo ========================================
echo 双脑Ralph系统 v3.0 打包工具
echo Dual-Brain Ralph System v3.0 Packager
echo ========================================
echo.

REM ========================================
REM 1. 清理旧文件
REM ========================================
echo [1/7] 清理旧文件...
if exist "%TARGET_DIR%" rmdir /s /q "%TARGET_DIR%"
if exist "%PACKAGE_NAME%.zip" del "%PACKAGE_NAME%.zip"
echo 清理完成
echo.

REM ========================================
REM 2. 创建目录结构
REM ========================================
echo [2/7] 创建目录结构...
mkdir "%TARGET_DIR%" 2>nul
mkdir "%TARGET_DIR%\.janus\core" 2>nul
mkdir "%TARGET_DIR%\.janus\knowledge" 2>nul
mkdir "%TARGET_DIR%\.janus\ui_library" 2>nul
mkdir "%TARGET_DIR%\.ralph\tools" 2>nul
mkdir "%TARGET_DIR%\.ralph\context\modules" 2>nul
mkdir "%TARGET_DIR%\.ralph\diagrams" 2>nul
mkdir "%TARGET_DIR%\.ralph\specs" 2>nul
mkdir "%TARGET_DIR%\.ralph\memories" 2>nul
mkdir "%TARGET_DIR%\.ralph\logs" 2>nul
mkdir "%TARGET_DIR%\.ralph\docs\generated" 2>nul
mkdir "%TARGET_DIR%\.ralph\scripts" 2>nul
echo 目录结构创建完成
echo.

REM ========================================
REM 3. 复制核心Python模块
REM ========================================
echo [3/7] 复制核心Python模块...
copy /y brain_v3.py "%TARGET_DIR%\" >nul 2>&1
copy /y brain.py "%TARGET_DIR%\" >nul 2>&1
copy /y dealer_v3.py "%TARGET_DIR%\" >nul 2>&1
copy /y dealer_enhanced.py "%TARGET_DIR%\" >nul 2>&1
copy /y setup.py "%TARGET_DIR%\" >nul 2>&1
copy /y quickstart.py "%TARGET_DIR%\" >nul 2>&1
copy /y quick_test.sh "%TARGET_DIR%\" >nul 2>&1
echo 核心模块复制完成
echo.

REM ========================================
REM 4. 复制.janus目录
REM ========================================
echo [4/7] 复制.janus核心记忆系统...
xcopy /e /i /y ".janus\core" "%TARGET_DIR%\.janus\core" >nul 2>&1
xcopy /e /i /y ".janus\knowledge" "%TARGET_DIR%\.janus\knowledge" >nul 2>&1
xcopy /e /i /y ".janus\ui_library" "%TARGET_DIR%\.janus\ui_library" >nul 2>&1
copy /y ".janus\config.json" "%TARGET_DIR%\.janus\" >nul 2>&1
copy /y ".janus\ui_templates.py" "%TARGET_DIR%\.janus\" >nul 2>&1
echo .janus目录复制完成
echo.

REM ========================================
REM 5. 复制.ralph目录
REM ========================================
echo [5/7] 复制.ralph工具集成层...
xcopy /e /i /y ".ralph\tools" "%TARGET_DIR%\.ralph\tools" >nul 2>&1
xcopy /e /i /y ".ralph\context" "%TARGET_DIR%\.ralph\context" >nul 2>&1
copy /y ".ralph\*.md" "%TARGET_DIR%\.ralph\" >nul 2>&1
if exist ".ralph\docs\tools-integration-analysis.md" copy /y ".ralph\docs\tools-integration-analysis.md" "%TARGET_DIR%\.ralph\docs\" >nul 2>&1
echo .ralph目录复制完成
echo.

REM ========================================
REM 6. 复制文档
REM ========================================
echo [6/7] 复制文档文件...
copy /y README_V3.md "%TARGET_DIR%\" >nul 2>&1
copy /y QUICK_START_V3.md "%TARGET_DIR%\" >nul 2>&1
copy /y DEPLOYMENT.md "%TARGET_DIR%\" >nul 2>&1
copy /y INTEGRATION_COMPLETE_SUMMARY.md "%TARGET_DIR%\" >nul 2>&1
if exist README.md copy /y README.md "%TARGET_DIR%\" >nul 2>&1

REM 创建requirements.txt
echo # 双脑Ralph系统 v3.0 完整版依赖 > "%TARGET_DIR%\requirements.txt"
echo # Dual-Brain Ralph System v3.0 Complete Dependencies >> "%TARGET_DIR%\requirements.txt"
echo # 最后更新: %mydate% >> "%TARGET_DIR%\requirements.txt"
echo. >> "%TARGET_DIR%\requirements.txt"
echo # ==================== >> "%TARGET_DIR%\requirements.txt"
echo # 核心依赖 / Core Dependencies >> "%TARGET_DIR%\requirements.txt"
echo # ==================== >> "%TARGET_DIR%\requirements.txt"
echo. >> "%TARGET_DIR%\requirements.txt"
echo # 中文分词 / Chinese Word Segmentation >> "%TARGET_DIR%\requirements.txt"
echo jieba>=0.42.1 >> "%TARGET_DIR%\requirements.txt"
echo. >> "%TARGET_DIR%\requirements.txt"
echo # Claude API / Anthropic SDK >> "%TARGET_DIR%\requirements.txt"
echo anthropic>=0.18.0 >> "%TARGET_DIR%\requirements.txt"
echo. >> "%TARGET_DIR%\requirements.txt"
echo # 剪贴板操作 / Clipboard Operations >> "%TARGET_DIR%\requirements.txt"
echo pyperclip>=1.8.2 >> "%TARGET_DIR%\requirements.txt"
echo. >> "%TARGET_DIR%\requirements.txt"
echo # 颜色输出 / Terminal Colors >> "%TARGET_DIR%\requirements.txt"
echo colorama>=0.4.6 >> "%TARGET_DIR%\requirements.txt"
echo. >> "%TARGET_DIR%\requirements.txt"
echo # HTTP请求 / HTTP Requests >> "%TARGET_DIR%\requirements.txt"
echo requests>=2.31.0 >> "%TARGET_DIR%\requirements.txt"

echo 文档文件复制完成
echo.

REM ========================================
REM 7. 清理缓存文件
REM ========================================
echo [7/7] 清理缓存文件...
for /d /r "%TARGET_DIR%" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo 缓存清理完成
echo.

REM ========================================
REM 打包完成统计
REM ========================================
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 部署包位置:
echo    %TARGET_DIR%\
echo.
echo 后续步骤:
echo    1. cd "%TARGET_DIR%"
echo    2. pip install -r requirements.txt
echo    3. python brain_v3.py "测试任务"
echo.
echo 打包成功！
echo.

pause
