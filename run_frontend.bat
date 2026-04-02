@echo off
REM Disease Progression Prediction - Web Frontend Starter
REM This script installs dependencies and runs the Flask web app

echo ========================================
echo Disease Progression Prediction System
echo Web Frontend Starter
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/3] Installing/Updating dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Flask web server...
echo.
echo ============================================
echo Web app is starting at:
echo http://localhost:5000
echo ============================================
echo.
echo Press Ctrl+C to stop the server.
echo.

timeout /t 2

REM Start Flask app
python app.py

pause
