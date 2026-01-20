"""
Verification Routes for ID Card Processing and Face Verification
API endpoints for PDF upload, processing, and face verification
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
from app.services.pdf_service import PDFService
from app.services.face_verification_service import FaceVerificationService
from app.utils.config import Config

logger = logging.getLogger(__name__)

# Create blueprint for verification routes
verification_bp = Blueprint('verification', __name__)

# Initialize services
pdf_service = PDFService()
face_verification_service = FaceVerificationService(
    tolerance=Config.FACE_RECOGNITION_TOLERANCE,
    model=Config.FACE_DETECTION_MODEL
)

@verification_bp.route('/upload-id-card', methods=['POST'])
def upload_id_card():
    """
    Upload and process college ID card PDF
    
    Returns:
        JSON response with PDF processing results
    """
    try:
        logger.info("ID card upload requested")
        
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file provided in request",
                "error_code": "NO_FILE"
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No file selected",
                "error_code": "NO_FILE_SELECTED"
            }), 400
        
        # Check file extension
        if not Config.allowed_file(file.filename):
            return jsonify({
                "status": "error",
                "message": "Invalid file format. Only PDF files are allowed",
                "error_code": "INVALID_FORMAT",
                "allowed_formats": list(Config.ALLOWED_EXTENSIONS)
            }), 400
        
        # Create upload directory
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        file.save(file_path)
        logger.info(f"File saved: {file_path}")
        
        # Process the ID card PDF
        processing_result = pdf_service.process_id_card(file_path, Config.UPLOAD_FOLDER)
        
        if processing_result["success"]:
            return jsonify({
                "status": "success",
                "message": "ID card processed successfully",
                "data": {
                    "file_info": {
                        "original_filename": file.filename,
                        "saved_filename": filename,
                        "file_path": file_path,
                        "upload_timestamp": timestamp
                    },
                    "processing_results": processing_result,
                    "next_steps": [
                        "ID card data extracted successfully",
                        "Use /capture-face to capture live photo",
                        "Use /verify to compare faces"
                    ]
                }
            }), 200
        else:
            # Clean up uploaded file if processing failed
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return jsonify({
                "status": "error",
                "message": processing_result["message"],
                "error_code": processing_result.get("error_code"),
                "suggestions": [
                    "Ensure the PDF contains a clear student photo",
                    "Check if the PDF has readable text content",
                    "Try uploading a different ID card PDF"
                ]
            }), 400
            
    except Exception as e:
        logger.error(f"Error in upload_id_card endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"ID card upload failed: {str(e)}",
            "error_code": "UPLOAD_EXCEPTION"
        }), 500

@verification_bp.route('/verify', methods=['POST'])
def verify_identity():
    """
    Verify identity by comparing live camera capture with ID card photo
    
    Expected JSON payload:
    {
        "camera_image_path": "path/to/camera/image.jpg",
        "id_card_image_path": "path/to/id/card/image.jpg",
        "student_details": {...} (optional)
    }
    
    Returns:
        JSON response with verification results
    """
    try:
        logger.info("Identity verification requested")
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided",
                "error_code": "NO_DATA"
            }), 400
        
        # Extract required parameters
        camera_image_path = data.get('camera_image_path')
        id_card_image_path = data.get('id_card_image_path')
        student_details = data.get('student_details', {})
        
        # Validate required parameters
        if not camera_image_path:
            return jsonify({
                "status": "error",
                "message": "camera_image_path is required",
                "error_code": "MISSING_CAMERA_IMAGE"
            }), 400
        
        if not id_card_image_path:
            return jsonify({
                "status": "error",
                "message": "id_card_image_path is required",
                "error_code": "MISSING_ID_CARD_IMAGE"
            }), 400
        
        # Check if files exist
        if not os.path.exists(camera_image_path):
            return jsonify({
                "status": "error",
                "message": f"Camera image not found: {camera_image_path}",
                "error_code": "CAMERA_IMAGE_NOT_FOUND"
            }), 400
        
        if not os.path.exists(id_card_image_path):
            return jsonify({
                "status": "error",
                "message": f"ID card image not found: {id_card_image_path}",
                "error_code": "ID_CARD_IMAGE_NOT_FOUND"
            }), 400
        
        # Validate image quality
        camera_quality = face_verification_service.validate_image_quality(camera_image_path)
        id_card_quality = face_verification_service.validate_image_quality(id_card_image_path)
        
        quality_issues = []
        if not camera_quality["valid"]:
            quality_issues.append(f"Camera image: {camera_quality['message']}")
        if not id_card_quality["valid"]:
            quality_issues.append(f"ID card image: {id_card_quality['message']}")
        
        if quality_issues:
            return jsonify({
                "status": "error",
                "message": "Image quality issues detected",
                "error_code": "POOR_IMAGE_QUALITY",
                "quality_issues": quality_issues,
                "suggestions": [
                    "Ensure images are well-lit and clear",
                    "Avoid blurry or low-resolution images",
                    "Retake photos if necessary"
                ]
            }), 400
        
        # Perform identity verification
        verification_result = face_verification_service.verify_identity(
            camera_image_path, 
            id_card_image_path, 
            student_details
        )
        
        if verification_result["success"]:
            # Format response according to requirements
            response_data = {
                "result": verification_result["result"],
                "confidence": f"{verification_result['confidence']}%",
                "student_details": {
                    "name": student_details.get("name", ""),
                    "register_number": student_details.get("register_number", ""),
                    "department": student_details.get("department", ""),
                    "college": student_details.get("college", ""),
                    "year": student_details.get("year", ""),
                    "course": student_details.get("course", "")
                },
                "verification_details": {
                    "is_match": verification_result["is_match"],
                    "face_distance": verification_result["face_distance"],
                    "tolerance_used": verification_result["verification_details"]["tolerance_used"],
                    "recommendation": verification_result.get("recommendation", ""),
                    "timestamp": verification_result["verification_details"]["timestamp"]
                },
                "image_info": {
                    "camera_image": camera_image_path,
                    "id_card_image": id_card_image_path,
                    "camera_quality": camera_quality["details"] if camera_quality["valid"] else None,
                    "id_card_quality": id_card_quality["details"] if id_card_quality["valid"] else None
                }
            }
            
            return jsonify({
                "status": "success",
                "message": verification_result["message"],
                "data": response_data
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": verification_result["message"],
                "error_code": verification_result.get("error_code"),
                "data": {
                    "result": "Verification Failed",
                    "confidence": "0%",
                    "student_details": student_details
                }
            }), 400
            
    except Exception as e:
        logger.error(f"Error in verify_identity endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Identity verification failed: {str(e)}",
            "error_code": "VERIFICATION_EXCEPTION"
        }), 500

@verification_bp.route('/extract-text', methods=['POST'])
def extract_text_from_pdf():
    """
    Extract text content from uploaded PDF
    
    Expected JSON payload:
    {
        "file_path": "path/to/pdf/file.pdf"
    }
    
    Returns:
        JSON response with extracted text and student details
    """
    try:
        logger.info("Text extraction requested")
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided",
                "error_code": "NO_DATA"
            }), 400
        
        file_path = data.get('file_path')
        if not file_path:
            return jsonify({
                "status": "error",
                "message": "file_path is required",
                "error_code": "MISSING_FILE_PATH"
            }), 400
        
        if not os.path.exists(file_path):
            return jsonify({
                "status": "error",
                "message": f"PDF file not found: {file_path}",
                "error_code": "FILE_NOT_FOUND"
            }), 400
        
        # Extract text from PDF
        text_result = pdf_service.extract_text_from_pdf(file_path)
        
        if text_result["success"]:
            return jsonify({
                "status": "success",
                "message": text_result["message"],
                "data": {
                    "extracted_text": text_result["text"],
                    "student_details": text_result["student_details"],
                    "text_length": text_result["text_length"]
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": text_result["message"],
                "error_code": text_result.get("error_code")
            }), 400
            
    except Exception as e:
        logger.error(f"Error in extract_text endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Text extraction failed: {str(e)}",
            "error_code": "TEXT_EXTRACTION_EXCEPTION"
        }), 500

@verification_bp.route('/extract-images', methods=['POST'])
def extract_images_from_pdf():
    """
    Extract images from uploaded PDF
    
    Expected JSON payload:
    {
        "file_path": "path/to/pdf/file.pdf"
    }
    
    Returns:
        JSON response with extracted images information
    """
    try:
        logger.info("Image extraction requested")
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided",
                "error_code": "NO_DATA"
            }), 400
        
        file_path = data.get('file_path')
        if not file_path:
            return jsonify({
                "status": "error",
                "message": "file_path is required",
                "error_code": "MISSING_FILE_PATH"
            }), 400
        
        if not os.path.exists(file_path):
            return jsonify({
                "status": "error",
                "message": f"PDF file not found: {file_path}",
                "error_code": "FILE_NOT_FOUND"
            }), 400
        
        # Extract images from PDF
        image_result = pdf_service.extract_images_from_pdf(file_path, Config.UPLOAD_FOLDER)
        
        if image_result["success"]:
            return jsonify({
                "status": "success",
                "message": image_result["message"],
                "data": {
                    "total_images": image_result["total_images"],
                    "images": image_result["images"]
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": image_result["message"],
                "error_code": image_result.get("error_code")
            }), 400
            
    except Exception as e:
        logger.error(f"Error in extract_images endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Image extraction failed: {str(e)}",
            "error_code": "IMAGE_EXTRACTION_EXCEPTION"
        }), 500

@verification_bp.route('/compare-faces', methods=['POST'])
def compare_faces_only():
    """
    Compare two face images without full verification process
    
    Expected JSON payload:
    {
        "image1_path": "path/to/first/image.jpg",
        "image2_path": "path/to/second/image.jpg"
    }
    
    Returns:
        JSON response with face comparison results
    """
    try:
        logger.info("Face comparison requested")
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided",
                "error_code": "NO_DATA"
            }), 400
        
        image1_path = data.get('image1_path')
        image2_path = data.get('image2_path')
        
        if not image1_path or not image2_path:
            return jsonify({
                "status": "error",
                "message": "Both image1_path and image2_path are required",
                "error_code": "MISSING_IMAGE_PATHS"
            }), 400
        
        if not os.path.exists(image1_path):
            return jsonify({
                "status": "error",
                "message": f"First image not found: {image1_path}",
                "error_code": "IMAGE1_NOT_FOUND"
            }), 400
        
        if not os.path.exists(image2_path):
            return jsonify({
                "status": "error",
                "message": f"Second image not found: {image2_path}",
                "error_code": "IMAGE2_NOT_FOUND"
            }), 400
        
        # Compare faces
        comparison_result = face_verification_service.compare_faces(image1_path, image2_path)
        
        if comparison_result["success"]:
            return jsonify({
                "status": "success",
                "message": comparison_result["message"],
                "data": {
                    "result": comparison_result["result"],
                    "is_match": comparison_result["is_match"],
                    "confidence": comparison_result["confidence"],
                    "face_distance": comparison_result["face_distance"],
                    "tolerance_used": comparison_result["tolerance_used"],
                    "details": comparison_result["details"]
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": comparison_result["message"],
                "error_code": comparison_result.get("error_code")
            }), 400
            
    except Exception as e:
        logger.error(f"Error in compare_faces endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Face comparison failed: {str(e)}",
            "error_code": "COMPARISON_EXCEPTION"
        }), 500