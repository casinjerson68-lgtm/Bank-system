@echo off
REM Bank Queue Management System - Windows Launcher
REM This script launches the Bank QMS GUI application

echo.
echo ============================================================
echo Bank Queue Management System
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Launching Bank Queue Management System...
echo.

REM Launch the application
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch application
    echo Please check that all required files are present
    pause
    exit /b 1
)
