package com.college.project.controller;

import com.college.project.model.ApiResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * Main Controller for API Documentation and Health Checks
 * Provides system information and API documentation endpoints
 */
@RestController
@CrossOrigin(origins = "*")
public class MainController {

    @Value("${spring.application.name:Face Verification System}")
    private String applicationName;

    /**
     * Root endpoint with API documentation
     * GET /
     */
    @GetMapping("/")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getApiDocumentation() {
        Map<String, Object> apiInfo = new HashMap<>();
        apiInfo.put("message", "Live Face Detection and College ID Card Verification System");
        apiInfo.put("version", "1.0.0");
        apiInfo.put("language", "Java");
        apiInfo.put("framework", "Spring Boot");
        apiInfo.put("status", "active");

        Map<String, String> endpoints = new HashMap<>();
        endpoints.put("POST /api/start-camera", "Initialize camera for face capture");
        endpoints.put("POST /api/capture-face", "Capture face from live camera");
        endpoints.put("GET /api/camera-status", "Get camera status information");
        endpoints.put("POST /api/upload-id-card", "Upload college ID card PDF");
        endpoints.put("POST /api/verify", "Verify face against ID card");
        endpoints.put("POST /api/extract-text", "Extract text from PDF");
        endpoints.put("POST /api/extract-images", "Extract images from PDF");
        endpoints.put("POST /api/compare-faces", "Compare two face images");
        endpoints.put("GET /health", "System health check");

        apiInfo.put("endpoints", endpoints);

        Map<String, String> features = new HashMap<>();
        features.put("Live Camera Integration", "Real-time face capture using Java");
        features.put("PDF Processing", "Extract text and images from ID cards");
        features.put("Face Recognition", "Compare faces using OpenCV");
        features.put("RESTful API", "Professional Spring Boot backend");
        features.put("Error Handling", "Comprehensive validation and error management");

        apiInfo.put("features", features);

        return ResponseEntity.ok(ApiResponse.success(
            "API Documentation - Java Face Verification System", apiInfo));
    }

    /**
     * Health check endpoint
     * GET /health
     */
    @GetMapping("/health")
    public ResponseEntity<ApiResponse<Map<String, Object>>> healthCheck() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "healthy");
        health.put("message", "Face Verification System is running");
        health.put("language", "Java");
        health.put("framework", "Spring Boot");
        health.put("timestamp", java.time.LocalDateTime.now());

        return ResponseEntity.ok(ApiResponse.success(
            "System is healthy", health));
    }

    /**
     * API documentation endpoint
     * GET /api/docs
     */
    @GetMapping("/api/docs")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getDetailedDocs() {
        Map<String, Object> docs = new HashMap<>();
        
        docs.put("title", "Live Face Detection and College ID Card Verification System");
        docs.put("description", "Java-based Face Verification System for College Final Year Project");
        docs.put("version", "1.0.0");
        docs.put("author", "AI/ML Full Stack Engineer");
        
        Map<String, Object> techStack = new HashMap<>();
        techStack.put("Language", "Java 17");
        techStack.put("Framework", "Spring Boot 3.2.1");
        techStack.put("Computer Vision", "OpenCV for Java");
        techStack.put("PDF Processing", "Apache PDFBox");
        techStack.put("Build Tool", "Maven");
        
        docs.put("techStack", techStack);
        
        Map<String, Object> usage = new HashMap<>();
        usage.put("1. Start Camera", "POST /api/start-camera");
        usage.put("2. Capture Face", "POST /api/capture-face");
        usage.put("3. Upload ID Card", "POST /api/upload-id-card with PDF file");
        usage.put("4. Verify Identity", "POST /api/verify with image paths");
        
        docs.put("usage", usage);

        return ResponseEntity.ok(ApiResponse.success(
            "Detailed API Documentation", docs));
    }

    /**
     * System information endpoint
     * GET /api/info
     */
    @GetMapping("/api/info")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getSystemInfo() {
        Map<String, Object> info = new HashMap<>();
        
        info.put("applicationName", applicationName);
        info.put("javaVersion", System.getProperty("java.version"));
        info.put("osName", System.getProperty("os.name"));
        info.put("osVersion", System.getProperty("os.version"));
        info.put("architecture", System.getProperty("os.arch"));
        info.put("availableProcessors", Runtime.getRuntime().availableProcessors());
        info.put("maxMemory", Runtime.getRuntime().maxMemory() / (1024 * 1024) + " MB");
        info.put("freeMemory", Runtime.getRuntime().freeMemory() / (1024 * 1024) + " MB");

        return ResponseEntity.ok(ApiResponse.success(
            "System Information", info));
    }
}