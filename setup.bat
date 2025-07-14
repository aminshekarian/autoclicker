@echo off
echo ================================
echo   AutoClicker Quick Setup
echo ================================

echo Step 1: Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Installing Python...
    echo Please wait...
    
    REM دانلود Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
    
    REM نصب Python با تنظیمات خودکار
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    REM منتظر تکمیل نصب
    timeout /t 30 /nobreak
    
    REM حذف installer
    del python-installer.exe
    
    echo Python installed successfully!
) else (
    echo Python is already installed!
)

echo Step 2: Running AutoClicker...
python autoclicker.py

echo.
echo AutoClicker finished!
pause
