@echo off
cd /d "%~dp0"
echo ============================
echo AutoClicker Quick Setup
echo ============================

echo Step 1: Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Installing Python...
    echo Please wait...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe' -OutFile 'python_installer.exe'}"
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo Python installed successfully!
) else (
    echo Python is already installed!
)

echo Step 2: Installing required packages...
pip install pyautogui keyboard tkinter --quiet

echo Step 3: Running AutoClicker...
if exist "autoclicker.py" (
    python autoclicker.py
) else (
    echo Error: autoclicker.py not found!
    echo Please make sure autoclicker.py is in the same folder as setup.bat
)

echo.
echo AutoClicker finished!
pause
