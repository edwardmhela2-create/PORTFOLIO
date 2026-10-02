@echo off
title P8 DOCKER - BENKI APP
cd /d "%~dp0"
echo Inajenga image na kuanzisha Benki App kwenye container...
docker compose up -d --build
if errorlevel 1 (
  echo HITILAFU: docker compose imehindikwa - hakikisha Docker Desktop imefunguka
  pause
  exit /b 1
)
echo.
echo IMEANZA! Fungua browser: http://localhost:5000
start "" http://localhost:5000
echo.
echo Amri muhimu:
echo   docker compose logs -f    (soma logs)
echo   docker compose down       (simamisha - data inabaki volume)
pause
