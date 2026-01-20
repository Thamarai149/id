@echo off
echo ========================================
echo Enable Mock Camera Mode
echo ========================================

echo.
echo This will enable mock camera mode for testing
echo when no physical camera is available.
echo.

echo Adding mock camera property...
echo app.camera.mock=true >> src\main\resources\application.properties

echo.
echo ✅ Mock camera mode enabled!
echo Now restart your application with: mvn spring-boot:run
echo.
pause