"""
API Routes for Criminal Record Management
"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import logging
from database.repository import RecordRepository
from services.matching_service import SketchMatchingService
from config import Config
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

bp = Blueprint('records', __name__)

# Initialize services
record_repo = RecordRepository()
matching_service = SketchMatchingService()

@bp.route('/', methods=['GET'])
def get_all_records():
    """
    Get all criminal records with pagination
    
    Query Parameters:
        skip: Number of records to skip (default: 0)
        limit: Maximum records to return (default: 100)
        status: Filter by status (active, caught, inactive)
        crime_type: Filter by crime type
    
    Returns:
        List of records
    """
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))
        
        # Build filters
        filters = {}
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('crime_type'):
            filters['crime_type'] = request.args.get('crime_type')
        
        records = record_repo.get_all(skip=skip, limit=limit, filters=filters)
        total = record_repo.count(filters=filters)
        
        return jsonify({
            'success': True,
            'records': records,
            'count': len(records),
            'total': total,
            'skip': skip,
            'limit': limit
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching records: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<record_id>', methods=['GET'])
def get_record(record_id):
    """Get single record by ID"""
    try:
        record = record_repo.get_by_id(record_id)
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        return jsonify({
            'success': True,
            'record': record
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_record():
    """
    Create new criminal record
    
    Form Data or JSON:
        name: Full name (required)
        age: Age
        gender: Gender
        height: Height in cm
        weight: Weight in kg
        eye_color: Eye color
        hair_color: Hair color
        crime_type: Type of crime
        crime_date: Date of crime
        location: Location
        description: Additional details
        photo: Photo file (form data)
    
    Returns:
        Created record information
    """
    try:
        # Handle multipart form data (with file)
        if request.content_type.startswith('multipart/form-data'):
            data = request.form.to_dict()
            photo_file = request.files.get('photo')
        else:
            # JSON data
            data = request.get_json()
            photo_file = None
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        # Generate record ID
        record_id = str(uuid.uuid4())
        
        # Handle photo upload
        photo_url = None
        if photo_file and photo_file.filename:
            if Config.allowed_file(photo_file.filename):
                filename = secure_filename(photo_file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f"record_{record_id}.{file_ext}"
                
                photo_path = os.path.join(Config.UPLOAD_FOLDER, 'records', new_filename)
                os.makedirs(os.path.dirname(photo_path), exist_ok=True)
                
                photo_file.save(photo_path)
                photo_url = photo_path
                
                logger.info(f"Photo saved: {photo_path}")
        
        # Create record data
        record_data = {
            'record_id': record_id,
            'name': data['name'],
            'age': int(data['age']) if data.get('age') else None,
            'gender': data.get('gender'),
            'height': float(data['height']) if data.get('height') else None,
            'weight': float(data['weight']) if data.get('weight') else None,
            'eye_color': data.get('eye_color'),
            'hair_color': data.get('hair_color'),
            'crime_type': data.get('crime_type'),
            'crime_date': datetime.fromisoformat(data['crime_date']) if data.get('crime_date') else None,
            'location': data.get('location'),
            'status': data.get('status', 'active'),
            'description': data.get('description'),
            'aliases': data.get('aliases', '').split(',') if data.get('aliases') else [],
            'tattoos': data.get('tattoos', '').split(',') if data.get('tattoos') else [],
            'scars': data.get('scars', '').split(',') if data.get('scars') else [],
            'photo_url': photo_url,
            'created_by': data.get('created_by', 'system')
        }
        
        # Create record
        created_id = record_repo.create(record_data)
        
        # Extract and store features if photo available
        if photo_url:
            try:
                features = matching_service.extract_and_store_features(record_id, photo_url)
                logger.info(f"Features extracted for record {record_id}")
            except Exception as e:
                logger.warning(f"Failed to extract features: {str(e)}")
        
        logger.info(f"Record created: {record_id}")
        
        return jsonify({
            'success': True,
            'record_id': record_id,
            'message': 'Record created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<record_id>', methods=['PUT'])
def update_record(record_id):
    """Update existing record"""
    try:
        # Handle multipart form data
        if request.content_type.startswith('multipart/form-data'):
            data = request.form.to_dict()
            photo_file = request.files.get('photo')
        else:
            data = request.get_json()
            photo_file = None
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if record exists
        existing = record_repo.get_by_id(record_id)
        if not existing:
            return jsonify({'error': 'Record not found'}), 404
        
        # Handle photo update
        if photo_file and photo_file.filename:
            if Config.allowed_file(photo_file.filename):
                filename = secure_filename(photo_file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f"record_{record_id}.{file_ext}"
                
                photo_path = os.path.join(Config.UPLOAD_FOLDER, 'records', new_filename)
                os.makedirs(os.path.dirname(photo_path), exist_ok=True)
                
                photo_file.save(photo_path)
                data['photo_url'] = photo_path
                
                # Re-extract features
                try:
                    matching_service.extract_and_store_features(record_id, photo_path)
                except Exception as e:
                    logger.warning(f"Failed to update features: {str(e)}")
        
        # Clean data
        update_data = {k: v for k, v in data.items() if v is not None and k != 'record_id'}
        
        # Update record
        success = record_repo.update(record_id, update_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Record updated successfully'
            }), 200
        else:
            return jsonify({'error': 'Update failed'}), 500
        
    except Exception as e:
        logger.error(f"Error updating record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete record"""
    try:
        # Check if record exists
        existing = record_repo.get_by_id(record_id)
        if not existing:
            return jsonify({'error': 'Record not found'}), 404
        
        # Delete associated files
        if existing.get('photo_url'):
            try:
                if os.path.exists(existing['photo_url']):
                    os.remove(existing['photo_url'])
            except Exception as e:
                logger.warning(f"Failed to delete photo file: {str(e)}")
        
        # Delete record
        success = record_repo.delete(record_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Record deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Delete failed'}), 500
        
    except Exception as e:
        logger.error(f"Error deleting record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['GET'])
def search_records():
    """
    Search records by name
    
    Query Parameters:
        q: Search query
    
    Returns:
        Matching records
    """
    try:
        query = request.args.get('q')
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        records = record_repo.search_by_name(query)
        
        return jsonify({
            'success': True,
            'records': records,
            'count': len(records),
            'query': query
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching records: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/photo/<record_id>', methods=['GET'])
def get_record_photo(record_id):
    """Get record photo"""
    try:
        record = record_repo.get_by_id(record_id)
        
        if not record or not record.get('photo_url'):
            return jsonify({'error': 'Photo not found'}), 404
        
        photo_path = record['photo_url']
        
        if not os.path.exists(photo_path):
            return jsonify({'error': 'Photo file not found'}), 404
        
        return send_file(photo_path, mimetype='image/jpeg')
        
    except Exception as e:
        logger.error(f"Error retrieving photo: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/stats', methods=['GET'])
def get_statistics():
    """Get database statistics"""
    try:
        total = record_repo.count()
        active = record_repo.count({'status': 'active'})
        caught = record_repo.count({'status': 'caught'})
        
        return jsonify({
            'success': True,
            'stats': {
                'total_records': total,
                'active': active,
                'caught': caught,
                'inactive': total - active - caught
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({'error': str(e)}), 500
