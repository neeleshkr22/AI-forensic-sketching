"""
OpenCV Image Processing Utilities
"""
import cv2
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Image processing utilities using OpenCV"""
    
    def __init__(self, face_cascade_path='models/haarcascade_frontalface_default.xml'):
        """
        Initialize image processor
        
        Args:
            face_cascade_path: Path to Haar Cascade XML for face detection
        """
        # Try to load face cascade
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if self.face_cascade.empty():
                logger.warning("Face cascade not loaded, downloading...")
                self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
        except:
            logger.warning("Using alternative face detection method")
            self.face_cascade = None
        
        logger.info("Image Processor initialized")
    
    def detect_face(self, image):
        """
        Detect face in image
        
        Args:
            image: PIL Image or numpy array
        
        Returns:
            Bounding box (x, y, w, h) or None
        """
        try:
            # Convert to numpy array
            if isinstance(image, Image.Image):
                img = np.array(image)
            else:
                img = image
            
            # Convert to grayscale
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img
            
            # Detect faces
            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                if len(faces) > 0:
                    # Return largest face
                    largest_face = max(faces, key=lambda f: f[2] * f[3])
                    return tuple(largest_face)
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting face: {str(e)}")
            return None
    
    def crop_face(self, image, padding=0.2):
        """
        Detect and crop face from image
        
        Args:
            image: Input image
            padding: Padding around face (percentage)
        
        Returns:
            Cropped face image or original if no face detected
        """
        try:
            face_bbox = self.detect_face(image)
            
            if face_bbox is None:
                logger.warning("No face detected, returning original image")
                return image
            
            # Convert to numpy
            if isinstance(image, Image.Image):
                img = np.array(image)
            else:
                img = image
            
            x, y, w, h = face_bbox
            
            # Add padding
            pad_w = int(w * padding)
            pad_h = int(h * padding)
            
            x1 = max(0, x - pad_w)
            y1 = max(0, y - pad_h)
            x2 = min(img.shape[1], x + w + pad_w)
            y2 = min(img.shape[0], y + h + pad_h)
            
            # Crop
            cropped = img[y1:y2, x1:x2]
            
            return Image.fromarray(cropped) if isinstance(image, Image.Image) else cropped
            
        except Exception as e:
            logger.error(f"Error cropping face: {str(e)}")
            return image
    
    def convert_to_sketch(self, image):
        """
        Convert photo to sketch
        
        Args:
            image: Input image
        
        Returns:
            Sketch image
        """
        try:
            # Convert to numpy
            if isinstance(image, Image.Image):
                img = np.array(image)
            else:
                img = image
            
            # Convert to grayscale
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img
            
            # Invert
            inverted = 255 - gray
            
            # Gaussian blur
            blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
            
            # Invert blurred image
            inverted_blur = 255 - blurred
            
            # Create sketch
            sketch = cv2.divide(gray, inverted_blur, scale=256.0)
            
            # Convert to RGB
            sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
            
            return Image.fromarray(sketch_rgb)
            
        except Exception as e:
            logger.error(f"Error converting to sketch: {str(e)}")
            raise
    
    def edge_detection(self, image, low_threshold=50, high_threshold=150):
        """
        Perform edge detection using Canny
        
        Args:
            image: Input image
            low_threshold: Lower threshold for Canny
            high_threshold: Upper threshold for Canny
        
        Returns:
            Edge image
        """
        try:
            # Convert to numpy
            if isinstance(image, Image.Image):
                img = np.array(image)
            else:
                img = image
            
            # Convert to grayscale
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img
            
            # Apply Canny edge detection
            edges = cv2.Canny(gray, low_threshold, high_threshold)
            
            # Convert to RGB
            edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            
            return Image.fromarray(edges_rgb)
            
        except Exception as e:
            logger.error(f"Error in edge detection: {str(e)}")
            raise
    
    def enhance_contrast(self, image):
        """
        Enhance image contrast using CLAHE
        
        Args:
            image: Input image
        
        Returns:
            Enhanced image
        """
        try:
            # Convert to numpy
            if isinstance(image, Image.Image):
                img = np.array(image)
            else:
                img = image
            
            # Convert to LAB color space
            if len(img.shape) == 3:
                lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
                l, a, b = cv2.split(lab)
            else:
                l = img
                a, b = None, None
            
            # Apply CLAHE
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced_l = clahe.apply(l)
            
            # Merge back
            if a is not None and b is not None:
                enhanced_lab = cv2.merge([enhanced_l, a, b])
                enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
            else:
                enhanced = enhanced_l
            
            return Image.fromarray(enhanced)
            
        except Exception as e:
            logger.error(f"Error enhancing contrast: {str(e)}")
            raise
    
    def denoise(self, image, strength=10):
        """
        Denoise image
        
        Args:
            image: Input image
            strength: Denoising strength
        
        Returns:
            Denoised image
        """
        try:
            # Convert to numpy
            if isinstance(image, Image.Image):
                img = np.array(image)
            else:
                img = image
            
            # Apply denoising
            if len(img.shape) == 3:
                denoised = cv2.fastNlMeansDenoisingColored(img, None, strength, strength, 7, 21)
            else:
                denoised = cv2.fastNlMeansDenoising(img, None, strength, 7, 21)
            
            return Image.fromarray(denoised)
            
        except Exception as e:
            logger.error(f"Error denoising image: {str(e)}")
            raise
    
    def resize_image(self, image, size=(256, 256), maintain_aspect=True):
        """
        Resize image
        
        Args:
            image: Input image
            size: Target size (width, height)
            maintain_aspect: Maintain aspect ratio
        
        Returns:
            Resized image
        """
        try:
            if isinstance(image, Image.Image):
                if maintain_aspect:
                    image.thumbnail(size, Image.Resampling.LANCZOS)
                    return image
                else:
                    return image.resize(size, Image.Resampling.LANCZOS)
            else:
                if maintain_aspect:
                    h, w = image.shape[:2]
                    aspect = w / h
                    if w > h:
                        new_w = size[0]
                        new_h = int(new_w / aspect)
                    else:
                        new_h = size[1]
                        new_w = int(new_h * aspect)
                    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
                else:
                    resized = cv2.resize(image, size, interpolation=cv2.INTER_LANCZOS4)
                
                return resized
                
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            raise
    
    def preprocess_for_matching(self, image):
        """
        Complete preprocessing pipeline for sketch matching
        
        Args:
            image: Input sketch
        
        Returns:
            Preprocessed image
        """
        try:
            # 1. Denoise
            denoised = self.denoise(image, strength=8)
            
            # 2. Enhance contrast
            enhanced = self.enhance_contrast(denoised)
            
            # 3. Detect and crop face
            cropped = self.crop_face(enhanced)
            
            # 4. Resize to standard size
            resized = self.resize_image(cropped, size=(256, 256), maintain_aspect=False)
            
            logger.debug("Image preprocessing complete")
            return resized
            
        except Exception as e:
            logger.error(f"Error in preprocessing pipeline: {str(e)}")
            raise
    
    def align_face(self, image):
        """
        Align face using facial landmarks (advanced feature)
        
        Args:
            image: Input image
        
        Returns:
            Aligned face image
        """
        # Placeholder for face alignment
        # Can be implemented using dlib or similar libraries
        logger.debug("Face alignment not implemented, returning original")
        return image

def create_sketch_from_photo(photo_path, output_path=None):
    """
    Utility function to create sketch from photo
    
    Args:
        photo_path: Path to photo
        output_path: Path to save sketch (optional)
    
    Returns:
        Sketch image
    """
    processor = ImageProcessor()
    
    # Load image
    image = Image.open(photo_path)
    
    # Convert to sketch
    sketch = processor.convert_to_sketch(image)
    
    # Save if output path provided
    if output_path:
        sketch.save(output_path)
    
    return sketch
