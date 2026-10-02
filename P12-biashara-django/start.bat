@echo off
cd /d "%~dp0"
python manage.py migrate --noinput
python manage.py runserver
pause
