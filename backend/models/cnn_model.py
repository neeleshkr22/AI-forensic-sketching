"""
CNN Model for Feature Extraction using VGGFace
"""
import torch
import torch.nn as nn
import numpy as np
from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
from PIL import Image
import logging
import os

logger = logging.getLogger(__name__)

class CNNFeatureExtractor:
    """
    CNN-based feature extractor using FaceNet (InceptionResnetV1)
    Extracts 512-dimensional feature vectors from face images
    """
    
    def __init__(self, model_path=None, device=None):
        """
        Initialize the CNN model
        
        Args:
            model_path: Path to saved model weights (optional)
            device: Computing device (cuda/cpu)
        """
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load pre-trained FaceNet model
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        
        # Image preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize((160, 160)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        
        logger.info(f"CNN Feature Extractor initialized on {self.device}")
    
    def preprocess_image(self, image):
        """
        Preprocess image for feature extraction
        
        Args:
            image: PIL Image or numpy array
        
        Returns:
            Preprocessed tensor
        """
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return self.transform(image).unsqueeze(0)
    
    def extract_features(self, image):
        """
        Extract feature vector from image
        
        Args:
            image: PIL Image, numpy array, or tensor
        
        Returns:
            Feature vector (512-dim numpy array)
        """
        try:
            # Preprocess image
            if not isinstance(image, torch.Tensor):
                image_tensor = self.preprocess_image(image)
            else:
                image_tensor = image
            
            image_tensor = image_tensor.to(self.device)
            
            # Extract features
            with torch.no_grad():
                features = self.model(image_tensor)
            
            # Convert to numpy
            feature_vector = features.cpu().numpy().flatten()
            
            # Normalize features
            feature_vector = feature_vector / (np.linalg.norm(feature_vector) + 1e-6)
            
            logger.debug(f"Extracted feature vector of shape: {feature_vector.shape}")
            return feature_vector
            
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            raise
    
    def extract_features_batch(self, images):
        """
        Extract features from multiple images
        
        Args:
            images: List of images
        
        Returns:
            Array of feature vectors
        """
        try:
            feature_vectors = []
            
            for img in images:
                features = self.extract_features(img)
                feature_vectors.append(features)
            
            return np.array(feature_vectors)
            
        except Exception as e:
            logger.error(f"Error in batch feature extraction: {str(e)}")
            raise
    
    def extract_from_path(self, image_path):
        """
        Extract features from image file
        
        Args:
            image_path: Path to image file
        
        Returns:
            Feature vector
        """
        try:
            image = Image.open(image_path)
            return self.extract_features(image)
        except Exception as e:
            logger.error(f"Error loading image from {image_path}: {str(e)}")
            raise
    
    def save_model(self, path):
        """Save model weights"""
        try:
            torch.save(self.model.state_dict(), path)
            logger.info(f"Model saved to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise
    
    def load_model(self, path):
        """Load model weights"""
        try:
            if os.path.exists(path):
                self.model.load_state_dict(torch.load(path, map_location=self.device))
                self.model.eval()
                logger.info(f"Model loaded from {path}")
            else:
                logger.warning(f"Model file not found: {path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

class VGGFaceFeatureExtractor:
    """
    Alternative CNN using VGG architecture
    Can be used for comparison or ensemble methods
    """
    
    def __init__(self):
        import tensorflow as tf
        from tensorflow.keras.applications import VGG16
        from tensorflow.keras.models import Model
        
        # Load VGG16 without top layers
        base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        
        # Create feature extraction model
        self.model = Model(inputs=base_model.input, outputs=base_model.output)
        self.model.trainable = False
        
        logger.info("VGGFace Feature Extractor initialized")
    
    def extract_features(self, image):
        """Extract features using VGG16"""
        import tensorflow as tf
        
        # Preprocess
        if isinstance(image, np.ndarray):
            img = image
        else:
            img = np.array(image)
        
        img = tf.image.resize(img, (224, 224))
        img = tf.keras.applications.vgg16.preprocess_input(img)
        img = np.expand_dims(img, axis=0)
        
        # Extract features
        features = self.model.predict(img, verbose=0)
        
        # Flatten and normalize
        feature_vector = features.flatten()
        feature_vector = feature_vector / (np.linalg.norm(feature_vector) + 1e-6)
        
        return feature_vector
