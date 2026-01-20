package com.college.project;

import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.college.project.model.StudentDetails;
import com.college.project.model.VerificationResult;
import com.college.project.service.CameraService;
import com.college.project.service.FaceVerificationService;
import com.college.project.service.PDFService;
import com.college.project.service.ReportGenerationService;

/**
 * Command Line Application for Face Capture and ID Card Processing
 * Automatically captures face, processes ID card PDF, and saves results
 */
@Component
public class CommandLineApp implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(CommandLineApp.class);

    @Autowired
    private CameraService cameraService;

    @Autowired
    private PDFService pdfService;

    @Autowired
    private FaceVerificationService faceVerificationService;

    @Autowired
    private ReportGenerationService reportGenerationService;
    
    // Store student details from PDF processing
    private StudentDetails extractedStudentDetails;

    @Override
    public void run(String... args) throws Exception {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("🎓 FACE CAPTURE AND ID CARD PROCESSING SYSTEM");
        System.out.println("=".repeat(60));

        Scanner scanner = new Scanner(System.in);

        try {
            // Step 1: Choose input method
            System.out.println("\n📷 STEP 1: CHOOSE FACE INPUT METHOD");
            System.out.println("-".repeat(40));
            System.out.println("1. Capture face from camera");
            System.out.println("2. Upload student photo (with file browser)");
            System.out.print("Enter your choice (1 or 2): ");
            
            String choice = scanner.nextLine().trim();
            String studentImagePath;
            
            switch (choice) {
                case "1" -> {
                    System.out.println("\n📷 CAPTURING FROM CAMERA");
                    System.out.println("-".repeat(30));
                    System.out.print("Press Enter to capture your face from camera...");
                    scanner.nextLine();
                    studentImagePath = captureFaceFromCamera();
                }
                case "2" -> {
                    System.out.println("\n📁 UPLOADING STUDENT PHOTO");
                    System.out.println("-".repeat(30));
                    studentImagePath = uploadStudentPhoto(scanner);
                }
                default -> {
                    System.out.println("❌ Invalid choice. Please run the application again.");
                    return;
                }
            }
            
            if (studentImagePath == null) {
                System.out.println("❌ Failed to get student image. Exiting...");
                return;
            }

            // Step 2: Process ID Card PDF
            System.out.println("\n� STEP 2: PROCESSING ID CARD PDF");
            System.out.println("-".repeat(40));
            
            File idCardFile = new File("idcard.pdf");
            if (!idCardFile.exists()) {
                System.out.println("❌ idcard.pdf not found in current directory!");
                System.out.println("Please place your ID card PDF file as 'idcard.pdf' in the project root.");
                return;
            }

            String processedPdfPath = processIdCardPdf(idCardFile);
            if (processedPdfPath == null) {
                System.out.println("❌ Failed to process ID card PDF. Exiting...");
                return;
            }

            // Step 3: Face Verification
            System.out.println("\n🔍 STEP 3: FACE VERIFICATION");
            System.out.println("-".repeat(40));
            performFaceVerification(studentImagePath, processedPdfPath);

            System.out.println("\n✅ PROCESS COMPLETED SUCCESSFULLY!");
            System.out.println("📁 Check the following folders for results:");
            System.out.println("   - camera/ (captured face images)");
            System.out.println("   - student_photos/ (uploaded student photos)");
            System.out.println("   - idcards/ (processed ID card PDF)");
            System.out.println("   - uploads/ (extracted images from PDF)");
            System.out.println("   - reports/ (verification reports named as StudentName.pdf)");

        } catch (Exception e) {
            logger.error("Error in command line application: {}", e.getMessage());
            System.out.println("❌ Error: " + e.getMessage());
        }

        System.out.println("\nPress Enter to exit...");
        scanner.nextLine();
    }

    /**
     * Capture face from camera
     */
    @SuppressWarnings({"java:S2142", "java:S2925"})
    private String captureFaceFromCamera() {
        try {
            System.out.println("🔄 Initializing camera...");
            
            // Initialize camera
            Map<String, Object> initResult = cameraService.initializeCamera();
            if (!(Boolean) initResult.get("success")) {
                System.out.println("❌ Camera initialization failed: " + initResult.get("message"));
                return null;
            }
            
            System.out.println("✅ Camera initialized successfully");
            System.out.println("📸 Capturing face in 3 seconds...");
            
            // Countdown
            for (int i = 3; i > 0; i--) {
                System.out.println("   " + i + "...");
                try {
                    TimeUnit.SECONDS.sleep(1); // More readable than Thread.sleep(1000)
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    System.out.println("⚠️ Countdown interrupted");
                    break;
                }
            }
            
            System.out.println("📷 CAPTURING NOW!");
            
            // Capture face
            Map<String, Object> captureResult = cameraService.captureFace();
            if (!(Boolean) captureResult.get("success")) {
                System.out.println("❌ Face capture failed: " + captureResult.get("message"));
                return null;
            }
            
            String imagePath = (String) captureResult.get("imagePath");
            System.out.println("✅ Face captured successfully!");
            System.out.println("📁 Saved to: " + imagePath);
            
            return imagePath;
            
        } catch (RuntimeException e) {
            logger.error("Error capturing face: {}", e.getMessage());
            System.out.println("❌ Error capturing face: " + e.getMessage());
            return null;
        }
    }

    /**
     * Upload student photo from file
     */
    private String uploadStudentPhoto(Scanner scanner) {
        try {
            // Create student_photos directory
            File studentPhotosDir = new File("student_photos");
            if (!studentPhotosDir.exists()) {
                boolean created = studentPhotosDir.mkdirs();
                if (created) {
                    logger.info("📁 Created student_photos directory");
                }
            }

            System.out.println("📁 Choose how to select your student photo:");
            System.out.println("1. Browse and select file (File Chooser)");
            System.out.println("2. Enter filename manually");
            System.out.print("Enter your choice (1 or 2): ");
            
            String choice = scanner.nextLine().trim();
            File sourceFile;
            
            switch (choice) {
                case "1" -> {
                    System.out.println("📂 Opening file chooser...");
                    sourceFile = openFileChooser();
                    if (sourceFile == null) {
                        System.out.println("❌ No file selected");
                        return null;
                    }
                }
                case "2" -> {
                    System.out.println("📁 Please place your student photo in the project root directory.");
                    System.out.println("Supported formats: .jpg, .jpeg, .png, .bmp");
                    System.out.println("Example: student_photo.jpg");
                    System.out.print("Enter the filename of your student photo: ");
                    
                    String filename = scanner.nextLine().trim();
                    
                    if (filename.isEmpty()) {
                        System.out.println("❌ No filename provided");
                        return null;
                    }
                    
                    sourceFile = new File(filename);
                    if (!sourceFile.exists()) {
                        System.out.println("❌ File not found: " + filename);
                        System.out.println("Please make sure the file exists in the project root directory.");
                        return null;
                    }
                }
                default -> {
                    System.out.println("❌ Invalid choice. Please try again.");
                    return null;
                }
            }
            
            // Additional null check
            if (sourceFile == null) {
                System.out.println("❌ No file selected");
                return null;
            }
            
            // Validate file format
            String filename = sourceFile.getName();
            if (filename == null) {
                System.out.println("❌ Invalid file name");
                return null;
            }
            
            String lowerFilename = filename.toLowerCase();
            if (!lowerFilename.endsWith(".jpg") && !lowerFilename.endsWith(".jpeg") && 
                !lowerFilename.endsWith(".png") && !lowerFilename.endsWith(".bmp")) {
                System.out.println("❌ Unsupported file format. Please use .jpg, .jpeg, .png, or .bmp");
                return null;
            }
            
            // Copy file to student_photos directory with timestamp
            String timestamp = java.time.LocalDateTime.now()
                .format(java.time.format.DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            
            String sourceFileName = sourceFile.getName();
            if (sourceFileName == null || !sourceFileName.contains(".")) {
                System.out.println("❌ Invalid file name");
                return null;
            }
            
            String extension = sourceFileName.substring(sourceFileName.lastIndexOf('.'));
            String newFilename = "student_photo_" + timestamp + extension;
            String destinationPath = "student_photos" + File.separator + newFilename;
            
            // Copy file
            java.nio.file.Files.copy(sourceFile.toPath(), 
                new File(destinationPath).toPath(), 
                java.nio.file.StandardCopyOption.REPLACE_EXISTING);
            
            System.out.println("✅ Student photo uploaded successfully!");
            System.out.println("📁 Source: " + sourceFile.getAbsolutePath());
            System.out.println("📁 Saved to: " + destinationPath);
            
            // Validate image can be read
            try {
                javax.imageio.ImageIO.read(new File(destinationPath));
                System.out.println("✅ Image format validated successfully");
            } catch (IOException | RuntimeException e) {
                System.out.println("⚠️ Warning: Could not validate image format: " + e.getMessage());
            }
            
            return destinationPath;
            
        } catch (IOException | RuntimeException e) {
            logger.error("Error uploading student photo: {}", e.getMessage());
            System.out.println("❌ Error uploading photo: " + e.getMessage());
            return null;
        }
    }

    /**
     * Open file chooser dialog to select image file
     */
    private File openFileChooser() {
        try {
            JFileChooser fileChooser = new JFileChooser();
            
            // Set dialog title
            fileChooser.setDialogTitle("Select Student Photo");
            
            // Set file filter for image files
            FileNameExtensionFilter imageFilter = new FileNameExtensionFilter(
                "Image Files (*.jpg, *.jpeg, *.png, *.bmp)", 
                "jpg", "jpeg", "png", "bmp");
            fileChooser.setFileFilter(imageFilter);
            
            // Set current directory to user's Pictures folder or current directory
            String userHome = System.getProperty("user.home");
            File picturesDir = new File(userHome, "Pictures");
            if (picturesDir.exists()) {
                fileChooser.setCurrentDirectory(picturesDir);
            } else {
                fileChooser.setCurrentDirectory(new File("."));
            }
            
            // Show open dialog
            int result = fileChooser.showOpenDialog(null);
            
            if (result == JFileChooser.APPROVE_OPTION) {
                File selectedFile = fileChooser.getSelectedFile();
                System.out.println("📸 Selected file: " + selectedFile.getAbsolutePath());
                return selectedFile;
            } else {
                System.out.println("📂 File selection cancelled");
                return null;
            }
            
        } catch (RuntimeException e) {
            logger.error("Error opening file chooser: {}", e.getMessage());
            System.out.println("❌ Error opening file chooser: " + e.getMessage());
            System.out.println("💡 Tip: Try option 2 (manual filename entry) instead");
            return null;
        }
    }

    /**
     * Process ID card PDF and save to idcards folder
     */
    private String processIdCardPdf(File idCardFile) {
        try {
            System.out.println("🔄 Processing ID card PDF: " + idCardFile.getName());
            
            // Process the PDF
            Map<String, Object> result = pdfService.processIdCardPdf(idCardFile);
            if (!(Boolean) result.get("success")) {
                System.out.println("❌ PDF processing failed: " + result.get("message"));
                return null;
            }
            
            @SuppressWarnings("unchecked")
            Map<String, Object> fileInfo = (Map<String, Object>) result.get("fileInfo");
            String savedPath = (String) fileInfo.get("savedPath");
            
            System.out.println("✅ ID card PDF processed successfully!");
            System.out.println("📁 Saved to: " + savedPath);
            
            // Display processing results
            @SuppressWarnings("unchecked")
            Map<String, Object> processingResults = (Map<String, Object>) result.get("processingResults");
            
            @SuppressWarnings("unchecked")
            Map<String, Object> images = (Map<String, Object>) processingResults.get("images");
            if (images != null && (Boolean) images.get("success")) {
                Integer totalImages = (Integer) images.get("totalImages");
                System.out.println("📸 Extracted " + totalImages + " images:");
                
                @SuppressWarnings("unchecked")
                java.util.List<Map<String, Object>> imagesList = (java.util.List<Map<String, Object>>) images.get("images");
                if (imagesList != null) {
                    for (int i = 0; i < imagesList.size(); i++) {
                        Map<String, Object> imageInfo = imagesList.get(i);
                        System.out.println("   - Image " + (i + 1) + ": " + imageInfo.get("path"));
                    }
                }
                
                @SuppressWarnings("unchecked")
                Map<String, Object> studentPhoto = (Map<String, Object>) images.get("studentPhoto");
                if (studentPhoto != null) {
                    System.out.println("   - Student Photo: " + studentPhoto.get("path"));
                }
            }
            
            @SuppressWarnings("unchecked")
            Map<String, Object> text = (Map<String, Object>) processingResults.get("text");
            if (text != null && (Boolean) text.get("success")) {
                if (text.get("studentDetails") instanceof StudentDetails studentDetails) {
                    // Store for later use in report generation
                    this.extractedStudentDetails = studentDetails;
                    
                    System.out.println("👤 Student Details:");
                    System.out.println("   - Name: " + (studentDetails.getName() != null ? studentDetails.getName() : "Not found"));
                    System.out.println("   - Register Number: " + (studentDetails.getRegisterNumber() != null ? studentDetails.getRegisterNumber() : "Not found"));
                    System.out.println("   - Department: " + (studentDetails.getDepartment() != null ? studentDetails.getDepartment() : "Not found"));
                }
            }
            
            return savedPath;
            
        } catch (Exception e) {
            logger.error("Error processing ID card PDF: {}", e.getMessage());
            System.out.println("❌ Error processing PDF: " + e.getMessage());
            return null;
        }
    }

    /**
     * Perform face verification between student image and ID card
     */
    @SuppressWarnings("unused")
    private void performFaceVerification(String studentImagePath, String processedPdfPath) {
        try {
            System.out.println("🔄 Performing face verification...");
            System.out.println("📸 Student image: " + studentImagePath);
            
            // Find the extracted student photo from uploads folder
            File uploadsDir = new File("uploads");
            String idCardPhotoPath = null;
            
            if (uploadsDir.exists()) {
                File[] imageFiles = uploadsDir.listFiles((dir, name) -> 
                    name.toLowerCase().endsWith(".jpg") || name.toLowerCase().endsWith(".png"));
                
                if (imageFiles != null && imageFiles.length > 0) {
                    idCardPhotoPath = imageFiles[0].getPath();
                    System.out.println("� ID card photo: " + idCardPhotoPath);
                }
            }
            
            if (idCardPhotoPath == null) {
                System.out.println("⚠️ No ID card photo found in uploads folder");
                System.out.println("📄 Verification will be based on PDF processing only");
                return;
            }
            
            // Get student details from the processed PDF
            StudentDetails studentDetails = getStudentDetailsFromProcessing();
            
            // Perform verification (compare student image with ID card photo)
            VerificationResult verificationResult = faceVerificationService.verifyIdentity(
                studentImagePath, idCardPhotoPath, studentDetails);
            
            if (verificationResult.getMessage() != null && verificationResult.getMessage().contains("failed")) {
                System.out.println("❌ Verification failed: " + verificationResult.getMessage());
                return;
            }
            
            boolean isMatch = verificationResult.isMatch();
            double confidence = verificationResult.getConfidence();
            
            System.out.println("\n🎯 VERIFICATION RESULTS:");
            System.out.println("-".repeat(30));
            System.out.println("Student Image: " + (studentImagePath.contains("camera") ? "Camera Captured" : "Uploaded Photo"));
            System.out.println("ID Card Photo: Extracted from PDF");
            System.out.println("Result: " + (isMatch ? "✅ MATCH" : "❌ NO MATCH"));
            System.out.println("Confidence: " + String.format("%.1f%%", confidence));
            System.out.println("Method: " + verificationResult.getMethod());
            
            if (verificationResult.getRecommendation() != null) {
                System.out.println("Recommendation: " + verificationResult.getRecommendation());
            }
            
            // Generate PDF report with student name
            System.out.println("\n📄 Generating verification report...");
            Map<String, Object> reportResult = reportGenerationService.generateVerificationReport(
                verificationResult, studentDetails, studentImagePath, idCardPhotoPath);
            
            if ((Boolean) reportResult.get("success")) {
                String reportPath = (String) reportResult.get("reportPath");
                String studentName = (String) reportResult.get("studentName");
                System.out.println("✅ Verification report saved successfully!");
                System.out.println("📁 Report saved as: " + reportPath);
                System.out.println("👤 Student: " + studentName);
                
                // Also generate a simple text report
                Map<String, Object> textReportResult = reportGenerationService.generateTextReport(
                    verificationResult, studentDetails);
                
                if ((Boolean) textReportResult.get("success")) {
                    System.out.println("📄 Text report also saved: " + textReportResult.get("reportPath"));
                }
            } else {
                System.out.println("⚠️ Failed to generate report: " + reportResult.get("message"));
            }
            
        } catch (Exception e) {
            logger.error("Error in face verification: {}", e.getMessage());
            System.out.println("❌ Error in verification: " + e.getMessage());
        }
    }
    
    /**
     * Get student details from the last processing (stored in a field or retrieved from uploads)
     */
    private StudentDetails getStudentDetailsFromProcessing() {
        // Return the extracted student details from PDF processing
        if (extractedStudentDetails != null) {
            return extractedStudentDetails;
        }
        
        // Fallback: create a default StudentDetails if extraction failed
        StudentDetails details = new StudentDetails();
        details.setName("UNKNOWN_STUDENT");
        details.setRegisterNumber("N/A");
        details.setDepartment("N/A");
        details.setCollege("N/A");
        details.setCourse("N/A");
        details.setYear("N/A");
        
        return details;
    }
}