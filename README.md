# Live Face Detection and College ID Card Verification System

A complete Python-based system for verifying student identity by comparing live camera captures with college ID card photos using advanced face recognition technology.

## 🎯 Project Overview

This system is designed as a college final year project that demonstrates:
- **Live Camera Integration**: Real-time face capture using OpenCV
- **PDF Processing**: Extract images and text from college ID cards
- **Face Recognition**: Advanced face comparison using face_recognition library
- **RESTful API**: Complete Flask-based backend with comprehensive endpoints
- **Error Handling**: Robust validation and error management

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Backend Framework**: Flask
- **Computer Vision**: OpenCV (cv2)
- **Face Recognition**: face_recognition library
- **PDF Processing**: PyMuPDF, pdfplumber
- **Image Processing**: NumPy, Pillow
- **API Documentation**: RESTful JSON APIs

## 🚀 Features

### 1. Live Camera Face Capture
- Initialize system camera (webcam)
- Real-time face detection with visual feedback
- Interactive capture (Press 'C' to capture, 'Q' to quit)
- Automatic face validation (single face detection)
- High-quality image saving

### 2. ID Card PDF Processing
- Upload college ID card in PDF format
- Extract student photos from PDF
- Extract text content and student details
- Support for various PDF formats
- Automatic student information parsing

### 3. Advanced Face Verification
- Detect faces in both live and ID card images
- Handle multiple error scenarios:
  - No face detected
  - Multiple faces detected
  - Poor image quality
- Calculate confidence scores using face_recognition
- Configurable tolerance levels

### 4. Comprehensive API Endpoints
- `POST /api/start-camera` - Initialize camera
- `POST /api/capture-face` - Capture live face
- `POST /api/upload-id-card` - Upload and process ID card
- `POST /api/verify` - Complete identity verification
- Additional utility endpoints for testing and debugging

## 📁 Project Structure

```
face-verification-system/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── camera_routes.py      # Camera and capture endpoints
│   │   └── verification_routes.py # PDF processing and verification
│   ├── services/
│   │   ├── __init__.py
│   │   ├── camera_service.py     # Camera operations
│   │   ├── pdf_service.py        # PDF processing
│   │   └── face_verification_service.py # Face recognition
│   └── utils/
│       ├── __init__.py
│       └── config.py             # Configuration settings
├── uploads/                      # ID card PDFs and extracted images
├── camera/                       # Live camera captures
├── app.py                        # Main application entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Webcam/Camera connected to your system
- Windows/Linux/macOS

### Step 1: Clone or Download Project
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
# On Windows:
face_verification_env\\Scripts\\activate
# On macOS/Linux:
source face_verification_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Installing `face_recognition` may take some time as it includes dlib compilation.

### Step 4: Verify Camera Access
- Ensure your camera is connected and not being used by other applications
- Test camera access by running any camera application

### Step 5: Run the Application
```bash
python app.py
```

The server will start at `http://localhost:5000`

## 📖 API Usage Guide

### 1. Initialize Camera
```bash
curl -X POST http://localhost:5000/api/start-camera
```

**Response:**
```json
{
  "status": "success",
  "message": "Camera initialized successfully",
  "data": {
    "camera_info": {
      "width": 640,
      "height": 480,
      "fps": 30
    }
  }
}
```

### 2. Capture Live Face
```bash
curl -X POST http://localhost:5000/api/capture-face
```

**Instructions:**
- Camera window will open
- Position your face in the frame
- Press 'C' key to capture
- Press 'Q' key to quit

**Response:**
```json
{
  "status": "success",
  "message": "Face captured successfully",
  "data": {
    "image_path": "camera/captured_face_20240120_143022.jpg",
    "timestamp": "2024-01-20T14:30:22.123456"
  }
}
```

### 3. Upload ID Card PDF
```bash
curl -X POST -F "file=@student_id_card.pdf" http://localhost:5000/api/upload-id-card
```

