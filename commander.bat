@echo off
chcp 65001 >nul
title Commander System

echo.
echo ==========================================
echo   Commander System v2.3
echo ==========================================
echo.
echo   1. Brain     (Brain Mode)
echo   2. Dealer    (Enhanced)
echo   3. Dealer    (Simple)
echo   4. Check     (System Check)
echo   5. Help      (Help)
echo   0. Exit
echo.

set /p choice=Choose (0-5):

if "%choice%"=="1" python brain.py
if "%choice%"=="2" python dealer_enhanced.py
if "%choice%"=="3" python dealer.py
if "%choice%"=="4" python quick_check.py
if "%choice%"=="5" goto help
if "%choice%"=="0" exit

pause
goto :eof

:help
echo.
echo Commands:
echo   python brain.py           - Brain mode
echo   python dealer_enhanced.py - Enhanced dealer
echo   python dealer.py          - Simple dealer
echo   python quick_check.py     - System check
echo.
pause
