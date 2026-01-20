@echo off
echo ========================================
echo Java Face Verification System - Manual Compilation
echo ========================================

echo.
echo Step 1: Creating directories...
if not exist target mkdir target
if not exist target\classes mkdir target\classes
if not exist uploads mkdir uploads
if not exist camera mkdir camera

echo.
echo Step 2: Downloading dependencies manually...
echo Note: This project requires Maven for dependency management.
echo Please install Maven from: https://maven.apache.org/download.cgi

echo.
echo Step 3: Alternative - Using Spring Boot CLI (if available)...
spring --version
if %errorlevel% neq 0 (
    echo Spring Boot CLI not found.
)

echo.
echo ========================================
echo MAVEN INSTALLATION REQUIRED
echo ========================================
echo.
echo This Java project uses Maven for dependency management.
echo Please install Maven to build and run the project:
echo.
echo 1. Download Maven from: https://maven.apache.org/download.cgi
echo 2. Extract to a folder (e.g., C:\apache-maven-3.9.6)
echo 3. Add Maven bin directory to your PATH environment variable
echo 4. Restart command prompt and run: mvn --version
echo 5. Then run: build_and_run.bat
echo.
echo Alternative: Use an IDE like IntelliJ IDEA or Eclipse that includes Maven
echo.
pause