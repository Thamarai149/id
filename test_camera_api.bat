@echo off
echo ========================================
echo Testing Camera API Endpoints
echo ========================================

echo.
echo 1. Testing camera status...
curl -X GET http://localhost:8080/api/camera-status

echo.
echo.
echo 2. Testing camera initialization...
curl -X POST http://localhost:8080/api/start-camera

echo.
echo.
echo 3. Testing camera capture...
curl -X POST http://localhost:8080/api/capture-face

echo.
echo.
echo 4. Testing system health...
curl -X GET http://localhost:8080/health

echo.
echo ========================================
echo Camera API Test Complete
echo ========================================
pause