# Installation Guide - Face Verification System

## 🚀 Quick Start (Recommended)

### Option 1: Automated Setup
```bash
python setup.py
```
This script will automatically:
- Check Python version
- Create virtual environment
- Install dependencies
- Test camera access
- Verify installation

### Option 2: Interactive System Runner
```bash
python run_system.py
```
This will guide you through the complete workflow including installation checks.

## 📋 Manual Installation

### Prerequisites
- **Python 3.8+** (Required)
- **Webcam/Camera** connected to your system
- **Windows/Linux/macOS** operating system

### Step 1: Download Project
```bash
# If using git
git clone <repository-url>
cd face-verification-system

# Or download and extract the project files
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv face_verification_env

# Activate virtual environment
# Windows:
face_verification_env\Scripts\activate
# macOS/Linux:
source face_verification_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Installing `face_recognition` may take 5-10 minutes as it compiles dlib.

### Step 4: Verify Installation
```bash
python -c "import cv2, face_recognition, flask; print('All packages installed successfully!')"
```

### Step 5: Test Camera
```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error'); cap.release()"
```

## 🔧 Troubleshooting

### Common Installation Issues

#### 1. face_recognition Installation Fails
**Windows:**
```bash
# Install Visual C++ Build Tools first
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Then install face_recognition
pip install cmake
pip install dlib
pip install face_recognition
```

**macOS:**
```bash
# Install Xcode command line tools
xcode-select --install

# Install face_recognition
pip install face_recognition
```

**Linux (Ubuntu/Debian):**
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev

# Install face_recognition
pip install face_recognition
```

#### 2. OpenCV Issues
```bash
# If cv2 import fails
pip uninstall opencv-python
pip install opencv-python==4.8.1.78

# For Linux, you might need:
sudo apt-get install python3-opencv
```

#### 3. Camera Not Working
- **Check camera permissions** in your OS settings
- **Close other applications** using the camera (Skype, Teams, etc.)
- **Try different camera index** in `app/utils/config.py`:
  ```python
  CAMERA_INDEX = 1  # Try 1, 2, etc. instead of 0
  ```

#### 4. PDF Processing Issues
```bash
# If PyMuPDF fails to install
pip install --upgrade pip
pip install PyMuPDF==1.23.8

# Alternative PDF library
pip install pdfplumber==0.10.0
```

#### 5. Memory Issues During Installation
```bash
# Increase pip timeout and use no-cache
pip install --no-cache-dir --timeout 1000 -r requirements.txt
```

## 🖥️ System-Specific Instructions

### Windows 10/11
1. **Install Python 3.8+** from python.org
2. **Install Visual C++ Build Tools** (for face_recognition)
3. **Enable camera permissions** in Windows Settings
4. **Run Command Prompt as Administrator** if needed

### macOS
1. **Install Python 3.8+** using Homebrew or python.org
2. **Install Xcode Command Line Tools**: `xcode-select --install`
3. **Grant camera permissions** in System Preferences > Security & Privacy
4. **Use Terminal** for all commands

### Linux (Ubuntu/Debian)
1. **Install Python 3.8+**: `sudo apt-get install python3.8 python3-pip`
2. **Install development tools**: `sudo apt-get install build-essential cmake`
3. **Install camera drivers** if needed
4. **Grant camera permissions** to your user

## 🧪 Verify Installation

### Test 1: Basic Import Test
```bash
python -c "
import flask
import cv2
import face_recognition
import fitz
import pdfplumber
import numpy
from PIL import Image
print('✅ All packages imported successfully!')
"
```

### Test 2: Camera Test
```bash
python -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print('✅ Camera is working!')
    else:
        print('❌ Camera detected but cannot capture')
    cap.release()
else:
    print('❌ Camera not detected')
"
```

### Test 3: Face Recognition Test
```bash
python -c "
import face_recognition
import numpy as np
# Create dummy face encoding
encoding = np.random.random(128)
print('✅ Face recognition library is working!')
"
```

### Test 4: Run Application
```bash
python app.py
```
Should show:
```
🚀 Starting Live Face Detection and ID Card Verification System...
📷 Make sure your camera is connected and working
🌐 Server will be available at: http://localhost:5000
```

## 📦 Alternative Installation Methods

### Using Conda
```bash
# Create conda environment
conda create -n face_verification python=3.9
conda activate face_verification

# Install packages
conda install flask opencv numpy pillow
pip install face_recognition PyMuPDF pdfplumber
```

### Using Docker (Advanced)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential cmake libopenblas-dev liblapack-dev \
    && pip install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔍 Dependency Details

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework |
| opencv-python | 4.8.1.78 | Camera and image processing |
| face-recognition | 1.3.0 | Face detection and recognition |
| PyMuPDF | 1.23.8 | PDF processing |
| pdfplumber | 0.10.0 | PDF text extraction |
| numpy | 1.24.3 | Numerical computations |
| Pillow | 10.0.1 | Image processing |

## 🆘 Getting Help

If you encounter issues:

1. **Check the error message** carefully
2. **Review this troubleshooting guide**
3. **Check Python and package versions**
4. **Verify camera permissions and availability**
5. **Try the automated setup script**: `python setup.py`
6. **Use the interactive runner**: `python run_system.py`

## ✅ Installation Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created (optional but recommended)
- [ ] All packages from requirements.txt installed
- [ ] Camera detected and accessible
- [ ] Flask server starts without errors
- [ ] All import tests pass
- [ ] Ready to run the complete system!

---

**Next Steps**: Once installation is complete, run `python run_system.py` for an interactive walkthrough of the complete system!