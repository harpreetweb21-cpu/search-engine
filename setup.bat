@echo off
echo ========================================
echo Search Engine - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Create virtual environment
echo Creating Python virtual environment...
cd /d "%~dp0"
if not exist "venv" (
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r python_server\requirements.txt

echo.
echo [OK] Python setup complete
echo.

REM Create data directory
if not exist "data" mkdir data

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the search engine:
echo   1. Run: start.bat
echo   2. Open: http://localhost:5000
echo.
echo Optional: Build C++ engine for better performance
echo   See README.md for C++ build instructions
echo.
pause
