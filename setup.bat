@echo off
echo ====================================
echo AI Criminal Sketch Matcher - Setup
echo ====================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    exit /b 1
)

REM Check MongoDB
mongod --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] MongoDB is not installed or not running
    echo Please ensure MongoDB is installed and running
)

echo [1/5] Setting up Python backend...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo [2/5] Creating directories...
if not exist uploads mkdir uploads
if not exist uploads\sketches mkdir uploads\sketches
if not exist uploads\records mkdir uploads\records
if not exist uploads\temp mkdir uploads\temp
if not exist uploads\enhanced mkdir uploads\enhanced
if not exist models\saved mkdir models\saved
if not exist logs mkdir logs

echo.
echo [3/5] Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo Please edit backend\.env with your configuration
)

echo.
echo [4/5] Setting up React frontend...
cd ..\frontend
call npm install

echo.
echo [5/5] Creating frontend .env...
if not exist .env (
    echo VITE_API_URL=http://localhost:5000 > .env
)

cd ..

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Configure backend\.env with your settings
echo 2. Ensure MongoDB is running
echo 3. Run start.bat to launch the application
echo.
pause
