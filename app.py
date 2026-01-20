"""
Live Face Detection and College ID Card Verification System
Main Flask Application Entry Point

Author: AI/ML Full Stack Engineer
Purpose: College Final Year Project - Face Verification System
"""

from flask import Flask, request, jsonify, render_template
import os
import logging
from app.routes.camera_routes import camera_bp
from app.routes.verification_routes import verification_bp
from app.utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app():
    """
    Application factory pattern for creating Flask app
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['CAMERA_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(camera_bp, url_prefix='/api')
    app.register_blueprint(verification_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "Face Verification System is running"
        })
    
    # Root endpoint with API documentation
    @app.route('/')
    def index():
        return jsonify({
            "message": "Live Face Detection and College ID Card Verification System",
            "version": "1.0.0",
            "endpoints": {
                "POST /api/start-camera": "Initialize camera for face capture",
                "POST /api/capture-face": "Capture face from live camera",
                "POST /api/upload-id-card": "Upload college ID card PDF",
                "POST /api/verify": "Verify face against ID card"
            },
            "status": "active"
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Live Face Detection and ID Card Verification System...")
    print("📷 Make sure your camera is connected and working")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API Documentation available at: http://localhost:5000")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )