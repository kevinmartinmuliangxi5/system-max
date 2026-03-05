@echo off
setlocal
set "CODEX_HOME=D:\AI_Projects\system-max\.codex-home"
if not exist "%CODEX_HOME%" mkdir "%CODEX_HOME%"
codex %*
