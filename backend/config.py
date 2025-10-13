"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Database
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/sketch_db')
    DB_NAME = os.getenv('DB_NAME', 'sketch_db')
    
    # Hugging Face
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
    HUGGINGFACE_MODEL = os.getenv('HUGGINGFACE_MODEL', 'stabilityai/stable-diffusion-2-1')
    
    # File Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Model Configuration
    MODEL_PATH = os.getenv('MODEL_PATH', './models/saved')
    CNN_MODEL = os.getenv('CNN_MODEL', 'vggface_model.h5')
    SVM_MODEL = os.getenv('SVM_MODEL', 'svm_classifier.pkl')
    GAN_MODEL = os.getenv('GAN_MODEL', 'pix2pix_generator.pth')
    
    # Security
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000')
    
    # AI Configuration
    FEATURE_VECTOR_SIZE = int(os.getenv('FEATURE_VECTOR_SIZE', 2048))
    SVM_KERNEL = os.getenv('SVM_KERNEL', 'rbf')
    SVM_C = float(os.getenv('SVM_C', 1.0))
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.6))
    
    # Image Processing
    IMAGE_SIZE = int(os.getenv('IMAGE_SIZE', 256))
    SKETCH_SIZE = int(os.getenv('SKETCH_SIZE', 512))
    FACE_CASCADE_PATH = os.getenv('FACE_CASCADE_PATH', './models/haarcascade_frontalface_default.xml')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/app.log')
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGODB_URI = 'mongodb://localhost:27017/sketch_db_test'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
