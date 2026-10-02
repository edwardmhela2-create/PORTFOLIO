@echo off
title P11 OFISI 360 (Django #2)
cd /d "%~dp0"
if not exist db.sqlite3 (
  echo Inatengeneza database...
  python manage.py migrate --noinput
  python manage.py anza
)
echo Mfumo uko: http://127.0.0.1:8000
python manage.py runserver
