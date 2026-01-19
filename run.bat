@echo off
REM ========================================
REM Change ENV_NAME to your conda environment
REM ========================================
set ENV_NAME=myenv

cd /d "%~dp0"
echo ========================================
echo   StockAgent Launcher
echo ========================================
echo.
echo Activating Conda environment: %ENV_NAME%
echo.

REM Activate conda environment
call conda activate %ENV_NAME%
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to activate environment: %ENV_NAME%
    echo.
    echo Please check:
    echo   1. Anaconda/Miniconda is installed
    echo   2. Environment name is correct (edit ENV_NAME at top of script)
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Environment activated
echo Starting application...
echo.
python -m streamlit run app_v2_enhanced.py
pause