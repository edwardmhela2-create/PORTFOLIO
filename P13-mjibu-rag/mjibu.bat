@echo off
cd /d "%~dp0"
echo Mjibu inaanza... fungua http://127.0.0.1:8002
python -m uvicorn mjibu.app:app --host 127.0.0.1 --port 8002
pause
