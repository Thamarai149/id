package com.college.project.controller;

import com.college.project.model.ApiResponse;
import com.college.project.service.CameraService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Camera Controller for Live Face Detection
 * REST API endpoints for camera operations and face capture
 */
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class CameraController {

    private static final Logger logger = LoggerFactory.getLogger(CameraController.class);

    @Autowired
    private CameraService cameraService;

    /**
     * Initialize camera for face capture
     * POST /api/start-camera
     */
    @PostMapping("/start-camera")
    public ResponseEntity<ApiResponse<Map<String, Object>>> startCamera() {
        try {
            logger.info("Camera initialization requested");

            Map<String, Object> result = cameraService.initializeCamera();
            boolean success = (Boolean) result.get("success");

            if (success) {
                Map<String, Object> data = new HashMap<>();
                data.put("cameraInfo", result.get("cameraInfo"));
                data.put("instructions", List.of(
                    "Camera is ready for face capture",
                    "Call /capture-face endpoint to start live capture",
                    "System will automatically detect and capture face",
                    "Ensure good lighting and single person in frame"
                ));

                return ResponseEntity.ok(ApiResponse.success(
                    (String) result.get("message"), data));
            } else {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    (String) result.get("message"), 
                    (String) result.get("errorCode")));
            }

        } catch (Exception e) {
            logger.error("Error in start_camera endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Camera initialization failed: " + e.getMessage(),
                "CAMERA_INIT_EXCEPTION"));
        }
    }

    /**
     * Capture face from camera
     * POST /api/capture-face
     */
    @PostMapping("/capture-face")
    public ResponseEntity<ApiResponse<Map<String, Object>>> captureFace() {
        try {
            logger.info("Face capture requested");

            Map<String, Object> result = cameraService.captureFace();
            boolean success = (Boolean) result.get("success");

            if (success) {
                Map<String, Object> data = new HashMap<>();
                data.put("imagePath", result.get("imagePath"));
                data.put("timestamp", result.get("timestamp"));
                data.put("faceCount", result.get("faceCount"));
                data.put("instructions", List.of(
                    "Face captured successfully",
                    "Image saved and ready for verification",
                    "Use /verify endpoint to compare with ID card"
                ));

                return ResponseEntity.ok(ApiResponse.success(
                    (String) result.get("message"), data));
            } else {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    (String) result.get("message"),
                    (String) result.get("errorCode")));
            }

        } catch (Exception e) {
            logger.error("Error in capture_face endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Face capture failed: " + e.getMessage(),
                "CAPTURE_EXCEPTION"));
        }
    }

    /**
     * Get camera status
     * GET /api/camera-status
     */
    @GetMapping("/camera-status")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getCameraStatus() {
        try {
            Map<String, Object> status = cameraService.getCameraStatus();
            status.put("supportedOperations", List.of(
                "start-camera", "capture-face", "camera-status", "test-camera"
            ));

            return ResponseEntity.ok(ApiResponse.success(
                "Camera status retrieved successfully", status));

        } catch (Exception e) {
            logger.error("Error in camera_status endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Failed to get camera status: " + e.getMessage(),
                "STATUS_ERROR"));
        }
    }

    /**
     * Test camera functionality
     * POST /api/test-camera
     */
    @PostMapping("/test-camera")
    public ResponseEntity<ApiResponse<Map<String, Object>>> testCamera() {
        try {
            logger.info("Camera test requested");

            Map<String, Object> result = cameraService.testCamera();
            boolean success = (Boolean) result.get("success");

            if (success) {
                return ResponseEntity.ok(ApiResponse.success(
                    (String) result.get("message"), result));
            } else {
                return ResponseEntity.badRequest().body(ApiResponse.error(
                    (String) result.get("message"),
                    (String) result.get("errorCode")));
            }

        } catch (Exception e) {
            logger.error("Error in test_camera endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Camera test failed: " + e.getMessage(),
                "TEST_EXCEPTION"));
        }
    }

    /**
     * Release camera resources
     * POST /api/release-camera
     */
    @PostMapping("/release-camera")
    public ResponseEntity<ApiResponse<Map<String, Object>>> releaseCamera() {
        try {
            logger.info("Camera release requested");

            cameraService.releaseCamera();

            Map<String, Object> data = new HashMap<>();
            data.put("cameraActive", false);
            data.put("message", "Camera is now available for other applications");

            return ResponseEntity.ok(ApiResponse.success(
                "Camera resources released successfully", data));

        } catch (Exception e) {
            logger.error("Error in release_camera endpoint: {}", e.getMessage());
            return ResponseEntity.internalServerError().body(ApiResponse.error(
                "Failed to release camera: " + e.getMessage(),
                "RELEASE_ERROR"));
        }
    }
}