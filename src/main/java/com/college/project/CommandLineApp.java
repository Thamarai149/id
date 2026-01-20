package com.college.project;

import java.io.File;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

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

    @Override
    public void run(String... args) throws Exception {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("🎓 FACE CAPTURE AND ID CARD PROCESSING SYSTEM");
        System.out.println("=".repeat(60));

        Scanner scanner = new Scanner(System.in);

        try {
            // Step 1: Capture Face
            System.out.println("\n📷 STEP 1: CAPTURING YOUR FACE");
            System.out.println("-".repeat(40));
            System.out.print("Press Enter to capture your face from camera...");
            scanner.nextLine();

            String capturedImagePath = captureFaceFromCamera();
            if (capturedImagePath == null) {
                System.out.println("❌ Failed to capture face. Exiting...");
                return;
            }

            // Step 2: Process ID Card PDF
            System.out.println("\n📄 STEP 2: PROCESSING ID CARD PDF");
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
            performFaceVerification(capturedImagePath, processedPdfPath);

            System.out.println("\n✅ PROCESS COMPLETED SUCCESSFULLY!");
            System.out.println("📁 Check the following folders for results:");
            System.out.println("   - camera/ (captured face images)");
            System.out.println("   - idcards/ (processed ID card PDF)");
            System.out.println("   - uploads/ (extracted images from PDF)");

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
     * Perform face verification between captured image and ID card
     */
    @SuppressWarnings("unused")
    private void performFaceVerification(String capturedImagePath, String processedPdfPath) {
        try {
            System.out.println("🔄 Performing face verification...");
            
            // Find the extracted student photo from uploads folder
            File uploadsDir = new File("uploads");
            String studentPhotoPath = null;
            
            if (uploadsDir.exists()) {
                File[] imageFiles = uploadsDir.listFiles((dir, name) -> 
                    name.toLowerCase().endsWith(".jpg") || name.toLowerCase().endsWith(".png"));
                
                if (imageFiles != null && imageFiles.length > 0) {
                    studentPhotoPath = imageFiles[0].getPath();
                    System.out.println("📸 Found student photo: " + studentPhotoPath);
                }
            }
            
            if (studentPhotoPath == null) {
                System.out.println("⚠️ No student photo found in uploads folder");
                System.out.println("📄 Verification will be based on PDF processing only");
                return;
            }
            
            // Perform verification
            VerificationResult verificationResult = faceVerificationService.verifyIdentity(
                capturedImagePath, studentPhotoPath, new StudentDetails());
            
            if (verificationResult.getMessage() != null && verificationResult.getMessage().contains("failed")) {
                System.out.println("❌ Verification failed: " + verificationResult.getMessage());
                return;
            }
            
            boolean isMatch = verificationResult.isMatch();
            double confidence = verificationResult.getConfidence();
            
            System.out.println("\n🎯 VERIFICATION RESULTS:");
            System.out.println("-".repeat(30));
            System.out.println("Result: " + (isMatch ? "✅ MATCH" : "❌ NO MATCH"));
            System.out.println("Confidence: " + String.format("%.1f%%", confidence));
            System.out.println("Method: " + verificationResult.getMethod());
            
            if (verificationResult.getRecommendation() != null) {
                System.out.println("Recommendation: " + verificationResult.getRecommendation());
            }
            
        } catch (Exception e) {
            logger.error("Error in face verification: {}", e.getMessage());
            System.out.println("❌ Error in verification: " + e.getMessage());
        }
    }
}