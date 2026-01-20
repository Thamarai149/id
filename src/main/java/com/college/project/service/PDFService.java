package com.college.project.service;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.imageio.ImageIO;

import org.apache.pdfbox.cos.COSName;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDResources;
import org.apache.pdfbox.pdmodel.graphics.PDXObject;
import org.apache.pdfbox.pdmodel.graphics.image.PDImageXObject;
import org.apache.pdfbox.text.PDFTextStripper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.college.project.model.StudentDetails;

/**
 * PDF Service for ID Card Processing
 * Handles PDF upload, text extraction, and image extraction from college ID cards using Java
 */
@Service
public class PDFService {

    private static final Logger logger = LoggerFactory.getLogger(PDFService.class);
    
    private static final String UPLOAD_FOLDER = "uploads";
    private static final String IDCARDS_FOLDER = "idcards";

    public PDFService() {
        createUploadDirectory();
        createIdCardsDirectory();
    }

    /**
     * Create upload directory if it doesn't exist
     */
    private void createUploadDirectory() {
        File uploadDir = new File(UPLOAD_FOLDER);
        if (!uploadDir.exists()) {
            boolean created = uploadDir.mkdirs();
            if (created) {
                logger.info("📁 Created upload directory: {}", UPLOAD_FOLDER);
            }
        }
    }

    /**
     * Create ID cards directory if it doesn't exist
     */
    private void createIdCardsDirectory() {
        File idCardsDir = new File(IDCARDS_FOLDER);
        if (!idCardsDir.exists()) {
            boolean created = idCardsDir.mkdirs();
            if (created) {
                logger.info("📁 Created ID cards directory: {}", IDCARDS_FOLDER);
            }
        }
    }

    /**
     * Validate PDF file
     */
    public Map<String, Object> validatePDF(String filePath) {
        Map<String, Object> result = new HashMap<>();
        
        try {
            File file = new File(filePath);
            
            if (!file.exists()) {
                result.put("valid", false);
                result.put("message", "File does not exist");
                result.put("errorCode", "FILE_NOT_FOUND");
                return result;
            }

            // Check file extension
            String fileName = file.getName().toLowerCase();
            if (!fileName.endsWith(".pdf")) {
                result.put("valid", false);
                result.put("message", "Invalid file format. Only PDF files are allowed");
                result.put("errorCode", "INVALID_FORMAT");
                return result;
            }

            // Try to open PDF with PDFBox
            try (PDDocument document = PDDocument.load(file)) {
                int pageCount = document.getNumberOfPages();
                
                if (pageCount == 0) {
                    result.put("valid", false);
                    result.put("message", "PDF file is empty");
                    result.put("errorCode", "EMPTY_PDF");
                    return result;
                }

                result.put("valid", true);
                result.put("message", "Valid PDF file");
                result.put("pageCount", pageCount);
                
            } catch (IOException e) {
                result.put("valid", false);
                result.put("message", "Corrupted or invalid PDF file: " + e.getMessage());
                result.put("errorCode", "CORRUPTED_PDF");
                return result;
            }

        } catch (SecurityException e) {
            logger.error("Security error validating PDF: {}", e.getMessage());
            result.put("valid", false);
            result.put("message", "PDF validation failed: " + e.getMessage());
            result.put("errorCode", "VALIDATION_ERROR");
        } catch (RuntimeException e) {
            logger.error("Runtime error validating PDF: {}", e.getMessage());
            result.put("valid", false);
            result.put("message", "PDF validation failed: " + e.getMessage());
            result.put("errorCode", "VALIDATION_ERROR");
        }

        return result;
    }

