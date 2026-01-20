@echo off
echo ========================================
echo Face Verification System
echo ========================================

echo.
echo Checking requirements...

REM Check if multi-student ID cards PDF exists
if not exist "cse_students_idcards.pdf" (
    echo ❌ ERROR: cse_students_idcards.pdf not found!
    echo.
    echo Please place the multi-student ID cards PDF as 'cse_students_idcards.pdf' in this directory.
    echo This PDF should contain ID cards of all CSE students from 3 classes.
    echo.
    pause
    exit /b 1
)

echo ✅ cse_students_idcards.pdf found
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

echo Starting Multi-Student Face Matching System...
echo.
echo Instructions:
echo 1. You can either capture from camera OR browse and select a photo from This PC
echo 2. Make sure your camera is connected (if using camera option)
echo 3. The system will search for your face in all CSE student ID cards
echo 4. Only your matching ID card will be extracted and saved as separate PDF
echo 5. Follow the on-screen prompts
echo.

REM Run the application
mvn spring-boot:run

echo.
echo Application finished.
pause