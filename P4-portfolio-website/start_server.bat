@echo off
title PORTFOLIO P4 - SERVER
cd /d "%~dp0.."
echo Inaanzisha server ya ndani (localhost:8000)...
start "" cmd /c "timeout /t 1 >nul & start http://localhost:8000/P4-portfolio-website/"
python -m http.server 8000
