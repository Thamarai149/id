"""
Configuration settings for the Face Verification System
"""

import os

class Config:
    """
    Application configuration class
    Contains all the settings needed for the face verification system
    """
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'face-verification-secret-key-2024'
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    CAMERA_FOLDER = 'camera'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Face recognition settings
    FACE_RECOGNITION_TOLERANCE = 0.6  # Lower = more strict, Higher = more lenient
    FACE_DETECTION_MODEL = 'hog'  # 'hog' is faster, 'cnn' is more accurate
    
    # Camera settings
    CAMERA_INDEX = 0  # Default camera (usually webcam)
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    
    # Image processing settings
    IMAGE_QUALITY = 95
    SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']
    
    @staticmethod
    def allowed_file(filename):
        """
        Check if uploaded file has allowed extension
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS