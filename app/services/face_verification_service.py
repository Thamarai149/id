"""
Face Verification Service
Handles face detection, recognition, and verification between live camera and ID card images
Automatically falls back to OpenCV-only methods if face_recognition is not available
"""

import cv2
import numpy as np
import os
import logging
from PIL import Image

# Try to import face_recognition, fall back to basic methods if not available
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("⚠️  face_recognition library not available. Using basic OpenCV methods.")

logger = logging.getLogger(__name__)

class FaceVerificationService:
    """
    Service class for face detection and verification operations
    Automatically uses advanced or basic methods based on available libraries
    """
    
    def __init__(self, tolerance=0.6, model='hog'):
        """
        Initialize face verification service
        
        Args:
            tolerance (float): Face recognition tolerance (lower = more strict)
            model (str): Face detection model ('hog' or 'cnn')
        """
        self.tolerance = tolerance
        self.model = model
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Load fallback service if face_recognition is not available
        if not FACE_RECOGNITION_AVAILABLE:
            from app.services.face_verification_service_fallback import FaceVerificationServiceFallback
            self.fallback_service = FaceVerificationServiceFallback(tolerance, model)
            logger.info("Using fallback face verification service (OpenCV only)")
        else:
            self.fallback_service = None
            logger.info("Using advanced face verification service (face_recognition)")
    
    def detect_faces_opencv(self, image_path):
        """
        Detect faces using OpenCV (faster but less accurate)
        
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
    
    def detect_faces_dlib(self, image_path):
        """
        Detect faces using face_recognition library (more accurate)
        Falls back to OpenCV if face_recognition is not available
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Face detection results with encodings
        """
        if not FACE_RECOGNITION_AVAILABLE:
            logger.info("face_recognition not available, using OpenCV fallback")
            return self.detect_faces_opencv(image_path)
        
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find face locations
            face_locations = face_recognition.face_locations(image, model=self.model)
            face_count = len(face_locations)
            
            if face_count == 0:
                return {
                    "success": True,
                    "face_count": 0,
                    "faces": [],
                    "encodings": [],
                    "message": "No faces detected in image"
                }
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            return {
                "success": True,
                "face_count": face_count,
                "faces": face_locations,
                "encodings": face_encodings,
                "message": f"Detected {face_count} face(s) using face_recognition library"
            }
            
        except Exception as e:
            logger.error(f"Error in face_recognition detection: {str(e)}")
            return {
                "success": False,
                "message": f"Face detection failed: {str(e)}",
                "error_code": "DLIB_DETECTION_ERROR"
            }
    
    def extract_face_encoding(self, image_path):
        """
        Extract face encoding from image for comparison
        Uses fallback method if face_recognition is not available
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Face encoding extraction results
        """
        if not FACE_RECOGNITION_AVAILABLE:
            return self.fallback_service.extract_face_features(image_path)
        
        try:
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "message": "Image file not found",
                    "error_code": "FILE_NOT_FOUND"
                }
            
            # Detect faces first
            detection_result = self.detect_faces_dlib(image_path)
            
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
            
            # Get the face encoding
            face_encoding = detection_result["encodings"][0]
            
            return {
                "success": True,
                "message": "Face encoding extracted successfully",
                "encoding": face_encoding,
                "face_location": detection_result["faces"][0]
            }
            
        except Exception as e:
            logger.error(f"Error extracting face encoding: {str(e)}")
            return {
                "success": False,
                "message": f"Face encoding extraction failed: {str(e)}",
                "error_code": "ENCODING_EXTRACTION_ERROR"
            }
    
    def compare_faces(self, image1_path, image2_path):
        """
        Compare two face images and return similarity score
        Uses fallback method if face_recognition is not available
        
        Args:
            image1_path (str): Path to first image (live camera capture)
            image2_path (str): Path to second image (ID card photo)
            
        Returns:
            dict: Face comparison results
        """
        if not FACE_RECOGNITION_AVAILABLE:
            return self.fallback_service.compare_faces_basic(image1_path, image2_path)
        
        try:
            logger.info(f"Comparing faces: {image1_path} vs {image2_path}")
            
            # Extract encodings from both images
            encoding1_result = self.extract_face_encoding(image1_path)
            encoding2_result = self.extract_face_encoding(image2_path)
            
            # Check if both extractions were successful
            if not encoding1_result["success"]:
                return {
                    "success": False,
                    "message": f"Live camera image: {encoding1_result['message']}",
                    "error_code": f"CAMERA_IMAGE_{encoding1_result.get('error_code', 'ERROR')}"
                }
            
            if not encoding2_result["success"]:
                return {
                    "success": False,
                    "message": f"ID card image: {encoding2_result['message']}",
                    "error_code": f"ID_CARD_IMAGE_{encoding2_result.get('error_code', 'ERROR')}"
                }
            
            # Get face encodings
            encoding1 = encoding1_result["encoding"]
            encoding2 = encoding2_result["encoding"]
            
            # Calculate face distance (lower = more similar)
            face_distance = face_recognition.face_distance([encoding1], encoding2)[0]
            
            # Calculate confidence percentage (higher = more confident match)
            confidence = max(0, (1 - face_distance) * 100)
            
            # Determine if faces match based on tolerance
            is_match = face_distance <= self.tolerance
            
            # Determine verification result
            if is_match:
                result_status = "Verified"
                result_message = f"Faces match with {confidence:.2f}% confidence"
            else:
                result_status = "Not Verified"
                result_message = f"Faces do not match. Confidence: {confidence:.2f}%"
            
            logger.info(f"Face comparison result: {result_status}, Distance: {face_distance:.4f}, Confidence: {confidence:.2f}%")
            
            return {
                "success": True,
                "result": result_status,
                "is_match": is_match,
                "confidence": round(confidence, 2),
                "face_distance": round(face_distance, 4),
                "tolerance_used": self.tolerance,
                "message": result_message,
                "method": "Advanced face_recognition library",
                "details": {
                    "camera_image": {
                        "path": image1_path,
                        "face_location": encoding1_result["face_location"]
                    },
                    "id_card_image": {
                        "path": image2_path,
                        "face_location": encoding2_result["face_location"]
                    }
                }
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
        Complete identity verification process
        Uses fallback method if face_recognition is not available
        
        Args:
            camera_image_path (str): Path to live camera capture
            id_card_image_path (str): Path to ID card photo
            student_details (dict): Extracted student details from ID card
            
        Returns:
            dict: Complete verification results
        """
        if not FACE_RECOGNITION_AVAILABLE:
            return self.fallback_service.verify_identity(camera_image_path, id_card_image_path, student_details)
        
        try:
            logger.info("Starting identity verification process")
            
            # Perform face comparison
            comparison_result = self.compare_faces(camera_image_path, id_card_image_path)
            
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
                "face_distance": comparison_result.get("face_distance", 0),
                "message": comparison_result["message"],
                "method": comparison_result.get("method", "Unknown"),
                "student_details": student_details or {},
                "verification_details": {
                    "tolerance_used": comparison_result["tolerance_used"],
                    "camera_image": camera_image_path,
                    "id_card_image": id_card_image_path,
                    "timestamp": self._get_timestamp()
                }
            }
            
            # Add recommendation based on confidence
            if comparison_result["confidence"] >= 80:
                verification_result["recommendation"] = "High confidence match"
            elif comparison_result["confidence"] >= 60:
                verification_result["recommendation"] = "Moderate confidence match"
            else:
                verification_result["recommendation"] = "Low confidence - manual review recommended"
            
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