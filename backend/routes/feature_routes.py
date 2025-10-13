"""
API Routes for Feature Extraction and AI Operations
"""
from flask import Blueprint, request, jsonify
import os
import logging
from services.matching_service import SketchMatchingService
from utils.image_processing import ImageProcessor
from config import Config

logger = logging.getLogger(__name__)

bp = Blueprint('features', __name__)

# Initialize services
matching_service = SketchMatchingService()
image_processor = ImageProcessor()

@bp.route('/extract', methods=['POST'])
def extract_features():
    """
    Extract facial features from image
    
    Form Data:
        file: Image file
    
    OR JSON:
        image_url: Path to image
    
    Returns:
        Feature vector
    """
    try:
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not Config.allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            # Save temporarily
            import uuid
            temp_filename = f"temp_{uuid.uuid4()}.png"
            temp_path = os.path.join(Config.UPLOAD_FOLDER, 'temp', temp_filename)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            file.save(temp_path)
            image_path = temp_path
            
        # Handle JSON request
        else:
            data = request.get_json()
            
            if not data or 'image_url' not in data:
                return jsonify({'error': 'Image file or URL required'}), 400
            
            image_path = data['image_url']
        
        # Extract features
        from PIL import Image
        image = Image.open(image_path)
        features = matching_service.cnn_extractor.extract_features(image)
        
        # Clean up temp file
        if 'temp_' in image_path:
            try:
                os.remove(image_path)
            except:
                pass
        
        return jsonify({
            'success': True,
            'features': features.tolist(),
            'feature_dim': len(features)
        }), 200
        
    except Exception as e:
        logger.error(f"Error extracting features: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/detect-face', methods=['POST'])
def detect_face():
    """
    Detect face in image
    
    Form Data:
        file: Image file
    
    Returns:
        Face detection result
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save temporarily
        import uuid
        temp_filename = f"temp_{uuid.uuid4()}.png"
        temp_path = os.path.join(Config.UPLOAD_FOLDER, 'temp', temp_filename)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        
        file.save(temp_path)
        
        # Detect face
        from PIL import Image
        image = Image.open(temp_path)
        face_bbox = image_processor.detect_face(image)
        
        # Clean up
        try:
            os.remove(temp_path)
        except:
            pass
        
        if face_bbox:
            x, y, w, h = face_bbox
            return jsonify({
                'success': True,
                'face_detected': True,
                'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
            }), 200
        else:
            return jsonify({
                'success': True,
                'face_detected': False,
                'bbox': None
            }), 200
        
    except Exception as e:
        logger.error(f"Error detecting face: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/photo-to-sketch', methods=['POST'])
def photo_to_sketch():
    """
    Convert photo to sketch
    
    Form Data:
        file: Photo file
    
    Returns:
        Sketch image URL
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save photo
        import uuid
        photo_id = str(uuid.uuid4())
        photo_filename = f"photo_{photo_id}.png"
        photo_path = os.path.join(Config.UPLOAD_FOLDER, 'temp', photo_filename)
        os.makedirs(os.path.dirname(photo_path), exist_ok=True)
        
        file.save(photo_path)
        
        # Convert to sketch
        from PIL import Image
        image = Image.open(photo_path)
        sketch = image_processor.convert_to_sketch(image)
        
        # Save sketch
        sketch_filename = f"sketch_{photo_id}.png"
        sketch_path = os.path.join(Config.UPLOAD_FOLDER, 'sketches', sketch_filename)
        os.makedirs(os.path.dirname(sketch_path), exist_ok=True)
        
        sketch.save(sketch_path)
        
        # Clean up photo
        try:
            os.remove(photo_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'sketch_url': sketch_path,
            'sketch_id': photo_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error converting photo to sketch: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/enhance', methods=['POST'])
def enhance_image():
    """
    Enhance image quality
    
    Form Data or JSON:
        file: Image file (form data)
        image_url: Image path (JSON)
    
    Returns:
        Enhanced image URL
    """
    try:
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save temporarily
            import uuid
            temp_filename = f"temp_{uuid.uuid4()}.png"
            temp_path = os.path.join(Config.UPLOAD_FOLDER, 'temp', temp_filename)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            file.save(temp_path)
            image_path = temp_path
            
        else:
            data = request.get_json()
            
            if not data or 'image_url' not in data:
                return jsonify({'error': 'Image required'}), 400
            
            image_path = data['image_url']
        
        # Enhance image
        from PIL import Image
        image = Image.open(image_path)
        
        # Apply enhancements
        enhanced = image_processor.enhance_contrast(image)
        enhanced = image_processor.denoise(enhanced)
        
        # Save enhanced image
        import uuid
        enhanced_id = str(uuid.uuid4())
        enhanced_filename = f"enhanced_{enhanced_id}.png"
        enhanced_path = os.path.join(Config.UPLOAD_FOLDER, 'enhanced', enhanced_filename)
        os.makedirs(os.path.dirname(enhanced_path), exist_ok=True)
        
        enhanced.save(enhanced_path)
        
        # Clean up temp file
        if 'temp_' in image_path:
            try:
                os.remove(image_path)
            except:
                pass
        
        return jsonify({
            'success': True,
            'enhanced_url': enhanced_path,
            'enhanced_id': enhanced_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error enhancing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/model-info', methods=['GET'])
def get_model_info():
    """Get AI model information"""
    try:
        service_status = matching_service.get_service_status()
        svm_info = matching_service.svm_matcher.get_model_info()
        
        return jsonify({
            'success': True,
            'models': {
                'cnn': {
                    'loaded': service_status['cnn_loaded'],
                    'architecture': 'FaceNet (InceptionResnetV1)',
                    'feature_dim': 512
                },
                'svm': {
                    'trained': service_status['svm_trained'],
                    'info': svm_info
                },
                'gan': {
                    'available': service_status['gan_available'],
                    'architecture': 'pix2pix U-Net'
                }
            },
            'database': {
                'total_records': service_status['total_records']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return jsonify({'error': str(e)}), 500
