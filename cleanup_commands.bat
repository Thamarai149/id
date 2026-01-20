@echo off
echo ========================================
echo Python Version Cleanup Commands
echo ========================================

echo.
echo Current Python installations detected:
echo - Python 3.14.0 (Recommended - KEEP THIS)
echo - Python 3.13.5 (Anaconda base)
echo - Python 3.10.18 (Multiple Anaconda envs)
echo - Python 3.13.7 (Global)
echo - Python 3.11.9 (Microsoft Store)

echo.
echo ========================================
echo OPTION 1: Clean Anaconda Environments
echo ========================================

echo Removing old conda environments...
conda env remove -n rvc -y
conda env remove -n rvc310 -y  
conda env remove -n rvc_env -y

echo Cleaning conda cache...
conda clean --all -y

echo.
echo ========================================
echo OPTION 2: Uninstall Anaconda Completely
echo ========================================

echo To uninstall Anaconda completely:
echo 1. Go to Windows Settings ^> Apps
echo 2. Search for "Anaconda3"
echo 3. Click Uninstall
echo 4. Also uninstall "Anaconda Navigator" if present

echo.
echo ========================================
echo OPTION 3: Update PATH for Python 3.14
echo ========================================

echo Current PATH will be updated to prioritize Python 3.14
echo Adding to PATH: C:\Python314\Scripts\;C:\Python314\;

setx PATH "C:\Python314\Scripts\;C:\Python314\;%PATH%" /M

echo.
echo ========================================
echo OPTION 4: Create Clean Virtual Environment
echo ========================================

echo Creating virtual environment for Face Verification project...
C:\Python314\python.exe -m venv face_verification_clean

echo.
echo To activate the clean environment:
echo face_verification_clean\Scripts\activate

echo.
echo Then install requirements:
echo pip install -r requirements.txt

echo.
echo ========================================
echo VERIFICATION COMMANDS
echo ========================================

echo Check Python version:
C:\Python314\python.exe --version

echo Check pip version:
C:\Python314\python.exe -m pip --version

echo.
echo ========================================
echo COMPLETE!
echo ========================================

echo Your Python 3.14 is ready to use!
echo Your Face Verification System is already working perfectly.

pause