    /**
     * Extract images from PDF file
     */
    public Map<String, Object> extractImagesFromPDF(String filePath) {
        Map<String, Object> result = new HashMap<>();
        
        // Validate PDF first
        Map<String, Object> validation = validatePDF(filePath);
        if (!(Boolean) validation.get("valid")) {
            return validation;
        }

        try (PDDocument document = PDDocument.load(new File(filePath))) {
            List<Map<String, Object>> extractedImages = new ArrayList<>();
            
            for (int pageNum = 0; pageNum < document.getNumberOfPages(); pageNum++) {
                PDPage page = document.getPage(pageNum);
                PDResources resources = page.getResources();
                
                for (COSName name : resources.getXObjectNames()) {
                    PDXObject xObject = resources.getXObject(name);
                    
                    if (xObject instanceof PDImageXObject imageXObject) {
                        
                        // Skip small images (likely not photos)
                        if (imageXObject.getWidth() < 50 || imageXObject.getHeight() < 50) {
                            continue;
                        }

                        // Extract and save image
                        BufferedImage bufferedImage = imageXObject.getImage();
                        String imageFileName = String.format("extracted_image_p%d_%s.png", 
                                                            pageNum + 1, name.getName());
                        String imagePath = UPLOAD_FOLDER + File.separator + imageFileName;
                        
                        File imageFile = new File(imagePath);
                        ImageIO.write(bufferedImage, "PNG", imageFile);

                        Map<String, Object> imageInfo = new HashMap<>();
                        imageInfo.put("filename", imageFileName);
                        imageInfo.put("path", imagePath);
                        imageInfo.put("page", pageNum + 1);
                        imageInfo.put("width", imageXObject.getWidth());
                        imageInfo.put("height", imageXObject.getHeight());
                        imageInfo.put("sizeBytes", imageFile.length());

                        extractedImages.add(imageInfo);
                        
                        logger.info("✅ Extracted image: {} ({}x{})", 
                                  imageFileName, imageXObject.getWidth(), imageXObject.getHeight());
                    }
                }
            }

            if (extractedImages.isEmpty()) {
                result.put("success", false);
                result.put("message", "No images found in the PDF file");
                result.put("errorCode", "NO_IMAGES_FOUND");
                return result;
            }

            // Find the largest image (likely to be the student photo)
            Map<String, Object> studentPhoto = extractedImages.stream()
                    .max(Comparator.comparingInt(img -> 
                            (Integer) img.get("width") * (Integer) img.get("height")))
                    .orElse(null);

            result.put("success", true);
            result.put("message", String.format("Successfully extracted %d images", extractedImages.size()));
            result.put("images", extractedImages);
            result.put("totalImages", extractedImages.size());
            result.put("studentPhoto", studentPhoto);

            logger.info("✅ Extracted {} images from PDF", extractedImages.size());

        } catch (IOException e) {
            logger.error("Error extracting images from PDF: {}", e.getMessage());
            result.put("success", false);
            result.put("message", "Image extraction failed: " + e.getMessage());
            result.put("errorCode", "EXTRACTION_ERROR");
        }

        return result;
    }

    /**
     * Extract text content from PDF file
     */
    public Map<String, Object> extractTextFromPDF(String filePath) {
        Map<String, Object> result = new HashMap<>();
        
        // Validate PDF first
        Map<String, Object> validation = validatePDF(filePath);
        if (!(Boolean) validation.get("valid")) {
            return validation;
        }

        try (PDDocument document = PDDocument.load(new File(filePath))) {
            PDFTextStripper textStripper = new PDFTextStripper();
            String extractedText = textStripper.getText(document);

            if (extractedText == null || extractedText.trim().isEmpty()) {
                result.put("success", false);
                result.put("message", "No text content found in the PDF");
                result.put("errorCode", "NO_TEXT_FOUND");
                return result;
            }

            // Parse student details from extracted text
            StudentDetails studentDetails = parseStudentDetails(extractedText);

            result.put("success", true);
            result.put("message", "Text extracted successfully");
            result.put("text", extractedText.trim());
            result.put("studentDetails", studentDetails);
            result.put("textLength", extractedText.trim().length());

            logger.info("✅ Text extraction completed successfully");

        } catch (IOException e) {
            logger.error("Error extracting text from PDF: {}", e.getMessage());
            result.put("success", false);
            result.put("message", "Text extraction failed: " + e.getMessage());
            result.put("errorCode", "TEXT_EXTRACTION_ERROR");
        }

        return result;
    }

