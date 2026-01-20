package com.college.project.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.util.Map;

/**
 * Face Verification Result
 * Contains the complete verification outcome and details
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public class VerificationResult {
    
    private String result; // "Verified" or "Not Verified"
    private boolean isMatch;
    private double confidence;
    private String message;
    private String recommendation;
    private StudentDetails studentDetails;
    private VerificationDetails verificationDetails;
    private String method;
    private String warning;

    public VerificationResult() {}

    public VerificationResult(String result, boolean isMatch, double confidence) {
        this.result = result;
        this.isMatch = isMatch;
        this.confidence = confidence;
    }

    /**
     * Verification Details inner class
     */
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class VerificationDetails {
        private double toleranceUsed;
        private String cameraImage;
        private String idCardImage;
        private LocalDateTime timestamp;
        private Map<String, Double> similarityBreakdown;
        private double faceDistance;

        public VerificationDetails() {
            this.timestamp = LocalDateTime.now();
        }

        // Getters and Setters
        public double getToleranceUsed() {
            return toleranceUsed;
        }

        public void setToleranceUsed(double toleranceUsed) {
            this.toleranceUsed = toleranceUsed;
        }

        public String getCameraImage() {
            return cameraImage;
        }

        public void setCameraImage(String cameraImage) {
            this.cameraImage = cameraImage;
        }

        public String getIdCardImage() {
            return idCardImage;
        }

        public void setIdCardImage(String idCardImage) {
            this.idCardImage = idCardImage;
        }

        public LocalDateTime getTimestamp() {
            return timestamp;
        }

        public void setTimestamp(LocalDateTime timestamp) {
            this.timestamp = timestamp;
        }

        public Map<String, Double> getSimilarityBreakdown() {
            return similarityBreakdown;
        }

        public void setSimilarityBreakdown(Map<String, Double> similarityBreakdown) {
            this.similarityBreakdown = similarityBreakdown;
        }

        public double getFaceDistance() {
            return faceDistance;
        }

        public void setFaceDistance(double faceDistance) {
            this.faceDistance = faceDistance;
        }
    }

    // Getters and Setters
    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public boolean isMatch() {
        return isMatch;
    }

    public void setMatch(boolean match) {
        isMatch = match;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getRecommendation() {
        return recommendation;
    }

    public void setRecommendation(String recommendation) {
        this.recommendation = recommendation;
    }

    public StudentDetails getStudentDetails() {
        return studentDetails;
    }

    public void setStudentDetails(StudentDetails studentDetails) {
        this.studentDetails = studentDetails;
    }

    public VerificationDetails getVerificationDetails() {
        return verificationDetails;
    }

    public void setVerificationDetails(VerificationDetails verificationDetails) {
        this.verificationDetails = verificationDetails;
    }

    public String getMethod() {
        return method;
    }

    public void setMethod(String method) {
        this.method = method;
    }

    public String getWarning() {
        return warning;
    }

    public void setWarning(String warning) {
        this.warning = warning;
    }
}