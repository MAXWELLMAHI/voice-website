@echo off
setlocal
cd /d "%~dp0"
python src\assemble.py
if errorlevel 1 exit /b 1
echo Website rebuilt. Reload your browser to see the changes.
pause
