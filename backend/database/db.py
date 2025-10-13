"""
Database Connection and Management
"""
from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import ConnectionFailure, OperationFailure
import logging
from config import Config

logger = logging.getLogger(__name__)

class Database:
    """MongoDB Database Manager"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[Config.DB_NAME]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB: {Config.DB_NAME}")
            
            # Initialize collections and indexes
            self.initialize_collections()
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    def initialize_collections(self):
        """Create collections and indexes"""
        try:
            # Criminal Records Collection
            if 'records' not in self.db.list_collection_names():
                self.db.create_collection('records')
            
            records_collection = self.db.records
            
            # Create indexes
            records_collection.create_index([('name', TEXT)])
            records_collection.create_index([('record_id', ASCENDING)], unique=True)
            records_collection.create_index([('created_at', ASCENDING)])
            
            # Sketches Collection
            if 'sketches' not in self.db.list_collection_names():
                self.db.create_collection('sketches')
            
            sketches_collection = self.db.sketches
            sketches_collection.create_index([('created_at', ASCENDING)])
            sketches_collection.create_index([('user_id', ASCENDING)])
            
            # Search History Collection
            if 'search_history' not in self.db.list_collection_names():
                self.db.create_collection('search_history')
            
            search_collection = self.db.search_history
            search_collection.create_index([('timestamp', ASCENDING)])
            search_collection.create_index([('user_id', ASCENDING)])
            
            logger.info("Database collections and indexes initialized successfully")
            
        except OperationFailure as e:
            logger.error(f"Failed to initialize collections: {str(e)}")
    
    def health_check(self):
        """Check database health"""
        try:
            self.client.admin.command('ping')
            return {
                'status': 'connected',
                'database': Config.DB_NAME,
                'collections': self.db.list_collection_names()
            }
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                'status': 'disconnected',
                'error': str(e)
            }
    
    def get_collection(self, collection_name):
        """Get a collection by name"""
        return self.db[collection_name]
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("Database connection closed")

# Singleton instance
_db_instance = None

def get_db():
    """Get database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
