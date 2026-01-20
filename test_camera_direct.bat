@echo off
echo ========================================
echo Direct Camera Test (No Windows Camera App)
echo ========================================

echo.
echo 1. Closing Windows Camera app if running...
taskkill /f /im WindowsCamera.exe 2>nul
timeout /t 2 >nul

echo.
echo 2. Testing camera API directly...
echo.

echo Testing camera initialization:
curl -s -X POST http://localhost:8080/api/start-camera | findstr "message"

echo.
echo.
echo Testing camera capture:
curl -s -X POST http://localhost:8080/api/capture-face | findstr "message"

echo.
echo.
echo 3. Check if images were captured:
if exist "camera\*.jpg" (
    echo ✅ Camera images found:
    dir camera\*.jpg /b
) else (
    echo ❌ No camera images found
)

echo.
echo ========================================
echo Direct Camera Test Complete
echo ========================================
echo.
echo Instructions:
echo 1. If camera works, you'll see success messages above
echo 2. Check the camera folder for captured images
echo 3. Use the web interface at http://localhost:8080
echo.
pause