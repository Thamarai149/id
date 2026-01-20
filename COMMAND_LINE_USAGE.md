# Face Capture and ID Card Processing - Command Line Mode

## Overview
This application captures your face from the camera, processes your ID card PDF, and performs face verification - all through a simple command line interface.

## Requirements
1. **Camera**: Working webcam connected to your computer
2. **ID Card PDF**: Place your ID card PDF as `idcard.pdf` in the project root directory
3. **Java 17**: Installed and configured
4. **Maven**: Installed and added to PATH

## How to Use

### Step 1: Prepare Your ID Card
- Place your college ID card PDF file in the project root directory
- Rename it to exactly: `idcard.pdf`

### Step 2: Run the Application
```cmd
run_face_capture.bat
```

Or manually:
```cmd
mvn spring-boot:run
```

### Step 3: Follow the Prompts
The application will guide you through:

1. **Face Capture**: 
   - Press Enter when ready
   - Look at your camera
   - The system will capture your face automatically

2. **ID Card Processing**:
   - The system will automatically process `idcard.pdf`
   - Extract images and text from both front and back
   - Save processed PDF to `idcards/` folder

3. **Face Verification**:
   - Compare your captured face with ID card photo
   - Display verification results

## Output Folders
After running, check these folders:

- `camera/` - Your captured face images
- `idcards/` - Processed ID card PDFs with timestamp
- `uploads/` - Extracted images from ID card PDF

## Troubleshooting

### Camera Issues
- Close other camera apps (Skype, Teams, Zoom)
- Check Windows Camera privacy settings
- Try Windows Camera app first to verify camera works

### PDF Issues
- Ensure `idcard.pdf` exists in project root
- Make sure PDF is not corrupted
- PDF should contain both text and images

### Application Issues
- Make sure Maven is installed: `mvn --version`
- Check Java version: `java --version` (should be 17+)
- Restart application if camera gets stuck

## Features
✅ Automatic face capture from camera  
✅ PDF processing (front and back pages)  
✅ Text extraction from ID card  
✅ Image extraction from ID card  
✅ Face verification between captured and ID card photos  
✅ Automatic file organization  
✅ No web interface - pure command line  

## Example Output
```
🎓 FACE CAPTURE AND ID CARD PROCESSING SYSTEM
============================================================

📷 STEP 1: CAPTURING YOUR FACE
----------------------------------------
Press Enter to capture your face from camera...
✅ Face captured successfully!
📁 Saved to: camera/captured_face_20260120_124530.jpg

📄 STEP 2: PROCESSING ID CARD PDF
----------------------------------------
✅ ID card PDF processed successfully!
📁 Saved to: idcards/idcard_20260120_124535.pdf
👤 Student Details:
   - Name: John Doe
   - Register Number: 12345678
   - Department: Computer Science

🔍 STEP 3: FACE VERIFICATION
----------------------------------------
🎯 VERIFICATION RESULTS:
------------------------------
Result: ✅ MATCH
Confidence: 85.2%
Method: Java Image Processing

✅ PROCESS COMPLETED SUCCESSFULLY!
```