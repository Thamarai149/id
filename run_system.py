"""
System Runner Script for Face Verification System
Provides an interactive way to run and test the complete system

Usage: python run_system.py
"""

import os
import sys
import time
import subprocess
import requests
import json
from datetime import datetime

class FaceVerificationSystemRunner:
    """
    Interactive system runner for the Face Verification System
    """
    
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.server_process = None
        self.camera_image_path = None
        self.id_card_image_path = None
        self.student_details = {}
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"🎯 {title}")
        print("="*60)
    
    def print_step(self, step_num, description):
        """Print formatted step"""
        print(f"\n📋 Step {step_num}: {description}")
        print("-" * 40)
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        self.print_header("Checking Dependencies")
        
        required_packages = [
            'flask', 'opencv-python', 'face-recognition', 
            'PyMuPDF', 'pdfplumber', 'numpy', 'Pillow'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"✅ {package} - OK")
            except ImportError:
                print(f"❌ {package} - MISSING")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
            print("Please install them using: pip install -r requirements.txt")
            return False
        
        print("\n✅ All dependencies are installed!")
        return True
    
    def start_server(self):
        """Start the Flask server"""
        self.print_header("Starting Server")
        
        try:
            # Check if server is already running
            response = requests.get(f"{self.base_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server is already running!")
                return True
        except:
            pass
        
        print("🚀 Starting Flask server...")
        print("Server will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop the server when done")
        
        # Start server in background
        try:
            self.server_process = subprocess.Popen([
                sys.executable, "app.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            for i in range(10):
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=1)
                    if response.status_code == 200:
                        print("✅ Server started successfully!")
                        return True
                except:
                    time.sleep(1)
                    print(f"⏳ Waiting for server... ({i+1}/10)")
            
            print("❌ Server failed to start within 10 seconds")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def test_camera(self):
        """Test camera functionality"""
        self.print_step(1, "Testing Camera")
        
        try:
            # Initialize camera
            response = requests.post(f"{self.base_url}/api/start-camera")
            if response.status_code != 200:
                print("❌ Camera initialization failed")
                print(response.json().get('message', 'Unknown error'))
                return False
            
            print("✅ Camera initialized successfully")
            
            # Test camera
            response = requests.post(f"{self.base_url}/api/test-camera")
            if response.status_code == 200:
                print("✅ Camera test passed")
                return True
            else:
                print("⚠️  Camera test failed, but you can still try manual capture")
                return True
                
        except Exception as e:
            print(f"❌ Camera test failed: {e}")
            return False
    
    def capture_face(self):
        """Capture face from camera"""
        self.print_step(2, "Capturing Live Face")
        
        print("📷 This will open your camera window")
        print("Instructions:")
        print("  - Position your face clearly in the frame")
        print("  - Press 'C' key to capture your face")
        print("  - Press 'Q' key to quit without capturing")
        
        proceed = input("\n🤔 Ready to capture your face? (y/n): ").lower()
        if proceed != 'y':
            print("⏭️  Face capture skipped")
            return False
        
        try:
            response = requests.post(f"{self.base_url}/api/capture-face")
            
            if response.status_code == 200:
                data = response.json()['data']
                self.camera_image_path = data['image_path']
                print(f"✅ Face captured successfully!")
                print(f"📁 Saved to: {self.camera_image_path}")
                return True
            else:
                print("❌ Face capture failed")
                print(response.json().get('message', 'Unknown error'))
                return False
                
        except Exception as e:
            print(f"❌ Face capture failed: {e}")
            return False
    
    def upload_id_card(self):
        """Upload and process ID card PDF"""
        self.print_step(3, "Uploading ID Card PDF")
        
        print("📄 Please prepare your college ID card in PDF format")
        
        # Get PDF file path from user
        while True:
            pdf_path = input("📁 Enter path to your ID card PDF file: ").strip()
            
            if not pdf_path:
                print("⏭️  ID card upload skipped")
                return False
            
            if not os.path.exists(pdf_path):
                print(f"❌ File not found: {pdf_path}")
                continue
            
            if not pdf_path.lower().endswith('.pdf'):
                print("❌ Please provide a PDF file")
                continue
            
            break
        
        try:
            # Upload PDF
            with open(pdf_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.base_url}/api/upload-id-card", files=files)
            
            if response.status_code == 200:
                data = response.json()['data']
                processing_results = data['processing_results']
                
                print("✅ ID card processed successfully!")
                
                # Extract student photo path
                if processing_results['images']['success']:
                    student_photo = processing_results['images']['student_photo']
                    if student_photo:
                        self.id_card_image_path = student_photo['path']
                        print(f"📸 Student photo extracted: {student_photo['filename']}")
                
                # Extract student details
                if processing_results['text']['success']:
                    self.student_details = processing_results['text']['student_details']
                    print("📋 Student details extracted:")
                    for key, value in self.student_details.items():
                        if value:
                            print(f"  - {key.replace('_', ' ').title()}: {value}")
                
                return True
            else:
                print("❌ ID card processing failed")
                print(response.json().get('message', 'Unknown error'))
                return False
                
        except Exception as e:
            print(f"❌ ID card upload failed: {e}")
            return False
    
    def verify_identity(self):
        """Perform identity verification"""
        self.print_step(4, "Verifying Identity")
        
        if not self.camera_image_path:
            print("❌ No camera image available. Please capture face first.")
            return False
        
        if not self.id_card_image_path:
            print("❌ No ID card image available. Please upload ID card first.")
            return False
        
        try:
            # Prepare verification request
            verification_data = {
                "camera_image_path": self.camera_image_path,
                "id_card_image_path": self.id_card_image_path,
                "student_details": self.student_details
            }
            
            print("🔍 Comparing faces...")
            print(f"📷 Live image: {self.camera_image_path}")
            print(f"🆔 ID card image: {self.id_card_image_path}")
            
            response = requests.post(
                f"{self.base_url}/api/verify",
                json=verification_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()['data']
                
                print("\n🎉 VERIFICATION RESULTS")
                print("=" * 40)
                print(f"Result: {data['result']}")
                print(f"Confidence: {data['confidence']}")
                print(f"Recommendation: {data['verification_details'].get('recommendation', 'N/A')}")
                
                if data['student_details']:
                    print("\n👤 Student Information:")
                    for key, value in data['student_details'].items():
                        if value:
                            print(f"  - {key.replace('_', ' ').title()}: {value}")
                
                # Determine success
                is_verified = data['result'] == 'Verified'
                if is_verified:
                    print("\n✅ IDENTITY VERIFIED SUCCESSFULLY!")
                else:
                    print("\n❌ IDENTITY VERIFICATION FAILED")
                
                return is_verified
            else:
                print("❌ Verification failed")
                print(response.json().get('message', 'Unknown error'))
                return False
                
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        self.print_header("Cleanup")
        
        try:
            # Release camera
            requests.post(f"{self.base_url}/api/release-camera")
            print("✅ Camera resources released")
        except:
            pass
        
        # Stop server if we started it
        if self.server_process:
            print("🛑 Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
            print("✅ Server stopped")
    
    def run_complete_workflow(self):
        """Run the complete face verification workflow"""
        self.print_header("Live Face Detection and ID Card Verification System")
        print("🎓 College Final Year Project")
        print("🤖 AI/ML Full Stack Implementation")
        
        try:
            # Check dependencies
            if not self.check_dependencies():
                return False
            
            # Start server
            if not self.start_server():
                return False
            
            # Run workflow steps
            steps = [
                ("Test Camera", self.test_camera),
                ("Capture Face", self.capture_face),
                ("Upload ID Card", self.upload_id_card),
                ("Verify Identity", self.verify_identity)
            ]
            
            results = []
            for step_name, step_func in steps:
                try:
                    result = step_func()
                    results.append((step_name, result))
                    
                    if not result:
                        print(f"\n⚠️  {step_name} failed or was skipped")
                        continue_anyway = input("Continue with next step? (y/n): ").lower()
                        if continue_anyway != 'y':
                            break
                except Exception as e:
                    print(f"❌ {step_name} failed with error: {e}")
                    results.append((step_name, False))
            
            # Print final summary
            self.print_header("WORKFLOW SUMMARY")
            
            for step_name, success in results:
                status = "✅ COMPLETED" if success else "❌ FAILED/SKIPPED"
                print(f"{status} - {step_name}")
            
            successful_steps = sum(1 for _, success in results if success)
            total_steps = len(results)
            
            print(f"\n📊 Completed: {successful_steps}/{total_steps} steps")
            
            if successful_steps == total_steps:
                print("\n🎉 SYSTEM TEST COMPLETED SUCCESSFULLY!")
                print("✅ Your Face Verification System is working perfectly!")
            else:
                print("\n⚠️  Some steps failed or were skipped")
                print("💡 Review the errors above and try again")
            
            return successful_steps == total_steps
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Workflow interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Workflow failed: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Main function"""
    print("🚀 Face Verification System Runner")
    print("This script will guide you through testing the complete system")
    
    runner = FaceVerificationSystemRunner()
    
    try:
        success = runner.run_complete_workflow()
        
        if success:
            print("\n🎓 Congratulations! Your college project is working perfectly!")
            print("📚 You can now demonstrate all the features:")
            print("  - Live camera face capture")
            print("  - PDF ID card processing")
            print("  - Advanced face recognition")
            print("  - Complete verification workflow")
        else:
            print("\n🔧 Some issues were encountered.")
            print("📖 Check the README.md for troubleshooting tips")
        
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("📖 Please check the README.md for help")
    
    print("\n👋 Thank you for using the Face Verification System!")

if __name__ == "__main__":
    main()