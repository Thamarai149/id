@echo off
echo ========================================
echo Face Verification System - Java
echo College Final Year Project
echo ========================================

echo.
echo Checking Java installation...
java -version
if %errorlevel% neq 0 (
    echo ❌ Java not found! Please install Java 17 or higher.
    pause
    exit /b 1
)

echo.
echo Checking Maven installation...
mvn -version
if %errorlevel% neq 0 (
    echo ❌ Maven not found! Please install Maven 3.6+.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Building the application...
echo ========================================
mvn clean compile
if %errorlevel% neq 0 (
    echo ❌ Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Build successful!

echo.
echo ========================================
echo Starting Face Verification System...
echo ========================================
echo 🚀 Starting Live Face Detection and ID Card Verification System...
echo 📷 Make sure your camera is connected and working
echo 🌐 Server will be available at: http://localhost:8080
echo 📖 API Documentation available at: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

mvn spring-boot:run