"""
Hugging Face API Integration for Text-to-Sketch Generation
"""
import requests
import io
import os
from PIL import Image
import logging
from config import Config

logger = logging.getLogger(__name__)

class HuggingFaceGenerator:
    """
    Text-to-sketch generation using Hugging Face API
    Uses Stable Diffusion for sketch generation
    """
    
    def __init__(self, api_key=None, model_id=None):
        """
        Initialize Hugging Face generator
        
        Args:
            api_key: Hugging Face API key
            model_id: Model identifier
        """
        self.api_key = api_key or Config.HUGGINGFACE_API_KEY
        self.model_id = model_id or Config.HUGGINGFACE_MODEL
        
        # API endpoints
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        
        # Headers
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        logger.info(f"Hugging Face Generator initialized with model: {self.model_id}")
    
    def generate_sketch_from_prompt(self, prompt, negative_prompt=None, num_images=1):
        """
        Generate sketch from text prompt
        
        Args:
            prompt: Text description
            negative_prompt: Things to avoid in generation
            num_images: Number of images to generate
        
        Returns:
            Generated image(s)
        """
        try:
            # Enhance prompt for sketch generation
            enhanced_prompt = f"pencil sketch, black and white drawing, detailed facial sketch, {prompt}"
            
            if negative_prompt is None:
                negative_prompt = "photo, photograph, realistic, color, colorful, painting"
            
            # Prepare payload
            payload = {
                "inputs": enhanced_prompt,
                "parameters": {
                    "negative_prompt": negative_prompt,
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5,
                    "width": 512,
                    "height": 512
                }
            }
            
            logger.info(f"Generating sketch with prompt: {prompt}")
            
            # Make API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                # Convert response to image
                image = Image.open(io.BytesIO(response.content))
                logger.info("Sketch generated successfully")
                return image
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                raise Exception(f"Failed to generate image: {response.text}")
                
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            raise Exception("Image generation timed out. Please try again.")
        except Exception as e:
            logger.error(f"Error generating sketch: {str(e)}")
            raise
    
    def generate_batch(self, prompts):
        """
        Generate multiple sketches from prompts
        
        Args:
            prompts: List of text prompts
        
        Returns:
            List of generated images
        """
        images = []
        
        for prompt in prompts:
            try:
                image = self.generate_sketch_from_prompt(prompt)
                images.append(image)
            except Exception as e:
                logger.error(f"Error generating sketch for prompt '{prompt}': {str(e)}")
                images.append(None)
        
        return images
    
    def save_generated_sketch(self, prompt, output_path):
        """
        Generate and save sketch
        
        Args:
            prompt: Text prompt
            output_path: Path to save image
        
        Returns:
            Path to saved image
        """
        try:
            image = self.generate_sketch_from_prompt(prompt)
            image.save(output_path)
            logger.info(f"Sketch saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving generated sketch: {str(e)}")
            raise

class LocalDiffusionGenerator:
    """
    Local Stable Diffusion using diffusers library
    Alternative to API-based generation
    """
    
    def __init__(self, model_id="stabilityai/stable-diffusion-2-1"):
        """Initialize local diffusion model"""
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            logger.info(f"Loading Stable Diffusion model on {self.device}...")
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.pipe = self.pipe.to(self.device)
            
            # Enable optimizations
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
            
            logger.info("Local Diffusion Generator initialized")
            
        except ImportError:
            logger.error("diffusers library not installed. Install with: pip install diffusers")
            raise
        except Exception as e:
            logger.error(f"Error initializing local generator: {str(e)}")
            raise
    
    def generate_sketch_from_prompt(self, prompt, negative_prompt=None, num_images=1):
        """
        Generate sketch locally
        
        Args:
            prompt: Text description
            negative_prompt: Things to avoid
            num_images: Number of images
        
        Returns:
            Generated image
        """
        try:
            # Enhance prompt
            enhanced_prompt = f"pencil sketch, black and white drawing, detailed facial sketch, {prompt}"
            
            if negative_prompt is None:
                negative_prompt = "photo, photograph, realistic, color, colorful, painting"
            
            # Generate
            result = self.pipe(
                enhanced_prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=50,
                guidance_scale=7.5,
                width=512,
                height=512,
                num_images_per_prompt=num_images
            )
            
            # Return first image
            return result.images[0]
            
        except Exception as e:
            logger.error(f"Error generating sketch: {str(e)}")
            raise

def generate_sketch_from_description(description, use_local=False, save_path=None):
    """
    Utility function to generate sketch from description
    
    Args:
        description: Text description
        use_local: Use local model instead of API
        save_path: Path to save generated sketch
    
    Returns:
        Generated sketch image
    """
    try:
        if use_local:
            generator = LocalDiffusionGenerator()
        else:
            generator = HuggingFaceGenerator()
        
        sketch = generator.generate_sketch_from_prompt(description)
        
        if save_path:
            sketch.save(save_path)
        
        return sketch
        
    except Exception as e:
        logger.error(f"Error in sketch generation: {str(e)}")
        raise
