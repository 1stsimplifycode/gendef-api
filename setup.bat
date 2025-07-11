@echo off
echo ===============================
echo  Setting up GENDEF Web Monitor
echo ===============================

:: Step 1: Create virtual environment
python -m venv venv

:: Step 2: Activate virtual environment
call venv\Scripts\activate

:: Step 3: Upgrade pip
echo [*] Upgrading pip...
pip install --upgrade pip

:: Step 4: Install dependencies
echo [*] Installing dependencies...
pip install -r requirements.txt

:: Step 5: Start FastAPI server
echo [*] Starting FastAPI logging server...
start cmd /k "call venv\Scripts\activate && uvicorn web_logger:app --reload"

:: Step 6: Start Streamlit monitoring app
echo [*] Starting Streamlit dashboard...
start cmd /k "call venv\Scripts\activate && streamlit run app.py"

:: Keep this window open
echo [*] Both services are now running in separate windows.
pause
