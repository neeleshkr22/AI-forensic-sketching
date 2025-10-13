"""
Test AI Sketch Generation with Hugging Face
Now with Pencil Sketch Conversion!
"""
import os
from dotenv import load_dotenv
from hf_client import generate_from_hf
from sketch_converter import convert_to_pencil_sketch
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

# Token will be loaded from .env file automatically
print("=" * 70)
print("AI SKETCH GENERATION - Stable Diffusion XL + Pencil Conversion")
print("=" * 70)

prompt = "Male, 35 years old, short hair, beard"
print(f"\nPrompt: {prompt}")
print("\nStep 1: Generating photorealistic portrait with AI...")

try:
    img_bytes = generate_from_hf(
        prompt=f"professional portrait photo of {prompt}, high quality, detailed, studio lighting, neutral background",
        negative_prompt="cartoon, anime, sketch, drawing, painting, low quality, blurry",
        guidance=7.5,
        width=512,
        height=768
    )
    
    # Save original photo
    photo_img = Image.open(io.BytesIO(img_bytes))
    os.makedirs('uploads', exist_ok=True)
    photo_img.save('uploads/step1_photo.png')
    print("✅ Photo generated!")
    
    print("\nStep 2: Converting to realistic pencil sketch...")
    sketch_img = convert_to_pencil_sketch(photo_img)
    sketch_img.save('uploads/ai_generated_realistic.png')
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! REALISTIC PENCIL SKETCH CREATED!")
    print("=" * 70)
    print(f"\n📁 Original Photo: uploads/step1_photo.png")
    print(f"✏️  Pencil Sketch: uploads/ai_generated_realistic.png")
    print(f"📊 Size: {sketch_img.size[0]}x{sketch_img.size[1]} pixels")
    print(f"\n🌐 View sketch at: http://localhost:5000/api/sample/latest")
    print("\nThis is a REAL pencil sketch, not a photo!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Model might be loading (wait 1 minute)")
    print("2. Check HF_API_TOKEN is valid")
    print("3. Check internet connection")
