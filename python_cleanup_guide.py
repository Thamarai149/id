"""
Python Version Cleanup Guide
Helps manage multiple Python installations on Windows

Usage: python python_cleanup_guide.py
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print('='*60)

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n📋 {description}")
    print(f"Command: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print("❌ Failed")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_current_python():
    """Check current Python version and location"""
    print_header("Current Python Information")
    
    print("🐍 Current Python version:")
    run_command("python --version", "Python version")
    
    print("\n📍 Python executable location:")
    run_command("where python", "Python location")
    
    print("\n📦 Pip version:")
    run_command("pip --version", "Pip version")

def list_conda_environments():
    """List all conda environments"""
    print_header("Anaconda Environments")
    
    print("📋 Listing all conda environments:")
    run_command("conda env list", "Conda environments")

def cleanup_conda_environments():
    """Guide for cleaning up conda environments"""
    print_header("Conda Environment Cleanup")
    
    print("🧹 To remove old conda environments, use these commands:")
    print("\n1. Remove specific environment:")
    print("   conda env remove -n rvc")
    print("   conda env remove -n rvc310")
    print("   conda env remove -n rvc_env")
    
    print("\n2. Remove all environments except base:")
    print("   conda env list | grep -v base | awk '{print $1}' | xargs -I {} conda env remove -n {}")
    
    print("\n3. Clean conda cache:")
    print("   conda clean --all")

def uninstall_python_versions():
    """Guide for uninstalling Python versions"""
    print_header("Python Version Uninstallation Guide")
    
    print("🗑️  To uninstall Python versions:")
    
    print("\n1. Uninstall via Windows Settings:")
    print("   - Open Settings > Apps")
    print("   - Search for 'Python'")
    print("   - Uninstall older versions")
    
    print("\n2. Uninstall Anaconda (if desired):")
    print("   - Use Anaconda-Navigator > File > Uninstall")
    print("   - Or use Windows Settings > Apps > Anaconda3")
    
    print("\n3. Clean up PATH environment variable:")
    print("   - Remove old Python paths from system PATH")
    print("   - Keep only: C:\\Python314\\Scripts\\;C:\\Python314\\;")

def setup_python314_only():
    """Guide for setting up Python 3.14 as the only version"""
    print_header("Python 3.14 Setup Guide")
    
    print("🎯 To use only Python 3.14:")
    
    print("\n1. Verify Python 3.14 installation:")
    print("   C:\\Python314\\python.exe --version")
    
    print("\n2. Update PATH environment variable:")
    print("   - Add to beginning of PATH: C:\\Python314\\Scripts\\;C:\\Python314\\;")
    print("   - Remove all other Python paths")
    
    print("\n3. Reinstall packages for Python 3.14:")
    print("   pip install -r requirements.txt")

def create_virtual_environment():
    """Guide for creating a virtual environment"""
    print_header("Virtual Environment Setup")
    
    print("🏠 Create a dedicated environment for your project:")
    
    print("\n1. Create virtual environment:")
    print("   python -m venv face_verification_env")
    
    print("\n2. Activate virtual environment:")
    print("   face_verification_env\\Scripts\\activate")
    
    print("\n3. Install project dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n4. Run your project:")
    print("   python app.py")

def main():
    """Main cleanup guide"""
    print("🚀 Python Version Cleanup Guide")
    print("This guide will help you manage your Python installations")
    
    # Check current setup
    check_current_python()
    
    # List conda environments
    try:
        list_conda_environments()
    except:
        print("⚠️  Anaconda not found or not in PATH")
    
    # Provide cleanup options
    print_header("Cleanup Options")
    
    print("Choose your preferred approach:")
    print("\n🎯 Option 1: Keep Python 3.14 only (Recommended)")
    print("   - Uninstall Anaconda completely")
    print("   - Use Python 3.14 with virtual environments")
    print("   - Cleaner, simpler setup")
    
    print("\n🐍 Option 2: Keep Anaconda with Python 3.14")
    print("   - Update Anaconda base to Python 3.14")
    print("   - Remove old environments")
    print("   - Use conda for package management")
    
    print("\n🔄 Option 3: Hybrid approach")
    print("   - Keep both systems")
    print("   - Use Python 3.14 for this project")
    print("   - Keep Anaconda for other projects")
    
    choice = input("\nWhich option do you prefer? (1/2/3): ").strip()
    
    if choice == "1":
        print_header("Option 1: Python 3.14 Only Setup")
        uninstall_python_versions()
        setup_python314_only()
        create_virtual_environment()
        
    elif choice == "2":
        print_header("Option 2: Anaconda with Python 3.14")
        cleanup_conda_environments()
        print("\n📋 Steps to update Anaconda base:")
        print("1. conda update conda")
        print("2. conda install python=3.14")
        print("3. conda create -n face_verification python=3.14")
        print("4. conda activate face_verification")
        
    elif choice == "3":
        print_header("Option 3: Hybrid Setup")
        create_virtual_environment()
        print("\n💡 Use virtual environment for this project:")
        print("   face_verification_env\\Scripts\\activate")
        
    else:
        print("❌ Invalid choice")
        return
    
    # Final recommendations
    print_header("Final Recommendations")
    
    print("🎯 For your Face Verification project:")
    print("✅ Use Python 3.14 (it's working perfectly)")
    print("✅ Create a dedicated virtual environment")
    print("✅ Install only required packages")
    print("✅ Keep the system clean and simple")
    
    print("\n🚀 Your project is already working with Python 3.14!")
    print("The cleanup is optional - your system is functional as-is.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Cleanup guide interrupted")
    except Exception as e:
        print(f"\n💥 Error: {e}")