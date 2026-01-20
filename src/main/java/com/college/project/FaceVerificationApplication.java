package com.college.project;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.MultipartConfigFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.util.unit.DataSize;

import jakarta.servlet.MultipartConfigElement;

/**
 * Live Face Detection and College ID Card Verification System
 * Main Spring Boot Application Class
 * 
 * @author AI/ML Full Stack Engineer
 * @version 1.0.0
 * @since 2026-01-20
 */
@SpringBootApplication
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
}