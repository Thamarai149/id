"""
Camera Service for Live Face Detection
Handles camera initialization, face capture, and image processing
"""

import cv2
import os
import time
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CameraService:
    """
    Service class for handling camera operations and face capture
    """
    
    def __init__(self, camera_index=0, width=640, height=480):
        """
        Initialize camera service
        
        Args:
            camera_index (int): Camera device index (0 for default webcam)
            width (int): Camera frame width
            height (int): Camera frame height
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.camera = None
        self.is_camera_active = False
        
        # Load face detection classifier
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def initialize_camera(self):
        """
        Initialize and configure the camera
        
        Returns:
            dict: Status of camera initialization
        """
        try:
            # Release any existing camera connection
            if self.camera is not None:
                self.camera.release()
            
            # Initialize camera
            self.camera = cv2.VideoCapture(self.camera_index)
            
            if not self.camera.isOpened():
                logger.error(f"Failed to open camera at index {self.camera_index}")
                return {
                    "success": False,
                    "message": "Camera not detected or already in use",
                    "error_code": "CAMERA_NOT_FOUND"
                }
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            # Test camera by reading a frame
            ret, frame = self.camera.read()
            if not ret:
                logger.error("Failed to read frame from camera")
                return {
                    "success": False,
                    "message": "Camera detected but unable to capture frames",
                    "error_code": "CAMERA_READ_ERROR"
                }
            
            self.is_camera_active = True
            logger.info("Camera initialized successfully")
            
            return {
                "success": True,
                "message": "Camera initialized successfully",
                "camera_info": {
                    "width": int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    "height": int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    "fps": int(self.camera.get(cv2.CAP_PROP_FPS))
                }
            }
            
        except Exception as e:
            logger.error(f"Error initializing camera: {str(e)}")
            return {
                "success": False,
                "message": f"Camera initialization failed: {str(e)}",
                "error_code": "CAMERA_INIT_ERROR"
            }
    
    def capture_face_live(self, save_path="camera"):
        """
        Start live camera feed and capture face when 'C' key is pressed
        
        Args:
            save_path (str): Directory to save captured images
            
        Returns:
            dict: Result of face capture operation
        """
        if not self.is_camera_active or self.camera is None:
            init_result = self.initialize_camera()
            if not init_result["success"]:
                return init_result
        
        try:
            # Create save directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            
            logger.info("Starting live face capture. Press 'C' to capture, 'Q' to quit")
            
            captured_image_path = None
            face_detected = False
            
            while True:
                # Read frame from camera
                ret, frame = self.camera.read()
                if not ret:
                    return {
                        "success": False,
                        "message": "Failed to read frame from camera",
                        "error_code": "FRAME_READ_ERROR"
                    }
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.1, 
                    minNeighbors=5, 
                    minSize=(30, 30)
                )
                
                # Draw rectangles around detected faces
                display_frame = frame.copy()
                face_count = len(faces)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(display_frame, 'Face Detected', (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display status information
                status_text = f"Faces: {face_count} | Press 'C' to capture, 'Q' to quit"
                cv2.putText(display_frame, status_text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if face_count == 0:
                    cv2.putText(display_frame, "No face detected", (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                elif face_count > 1:
                    cv2.putText(display_frame, "Multiple faces detected", (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
                else:
                    cv2.putText(display_frame, "Ready to capture", (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Show the frame
                cv2.imshow('Live Face Capture - College ID Verification', display_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('c') or key == ord('C'):
                    # Capture face
                    if face_count == 0:
                        logger.warning("No face detected for capture")
                        continue
                    elif face_count > 1:
                        logger.warning("Multiple faces detected, cannot capture")
                        continue
                    
                    # Save the captured image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"captured_face_{timestamp}.jpg"
                    captured_image_path = os.path.join(save_path, filename)
                    
                    cv2.imwrite(captured_image_path, frame)
                    face_detected = True
                    logger.info(f"Face captured and saved: {captured_image_path}")
                    break
                
                elif key == ord('q') or key == ord('Q'):
                    # Quit without capturing
                    logger.info("Face capture cancelled by user")
                    break
            
            # Clean up
            cv2.destroyAllWindows()
            
            if face_detected and captured_image_path:
                return {
                    "success": True,
                    "message": "Face captured successfully",
                    "image_path": captured_image_path,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "message": "Face capture cancelled or failed",
                    "error_code": "CAPTURE_CANCELLED"
                }
                
        except Exception as e:
            logger.error(f"Error during face capture: {str(e)}")
            cv2.destroyAllWindows()
            return {
                "success": False,
                "message": f"Face capture failed: {str(e)}",
                "error_code": "CAPTURE_ERROR"
            }
    
    def detect_faces_in_image(self, image_path):
        """
        Detect faces in a static image
        
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
                minSize=(30, 30)
            )
            
            face_count = len(faces)
            
            return {
                "success": True,
                "face_count": face_count,
                "faces": faces.tolist() if face_count > 0 else [],
                "message": f"Detected {face_count} face(s) in image"
            }
            
        except Exception as e:
            logger.error(f"Error detecting faces in image: {str(e)}")
            return {
                "success": False,
                "message": f"Face detection failed: {str(e)}",
                "error_code": "FACE_DETECTION_ERROR"
            }
    
    def release_camera(self):
        """
        Release camera resources
        """
        try:
            if self.camera is not None:
                self.camera.release()
                self.camera = None
            cv2.destroyAllWindows()
            self.is_camera_active = False
            logger.info("Camera resources released")
        except Exception as e:
            logger.error(f"Error releasing camera: {str(e)}")
    
    def __del__(self):
        """
        Destructor to ensure camera is released
        """
        self.release_camera()