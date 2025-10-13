"""
GAN Model for Sketch Enhancement (pix2pix)
"""
import torch
import torch.nn as nn
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import logging

logger = logging.getLogger(__name__)

class UNetGenerator(nn.Module):
    """
    U-Net Generator for pix2pix GAN
    Converts sketches to photo-realistic images
    """
    
    def __init__(self, in_channels=3, out_channels=3):
        super(UNetGenerator, self).__init__()
        
        # Encoder (Downsampling)
        self.enc1 = self.conv_block(in_channels, 64, normalize=False)
        self.enc2 = self.conv_block(64, 128)
        self.enc3 = self.conv_block(128, 256)
        self.enc4 = self.conv_block(256, 512)
        self.enc5 = self.conv_block(512, 512)
        self.enc6 = self.conv_block(512, 512)
        self.enc7 = self.conv_block(512, 512)
        self.enc8 = self.conv_block(512, 512, normalize=False)
        
        # Decoder (Upsampling)
        self.dec1 = self.deconv_block(512, 512, dropout=True)
        self.dec2 = self.deconv_block(1024, 512, dropout=True)
        self.dec3 = self.deconv_block(1024, 512, dropout=True)
        self.dec4 = self.deconv_block(1024, 512)
        self.dec5 = self.deconv_block(1024, 256)
        self.dec6 = self.deconv_block(512, 128)
        self.dec7 = self.deconv_block(256, 64)
        
        # Final layer
        self.final = nn.Sequential(
            nn.ConvTranspose2d(128, out_channels, 4, 2, 1),
            nn.Tanh()
        )
    
    def conv_block(self, in_c, out_c, normalize=True):
        """Convolutional block for encoder"""
        layers = [nn.Conv2d(in_c, out_c, 4, 2, 1)]
        if normalize:
            layers.append(nn.BatchNorm2d(out_c))
        layers.append(nn.LeakyReLU(0.2))
        return nn.Sequential(*layers)
    
    def deconv_block(self, in_c, out_c, dropout=False):
        """Deconvolutional block for decoder"""
        layers = [
            nn.ConvTranspose2d(in_c, out_c, 4, 2, 1),
            nn.BatchNorm2d(out_c),
            nn.ReLU()
        ]
        if dropout:
            layers.append(nn.Dropout(0.5))
        return nn.Sequential(*layers)
    
    def forward(self, x):
        """Forward pass with skip connections"""
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(e1)
        e3 = self.enc3(e2)
        e4 = self.enc4(e3)
        e5 = self.enc5(e4)
        e6 = self.enc6(e5)
        e7 = self.enc7(e6)
        e8 = self.enc8(e7)
        
        # Decoder with skip connections
        d1 = self.dec1(e8)
        d1 = torch.cat([d1, e7], dim=1)
        
        d2 = self.dec2(d1)
        d2 = torch.cat([d2, e6], dim=1)
        
        d3 = self.dec3(d2)
        d3 = torch.cat([d3, e5], dim=1)
        
        d4 = self.dec4(d3)
        d4 = torch.cat([d4, e4], dim=1)
        
        d5 = self.dec5(d4)
        d5 = torch.cat([d5, e3], dim=1)
        
        d6 = self.dec6(d5)
        d6 = torch.cat([d6, e2], dim=1)
        
        d7 = self.dec7(d6)
        d7 = torch.cat([d7, e1], dim=1)
        
        output = self.final(d7)
        return output

