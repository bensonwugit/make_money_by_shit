@echo off
REM Make Money by Shit - Setup & Run Script for Windows

echo.
echo Make Money by Shit - Setup Script
echo ==================================
echo.

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is required but not installed.
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo Initializing database...
python init_db.py

REM Done
echo.
echo Setup complete!
echo.
echo To start the application, run:
echo   venv\Scripts\activate.bat
echo   python run.py
echo.
echo Open http://localhost:5000 in your browser
echo.
echo Default credentials:
echo   Username: shit
echo   Password: money
echo.
pause
