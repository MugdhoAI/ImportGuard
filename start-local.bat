@echo off
setlocal
cd /d "%~dp0"

echo Building the frontend...
call npm.cmd --prefix frontend run build
if errorlevel 1 (
  echo Frontend build failed. The server was not started.
  exit /b 1
)

echo Starting ImportGuard at http://127.0.0.1:8000
where py >nul 2>&1
if not errorlevel 1 goto use_py

where python >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Install Python 3.11 or newer and try again.
  exit /b 1
)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
exit /b %errorlevel%

:use_py
py -3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
exit /b %errorlevel%
