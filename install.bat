@echo off
REM Simple installation script for Financial Tools (Windows)

echo 🚀 Installing Financial Tools...
echo ================================

REM Check if Python 3 is available
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python found
    python setup.py
) else (
    python3 --version >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Python 3 found
        python3 setup.py
    ) else (
        echo ❌ Error: Python 3 is required but not found
        echo    Please install Python 3.7 or higher
        pause
        exit /b 1
    )
)

pause 