**Response:**
```json
{
  "status": "success",
  "message": "ID card processed successfully",
  "data": {
    "processing_results": {
      "images": {
        "total_images": 1,
        "student_photo": {
          "filename": "extracted_image_p1_1.png",
          "path": "uploads/extracted_image_p1_1.png"
        }
      },
      "text": {
        "student_details": {
          "name": "John Doe",
          "register_number": "REG123456",
          "department": "Computer Science",
          "college": "ABC College of Engineering"
        }
      }
    }
  }
}
```

### 4. Verify Identity
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "camera_image_path": "camera/captured_face_20240120_143022.jpg",
  "id_card_image_path": "uploads/extracted_image_p1_1.png",
  "student_details": {
    "name": "John Doe",
    "register_number": "REG123456"
  }
}' http://localhost:5000/api/verify
```

**Response:**
```json
{
  "status": "success",
  "message": "Faces match with 87.45% confidence",
  "data": {
    "result": "Verified",
    "confidence": "87.45%",
    "student_details": {
      "name": "John Doe",
      "register_number": "REG123456",
      "department": "Computer Science"
    },
    "verification_details": {
      "is_match": true,
      "face_distance": 0.3255,
      "recommendation": "High confidence match"
    }
  }
}
```

## 🔍 Error Handling

The system handles various error scenarios:

### Camera Errors
- **Camera not detected**: Check camera connection
- **Camera in use**: Close other applications using camera
- **No face detected**: Ensure face is visible and well-lit
- **Multiple faces**: Only one person should be in frame

### PDF Processing Errors
- **Invalid PDF**: Only PDF files are accepted
- **No images found**: ID card must contain student photo
- **Corrupted PDF**: Upload a valid PDF file
- **No text content**: PDF must contain readable text

### Face Verification Errors
- **Poor image quality**: Ensure good lighting and focus
- **Face not detected**: Images must contain clear faces
- **Low confidence**: May indicate different persons

## ⚙️ Configuration

Edit `app/utils/config.py` to customize:

```python
# Face recognition settings
FACE_RECOGNITION_TOLERANCE = 0.6  # Lower = more strict
FACE_DETECTION_MODEL = 'hog'      # 'hog' or 'cnn'

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# File upload settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## 🧪 Testing the System

### Test Camera Functionality
```bash
curl -X POST http://localhost:5000/api/test-camera
```

### Check System Health
```bash
curl http://localhost:5000/health
```

### Get API Documentation
```bash
curl http://localhost:5000/
```

## 📝 Sample Workflow

1. **Start the application**: `python app.py`
2. **Initialize camera**: Call `/api/start-camera`
3. **Capture live face**: Call `/api/capture-face` and press 'C'
4. **Upload ID card**: Call `/api/upload-id-card` with PDF file
5. **Verify identity**: Call `/api/verify` with both image paths
6. **Get results**: Receive verification status and confidence score

## 🎓 College Project Features

This project demonstrates:
- **Computer Vision**: Real-time face detection and recognition
- **Machine Learning**: Face encoding and similarity comparison
- **Web Development**: RESTful API design and implementation
- **File Processing**: PDF parsing and image extraction
- **Error Handling**: Comprehensive validation and error management
- **Documentation**: Professional code documentation and API guides

## 🔧 Troubleshooting

### Common Issues

1. **Camera not working**:
   - Check camera permissions
   - Ensure camera is not used by other apps
   - Try different camera index in config

2. **Face recognition errors**:
   - Install Visual C++ redistributables (Windows)
   - Ensure good lighting for photos
   - Use high-quality images

3. **PDF processing issues**:
   - Ensure PDF contains images
   - Check PDF is not password protected
   - Verify PDF is not corrupted

4. **Import errors**:
   - Reinstall requirements: `pip install -r requirements.txt`
   - Check Python version compatibility
   - Use virtual environment

## 📄 License

This project is created for educational purposes as a college final year project.

## 👥 Contributors

- AI/ML Full Stack Engineer - Complete system development

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages and logs
3. Ensure all dependencies are properly installed
4. Verify camera and file permissions

---

**Note**: This system is designed for educational purposes and demonstrates face recognition technology. For production use, additional security measures and optimizations should be implemented.