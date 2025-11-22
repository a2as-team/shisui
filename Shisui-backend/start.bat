@echo off
REM Shisui Backend Startup Script
REM This script checks if MySQL is running before starting the app

echo ============================================
echo Shisui Backend Startup
echo ============================================
echo.

REM Check if MySQL is running
echo [1/2] Checking MySQL service...
sc query MySQL | find "RUNNING" >nul
if %errorlevel% equ 0 (
    echo [OK] MySQL is running
) else (
    echo [WARNING] MySQL is not running!
    echo.
    echo Please start MySQL:
    echo   - Open XAMPP/WAMP Control Panel
    echo   - Click "Start" next to MySQL
    echo   - Or run: start.bat
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
)

echo.
echo [2/2] Starting Shisui Backend...
echo.

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python main.py

pause
