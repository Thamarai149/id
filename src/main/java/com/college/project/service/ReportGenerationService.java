package com.college.project.service;

import com.college.project.model.StudentDetails;
import com.college.project.model.VerificationResult;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.font.PDType1Font;
import org.apache.pdfbox.pdmodel.graphics.image.PDImageXObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

/**
 * Report Generation Service
 * Creates PDF reports for face verification results
 */
@Service
public class ReportGenerationService {

    private static final Logger logger = LoggerFactory.getLogger(ReportGenerationService.class);
    private static final String REPORTS_FOLDER = "reports";

    public ReportGenerationService() {
        createReportsDirectory();
    }

    /**
     * Create reports directory if it doesn't exist
     */
    private void createReportsDirectory() {
        File reportsDir = new File(REPORTS_FOLDER);
        if (!reportsDir.exists()) {
            boolean created = reportsDir.mkdirs();
            if (created) {
                logger.info("📁 Created reports directory: {}", REPORTS_FOLDER);
            }
        }
    }

    /**
     * Generate verification report PDF
     */
    public Map<String, Object> generateVerificationReport(
            VerificationResult verificationResult,
            StudentDetails studentDetails,
            String capturedImagePath,
            String idCardImagePath) {
        
        Map<String, Object> result = new HashMap<>();
        
        try {
            // Generate filename based on student name
            String studentName = studentDetails.getName() != null ? 
                studentDetails.getName().replaceAll("[^a-zA-Z0-9]", "_").toUpperCase() : 
                "UNKNOWN_STUDENT";
            
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String filename = studentName + "_verification_" + timestamp + ".pdf";
            String reportPath = REPORTS_FOLDER + File.separator + filename;

            // Create PDF document
            try (PDDocument document = new PDDocument()) {
                PDPage page = new PDPage(PDRectangle.A4);
                document.addPage(page);

                try (PDPageContentStream contentStream = new PDPageContentStream(document, page)) {
                    
                    // Title
                    contentStream.beginText();
                    contentStream.setFont(PDType1Font.HELVETICA_BOLD, 20);
                    contentStream.newLineAtOffset(50, 750);
                    contentStream.showText("FACE VERIFICATION REPORT");
                    contentStream.endText();

                    // Verification Status
                    contentStream.beginText();
                    contentStream.setFont(PDType1Font.HELVETICA_BOLD, 16);
                    contentStream.newLineAtOffset(50, 700);
                    String status = verificationResult.isMatch() ? "VERIFICATION SUCCESSFUL" : "VERIFICATION FAILED";
                    contentStream.showText("Status: " + status);
                    contentStream.endText();

                    // Student Details Section
                    contentStream.beginText();
                    contentStream.setFont(PDType1Font.HELVETICA_BOLD, 14);
                    contentStream.newLineAtOffset(50, 650);
                    contentStream.showText("STUDENT DETAILS:");
                    contentStream.endText();

                    float yPosition = 620;
                    contentStream.setFont(PDType1Font.HELVETICA, 12);
                    
                    // Student information
                    String[][] studentInfo = {
                        {"Name:", studentDetails.getName() != null ? studentDetails.getName() : "Not Available"},
                        {"Register Number:", studentDetails.getRegisterNumber() != null ? studentDetails.getRegisterNumber() : "Not Available"},
                        {"Department:", studentDetails.getDepartment() != null ? studentDetails.getDepartment() : "Not Available"},
                        {"College:", studentDetails.getCollege() != null ? studentDetails.getCollege() : "Not Available"},
                        {"Course:", studentDetails.getCourse() != null ? studentDetails.getCourse() : "Not Available"},
                        {"Year:", studentDetails.getYear() != null ? studentDetails.getYear() : "Not Available"}
                    };

                    for (String[] info : studentInfo) {
                        contentStream.beginText();
                        contentStream.newLineAtOffset(70, yPosition);
                        contentStream.showText(info[0] + " " + info[1]);
                        contentStream.endText();
                        yPosition -= 20;
                    }

                    // Verification Results Section
                    yPosition -= 20;
                    contentStream.beginText();
                    contentStream.setFont(PDType1Font.HELVETICA_BOLD, 14);
                    contentStream.newLineAtOffset(50, yPosition);
                    contentStream.showText("VERIFICATION RESULTS:");
                    contentStream.endText();

                    yPosition -= 30;
                    contentStream.setFont(PDType1Font.HELVETICA, 12);
                    
                    String[][] verificationInfo = {
                        {"Result:", verificationResult.getResult()},
                        {"Match Status:", verificationResult.isMatch() ? "MATCH" : "NO MATCH"},
                        {"Confidence:", String.format("%.1f%%", verificationResult.getConfidence())},
                        {"Method:", verificationResult.getMethod() != null ? verificationResult.getMethod() : "Java Image Processing"},
                        {"Timestamp:", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))}
                    };

                    for (String[] info : verificationInfo) {
                        contentStream.beginText();
                        contentStream.newLineAtOffset(70, yPosition);
                        contentStream.showText(info[0] + " " + info[1]);
                        contentStream.endText();
                        yPosition -= 20;
                    }

                    // Recommendation
                    if (verificationResult.getRecommendation() != null) {
                        yPosition -= 10;
                        contentStream.beginText();
                        contentStream.setFont(PDType1Font.HELVETICA_BOLD, 12);
                        contentStream.newLineAtOffset(70, yPosition);
                        contentStream.showText("Recommendation:");
                        contentStream.endText();
                        
                        yPosition -= 20;
                        contentStream.beginText();
                        contentStream.setFont(PDType1Font.HELVETICA, 11);
                        contentStream.newLineAtOffset(70, yPosition);
                        contentStream.showText(verificationResult.getRecommendation());
                        contentStream.endText();
                    }

                    // Add images if available
                    yPosition -= 40;
                    if (capturedImagePath != null && new File(capturedImagePath).exists()) {
                        try {
                            contentStream.beginText();
                            contentStream.setFont(PDType1Font.HELVETICA_BOLD, 12);
                            contentStream.newLineAtOffset(50, yPosition);
                            contentStream.showText("CAPTURED FACE:");
                            contentStream.endText();
                            
                            PDImageXObject capturedImage = PDImageXObject.createFromFile(capturedImagePath, document);
                            float imageWidth = 150;
                            float imageHeight = 150;
                            contentStream.drawImage(capturedImage, 70, yPosition - imageHeight - 10, imageWidth, imageHeight);
                            
                        } catch (IOException e) {
                            logger.warn("Could not add captured image to PDF: {}", e.getMessage());
                        }
                    }

                    // Footer
                    contentStream.beginText();
                    contentStream.setFont(PDType1Font.HELVETICA, 10);
                    contentStream.newLineAtOffset(50, 50);
                    contentStream.showText("Generated by Face Verification System - " + 
                        LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
                    contentStream.endText();
                }

                // Save the document
                document.save(reportPath);
                logger.info("✅ Verification report saved: {}", reportPath);

                result.put("success", true);
                result.put("message", "Verification report generated successfully");
                result.put("reportPath", reportPath);
                result.put("filename", filename);
                result.put("studentName", studentName);

            }

        } catch (IOException e) {
            logger.error("Error generating verification report: {}", e.getMessage());
            result.put("success", false);
            result.put("message", "Failed to generate verification report: " + e.getMessage());
            result.put("errorCode", "REPORT_GENERATION_ERROR");
        }

