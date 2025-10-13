"""
PROFESSIONAL PENCIL SKETCH GENERATOR
Using OpenCV and advanced image processing for realistic results
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random

def generate_realistic_face_sketch(prompt):
    """
    Generate a realistic pencil sketch of a human face
    Uses procedural generation with realistic shading and proportions
    """
    
    # Parse prompt
    prompt_lower = prompt.lower()
    is_male = 'male' in prompt_lower or 'man' in prompt_lower
    is_female = 'female' in prompt_lower or 'woman' in prompt_lower
    has_beard = 'beard' in prompt_lower
    has_glasses = 'glasses' in prompt_lower
    is_long_hair = 'long' in prompt_lower
    is_short_hair = 'short' in prompt_lower
    is_bald = 'bald' in prompt_lower
    
    # Default female if not specified
    if not is_male and not is_female:
        is_female = True
        is_long_hair = True
    
    # Create base image
    width, height = 800, 1000
    
    # Start with white canvas
    img = np.ones((height, width), dtype=np.uint8) * 255
    
    # === CREATE REALISTIC FACE BASE ===
    
    center_x = width // 2
    face_top = 150
    face_height = 600
    face_width = 380 if is_female else 400
    
    # Face oval using ellipse
    face_center_y = face_top + face_height // 2
    cv2.ellipse(img, (center_x, face_center_y), (face_width//2, face_height//2), 
                0, 0, 360, 240, -1)
    
    # Add Gaussian blur for soft face base
    img = cv2.GaussianBlur(img, (21, 21), 0)
    
    # Face shading - darker on edges
    face_mask = np.ones((height, width), dtype=np.uint8) * 255
    cv2.ellipse(face_mask, (center_x, face_center_y), (face_width//2 - 50, face_height//2 - 50),
                0, 0, 360, 200, -1)
    cv2.ellipse(face_mask, (center_x, face_center_y), (face_width//2, face_height//2),
                0, 0, 360, 240, 5)
    
    img = cv2.GaussianBlur(img, (51, 51), 0)
    img = np.minimum(img, face_mask)
    
    # Cheekbones (lighter areas)
    cheek_y = face_top + int(face_height * 0.5)
    cv2.ellipse(img, (center_x - 100, cheek_y), (60, 40), 0, 0, 360, 250, -1)
    cv2.ellipse(img, (center_x + 100, cheek_y), (60, 40), 0, 0, 360, 250, -1)
    img = cv2.GaussianBlur(img, (31, 31), 0)
    
    # Forehead highlight
    forehead_y = face_top + 100
    cv2.ellipse(img, (center_x, forehead_y), (120, 80), 0, 0, 360, 250, -1)
    img = cv2.GaussianBlur(img, (31, 31), 0)
    
    # === EYES (REALISTIC) ===
    
    eye_y = face_top + int(face_height * 0.36)
    eye_spacing = 80
    left_eye_x = center_x - eye_spacing
    right_eye_x = center_x + eye_spacing
    
    def draw_eye(img, eye_x, eye_y):
        # Eye socket shadow
        cv2.ellipse(img, (eye_x, eye_y), (50, 35), 0, 0, 360, 210, -1)
        img_local = cv2.GaussianBlur(img, (25, 25), 0)
        
        # Eyeball white
        cv2.ellipse(img_local, (eye_x, eye_y), (35, 18), 0, 0, 360, 245, -1)
        
        # Iris
        cv2.circle(img_local, (eye_x, eye_y), 18, 140, -1)
        
        # Pupil
        cv2.circle(img_local, (eye_x, eye_y), 8, 30, -1)
        
        # Highlight
        cv2.circle(img_local, (eye_x + 5, eye_y - 5), 4, 255, -1)
        
        # Upper eyelid
        pts = np.array([[eye_x - 38, eye_y - 15], [eye_x, eye_y - 20], [eye_x + 38, eye_y - 15]], np.int32)
        cv2.polylines(img_local, [pts], False, 40, 4)
        
        # Lower eyelid
        pts = np.array([[eye_x - 38, eye_y + 15], [eye_x, eye_y + 18], [eye_x + 38, eye_y + 15]], np.int32)
        cv2.polylines(img_local, [pts], False, 80, 2)
        
        # Eyelashes effect
        for i in range(-35, 36, 4):
            x1 = eye_x + i
            y1 = eye_y - 20
            x2 = x1 + random.randint(-3, 3)
            y2 = y1 - random.randint(8, 15)
            cv2.line(img_local, (x1, y1), (x2, y2), 50, 1)
        
        # Eyebrow
        brow_y = eye_y - 50
        pts = np.array([[eye_x - 45, brow_y + 5], [eye_x - 15, brow_y], 
                       [eye_x + 15, brow_y], [eye_x + 45, brow_y + 5]], np.int32)
        cv2.polylines(img_local, [pts], False, 70, 8)
        
        return img_local
    
    img = draw_eye(img, left_eye_x, eye_y)
    img = draw_eye(img, right_eye_x, eye_y)
    
    # === NOSE ===
    
    nose_top_y = eye_y + 50
    nose_bottom_y = face_top + int(face_height * 0.63)
    
    # Nose bridge
    pts = np.array([[center_x - 8, nose_top_y], [center_x - 10, nose_bottom_y - 30]], np.int32)
    cv2.polylines(img, [pts], False, 200, 3)
    pts = np.array([[center_x + 8, nose_top_y], [center_x + 10, nose_bottom_y - 30]], np.int32)
    cv2.polylines(img, [pts], False, 200, 3)
    
    # Nose tip
    cv2.ellipse(img, (center_x, nose_bottom_y - 20), (25, 20), 0, 0, 360, 200, -1)
    img = cv2.GaussianBlur(img, (11, 11), 0)
    
    # Nostrils
    cv2.ellipse(img, (center_x - 18, nose_bottom_y - 5), (8, 6), 0, 180, 360, 80, -1)
    cv2.ellipse(img, (center_x + 18, nose_bottom_y - 5), (8, 6), 0, 180, 360, 80, -1)
    
    # Nose shading
    cv2.ellipse(img, (center_x - 25, nose_bottom_y - 15), (15, 25), 0, 0, 360, 210, -1)
    cv2.ellipse(img, (center_x + 25, nose_bottom_y - 15), (15, 25), 0, 0, 360, 210, -1)
    img = cv2.GaussianBlur(img, (15, 15), 0)
    
    # === MOUTH ===
    
    mouth_y = face_top + int(face_height * 0.78)
    mouth_width = 100 if is_female else 110
    
    # Upper lip
    pts = np.array([
        [center_x - mouth_width//2, mouth_y],
        [center_x - 15, mouth_y - 5],
        [center_x, mouth_y - 8],
        [center_x + 15, mouth_y - 5],
        [center_x + mouth_width//2, mouth_y]
    ], np.int32)
    cv2.polylines(img, [pts], False, 100, 3)
    
    # Lower lip
    cv2.ellipse(img, (center_x, mouth_y + 12), (mouth_width//2, 15), 0, 0, 180, 180, -1)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    
    # Lip highlight
    cv2.ellipse(img, (center_x, mouth_y + 12), (mouth_width//2 - 10, 10), 0, 0, 180, 230, -1)
    
    # Lip line
    cv2.line(img, (center_x - mouth_width//2, mouth_y), 
             (center_x + mouth_width//2, mouth_y), 60, 2)
    
    # === FACIAL CONTOURS ===
    
    chin_y = face_top + face_height
    
    # Jawline shading
    jaw_pts_left = []
    jaw_pts_right = []
    for i in range(0, 100, 5):
        x_offset = int(face_width // 2 - i * 0.5)
        y = chin_y - 80 + i
        jaw_pts_left.append([center_x - x_offset, y])
        jaw_pts_right.append([center_x + x_offset, y])
    
    jaw_pts_left = np.array(jaw_pts_left, np.int32)
    jaw_pts_right = np.array(jaw_pts_right, np.int32)
    
    cv2.polylines(img, [jaw_pts_left], False, 200, 3)
    cv2.polylines(img, [jaw_pts_right], False, 200, 3)
    
    img = cv2.GaussianBlur(img, (11, 11), 0)
    
    # Chin highlight
    cv2.circle(img, (center_x, chin_y - 40), 35, 245, -1)
    img = cv2.GaussianBlur(img, (21, 21), 0)
    
    # Neck
    neck_width = 70
    cv2.rectangle(img, (center_x - neck_width, chin_y), 
                 (center_x + neck_width, height - 50), 220, -1)
    img = cv2.GaussianBlur(img, (21, 21), 0)
    
    # === HAIR ===
    
    hairline_y = face_top + 30
    
    if not is_bald:
        if is_long_hair or is_female:
            # Long hair
            hair_region = np.ones((height, width), dtype=np.uint8) * 255
            
            # Hair mass on sides
            cv2.ellipse(hair_region, (center_x - 180, face_center_y), 
                       (120, 350), 0, 0, 360, 100, -1)
            cv2.ellipse(hair_region, (center_x + 180, face_center_y), 
                       (120, 350), 0, 0, 360, 100, -1)
            
            # Top hair
            cv2.ellipse(hair_region, (center_x, hairline_y - 30), 
                       (200, 100), 0, 0, 360, 100, -1)
            
            # Hair strands
            for i in range(100):
                x1 = center_x + random.randint(-200, 200)
                y1 = hairline_y + random.randint(-20, 50)
                x2 = x1 + random.randint(-30, 30)
                y2 = y1 + random.randint(300, 600)
                cv2.line(hair_region, (x1, y1), (x2, y2), 
                        random.randint(70, 110), 2)
            
            hair_region = cv2.GaussianBlur(hair_region, (15, 15), 0)
            img = np.minimum(img, hair_region)
            
        else:
            # Short hair
            hair_region = np.ones((height, width), dtype=np.uint8) * 255
            
            cv2.ellipse(hair_region, (center_x, hairline_y - 20), 
                       (face_width//2 + 30, 80), 0, 0, 360, 90, -1)
            
            # Hair texture
            for i in range(200):
                x = center_x + random.randint(-face_width//2, face_width//2)
                y = hairline_y + random.randint(-30, 100)
                angle = random.uniform(-0.5, 0.5)
                length = random.randint(10, 25)
                x2 = int(x + length * np.cos(angle))
                y2 = int(y + length * np.sin(angle))
                cv2.line(hair_region, (x, y), (x2, y2), 
                        random.randint(70, 100), 1)
            
            hair_region = cv2.GaussianBlur(hair_region, (9, 9), 0)
            img = np.minimum(img, hair_region)
    
    # === BEARD (if specified) ===
    
    if has_beard and is_male:
        beard_region = np.ones((height, width), dtype=np.uint8) * 255
        
        # Beard mass
        cv2.ellipse(beard_region, (center_x, chin_y - 20), 
                   (90, 100), 0, 0, 180, 90, -1)
        
        # Beard texture
        for i in range(150):
            x = center_x + random.randint(-100, 100)
            y = mouth_y + 30 + random.randint(0, chin_y - mouth_y)
            length = random.randint(8, 18)
            cv2.line(beard_region, (x, y), (x, y + length), 
                    random.randint(70, 100), 1)
        
        beard_region = cv2.GaussianBlur(beard_region, (7, 7), 0)
        img = np.minimum(img, beard_region)
    
    # === GLASSES (if specified) ===
    
    if has_glasses:
        # Left lens
        cv2.ellipse(img, (left_eye_x, eye_y), (42, 28), 0, 0, 360, 60, 3)
        # Right lens
        cv2.ellipse(img, (right_eye_x, eye_y), (42, 28), 0, 0, 360, 60, 3)
        # Bridge
        cv2.line(img, (left_eye_x + 42, eye_y), (right_eye_x - 42, eye_y), 60, 3)
        # Temples
        cv2.line(img, (left_eye_x - 42, eye_y), (left_eye_x - 80, eye_y + 5), 60, 2)
        cv2.line(img, (right_eye_x + 42, eye_y), (right_eye_x + 80, eye_y + 5), 60, 2)
    
    # === PROFESSIONAL PENCIL SKETCH EFFECT ===
    
    # Apply dodge and burn for pencil effect
    img_inv = 255 - img
    img_blur = cv2.GaussianBlur(img_inv, (21, 21), 0)
    
    def dodge(front, back):
        result = front * 255 / (255 - back + 1)
        result[result > 255] = 255
        result[back == 255] = 255
        return result.astype('uint8')
    
    sketch = dodge(img_blur, img)
    
    # Enhance contrast
    sketch = cv2.convertScaleAbs(sketch, alpha=1.3, beta=-20)
    
    # Add pencil texture
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sketch = cv2.filter2D(sketch, -1, kernel)
    
    # Slight blur for smoothness
    sketch = cv2.GaussianBlur(sketch, (3, 3), 0)
    
    # Convert to PIL Image
    sketch_pil = Image.fromarray(sketch)
    
    # Final enhancements
    enhancer = ImageEnhance.Contrast(sketch_pil)
    sketch_pil = enhancer.enhance(1.2)
    
    enhancer = ImageEnhance.Sharpness(sketch_pil)
    sketch_pil = enhancer.enhance(1.5)
    
    # Convert back to RGB
    sketch_rgb = sketch_pil.convert('RGB')
    
    return sketch_rgb
