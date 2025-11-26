"""
Sketch Generation Service
Handles both drag-and-drop composition and AI generation
"""
import os
import logging
from PIL import Image, ImageDraw
import numpy as np
from utils.huggingface_api import HuggingFaceGenerator, LocalDiffusionGenerator
from utils.image_processing import ImageProcessor
from database.repository import SketchRepository
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class SketchGenerationService:
    """
    Service for generating sketches via:
    1. AI text-to-image (Hugging Face)
    2. Component composition (drag & drop)
    """
    
    def __init__(self, use_local_model=False):
        """
        Initialize generation service
        
        Args:
            use_local_model: Use local diffusion model instead of API
        """
        self.use_local = use_local_model
        
        # Initialize AI generator
        try:
            if use_local_model:
                self.ai_generator = LocalDiffusionGenerator()
            else:
                self.ai_generator = HuggingFaceGenerator()
            self.ai_available = True
        except Exception as e:
            logger.warning(f"AI generator not available: {str(e)}")
            self.ai_generator = None
            self.ai_available = False
        
        # Image processor
        self.image_processor = ImageProcessor()
        
        # Database repository
        self.sketch_repo = SketchRepository()
        
        logger.info(f"Sketch Generation Service initialized (AI: {self.ai_available})")
    
    def generate_from_prompt(self, prompt, user_id=None, save_to_db=True):
        """
        Generate sketch from text prompt using AI with OpenCV fallback
        
        Args:
            prompt: Text description
            user_id: User identifier
            save_to_db: Save to database
        
        Returns:
            Generated sketch and metadata
        """
        generation_method = 'ai'
        sketch_image = None
        
        try:
            # Try AI generation first
            if self.ai_available:
                logger.info(f"Generating sketch from prompt using AI: '{prompt}'")
                try:
                    sketch_image = self.ai_generator.generate_sketch_from_prompt(prompt)
                    generation_method = 'huggingface-api'
                except Exception as ai_error:
                    logger.warning(f"AI generation failed: {str(ai_error)}, falling back to OpenCV")
                    sketch_image = None
            
            # Fallback to OpenCV generator if AI fails or unavailable
            if sketch_image is None:
                logger.info(f"Generating sketch from prompt using OpenCV: '{prompt}'")
                from opencv_sketch_generator import generate_realistic_face_sketch
                sketch_array = generate_realistic_face_sketch(prompt)
                sketch_image = Image.fromarray(sketch_array)
                generation_method = 'opencv-procedural'
            
            # Generate unique filename
            sketch_id = str(uuid.uuid4())
            filename = f"sketch_{sketch_id}.png"
            sketch_path = os.path.join('uploads', 'sketches', filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(sketch_path), exist_ok=True)
            
            # Save image
            sketch_image.save(sketch_path)
            
            # Save to database
            if save_to_db:
                sketch_data = {
                    'sketch_id': sketch_id,
                    'sketch_url': sketch_path,
                    'sketch_type': 'ai-generated',
                    'prompt': prompt,
                    'user_id': user_id,
                    'face_detected': self._detect_face(sketch_image)
                }
                
                self.sketch_repo.create(sketch_data)
            
            logger.info(f"Sketch generated and saved: {sketch_path} (method: {generation_method})")
            
            return {
                'sketch_id': sketch_id,
                'sketch_url': sketch_path,
                'sketch_image': sketch_image,
                'prompt': prompt,
                'generation_method': generation_method
            }
            
        except Exception as e:
            logger.error(f"Error generating sketch from prompt: {str(e)}")
            raise
    
    def compose_from_components(self, components, canvas_size=(512, 512), user_id=None, save_to_db=True):
        """
        Compose sketch from drag-and-drop components
        
        Args:
            components: List of component data with positions
                       [{'image_path': str, 'position': (x, y), 'scale': float, 'rotation': float}]
            canvas_size: Output canvas size
            user_id: User identifier
            save_to_db: Save to database
        
        Returns:
            Composed sketch and metadata
        """
        try:
            logger.info(f"Composing sketch from {len(components)} components")
            
            # Create blank canvas
            canvas = Image.new('RGB', canvas_size, color='white')
            
            # Composite components
            for component in components:
                try:
                    # Load component image
                    comp_img = Image.open(component['image_path']).convert('RGBA')
                    
                    # Apply transformations
                    if 'scale' in component and component['scale'] != 1.0:
                        new_size = tuple(int(dim * component['scale']) for dim in comp_img.size)
                        comp_img = comp_img.resize(new_size, Image.Resampling.LANCZOS)
                    
                    if 'rotation' in component and component['rotation'] != 0:
                        comp_img = comp_img.rotate(component['rotation'], expand=True)
                    
                    # Get position
                    position = component.get('position', (0, 0))
                    
                    # Paste onto canvas
                    canvas.paste(comp_img, position, comp_img)
                    
                except Exception as e:
                    logger.warning(f"Error adding component {component.get('image_path')}: {str(e)}")
            
            # Convert to RGB
            sketch_image = canvas.convert('RGB')
            
            # Generate unique filename
            sketch_id = str(uuid.uuid4())
            filename = f"sketch_{sketch_id}.png"
            sketch_path = os.path.join('uploads', 'sketches', filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(sketch_path), exist_ok=True)
            
            # Save image
            sketch_image.save(sketch_path)
            
            # Save to database
            if save_to_db:
                sketch_data = {
                    'sketch_id': sketch_id,
                    'sketch_url': sketch_path,
                    'sketch_type': 'manual',
                    'components': components,
                    'user_id': user_id,
                    'face_detected': self._detect_face(sketch_image)
                }
                
                self.sketch_repo.create(sketch_data)
            
            logger.info(f"Sketch composed and saved: {sketch_path}")
            
            return {
                'sketch_id': sketch_id,
                'sketch_url': sketch_path,
                'sketch_image': sketch_image,
                'num_components': len(components),
                'generation_method': 'manual'
            }
            
        except Exception as e:
            logger.error(f"Error composing sketch: {str(e)}")
            raise
    
    def _detect_face(self, image):
        """
        Detect if image contains a face
        
        Args:
            image: PIL Image
        
        Returns:
            Boolean
        """
        try:
            face_bbox = self.image_processor.detect_face(image)
            return face_bbox is not None
        except:
            return False
    
    def get_recent_sketches(self, user_id=None, limit=20):
        """
        Get recent sketches from database
        
        Args:
            user_id: Filter by user
            limit: Maximum number of sketches
        
        Returns:
            List of sketch records
        """
        try:
            return self.sketch_repo.get_recent(limit=limit, user_id=user_id)
        except Exception as e:
            logger.error(f"Error fetching recent sketches: {str(e)}")
            return []
    
    def enhance_sketch(self, sketch_id):
        """
        Enhance existing sketch using image processing
        
        Args:
            sketch_id: Sketch ID
        
        Returns:
            Enhanced sketch info
        """
        try:
            # Get sketch from database
            sketch = self.sketch_repo.get_by_id(sketch_id)
            
            if not sketch:
                raise ValueError(f"Sketch not found: {sketch_id}")
            
            # Load image
            image = Image.open(sketch['sketch_url'])
            
            # Enhance
            enhanced = self.image_processor.enhance_contrast(image)
            enhanced = self.image_processor.denoise(enhanced)
            
            # Save enhanced version
            enhanced_path = sketch['sketch_url'].replace('.png', '_enhanced.png')
            enhanced.save(enhanced_path)
            
            logger.info(f"Sketch enhanced: {enhanced_path}")
            
            return {
                'sketch_id': sketch_id,
                'original_url': sketch['sketch_url'],
                'enhanced_url': enhanced_path
            }
            
        except Exception as e:
            logger.error(f"Error enhancing sketch: {str(e)}")
            raise
