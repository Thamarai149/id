package com.college.project;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.MultipartConfigFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.util.unit.DataSize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import jakarta.servlet.MultipartConfigElement;
import java.util.HashMap;
import java.util.Map;

/**
 * Live Face Detection and College ID Card Verification System
 * Main Spring Boot Application Class
 * 
 * @author AI/ML Full Stack Engineer
 * @version 1.0.0
 * @since 2026-01-20
 */
@SpringBootApplication
@RestController
public class FaceVerificationApplication {

    public static void main(String[] args) {
        System.out.println("🚀 Starting Live Face Detection and ID Card Verification System...");
        System.out.println("📷 Make sure your camera is connected and working");
        System.out.println("🌐 Server will be available at: http://localhost:8080");
        System.out.println("📖 API Documentation available at: http://localhost:8080");
        
        SpringApplication.run(FaceVerificationApplication.class, args);
        
        System.out.println("✅ Face Verification System started successfully!");
        System.out.println("🎓 College Final Year Project - Java Implementation");
    }

    /**
     * Configure multipart file upload
     */
    @Bean
    public MultipartConfigElement multipartConfigElement() {
        MultipartConfigFactory factory = new MultipartConfigFactory();
        factory.setMaxFileSize(DataSize.ofMegabytes(16));
        factory.setMaxRequestSize(DataSize.ofMegabytes(16));
        return factory.createMultipartConfig();
    }

    /**
     * API Documentation endpoint
     */
    @GetMapping("/")
    public Map<String, Object> getApiDocumentation() {
        Map<String, Object> docs = new HashMap<>();
        docs.put("title", "Live Face Detection and College ID Card Verification System");
        docs.put("version", "1.0.0");
        docs.put("description", "Java-based Face Verification System for College Final Year Project");
        docs.put("technology", "Spring Boot + OpenCV + Apache PDFBox");
        
        Map<String, String> endpoints = new HashMap<>();
        endpoints.put("POST /api/start-camera", "Initialize camera for face capture");
        endpoints.put("POST /api/capture-face", "Capture face from camera");
        endpoints.put("GET /api/camera-status", "Get camera status");
        endpoints.put("POST /api/test-camera", "Test camera functionality");
        endpoints.put("POST /api/upload-id-card", "Upload and process ID card PDF");
        endpoints.put("POST /api/verify", "Verify identity by comparing faces");
        endpoints.put("POST /api/compare-faces", "Compare two face images");
        endpoints.put("POST /api/extract-text", "Extract text from PDF");
        endpoints.put("POST /api/extract-images", "Extract images from PDF");
        endpoints.put("GET /health", "System health check");
        
        docs.put("endpoints", endpoints);
        docs.put("status", "operational");
        docs.put("author", "AI/ML Full Stack Engineer");
        
        return docs;
    }

    /**
     * Health check endpoint
     */
    @GetMapping("/health")
    public Map<String, Object> healthCheck() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("service", "Face Verification System");
        health.put("version", "1.0.0");
        health.put("timestamp", java.time.LocalDateTime.now().toString());
        return health;
    }

    /**
     * System information endpoint
     */
    @GetMapping("/api/info")
    public Map<String, Object> getSystemInfo() {
        Map<String, Object> info = new HashMap<>();
        info.put("systemName", "Live Face Detection and College ID Card Verification System");
        info.put("version", "1.0.0");
        info.put("framework", "Spring Boot 3.2.1");
        info.put("javaVersion", System.getProperty("java.version"));
        info.put("libraries", Map.of(
            "opencv", "4.8.0",
            "pdfbox", "3.0.1",
            "webcam-capture", "0.3.12",
            "javacv", "1.5.9"
        ));
        info.put("features", new String[]{
            "Live Camera Face Capture",
            "PDF ID Card Processing", 
            "Face Recognition & Verification",
            "Student Details Extraction",
            "REST API Interface"
        });
        return info;
    }
}