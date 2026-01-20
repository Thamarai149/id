@echo off
echo ========================================
echo Face Verification System - Java Build
echo ========================================

echo.
echo Step 1: Cleaning previous builds...
if exist target rmdir /s /q target
if exist .m2 rmdir /s /q .m2

echo.
echo Step 2: Checking Java installation...
java -version
if %errorlevel% neq 0 (
    echo ❌ Java not found! Please install Java 17 or higher.
    pause
    exit /b 1
)

echo.
echo Step 3: Checking Maven installation...
mvn -version
if %errorlevel% neq 0 (
    echo ❌ Maven not found! Please install Maven 3.6+.
    pause
    exit /b 1
)

echo.
echo Step 4: Creating directories...
if not exist uploads mkdir uploads
if not exist camera mkdir camera

echo.
echo Step 5: Downloading dependencies...
mvn dependency:resolve
if %errorlevel% neq 0 (
    echo ❌ Failed to resolve dependencies!
    pause
    exit /b 1
)

echo.
echo Step 6: Compiling the project...
mvn clean compile
if %errorlevel% neq 0 (
    echo ❌ Compilation failed!
    pause
    exit /b 1
)

echo.
echo ✅ Build successful!

echo.
echo Step 7: Starting the application...
echo ========================================
echo 🚀 Starting Java Face Verification System...
echo 📷 Make sure your camera is connected and working
echo 🌐 Server will be available at: http://localhost:8080
echo 📖 API Documentation available at: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo ========================================

mvn spring-boot:run