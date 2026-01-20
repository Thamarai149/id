# CSE Multi-Student ID Card Face Matching System

## Project Overview

This Java console application is developed to **automatically identify and extract a specific student ID card from a PDF containing multiple student ID cards** of the CSE department (three classes). The system uses advanced face recognition techniques to match a user's face with ID cards in a multi-student database.

## How It Works

### 1. **Face Input**
The application provides two options for face input:
- **Camera Capture**: Activates the laptop camera to capture the user's face in real-time
- **Photo Upload**: Browse and select a photo from anywhere on the computer (This PC)

### 2. **Face Processing**
Using OpenCV-based face detection and recognition techniques, the captured/uploaded face is processed and encoded for comparison.

### 3. **Multi-Student PDF Processing**
The program reads a multi-page PDF file (`cse_students_idcards.pdf`) containing ID cards of all CSE students from 3 classes and:
- Extracts individual ID card images from each page
- Detects faces present on each ID card
- Processes student information from each card

### 4. **Face Matching Algorithm**
The system compares the user's face with **ALL** faces extracted from the CSE student ID cards:
- Performs face-to-face comparison with each student ID card
- Calculates confidence scores for each comparison
- Identifies the best matching ID card based on highest confidence

### 5. **Selective Extraction**
When a matching face is found:
- **ONLY** the corresponding student's ID card is selected
- **ALL** other students' ID cards are ignored
- The matched ID card is saved as a separate PDF file

### 6. **Automated Reporting**
The system generates comprehensive reports including:
- Verification results with confidence scores
- Detailed matching information
- PDF reports named after the matched student

## Key Features

### 🎯 **Automated ID Verification**
- Eliminates manual searching through hundreds of ID cards
- Automatically finds your ID card from the entire CSE database
- Reduces human error in ID verification processes

### 🔍 **Advanced Face Recognition**
- Uses OpenCV-based face detection algorithms
- Compares facial features with high accuracy
- Handles different lighting conditions and image qualities

### 📊 **Multi-Class Support**
- Processes ID cards from 3 CSE classes simultaneously
- Handles large databases of student ID cards
- Scalable to accommodate more classes/students

### 💻 **User-Friendly Interface**
- Simple command-line interface with clear instructions
- Multiple input options (camera capture or file upload)
- File browser integration for easy photo selection

### 📄 **Intelligent PDF Processing**
- Extracts individual images from multi-page PDFs
- Processes text information from ID cards
- Creates separate PDF files for matched ID cards

## Technical Implementation

### **Technologies Used**
- **Java 17** with Spring Boot framework
- **OpenCV** for face detection and recognition
- **Apache PDFBox** for PDF processing and manipulation
- **Java Swing** for file chooser interface
- **Maven** for dependency management

### **Architecture**
- **Service-Oriented Architecture** with separate services for:
  - Camera operations (`CameraService`)
  - PDF processing (`PDFService`)
  - Face verification (`FaceVerificationService`)
  - Report generation (`ReportGenerationService`)

### **Face Recognition Pipeline**
1. **Face Detection**: Locate faces in images using OpenCV
2. **Feature Extraction**: Extract facial features and create encodings
3. **Comparison Algorithm**: Compare feature vectors between faces
4. **Confidence Scoring**: Calculate similarity percentages
5. **Best Match Selection**: Choose highest confidence match

## File Structure

```
📁 Project Root
├── 📄 cse_students_idcards.pdf (Input: Multi-student ID cards)
├── 📁 camera/ (Camera captured images)
├── 📁 student_photos/ (Uploaded photos)
├── 📁 extracted_idcards/ (Individual ID cards from PDF)
├── 📁 matched_idcards/ (Your matching ID card as separate PDF)
├── 📁 uploads/ (Extracted images from PDF processing)
└── 📁 reports/ (Verification reports and results)
```

## Usage Instructions

### **Prerequisites**
1. Place the multi-student ID cards PDF as `cse_students_idcards.pdf` in project root
2. Ensure Java 17 and Maven are installed
3. Have a working camera (if using camera capture option)

### **Running the Application**
```bash
# Using the batch file
run_face_capture.bat

# Or manually with Maven
mvn spring-boot:run
```

### **Step-by-Step Process**
1. **Choose Input Method**: Camera capture OR photo upload
2. **Provide Your Face**: Either capture live or browse for existing photo
3. **Automatic Processing**: System processes multi-student PDF
4. **Face Matching**: Compares your face with all CSE student faces
5. **Result**: Get your matching ID card as separate PDF

## Example Output

```
🎓 CSE MULTI-STUDENT ID CARD FACE MATCHING SYSTEM
======================================================================
📊 Automatically find and extract your ID card from CSE database
🔍 Compares your face with all CSE students (3 classes)

📷 STEP 1: CHOOSE FACE INPUT METHOD
1. Capture face from camera
2. Upload student photo (browse from This PC)

📄 STEP 2: PROCESSING MULTI-STUDENT ID CARDS PDF
📊 This PDF contains ID cards from CSE department (3 classes)
📸 Extracted 45 images from multi-student PDF
🎓 Found 45 potential student ID cards

🔍 STEP 3: FACE MATCHING AND ID CARD EXTRACTION
🔄 Searching for matching face in all CSE student ID cards...
🔍 Comparing your face with 45 ID card photos...
   Checking ID Card 23/45: extracted_image_p23_Im0.png
      → Confidence: 87.3% ✅ MATCH

🎯 BEST MATCH FOUND!
📸 Matching ID card: uploads/extracted_image_p23_Im0.png
🎯 Confidence: 87.3%
📄 Extracting matching ID card as separate PDF...
✅ Matching ID card saved as PDF: matched_idcards/Student_23_IDCard_20260120_143022.pdf

✅ MATCHING ID CARD FOUND AND EXTRACTED!
📁 Matched ID card saved to: matched_idcards/Student_23_IDCard_20260120_143022.pdf
```

## Benefits for College Projects

### **Academic Value**
- Demonstrates practical application of computer vision
- Combines multiple technologies (Java, OpenCV, PDF processing)
- Shows real-world problem-solving skills
- Implements automated document processing

### **Industry Relevance**
- Addresses actual problems in educational institutions
- Showcases skills in face recognition technology
- Demonstrates ability to handle large datasets
- Shows understanding of user experience design

### **Technical Skills Demonstrated**
- Object-oriented programming in Java
- Integration of multiple libraries and frameworks
- File processing and manipulation
- User interface design
- Error handling and validation
- Automated report generation

## Future Enhancements

- **Database Integration**: Store student information in database
- **Web Interface**: Create web-based version for easier access
- **Batch Processing**: Process multiple student faces simultaneously
- **Advanced ML**: Implement deep learning models for better accuracy
- **Mobile App**: Create mobile version for on-the-go verification
- **Cloud Integration**: Deploy to cloud for scalable access

## Conclusion

This project successfully demonstrates the practical application of face recognition technology in an educational setting. It reduces manual effort, improves accuracy, and provides an automated solution for ID card verification in large student databases. The system is suitable as a college mini project and showcases advanced programming skills with real-world applications.