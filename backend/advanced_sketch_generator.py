"""
Advanced Realistic Sketch Generator
Ultra-realistic forensic sketch with hand-drawn quality
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

def generate_realistic_sketch(prompt):
    """Generate ultra-realistic hand-drawn forensic sketch"""
    
    # Canvas setup - larger for detail
    width, height = 1000, 1200
    img = Image.new('RGB', (width, height), color='#FAF8F3')
    draw = ImageDraw.Draw(img)
    
    # Parse features from prompt
    prompt_lower = prompt.lower()
    is_male = 'male' in prompt_lower or 'man' in prompt_lower
    is_female = 'female' in prompt_lower or 'woman' in prompt_lower
    has_beard = 'beard' in prompt_lower
    has_mustache = 'mustache' in prompt_lower or 'moustache' in prompt_lower
    has_glasses = 'glasses' in prompt_lower or 'spectacles' in prompt_lower
    
    # Hair type
    is_bald = 'bald' in prompt_lower
    is_long_hair = 'long hair' in prompt_lower
    is_short_hair = 'short hair' in prompt_lower or (is_male and not is_long_hair and not is_bald)
    is_curly = 'curly' in prompt_lower
    
    # Age estimation
    age = 30
    if '20s' in prompt_lower or 'young' in prompt_lower:
        age = 25
    elif '40s' in prompt_lower or 'middle' in prompt_lower:
        age = 40
    elif '50s' in prompt_lower or '60s' in prompt_lower or 'old' in prompt_lower:
        age = 55
    
    # Helper functions for realistic drawing
    def draw_pencil_line(x1, y1, x2, y2, darkness=60, thickness=1, roughness=0.3):
        """Draw a sketchy, hand-drawn looking line with natural imperfections"""
        steps = int(math.sqrt((x2-x1)**2 + (y2-y1)**2) / 2)
        if steps < 2:
            steps = 2
        
        points = []
        for i in range(steps + 1):
            t = i / steps
            x = x1 + (x2 - x1) * t + random.uniform(-roughness, roughness)
            y = y1 + (y2 - y1) * t + random.uniform(-roughness, roughness)
            points.append((x, y))
        
        for i in range(len(points) - 1):
            gray = darkness + random.randint(-10, 10)
            gray = max(20, min(100, gray))
            draw.line([points[i], points[i+1]], fill=(gray, gray, gray), width=thickness)
    
    def draw_pencil_curve(points, darkness=60, thickness=1):
        """Draw a curved line through points"""
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            draw_pencil_line(x1, y1, x2, y2, darkness, thickness, roughness=0.5)
    
    def cross_hatch_area(x, y, w, h, density=5, angle1=45, angle2=-45, darkness=80):
        """Create cross-hatching for shading (professional technique)"""
        # First direction
        for i in range(density):
            offset = i * (h / density)
            x1 = x
            y1 = y + offset
            x2 = x + w
            y2 = y + offset
            
            # Rotate around center
            cx, cy = x + w/2, y + h/2
            angle_rad = math.radians(angle1)
            x1r = cx + (x1 - cx) * math.cos(angle_rad) - (y1 - cy) * math.sin(angle_rad)
            y1r = cy + (x1 - cx) * math.sin(angle_rad) + (y1 - cy) * math.cos(angle_rad)
            x2r = cx + (x2 - cx) * math.cos(angle_rad) - (y2 - cy) * math.sin(angle_rad)
            y2r = cy + (x2 - cx) * math.sin(angle_rad) + (y2 - cy) * math.cos(angle_rad)
            
            draw_pencil_line(x1r, y1r, x2r, y2r, darkness + random.randint(-5, 5), 1, 0.5)
        
        # Second direction (cross)
        for i in range(density):
            offset = i * (h / density)
            x1 = x
            y1 = y + offset
            x2 = x + w
            y2 = y + offset
            
            cx, cy = x + w/2, y + h/2
            angle_rad = math.radians(angle2)
            x1r = cx + (x1 - cx) * math.cos(angle_rad) - (y1 - cy) * math.sin(angle_rad)
            y1r = cy + (x1 - cx) * math.sin(angle_rad) + (y1 - cy) * math.cos(angle_rad)
            x2r = cx + (x2 - cx) * math.cos(angle_rad) - (y2 - cy) * math.sin(angle_rad)
            y2r = cy + (x2 - cx) * math.sin(angle_rad) + (y2 - cy) * math.cos(angle_rad)
            
            draw_pencil_line(x1r, y1r, x2r, y2r, darkness + random.randint(-5, 5), 1, 0.5)
    
    def stipple_shade(x, y, w, h, density=50, darkness=70):
        """Create stippling effect for soft shading"""
        for _ in range(density):
            px = x + random.uniform(0, w)
            py = y + random.uniform(0, h)
            size = random.randint(1, 2)
            gray = darkness + random.randint(-20, 20)
            draw.ellipse([px, py, px+size, py+size], fill=(gray, gray, gray))
    
    # === FACE STRUCTURE ===
    face_center_x = width // 2
    face_top = 150
    face_bottom = 900
    face_width = 280
    face_left = face_center_x - face_width // 2
    face_right = face_center_x + face_width // 2
    
    # Draw face outline with organic, hand-drawn feel
    # Top of head to chin
    face_points = []
    for i in range(30):
        angle = (i / 30) * math.pi  # Half circle
        x = face_center_x + math.sin(angle) * (face_width/2) + random.uniform(-1, 1)
        y = face_top + (face_bottom - face_top) * (i / 30) + random.uniform(-2, 2)
        if i > 20:  # Jaw area - make more angular
            y = face_bottom - (30 - i) * 15
        face_points.append((x, y))
    
    # Draw face contour with sketchy lines
    for i in range(len(face_points) - 1):
        x1, y1 = face_points[i]
        x2, y2 = face_points[i + 1]
        draw_pencil_line(x1, y1, x2, y2, darkness=45, thickness=2, roughness=0.8)
    
    # Mirror for other side
    for i in range(len(face_points) - 1, -1, -1):
        x, y = face_points[i]
        x_mirror = face_center_x - (x - face_center_x)
        draw_pencil_line(x_mirror, y, x_mirror, y + 1, darkness=45, thickness=2, roughness=0.8)
    
    # === EYES (ultra-realistic) ===
    eye_y = face_top + 280
    eye_spacing = 120
    left_eye_x = face_center_x - eye_spacing
    right_eye_x = face_center_x + eye_spacing
    eye_width = 55
    eye_height = 32
    
    def draw_realistic_eye(center_x, center_y):
        """Draw a highly detailed realistic eye"""
        # Upper eyelid - bold organic curve
        upper_lid_points = []
        for i in range(15):
            t = i / 14
            x = center_x - eye_width/2 + eye_width * t
            y_curve = -math.sin(t * math.pi) * 8
            y = center_y - eye_height/2 + y_curve + random.uniform(-0.3, 0.3)
            upper_lid_points.append((x, y))
        
        for i in range(len(upper_lid_points) - 1):
            x1, y1 = upper_lid_points[i]
            x2, y2 = upper_lid_points[i+1]
            draw_pencil_line(x1, y1, x2, y2, darkness=30, thickness=3, roughness=0.2)
        
        # Lower eyelid - softer line
        lower_lid_points = []
        for i in range(15):
            t = i / 14
            x = center_x - eye_width/2 + eye_width * t
            y_curve = math.sin(t * math.pi) * 4
            y = center_y + eye_height/2 + y_curve + random.uniform(-0.3, 0.3)
            lower_lid_points.append((x, y))
        
        for i in range(len(lower_lid_points) - 1):
            x1, y1 = lower_lid_points[i]
            x2, y2 = lower_lid_points[i+1]
            draw_pencil_line(x1, y1, x2, y2, darkness=60, thickness=2, roughness=0.2)
        
        # Iris - detailed with texture
        iris_radius = 18
        iris_x = center_x
        iris_y = center_y
        
        # Outer iris circle
        iris_points = []
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            x = iris_x + math.cos(rad) * iris_radius + random.uniform(-0.3, 0.3)
            y = iris_y + math.sin(rad) * iris_radius + random.uniform(-0.3, 0.3)
            iris_points.append((x, y))
        iris_points.append(iris_points[0])
        
        for i in range(len(iris_points) - 1):
            draw_pencil_line(iris_points[i][0], iris_points[i][1],
                           iris_points[i+1][0], iris_points[i+1][1],
                           darkness=40, thickness=2, roughness=0.1)
        
        # Iris texture - radial lines
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            x1 = iris_x + math.cos(rad) * 5
            y1 = iris_y + math.sin(rad) * 5
            x2 = iris_x + math.cos(rad) * (iris_radius - 2)
            y2 = iris_y + math.sin(rad) * (iris_radius - 2)
            draw_pencil_line(x1, y1, x2, y2, darkness=65, thickness=1, roughness=0.3)
        
        # Pupil - dark center
        pupil_radius = 7
        for r in range(pupil_radius, 0, -1):
            gray = 20 + (pupil_radius - r) * 5
            draw.ellipse([iris_x-r, iris_y-r, iris_x+r, iris_y+r],
                        fill=(gray, gray, gray))
        
        # Light reflection - makes eye "alive"
        highlight_x = iris_x + 4
        highlight_y = iris_y - 5
        draw.ellipse([highlight_x-3, highlight_y-3, highlight_x+3, highlight_y+3],
                    fill=(220, 220, 220))
        draw.ellipse([highlight_x+6, highlight_y+2, highlight_x+8, highlight_y+4],
                    fill=(200, 200, 200))
        
        # Eyelashes - individual strokes
        for i in range(12):
            lash_x = center_x - eye_width/2 + (eye_width * i / 12)
            lash_y = center_y - eye_height/2
            lash_length = random.randint(8, 14)
            lash_angle = random.uniform(-20, -60)
            rad = math.radians(lash_angle)
            end_x = lash_x + math.cos(rad) * lash_length
            end_y = lash_y + math.sin(rad) * lash_length
            draw_pencil_line(lash_x, lash_y, end_x, end_y, darkness=25, thickness=2, roughness=0.1)
        
        # Eyebrow - many individual hair strokes
        brow_y = center_y - 35
        for i in range(25):
            hair_x = center_x - 35 + i * 3
            hair_y = brow_y + math.sin(i * 0.3) * 3
            hair_length = random.randint(8, 12)
            hair_angle = random.uniform(-70, -110)
            rad = math.radians(hair_angle)
            end_x = hair_x + math.cos(rad) * hair_length
            end_y = hair_y + math.sin(rad) * hair_length
            draw_pencil_line(hair_x, hair_y, end_x, end_y, 
                           darkness=45 + random.randint(-10, 10),
                           thickness=2, roughness=0.2)
        
        # Eye shadow/depth
        cross_hatch_area(center_x - eye_width/2 - 5, center_y - 8,
                        15, 16, density=4, darkness=110)
    
    # Draw both eyes
    draw_realistic_eye(left_eye_x, eye_y)
    draw_realistic_eye(right_eye_x, eye_y)
    
    # === NOSE (ultra-realistic with shading) ===
    nose_top_y = eye_y + 45
    nose_bottom_y = nose_top_y + 135
    nose_x = face_center_x
    
    # Bridge from between eyes
    draw_pencil_line(nose_x - 8, nose_top_y, nose_x - 6, nose_bottom_y - 40,
                    darkness=55, thickness=2, roughness=0.5)
    draw_pencil_line(nose_x + 8, nose_top_y, nose_x + 6, nose_bottom_y - 40,
                    darkness=55, thickness=2, roughness=0.5)
    
    # Nose tip - rounded bulb shape
    tip_points = []
    for angle in range(180, 360, 10):
        rad = math.radians(angle)
        x = nose_x + math.cos(rad) * 22
        y = nose_bottom_y - 10 + math.sin(rad) * 12
        tip_points.append((x, y))
    draw_pencil_curve(tip_points, darkness=50, thickness=2)
    
    # Nostrils - deep shading for depth
    def draw_nostril(x, y, is_left=True):
        # Nostril opening
        nostril_points = []
        for angle in range(180, 360, 15):
            rad = math.radians(angle)
            offset = 11 if is_left else 11
            nx = x + math.cos(rad) * offset
            ny = y + math.sin(rad) * 6
            nostril_points.append((nx, ny))
        draw_pencil_curve(nostril_points, darkness=35, thickness=3)
        
        # Dark interior
        stipple_shade(x - 8, y - 3, 16, 8, density=30, darkness=40)
        
        # Wing of nose
        wing_start_x = x - 15 if is_left else x + 15
        draw_pencil_line(wing_start_x, y - 10, x, y + 2,
                        darkness=60, thickness=2, roughness=0.4)
    
    draw_nostril(nose_x - 14, nose_bottom_y, is_left=True)
    draw_nostril(nose_x + 14, nose_bottom_y, is_left=False)
    
    # Nose shading - creates 3D form
    cross_hatch_area(nose_x - 20, nose_bottom_y - 30, 10, 35,
                    density=5, angle1=30, angle2=-30, darkness=95)
    cross_hatch_area(nose_x + 10, nose_bottom_y - 30, 10, 35,
                    density=5, angle1=30, angle2=-30, darkness=95)
    
    # === MOUTH (ultra-realistic lips) ===
    mouth_y = nose_bottom_y + 70
    mouth_width = 110
    
    # Upper lip with detailed cupid's bow
    upper_lip_points = [
        (nose_x - mouth_width/2, mouth_y),
        (nose_x - 35, mouth_y - 2),
        (nose_x - 18, mouth_y - 8),  # Left peak
        (nose_x - 5, mouth_y - 5),   # Dip
        (nose_x, mouth_y - 3),        # Center
        (nose_x + 5, mouth_y - 5),   # Dip
        (nose_x + 18, mouth_y - 8),  # Right peak
        (nose_x + 35, mouth_y - 2),
        (nose_x + mouth_width/2, mouth_y),
    ]
    draw_pencil_curve(upper_lip_points, darkness=40, thickness=3)
    
    # Lower lip - fuller curve
    lower_lip_points = []
    for i in range(20):
        t = i / 19
        x = nose_x - mouth_width/2 + mouth_width * t
        y_curve = math.sin(t * math.pi) * 18
        y = mouth_y + 2 + y_curve
        lower_lip_points.append((x, y))
    draw_pencil_curve(lower_lip_points, darkness=45, thickness=3)
    
    # Lip line (separation between lips)
    lip_line_points = []
    for i in range(20):
        t = i / 19
        x = nose_x - mouth_width/2 + mouth_width * t
        y = mouth_y + random.uniform(-0.5, 0.5)
        lip_line_points.append((x, y))
    draw_pencil_curve(lip_line_points, darkness=30, thickness=2)
    
    # Lip shading for volume
    stipple_shade(nose_x - mouth_width/2, mouth_y + 2, mouth_width, 15,
                 density=60, darkness=85)
    cross_hatch_area(nose_x - 40, mouth_y - 6, 30, 8,
                    density=3, angle1=80, angle2=100, darkness=100)
    cross_hatch_area(nose_x + 10, mouth_y - 6, 30, 8,
                    density=3, angle1=80, angle2=100, darkness=100)
    
    # Philtrum (groove above upper lip)
    draw_pencil_line(nose_x - 4, nose_bottom_y + 15, nose_x - 3, mouth_y - 8,
                    darkness=70, thickness=1, roughness=0.3)
    draw_pencil_line(nose_x + 4, nose_bottom_y + 15, nose_x + 3, mouth_y - 8,
                    darkness=70, thickness=1, roughness=0.3)
    
    # === HAIR ===
    hairline_y = face_top + 50
    
    if not is_bald:
        if is_short_hair or is_male:
            # Short hair - dense individual strokes
            for i in range(200):
                hair_x = face_left - 30 + random.uniform(0, face_width + 60)
                hair_y = hairline_y - 20 + random.uniform(-30, 80)
                length = random.randint(15, 35)
                angle = random.uniform(-90, -70) if hair_x < face_center_x else random.uniform(-110, -90)
                rad = math.radians(angle)
                end_x = hair_x + math.cos(rad) * length
                end_y = hair_y + math.sin(rad) * length
                darkness = random.randint(35, 50)
                draw_pencil_line(hair_x, hair_y, end_x, end_y,
                               darkness=darkness, thickness=2, roughness=0.3)
        
        elif is_long_hair:
            # Long flowing hair
            for i in range(150):
                side = random.choice([-1, 1])
                start_x = face_center_x + side * random.uniform(80, 150)
                start_y = hairline_y + random.uniform(-20, 100)
                length = random.randint(250, 450)
                curve = random.uniform(-30, 30)
                
                # Bezier-like curve
                mid_x = start_x + side * random.uniform(-20, 40)
                mid_y = start_y + length / 2
                end_x = start_x + side * random.uniform(-40, 20)
                end_y = start_y + length
                
                steps = 20
                for s in range(steps):
                    t = s / steps
                    # Quadratic bezier
                    x1 = (1-t)**2 * start_x + 2*(1-t)*t * mid_x + t**2 * end_x
                    y1 = (1-t)**2 * start_y + 2*(1-t)*t * mid_y + t**2 * end_y
                    t2 = (s+1) / steps
                    x2 = (1-t2)**2 * start_x + 2*(1-t2)*t2 * mid_x + t2**2 * end_x
                    y2 = (1-t2)**2 * start_y + 2*(1-t2)*t2 * mid_y + t2**2 * end_y
                    
                    draw_pencil_line(x1, y1, x2, y2, darkness=40 + random.randint(-10, 10),
                                   thickness=2, roughness=0.4)
        
        elif is_curly:
            # Curly hair texture
            for i in range(100):
                start_x = face_left - 20 + random.uniform(0, face_width + 40)
                start_y = hairline_y - 30 + random.uniform(0, 150)
                
                # Create spiral/curl
                for angle in range(0, 720, 30):
                    rad1 = math.radians(angle)
                    rad2 = math.radians(angle + 30)
                    radius = 8 + (angle / 720) * 5
                    x1 = start_x + math.cos(rad1) * radius
                    y1 = start_y + math.sin(rad1) * radius + angle * 0.1
                    x2 = start_x + math.cos(rad2) * radius
                    y2 = start_y + math.sin(rad2) * radius + (angle + 30) * 0.1
                    draw_pencil_line(x1, y1, x2, y2, darkness=45, thickness=2, roughness=0.2)
    
    # === EARS ===
    def draw_ear(x, y, is_left=True):
        """Draw detailed ear"""
        flip = -1 if is_left else 1
        
        # Outer helix
        ear_points = []
        for angle in range(-20, 200, 10):
            rad = math.radians(angle)
            ex = x + flip * math.cos(rad) * 25
            ey = y + math.sin(rad) * 40
            ear_points.append((ex, ey))
        draw_pencil_curve(ear_points, darkness=55, thickness=2)
        
        # Inner structures
        inner_points = []
        for angle in range(20, 160, 10):
            rad = math.radians(angle)
            ex = x + flip * math.cos(rad) * 15
            ey = y + math.sin(rad) * 25
            inner_points.append((ex, ey))
        draw_pencil_curve(inner_points, darkness=60, thickness=1)
        
        # Earlobe
        draw_pencil_line(x + flip * 12, y + 35, x + flip * 8, y + 50,
                        darkness=50, thickness=2, roughness=0.3)
        
        # Shading
        stipple_shade(x - 15 if is_left else x + 5, y - 10, 20, 50,
                     density=25, darkness=90)
    
    draw_ear(face_left - 15, eye_y + 50, is_left=True)
    draw_ear(face_right + 15, eye_y + 50, is_left=False)
    
    # === FACIAL HAIR ===
    if has_beard or has_mustache:
        # Mustache
        if has_mustache or has_beard:
            for i in range(100):
                mx = nose_x - 55 + random.uniform(0, 110)
                my = mouth_y - 20 + random.uniform(0, 15)
                length = random.randint(6, 12)
                angle = random.uniform(-100, -80)
                rad = math.radians(angle)
                end_x = mx + math.cos(rad) * length
                end_y = my + math.sin(rad) * length
                draw_pencil_line(mx, my, end_x, end_y, darkness=40, thickness=1, roughness=0.2)
        
        # Beard
        if has_beard:
            for i in range(250):
                bx = face_left + 40 + random.uniform(0, face_width - 80)
                by = mouth_y + 30 + random.uniform(0, 200)
                length = random.randint(10, 25)
                angle = random.uniform(-95, -85)
                rad = math.radians(angle)
                end_x = bx + math.cos(rad) * length
                end_y = by + math.sin(rad) * length
                darkness = random.randint(38, 52)
                draw_pencil_line(bx, by, end_x, end_y, darkness=darkness,
                               thickness=random.randint(1, 2), roughness=0.3)
    
    # === FACIAL CONTOURS AND SHADING ===
    # Cheekbones
    draw_pencil_line(face_left + 30, eye_y + 90, face_left + 60, eye_y + 120,
                    darkness=65, thickness=1, roughness=0.5)
    draw_pencil_line(face_right - 30, eye_y + 90, face_right - 60, eye_y + 120,
                    darkness=65, thickness=1, roughness=0.5)
    
    # Jawline definition
    cross_hatch_area(face_left - 10, face_bottom - 100, 35, 90,
                    density=4, angle1=45, angle2=-45, darkness=105)
    cross_hatch_area(face_right - 25, face_bottom - 100, 35, 90,
                    density=4, angle1=45, angle2=-45, darkness=105)
    
    # Neck and shoulders
    neck_width = 90
    draw_pencil_line(nose_x - neck_width//2, face_bottom + 5,
                    nose_x - neck_width//2 - 40, height - 100,
                    darkness=50, thickness=3, roughness=0.8)
    draw_pencil_line(nose_x + neck_width//2, face_bottom + 5,
                    nose_x + neck_width//2 + 40, height - 100,
                    darkness=50, thickness=3, roughness=0.8)
    
    # Neck shading
    cross_hatch_area(nose_x - 50, face_bottom + 10, 40, 80,
                    density=5, angle1=90, angle2=0, darkness=100)
    
    # Shoulders
    draw_pencil_line(nose_x - neck_width//2 - 40, height - 100,
                    100, height - 50, darkness=55, thickness=2, roughness=1)
    draw_pencil_line(nose_x + neck_width//2 + 40, height - 100,
                    900, height - 50, darkness=55, thickness=2, roughness=1)
    
    # Clothing suggestion (collar)
    collar_y = height - 120
    for i in range(15):
        cx = nose_x - 80 + i * 12
        cy = collar_y + random.uniform(-3, 3)
        draw_pencil_line(cx, cy, cx + 10, cy + random.uniform(-2, 2),
                        darkness=60, thickness=2, roughness=0.5)
    
    # === GLASSES (if mentioned) ===
    if has_glasses:
        def draw_glasses_lens(cx, cy, w, h):
            # Frame
            frame_points = []
            for angle in range(0, 360, 10):
                rad = math.radians(angle)
                x = cx + math.cos(rad) * w
                y = cy + math.sin(rad) * h
                frame_points.append((x, y))
            frame_points.append(frame_points[0])
            
            for i in range(len(frame_points) - 1):
                draw_pencil_line(frame_points[i][0], frame_points[i][1],
                               frame_points[i+1][0], frame_points[i+1][1],
                               darkness=35, thickness=3, roughness=0.2)
            
            # Lens reflection
            for i in range(3):
                ref_x = cx - 10 + i * 8
                ref_y = cy - 15 + i * 5
                draw_pencil_line(ref_x, ref_y, ref_x + 25, ref_y - 8,
                               darkness=120, thickness=1, roughness=0.1)
        
        draw_glasses_lens(left_eye_x, eye_y, 32, 22)
        draw_glasses_lens(right_eye_x, eye_y, 32, 22)
        
        # Bridge
        draw_pencil_line(left_eye_x + 32, eye_y, right_eye_x - 32, eye_y,
                        darkness=40, thickness=3, roughness=0.3)
        
        # Temple arms
        draw_pencil_line(left_eye_x - 32, eye_y, face_left - 20, eye_y + 10,
                        darkness=45, thickness=2, roughness=0.4)
        draw_pencil_line(right_eye_x + 32, eye_y, face_right + 20, eye_y + 10,
                        darkness=45, thickness=2, roughness=0.4)
    
    # === AGE LINES (for older subjects) ===
    if age > 35:
        # Forehead lines
        for i in range(3):
            y = face_top + 100 + i * 25
            line_points = []
            for x in range(20):
                lx = face_left + 40 + x * 10
                ly = y + random.uniform(-2, 2)
                line_points.append((lx, ly))
            draw_pencil_curve(line_points, darkness=75, thickness=1)
        
        # Crow's feet
        for i in range(4):
            angle = 20 + i * 15
            rad = math.radians(angle)
            draw_pencil_line(left_eye_x - 30, eye_y,
                           left_eye_x - 30 - math.cos(rad) * 20,
                           eye_y + math.sin(rad) * 15,
                           darkness=70, thickness=1, roughness=0.3)
            draw_pencil_line(right_eye_x + 30, eye_y,
                           right_eye_x + 30 + math.cos(rad) * 20,
                           eye_y + math.sin(rad) * 15,
                           darkness=70, thickness=1, roughness=0.3)
        
        # Nasolabial folds
        draw_pencil_curve([(nose_x - 18, nose_bottom_y - 20),
                          (nose_x - 35, mouth_y - 10),
                          (nose_x - 45, mouth_y + 15)],
                         darkness=60, thickness=2)
        draw_pencil_curve([(nose_x + 18, nose_bottom_y - 20),
                          (nose_x + 35, mouth_y - 10),
                          (nose_x + 45, mouth_y + 15)],
                         darkness=60, thickness=2)
    
    # === FINAL TOUCHES ===
    # Add subtle paper texture
    for _ in range(500):
        px = random.randint(0, width)
        py = random.randint(0, height)
        gray = random.randint(240, 250)
        draw.point((px, py), fill=(gray, gray, gray))
    
    # Signature
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, height - 60), "Forensic Sketch", fill=(100, 100, 100), font=font)
    draw.text((50, height - 40), f"Generated from: {prompt[:50]}", fill=(120, 120, 120), font=font)
    
    # === FINAL REALISTIC ENHANCEMENTS ===
    
    # 1. Add graphite smudging effect (very subtle)
    smudge_layer = Image.new('L', img.size, 255)
    smudge_draw = ImageDraw.Draw(smudge_layer)
    
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(10, 40)
        smudge_draw.ellipse([x-size, y-size, x+size, y+size], 
                           fill=random.randint(240, 250))
    
    smudge_layer = smudge_layer.filter(ImageFilter.GaussianBlur(radius=20))
    img = ImageChops.multiply(img, smudge_layer.convert('RGB'))
    
    # 2. Apply subtle Gaussian blur for pencil softness
    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    
    # 3. Add paper grain texture (more pronounced)
    grain = Image.new('L', img.size, 255)
    grain_draw = ImageDraw.Draw(grain)
    for _ in range(2000):  # More grain particles
        x = random.randint(0, width)
        y = random.randint(0, height)
        grain_draw.point((x, y), fill=random.randint(245, 255))
    
    grain = grain.filter(ImageFilter.GaussianBlur(radius=0.2))
    img = ImageChops.multiply(img, grain.convert('RGB'))
    
    # 4. Enhance contrast for professional look
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.15)  # Slight contrast boost
    
    # 5. Add subtle vignette (darker edges like real sketch paper)
    vignette = Image.new('L', img.size, 255)
    vignette_draw = ImageDraw.Draw(vignette)
    for i in range(100):
        intensity = int(255 - (i * 1.5))
        vignette_draw.rectangle([i, i, width-i, height-i], outline=intensity)
    
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=50))
    img = ImageChops.multiply(img, vignette.convert('RGB'))
    
    return img
