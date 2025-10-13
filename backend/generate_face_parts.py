"""
Generate placeholder facial component images for drag-and-drop
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create output directory
output_dir = r"c:\Users\mrana\OneDrive\Desktop\Major project final\frontend\public\assets\face-parts"
os.makedirs(output_dir, exist_ok=True)

# Component definitions
components = {
    "eyes": [
        ("eye1.png", "Round Eyes"),
        ("eye2.png", "Almond Eyes"),
        ("eye3.png", "Narrow Eyes"),
        ("eye4.png", "Wide Eyes"),
    ],
    "nose": [
        ("nose1.png", "Straight Nose"),
        ("nose2.png", "Button Nose"),
        ("nose3.png", "Hook Nose"),
        ("nose4.png", "Broad Nose"),
    ],
    "mouth": [
        ("mouth1.png", "Thin Lips"),
        ("mouth2.png", "Full Lips"),
        ("mouth3.png", "Wide Mouth"),
        ("mouth4.png", "Small Mouth"),
    ],
    "hair": [
        ("hair1.png", "Short Hair"),
        ("hair2.png", "Long Hair"),
        ("hair3.png", "Curly Hair"),
        ("hair4.png", "Bald"),
    ],
    "face": [
        ("face1.png", "Oval Face"),
        ("face2.png", "Round Face"),
        ("face3.png", "Square Face"),
        ("face4.png", "Long Face"),
    ]
}

def create_component_image(filename, label, category):
    """Create a realistic placeholder image for a facial component"""
    # Image size
    width, height = 200, 150
    
    # Create image with sketch paper background
    img = Image.new('RGBA', (width, height), (245, 245, 220, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw realistic components based on category
    if category == "eyes":
        # Draw realistic eyes
        eye_y = 50
        
        # Left eye
        left_x = 40
        # Upper eyelid (thicker, darker)
        draw.arc([left_x, eye_y, left_x+50, eye_y+30], 180, 360, fill=(30, 30, 30), width=3)
        # Lower eyelid
        draw.arc([left_x, eye_y, left_x+50, eye_y+30], 0, 180, fill=(80, 80, 80), width=2)
        # Iris
        draw.ellipse([left_x+18, eye_y+8, left_x+32, eye_y+22], outline=(20, 20, 20), width=2)
        # Pupil
        draw.ellipse([left_x+22, eye_y+12, left_x+28, eye_y+18], fill=(10, 10, 10))
        # Reflection
        draw.ellipse([left_x+25, eye_y+13, left_x+27, eye_y+15], fill=(200, 200, 200))
        # Eyebrow strokes
        for i in range(6):
            draw.line([left_x-5+i*10, eye_y-15, left_x+i*10, eye_y-12], fill=(40, 40, 40), width=2)
        
        # Right eye (mirror)
        right_x = 110
        draw.arc([right_x, eye_y, right_x+50, eye_y+30], 180, 360, fill=(30, 30, 30), width=3)
        draw.arc([right_x, eye_y, right_x+50, eye_y+30], 0, 180, fill=(80, 80, 80), width=2)
        draw.ellipse([right_x+18, eye_y+8, right_x+32, eye_y+22], outline=(20, 20, 20), width=2)
        draw.ellipse([right_x+22, eye_y+12, right_x+28, eye_y+18], fill=(10, 10, 10))
        draw.ellipse([right_x+25, eye_y+13, right_x+27, eye_y+15], fill=(200, 200, 200))
        for i in range(6):
            draw.line([right_x+5+i*10, eye_y-12, right_x+7+i*10, eye_y-15], fill=(40, 40, 40), width=2)
        
    elif category == "nose":
        # Draw realistic nose with shading
        nose_x = width // 2
        nose_top = 30
        nose_bottom = 100
        
        # Bridge
        draw.line([nose_x-3, nose_top, nose_x-5, nose_bottom-20], fill=(60, 60, 60), width=2)
        draw.line([nose_x+3, nose_top, nose_x+5, nose_bottom-20], fill=(60, 60, 60), width=2)
        
        # Tip
        draw.ellipse([nose_x-15, nose_bottom-15, nose_x+15, nose_bottom+5], outline=(50, 50, 50), width=2)
        
        # Nostrils with depth
        draw.arc([nose_x-13, nose_bottom-8, nose_x-5, nose_bottom+2], 180, 360, fill=(40, 40, 40), width=3)
        draw.arc([nose_x+5, nose_bottom-8, nose_x+13, nose_bottom+2], 180, 360, fill=(40, 40, 40), width=3)
        
        # Shading for depth
        for i in range(5):
            draw.line([nose_x-10+i*2, nose_bottom-10+i*2, nose_x-10+i*2, nose_bottom-5+i*2],
                     fill=(150-i*10, 150-i*10, 150-i*10), width=1)
        
    elif category == "mouth":
        # Draw realistic lips
        mouth_y = 60
        mouth_x_left = 50
        mouth_x_right = 150
        mouth_center = (mouth_x_left + mouth_x_right) // 2
        
        # Upper lip with cupid's bow
        draw.line([mouth_x_left, mouth_y, mouth_center-15, mouth_y-6], fill=(50, 50, 50), width=3)
        draw.line([mouth_center-15, mouth_y-6, mouth_center, mouth_y-4], fill=(50, 50, 50), width=3)
        draw.line([mouth_center, mouth_y-4, mouth_center+15, mouth_y-6], fill=(50, 50, 50), width=3)
        draw.line([mouth_center+15, mouth_y-6, mouth_x_right, mouth_y], fill=(50, 50, 50), width=3)
        
        # Lower lip
        draw.arc([mouth_x_left, mouth_y-3, mouth_x_right, mouth_y+25], 0, 180, fill=(50, 50, 50), width=3)
        
        # Lip line
        draw.line([mouth_x_left, mouth_y, mouth_x_right, mouth_y], fill=(30, 30, 30), width=2)
        
        # Shading for volume
        for i in range(3):
            draw.arc([mouth_x_left+i*3, mouth_y, mouth_x_right-i*3, mouth_y+22],
                    0, 180, fill=(80+i*15, 80+i*15, 80+i*15), width=1)
        
    elif category == "hair":
        # Draw realistic hair texture
        if "short" in label.lower():
            # Short hair strokes
            for i in range(25):
                x = 20 + i * 7
                draw.line([x, 20, x+5, 50], fill=(40, 40, 40), width=2)
        elif "long" in label.lower():
            # Long flowing hair
            for i in range(15):
                x = 30 + i * 10
                draw.line([x, 20, x-10, 120], fill=(40, 40, 40), width=2)
                draw.line([x+5, 20, x-5, 120], fill=(50, 50, 50), width=1)
        elif "curly" in label.lower():
            # Curly hair texture
            for i in range(12):
                x = 25 + i * 15
                for j in range(4):
                    y = 20 + j * 25
                    draw.arc([x, y, x+15, y+15], 0, 360, fill=(40, 40, 40), width=2)
        else:  # Bald
            # Smooth head outline
            draw.arc([40, 20, 160, 130], 180, 360, fill=(100, 100, 100), width=2)
            # Add some skin texture
            for i in range(8):
                draw.arc([50+i*15, 30, 70+i*15, 50], 180, 360, fill=(120, 120, 120), width=1)
        
    elif category == "face":
        # Draw realistic face outline with shading
        face_type = label.lower()
        
        if "oval" in face_type:
            # Oval face
            draw.ellipse([50, 20, 150, 130], outline=(60, 60, 60), width=3)
        elif "round" in face_type:
            # Round face
            draw.ellipse([55, 25, 145, 125], outline=(60, 60, 60), width=3)
        elif "square" in face_type:
            # Square jaw
            draw.line([60, 25, 140, 25], fill=(60, 60, 60), width=3)  # Top
            draw.line([60, 25, 55, 110], fill=(60, 60, 60), width=3)  # Left
            draw.line([140, 25, 145, 110], fill=(60, 60, 60), width=3)  # Right
            draw.line([55, 110, 100, 120], fill=(60, 60, 60), width=3)  # Bottom left
            draw.line([145, 110, 100, 120], fill=(60, 60, 60), width=3)  # Bottom right
        else:  # Long face
            draw.ellipse([60, 15, 140, 135], outline=(60, 60, 60), width=3)
        
        # Add cheekbone contour
        draw.line([65, 70, 80, 85], fill=(80, 80, 80), width=2)
        draw.line([135, 70, 120, 85], fill=(80, 80, 80), width=2)
        
        # Add subtle shading
        for i in range(8):
            draw.line([60+i*2, 40+i*8, 60+i*2, 50+i*8], 
                     fill=(180-i*5, 180-i*5, 180-i*5), width=1)
    
    # Add text label with better font
    try:
        font = ImageFont.truetype("arial.ttf", 11)
    except:
        font = ImageFont.load_default()
    
    # Text background
    bbox = draw.textbbox((0, 0), label, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    
    draw.rectangle([text_x - 5, height - 25, text_x + text_width + 5, height - 5], 
                  fill=(255, 255, 255, 230))
    draw.text((text_x, height - 22), label, fill=(60, 60, 60), font=font)
    
    # Save image
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    print(f"Created: {filepath}")

# Generate all components
for category, items in components.items():
    for filename, label in items:
        create_component_image(filename, label, category)

print(f"\nSuccessfully created {sum(len(items) for items in components.values())} facial component images!")
print(f"Location: {output_dir}")
