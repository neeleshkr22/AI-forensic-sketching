"""
REALISTIC HUMAN PORTRAIT GENERATOR
Using proper facial anatomy and smooth photorealistic shading
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
import math

def create_realistic_portrait(prompt):
    """Generate realistic human face portrait with proper anatomy"""
    
    # High resolution canvas
    width, height = 1200, 1600
    
    # Create base image with paper texture
    img = Image.new('L', (width, height), 250)
    
    # Parse prompt
    prompt_lower = prompt.lower()
    is_male = 'male' in prompt_lower or 'man' in prompt_lower
    is_female = 'female' in prompt_lower or 'woman' in prompt_lower
    has_beard = 'beard' in prompt_lower
    has_glasses = 'glasses' in prompt_lower
    is_long_hair = 'long' in prompt_lower
    is_short_hair = 'short' in prompt_lower
    is_bald = 'bald' in prompt_lower
    
    # Default to female if not specified
    if not is_male and not is_female:
        is_female = True
        is_long_hair = True
    
    # Age
    age = 30
    if '20s' in prompt_lower or 'young' in prompt_lower:
        age = 25
    elif '40s' in prompt_lower:
        age = 40
    elif '50s' in prompt_lower or '60s' in prompt_lower:
        age = 55
    
    # === PROPER FACIAL PROPORTIONS (GOLDEN RATIO) ===
    
    face_center_x = width // 2
    face_top = 250
    
    # Standard facial measurements
    face_height = 800
    face_width = 540 if is_female else 560
    
    # Key facial landmarks using standard proportions
    hairline_y = face_top + int(face_height * 0.05)
    eyebrow_y = face_top + int(face_height * 0.25)
    eye_y = face_top + int(face_height * 0.33)
    nose_bottom_y = face_top + int(face_height * 0.60)
    mouth_y = face_top + int(face_height * 0.75)
    chin_y = face_top + face_height
    
    # Eye spacing (standard: one eye width apart)
    eye_width = 80
    eye_spacing = eye_width
    left_eye_x = face_center_x - eye_spacing
    right_eye_x = face_center_x + eye_spacing
    
    # Create pixel array for direct manipulation
    pixels = img.load()
    
    # === HELPER FUNCTIONS ===
    
    def set_pixel_safe(x, y, value):
        """Safely set pixel value"""
        x, y = int(x), int(y)
        if 0 <= x < width and 0 <= y < height:
            # Blend with existing (darker wins)
            current = pixels[x, y]
            pixels[x, y] = min(current, value)
    
    def smooth_circle(cx, cy, radius, center_value, edge_value):
        """Draw smooth gradient circle"""
        for y in range(int(cy - radius - 20), int(cy + radius + 20)):
            for x in range(int(cx - radius - 20), int(cx + radius + 20)):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                if dist <= radius + 20:
                    # Smooth gradient from center to edge
                    ratio = dist / (radius + 20)
                    value = int(center_value + (edge_value - center_value) * ratio)
                    set_pixel_safe(x, y, value)
    
    def smooth_ellipse(cx, cy, rx, ry, center_value, edge_value):
        """Draw smooth gradient ellipse"""
        for y in range(int(cy - ry - 20), int(cy + ry + 20)):
            for x in range(int(cx - rx - 20), int(cx + rx + 20)):
                # Ellipse distance formula
                dist = math.sqrt(((x - cx) / rx)**2 + ((y - cy) / ry)**2)
                if dist <= 1.3:
                    ratio = dist / 1.3
                    value = int(center_value + (edge_value - center_value) * ratio)
                    set_pixel_safe(x, y, value)
    
    def radial_gradient(cx, cy, inner_radius, outer_radius, inner_value, outer_value):
        """Create radial gradient"""
        for y in range(int(cy - outer_radius), int(cy + outer_radius)):
            for x in range(int(cx - outer_radius), int(cx + outer_radius)):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                if inner_radius <= dist <= outer_radius:
                    ratio = (dist - inner_radius) / (outer_radius - inner_radius)
                    value = int(inner_value + (outer_value - inner_value) * ratio)
                    set_pixel_safe(x, y, value)
                elif dist < inner_radius:
                    set_pixel_safe(x, y, inner_value)
    
    # === FACE BASE STRUCTURE ===
    
    # Face oval with proper shading (lighter in center, darker on edges)
    face_radius_y = face_height // 2
    face_radius_x = face_width // 2
    
    smooth_ellipse(face_center_x, face_top + face_radius_y, 
                   face_radius_x, face_radius_y, 240, 180)
    
    # Forehead highlight (lighter area)
    forehead_y = face_top + int(face_height * 0.15)
    smooth_circle(face_center_x, forehead_y, 140, 248, 230)
    
    # Cheekbone highlights
    cheek_y = face_top + int(face_height * 0.50)
    smooth_circle(face_center_x - 140, cheek_y, 80, 245, 220)
    smooth_circle(face_center_x + 140, cheek_y, 80, 245, 220)
    
    # Nose bridge highlight
    nose_top_y = eye_y + 40
    for y in range(int(nose_top_y), int(nose_bottom_y - 30)):
        for x in range(-8, 8):
            px = face_center_x + x
            dist = abs(x)
            value = int(235 - dist * 2)
            set_pixel_safe(px, y, value)
    
    # === EYES (REALISTIC ANATOMY) ===
    
    def draw_realistic_eye(eye_x, eye_y):
        """Draw anatomically correct eye with smooth shading"""
        
        # Eye socket (orbital bone) - darker depression
        radial_gradient(eye_x, eye_y, 0, 65, 215, 235)
        
        # Upper eyelid shadow
        for y in range(-25, -10):
            for x in range(-45, 45):
                dist = math.sqrt(x**2 + (y + 20)**2)
                if dist < 50:
                    value = int(200 - (50 - dist) * 1.5)
                    set_pixel_safe(eye_x + x, eye_y + y, value)
        
        # Eyeball (slightly shaded sphere)
        smooth_ellipse(eye_x, eye_y, 38, 22, 245, 235)
        
        # Iris (detailed with color variation)
        iris_radius = 20
        for y in range(-iris_radius, iris_radius):
            for x in range(-iris_radius, iris_radius):
                dist = math.sqrt(x**2 + y**2)
                if dist < iris_radius:
                    # Radial pattern in iris
                    angle = math.atan2(y, x)
                    pattern = abs(math.sin(angle * 10)) * 20
                    value = int(120 + dist * 2.5 + pattern + random.randint(-8, 8))
                    set_pixel_safe(eye_x + x, eye_y + y, value)
        
        # Pupil (very dark with subtle gradient)
        pupil_radius = 9
        for y in range(-pupil_radius, pupil_radius):
            for x in range(-pupil_radius, pupil_radius):
                dist = math.sqrt(x**2 + y**2)
                if dist < pupil_radius:
                    value = int(25 + dist * 3)
                    set_pixel_safe(eye_x + x, eye_y + y, value)
        
        # Light reflection (catchlight)
        catch_x, catch_y = eye_x + 7, eye_y - 6
        for y in range(-5, 5):
            for x in range(-5, 5):
                dist = math.sqrt(x**2 + y**2)
                if dist < 5:
                    value = int(255 - dist * 10)
                    set_pixel_safe(catch_x + x, catch_y + y, max(value, 230))
        
        # Upper eyelid (dark line with thickness)
        for offset in range(-42, 42):
            lid_curve = abs(offset) * 0.12
            lid_y = eye_y - 20 + int(lid_curve)
            
            for thickness in range(-3, 1):
                value = 40 + abs(thickness) * 25 + random.randint(-10, 10)
                set_pixel_safe(eye_x + offset, lid_y + thickness, value)
        
        # Lower eyelid (lighter)
        for offset in range(-42, 42):
            lid_curve = abs(offset) * 0.08
            lid_y = eye_y + 20 - int(lid_curve)
            
            current = pixels[eye_x + offset, lid_y] if 0 <= eye_x + offset < width and 0 <= lid_y < height else 250
            value = max(40, current - 25)
            set_pixel_safe(eye_x + offset, lid_y, value)
        
        # Eyelashes (subtle individual lashes)
        for i in range(25):
            lash_x_offset = -42 + i * 3.5
            
            if i < 12:
                angle = math.radians(-110 + i * 8)
            else:
                angle = math.radians(-20 + (i - 12) * 6)
            
            lash_length = random.randint(12, 18)
            
            for step in range(lash_length):
                lx = int(eye_x + lash_x_offset + step * math.cos(angle) * 0.8)
                ly = int(eye_y - 20 + step * math.sin(angle) * 0.8)
                
                if step < 3:
                    value = 35
                else:
                    value = 35 + step * 8
                
                set_pixel_safe(lx, ly, value)
                set_pixel_safe(lx + 1, ly, value + 20)
        
        # Eyebrow (natural hair pattern)
        brow_y = eye_y - 60
        
        # Brow base shadow
        for y in range(-10, 18):
            for x in range(-50, 50):
                if y < 8:
                    value = 190 - abs(y) * 5 + random.randint(-10, 10)
                    set_pixel_safe(eye_x + x, brow_y + y, value)
        
        # Individual brow hairs
        for i in range(80):
            hair_x = eye_x - 50 + random.randint(0, 100)
            hair_angle = math.radians(random.randint(-15, 25))
            hair_length = random.randint(10, 18)
            
            for step in range(hair_length):
                hx = int(hair_x + step * math.cos(hair_angle))
                hy = int(brow_y + step * math.sin(hair_angle))
                
                value = 70 + step * 5 + random.randint(-15, 15)
                set_pixel_safe(hx, hy, value)
    
    # Draw both eyes
    draw_realistic_eye(left_eye_x, eye_y)
    draw_realistic_eye(right_eye_x, eye_y)
    
    # === NOSE (PROPER ANATOMY) ===
    
    # Nose bridge shading
    for y in range(int(nose_top_y), int(nose_bottom_y - 40)):
        for x in range(-15, 15):
            dist = abs(x)
            value = int(220 - dist * 1.5)
            set_pixel_safe(face_center_x + x, y, value)
    
    # Nose tip (bulbous shape)
    nose_tip_y = nose_bottom_y - 25
    smooth_circle(face_center_x, nose_tip_y, 35, 215, 200)
    
    # Nostrils (dark with proper shape)
    nostril_y = nose_bottom_y - 10
    nostril_offset = 22
    
    for side in [-1, 1]:
        nostril_x = face_center_x + side * nostril_offset
        
        # Nostril shadow
        for y in range(-10, 12):
            for x in range(-8, 8):
                dist = math.sqrt((x * 1.3)**2 + y**2)
                if dist < 9:
                    value = int(70 + dist * 10)
                    set_pixel_safe(int(nostril_x + x), int(nostril_y + y), value)
        
        # Nostril rim
        for angle in range(180, 360, 5):
            rad = math.radians(angle)
            rim_x = nostril_x + 9 * math.cos(rad)
            rim_y = nostril_y + 6 * math.sin(rad)
            set_pixel_safe(rim_x, rim_y, 90)
    
    # Nose sides shading
    for y in range(int(nose_bottom_y - 50), int(nose_bottom_y + 15)):
        for side in [-1, 1]:
            for x in range(20, 45):
                dist = x - 20
                value = int(215 - dist * 1.2)
                set_pixel_safe(face_center_x + side * x, y, value)
    
    # === MOUTH (REALISTIC LIPS) ===
    
    # Philtrum (indent from nose to upper lip)
    philtrum_top_y = nose_bottom_y + 30
    for y in range(int(philtrum_top_y), int(mouth_y - 15)):
        for x in range(-6, 6):
            dist = abs(x)
            value = int(220 - dist * 3)
            set_pixel_safe(face_center_x + x, y, value)
    
    # Mouth dimensions
    mouth_width = 120 if is_female else 130
    
    # Upper lip (with cupid's bow)
    for y in range(-18, 2):
        for x in range(-mouth_width//2, mouth_width//2):
            # Cupid's bow shape
            bow_curve = 0
            if abs(x) < 20:
                bow_curve = -10 + (abs(x) / 20) ** 2 * 10
            else:
                bow_curve = -5
            
            if y > bow_curve:
                dist_from_edge = min(abs(y - bow_curve), abs(y + 18))
                value = int(180 - dist_from_edge * 4)
                set_pixel_safe(face_center_x + x, mouth_y + y, value)
    
    # Lower lip (fuller, with highlight)
    for y in range(0, 30):
        for x in range(-mouth_width//2, mouth_width//2):
            # Elliptical shape
            lip_dist = math.sqrt((x / (mouth_width//2))**2 + ((y - 15) / 18)**2)
            
            if lip_dist < 1.0:
                # Center highlight
                value = int(210 + (1.0 - lip_dist) * 35)
                set_pixel_safe(face_center_x + x, mouth_y + y, value)
    
    # Lip line (separation between lips)
    for x in range(-mouth_width//2, mouth_width//2):
        for thickness in range(-2, 2):
            value = 60 + abs(thickness) * 20
            set_pixel_safe(face_center_x + x, mouth_y + thickness, value)
    
    # Mouth corners (shadow)
    for corner in [-mouth_width//2, mouth_width//2]:
        for y in range(-8, 12):
            for x in range(-10, 10):
                dist = math.sqrt(x**2 + y**2)
                if dist < 10:
                    value = int(170 - (10 - dist) * 6)
                    set_pixel_safe(face_center_x + corner + x, mouth_y + y, value)
    
    # === FACIAL CONTOURS ===
    
    # Jawline shading
    for x in range(face_center_x - face_width//2, face_center_x + face_width//2):
        dist_from_center = abs(x - face_center_x)
        jaw_y = int(chin_y - 60 - (dist_from_center / 5))
        
        for y in range(jaw_y, chin_y + 30):
            value = int(215 - (y - jaw_y) * 1.8)
            set_pixel_safe(x, y, value)
    
    # Chin highlight
    smooth_circle(face_center_x, chin_y - 30, 50, 245, 220)
    
    # Neck shading
    neck_top = chin_y + 10
    for y in range(neck_top, min(neck_top + 200, height)):
        for x in range(face_center_x - 90, face_center_x + 90):
            dist_from_center = abs(x - face_center_x)
            value = int(220 - dist_from_center * 0.6 - (y - neck_top) * 0.4)
            set_pixel_safe(x, y, value)
    
    # === HAIR (REALISTIC TEXTURE) ===
    
    if not is_bald:
        if is_long_hair or is_female:
            # Long flowing hair
            for strand in range(150):
                start_x = face_center_x - face_width//2 - 60 + random.randint(0, face_width + 120)
                start_y = hairline_y + random.randint(-30, 80)
                
                angle = math.radians(85 + random.randint(-15, 15))
                length = random.randint(500, 900)
                
                for step in range(0, length, 3):
                    # Wave pattern
                    wave = math.sin(step * 0.02) * 25
                    
                    x = start_x + step * math.cos(angle) + wave
                    y = start_y + step * math.sin(angle)
                    
                    # Hair darkness (gradient)
                    darkness = 80 + (step / length) * 60 + random.randint(-20, 20)
                    
                    # Draw thick strand
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            set_pixel_safe(x + dx, y + dy, int(darkness))
        else:
            # Short hair
            for i in range(300):
                hx = face_center_x - face_width//2 - 30 + random.randint(0, face_width + 60)
                hy = hairline_y + random.randint(-20, 140)
                
                angle = random.uniform(-0.6, 0.6)
                length = random.randint(18, 45)
                darkness = random.randint(70, 110)
                
                for step in range(length):
                    sx = int(hx + step * math.cos(angle))
                    sy = int(hy + step * math.sin(angle))
                    set_pixel_safe(sx, sy, darkness)
                    set_pixel_safe(sx + 1, sy, darkness + 10)
    
    # === BEARD (IF SPECIFIED) ===
    
    if has_beard and is_male:
        beard_top = mouth_y + 35
        
        for i in range(400):
            bx = face_center_x + random.randint(-120, 120)
            by = beard_top + random.randint(0, chin_y - beard_top + 80)
            
            angle = math.radians(90 + random.randint(-30, 30))
            length = random.randint(8, 20)
            darkness = random.randint(60, 90)
            
            for step in range(length):
                sx = int(bx + step * math.cos(angle))
                sy = int(by + step * math.sin(angle))
                set_pixel_safe(sx, sy, darkness)
    
    # === POST-PROCESSING FOR PHOTOREALISM ===
    
    # Convert to RGB
    img = img.convert('RGB')
    
    # Strong Gaussian blur for smooth pencil shading
    img = img.filter(ImageFilter.GaussianBlur(radius=2.5))
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.35)
    
    # Sharpen details
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=180, threshold=2))
    
    # Add paper texture
    from PIL import ImageChops
    
    noise = Image.new('L', (width, height), 255)
    noise_pixels = noise.load()
    for _ in range(8000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        noise_pixels[x, y] = random.randint(242, 255)
    
    noise = noise.filter(ImageFilter.GaussianBlur(radius=0.3))
    img_gray = img.convert('L')
    img_gray = ImageChops.multiply(img_gray, noise)
    img = img_gray.convert('RGB')
    
    # Final contrast boost
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.15)
    
    # Slight brightness adjustment
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.05)
    
    return img
