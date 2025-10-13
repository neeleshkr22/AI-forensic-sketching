"""
AI-POWERED REALISTIC SKETCH GENERATOR
Using Hugging Face Inference API with pre-trained Stable Diffusion model
Generates photorealistic pencil sketches of human faces
"""
import requests
from PIL import Image
import io
import base64
import time

# Hugging Face API endpoint (free tier)
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

def generate_ai_sketch(prompt):
    """
    Generate realistic human face sketch using Stable Diffusion AI model
    Falls back to local generation if API is unavailable
    """
    
    # Enhanced prompt for realistic pencil sketch
    enhanced_prompt = f"highly detailed pencil sketch portrait drawing of {prompt}, "
    enhanced_prompt += "professional forensic sketch artist style, realistic human face proportions, "
    enhanced_prompt += "smooth graphite shading, photorealistic facial features, "
    enhanced_prompt += "detailed eyes nose lips, natural hair texture, "
    enhanced_prompt += "charcoal and pencil artwork, black and white portrait drawing, "
    enhanced_prompt += "high resolution, masterpiece quality, anatomically correct"
    
    # Negative prompt to avoid cartoon style
    negative_prompt = "cartoon, anime, comic, illustration, 3d render, painting, colorful, unrealistic, distorted face, bad anatomy"
    
    try:
        # Try Hugging Face Inference API (free, no auth needed for public models)
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "inputs": enhanced_prompt,
            "parameters": {
                "negative_prompt": negative_prompt,
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "width": 768,
                "height": 1024,
            }
        }
        
        print(f"Generating AI sketch with prompt: {enhanced_prompt[:100]}...")
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            # Success - convert to PIL Image
            image = Image.open(io.BytesIO(response.content))
            
            # Convert to grayscale (pencil sketch effect)
            image = image.convert('L')
            
            # Enhance for pencil look
            from PIL import ImageEnhance, ImageFilter
            
            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.4)
            
            # Slight blur for pencil softness
            image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # Sharpen details
            image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            
            # Convert to RGB
            image = image.convert('RGB')
            
            print("✓ AI sketch generated successfully!")
            return image
        
        elif response.status_code == 503:
            # Model is loading, wait and retry
            print("Model is loading, waiting 20 seconds...")
            time.sleep(20)
            
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                image = image.convert('L').convert('RGB')
                print("✓ AI sketch generated successfully (after retry)!")
                return image
        
        # If API failed, fall back to local generation
        print(f"API returned {response.status_code}, falling back to local generation...")
        return generate_local_sketch(prompt)
        
    except Exception as e:
        print(f"Error with AI API: {str(e)}, using local generation...")
        return generate_local_sketch(prompt)


def generate_local_sketch(prompt):
    """
    Fallback: Generate sketch using OpenCV when AI API is unavailable
    """
    from opencv_sketch_generator import generate_realistic_face_sketch
    return generate_realistic_face_sketch(prompt)
