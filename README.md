# Live Face Detection and College ID Card Verification System - Java Implementation

A complete **Java-based system** for verifying student identity by comparing live camera captures with college ID card photos using advanced computer vision technology.

## 🎯 Project Overview

This system is designed as a **college final year project** that demonstrates:
- **Live Camera Integration**: Real-time face capture using Java and OpenCV
- **PDF Processing**: Extract images and text from college ID cards using Apache PDFBox
- **Face Recognition**: Advanced face comparison using OpenCV for Java
- **RESTful API**: Complete Spring Boot-based backend with comprehensive endpoints
- **Error Handling**: Robust validation and error management

## 🛠️ Tech Stack

- **Language**: Java 17
- **Framework**: Spring Boot 3.2.1
- **Computer Vision**: OpenCV for Java
- **PDF Processing**: Apache PDFBox
- **Image Processing**: Java BufferedImage, OpenCV Mat
- **Build Tool**: Maven
- **Web Camera**: Webcam Capture Library

## 🚀 Features

### 1. Live Camera Face Capture
- Initialize system camera (webcam) using Java
- Real-time face detection with OpenCV
- Automatic face capture and validation
- High-quality image saving with timestamps

### 2. ID Card PDF Processing
- Upload college ID card in PDF format using Spring Boot
- Extract student photos from PDF using Apache PDFBox
- Extract text content and student details with regex parsing
- Support for various PDF formats

### 3. Advanced Face Verification
- Detect faces in both live and ID card images using OpenCV
- Handle multiple error scenarios with proper validation
- Calculate confidence scores using similarity algorithms
- Configurable tolerance levels

### 4. Comprehensive REST API
- `POST /api/start-camera` - Initialize camera
- `POST /api/capture-face` - Capture live face
- `POST /api/upload-id-card` - Upload and process ID card
- `POST /api/verify` - Complete identity verification
- Additional utility endpoints for testing and debugging

## 📁 Project Structure

```
face-verification-system/
├── src/main/java/com/college/project/
│   ├── FaceVerificationApplication.java    # Main Spring Boot application
│   ├── config/
│   │   └── OpenCVConfig.java              # OpenCV configuration
│   ├── controller/
│   │   ├── MainController.java            # API documentation endpoints
│   │   ├── CameraController.java          # Camera operations
│   │   └── VerificationController.java    # PDF processing and verification
│   ├── service/
│   │   ├── CameraService.java             # Camera operations
│   │   ├── PDFService.java                # PDF processing
│   │   └── FaceVerificationService.java   # Face recognition
│   └── model/
│       ├── ApiResponse.java               # Standard API response
│       ├── StudentDetails.java            # Student information model
│       └── VerificationResult.java        # Verification result model
├── src/main/resources/
│   └── application.properties             # Spring Boot configuration
├── uploads/                               # ID card PDFs and extracted images
├── camera/                                # Live camera captures
├── pom.xml                                # Maven dependencies
└── README.md                              # This file
```

## 🔧 Installation & Setup

### Prerequisites
- **Java 17** or higher
- **Maven 3.6+**
- **Webcam/Camera** connected to your system
- **Windows/Linux/macOS**

### Step 1: Install Maven
Follow the instructions in `INSTALL_MAVEN.md` to install Maven on your system.

### Step 2: Build and Run
```bash
# Run the build script
build_and_run.bat

# Or manually:
mvn clean compile
mvn spring-boot:run
```

### Step 3: Test the System
```bash
# Test all endpoints
python test_java_api.py
```

The server will start at `http://localhost:8080`

## 📖 API Usage Guide

### 1. Initialize Camera
```bash
curl -X POST http://localhost:8080/api/start-camera
```

### 2. Capture Live Face
```bash
curl -X POST http://localhost:8080/api/capture-face
```

### 3. Upload ID Card PDF
```bash
curl -X POST -F "file=@student_id_card.pdf" http://localhost:8080/api/upload-id-card
```

### 4. Verify Identity
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "cameraImagePath": "camera/captured_face_20240120_143022.jpg",
  "idCardImagePath": "uploads/extracted_image_p1_1.png",
  "studentDetails": {
    "name": "John Doe",
    "registerNumber": "REG123456"
  }
}' http://localhost:8080/api/verify
```

## 🧪 Testing the System

### Test System Health
```bash
curl http://localhost:8080/health
```

### Get API Documentation
```bash
curl http://localhost:8080/
```

### Complete API Testing
```bash
python test_java_api.py
```

## 🎓 College Project Excellence

### **Demonstrates Advanced Concepts:**
- ✅ **Computer Vision**: Real-time face detection using OpenCV for Java
- ✅ **Machine Learning**: Face comparison and similarity analysis
- ✅ **Web Development**: Professional Spring Boot REST API
- ✅ **File Processing**: Advanced PDF parsing with Apache PDFBox
- ✅ **Error Handling**: Comprehensive validation and user feedback
- ✅ **Software Architecture**: Clean, modular Spring Boot design
- ✅ **Documentation**: Professional-grade API documentation

### **Production-Ready Features:**
- ✅ Comprehensive error handling with helpful messages
- ✅ Professional logging and debugging capabilities
- ✅ Modular Spring Boot architecture
- ✅ Complete REST API with proper HTTP status codes
- ✅ Cross-platform compatibility (Java)
- ✅ Maven-based dependency management

## 🚀 Building and Deployment

### Build JAR File
```bash
mvn clean package
```

### Run JAR File
```bash
java -jar target/face-verification-system-1.0.0.jar
```

## 📄 Dependencies

Key Maven dependencies used:
- **Spring Boot Starter Web**: REST API framework
- **OpenCV**: Computer vision and face detection
- **Apache PDFBox**: PDF processing and text extraction
- **Webcam Capture**: Java webcam integration
- **Jackson**: JSON processing
- **Spring Boot Actuator**: Health checks and monitoring

## 🔧 Troubleshooting

### Common Issues

1. **Maven not found**:
   - Follow `INSTALL_MAVEN.md` for installation instructions
   - Ensure Maven is added to your PATH environment variable

2. **Camera not working**:
   - Check camera permissions in your OS
   - Ensure camera is not used by other applications
   - Verify webcam-capture library compatibility

3. **PDF processing issues**:
   - Ensure PDF contains images and text
   - Check PDF is not password protected
   - Verify Apache PDFBox compatibility

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages and logs
3. Ensure all dependencies are properly installed
4. Verify camera and file permissions

---

**🎉 Congratulations! You now have a complete Java-based Face Verification System perfect for your college final year project!**