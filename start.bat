@echo off
echo ========================================
echo Starting Search Engine Server
echo ========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found
    echo Run setup.bat first to create it
)

echo Starting server on http://localhost:5000
echo Press Ctrl+C to stop
echo.

python python_server\app.py
