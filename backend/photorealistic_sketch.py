"""
PHOTOREALISTIC PENCIL PORTRAIT GENERATOR
Creates realistic human face sketches with smooth shading like the reference image
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
import math

def generate_photorealistic_sketch(prompt):
    """Generate photorealistic pencil sketch portrait"""
    
    # High resolution for smooth shading
    width, height = 1200, 1400
    
    # Start with off-white paper
    img = Image.new('RGB', (width, height), color='#F8F6F0')
    draw = ImageDraw.Draw(img)
    
    # Parse prompt
    prompt_lower = prompt.lower()
    is_male = 'male' in prompt_lower or 'man' in prompt_lower
    is_female = 'female' in prompt_lower or 'woman' in prompt_lower
    has_beard = 'beard' in prompt_lower
    has_glasses = 'glasses' in prompt_lower
    is_long_hair = 'long' in prompt_lower
    is_short_hair = 'short' in prompt_lower
    is_bald = 'bald' in prompt_lower
    
    # Age
    age = 30
    if '20s' in prompt_lower or 'young' in prompt_lower:
        age = 25
    elif '40s' in prompt_lower:
        age = 45
    elif '50s' in prompt_lower or '60s' in prompt_lower:
        age = 55
    
    # Default to female with long hair if gender not specified
    if not is_male and not is_female:
        is_female = True
        is_long_hair = True
    
    # Face positioning
    face_center_x = width // 2
    face_top = 200
    face_width = 450 if is_female else 480
    face_height = 580
    
    # === SMOOTH SHADING HELPER ===
    def smooth_gradient(bbox, start_gray, end_gray, direction='radial', center=None):
        """Create smooth gradient shading"""
        x1, y1, x2, y2 = bbox
        w, h = x2 - x1, y2 - y1
        
        for y in range(int(y1), int(y2)):
            for x in range(int(x1), int(x2)):
                if direction == 'radial' and center:
                    # Radial gradient from center
                    cx, cy = center
                    dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                    max_dist = math.sqrt(w**2 + h**2) / 2
                    ratio = min(dist / max_dist, 1.0)
                elif direction == 'vertical':
                    ratio = (y - y1) / h
                elif direction == 'horizontal':
                    ratio = (x - x1) / w
                else:
                    ratio = 0.5
                
                gray = int(start_gray + (end_gray - start_gray) * ratio)
                gray = max(0, min(255, gray))
                
                # Add subtle noise for pencil texture
                noise = random.randint(-3, 3)
                gray = max(0, min(255, gray + noise))
                
                try:
                    current = img.getpixel((x, y))
                    # Blend with existing
                    new_gray = min(current[0], gray)
                    img.putpixel((x, y), (new_gray, new_gray, new_gray))
                except:
                    pass
    
    def soft_ellipse(center, radius_x, radius_y, darkness=200, blur_amount=15):
        """Draw soft ellipse with gradient"""
        cx, cy = center
        
        # Create temporary layer
        temp = Image.new('L', (width, height), 255)
        temp_draw = ImageDraw.Draw(temp)
        
        # Draw filled ellipse
        temp_draw.ellipse([cx - radius_x, cy - radius_y, cx + radius_x, cy + radius_y],
                         fill=darkness)
        
        # Blur for softness
        temp = temp.filter(ImageFilter.GaussianBlur(radius=blur_amount))
        
        # Composite
        img_temp = img.convert('L')
        img_temp = Image.composite(temp, img_temp, temp)
        
        return img_temp.convert('RGB')
    
    # === FACE BASE STRUCTURE ===
    
    # Face shape (smooth oval with shading)
    face_left = face_center_x - face_width // 2
    face_right = face_center_x + face_width // 2
    face_bottom = face_top + face_height
    
    # Face oval shading (darker on edges, lighter in center)
    for angle in range(0, 360, 2):
        rad = math.radians(angle)
        
        # Outer edge
        outer_x = face_center_x + (face_width // 2 + 40) * math.cos(rad)
        outer_y = face_top + face_height // 2 + (face_height // 2 + 40) * math.sin(rad)
        
        # Inner lighter area
        inner_x = face_center_x + (face_width // 2 - 100) * math.cos(rad)
        inner_y = face_top + face_height // 2 + (face_height // 2 - 100) * math.sin(rad)
        
        # Draw gradient line from outer to inner
        steps = 70
        for i in range(steps):
            t = i / steps
            x = outer_x + (inner_x - outer_x) * t
            y = outer_y + (inner_y - outer_y) * t
            
            # Darkness decreases toward center
            gray = int(120 + 135 * t)
            
            try:
                img.putpixel((int(x), int(y)), (gray, gray, gray))
            except:
                pass
    
    # Cheekbone highlights (lighter areas)
    cheek_left_x = face_center_x - 120
    cheek_right_x = face_center_x + 120
    cheek_y = face_top + face_height // 2
    
    for y in range(-40, 60):
        for x in range(-50, 50):
            dist = math.sqrt(x**2 + y**2)
            if dist < 50:
                gray = int(245 - dist * 1.5)
                px_left = cheek_left_x + x
                py = cheek_y + y
                px_right = cheek_right_x + x
                
                try:
                    current_left = img.getpixel((px_left, py))
                    img.putpixel((px_left, py), (max(current_left[0], gray), max(current_left[0], gray), max(current_left[0], gray)))
                    
                    current_right = img.getpixel((px_right, py))
                    img.putpixel((px_right, py), (max(current_right[0], gray), max(current_right[0], gray), max(current_right[0], gray)))
                except:
                    pass
    
    # Nose bridge shadow (subtle vertical shadow)
    nose_x = face_center_x
    nose_top = face_top + 280
    nose_bottom = face_top + 480
    
    for y in range(int(nose_top), int(nose_bottom)):
        for offset in range(-12, 12):
            x = nose_x + offset
            dist = abs(offset)
            gray = int(200 - dist * 3)
            
            try:
                current = img.getpixel((x, y))
                img.putpixel((x, y), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
            except:
                pass
    
    # Nose tip (rounded shading)
    nose_tip_y = nose_bottom - 20
    for y in range(-25, 25):
        for x in range(-30, 30):
            dist = math.sqrt(x**2 + (y*1.2)**2)
            if dist < 25:
                gray = int(190 - dist * 2)
                px = nose_x + x
                py = nose_tip_y + y
                
                try:
                    current = img.getpixel((px, py))
                    img.putpixel((px, py), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
                except:
                    pass
    
    # Nostrils (small dark areas)
    nostril_left_x = nose_x - 18
    nostril_right_x = nose_x + 18
    nostril_y = nose_bottom - 10
    
    for nostril_x in [nostril_left_x, nostril_right_x]:
        for y in range(-8, 8):
            for x in range(-6, 6):
                dist = math.sqrt((x*1.5)**2 + y**2)
                if dist < 6:
                    gray = int(80 + dist * 10)
                    px = nostril_x + x
                    py = nostril_y + y
                    
                    try:
                        current = img.getpixel((px, py))
                        img.putpixel((px, py), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
                    except:
                        pass
    
    # === EYES (PHOTOREALISTIC) ===
    
    eye_y = face_top + 280
    eye_spacing = 200 if is_female else 210
    left_eye_x = face_center_x - eye_spacing // 2
    right_eye_x = face_center_x + eye_spacing // 2
    
    def draw_photorealistic_eye(eye_x, eye_y, is_left=True):
        """Draw realistic eye with smooth shading"""
        
        # Eye socket shadow (deep gradient)
        for y in range(-45, 50):
            for x in range(-55, 55):
                dist = math.sqrt(x**2 + (y*0.8)**2)
                if dist < 50:
                    gray = int(200 - (50 - dist) * 1.2)
                    px = eye_x + x
                    py = eye_y + y
                    
                    try:
                        current = img.getpixel((px, py))
                        img.putpixel((px, py), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
                    except:
                        pass
        
        # Eyeball white (slightly shaded)
        for y in range(-18, 18):
            for x in range(-40, 40):
                dist = math.sqrt((x*0.6)**2 + y**2)
                if dist < 20:
                    gray = int(235 + dist * 0.5)
                    px = eye_x + x
                    py = eye_y + y
                    
                    try:
                        img.putpixel((px, py), (gray, gray, gray))
                    except:
                        pass
        
        # Iris (detailed with radial gradient)
        iris_radius = 22
        for y in range(-iris_radius, iris_radius):
            for x in range(-iris_radius, iris_radius):
                dist = math.sqrt(x**2 + y**2)
                if dist < iris_radius:
                    # Radial pattern
                    angle = math.atan2(y, x)
                    pattern = abs(math.sin(angle * 8)) * 15
                    gray = int(110 + dist * 2 + pattern)
                    px = eye_x + x
                    py = eye_y + y
                    
                    try:
                        img.putpixel((px, py), (gray, gray, gray))
                    except:
                        pass
        
        # Pupil (very dark with highlight)
        pupil_radius = 10
        for y in range(-pupil_radius, pupil_radius):
            for x in range(-pupil_radius, pupil_radius):
                dist = math.sqrt(x**2 + y**2)
                if dist < pupil_radius:
                    gray = int(30 + dist * 2)
                    px = eye_x + x
                    py = eye_y + y
                    
                    try:
                        img.putpixel((px, py), (gray, gray, gray))
                    except:
                        pass
        
        # Eye highlight (light reflection)
        highlight_x = eye_x + 6
        highlight_y = eye_y - 6
        for y in range(-4, 4):
            for x in range(-4, 4):
                dist = math.sqrt(x**2 + y**2)
                if dist < 4:
                    gray = int(255 - dist * 20)
                    px = highlight_x + x
                    py = highlight_y + y
                    
                    try:
                        img.putpixel((px, py), (gray, gray, gray))
                    except:
                        pass
        
        # Upper eyelid (dark curved line)
        for offset_x in range(-42, 42):
            lid_y = int(eye_y - 18 + abs(offset_x) * 0.15)
            for thick in range(-2, 3):
                px = eye_x + offset_x
                py = lid_y + thick
                gray = 40 + abs(thick) * 15
                
                try:
                    current = img.getpixel((px, py))
                    img.putpixel((px, py), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
                except:
                    pass
        
        # Lower eyelid (lighter)
        for offset_x in range(-42, 42):
            lid_y = int(eye_y + 18 - abs(offset_x) * 0.1)
            px = eye_x + offset_x
            py = lid_y
            
            try:
                current = img.getpixel((px, py))
                gray = current[0] - 30
                img.putpixel((px, py), (max(0, gray), max(0, gray), max(0, gray)))
            except:
                pass
        
        # Eyelashes (soft individual lashes)
        for i in range(30):
            lash_x = eye_x - 42 + i * 2.8
            if i < 15:
                lash_angle = math.radians(-95 + i * 5)
            else:
                lash_angle = math.radians(-20 + (i - 15) * 5)
            
            lash_length = random.randint(10, 16)
            
            for step in range(lash_length):
                lx = int(lash_x + step * math.cos(lash_angle))
                ly = int(eye_y - 18 + step * math.sin(lash_angle))
                
                try:
                    current = img.getpixel((lx, ly))
                    gray = max(0, current[0] - 40)
                    img.putpixel((lx, ly), (gray, gray, gray))
                except:
                    pass
        
        # Eyebrow (smooth shading with hair texture)
        brow_y = eye_y - 55
        brow_length = 85
        
        # Brow shadow base
        for y in range(-8, 15):
            for x in range(-brow_length//2, brow_length//2):
                dist_y = abs(y)
                gray = int(180 - dist_y * 8)
                px = eye_x + x
                py = brow_y + y
                
                try:
                    current = img.getpixel((px, py))
                    img.putpixel((px, py), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
                except:
                    pass
        
        # Individual brow hairs
        for i in range(60):
            hair_x = eye_x - brow_length//2 + random.randint(0, brow_length)
            hair_angle = math.radians(10 + random.randint(-20, 20))
            hair_length = random.randint(8, 14)
            
            for step in range(hair_length):
                hx = int(hair_x + step * math.cos(hair_angle))
                hy = int(brow_y + step * math.sin(hair_angle))
                
                try:
                    current = img.getpixel((hx, hy))
                    gray = max(0, current[0] - random.randint(30, 50))
                    img.putpixel((hx, hy), (gray, gray, gray))
                except:
                    pass
    
    # Draw both eyes
    draw_photorealistic_eye(left_eye_x, eye_y, True)
    draw_photorealistic_eye(right_eye_x, eye_y, False)
    
    # === LIPS (SMOOTH AND REALISTIC) ===
    
    mouth_y = nose_bottom + 100
    mouth_width = 130 if is_female else 140
    
    # Philtrum (groove from nose to upper lip)
    philtrum_x = face_center_x
    for y in range(int(nose_bottom + 20), int(mouth_y - 10)):
        for x in range(-5, 5):
            px = philtrum_x + x
            dist = abs(x)
            gray = int(210 - dist * 5)
            
            try:
                current = img.getpixel((px, y))
                img.putpixel((px, y), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
            except:
                pass
    
    # Upper lip (smooth shading with cupid's bow)
    for y in range(-15, 5):
        for x in range(-mouth_width//2, mouth_width//2):
            # Cupid's bow shape
            center_dist = abs(x)
            bow_height = int(-10 + (center_dist / 15) ** 2) if center_dist < 20 else -8
            
            if y > bow_height and y < 0:
                dist_from_edge = min(abs(y - bow_height), abs(y))
                gray = int(170 - dist_from_edge * 10)
                px = face_center_x + x
                py = mouth_y + y
                
                try:
                    current = img.getpixel((px, py))
                    img.putpixel((px, py), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
                except:
                    pass
    
    # Lower lip (fuller, lighter)
    for y in range(0, 28):
        for x in range(-mouth_width//2, mouth_width//2):
            # Elliptical shape
            dist = math.sqrt((x / (mouth_width//2))**2 + ((y - 14) / 14)**2)
            
            if dist < 1.0:
                # Lighter in center (highlight)
                gray = int(190 + (1.0 - dist) * 40)
                px = face_center_x + x
                py = mouth_y + y
                
                try:
                    current = img.getpixel((px, py))
                    img.putpixel((px, py), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
                except:
                    pass
    
    # Lip line (separation)
    for x in range(-mouth_width//2, mouth_width//2):
        px = face_center_x + x
        for thick in range(-1, 2):
            py = mouth_y + thick
            
            try:
                current = img.getpixel((px, py))
                gray = max(0, current[0] - 60)
                img.putpixel((px, py), (gray, gray, gray))
            except:
                pass
    
    # Mouth corners (slightly darker)
    for corner_x in [face_center_x - mouth_width//2, face_center_x + mouth_width//2]:
        for y in range(-5, 10):
            for x in range(-8, 8):
                dist = math.sqrt(x**2 + y**2)
                if dist < 8:
                    gray = int(160 - (8 - dist) * 5)
                    px = corner_x + x
                    py = mouth_y + y
                    
                    try:
                        current = img.getpixel((px, py))
                        img.putpixel((px, py), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
                    except:
                        pass
    
    # === HAIR (FLOWING AND REALISTIC) ===
    
    hairline_y = face_top + 20
    
    if not is_bald:
        if is_long_hair or is_female:
            # Long flowing hair with smooth strands
            for strand in range(120):
                start_x = face_left - 40 + random.randint(0, face_width + 80)
                start_y = hairline_y + random.randint(-20, 60)
                
                # Create flowing curve
                angle = math.radians(random.randint(70, 110))
                length = random.randint(400, 700)
                
                prev_x, prev_y = start_x, start_y
                
                for step in range(0, length, 5):
                    t = step / length
                    
                    # Wavy pattern
                    wave = math.sin(step * 0.03) * 15
                    
                    x = start_x + step * math.cos(angle) + wave
                    y = start_y + step * math.sin(angle)
                    
                    # Draw strand with gradient darkness
                    darkness = int(80 + t * 40 + random.randint(-15, 15))
                    
                    # Draw thick strand
                    for radius in range(1, 3):
                        for dy in range(-radius, radius + 1):
                            for dx in range(-radius, radius + 1):
                                if dx*dx + dy*dy <= radius*radius:
                                    px = int(x + dx)
                                    py = int(y + dy)
                                    
                                    if 0 <= px < width and 0 <= py < height:
                                        try:
                                            current = img.getpixel((px, py))
                                            img.putpixel((px, py), (min(current[0], darkness), min(current[0], darkness), min(current[0], darkness)))
                                        except:
                                            pass
                    
                    prev_x, prev_y = x, y
        
        else:
            # Short hair (male style)
            for i in range(250):
                x = face_left - 20 + random.randint(0, face_width + 40)
                y = hairline_y + random.randint(-10, 120)
                
                angle = random.uniform(-0.5, 0.5)
                length = random.randint(15, 35)
                darkness = random.randint(60, 100)
                
                for step in range(length):
                    sx = int(x + step * math.cos(angle))
                    sy = int(y + step * math.sin(angle))
                    
                    if 0 <= sx < width and 0 <= sy < height:
                        try:
                            current = img.getpixel((sx, sy))
                            img.putpixel((sx, sy), (min(current[0], darkness), min(current[0], darkness), min(current[0], darkness)))
                        except:
                            pass
    
    # === FACIAL CONTOURS ===
    
    # Jawline shadow (soft gradient)
    for x in range(face_left + 30, face_right - 30):
        distance_from_center = abs(x - face_center_x)
        jaw_y = int(face_bottom - 30 - (distance_from_center / 4))
        
        for y in range(jaw_y, face_bottom + 20):
            dist = y - jaw_y
            gray = int(200 - dist * 1.5)
            
            try:
                current = img.getpixel((x, y))
                img.putpixel((x, y), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
            except:
                pass
    
    # Neck shadow
    neck_top = face_bottom
    for y in range(neck_top, min(neck_top + 150, height)):
        for x in range(face_center_x - 70, face_center_x + 70):
            dist_from_center = abs(x - face_center_x)
            gray = int(210 - dist_from_center * 0.5 - (y - neck_top) * 0.3)
            
            try:
                current = img.getpixel((x, y))
                img.putpixel((x, y), (min(current[0], gray), min(current[0], gray), min(current[0], gray)))
            except:
                pass
    
    # === POST-PROCESSING FOR REALISM ===
    
    # Apply Gaussian blur for smooth pencil effect
    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    
    # Slight sharpening for detail
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # Add subtle paper texture
    noise = Image.new('L', (width, height), 255)
    noise_pixels = noise.load()
    for _ in range(5000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        noise_pixels[x, y] = random.randint(245, 255)
    
    noise = noise.filter(ImageFilter.GaussianBlur(radius=0.2))
    
    # Composite with original
    from PIL import ImageChops
    img_gray = img.convert('L')
    img_gray = ImageChops.multiply(img_gray, noise)
    img = img_gray.convert('RGB')
    
    # Final contrast adjustment
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.1)
    
    return img
