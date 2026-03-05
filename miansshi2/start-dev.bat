@echo off
echo Starting Gongkao AI Interviewer...
echo.

:: Start backend
echo [1/2] Starting backend server on port 8000...
start "Backend" cmd /c "cd /d %~dp0backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

:: Wait for backend to start
timeout /t 3 /nobreak > nul

:: Start frontend
echo [2/2] Starting frontend server on port 5173...
start "Frontend" cmd /c "cd /d %~dp0frontend && npm run dev"

echo.
echo ============================================
echo  Servers started!
echo  Frontend: http://localhost:5173
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo ============================================
echo.
echo Press any key to open the app in browser...
pause > nul
start http://localhost:5173
