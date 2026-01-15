@echo off
cd /d "%~dp0"
REM 使用 conda 环境中的 Python 运行 streamlit
"F:\anaconda\envs\data_work\python.exe" -m streamlit run app_v2_enhanced.py
pause
