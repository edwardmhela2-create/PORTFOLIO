@echo off
title P10 BENKI 360 (Django)
cd /d "%~dp0"
if not exist db.sqlite3 (
  echo Inatengeneza database...
  python manage.py migrate --noinput
  python manage.py anza
)
echo Mfumo uko: http://127.0.0.1:8000  (admin ya: /admin/)
python manage.py runserver
