@echo off
setlocal
cd /d "%~dp0"
echo Open http://127.0.0.1:4173/ in your browser.
echo Press Ctrl+C to stop the preview.
python -m http.server 4173 --bind 127.0.0.1 --directory dist
pause
