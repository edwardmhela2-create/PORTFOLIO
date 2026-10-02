@echo off
title P6 BENKI APP
cd /d "%~dp0"
echo Inafungua Benki App (P6) kwenye http://localhost:5000 ...
start "" cmd /c "timeout /t 2 >nul & start http://localhost:5000"
python app.py
pause
