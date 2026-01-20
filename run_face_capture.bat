@echo off
echo ========================================
echo Face Verification System
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

echo Starting Face Verification System...
echo.
echo Instructions:
echo 1. You can either capture from camera OR upload a student photo
echo 2. Make sure your camera is connected (if using camera option)
echo 3. For photo upload, place your student photo in this directory
echo 4. Follow the on-screen prompts
echo.

REM Run the application
mvn spring-boot:run

echo.
echo Application finished.
pause