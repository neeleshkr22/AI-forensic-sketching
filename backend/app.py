"""
AI Criminal Sketch Matching System - Main Application
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from database.db import Database
from routes.sketch_routes import bp as sketch_bp
from routes.record_routes import bp as records_bp
from routes.feature_routes import bp as features_bp
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Setup CORS
CORS(app, resources={
    r"/api/*": {
        "origins": app.config['CORS_ORIGINS'].split(','),
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Setup logging
logger = setup_logger(__name__)

# Initialize database
db = Database()

# Create upload directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MODEL_PATH'], exist_ok=True)
os.makedirs('./logs', exist_ok=True)

# Register blueprints
app.register_blueprint(sketch_bp, url_prefix='/api/sketch')
app.register_blueprint(records_bp, url_prefix='/api/records')
app.register_blueprint(features_bp, url_prefix='/api/features')

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'AI Criminal Sketch Matching System API',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    """Detailed health check"""
    try:
        db_status = db.health_check()
        return jsonify({
            'status': 'healthy',
            'database': db_status,
            'models': {
                'cnn': os.path.exists(os.path.join(app.config['MODEL_PATH'], app.config['CNN_MODEL'])),
                'svm': os.path.exists(os.path.join(app.config['MODEL_PATH'], app.config['SVM_MODEL'])),
                'gan': os.path.exists(os.path.join(app.config['MODEL_PATH'], app.config['GAN_MODEL']))
            }
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting AI Criminal Sketch Matching System...")
    logger.info(f"Environment: {app.config['FLASK_ENV']}")
    logger.info(f"Database: {app.config['MONGODB_URI']}")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=False,
        use_reloader=False
    )
