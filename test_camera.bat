@echo off
echo ========================================
echo Camera Availability Test
echo ========================================

echo.
echo Testing camera access...
echo.

echo 1. Checking Windows Camera app...
start ms-windows-store://pdp/?productid=9wzdncrfjbbg
timeout /t 3 >nul

echo.
echo 2. Testing with PowerShell...
powershell -Command "Get-PnpDevice -Class Camera | Select-Object FriendlyName, Status"

echo.
echo 3. Checking camera processes...
tasklist | findstr /i "camera"
tasklist | findstr /i "webcam"

echo.
echo ========================================
echo Camera Test Instructions:
echo ========================================
echo 1. Close all camera apps (Skype, Teams, Zoom)
echo 2. Check Windows Camera privacy settings
echo 3. Try Windows Camera app first
echo 4. Then test our Java application
echo.
pause