        return result;
    }

    /**
     * Generate simple text-based report
     */
    public Map<String, Object> generateTextReport(
            VerificationResult verificationResult,
            StudentDetails studentDetails) {
        
        Map<String, Object> result = new HashMap<>();
        
        try {
            String studentName = studentDetails.getName() != null ? 
                studentDetails.getName().replaceAll("[^a-zA-Z0-9]", "_").toUpperCase() : 
                "UNKNOWN_STUDENT";
            
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String filename = studentName + "_report_" + timestamp + ".txt";
            String reportPath = REPORTS_FOLDER + File.separator + filename;

            StringBuilder report = new StringBuilder();
            report.append("=".repeat(60)).append("\n");
            report.append("FACE VERIFICATION REPORT\n");
            report.append("=".repeat(60)).append("\n\n");
            
            report.append("STUDENT DETAILS:\n");
            report.append("-".repeat(30)).append("\n");
            report.append("Name: ").append(studentDetails.getName() != null ? studentDetails.getName() : "Not Available").append("\n");
            report.append("Register Number: ").append(studentDetails.getRegisterNumber() != null ? studentDetails.getRegisterNumber() : "Not Available").append("\n");
            report.append("Department: ").append(studentDetails.getDepartment() != null ? studentDetails.getDepartment() : "Not Available").append("\n");
            report.append("College: ").append(studentDetails.getCollege() != null ? studentDetails.getCollege() : "Not Available").append("\n");
            report.append("Course: ").append(studentDetails.getCourse() != null ? studentDetails.getCourse() : "Not Available").append("\n");
            report.append("Year: ").append(studentDetails.getYear() != null ? studentDetails.getYear() : "Not Available").append("\n\n");
            
            report.append("VERIFICATION RESULTS:\n");
            report.append("-".repeat(30)).append("\n");
            report.append("Status: ").append(verificationResult.isMatch() ? "VERIFICATION SUCCESSFUL" : "VERIFICATION FAILED").append("\n");
            report.append("Result: ").append(verificationResult.getResult()).append("\n");
            report.append("Match: ").append(verificationResult.isMatch() ? "YES" : "NO").append("\n");
            report.append("Confidence: ").append(String.format("%.1f%%", verificationResult.getConfidence())).append("\n");
            report.append("Method: ").append(verificationResult.getMethod() != null ? verificationResult.getMethod() : "Java Image Processing").append("\n");
            report.append("Timestamp: ").append(LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))).append("\n");
            
            if (verificationResult.getRecommendation() != null) {
                report.append("Recommendation: ").append(verificationResult.getRecommendation()).append("\n");
            }
            
            report.append("\n").append("=".repeat(60)).append("\n");
            report.append("Generated by Face Verification System\n");

            // Write to file
            java.nio.file.Files.write(java.nio.file.Paths.get(reportPath), report.toString().getBytes());
            
            result.put("success", true);
            result.put("message", "Text report generated successfully");
            result.put("reportPath", reportPath);
            result.put("filename", filename);
            result.put("studentName", studentName);

        } catch (IOException e) {
            logger.error("Error generating text report: {}", e.getMessage());
            result.put("success", false);
            result.put("message", "Failed to generate text report: " + e.getMessage());
            result.put("errorCode", "TEXT_REPORT_ERROR");
        }

        return result;
    }
}