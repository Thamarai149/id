@echo off
echo ========================================
echo Java Syntax Verification
echo ========================================

echo.
echo Checking Java syntax for all source files...
echo.

set JAVA_FILES=0
set SYNTAX_ERRORS=0

echo Checking main application...
javac -cp . -d temp_classes src/main/java/com/college/project/FaceVerificationApplication.java 2>nul
if %errorlevel% equ 0 (
    echo ✅ FaceVerificationApplication.java - OK
) else (
    echo ❌ FaceVerificationApplication.java - SYNTAX ERROR
    set /a SYNTAX_ERRORS+=1
)
set /a JAVA_FILES+=1

echo.
echo Checking model classes...
javac -cp . -d temp_classes src/main/java/com/college/project/model/*.java 2>nul
if %errorlevel% equ 0 (
    echo ✅ Model classes - OK
) else (
    echo ❌ Model classes - SYNTAX ERROR
    set /a SYNTAX_ERRORS+=1
)
set /a JAVA_FILES+=1

echo.
echo Checking service classes...
javac -cp . -d temp_classes src/main/java/com/college/project/service/*.java 2>nul
if %errorlevel% equ 0 (
    echo ✅ Service classes - OK
) else (
    echo ❌ Service classes - SYNTAX ERROR
    set /a SYNTAX_ERRORS+=1
)
set /a JAVA_FILES+=1

echo.
echo Checking controller classes...
javac -cp . -d temp_classes src/main/java/com/college/project/controller/*.java 2>nul
if %errorlevel% equ 0 (
    echo ✅ Controller classes - OK
) else (
    echo ❌ Controller classes - SYNTAX ERROR
    set /a SYNTAX_ERRORS+=1
)
set /a JAVA_FILES+=1

echo.
echo Checking configuration classes...
javac -cp . -d temp_classes src/main/java/com/college/project/config/*.java 2>nul
if %errorlevel% equ 0 (
    echo ✅ Configuration classes - OK
) else (
    echo ❌ Configuration classes - SYNTAX ERROR
    set /a SYNTAX_ERRORS+=1
)
set /a JAVA_FILES+=1

echo.
echo Cleaning up temporary files...
if exist temp_classes rmdir /s /q temp_classes

echo.
echo ========================================
echo SYNTAX VERIFICATION RESULTS
echo ========================================
echo Total Java file groups checked: %JAVA_FILES%
echo Syntax errors found: %SYNTAX_ERRORS%

if %SYNTAX_ERRORS% equ 0 (
    echo.
    echo ✅ SUCCESS! All Java files have correct syntax
    echo 🎉 Your Java project is ready for Maven build
    echo.
    echo Next steps:
    echo 1. Install Maven following INSTALL_MAVEN.md
    echo 2. Run: build_and_run.bat
    echo 3. Test: python test_java_api.py
) else (
    echo.
    echo ❌ SYNTAX ERRORS FOUND!
    echo Please fix the syntax errors before proceeding.
)

echo.
pause