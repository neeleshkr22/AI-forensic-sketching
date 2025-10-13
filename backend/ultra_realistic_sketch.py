"""
ULTRA REALISTIC FORENSIC SKETCH GENERATOR
Professional hand-drawn quality with maximum realism
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import random
import math

def generate_ultra_realistic_sketch(prompt):
    """Generate EXTREMELY realistic hand-drawn forensic sketch"""
    
    # High-resolution canvas for maximum detail
    width, height = 1200, 1400
    # Off-white paper color for authentic look
    img = Image.new('RGB', (width, height), color='#F5F3ED')
    draw = ImageDraw.Draw(img)
    
    # Parse features from prompt
    prompt_lower = prompt.lower()
    is_male = 'male' in prompt_lower or 'man' in prompt_lower
    has_beard = 'beard' in prompt_lower
    has_glasses = 'glasses' in prompt_lower
    is_bald = 'bald' in prompt_lower
    is_long_hair = 'long hair' in prompt_lower
    is_curly = 'curly' in prompt_lower
    
    # Age detection
    age = 30
    if '20s' in prompt_lower or 'young' in prompt_lower:
        age = 25
    elif '40s' in prompt_lower:
        age = 40
    elif '50s' in prompt_lower or '60s' in prompt_lower or 'elderly' in prompt_lower:
        age = 55
    
    # === ULTRA REALISTIC DRAWING HELPERS ===
    
    def organic_line(p1, p2, darkness=30, width=2, waviness=1.2):
        """Draw extremely organic, hand-drawn line with natural tremor"""
        x1, y1 = p1
        x2, y2 = p2
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        steps = max(int(distance / 0.8), 4)
        
        points = []
        for i in range(steps + 1):
            t = i / steps
            # Base position with bezier-like curve
            mid_push = math.sin(t * math.pi) * waviness
            x = x1 + (x2-x1) * t + random.gauss(0, mid_push)
            y = y1 + (y2-y1) * t + random.gauss(0, mid_push)
            
            # Natural hand tremor
            tremor = 0.4
            x += random.gauss(0, tremor)
            y += random.gauss(0, tremor)
            
            points.append((x, y))
        
        # Draw with varying pressure
        for i in range(len(points) - 1):
            progress = i / len(points)
            # Pressure curve (stronger in middle)
            pressure = 1.0 - abs(progress - 0.5) * 0.4
            pressure *= random.uniform(0.8, 1.2)
            
            gray = int(darkness / pressure)
            gray = max(15, min(90, gray))
            line_width = max(1, int(width * pressure))
            
            draw.line([points[i], points[i+1]], fill=(gray, gray, gray), width=line_width)
            
            # Add micro-texture (graphite grain)
            if random.random() > 0.6:
                draw.point(points[i], fill=(gray + 10, gray + 10, gray + 10))
    
    def advanced_crosshatch(bbox, layers=3, base_darkness=45):
        """Multi-layer cross-hatching for professional depth"""
        x1, y1, x2, y2 = bbox
        w, h = x2 - x1, y2 - y1
        
        angles = [30, -30, 60, -60, 0, 90]  # More angles = more realistic
        
        for layer in range(layers):
            darkness = base_darkness - (layer * 8)
            spacing = 4 + (layer * 3)
            
            # Use subset of angles per layer
            layer_angles = angles[:2 + layer]
            
            for angle in layer_angles:
                # Calculate hatching lines
                for offset in range(0, max(w, h), spacing):
                    if angle == 0:
                        # Horizontal
                        y = y1 + offset
                        if y < y2:
                            organic_line((x1, y), (x2, y), darkness, 1, 0.3)
                    elif angle == 90:
                        # Vertical
                        x = x1 + offset
                        if x < x2:
                            organic_line((x, y1), (x, y2), darkness, 1, 0.3)
                    else:
                        # Diagonal
                        rad = math.radians(angle)
                        # Start from edges
                        for start in range(-max(w,h), max(w,h), spacing):
                            sx = x1 + start
                            sy = y1
                            ex = sx + h * math.tan(rad)
                            ey = y2
                            
                            # Clip to bounds
                            if x1 <= sx <= x2 and y1 <= sy <= y2:
                                if x1 <= ex <= x2 and y1 <= ey <= y2:
                                    organic_line((sx, sy), (ex, ey), darkness + random.randint(-5, 5), 1, 0.2)
    
    def stipple_gradient(center, radius, darkness=40, density=200):
        """Advanced stippling with gradient density"""
        cx, cy = center
        for _ in range(density):
            angle = random.uniform(0, 2 * math.pi)
            # Gradient: more dots toward center
            r = random.betavariate(2, 5) * radius
            
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            
            # Dot size and darkness vary with distance
            distance_ratio = r / radius
            dot_darkness = int(darkness * (1.5 - distance_ratio))
            dot_size = max(1, int(2 * (1 - distance_ratio * 0.5)))
            
            if random.random() > 0.2:  # 80% fill
                for dx in range(-dot_size, dot_size + 1):
                    for dy in range(-dot_size, dot_size + 1):
                        if dx*dx + dy*dy <= dot_size*dot_size:
                            px, py = int(x + dx), int(y + dy)
                            if 0 <= px < width and 0 <= py < height:
                                draw.point((px, py), fill=(dot_darkness, dot_darkness, dot_darkness))
    
    # === FACE STRUCTURE (PROFESSIONAL PROPORTIONS) ===
    
    face_center_x = width // 2
    face_top = 150
    face_bottom = 1050
    face_width = 380
    face_left = face_center_x - face_width // 2
    face_right = face_center_x + face_width // 2
    
    # Face outline with organic curves
    # Left side of face
    left_points = [
        (face_left + 20, face_top + 50),
        (face_left, face_top + 200),
        (face_left - 10, face_top + 400),
        (face_left + 5, face_top + 600),
        (face_left + 30, face_top + 750),
        (face_left + 70, face_top + 850),
        (face_center_x - 40, face_bottom)
    ]
    for i in range(len(left_points) - 1):
        organic_line(left_points[i], left_points[i+1], 25, 3, 1.0)
    
    # Right side of face (mirror)
    right_points = [
        (face_right - 20, face_top + 50),
        (face_right, face_top + 200),
        (face_right + 10, face_top + 400),
        (face_right - 5, face_top + 600),
        (face_right - 30, face_top + 750),
        (face_right - 70, face_top + 850),
        (face_center_x + 40, face_bottom)
    ]
    for i in range(len(right_points) - 1):
        organic_line(right_points[i], right_points[i+1], 25, 3, 1.0)
    
    # Chin connection
    organic_line((face_center_x - 40, face_bottom), (face_center_x + 40, face_bottom), 25, 3, 0.5)
    
    # Cheekbones (subtle shading)
    advanced_crosshatch([face_left + 30, face_top + 500, face_left + 90, face_top + 600], 2, 70)
    advanced_crosshatch([face_right - 90, face_top + 500, face_right - 30, face_top + 600], 2, 70)
    
    # Jawline definition
    organic_line((face_left + 70, face_top + 850), (face_center_x - 20, face_bottom - 10), 30, 2, 0.8)
    organic_line((face_right - 70, face_top + 850), (face_center_x + 20, face_bottom - 10), 30, 2, 0.8)
    
    # === HAIR (ULTRA DETAILED) ===
    
    hairline_y = face_top + 40
    
    if not is_bald:
        if is_long_hair:
            # Long flowing hair with individual strands
            for i in range(60):
                start_x = face_left - 30 + i * 7
                start_y = hairline_y + random.randint(-10, 20)
                
                # Create flowing curve
                mid_x = start_x + random.randint(-20, 20)
                mid_y = start_y + 300 + random.randint(-50, 50)
                end_x = start_x + random.randint(-30, 30)
                end_y = start_y + 600 + random.randint(-100, 100)
                
                # Draw strand with organic curves
                points = [(start_x, start_y), (mid_x, mid_y), (end_x, end_y)]
                for j in range(len(points) - 1):
                    organic_line(points[j], points[j+1], 35, 2, 1.5)
        
        elif is_curly:
            # Curly hair with tight spirals
            for i in range(40):
                start_x = face_left + i * 10
                start_y = hairline_y + random.randint(-5, 15)
                
                # Draw spiral
                for turn in range(4):
                    angle = turn * math.pi / 2
                    radius = 15
                    x1 = start_x + radius * math.cos(angle)
                    y1 = start_y + turn * 20 + radius * math.sin(angle)
                    x2 = start_x + radius * math.cos(angle + math.pi/2)
                    y2 = start_y + (turn + 0.5) * 20 + radius * math.sin(angle + math.pi/2)
                    organic_line((x1, y1), (x2, y2), 30, 2, 0.5)
        
        else:
            # Short hair texture (male typical)
            for i in range(200):
                x = face_left + random.randint(-20, face_width + 20)
                y = hairline_y + random.randint(-10, 100)
                
                # Short strokes with varied angles
                angle = random.uniform(-0.5, 0.5)
                length = random.randint(8, 20)
                ex = x + length * math.cos(angle)
                ey = y + length * math.sin(angle)
                
                organic_line((x, y), (ex, ey), random.randint(25, 40), 1, 0.3)
    
    # === EYES (HYPER-REALISTIC) ===
    
    eye_y = face_top + 380
    eye_spacing = 180
    left_eye_x = face_center_x - eye_spacing // 2
    right_eye_x = face_center_x + eye_spacing // 2
    eye_width = 90
    eye_height = 45
    
    def draw_realistic_eye(center_x, eye_y):
        """Draw incredibly realistic eye"""
        # Upper eyelid (darker, multiple strokes)
        for offset in range(-1, 2):
            upper_y = eye_y + offset
            organic_line((center_x - eye_width//2, upper_y), 
                        (center_x, upper_y - eye_height//3), 20, 3, 0.4)
            organic_line((center_x, upper_y - eye_height//3), 
                        (center_x + eye_width//2, upper_y), 20, 3, 0.4)
        
        # Lower eyelid (lighter)
        organic_line((center_x - eye_width//2, eye_y), 
                    (center_x, eye_y + eye_height//3), 50, 2, 0.3)
        organic_line((center_x, eye_y + eye_height//3), 
                    (center_x + eye_width//2, eye_y), 50, 2, 0.3)
        
        # Iris (detailed)
        iris_radius = 18
        iris_center = (center_x, eye_y)
        
        # Iris outline
        for angle in range(0, 360, 5):
            rad1 = math.radians(angle)
            rad2 = math.radians(angle + 5)
            x1 = center_x + iris_radius * math.cos(rad1)
            y1 = eye_y + iris_radius * math.sin(rad1)
            x2 = center_x + iris_radius * math.cos(rad2)
            y2 = eye_y + iris_radius * math.sin(rad2)
            organic_line((x1, y1), (x2, y2), 25, 2, 0.1)
        
        # Iris radial lines (texture)
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            x1 = center_x + 8 * math.cos(rad)
            y1 = eye_y + 8 * math.sin(rad)
            x2 = center_x + iris_radius * math.cos(rad)
            y2 = eye_y + iris_radius * math.sin(rad)
            organic_line((x1, y1), (x2, y2), 40, 1, 0.2)
        
        # Pupil (dark center with gradient)
        pupil_radius = 8
        stipple_gradient((center_x, eye_y), pupil_radius, 15, 150)
        
        # Light reflection (bright spot)
        reflect_x, reflect_y = center_x + 5, eye_y - 5
        for r in range(4, 0, -1):
            gray = 200 - r * 30
            draw.ellipse([reflect_x - r, reflect_y - r, reflect_x + r, reflect_y + r],
                        fill=(gray, gray, gray))
        
        # Eyelashes (individual strokes)
        for i in range(15):
            # Upper lashes
            lash_x = center_x - eye_width//2 + i * (eye_width / 15)
            lash_angle = math.radians(-70 + i * 10)
            lash_length = random.randint(10, 18)
            lash_ex = lash_x + lash_length * math.cos(lash_angle)
            lash_ey = eye_y - eye_height//3 + lash_length * math.sin(lash_angle)
            organic_line((lash_x, eye_y - eye_height//3), (lash_ex, lash_ey), 20, 1, 0.2)
        
        # Eyebrow (individual hairs)
        brow_y = eye_y - 50
        for i in range(25):
            hair_x = center_x - 50 + i * 4
            hair_angle = math.radians(-10 + random.randint(-15, 15))
            hair_length = random.randint(8, 15)
            hair_ex = hair_x + hair_length * math.cos(hair_angle)
            hair_ey = brow_y + hair_length * math.sin(hair_angle)
            organic_line((hair_x, brow_y), (hair_ex, hair_ey), 30, 2, 0.3)
        
        # Eye socket shading
        stipple_gradient((center_x, eye_y - 30), 35, 60, 80)
    
    # Draw both eyes
    draw_realistic_eye(left_eye_x, eye_y)
    draw_realistic_eye(right_eye_x, eye_y)
    
    # === NOSE (ANATOMICALLY ACCURATE) ===
    
    nose_top_y = eye_y + 80
    nose_bottom_y = nose_top_y + 200
    
    # Nose bridge (from between eyes)
    organic_line((face_center_x - 8, eye_y + 50), (face_center_x - 12, nose_bottom_y - 40), 35, 2, 0.8)
    organic_line((face_center_x + 8, eye_y + 50), (face_center_x + 12, nose_bottom_y - 40), 35, 2, 0.8)
    
    # Nose tip (rounded, organic)
    tip_points = [
        (face_center_x - 25, nose_bottom_y - 20),
        (face_center_x - 30, nose_bottom_y),
        (face_center_x - 20, nose_bottom_y + 15),
        (face_center_x, nose_bottom_y + 20),
        (face_center_x + 20, nose_bottom_y + 15),
        (face_center_x + 30, nose_bottom_y),
        (face_center_x + 25, nose_bottom_y - 20)
    ]
    for i in range(len(tip_points) - 1):
        organic_line(tip_points[i], tip_points[i+1], 30, 2, 0.5)
    
    # Nostrils (deep shading)
    stipple_gradient((face_center_x - 18, nose_bottom_y + 5), 10, 20, 100)
    stipple_gradient((face_center_x + 18, nose_bottom_y + 5), 10, 20, 100)
    
    # Nostril definition
    for angle in range(180, 360, 10):
        rad = math.radians(angle)
        r = 8
        x1 = face_center_x - 18 + r * math.cos(rad)
        y1 = nose_bottom_y + 5 + r * 0.7 * math.sin(rad)
        x2 = face_center_x - 18 + (r-2) * math.cos(rad + 0.2)
        y2 = nose_bottom_y + 5 + (r-2) * 0.7 * math.sin(rad + 0.2)
        organic_line((x1, y1), (x2, y2), 25, 2, 0.1)
    
    for angle in range(180, 360, 10):
        rad = math.radians(angle)
        r = 8
        x1 = face_center_x + 18 + r * math.cos(rad)
        y1 = nose_bottom_y + 5 + r * 0.7 * math.sin(rad)
        x2 = face_center_x + 18 + (r-2) * math.cos(rad + 0.2)
        y2 = nose_bottom_y + 5 + (r-2) * 0.7 * math.sin(rad + 0.2)
        organic_line((x1, y1), (x2, y2), 25, 2, 0.1)
    
    # Nose side shading
    advanced_crosshatch([face_center_x - 35, nose_bottom_y - 30, face_center_x - 15, nose_bottom_y + 10], 2, 65)
    advanced_crosshatch([face_center_x + 15, nose_bottom_y - 30, face_center_x + 35, nose_bottom_y + 10], 2, 65)
    
    # === MOUTH (REALISTIC LIPS) ===
    
    mouth_y = nose_bottom_y + 120
    mouth_width = 150
    
    # Upper lip with cupid's bow
    upper_lip_points = [
        (face_center_x - mouth_width//2, mouth_y),
        (face_center_x - mouth_width//4, mouth_y - 8),
        (face_center_x - 15, mouth_y - 4),
        (face_center_x, mouth_y - 10),
        (face_center_x + 15, mouth_y - 4),
        (face_center_x + mouth_width//4, mouth_y - 8),
        (face_center_x + mouth_width//2, mouth_y)
    ]
    for i in range(len(upper_lip_points) - 1):
        organic_line(upper_lip_points[i], upper_lip_points[i+1], 25, 3, 0.6)
    
    # Lower lip
    lower_lip_points = [
        (face_center_x - mouth_width//2, mouth_y),
        (face_center_x - mouth_width//3, mouth_y + 20),
        (face_center_x, mouth_y + 25),
        (face_center_x + mouth_width//3, mouth_y + 20),
        (face_center_x + mouth_width//2, mouth_y)
    ]
    for i in range(len(lower_lip_points) - 1):
        organic_line(lower_lip_points[i], lower_lip_points[i+1], 25, 3, 0.6)
    
    # Lip line (center separation)
    organic_line((face_center_x - mouth_width//2, mouth_y), 
                (face_center_x + mouth_width//2, mouth_y), 20, 2, 0.4)
    
    # Lip shading (volume)
    advanced_crosshatch([face_center_x - mouth_width//2 + 10, mouth_y + 5, 
                        face_center_x + mouth_width//2 - 10, mouth_y + 22], 2, 70)
    
    # Philtrum (groove above upper lip)
    organic_line((face_center_x - 5, nose_bottom_y + 30), 
                (face_center_x - 3, mouth_y - 10), 50, 1, 0.3)
    organic_line((face_center_x + 5, nose_bottom_y + 30), 
                (face_center_x + 3, mouth_y - 10), 50, 1, 0.3)
    
    # === FACIAL HAIR ===
    
    if has_beard:
        # Full beard with individual hair strokes
        for i in range(300):
            x = face_center_x + random.randint(-100, 100)
            y = mouth_y + 40 + random.randint(0, face_bottom - mouth_y - 40)
            
            angle = random.uniform(-0.3, 0.3)
            length = random.randint(6, 14)
            ex = x + length * math.cos(angle + math.pi/2)
            ey = y + length * math.sin(angle + math.pi/2)
            
            organic_line((x, y), (ex, ey), random.randint(30, 45), 1, 0.2)
    
    # === EARS ===
    
    ear_y = eye_y + 50
    ear_height = 100
    
    # Left ear
    outer_ear_left = [
        (face_left - 20, ear_y),
        (face_left - 35, ear_y + ear_height//3),
        (face_left - 30, ear_y + 2*ear_height//3),
        (face_left - 15, ear_y + ear_height)
    ]
    for i in range(len(outer_ear_left) - 1):
        organic_line(outer_ear_left[i], outer_ear_left[i+1], 35, 2, 0.5)
    
    # Inner ear detail
    organic_line((face_left - 25, ear_y + 20), (face_left - 10, ear_y + 50), 40, 1, 0.4)
    stipple_gradient((face_left - 20, ear_y + 50), 15, 50, 50)
    
    # Right ear
    outer_ear_right = [
        (face_right + 20, ear_y),
        (face_right + 35, ear_y + ear_height//3),
        (face_right + 30, ear_y + 2*ear_height//3),
        (face_right + 15, ear_y + ear_height)
    ]
    for i in range(len(outer_ear_right) - 1):
        organic_line(outer_ear_right[i], outer_ear_right[i+1], 35, 2, 0.5)
    
    organic_line((face_right + 25, ear_y + 20), (face_right + 10, ear_y + 50), 40, 1, 0.4)
    stipple_gradient((face_right + 20, ear_y + 50), 15, 50, 50)
    
    # === NECK AND SHOULDERS ===
    
    neck_width = 140
    organic_line((face_center_x - neck_width//2, face_bottom), 
                (face_center_x - neck_width//2 - 20, height - 100), 30, 3, 1.0)
    organic_line((face_center_x + neck_width//2, face_bottom), 
                (face_center_x + neck_width//2 + 20, height - 100), 30, 3, 1.0)
    
    # Adam's apple (if male)
    if is_male:
        organic_line((face_center_x - 15, face_bottom + 100), 
                    (face_center_x + 15, face_bottom + 100), 35, 2, 0.3)
    
    # === GLASSES ===
    
    if has_glasses:
        # Left lens (detailed frame)
        for offset in range(-1, 2):
            for angle in range(0, 360, 3):
                rad1 = math.radians(angle)
                rad2 = math.radians(angle + 3)
                rx, ry = 45, 30
                x1 = left_eye_x + rx * math.cos(rad1) + offset
                y1 = eye_y + ry * math.sin(rad1)
                x2 = left_eye_x + rx * math.cos(rad2) + offset
                y2 = eye_y + ry * math.sin(rad2)
                organic_line((x1, y1), (x2, y2), 25, 2, 0.1)
        
        # Right lens
        for offset in range(-1, 2):
            for angle in range(0, 360, 3):
                rad1 = math.radians(angle)
                rad2 = math.radians(angle + 3)
                rx, ry = 45, 30
                x1 = right_eye_x + rx * math.cos(rad1) + offset
                y1 = eye_y + ry * math.sin(rad1)
                x2 = right_eye_x + rx * math.cos(rad2) + offset
                y2 = eye_y + ry * math.sin(rad2)
                organic_line((x1, y1), (x2, y2), 25, 2, 0.1)
        
        # Bridge
        organic_line((left_eye_x + 45, eye_y), (right_eye_x - 45, eye_y), 25, 3, 0.2)
        
        # Temple arms
        organic_line((left_eye_x - 45, eye_y), (face_left - 15, eye_y + 10), 25, 2, 0.3)
        organic_line((right_eye_x + 45, eye_y), (face_right + 15, eye_y + 10), 25, 2, 0.3)
    
    # === AGE DETAILS ===
    
    if age > 35:
        # Forehead lines
        for i in range(3):
            y = face_top + 120 + i * 25
            organic_line((face_center_x - 80, y), (face_center_x + 80, y), 55, 1, 0.4)
        
        # Crow's feet
        for i in range(4):
            angle = math.radians(30 + i * 15)
            length = 20 + i * 5
            organic_line((left_eye_x + 45, eye_y), 
                        (left_eye_x + 45 + length * math.cos(angle), 
                         eye_y + length * math.sin(angle)), 50, 1, 0.3)
            organic_line((right_eye_x - 45, eye_y), 
                        (right_eye_x - 45 - length * math.cos(angle), 
                         eye_y + length * math.sin(angle)), 50, 1, 0.3)
        
        # Nasolabial folds
        organic_line((face_center_x - 30, nose_bottom_y + 20), 
                    (face_center_x - 70, mouth_y + 15), 40, 2, 0.6)
        organic_line((face_center_x + 30, nose_bottom_y + 20), 
                    (face_center_x + 70, mouth_y + 15), 40, 2, 0.6)
    
    # === PROFESSIONAL FINISHING ===
    
    # 1. Graphite smudging simulation
    smudge = Image.new('L', img.size, 255)
    smudge_draw = ImageDraw.Draw(smudge)
    for _ in range(150):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(15, 60)
        smudge_draw.ellipse([x-r, y-r, x+r, y+r], fill=random.randint(235, 250))
    smudge = smudge.filter(ImageFilter.GaussianBlur(radius=25))
    img = ImageChops.multiply(img, smudge.convert('RGB'))
    
    # 2. Paper grain texture
    grain = Image.new('L', img.size, 255)
    grain_pixels = grain.load()
    for _ in range(3000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        grain_pixels[x, y] = random.randint(240, 255)
    grain = grain.filter(ImageFilter.GaussianBlur(radius=0.3))
    img = ImageChops.multiply(img, grain.convert('RGB'))
    
    # 3. Subtle pencil blur
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # 4. Contrast enhancement
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    # 5. Slight sharpening for detail
    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=2))
    
    # 6. Vignette effect
    vignette = Image.new('L', img.size, 255)
    vignette_draw = ImageDraw.Draw(vignette)
    for i in range(150):
        intensity = int(255 - i * 0.8)
        vignette_draw.rectangle([i, i, width - i, height - i], outline=intensity)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=60))
    img = ImageChops.multiply(img, vignette.convert('RGB'))
    
    return img
