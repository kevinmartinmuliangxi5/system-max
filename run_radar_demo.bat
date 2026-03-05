@echo off
echo ============================================
echo Plotly Radar Chart Demo Launcher
echo ============================================
echo.

REM 检查Python环境
python --version
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查依赖
echo [1/3] 检查依赖...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [错误] 未安装Streamlit，正在安装...
    pip install -r requirements.txt
)

echo [2/3] 依赖检查完成
echo.

REM 显示菜单
echo ============================================
echo 请选择要运行的示例:
echo ============================================
echo [1] 完整演示应用 (包含所有功能)
echo [2] 快速参考 (简洁代码示例)
echo [3] 仅运行Streamlit (用于自己的代码)
echo [4] 安装/更新依赖
echo [0] 退出
echo.

set /p choice=
set /p choice=

:menu
set /p choice=
set /p choice=

if "%choice%"=="" set /p choice=1

if "%choice%"=="1" (
    echo 启动完整演示应用...
    streamlit run streamlit_radar_chart_demo.py
    goto end
)

if "%choice%"=="2" (
    echo 启动快速参考示例...
    streamlit run streamlit_radar_chart_quick_reference.py
    goto end
)

if "%choice%"=="3" (
    echo.
    echo 请将你的Streamlit代码放在当前目录
    echo 然后运行: streamlit run your_file.py
    echo.
    pause
    goto end
)

if "%choice%"=="4" (
    echo 正在安装/更新依赖...
    pip install -U -r requirements.txt
    echo.
    echo 安装完成！
    goto end
)

if "%choice%"=="0" (
    echo 再见！
    goto end
)

echo 无效选择，请重新运行
pause

:end
