"""
Quick Installation Script for Face Verification System
Handles Python 3.14 compatibility and installation issues

Usage: python quick_install.py
"""

import subprocess
import sys
import os

def print_step(step, description):
    print(f"\n{'='*50}")
    print(f"Step {step}: {description}")
    print('='*50)

def install_package(package_name, alternative_name=None):
    """Install a package with error handling"""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        if alternative_name:
            try:
                print(f"Trying alternative: {alternative_name}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", alternative_name])
                print(f"✅ {alternative_name} installed successfully")
                return True
            except subprocess.CalledProcessError:
                print(f"❌ Alternative {alternative_name} also failed")
        return False

def main():
    print("🚀 Quick Installation for Face Verification System")
    print("This script will install packages one by one to handle compatibility issues")
    
    # Check Python version
    print_step(1, "Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Install packages one by one
    packages = [
        ("Flask==2.3.3", None),
        ("numpy==1.24.3", "numpy"),
        ("Pillow==10.0.1", "Pillow"),
        ("opencv-python==4.8.1.78", "opencv-python"),
        ("pdfplumber==0.10.0", None),
        ("Werkzeug==2.3.7", None),
        ("python-multipart==0.0.6", None)
    ]
    
    print_step(2, "Installing Core Packages")
    
    failed_packages = []
    
    for package, alternative in packages:
        if not install_package(package, alternative):
            failed_packages.append(package)
    
    # Try to install face_recognition (this might fail)
    print_step(3, "Installing Face Recognition (This may take time)")
    print("⏳ Installing face_recognition - this may take 5-10 minutes...")
    print("💡 If this fails, you can still run the system without face recognition")
    
    face_recognition_installed = install_package("face_recognition==1.3.0", "face_recognition")
    
    if not face_recognition_installed:
        print("\n⚠️  Face recognition failed to install")
        print("This is likely due to:")
        print("1. Missing Visual Studio Build Tools (Windows)")
        print("2. Python 3.14 compatibility issues")
        print("3. Missing system dependencies")
        print("\n💡 Solutions:")
        print("1. Install Visual Studio Build Tools from:")
        print("   https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        print("2. Use Python 3.9-3.11 instead of 3.14")
        print("3. Try: pip install cmake dlib face_recognition")
    
    # Test imports
    print_step(4, "Testing Package Imports")
    
    test_packages = [
        ("flask", "Flask"),
        ("cv2", "OpenCV"),
        ("pdfplumber", "PDF Plumber"),
        ("numpy", "NumPy"),
        ("PIL", "Pillow")
    ]
    
    working_packages = []
    
    for package, name in test_packages:
        try:
            __import__(package)
            print(f"✅ {name} - Working")
            working_packages.append(name)
        except ImportError:
            print(f"❌ {name} - Failed")
    
    # Test face_recognition separately
    try:
        import face_recognition
        print("✅ Face Recognition - Working")
        working_packages.append("Face Recognition")
    except ImportError:
        print("❌ Face Recognition - Not available")
    
    # Summary
    print_step(5, "Installation Summary")
    
    print(f"✅ Working packages: {len(working_packages)}")
    for pkg in working_packages:
        print(f"  - {pkg}")
    
    if failed_packages:
        print(f"\n❌ Failed packages: {len(failed_packages)}")
        for pkg in failed_packages:
            print(f"  - {pkg}")
    
    # Check if minimum requirements are met
    essential_packages = ["Flask", "OpenCV", "PDF Plumber", "NumPy", "Pillow"]
    essential_working = [pkg for pkg in essential_packages if pkg in working_packages]
    
    if len(essential_working) >= 4:  # At least 4 out of 5 essential packages
        print("\n🎉 Minimum requirements met! You can run the system.")
        print("\n📋 Next steps:")
        print("1. Run: python app.py")
        print("2. Or run: python run_system.py")
        
        if "Face Recognition" not in working_packages:
            print("\n⚠️  Note: Face recognition is not available")
            print("The system will work but face comparison will be limited")
            print("To fix this, install Visual Studio Build Tools and try again")
        
        return True
    else:
        print("\n❌ Insufficient packages installed")
        print("Please resolve the installation issues above")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 Ready to run the Face Verification System!")
        else:
            print("\n🔧 Please fix the installation issues and try again")
    except KeyboardInterrupt:
        print("\n\n⏹️  Installation cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")