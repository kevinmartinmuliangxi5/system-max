@echo off
REM Python文件快速备份脚本
REM 使用方法：双击运行或在命令行执行

echo ========================================
echo     Python文件自动备份工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 执行备份
python "%~dp0backup_py_files.py"

REM 检查执行结果
if errorlevel 1 (
    echo.
    echo [警告] 备份过程中可能出现了一些问题
) else (
    echo.
    echo [成功] 备份完成！
)

echo.
pause
