@echo off
echo ========================================
echo Face Capture and ID Card Processing
echo ========================================

echo.
echo Checking requirements...

REM Check if idcard.pdf exists
if not exist "idcard.pdf" (
    echo ❌ ERROR: idcard.pdf not found!
    echo.
    echo Please place your ID card PDF file as 'idcard.pdf' in this directory.
    echo.
    pause
    exit /b 1
)

echo ✅ idcard.pdf found
echo.

REM Check if Maven is available
mvn --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Maven not found!
    echo Please install Maven and add it to your PATH.
    echo.
    pause
    exit /b 1
)

echo ✅ Maven is available
echo.

echo Starting Face Capture and ID Card Processing System...
echo.
echo Instructions:
echo 1. Make sure your camera is connected and working
echo 2. Close any other camera applications (Skype, Teams, etc.)
echo 3. Follow the on-screen prompts
echo.

REM Run the application
mvn spring-boot:run

echo.
echo Application finished.
pause