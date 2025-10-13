"""
Sketch Style Converter - Convert any image to realistic pencil sketch
Professional quality with proper shading and white background
"""
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def convert_to_pencil_sketch(image):
    """
    Convert a PIL Image to realistic pencil sketch with proper shading
    Like the second reference image - detailed with white background
    """
    # Convert PIL to numpy array
    if isinstance(image, Image.Image):
        img = np.array(image.convert('RGB'))
    else:
        img = cv2.imread(image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # DODGE AND BURN TECHNIQUE for pencil sketch
    # Invert the grayscale image
    inverted = 255 - gray
    
    # Apply Gaussian blur to inverted image
    blurred = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)
    
    # Blend using dodge blend mode (color dodge)
    def dodge_blend(front, back):
        # Avoid division by zero
        result = back * 255 / (255 - front + 1)
        result[result > 255] = 255
        result[back == 255] = 255
        return result.astype(np.uint8)
    
    sketch = dodge_blend(blurred, gray)
    
    # Enhance contrast for more defined lines
    sketch = cv2.convertScaleAbs(sketch, alpha=1.4, beta=-20)
    
    # Ensure white background - brighten the image
    sketch = cv2.convertScaleAbs(sketch, alpha=1.1, beta=30)
    
    # Apply adaptive histogram equalization for better tonal range
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    sketch = clahe.apply(sketch)
    
    # Slight sharpening for pencil detail
    kernel = np.array([[-1,-1,-1],
                       [-1, 9,-1],
                       [-1,-1,-1]]) / 1.5
    sketch = cv2.filter2D(sketch, -1, kernel)
    
    # Final brightness adjustment to ensure white background
    sketch = np.clip(sketch + 20, 0, 255).astype(np.uint8)
    
    # Convert back to PIL Image
    result = Image.fromarray(sketch)
    
    # Enhance brightness in PIL for extra white background
    enhancer = ImageEnhance.Brightness(result)
    result = enhancer.enhance(1.2)
    
    return result

def convert_to_detailed_sketch(image):
    """
    Alternative method: More detailed edge-based sketch
    """
    if isinstance(image, Image.Image):
        img = np.array(image.convert('RGB'))
    else:
        img = cv2.imread(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Detect edges using Canny
    edges = cv2.Canny(gray, 50, 150)
    
    # Invert so edges are dark on white
    edges = 255 - edges
    
    # Dilate edges slightly for pencil thickness
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Combine with tonal sketch
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = 255 - blurred
    tonal = cv2.divide(gray, inverted_blur, scale=256.0)
    
    # Blend edges and tonal
    sketch = cv2.addWeighted(edges, 0.3, tonal, 0.7, 0)
    
    # Enhance
    sketch = cv2.convertScaleAbs(sketch, alpha=1.3, beta=5)
    
    return Image.fromarray(sketch)
