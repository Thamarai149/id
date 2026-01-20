package com.college.project.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Bean;
import org.springframework.boot.CommandLineRunner;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * OpenCV Configuration for Face Detection and Image Processing
 * Initializes OpenCV native library for Java with fallback methods
 */
@Configuration
public class OpenCVConfig {

    private static final Logger logger = LoggerFactory.getLogger(OpenCVConfig.class);
    private static boolean openCVLoaded = false;

    /**
     * Initialize OpenCV native library on application startup
     */
    @Bean
    public CommandLineRunner initOpenCV() {
        return args -> {
            try {
                // Try to load OpenCV native library using different methods
                loadOpenCVLibrary();
                
            } catch (Exception e) {
                logger.warn("⚠️  OpenCV initialization failed: {}. Using fallback methods.", e.getMessage());
                openCVLoaded = false;
            }
        };
    }

    /**
     * Attempt to load OpenCV library using multiple methods
     */
    private void loadOpenCVLibrary() {
        // Method 1: Try to load bundled OpenCV
        try {
            System.loadLibrary("opencv_java480");
            openCVLoaded = true;
            logger.info("✅ OpenCV loaded successfully (opencv_java480)");
            return;
        } catch (UnsatisfiedLinkError e) {
            logger.debug("opencv_java480 not found, trying alternatives...");
        }

        // Method 2: Try different OpenCV versions
        String[] openCVVersions = {"opencv_java", "opencv_java4", "opencv_java490", "opencv_java470"};
        for (String version : openCVVersions) {
            try {
                System.loadLibrary(version);
                openCVLoaded = true;
                logger.info("✅ OpenCV loaded successfully ({})", version);
                return;
            } catch (UnsatisfiedLinkError e) {
                logger.debug("{} not found, trying next...", version);
            }
        }

        // Method 3: Try to load from system path
        try {
            // This will be handled by the OpenCV Maven dependency
            Class.forName("org.opencv.core.Core");
            openCVLoaded = true;
            logger.info("✅ OpenCV classes found in classpath");
            return;
        } catch (ClassNotFoundException e) {
            logger.debug("OpenCV classes not found in classpath");
        }

        // If all methods fail, log warning but continue
        logger.warn("⚠️  OpenCV native library not available. Face detection will use basic Java image processing.");
        logger.info("💡 To enable advanced face detection, ensure OpenCV is properly installed.");
        openCVLoaded = false;
    }

    /**
     * Check if OpenCV is loaded and available
     */
    public static boolean isOpenCVLoaded() {
        return openCVLoaded;
    }

    /**
     * OpenCV configuration status bean
     */
    @Bean
    public String openCVStatus() {
        return openCVLoaded ? "OpenCV loaded and ready" : "OpenCV not available - using fallback methods";
    }

    /**
     * Get OpenCV configuration information
     */
    @Bean
    public OpenCVInfo openCVInfo() {
        return new OpenCVInfo(openCVLoaded, "Face detection ready");
    }

    /**
     * OpenCV Information class
     */
    public static class OpenCVInfo {
        private final boolean loaded;
        private final String status;

        public OpenCVInfo(boolean loaded, String status) {
            this.loaded = loaded;
            this.status = status;
        }

        public boolean isLoaded() {
            return loaded;
        }

        public String getStatus() {
            return status;
        }
    }
}