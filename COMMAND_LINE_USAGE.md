# Face Verification System - Command Line Mode

## Overview
This application verifies student identity by comparing a student photo (captured from camera OR uploaded from file) with their ID card PDF. It processes the ID card, extracts information, and generates detailed verification reports.

## Requirements
1. **Camera OR Student Photo**: Working webcam OR student photo file (jpg, png, bmp)
2. **ID Card PDF**: Place your ID card PDF as `idcard.pdf` in the project root directory
3. **Java 17**: Installed and configured
4. **Maven**: Installed and added to PATH

## How to Use

### Step 1: Prepare Your Files
- Place your college ID card PDF file in the project root directory
- Rename it to exactly: `idcard.pdf`
- (Optional) If uploading photo: place your student photo in the project root

### Step 2: Run the Application
```cmd
run_face_capture.bat
```

Or manually:
```cmd
mvn spring-boot:run
```

### Step 3: Choose Input Method
The application will ask you to choose:

**Option 1: Camera Capture**
- Press Enter when ready
- Look at your camera
- 3-second countdown before capture

**Option 2: Upload Photo**
- Place your student photo in project directory
- Enter the filename (e.g., `my_photo.jpg`)
- System validates and copies the photo

### Step 4: Automatic Processing
The system will automatically:
- Process your `idcard.pdf`
- Extract images and text from ID card
- Save processed PDF to `idcards/` folder
- Compare your photo with ID card photo
- Generate verification report

## Output Folders
After running, check these folders:

- `camera/` - Captured face images (if using camera)
- `student_photos/` - Uploaded student photos (if uploading)
- `idcards/` - Processed ID card PDFs with timestamp
- `uploads/` - Extracted images from ID card PDF
- `reports/` - Verification reports named as `STUDENT_NAME_verification_timestamp.pdf`

## Supported Photo Formats
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`

## Troubleshooting

### Camera Issues (Option 1)
- Close other camera apps (Skype, Teams, Zoom)
- Check Windows Camera privacy settings
- Try Windows Camera app first to verify camera works

### Photo Upload Issues (Option 2)
- Ensure photo file exists in project root directory
- Check file format is supported (.jpg, .png, .bmp)
- Make sure filename is typed correctly

### PDF Issues
- Ensure `idcard.pdf` exists in project root
- Make sure PDF is not corrupted
- PDF should contain both text and images

### Application Issues
- Make sure Maven is installed: `mvn --version`
- Check Java version: `java --version` (should be 17+)
- Restart application if camera gets stuck

## Features
✅ **Dual Input Options**: Camera capture OR photo upload  
✅ **PDF Processing**: Extract text and images from ID cards  
✅ **Face Verification**: Compare student photo with ID card photo  
✅ **Detailed Reports**: PDF and text reports with verification results  
✅ **Automatic File Organization**: Organized folder structure  
✅ **Student Name Detection**: Reports named after detected student name  
✅ **No Web Interface**: Pure command line application  

## Example Output
```
🎓 FACE CAPTURE AND ID CARD PROCESSING SYSTEM
============================================================

📷 STEP 1: CHOOSE FACE INPUT METHOD
----------------------------------------
1. Capture face from camera
2. Upload student photo from file
Enter your choice (1 or 2): 2

📁 UPLOADING STUDENT PHOTO
------------------------------
Please place your student photo in the project root directory.
Supported formats: .jpg, .jpeg, .png, .bmp
Example: student_photo.jpg
Enter the filename of your student photo: my_photo.jpg
✅ Student photo uploaded successfully!
📁 Saved to: student_photos/student_photo_20260120_130245.jpg

📄 STEP 2: PROCESSING ID CARD PDF
----------------------------------------
✅ ID card PDF processed successfully!
📁 Saved to: idcards/idcard_20260120_130250.pdf
👤 Student Details:
   - Name: THAMARAI SELVAN S
   - Register Number: 23CS149
   - Department: CSE C

🔍 STEP 3: FACE VERIFICATION
----------------------------------------
📸 Student image: student_photos/student_photo_20260120_130245.jpg
📄 ID card photo: uploads/extracted_image_p1_Im0.png

🎯 VERIFICATION RESULTS:
------------------------------
Student Image: Uploaded Photo
ID Card Photo: Extracted from PDF
Result: ✅ MATCH
Confidence: 87.3%
Method: Java Image Processing

📄 Generating verification report...
✅ Verification report saved successfully!
📁 Report saved as: reports/THAMARAI_SELVAN_S_verification_20260120_130255.pdf
👤 Student: THAMARAI_SELVAN_S

✅ PROCESS COMPLETED SUCCESSFULLY!
```