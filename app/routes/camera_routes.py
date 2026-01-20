"""
Camera Routes for Live Face Detection
API endpoints for camera operations and face capture
"""

from flask import Blueprint, request, jsonify
import os
import logging
from app.services.camera_service import CameraService
from app.utils.config import Config

logger = logging.getLogger(__name__)

# Create blueprint for camera routes
camera_bp = Blueprint('camera', __name__)

# Initialize camera service
camera_service = CameraService(
    camera_index=Config.CAMERA_INDEX,
    width=Config.CAMERA_WIDTH,
    height=Config.CAMERA_HEIGHT
)

@camera_bp.route('/start-camera', methods=['POST'])
def start_camera():
    """
    Initialize camera for face capture
    
    Returns:
        JSON response with camera initialization status
    """
    try:
        logger.info("Camera initialization requested")
        
        # Initialize camera
        result = camera_service.initialize_camera()
        
        if result["success"]:
            return jsonify({
                "status": "success",
                "message": result["message"],
                "data": {
                    "camera_info": result.get("camera_info", {}),
                    "instructions": [
                        "Camera is ready for face capture",
                        "Call /capture-face endpoint to start live capture",
                        "Press 'C' key to capture face during live feed",
                        "Press 'Q' key to quit without capturing"
                    ]
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": result["message"],
                "error_code": result.get("error_code"),
                "suggestions": [
                    "Check if camera is connected and not being used by another application",
                    "Try restarting the application",
                    "Check camera permissions"
                ]
            }), 400
            
    except Exception as e:
        logger.error(f"Error in start_camera endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Camera initialization failed: {str(e)}",
            "error_code": "CAMERA_INIT_EXCEPTION"
        }), 500

@camera_bp.route('/capture-face', methods=['POST'])
def capture_face():
    """
    Start live camera feed and capture face when user presses 'C'
    
    Returns:
        JSON response with face capture results
    """
    try:
        logger.info("Face capture requested")
        
        # Get optional parameters from request
        data = request.get_json() or {}
        save_path = data.get('save_path', Config.CAMERA_FOLDER)
        
        # Ensure save directory exists
        os.makedirs(save_path, exist_ok=True)
        
        # Start face capture
        result = camera_service.capture_face_live(save_path)
        
        if result["success"]:
            return jsonify({
                "status": "success",
                "message": result["message"],
                "data": {
                    "image_path": result["image_path"],
                    "timestamp": result["timestamp"],
                    "instructions": [
                        "Face captured successfully",
                        "Image saved and ready for verification",
                        "Use /verify endpoint to compare with ID card"
                    ]
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": result["message"],
                "error_code": result.get("error_code"),
                "suggestions": [
                    "Ensure camera is initialized using /start-camera",
                    "Make sure your face is clearly visible",
                    "Avoid multiple faces in the camera view",
                    "Press 'C' key to capture when ready"
                ]
            }), 400
            
    except Exception as e:
        logger.error(f"Error in capture_face endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Face capture failed: {str(e)}",
            "error_code": "CAPTURE_EXCEPTION"
        }), 500

@camera_bp.route('/camera-status', methods=['GET'])
def camera_status():
    """
    Get current camera status and information
    
    Returns:
        JSON response with camera status
    """
    try:
        return jsonify({
            "status": "success",
            "data": {
                "camera_active": camera_service.is_camera_active,
                "camera_index": camera_service.camera_index,
                "resolution": {
                    "width": camera_service.width,
                    "height": camera_service.height
                },
                "camera_folder": Config.CAMERA_FOLDER,
                "supported_operations": [
                    "start-camera",
                    "capture-face",
                    "camera-status"
                ]
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in camera_status endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to get camera status: {str(e)}",
            "error_code": "STATUS_ERROR"
        }), 500

@camera_bp.route('/release-camera', methods=['POST'])
def release_camera():
    """
    Release camera resources
    
    Returns:
        JSON response with release status
    """
    try:
        logger.info("Camera release requested")
        
        # Release camera
        camera_service.release_camera()
        
        return jsonify({
            "status": "success",
            "message": "Camera resources released successfully",
            "data": {
                "camera_active": False,
                "message": "Camera is now available for other applications"
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in release_camera endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to release camera: {str(e)}",
            "error_code": "RELEASE_ERROR"
        }), 500

@camera_bp.route('/test-camera', methods=['POST'])
def test_camera():
    """
    Test camera functionality without capturing
    
    Returns:
        JSON response with camera test results
    """
    try:
        logger.info("Camera test requested")
        
        # Initialize camera for testing
        result = camera_service.initialize_camera()
        
        if result["success"]:
            # Test face detection on a single frame
            import cv2
            ret, frame = camera_service.camera.read()
            
            if ret:
                # Save test frame temporarily
                test_path = os.path.join(Config.CAMERA_FOLDER, "camera_test.jpg")
                os.makedirs(Config.CAMERA_FOLDER, exist_ok=True)
                cv2.imwrite(test_path, frame)
                
                # Test face detection
                face_result = camera_service.detect_faces_in_image(test_path)
                
                # Clean up test file
                if os.path.exists(test_path):
                    os.remove(test_path)
                
                return jsonify({
                    "status": "success",
                    "message": "Camera test completed successfully",
                    "data": {
                        "camera_working": True,
                        "frame_captured": True,
                        "face_detection": face_result,
                        "camera_info": result.get("camera_info", {})
                    }
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": "Camera initialized but failed to capture test frame",
                    "error_code": "TEST_FRAME_ERROR"
                }), 400
        else:
            return jsonify({
                "status": "error",
                "message": result["message"],
                "error_code": result.get("error_code")
            }), 400
            
    except Exception as e:
        logger.error(f"Error in test_camera endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Camera test failed: {str(e)}",
            "error_code": "TEST_EXCEPTION"
        }), 500