class GANSketchEnhancer:
    """
    GAN-based sketch enhancement system
    Uses pix2pix to convert sketches to photo-realistic images
    """
    
    def __init__(self, model_path=None, device=None):
        """
        Initialize GAN enhancer
        
        Args:
            model_path: Path to pre-trained generator weights
            device: Computing device
        """
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize generator
        self.generator = UNetGenerator().to(self.device)
        self.generator.eval()
        
        # Image transforms
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        
        self.inverse_transform = transforms.Compose([
            transforms.Normalize([-1, -1, -1], [2, 2, 2]),  # Denormalize
            transforms.ToPILImage()
        ])
        
        # Load pre-trained weights if available
        if model_path:
            self.load_model(model_path)
        
        logger.info(f"GAN Sketch Enhancer initialized on {self.device}")
    
    def enhance_sketch(self, sketch_image):
        """
        Enhance sketch using GAN
        
        Args:
            sketch_image: PIL Image or numpy array
        
        Returns:
            Enhanced image (PIL Image)
        """
        try:
            # Preprocess
            if isinstance(sketch_image, np.ndarray):
                sketch_image = Image.fromarray(sketch_image)
            
            if sketch_image.mode != 'RGB':
                sketch_image = sketch_image.convert('RGB')
            
            # Transform to tensor
            input_tensor = self.transform(sketch_image).unsqueeze(0).to(self.device)
            
            # Generate enhanced image
            with torch.no_grad():
                output_tensor = self.generator(input_tensor)
            
            # Convert back to PIL Image
            output_tensor = output_tensor.cpu().squeeze(0)
            enhanced_image = self.inverse_transform(output_tensor)
            
            logger.debug("Sketch enhanced successfully")
            return enhanced_image
            
        except Exception as e:
            logger.error(f"Error enhancing sketch: {str(e)}")
            raise
    
    def enhance_sketch_array(self, sketch_image):
        """
        Enhance sketch and return as numpy array
        
        Args:
            sketch_image: Input sketch
        
        Returns:
            Enhanced image as numpy array
        """
        enhanced = self.enhance_sketch(sketch_image)
        return np.array(enhanced)
    
    def enhance_batch(self, sketch_images):
        """
        Enhance multiple sketches
        
        Args:
            sketch_images: List of PIL Images
        
        Returns:
            List of enhanced images
        """
        try:
            enhanced_images = []
            
            for sketch in sketch_images:
                enhanced = self.enhance_sketch(sketch)
                enhanced_images.append(enhanced)
            
            return enhanced_images
            
        except Exception as e:
            logger.error(f"Error in batch enhancement: {str(e)}")
            raise
    
    def save_model(self, path):
        """Save generator weights"""
        try:
            torch.save(self.generator.state_dict(), path)
            logger.info(f"GAN model saved to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise
    
    def load_model(self, path):
        """Load generator weights"""
        try:
            import os
            if os.path.exists(path):
                self.generator.load_state_dict(
                    torch.load(path, map_location=self.device)
                )
                self.generator.eval()
                logger.info(f"GAN model loaded from {path}")
            else:
                logger.warning(f"Model file not found: {path}. Using default initialization.")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            logger.warning("Continuing with default initialized model")
    
    def train_step(self, real_images, sketch_images, optimizer, criterion):
        """
        Single training step (for fine-tuning)
        
        Args:
            real_images: Target real images
            sketch_images: Input sketches
            optimizer: Optimizer
            criterion: Loss function
        
        Returns:
            Loss value
        """
        self.generator.train()
        
        # Forward pass
        fake_images = self.generator(sketch_images)
        
        # Calculate loss
        loss = criterion(fake_images, real_images)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        self.generator.eval()
        
        return loss.item()

class SimpleSketchEnhancer:
    """
    Lightweight sketch enhancement using traditional CV methods
    Fallback when GAN model is not available
    """
    
    def __init__(self):
        logger.info("Simple Sketch Enhancer initialized (OpenCV-based)")
    
    def enhance_sketch(self, sketch_image):
        """
        Enhance sketch using OpenCV
        
        Args:
            sketch_image: PIL Image or numpy array
        
        Returns:
            Enhanced image
        """
        import cv2
        
        # Convert to numpy
        if isinstance(sketch_image, Image.Image):
            img = np.array(sketch_image)
        else:
            img = sketch_image
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img
        
        # Apply enhancement
        # 1. Denoise
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # 2. Sharpen
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        
        # 3. Contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(sharpened)
        
        # Convert back to RGB
        enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
        
        return Image.fromarray(enhanced_rgb)
