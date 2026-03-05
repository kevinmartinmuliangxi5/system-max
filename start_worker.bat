@echo off
chcp 65001 >nul 2>&1
title 👷 WORKER (GLM-5)
color 0A
echo ===========================================
echo 👷 [WorkerTerm] GLM-5 Worker Unit
echo ===========================================

:: 尝试从配置文件加载 API Key（如果环境变量未设置）
if "%ZHIPU_API_KEY%"=="" (
    if exist ".janus\config.json" (
        for /f "tokens=2 delims=:, " %%a in ('findstr "ZHIPU_API_KEY" .janus\config.json') do (
            set ZHIPU_API_KEY=%%~a
        )
    )
)

:: 最终检查
if "%ZHIPU_API_KEY%"=="" (
    color 0C
    echo [ERROR] API Key 未配置！
    echo 请设置环境变量 ZHIPU_API_KEY 或编辑 .janus\config.json
    pause
    exit /b 1
)

:: 简单的连通性检查 (不阻塞，仅提示)
python -c "import requests,os; print('✅ API 连接正常' if requests.get('https://open.bigmodel.cn', timeout=3).status_code < 500 else '⚠️ API 连接可能受限')" 2>nul || echo ⚠️ 连接检查跳过

:: GLM Coding Plan 配置
set ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
set ANTHROPIC_AUTH_TOKEN=%ZHIPU_API_KEY%
set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
set API_TIMEOUT_MS=3000000

:: GLM-5 模型配置 (Max/Pro 套餐支持)
set ANTHROPIC_DEFAULT_OPUS_MODEL=GLM-5
set ANTHROPIC_DEFAULT_SONNET_MODEL=GLM-5
set ANTHROPIC_DEFAULT_HAIKU_MODEL=GLM-4.5-Air

echo ✅ GLM-5 Worker 已就绪
echo    - Opus/Sonnet: GLM-5
echo    - Haiku: GLM-4.5-Air
echo.
:: 启动 Claude Code
call npx @anthropic-ai/claude-code --dangerously-skip-permissions