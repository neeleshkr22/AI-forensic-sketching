"""
Database Repository Pattern - CRUD Operations
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
import logging
from database.db import get_db
from database.models import CriminalRecord, SketchRecord, SearchHistory

logger = logging.getLogger(__name__)

class RecordRepository:
    """Repository for Criminal Records"""
    
    def __init__(self):
        self.collection = get_db().get_collection('criminal_records')
    
    def create(self, record: Dict[str, Any]) -> str:
        """Create a new criminal record"""
        try:
            record['created_at'] = datetime.utcnow()
            record['updated_at'] = datetime.utcnow()
            result = self.collection.insert_one(record)
            logger.info(f"Created record: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating record: {str(e)}")
            raise
    
    def get_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Get record by ID"""
        try:
            record = self.collection.find_one({'record_id': record_id})
            if record:
                record['_id'] = str(record['_id'])
            return record
        except Exception as e:
            logger.error(f"Error fetching record: {str(e)}")
            return None
    
    def get_all(self, skip: int = 0, limit: int = 100, filters: Dict = None) -> List[Dict[str, Any]]:
        """Get all records with pagination"""
        try:
            query = filters or {}
            records = list(self.collection.find(query).skip(skip).limit(limit).sort('created_at', -1))
            for record in records:
                record['_id'] = str(record['_id'])
            return records
        except Exception as e:
            logger.error(f"Error fetching records: {str(e)}")
            return []
    
    def update(self, record_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a record"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'record_id': record_id},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating record: {str(e)}")
            return False
    
    def delete(self, record_id: str) -> bool:
        """Delete a record"""
        try:
            result = self.collection.delete_one({'record_id': record_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting record: {str(e)}")
            return False
    
    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search records by name"""
        try:
            records = list(self.collection.find({
                '$text': {'$search': name}
            }).limit(50))
            for record in records:
                record['_id'] = str(record['_id'])
            return records
        except Exception as e:
            logger.error(f"Error searching records: {str(e)}")
            return []
    
    def get_all_feature_vectors(self) -> List[Dict[str, Any]]:
        """Get all records with feature vectors"""
        try:
            records = list(self.collection.find(
                {'feature_vector': {'$exists': True, '$ne': None}},
                {'record_id': 1, 'name': 1, 'feature_vector': 1, 'photo_url': 1}
            ))
            for record in records:
                record['_id'] = str(record['_id'])
            return records
        except Exception as e:
            logger.error(f"Error fetching feature vectors: {str(e)}")
            return []
    
    def count(self, filters: Dict = None) -> int:
        """Count records"""
        try:
            query = filters or {}
            return self.collection.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting records: {str(e)}")
            return 0

class SketchRepository:
    """Repository for Sketch Records"""
    
    def __init__(self):
        self.collection = get_db().get_collection('sketches')
    
    def create(self, sketch: Dict[str, Any]) -> str:
        """Create a new sketch record"""
        try:
            sketch['created_at'] = datetime.utcnow()
            result = self.collection.insert_one(sketch)
            logger.info(f"Created sketch: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating sketch: {str(e)}")
            raise
    
    def get_by_id(self, sketch_id: str) -> Optional[Dict[str, Any]]:
        """Get sketch by ID"""
        try:
            sketch = self.collection.find_one({'sketch_id': sketch_id})
            if sketch:
                sketch['_id'] = str(sketch['_id'])
            return sketch
        except Exception as e:
            logger.error(f"Error fetching sketch: {str(e)}")
            return None
    
    def get_recent(self, limit: int = 20, user_id: str = None) -> List[Dict[str, Any]]:
        """Get recent sketches"""
        try:
            query = {'user_id': user_id} if user_id else {}
            sketches = list(self.collection.find(query).limit(limit).sort('created_at', -1))
            for sketch in sketches:
                sketch['_id'] = str(sketch['_id'])
            return sketches
        except Exception as e:
            logger.error(f"Error fetching recent sketches: {str(e)}")
            return []

class SearchHistoryRepository:
    """Repository for Search History"""
    
    def __init__(self):
        self.collection = get_db().get_collection('search_history')
    
    def create(self, search: Dict[str, Any]) -> str:
        """Create search history entry"""
        try:
            search['timestamp'] = datetime.utcnow()
            result = self.collection.insert_one(search)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating search history: {str(e)}")
            raise
    
    def get_recent(self, limit: int = 50, user_id: str = None) -> List[Dict[str, Any]]:
        """Get recent searches"""
        try:
            query = {'user_id': user_id} if user_id else {}
            searches = list(self.collection.find(query).limit(limit).sort('timestamp', -1))
            for search in searches:
                search['_id'] = str(search['_id'])
            return searches
        except Exception as e:
            logger.error(f"Error fetching search history: {str(e)}")
            return []
