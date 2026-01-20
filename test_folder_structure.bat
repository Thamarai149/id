@echo off
echo ========================================
echo Testing Folder Structure
echo ========================================

echo.
echo Creating test directories...
if not exist idcards mkdir idcards
if not exist uploads mkdir uploads
if not exist camera mkdir camera

echo.
echo Directory structure:
dir /b

echo.
echo ID Cards folder:
dir idcards /b 2>nul || echo (empty)

echo.
echo Uploads folder:
dir uploads /b 2>nul || echo (empty)

echo.
echo Camera folder:
dir camera /b 2>nul || echo (empty)

echo.
echo ✅ Folder structure ready!
echo 📁 idcards/ - For storing original ID card PDFs
echo 📁 uploads/ - For storing extracted images from PDFs
echo 📁 camera/ - For storing captured face images

pause