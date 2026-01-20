package com.college.project.controller;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.college.project.model.ApiResponse;
import com.college.project.model.StudentDetails;
import com.college.project.model.VerificationResult;
import com.college.project.service.FaceVerificationService;
import com.college.project.service.PDFService;

/**
 * Verification Controller for ID Card Processing and Face Verification
 * REST API endpoints for PDF upload, processing, and face verification
 */
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class VerificationController {

    private static final Logger logger = LoggerFactory.getLogger(VerificationController.class);

    @Autowired
    private PDFService pdfService;

    @Autowired
    private FaceVerificationService faceVerificationService;

    private static final String IDCARDS_FOLDER = "idcards";

    /**
     * Upload and process college ID card PDF
     * POST /api/upload-id-card
     */
    @PostMapping("/upload-id-card")
    public ResponseEntity<ApiResponse<Map<String, Object>>> uploadIdCard(
            @RequestParam("file") MultipartFile file) {
        try {
            logger.info("ID card upload requested");

            // Validate file
            if (file.isEmpty()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "No file selected", "NO_FILE_SELECTED"));
            }

            String originalFilename = file.getOriginalFilename();
            if (originalFilename == null || !originalFilename.toLowerCase().endsWith(".pdf")) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "Invalid file format. Only PDF files are allowed", 
                    "INVALID_FORMAT"));
            }

            // Create ID cards directory
            File idCardsDir = new File(IDCARDS_FOLDER);
            if (!idCardsDir.exists()) {
                idCardsDir.mkdirs();
            }

            // Save uploaded ID card file in idcards folder
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String filename = timestamp + "_" + originalFilename;
            String filePath = IDCARDS_FOLDER + File.separator + filename;

            File savedFile = new File(filePath);
            file.transferTo(savedFile);
            logger.info("ID card saved: {}", filePath);

            // Process the ID card PDF
            Map<String, Object> processingResult = pdfService.processIdCard(filePath);
            boolean success = (Boolean) processingResult.get("success");

            if (success) {
                Map<String, Object> data = new HashMap<>();
                data.put("fileInfo", Map.of(
                    "originalFilename", originalFilename,
                    "savedFilename", filename,
                    "filePath", filePath,
                    "uploadTimestamp", timestamp,
                    "fileSize", file.getSize()
                ));
                data.put("processingResults", processingResult);
                data.put("nextSteps", List.of(
                    "ID card data extracted successfully",
                    "Use /capture-face to capture live photo",
                    "Use /verify to compare faces"
                ));

                return ResponseEntity.ok(ApiResponse.success(
                    "ID card processed successfully", data));
            } else {
                // Clean up uploaded file if processing failed
                if (savedFile.exists()) {
                    savedFile.delete();
                }

                return ResponseEntity.badRequest().body(ApiResponse.error(
                    (String) processingResult.get("message"),
                    (String) processingResult.get("errorCode")));
            }

        } catch (IOException | SecurityException e) {
            logger.error("Error saving uploaded file: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "File upload failed: " + e.getMessage(),
                "UPLOAD_ERROR"));
        } catch (RuntimeException e) {
            logger.error("Unexpected error in upload_id_card endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "ID card upload failed: " + e.getMessage(),
                "UPLOAD_EXCEPTION"));
        }
    }
    /**
     * Verify identity by comparing live camera capture with ID card photo
     * POST /api/verify
     */
    @PostMapping("/verify")
    public ResponseEntity<ApiResponse<VerificationResult>> verifyIdentity(
            @RequestBody Map<String, Object> request) {
        try {
            logger.info("Identity verification requested");

            // Extract parameters
            String cameraImagePath = (String) request.get("cameraImagePath");
            String idCardImagePath = (String) request.get("idCardImagePath");
            @SuppressWarnings("unchecked")
            Map<String, Object> studentDetailsMap = (Map<String, Object>) request.get("studentDetails");

            // Validate required parameters
            if (cameraImagePath == null || cameraImagePath.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "cameraImagePath is required", "MISSING_CAMERA_IMAGE"));
            }

            if (idCardImagePath == null || idCardImagePath.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "idCardImagePath is required", "MISSING_ID_CARD_IMAGE"));
            }

            // Check if files exist
            if (!new File(cameraImagePath).exists()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "Camera image not found: " + cameraImagePath,
                    "CAMERA_IMAGE_NOT_FOUND"));
            }

            if (!new File(idCardImagePath).exists()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "ID card image not found: " + idCardImagePath,
                    "ID_CARD_IMAGE_NOT_FOUND"));
            }

            // Convert student details map to object
            StudentDetails studentDetails = mapToStudentDetails(studentDetailsMap);

            // Validate image quality
            Map<String, Object> cameraQuality = faceVerificationService.validateImageQuality(cameraImagePath);
            Map<String, Object> idCardQuality = faceVerificationService.validateImageQuality(idCardImagePath);

            if (!(Boolean) cameraQuality.get("valid") || !(Boolean) idCardQuality.get("valid")) {
                String message = "Image quality issues detected: ";
                if (!(Boolean) cameraQuality.get("valid")) {
                    message += "Camera image: " + cameraQuality.get("message") + ". ";
                }
                if (!(Boolean) idCardQuality.get("valid")) {
                    message += "ID card image: " + idCardQuality.get("message");
                }

                return ResponseEntity.badRequest().body(ApiResponse.error(
                    message, "POOR_IMAGE_QUALITY"));
            }

            // Perform identity verification
            VerificationResult verificationResult = faceVerificationService.verifyIdentity(
                cameraImagePath, idCardImagePath, studentDetails);

            return ResponseEntity.ok(ApiResponse.success(
                verificationResult.getMessage(), verificationResult));

        } catch (RuntimeException e) {
            logger.error("Error in verify_identity endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Identity verification failed: " + e.getMessage(),
                "VERIFICATION_EXCEPTION"));
        }
    }

    /**
     * Extract text from PDF
     * POST /api/extract-text
     */
    @PostMapping("/extract-text")
    public ResponseEntity<ApiResponse<Map<String, Object>>> extractText(
            @RequestBody Map<String, String> request) {
        try {
            logger.info("Text extraction requested");

            String filePath = request.get("filePath");
            if (filePath == null || filePath.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "filePath is required", "MISSING_FILE_PATH"));
            }

            if (!new File(filePath).exists()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "PDF file not found: " + filePath, "FILE_NOT_FOUND"));
            }

            Map<String, Object> result = pdfService.extractTextFromPDF(filePath);
            boolean success = (Boolean) result.get("success");

            if (success) {
                Map<String, Object> data = new HashMap<>();
                data.put("extractedText", result.get("text"));
                data.put("studentDetails", result.get("studentDetails"));
                data.put("textLength", result.get("textLength"));

                return ResponseEntity.ok(ApiResponse.success(
                    (String) result.get("message"), data));
            } else {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    (String) result.get("message"),
                    (String) result.get("errorCode")));
            }

        } catch (RuntimeException e) {
            logger.error("Error in extract_text endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Text extraction failed: " + e.getMessage(),
                "TEXT_EXTRACTION_EXCEPTION"));
        }
    }

    /**
     * Extract images from PDF
     * POST /api/extract-images
     */
    @PostMapping("/extract-images")
    public ResponseEntity<ApiResponse<Map<String, Object>>> extractImages(
            @RequestBody Map<String, String> request) {
        try {
            logger.info("Image extraction requested");

            String filePath = request.get("filePath");
            if (filePath == null || filePath.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "filePath is required", "MISSING_FILE_PATH"));
            }

            if (!new File(filePath).exists()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "PDF file not found: " + filePath, "FILE_NOT_FOUND"));
            }

            Map<String, Object> result = pdfService.extractImagesFromPDF(filePath);
            boolean success = (Boolean) result.get("success");

            if (success) {
                Map<String, Object> data = new HashMap<>();
                data.put("totalImages", result.get("totalImages"));
                data.put("images", result.get("images"));
                data.put("studentPhoto", result.get("studentPhoto"));

                return ResponseEntity.ok(ApiResponse.success(
                    (String) result.get("message"), data));
            } else {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    (String) result.get("message"),
                    (String) result.get("errorCode")));
            }

        } catch (RuntimeException e) {
            logger.error("Error in extract_images endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Image extraction failed: " + e.getMessage(),
                "IMAGE_EXTRACTION_EXCEPTION"));
        }
    }

    /**
     * Compare two face images
     * POST /api/compare-faces
     */
    @PostMapping("/compare-faces")
    public ResponseEntity<ApiResponse<VerificationResult>> compareFaces(
            @RequestBody Map<String, String> request) {
        try {
            logger.info("Face comparison requested");

            String image1Path = request.get("image1Path");
            String image2Path = request.get("image2Path");

            if (image1Path == null || image2Path == null) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "Both image1Path and image2Path are required",
                    "MISSING_IMAGE_PATHS"));
            }

            if (!new File(image1Path).exists()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "First image not found: " + image1Path,
                    "IMAGE1_NOT_FOUND"));
            }

            if (!new File(image2Path).exists()) {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    "Second image not found: " + image2Path,
                    "IMAGE2_NOT_FOUND"));
            }

            VerificationResult result = faceVerificationService.compareFaces(image1Path, image2Path);

            return ResponseEntity.ok(ApiResponse.success(
                result.getMessage(), result));

        } catch (RuntimeException e) {
            logger.error("Error in compare_faces endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Face comparison failed: " + e.getMessage(),
                "COMPARISON_EXCEPTION"));
        }
    }

    /**
     * Convert Map to StudentDetails object
     */
    private StudentDetails mapToStudentDetails(Map<String, Object> map) {
        if (map == null) {
            return new StudentDetails();
        }

        StudentDetails details = new StudentDetails();
        details.setName((String) map.get("name"));
        details.setRegisterNumber((String) map.get("registerNumber"));
        details.setRollNumber((String) map.get("rollNumber"));
        details.setDepartment((String) map.get("department"));
        details.setCollege((String) map.get("college"));
        details.setYear((String) map.get("year"));
        details.setCourse((String) map.get("course"));
        details.setBatch((String) map.get("batch"));
        details.setSection((String) map.get("section"));

        return details;
    }
}