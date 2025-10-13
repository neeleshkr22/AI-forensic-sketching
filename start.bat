@echo off
echo ====================================
echo AI Criminal Sketch Matcher - Start
echo ====================================
echo.

REM Start MongoDB (if not already running)
echo Starting MongoDB...
start "MongoDB" mongod --dbpath ./data/db

REM Wait for MongoDB
timeout /t 3 /nobreak >nul

REM Start Backend
echo Starting Backend Server...
start "Backend" cmd /k "cd backend && venv\Scripts\activate && python app.py"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start Frontend
echo Starting Frontend Server...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo Application Started!
echo ====================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:5173
echo.
echo Press any key to stop all servers...
pause >nul

REM Stop servers (close windows)
taskkill /FI "WindowTitle eq Backend*" /T /F
taskkill /FI "WindowTitle eq Frontend*" /T /F
taskkill /FI "WindowTitle eq MongoDB*" /T /F
