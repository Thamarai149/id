package com.college.project;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration;

/**
 * Live Face Detection and College ID Card Verification System
 * Command Line Application - No Web Interface
 * 
 * @author AI/ML Full Stack Engineer
 * @version 1.0.0
 * @since 2026-01-20
 */
@SpringBootApplication(exclude = {WebMvcAutoConfiguration.class})
public class FaceVerificationApplication {

    public static void main(String[] args) {
        System.out.println("🚀 Starting Face Capture and ID Card Processing System...");
        System.out.println("📷 Make sure your camera is connected and working");
        System.out.println("📄 Place your ID card PDF as 'idcard.pdf' in the project root");
        System.out.println();
        
        // Disable web server
        System.setProperty("spring.main.web-application-type", "none");
        
        SpringApplication.run(FaceVerificationApplication.class, args);
    }
}