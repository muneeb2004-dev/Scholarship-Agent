@echo off
REM run.bat - Development startup script for Windows

echo.
echo  ======================================
echo  AI Scholarship Finder
echo  ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [*] Installing dependencies...
pip install -q -r requirements.txt

REM Initialize database
echo [*] Initializing database...
python -c "from utils.db_manager import DatabaseManager; db = DatabaseManager(); db.init_db(); print('Database ready!')"

REM Set environment variables
set FLASK_ENV=development
set FLASK_DEBUG=True

REM Run Flask app
echo.
echo [+] Starting Flask app...
echo [+] Visit http://localhost:5000 in your browser
echo.

python flask_app.py

pause
