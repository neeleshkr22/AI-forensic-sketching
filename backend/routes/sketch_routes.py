"""
API Routes for Sketch Operations
"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import logging
from services.matching_service import SketchMatchingService
from services.generation_service import SketchGenerationService
from database.repository import SearchHistoryRepository
from config import Config
import uuid

logger = logging.getLogger(__name__)

bp = Blueprint('sketch', __name__)

# Initialize services
matching_service = SketchMatchingService()
generation_service = SketchGenerationService()
search_history_repo = SearchHistoryRepository()

@bp.route('/generate', methods=['POST'])
def generate_sketch():
    """
    Generate sketch from text prompt
    
    Request Body:
        {
            "prompt": "description of person",
            "user_id": "optional user identifier"
        }
    
    Returns:
        Generated sketch information
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
        
        prompt = data['prompt']
        user_id = data.get('user_id')
        
        logger.info(f"Generating sketch from prompt: {prompt}")
        
        # Generate sketch
        result = generation_service.generate_from_prompt(prompt, user_id=user_id)
        
        return jsonify({
            'success': True,
            'sketch_id': result['sketch_id'],
            'sketch_url': result['sketch_url'],
            'prompt': result['prompt'],
            'generation_method': result['generation_method']
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating sketch: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/compose', methods=['POST'])
def compose_sketch():
    """
    Compose sketch from drag-and-drop components
    
    Request Body:
        {
            "components": [
                {
                    "image_path": "path/to/component",
                    "position": [x, y],
                    "scale": 1.0,
                    "rotation": 0
                }
            ],
            "user_id": "optional user identifier"
        }
    
    Returns:
        Composed sketch information
    """
    try:
        data = request.get_json()
        
        if not data or 'components' not in data:
            return jsonify({'error': 'Components are required'}), 400
        
        components = data['components']
        user_id = data.get('user_id')
        
        logger.info(f"Composing sketch from {len(components)} components")
        
        # Compose sketch
        result = generation_service.compose_from_components(
            components,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'sketch_id': result['sketch_id'],
            'sketch_url': result['sketch_url'],
            'num_components': result['num_components'],
            'generation_method': result['generation_method']
        }), 200
        
    except Exception as e:
        logger.error(f"Error composing sketch: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/upload', methods=['POST'])
def upload_sketch():
    """
    Upload sketch image
    
    Form Data:
        file: Image file
        user_id: Optional user identifier
    
    Returns:
        Uploaded sketch information
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not Config.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        sketch_id = str(uuid.uuid4())
        file_ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"sketch_{sketch_id}.{file_ext}"
        
        upload_path = os.path.join(Config.UPLOAD_FOLDER, 'sketches', new_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        
        file.save(upload_path)
        
        logger.info(f"Sketch uploaded: {upload_path}")
        
        return jsonify({
            'success': True,
            'sketch_id': sketch_id,
            'sketch_url': upload_path,
            'filename': new_filename
        }), 200
        
    except Exception as e:
        logger.error(f"Error uploading sketch: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['POST'])
def search_with_sketch():
    """
    Search database with sketch
    
    Request Body (JSON):
        {
            "sketch_url": "path/to/sketch",
            "top_k": 10,
            "threshold": 0.5,
            "user_id": "optional"
        }
    
    OR Form Data:
        file: Sketch image
        top_k: Number of results
        threshold: Confidence threshold
    
    Returns:
        Matching results
    """
    try:
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save temporarily
            sketch_id = str(uuid.uuid4())
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            temp_filename = f"temp_sketch_{sketch_id}.{file_ext}"
            temp_path = os.path.join(Config.UPLOAD_FOLDER, 'temp', temp_filename)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            file.save(temp_path)
            sketch_url = temp_path
            
            top_k = int(request.form.get('top_k', 10))
            threshold = float(request.form.get('threshold', 0.5))
            user_id = request.form.get('user_id')
            
        # Handle JSON request
        else:
            data = request.get_json()
            
            if not data or 'sketch_url' not in data:
                return jsonify({'error': 'Sketch URL or file is required'}), 400
            
            sketch_url = data['sketch_url']
            top_k = data.get('top_k', 10)
            threshold = data.get('threshold', 0.5)
            user_id = data.get('user_id')
        
        logger.info(f"Searching database with sketch: {sketch_url}")
        
        # Perform matching
        result = matching_service.match_sketch(
            sketch_url,
            top_k=top_k,
            threshold=threshold,
            save_processed=False
        )
        
        # Save search history
        try:
            search_data = {
                'sketch_id': str(uuid.uuid4()),
                'sketch_url': sketch_url,
                'results': result['matches'],
                'total_matches': result['total_matches'],
                'search_time': result['search_time'],
                'user_id': user_id
            }
            search_history_repo.create(search_data)
        except Exception as e:
            logger.warning(f"Failed to save search history: {str(e)}")
        
        return jsonify({
            'success': True,
            'matches': result['matches'],
            'total_matches': result['total_matches'],
            'search_time': result['search_time'],
            'threshold': threshold
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching with sketch: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/recent', methods=['GET'])
def get_recent_sketches():
    """Get recent sketches"""
    try:
        user_id = request.args.get('user_id')
        limit = int(request.args.get('limit', 20))
        
        sketches = generation_service.get_recent_sketches(user_id=user_id, limit=limit)
        
        return jsonify({
            'success': True,
            'sketches': sketches,
            'count': len(sketches)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching recent sketches: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/image/<sketch_id>', methods=['GET'])
def get_sketch_image(sketch_id):
    """Get sketch image file"""
    try:
        # Find sketch file
        sketch_path = os.path.join(Config.UPLOAD_FOLDER, 'sketches', f"sketch_{sketch_id}.png")
        
        if not os.path.exists(sketch_path):
            # Try other extensions
            for ext in ['jpg', 'jpeg', 'gif']:
                alt_path = sketch_path.replace('.png', f'.{ext}')
                if os.path.exists(alt_path):
                    sketch_path = alt_path
                    break
        
        if not os.path.exists(sketch_path):
            return jsonify({'error': 'Sketch not found'}), 404
        
        return send_file(sketch_path, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Error retrieving sketch image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/status', methods=['GET'])
def get_service_status():
    """Get sketch service status"""
    try:
        status = matching_service.get_service_status()
        
        return jsonify({
            'success': True,
            'status': status
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting service status: {str(e)}")
        return jsonify({'error': str(e)}), 500
