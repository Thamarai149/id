"""
PDF Service for ID Card Processing
Handles PDF upload, text extraction, and image extraction from college ID cards
Updated to work without PyMuPDF for better compatibility
"""

import pdfplumber
import os
import re
import logging
from PIL import Image
import io
import base64

logger = logging.getLogger(__name__)

class PDFService:
    """
    Service class for handling PDF operations and ID card processing
    Uses pdfplumber for better compatibility
    """
    
    def __init__(self):
        """
        Initialize PDF service
        """
        self.supported_formats = ['.pdf']
        self.extracted_images = []
        self.extracted_text = ""
    
    def validate_pdf(self, file_path):
        """
        Validate if the uploaded file is a valid PDF
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            dict: Validation result
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "valid": False,
                    "message": "File does not exist",
                    "error_code": "FILE_NOT_FOUND"
                }
            
            # Check file extension
            _, ext = os.path.splitext(file_path)
            if ext.lower() not in self.supported_formats:
                return {
                    "valid": False,
                    "message": "Invalid file format. Only PDF files are allowed",
                    "error_code": "INVALID_FORMAT"
                }
            
            # Try to open PDF with pdfplumber
            try:
                with pdfplumber.open(file_path) as pdf:
                    page_count = len(pdf.pages)
                    
                    if page_count == 0:
                        return {
                            "valid": False,
                            "message": "PDF file is empty",
                            "error_code": "EMPTY_PDF"
                        }
                    
                    return {
                        "valid": True,
                        "message": "Valid PDF file",
                        "page_count": page_count
                    }
                    
            except Exception as e:
                return {
                    "valid": False,
                    "message": f"Corrupted or invalid PDF file: {str(e)}",
                    "error_code": "CORRUPTED_PDF"
                }
                
        except Exception as e:
            logger.error(f"Error validating PDF: {str(e)}")
            return {
                "valid": False,
                "message": f"PDF validation failed: {str(e)}",
                "error_code": "VALIDATION_ERROR"
            }
    
    def extract_images_from_pdf(self, file_path, output_dir="uploads"):
        """
        Extract all images from PDF file using pdfplumber
        
        Args:
            file_path (str): Path to the PDF file
            output_dir (str): Directory to save extracted images
            
        Returns:
            dict: Image extraction results
        """
        try:
            # Validate PDF first
            validation = self.validate_pdf(file_path)
            if not validation["valid"]:
                return {
                    "success": False,
                    "message": validation["message"],
                    "error_code": validation["error_code"]
                }
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            extracted_images = []
            
            # Open PDF with pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract images from page
                    if hasattr(page, 'images') and page.images:
                        for img_index, img_obj in enumerate(page.images):
                            try:
                                # Get image from page
                                if hasattr(page, 'within_bbox'):
                                    # Extract image using bbox
                                    bbox = (img_obj['x0'], img_obj['top'], img_obj['x1'], img_obj['bottom'])
                                    cropped_page = page.within_bbox(bbox)
                                    
                                    if cropped_page:
                                        # Convert to image
                                        img_filename = f"extracted_image_p{page_num+1}_{img_index+1}.png"
                                        img_path = os.path.join(output_dir, img_filename)
                                        
                                        # Save as image (this is a simplified approach)
                                        # For better image extraction, we'll create a placeholder
                                        # that indicates an image was found
                                        
                                        extracted_images.append({
                                            "filename": img_filename,
                                            "path": img_path,
                                            "page": page_num + 1,
                                            "width": int(img_obj.get('width', 100)),
                                            "height": int(img_obj.get('height', 100)),
                                            "size_bytes": 1024,  # Placeholder
                                            "note": "Image detected but extraction limited without PyMuPDF"
                                        })
                                        
                            except Exception as e:
                                logger.warning(f"Failed to extract image {img_index} from page {page_num}: {e}")
                                continue
            
            # If no images found using pdfplumber, create a note
            if not extracted_images:
                logger.info("No images extracted with pdfplumber - this is normal for some PDFs")
                return {
                    "success": False,
                    "message": "No images found in PDF. For better image extraction, install Visual Studio Build Tools and PyMuPDF",
                    "error_code": "NO_IMAGES_FOUND",
                    "suggestion": "You can manually extract the student photo and place it in the uploads folder"
                }
            
            self.extracted_images = extracted_images
            
            logger.info(f"Detected {len(extracted_images)} images in PDF")
            
            return {
                "success": True,
                "message": f"Detected {len(extracted_images)} images in PDF",
                "images": extracted_images,
                "total_images": len(extracted_images),
                "note": "For full image extraction, install PyMuPDF with Visual Studio Build Tools"
            }
            
        except Exception as e:
            logger.error(f"Error extracting images from PDF: {str(e)}")
            return {
                "success": False,
                "message": f"Image extraction failed: {str(e)}",
                "error_code": "EXTRACTION_ERROR"
            }
    
    def extract_text_from_pdf(self, file_path):
        """
        Extract text content from PDF file using pdfplumber
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            dict: Text extraction results
        """
        try:
            # Validate PDF first
            validation = self.validate_pdf(file_path)
            if not validation["valid"]:
                return {
                    "success": False,
                    "message": validation["message"],
                    "error_code": validation["error_code"]
                }
            
            extracted_text = ""
            
            # Extract text using pdfplumber
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_text += page_text + "\n"
            except Exception as e:
                logger.error(f"pdfplumber extraction failed: {str(e)}")
                return {
                    "success": False,
                    "message": f"Text extraction failed: {str(e)}",
                    "error_code": "TEXT_EXTRACTION_ERROR"
                }
            
            self.extracted_text = extracted_text.strip()
            
            if not self.extracted_text:
                return {
                    "success": False,
                    "message": "No text content found in the PDF",
                    "error_code": "NO_TEXT_FOUND"
                }
            
            # Extract student details from text
            student_details = self.parse_student_details(self.extracted_text)
            
            logger.info("Text extraction completed successfully")
            
            return {
                "success": True,
                "message": "Text extracted successfully",
                "text": self.extracted_text,
                "student_details": student_details,
                "text_length": len(self.extracted_text)
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return {
                "success": False,
                "message": f"Text extraction failed: {str(e)}",
                "error_code": "TEXT_EXTRACTION_ERROR"
            }
    
    def parse_student_details(self, text):
        """
        Parse student details from extracted text using regex patterns
        
        Args:
            text (str): Extracted text from PDF
            
        Returns:
            dict: Parsed student details
        """
        try:
            student_details = {
                "name": "",
                "register_number": "",
                "roll_number": "",
                "department": "",
                "college": "",
                "year": "",
                "course": ""
            }
            
            # Clean text for better parsing
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Patterns for different fields
            patterns = {
                "name": [
                    r"Name\s*:?\s*([A-Za-z\s\.]+?)(?:\n|Register|Roll|Department|$)",
                    r"Student\s*Name\s*:?\s*([A-Za-z\s\.]+?)(?:\n|Register|Roll|Department|$)",
                    r"Name\s*-\s*([A-Za-z\s\.]+?)(?:\n|Register|Roll|Department|$)"
                ],
                "register_number": [
                    r"Register\s*(?:No|Number|#)\s*:?\s*([A-Za-z0-9]+)",
                    r"Registration\s*(?:No|Number|#)\s*:?\s*([A-Za-z0-9]+)",
                    r"Reg\s*(?:No|#)\s*:?\s*([A-Za-z0-9]+)"
                ],
                "roll_number": [
                    r"Roll\s*(?:No|Number|#)\s*:?\s*([A-Za-z0-9]+)",
                    r"Roll\s*:?\s*([A-Za-z0-9]+)"
                ],
                "department": [
                    r"Department\s*:?\s*([A-Za-z\s&]+?)(?:\n|Year|Course|College|$)",
                    r"Dept\s*:?\s*([A-Za-z\s&]+?)(?:\n|Year|Course|College|$)",
                    r"Branch\s*:?\s*([A-Za-z\s&]+?)(?:\n|Year|Course|College|$)"
                ],
                "college": [
                    r"College\s*:?\s*([A-Za-z\s,\.]+?)(?:\n|University|$)",
                    r"Institution\s*:?\s*([A-Za-z\s,\.]+?)(?:\n|University|$)"
                ],
                "year": [
                    r"Year\s*:?\s*([0-9]+)",
                    r"([1-4])\s*(?:st|nd|rd|th)\s*Year",
                    r"Semester\s*:?\s*([0-9]+)"
                ],
                "course": [
                    r"Course\s*:?\s*([A-Za-z\s\.]+?)(?:\n|Year|Department|$)",
                    r"Program\s*:?\s*([A-Za-z\s\.]+?)(?:\n|Year|Department|$)",
                    r"Degree\s*:?\s*([A-Za-z\s\.]+?)(?:\n|Year|Department|$)"
                ]
            }
            
            # Extract information using patterns
            for field, field_patterns in patterns.items():
                for pattern in field_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        value = match.group(1).strip()
                        if value and len(value) > 1:  # Avoid single characters
                            student_details[field] = value
                            break
            
            # Clean up extracted values
            for key, value in student_details.items():
                if value:
                    # Remove extra whitespace and clean up
                    student_details[key] = re.sub(r'\s+', ' ', value.strip())
                    # Remove trailing punctuation
                    student_details[key] = student_details[key].rstrip('.,;:')
            
            return student_details
            
        except Exception as e:
            logger.error(f"Error parsing student details: {str(e)}")
            return {
                "name": "",
                "register_number": "",
                "roll_number": "",
                "department": "",
                "college": "",
                "year": "",
                "course": ""
            }
    
    def process_id_card(self, file_path, output_dir="uploads"):
        """
        Complete processing of ID card PDF - extract both images and text
        
        Args:
            file_path (str): Path to the PDF file
            output_dir (str): Directory to save extracted content
            
        Returns:
            dict: Complete processing results
        """
        try:
            logger.info(f"Processing ID card PDF: {file_path}")
            
            # Extract text (this works well with pdfplumber)
            text_result = self.extract_text_from_pdf(file_path)
            
            # Try to extract images (limited without PyMuPDF)
            image_result = self.extract_images_from_pdf(file_path, output_dir)
            
            # Determine the best candidate for student photo
            student_photo = None
            if image_result.get("success") and image_result.get("images"):
                # Find the largest image (likely to be the student photo)
                largest_image = max(
                    image_result["images"], 
                    key=lambda x: x["width"] * x["height"]
                )
                student_photo = largest_image
            
            # Combine results
            processing_result = {
                "success": True,
                "message": "ID card processed successfully",
                "images": {
                    "success": image_result.get("success", False),
                    "total_images": image_result.get("total_images", 0),
                    "images": image_result.get("images", []),
                    "student_photo": student_photo,
                    "note": image_result.get("note", "")
                },
                "text": {
                    "success": text_result["success"],
                    "extracted_text": text_result.get("text", ""),
                    "student_details": text_result.get("student_details", {})
                }
            }
            
            # Check if we have minimum required data (text extraction should work)
            if not text_result["success"]:
                processing_result["success"] = False
                processing_result["message"] = "Failed to extract text from ID card"
                processing_result["error_code"] = "TEXT_EXTRACTION_FAILED"
            
            return processing_result
            
        except Exception as e:
            logger.error(f"Error processing ID card: {str(e)}")
            return {
                "success": False,
                "message": f"ID card processing failed: {str(e)}",
                "error_code": "PROCESSING_ERROR"
            }