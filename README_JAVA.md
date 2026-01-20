# Live Face Detection and College ID Card Verification System - Java Implementation

A complete Java-based system for verifying student identity by comparing live camera captures with college ID card photos using advanced computer vision technology.

## 🎯 Project Overview

This system is designed as a college final year project that demonstrates:
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
└── README_JAVA.md                         # This file
```

## 🔧 Installation & Setup

### Prerequisites
- **Java 17** or higher
- **Maven 3.6+**
- **Webcam/Camera** connected to your system
- **Windows/Linux/macOS**

### Step 1: Clone or Download Project
```bash
# If using git
git clone <repository-url>
cd face-verification-system

# Or download and extract the project files
```

### Step 2: Install Dependencies
```bash
# Install Maven dependencies
mvn clean install
```

### Step 3: Verify Java and Maven
```bash
# Check Java version
java -version

# Check Maven version
mvn -version
```

### Step 4: Run the Application
```bash
# Run using Maven
mvn spring-boot:run

# Or run the JAR file
java -jar target/face-verification-system-1.0.0.jar
```

The server will start at `http://localhost:8080`

## 📖 API Usage Guide

### 1. Initialize Camera
```bash
curl -X POST http://localhost:8080/api/start-camera
```

**Response:**
```json
{
  "status": "success",
  "message": "Camera initialized successfully",
  "data": {
    "cameraInfo": {
      "width": 640,
      "height": 480,
      "fps": 30
    }
  }
}
```

### 2. Capture Live Face
```bash
curl -X POST http://localhost:8080/api/capture-face
```

**Response:**
```json
{
  "status": "success",
  "message": "Face captured successfully",
  "data": {
    "imagePath": "camera/captured_face_20240120_143022.jpg",
    "timestamp": "2024-01-20T14:30:22.123456",
    "faceCount": 1
  }
}
```

### 3. Upload ID Card PDF
```bash
curl -X POST -F "file=@student_id_card.pdf" http://localhost:8080/api/upload-id-card
```

**Response:**
```json
{
  "status": "success",
  "message": "ID card processed successfully",
  "data": {
    "processingResults": {
      "images": {
        "totalImages": 1,
        "studentPhoto": {
          "filename": "extracted_image_p1_1.png",
          "path": "uploads/extracted_image_p1_1.png"
        }
      },
      "text": {
        "studentDetails": {
          "name": "John Doe",
          "registerNumber": "REG123456",
          "department": "Computer Science"
        }
      }
    }
  }
}
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

**Response:**
```json
{
  "status": "success",
  "message": "Faces appear to match with 87.45% confidence",
  "data": {
    "result": "Verified",
    "confidence": 87.45,
    "isMatch": true,
    "studentDetails": {
      "name": "John Doe",
      "registerNumber": "REG123456"
    },
    "method": "Basic OpenCV comparison (Java)",
    "recommendation": "Moderate confidence match"
  }
}
```

## 🔍 Error Handling

The system handles various error scenarios:

### Camera Errors
- **Camera not detected**: Check camera connection and permissions
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

Edit `src/main/resources/application.properties` to customize:

```properties
# Camera settings
app.camera.width=640
app.camera.height=480
app.camera.fps=30

# Face recognition settings
app.face.recognition.tolerance=0.6

# File upload settings
spring.servlet.multipart.max-file-size=16MB

# Server settings
server.port=8080
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

### Get System Information
```bash
curl http://localhost:8080/api/info
```

## 📝 Sample Workflow

1. **Start the application**: `mvn spring-boot:run`
2. **Initialize camera**: Call `/api/start-camera`
3. **Capture live face**: Call `/api/capture-face`
4. **Upload ID card**: Call `/api/upload-id-card` with PDF file
5. **Verify identity**: Call `/api/verify` with both image paths
6. **Get results**: Receive verification status and confidence score

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

### Create Docker Image (Optional)
```dockerfile
FROM openjdk:17-jdk-slim
COPY target/face-verification-system-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
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

1. **OpenCV not loading**:
   - Ensure OpenCV native libraries are properly loaded
   - Check system architecture compatibility

2. **Camera not working**:
   - Check camera permissions in your OS
   - Ensure camera is not used by other applications
   - Verify webcam-capture library compatibility

3. **PDF processing issues**:
   - Ensure PDF contains images and text
   - Check PDF is not password protected
   - Verify Apache PDFBox compatibility

4. **Build errors**:
   - Ensure Java 17 is installed and configured
   - Check Maven is properly installed
   - Verify internet connection for dependency download

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages and logs
3. Ensure all dependencies are properly installed
4. Verify camera and file permissions

---

**🎉 Congratulations! You now have a complete Java-based Face Verification System perfect for your college final year project!**