"""
Fallback Face Verification Service
Works without face_recognition library using OpenCV only
For use when face_recognition library is not available
"""

import cv2
import numpy as np
import os
import logging
from PIL import Image

logger = logging.getLogger(__name__)

class FaceVerificationServiceFallback:
    """
    Fallback service class for face detection and basic verification operations
    Uses only OpenCV when face_recognition library is not available
    """
    
    def __init__(self, tolerance=0.6, model='hog'):
        """
        Initialize fallback face verification service
        
        Args:
            tolerance (float): Face recognition tolerance (not used in fallback)
            model (str): Face detection model (not used in fallback)
        """
        self.tolerance = tolerance
        self.model = model
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Load additional cascades for better detection
        try:
            self.profile_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_profileface.xml'
            )
        except:
            self.profile_cascade = None
    
    def detect_faces_opencv(self, image_path):
        """
        Detect faces using OpenCV
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Face detection results
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {
                    "success": False,
                    "message": "Could not read image file",
                    "error_code": "IMAGE_READ_ERROR"
                }
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            face_count = len(faces)
            
            return {
                "success": True,
                "face_count": face_count,
                "faces": faces.tolist(),
                "message": f"Detected {face_count} face(s) using OpenCV"
            }
            
        except Exception as e:
            logger.error(f"Error in OpenCV face detection: {str(e)}")
            return {
                "success": False,
                "message": f"Face detection failed: {str(e)}",
                "error_code": "OPENCV_DETECTION_ERROR"
            }
    
    def extract_face_features(self, image_path):
        """
        Extract basic face features using OpenCV (fallback method)
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Basic face feature extraction results
        """
        try:
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "message": "Image file not found",
                    "error_code": "FILE_NOT_FOUND"
                }
            
            # Detect faces first
            detection_result = self.detect_faces_opencv(image_path)
            
            if not detection_result["success"]:
                return detection_result
            
            face_count = detection_result["face_count"]
            
            if face_count == 0:
                return {
                    "success": False,
                    "message": "No face detected in image",
                    "error_code": "NO_FACE_DETECTED"
                }
            
            if face_count > 1:
                return {
                    "success": False,
                    "message": f"Multiple faces detected ({face_count}). Please use image with single face",
                    "error_code": "MULTIPLE_FACES_DETECTED"
                }
            
            # Read image and extract face region
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Get the face coordinates
            face_coords = detection_result["faces"][0]
            x, y, w, h = face_coords
            
            # Extract face region
            face_region = gray[y:y+h, x:x+w]
            
            # Calculate basic features (histogram, mean, std)
            face_histogram = cv2.calcHist([face_region], [0], None, [256], [0, 256])
            face_mean = np.mean(face_region)
            face_std = np.std(face_region)
            
            # Create a simple feature vector
            features = {
                "histogram": face_histogram.flatten().tolist()[:50],  # First 50 bins
                "mean_intensity": float(face_mean),
                "std_intensity": float(face_std),
                "face_area": int(w * h),
                "aspect_ratio": float(w / h),
                "face_coords": face_coords
            }
            
            return {
                "success": True,
                "message": "Basic face features extracted successfully",
                "features": features,
                "face_location": face_coords
            }
            
        except Exception as e:
            logger.error(f"Error extracting face features: {str(e)}")
            return {
                "success": False,
                "message": f"Face feature extraction failed: {str(e)}",
                "error_code": "FEATURE_EXTRACTION_ERROR"
            }
    
    def compare_faces_basic(self, image1_path, image2_path):
        """
        Compare two face images using basic OpenCV methods (fallback)
        
        Args:
            image1_path (str): Path to first image (live camera capture)
            image2_path (str): Path to second image (ID card photo)
            
        Returns:
            dict: Basic face comparison results
        """
        try:
            logger.info(f"Comparing faces (basic method): {image1_path} vs {image2_path}")
            
            # Extract features from both images
            features1_result = self.extract_face_features(image1_path)
            features2_result = self.extract_face_features(image2_path)
            
            # Check if both extractions were successful
            if not features1_result["success"]:
                return {
                    "success": False,
                    "message": f"Live camera image: {features1_result['message']}",
                    "error_code": f"CAMERA_IMAGE_{features1_result.get('error_code', 'ERROR')}"
                }
            
            if not features2_result["success"]:
                return {
                    "success": False,
                    "message": f"ID card image: {features2_result['message']}",
                    "error_code": f"ID_CARD_IMAGE_{features2_result.get('error_code', 'ERROR')}"
                }
            
            # Get features
            features1 = features1_result["features"]
            features2 = features2_result["features"]
            
            # Calculate basic similarity metrics
            
            # 1. Histogram correlation
            hist1 = np.array(features1["histogram"])
            hist2 = np.array(features2["histogram"])
            hist_correlation = cv2.compareHist(hist1.astype(np.float32), hist2.astype(np.float32), cv2.HISTCMP_CORREL)
            
            # 2. Intensity similarity
            intensity_diff = abs(features1["mean_intensity"] - features2["mean_intensity"])
            intensity_similarity = max(0, 1 - (intensity_diff / 255.0))
            
            # 3. Aspect ratio similarity
            ratio_diff = abs(features1["aspect_ratio"] - features2["aspect_ratio"])
            ratio_similarity = max(0, 1 - ratio_diff)
            
            # 4. Size similarity
            area1 = features1["face_area"]
            area2 = features2["face_area"]
            size_ratio = min(area1, area2) / max(area1, area2)
            
            # Combine similarities (weighted average)
            weights = {
                "histogram": 0.4,
                "intensity": 0.2,
                "ratio": 0.2,
                "size": 0.2
            }
            
            combined_similarity = (
                hist_correlation * weights["histogram"] +
                intensity_similarity * weights["intensity"] +
                ratio_similarity * weights["ratio"] +
                size_ratio * weights["size"]
            )
            
            # Convert to confidence percentage
            confidence = max(0, min(100, combined_similarity * 100))
            
            # Determine if faces match (using a lower threshold for basic method)
            basic_threshold = 0.4  # Lower threshold since this is a basic method
            is_match = combined_similarity >= basic_threshold
            
            # Determine verification result
            if is_match:
                result_status = "Verified"
                result_message = f"Faces appear to match with {confidence:.2f}% confidence (basic method)"
            else:
                result_status = "Not Verified"
                result_message = f"Faces do not appear to match. Confidence: {confidence:.2f}% (basic method)"
            
            logger.info(f"Basic face comparison result: {result_status}, Similarity: {combined_similarity:.4f}, Confidence: {confidence:.2f}%")
            
            return {
                "success": True,
                "result": result_status,
                "is_match": is_match,
                "confidence": round(confidence, 2),
                "similarity_score": round(combined_similarity, 4),
                "tolerance_used": basic_threshold,
                "message": result_message,
                "method": "Basic OpenCV comparison",
                "details": {
                    "camera_image": {
                        "path": image1_path,
                        "face_location": features1_result["face_location"]
                    },
                    "id_card_image": {
                        "path": image2_path,
                        "face_location": features2_result["face_location"]
                    },
                    "similarity_breakdown": {
                        "histogram_correlation": round(hist_correlation, 4),
                        "intensity_similarity": round(intensity_similarity, 4),
                        "ratio_similarity": round(ratio_similarity, 4),
                        "size_similarity": round(size_ratio, 4)
                    }
                },
                "warning": "This is a basic comparison method. For better accuracy, install face_recognition library."
            }
            
        except Exception as e:
            logger.error(f"Error comparing faces: {str(e)}")
            return {
                "success": False,
                "message": f"Face comparison failed: {str(e)}",
                "error_code": "COMPARISON_ERROR"
            }
    
    def verify_identity(self, camera_image_path, id_card_image_path, student_details=None):
        """
        Complete identity verification process using basic methods
        
        Args:
            camera_image_path (str): Path to live camera capture
            id_card_image_path (str): Path to ID card photo
            student_details (dict): Extracted student details from ID card
            
        Returns:
            dict: Complete verification results
        """
        try:
            logger.info("Starting identity verification process (basic method)")
            
            # Perform face comparison
            comparison_result = self.compare_faces_basic(camera_image_path, id_card_image_path)
            
            if not comparison_result["success"]:
                return {
                    "success": False,
                    "result": "Verification Failed",
                    "confidence": 0,
                    "message": comparison_result["message"],
                    "error_code": comparison_result.get("error_code"),
                    "student_details": student_details or {}
                }
            
            # Prepare final result
            verification_result = {
                "success": True,
                "result": comparison_result["result"],
                "is_match": comparison_result["is_match"],
                "confidence": comparison_result["confidence"],
                "similarity_score": comparison_result["similarity_score"],
                "message": comparison_result["message"],
                "method": comparison_result["method"],
                "warning": comparison_result.get("warning", ""),
                "student_details": student_details or {},
                "verification_details": {
                    "tolerance_used": comparison_result["tolerance_used"],
                    "camera_image": camera_image_path,
                    "id_card_image": id_card_image_path,
                    "timestamp": self._get_timestamp(),
                    "similarity_breakdown": comparison_result["details"]["similarity_breakdown"]
                }
            }
            
            # Add recommendation based on confidence
            if comparison_result["confidence"] >= 70:
                verification_result["recommendation"] = "Moderate confidence match (basic method)"
            elif comparison_result["confidence"] >= 50:
                verification_result["recommendation"] = "Low confidence match (basic method)"
            else:
                verification_result["recommendation"] = "Very low confidence - manual review required"
            
            logger.info(f"Identity verification completed: {verification_result['result']}")
            
            return verification_result
            
        except Exception as e:
            logger.error(f"Error in identity verification: {str(e)}")
            return {
                "success": False,
                "result": "Verification Failed",
                "confidence": 0,
                "message": f"Identity verification failed: {str(e)}",
                "error_code": "VERIFICATION_ERROR",
                "student_details": student_details or {}
            }
    
    def _get_timestamp(self):
        """
        Get current timestamp for verification records
        
        Returns:
            str: ISO format timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def validate_image_quality(self, image_path):
        """
        Validate image quality for face recognition
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Image quality validation results
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {
                    "valid": False,
                    "message": "Could not read image file",
                    "error_code": "IMAGE_READ_ERROR"
                }
            
            height, width = image.shape[:2]
            
            # Check minimum resolution
            if width < 100 or height < 100:
                return {
                    "valid": False,
                    "message": f"Image resolution too low: {width}x{height}. Minimum 100x100 required",
                    "error_code": "LOW_RESOLUTION"
                }
            
            # Check if image is too dark or too bright
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
            
            if mean_brightness < 30:
                return {
                    "valid": False,
                    "message": "Image is too dark for face recognition",
                    "error_code": "TOO_DARK"
                }
            
            if mean_brightness > 225:
                return {
                    "valid": False,
                    "message": "Image is too bright for face recognition",
                    "error_code": "TOO_BRIGHT"
                }
            
            # Check for blur (using Laplacian variance)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            if laplacian_var < 100:
                return {
                    "valid": False,
                    "message": "Image appears to be blurry",
                    "error_code": "BLURRY_IMAGE"
                }
            
            return {
                "valid": True,
                "message": "Image quality is acceptable for face recognition",
                "details": {
                    "resolution": f"{width}x{height}",
                    "brightness": round(mean_brightness, 2),
                    "sharpness": round(laplacian_var, 2)
                }
            }
            
        except Exception as e:
            logger.error(f"Error validating image quality: {str(e)}")
            return {
                "valid": False,
                "message": f"Image quality validation failed: {str(e)}",
                "error_code": "VALIDATION_ERROR"
            }