    /**
     * Parse student details from extracted text using regex patterns
     */
    private StudentDetails parseStudentDetails(String text) {
        StudentDetails details = new StudentDetails();
        
        try {
            // Clean text for better parsing
            String cleanText = text.replaceAll("\\s+", " ").trim();

            // Define regex patterns for different fields
            Map<String, List<String>> patterns = new HashMap<>();
            
            patterns.put("name", Arrays.asList(
                "Name\\s*:?\\s*([A-Za-z\\s\\.]+?)(?:\\n|Register|Roll|Department|$)",
                "Student\\s*Name\\s*:?\\s*([A-Za-z\\s\\.]+?)(?:\\n|Register|Roll|Department|$)",
                "Name\\s*-\\s*([A-Za-z\\s\\.]+?)(?:\\n|Register|Roll|Department|$)"
            ));
            
            patterns.put("registerNumber", Arrays.asList(
                "Register\\s*(?:No|Number|#)\\s*:?\\s*([A-Za-z0-9]+)",
                "Registration\\s*(?:No|Number|#)\\s*:?\\s*([A-Za-z0-9]+)",
                "Reg\\s*(?:No|#)\\s*:?\\s*([A-Za-z0-9]+)"
            ));
            
            patterns.put("rollNumber", Arrays.asList(
                "Roll\\s*(?:No|Number|#)\\s*:?\\s*([A-Za-z0-9]+)",
                "Roll\\s*:?\\s*([A-Za-z0-9]+)"
            ));
            
            patterns.put("department", Arrays.asList(
                "Department\\s*:?\\s*([A-Za-z\\s&]+?)(?:\\n|Year|Course|College|$)",
                "Dept\\s*:?\\s*([A-Za-z\\s&]+?)(?:\\n|Year|Course|College|$)",
                "Branch\\s*:?\\s*([A-Za-z\\s&]+?)(?:\\n|Year|Course|College|$)"
            ));
            
            patterns.put("college", Arrays.asList(
                "College\\s*:?\\s*([A-Za-z\\s,\\.]+?)(?:\\n|University|$)",
                "Institution\\s*:?\\s*([A-Za-z\\s,\\.]+?)(?:\\n|University|$)"
            ));
            
            patterns.put("year", Arrays.asList(
                "Year\\s*:?\\s*([0-9]+)",
                "([1-4])\\s*(?:st|nd|rd|th)\\s*Year",
                "Semester\\s*:?\\s*([0-9]+)"
            ));
            
            patterns.put("course", Arrays.asList(
                "Course\\s*:?\\s*([A-Za-z\\s\\.]+?)(?:\\n|Year|Department|$)",
                "Program\\s*:?\\s*([A-Za-z\\s\\.]+?)(?:\\n|Year|Department|$)",
                "Degree\\s*:?\\s*([A-Za-z\\s\\.]+?)(?:\\n|Year|Department|$)"
            ));

            // Extract information using patterns
            for (Map.Entry<String, List<String>> entry : patterns.entrySet()) {
                String field = entry.getKey();
                List<String> fieldPatterns = entry.getValue();
                
                for (String patternStr : fieldPatterns) {
                    Pattern pattern = Pattern.compile(patternStr, Pattern.CASE_INSENSITIVE);
                    Matcher matcher = pattern.matcher(cleanText);
                    
                    if (matcher.find()) {
                        String value = matcher.group(1).trim();
                        if (value.length() > 1) { // Avoid single characters
                            setStudentDetailField(details, field, cleanValue(value));
                            break;
                        }
                    }
                }
            }

        } catch (RuntimeException e) {
            logger.error("Error parsing student details: {}", e.getMessage());
        }

        return details;
    }

    /**
     * Set field value in StudentDetails object
     */
    private void setStudentDetailField(StudentDetails details, String field, String value) {
        switch (field) {
            case "name" -> details.setName(value);
            case "registerNumber" -> details.setRegisterNumber(value);
            case "rollNumber" -> details.setRollNumber(value);
            case "department" -> details.setDepartment(value);
            case "college" -> details.setCollege(value);
            case "year" -> details.setYear(value);
            case "course" -> details.setCourse(value);
        }
    }

    /**
     * Clean extracted value
     */
    private String cleanValue(String value) {
        return value.replaceAll("\\s+", " ").trim().replaceAll("[.,;:]+$", "");
    }

    /**
     * Complete processing of ID card PDF - extract both images and text
     */
    public Map<String, Object> processIdCard(String filePath) {
        Map<String, Object> result = new HashMap<>();
        
        try {
            logger.info("Processing ID card PDF: {}", filePath);

            // Extract text
            Map<String, Object> textResult = extractTextFromPDF(filePath);
            
            // Extract images
            Map<String, Object> imageResult = extractImagesFromPDF(filePath);

            // Combine results
            Map<String, Object> images = new HashMap<>();
            images.put("success", imageResult.get("success"));
            images.put("totalImages", imageResult.getOrDefault("totalImages", 0));
            images.put("images", imageResult.getOrDefault("images", new ArrayList<>()));
            images.put("studentPhoto", imageResult.get("studentPhoto"));

            Map<String, Object> text = new HashMap<>();
            text.put("success", textResult.get("success"));
            text.put("extractedText", textResult.getOrDefault("text", ""));
            text.put("studentDetails", textResult.getOrDefault("studentDetails", new StudentDetails()));

            result.put("success", true);
            result.put("message", "ID card processed successfully");
            result.put("images", images);
            result.put("text", text);

            // Check if we have minimum required data (text extraction should work)
            if (!(Boolean) textResult.get("success")) {
                result.put("success", false);
                result.put("message", "Failed to extract text from ID card");
                result.put("errorCode", "TEXT_EXTRACTION_FAILED");
            }

        } catch (RuntimeException e) {
            logger.error("Error processing ID card: {}", e.getMessage());
            result.put("success", false);
            result.put("message", "ID card processing failed: " + e.getMessage());
            result.put("errorCode", "PROCESSING_ERROR");
        }

        return result;
    }
}