# JobTracker Pro
A Python 3.11+ / Django 5.2 portfolio project, with SQLite for easy local setup.

## Windows: Roman Urdu instructions
1. ZIP ko extract karo. Purane JobTracker folder ke upar paste mat karo: ye naya standalone project hai.
2. Extracted JobTracker_Pro folder kholo aur START_WINDOWS.bat par double click karo.
3. Pehli baar internet chahiye: Django install hoga, database automatic banega.
4. Browser mein http://127.0.0.1:8000/signup/ kholo aur apna account banao.
5. Add application se jobs add karo. Edit se status aur interview date update karo.
6. Terminal band karoge to website ruk jayegi. Dobara START_WINDOWS.bat chalao.

## VS Code / PowerShell alternative
Open this folder in VS Code. Run one command at a time:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```
Then open http://127.0.0.1:8000/signup/.
Admin is optional: stop server with Ctrl+C, run `.\.venv\Scripts\python.exe manage.py createsuperuser`, restart server and visit /admin/.

## Features
- Signup, login, POST logout; Django password hashing and password validators.
- Per-user applications with create, edit, confirmed delete.
- Dashboard counts and proportional status bars.
- Company/role search, status filtering, salary, notes and job links.
- Upcoming interviews, displayed in Pakistan time.
- CSV export with spreadsheet formula injection protection.
- Responsive CSS without external assets or API keys.
- Ownership checks on read, edit, delete and export; CSRF protection.

## Explain it in an interview
Model = database structure. Form = validation. View = request handling and user isolation.
URL = route. Template = rendered HTML. Migration = versioned database change.
Trace: browser POST -> CSRF middleware -> login/ownership check -> form validation -> model save -> redirect -> dashboard.
Practice explaining why user is assigned on the server, why deletion requires POST, and why querysets filter request.user.
Run `python manage.py test` to demonstrate account isolation and CRUD tests.

## Scope and next steps
This is a complete local portfolio foundation, not a hosted service. No CV upload, email reminders or AI features are claimed. Before public deployment configure production hosts, HTTPS, DEBUG=0, secret management, static serving, production database and backups. SQLite data stays on your computer. Add PostgreSQL, pagination and a deployment pipeline as your next learning steps.
