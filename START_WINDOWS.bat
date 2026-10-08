@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3.11 -m venv .venv
  if errorlevel 1 python -m venv .venv
)
if not exist .venv\Scripts\python.exe goto fail
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto fail
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto fail
start "" http://127.0.0.1:8000/signup/
.venv\Scripts\python.exe manage.py runserver
pause
exit /b
:fail
echo Setup failed. Copy the error and send it for help.
pause
