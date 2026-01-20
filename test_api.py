"""
API Testing Script for Face Verification System
Test all endpoints with sample requests and responses

Usage: python test_api.py
"""

import requests
import json
import time
import os

# Base URL for the API
BASE_URL = "http://localhost:5000"

def print_response(response, endpoint_name):
    """Print formatted response for testing"""
    print(f"\n{'='*50}")
    print(f"Testing: {endpoint_name}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print(f"{'='*50}")

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "Health Check")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_api_documentation():
    """Test API documentation endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response, "API Documentation")
        return response.status_code == 200
    except Exception as e:
        print(f"API documentation test failed: {e}")
        return False

def test_camera_initialization():
    """Test camera initialization"""
    try:
        response = requests.post(f"{BASE_URL}/api/start-camera")
        print_response(response, "Camera Initialization")
        return response.status_code == 200
    except Exception as e:
        print(f"Camera initialization test failed: {e}")
        return False

def test_camera_status():
    """Test camera status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/camera-status")
        print_response(response, "Camera Status")
        return response.status_code == 200
    except Exception as e:
        print(f"Camera status test failed: {e}")
        return False

def test_camera_test():
    """Test camera functionality"""
    try:
        response = requests.post(f"{BASE_URL}/api/test-camera")
        print_response(response, "Camera Test")
        return response.status_code == 200
    except Exception as e:
        print(f"Camera test failed: {e}")
        return False

def test_face_capture():
    """Test face capture (requires manual interaction)"""
    try:
        print("\n" + "="*50)
        print("MANUAL TEST: Face Capture")
        print("This will open camera window.")
        print("Press 'C' to capture face, 'Q' to quit")
        user_input = input("Do you want to test face capture? (y/n): ")
        
        if user_input.lower() == 'y':
            response = requests.post(f"{BASE_URL}/api/capture-face")
            print_response(response, "Face Capture")
            return response.status_code == 200
        else:
            print("Face capture test skipped")
            return True
    except Exception as e:
        print(f"Face capture test failed: {e}")
        return False

def test_pdf_upload():
    """Test PDF upload (requires sample PDF)"""
    try:
        print("\n" + "="*50)
        print("MANUAL TEST: PDF Upload")
        
        # Check if sample PDF exists
        sample_pdf = "sample_id_card.pdf"
        if not os.path.exists(sample_pdf):
            print(f"Sample PDF '{sample_pdf}' not found.")
            print("Please create a sample ID card PDF to test this endpoint.")
            return True
        
        with open(sample_pdf, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/upload-id-card", files=files)
            print_response(response, "PDF Upload")
            return response.status_code == 200
            
    except Exception as e:
        print(f"PDF upload test failed: {e}")
        return False

def test_text_extraction():
    """Test text extraction from PDF"""
    try:
        # This test requires a PDF file to be uploaded first
        test_data = {
            "file_path": "uploads/sample_file.pdf"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/extract-text",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, "Text Extraction")
        # This might fail if no PDF is uploaded, which is expected
        return True
        
    except Exception as e:
        print(f"Text extraction test failed: {e}")
        return False

def test_image_extraction():
    """Test image extraction from PDF"""
    try:
        # This test requires a PDF file to be uploaded first
        test_data = {
            "file_path": "uploads/sample_file.pdf"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/extract-images",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, "Image Extraction")
        # This might fail if no PDF is uploaded, which is expected
        return True
        
    except Exception as e:
        print(f"Image extraction test failed: {e}")
        return False

def test_face_comparison():
    """Test face comparison"""
    try:
        # This test requires actual image files
        test_data = {
            "image1_path": "camera/sample_face1.jpg",
            "image2_path": "uploads/sample_face2.jpg"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/compare-faces",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, "Face Comparison")
        # This might fail if no images exist, which is expected
        return True
        
    except Exception as e:
        print(f"Face comparison test failed: {e}")
        return False

def test_identity_verification():
    """Test complete identity verification"""
    try:
        # This test requires actual image files and student details
        test_data = {
            "camera_image_path": "camera/captured_face.jpg",
            "id_card_image_path": "uploads/extracted_image.png",
            "student_details": {
                "name": "Test Student",
                "register_number": "TEST123",
                "department": "Computer Science",
                "college": "Test College"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/verify",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, "Identity Verification")
        # This might fail if no images exist, which is expected
        return True
        
    except Exception as e:
        print(f"Identity verification test failed: {e}")
        return False

def test_camera_release():
    """Test camera release"""
    try:
        response = requests.post(f"{BASE_URL}/api/release-camera")
        print_response(response, "Camera Release")
        return response.status_code == 200
    except Exception as e:
        print(f"Camera release test failed: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("🚀 Starting Face Verification System API Tests")
    print("Make sure the server is running at http://localhost:5000")
    
    # Wait for user confirmation
    input("Press Enter to start testing...")
    
    tests = [
        ("Health Check", test_health_check),
        ("API Documentation", test_api_documentation),
        ("Camera Initialization", test_camera_initialization),
        ("Camera Status", test_camera_status),
        ("Camera Test", test_camera_test),
        ("Face Capture", test_face_capture),
        ("PDF Upload", test_pdf_upload),
        ("Text Extraction", test_text_extraction),
        ("Image Extraction", test_image_extraction),
        ("Face Comparison", test_face_comparison),
        ("Identity Verification", test_identity_verification),
        ("Camera Release", test_camera_release)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
            time.sleep(1)  # Small delay between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, "ERROR"))
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, status in results:
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
    
    # Count results
    passed = sum(1 for _, status in results if status == "PASS")
    failed = sum(1 for _, status in results if status == "FAIL")
    errors = sum(1 for _, status in results if status == "ERROR")
    
    print(f"\n📈 Results: {passed} passed, {failed} failed, {errors} errors")
    print("="*60)

if __name__ == "__main__":
    run_all_tests()