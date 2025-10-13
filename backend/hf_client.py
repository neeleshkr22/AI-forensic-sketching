import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HF_API = os.environ.get('HF_API_TOKEN') or os.environ.get('HUGGINGFACE_API_KEY')
# Use Stable Diffusion XL - best quality model available
HF_HOST = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0'

headers = {}
if HF_API:
    headers['Authorization'] = f'Bearer {HF_API}'


def generate_from_hf(prompt, negative_prompt=None, guidance=7.5, width=768, height=1024):
    """
    Call Hugging Face Inference API to generate sketch from text.
    Uses Stable Diffusion 2.1 for photorealistic pencil sketch generation.
    
    Args:
        prompt: Text description of the sketch (e.g., "Male, 30s, beard, realistic pencil portrait")
        negative_prompt: Things to avoid (e.g., "cartoon, anime, low quality")
        guidance: Guidance scale (7-15, higher = more adherence to prompt)
        width: Output width in pixels
        height: Output height in pixels
    
    Returns:
        bytes: PNG image data
        
    Raises:
        RuntimeError: If API call fails
    """
    if not HF_API:
        raise RuntimeError("HF_API_TOKEN not set. Please set environment variable.")
    
    payload = {
        'inputs': prompt,
        'options': {'wait_for_model': True},
        'parameters': {
            'negative_prompt': negative_prompt or 'cartoon, anime, low quality, blurry, distorted',
            'guidance_scale': guidance,
            'width': width,
            'height': height,
            'num_inference_steps': 50  # More steps = better quality
        }
    }
    
    print(f"[HF] Calling Stable Diffusion 2.1...")
    print(f"[HF] Prompt: {prompt}")
    print(f"[HF] Negative: {payload['parameters']['negative_prompt']}")
    
    response = requests.post(HF_HOST, headers=headers, json=payload, timeout=120)
    
    if response.status_code == 200:
        print(f"[HF] SUCCESS - Generated image ({len(response.content)} bytes)")
        return response.content
    else:
        error_msg = f"HF inference failed: {response.status_code} {response.text}"
        print(f"[HF] ERROR - {error_msg}")
        raise RuntimeError(error_msg)

