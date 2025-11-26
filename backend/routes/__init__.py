"""
Routes Package
"""
from .sketch_routes import bp as sketch_bp
from .record_routes import bp as records_bp
from .feature_routes import bp as features_bp

__all__ = ['sketch_bp', 'records_bp', 'features_bp']
