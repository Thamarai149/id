"""
Setup Script for Face Verification System
Automated installation and setup process

Usage: python setup.py
"""

import os
import sys
import subprocess
import platform

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60)

def print_step(step_num, description):
    """Print formatted step"""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)

def check_python_version():
    """Check if Python version is compatible"""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print("Please upgrade your Python installation")
        return False
    
    print("✅ Python version is compatible")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    print_step(2, "Creating Virtual Environment")
    
    venv_name = "face_verification_env"
    
    if os.path.exists(venv_name):
        print(f"✅ Virtual environment '{venv_name}' already exists")
        return True
    
    try:
        print(f"Creating virtual environment: {venv_name}")
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print(f"✅ Virtual environment '{venv_name}' created successfully")
        
        # Print activation instructions
        system = platform.system().lower()
        if system == "windows":
            activate_cmd = f"{venv_name}\\Scripts\\activate"
        else:
            activate_cmd = f"source {venv_name}/bin/activate"
        
        print(f"\n💡 To activate the virtual environment, run:")
        print(f"   {activate_cmd}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print_step(3, "Installing Dependencies")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    try:
        print("Installing packages from requirements.txt...")
        print("⏳ This may take several minutes, especially for face_recognition...")
        
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("\n💡 Try installing manually:")
        print("   pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    print_step(4, "Creating Directories")
    
    directories = ["uploads", "camera"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory already exists: {directory}")
    
    return True

def test_imports():
    """Test if all required packages can be imported"""
    print_step(5, "Testing Package Imports")
    
    packages = [
        ("flask", "Flask"),
        ("cv2", "OpenCV"),
        ("face_recognition", "Face Recognition"),
        ("fitz", "PyMuPDF"),
        ("pdfplumber", "PDF Plumber"),
        ("numpy", "NumPy"),
        ("PIL", "Pillow")
    ]
    
    failed_imports = []
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name} - OK")
        except ImportError:
            print(f"❌ {name} - FAILED")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️  Failed imports: {', '.join(failed_imports)}")
        print("Please check the installation and try again")
        return False
    
    print("\n✅ All packages imported successfully!")
    return True

def check_camera():
    """Check if camera is available"""
    print_step(6, "Checking Camera Access")
    
    try:
        import cv2
        
        # Try to open camera
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("⚠️  Camera not detected or not accessible")
            print("💡 Make sure:")
            print("   - Camera is connected")
            print("   - Camera is not being used by other applications")
            print("   - Camera permissions are granted")
            return False
        
        # Try to read a frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print("⚠️  Camera detected but cannot capture frames")
            return False
        
        print("✅ Camera is working properly")
        return True
        
    except Exception as e:
        print(f"❌ Camera check failed: {e}")
        return False

def print_next_steps():
    """Print instructions for next steps"""
    print_header("Setup Complete!")
    
    print("🎉 Your Face Verification System is ready!")
    print("\n📋 Next Steps:")
    print("1. Run the system:")
    print("   python app.py")
    print("\n2. Or use the interactive runner:")
    print("   python run_system.py")
    print("\n3. Or test the API:")
    print("   python test_api.py")
    
    print("\n📖 Documentation:")
    print("- README.md - Complete documentation")
    print("- API endpoints available at http://localhost:5000")
    
    print("\n🎓 College Project Features:")
    print("✅ Live camera face capture")
    print("✅ PDF ID card processing")
    print("✅ Advanced face recognition")
    print("✅ RESTful API design")
    print("✅ Comprehensive error handling")
    print("✅ Professional documentation")

def main():
    """Main setup function"""
    print_header("Face Verification System Setup")
    print("🎓 College Final Year Project")
    print("🤖 AI/ML Full Stack Implementation")
    
    print("\nThis script will:")
    print("1. Check Python version compatibility")
    print("2. Create virtual environment (optional)")
    print("3. Install required dependencies")
    print("4. Create necessary directories")
    print("5. Test package imports")
    print("6. Check camera access")
    
    proceed = input("\n🤔 Continue with setup? (y/n): ").lower()
    if proceed != 'y':
        print("Setup cancelled.")
        return
    
    # Run setup steps
    steps = [
        ("Python Version Check", check_python_version),
        ("Virtual Environment", create_virtual_environment),
        ("Install Dependencies", install_dependencies),
        ("Create Directories", create_directories),
        ("Test Imports", test_imports),
        ("Camera Check", check_camera)
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            if step_name == "Virtual Environment":
                # Ask user if they want to create virtual environment
                create_venv = input("\n🤔 Create virtual environment? (recommended) (y/n): ").lower()
                if create_venv == 'y':
                    result = step_func()
                else:
                    print("⏭️  Virtual environment creation skipped")
                    result = True
            else:
                result = step_func()
            
            results.append((step_name, result))
            
            if not result and step_name in ["Python Version Check", "Install Dependencies"]:
                print(f"\n❌ Critical step failed: {step_name}")
                print("Cannot continue with setup.")
                return
                
        except Exception as e:
            print(f"❌ {step_name} failed with error: {e}")
            results.append((step_name, False))
    
    # Print summary
    print_header("Setup Summary")
    
    for step_name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} - {step_name}")
    
    successful_steps = sum(1 for _, success in results if success)
    total_steps = len(results)
    
    print(f"\n📊 Completed: {successful_steps}/{total_steps} steps")
    
    if successful_steps >= 4:  # At least core steps completed
        print_next_steps()
    else:
        print("\n⚠️  Setup incomplete. Please resolve the issues above.")
        print("📖 Check README.md for troubleshooting help.")

if __name__ == "__main__":
    main()