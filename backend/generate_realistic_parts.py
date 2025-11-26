"""
Generate Realistic Pencil Sketch Facial Components
Creates professional-looking facial parts for drag-and-drop composition
"""
import cv2
import numpy as np
from PIL import Image
import os

def create_realistic_eye(eye_type=1, width=150, height=100):
    """Generate realistic eye sketches"""
    img = np.ones((height, width, 3), dtype=np.uint8) * 250
    
    center_x = width // 2
    center_y = height // 2
    
    if eye_type == 1:  # Normal open eye
        cv2.ellipse(img, (center_x, center_y), (50, 25), 0, 180, 360, (30, 30, 30), 2)
        cv2.ellipse(img, (center_x, center_y), (50, 20), 0, 0, 180, (30, 30, 30), 1)
        cv2.circle(img, (center_x, center_y), 18, (50, 50, 50), 2)
        cv2.circle(img, (center_x, center_y), 8, (0, 0, 0), -1)
        cv2.circle(img, (center_x - 5, center_y - 5), 3, (255, 255, 255), -1)
        for i in range(-40, 45, 8):
            x = center_x + i
            y_start = center_y - int(np.sqrt(max(0, 2500 - i*i)) * 0.5)
            cv2.line(img, (x, y_start), (x + np.random.randint(-2, 3), y_start - 8), (20, 20, 20), 1)
    elif eye_type == 2:  # Almond shaped
        cv2.ellipse(img, (center_x, center_y), (55, 28), 0, 180, 360, (30, 30, 30), 2)
        cv2.ellipse(img, (center_x, center_y), (55, 22), 0, 0, 180, (30, 30, 30), 1)
        cv2.circle(img, (center_x + 5, center_y), 16, (50, 50, 50), 2)
        cv2.circle(img, (center_x + 5, center_y), 7, (0, 0, 0), -1)
    elif eye_type == 3:  # Round eye
        cv2.ellipse(img, (center_x, center_y), (45, 30), 0, 180, 360, (30, 30, 30), 2)
        cv2.ellipse(img, (center_x, center_y), (45, 25), 0, 0, 180, (30, 30, 30), 1)
        cv2.circle(img, (center_x, center_y), 20, (50, 50, 50), 2)
        cv2.circle(img, (center_x, center_y), 9, (0, 0, 0), -1)
    elif eye_type == 4:  # Narrow eye
        cv2.ellipse(img, (center_x, center_y), (52, 20), 0, 180, 360, (30, 30, 30), 2)
        cv2.ellipse(img, (center_x, center_y), (52, 18), 0, 0, 180, (30, 30, 30), 1)
        cv2.circle(img, (center_x, center_y), 15, (50, 50, 50), 2)
        cv2.circle(img, (center_x, center_y), 6, (0, 0, 0), -1)
    
    eyebrow_y = center_y - 35
    pts = np.array([[center_x - 55, eyebrow_y + 5], [center_x - 20, eyebrow_y], 
                    [center_x + 20, eyebrow_y], [center_x + 55, eyebrow_y + 8]], np.int32)
    cv2.polylines(img, [pts], False, (40, 40, 40), 2)
    
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def create_realistic_nose(nose_type=1, width=120, height=150):
    """Generate realistic nose sketches"""
    img = np.ones((height, width, 3), dtype=np.uint8) * 250
    center_x = width // 2
    center_y = height // 2
    
    if nose_type == 1:  # Straight nose
        cv2.line(img, (center_x - 8, 20), (center_x - 8, center_y + 20), (60, 60, 60), 1)
        cv2.ellipse(img, (center_x, center_y + 25), (20, 15), 0, 0, 180, (50, 50, 50), 2)
        cv2.ellipse(img, (center_x - 15, center_y + 30), (8, 10), 45, 0, 180, (30, 30, 30), 2)
        cv2.ellipse(img, (center_x + 15, center_y + 30), (8, 10), 135, 0, 180, (30, 30, 30), 2)
    elif nose_type == 2:  # Button nose
        cv2.ellipse(img, (center_x, center_y + 20), (18, 18), 0, 0, 180, (50, 50, 50), 2)
        cv2.ellipse(img, (center_x - 12, center_y + 25), (6, 8), 45, 0, 180, (30, 30, 30), 2)
        cv2.ellipse(img, (center_x + 12, center_y + 25), (6, 8), 135, 0, 180, (30, 30, 30), 2)
    elif nose_type == 3:  # Aquiline nose
        pts = np.array([[center_x - 10, 20], [center_x - 12, center_y], 
                       [center_x - 8, center_y + 20]], np.int32)
        cv2.polylines(img, [pts], False, (60, 60, 60), 2)
        cv2.ellipse(img, (center_x, center_y + 25), (22, 16), 0, 0, 180, (50, 50, 50), 2)
        cv2.ellipse(img, (center_x - 16, center_y + 32), (9, 11), 45, 0, 180, (30, 30, 30), 2)
        cv2.ellipse(img, (center_x + 16, center_y + 32), (9, 11), 135, 0, 180, (30, 30, 30), 2)
    elif nose_type == 4:  # Wide nose
        cv2.line(img, (center_x - 12, 25), (center_x - 10, center_y + 20), (60, 60, 60), 2)
        cv2.ellipse(img, (center_x, center_y + 25), (25, 15), 0, 0, 180, (50, 50, 50), 2)
        cv2.ellipse(img, (center_x - 18, center_y + 30), (10, 12), 45, 0, 180, (30, 30, 30), 2)
        cv2.ellipse(img, (center_x + 18, center_y + 30), (10, 12), 135, 0, 180, (30, 30, 30), 2)
    
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def create_realistic_mouth(mouth_type=1, width=180, height=100):
    """Generate realistic mouth sketches"""
    img = np.ones((height, width, 3), dtype=np.uint8) * 250
    center_x = width // 2
    center_y = height // 2
    
    if mouth_type == 1:  # Neutral smile
        pts_upper = np.array([[center_x - 50, center_y], [center_x - 15, center_y - 8],
                              [center_x, center_y - 5], [center_x + 15, center_y - 8],
                              [center_x + 50, center_y]], np.int32)
        cv2.polylines(img, [pts_upper], False, (40, 40, 40), 2)
        cv2.ellipse(img, (center_x, center_y + 12), (50, 15), 0, 0, 180, (40, 40, 40), 2)
    elif mouth_type == 2:  # Slight smile
        pts_upper = np.array([[center_x - 55, center_y - 5], [center_x - 18, center_y - 10],
                              [center_x, center_y - 8], [center_x + 18, center_y - 10],
                              [center_x + 55, center_y - 5]], np.int32)
        cv2.polylines(img, [pts_upper], False, (40, 40, 40), 2)
        cv2.ellipse(img, (center_x, center_y + 10), (53, 18), 0, 0, 180, (40, 40, 40), 2)
    elif mouth_type == 3:  # Full lips
        pts_upper = np.array([[center_x - 52, center_y], [center_x - 20, center_y - 12],
                              [center_x, center_y - 10], [center_x + 20, center_y - 12],
                              [center_x + 52, center_y]], np.int32)
        cv2.polylines(img, [pts_upper], False, (40, 40, 40), 2)
        cv2.ellipse(img, (center_x, center_y + 15), (52, 20), 0, 0, 180, (40, 40, 40), 2)
    elif mouth_type == 4:  # Thin lips
        cv2.ellipse(img, (center_x, center_y), (48, 5), 0, 180, 360, (40, 40, 40), 2)
        cv2.ellipse(img, (center_x, center_y + 8), (48, 8), 0, 0, 180, (40, 40, 40), 2)
    
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def create_realistic_hair(hair_type=1, width=200, height=250):
    """Generate realistic hair sketches"""
    img = np.ones((height, width, 3), dtype=np.uint8) * 250
    center_x = width // 2
    
    if hair_type == 1:  # Long straight hair
        for i in range(20, width - 20, 15):
            for j in range(5):
                pts = [[i + np.random.randint(-3, 4), y] for y in range(10, height - 20, 30)]
                cv2.polylines(img, [np.array(pts, np.int32)], False, (60 + j * 10, 60 + j * 10, 60 + j * 10), 1)
    elif hair_type == 2:  # Short hair
        cv2.ellipse(img, (center_x, 80), (90, 70), 0, 180, 360, (50, 50, 50), 2)
        for angle in range(180, 360, 10):
            rad = np.radians(angle)
            x_start = int(center_x + 90 * np.cos(rad))
            y_start = int(80 + 70 * np.sin(rad))
            length = np.random.randint(15, 30)
            x_end = int(x_start + length * np.cos(rad - 0.3))
            y_end = int(y_start + length * np.sin(rad - 0.3))
            cv2.line(img, (x_start, y_start), (x_end, y_end), (60, 60, 60), 1)
    elif hair_type == 3:  # Wavy hair
        for i in range(15, width - 15, 12):
            amplitude = np.random.randint(8, 15)
            pts = [[i + int(amplitude * np.sin(0.1 * y)), y] for y in range(10, height - 20, 8)]
            cv2.polylines(img, [np.array(pts, np.int32)], False, (60, 60, 60), 1)
    elif hair_type == 4:  # Curly hair
        for i in range(20, width - 20, 20):
            for j in range(10, height - 30, 40):
                cv2.ellipse(img, (i + np.random.randint(-5, 6), j), (np.random.randint(15, 25), np.random.randint(15, 25)), 
                           0, np.random.randint(0, 180), np.random.randint(180, 450), (60, 60, 60), 1)
    
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def create_realistic_face(face_type=1, width=180, height=220):
    """Generate realistic face shape outlines"""
    img = np.ones((height, width, 3), dtype=np.uint8) * 250
    center_x = width // 2
    center_y = height // 2
    
    if face_type == 1:  # Oval face
        cv2.ellipse(img, (center_x, center_y), (70, 100), 0, 0, 360, (60, 60, 60), 2)
    elif face_type == 2:  # Round face
        cv2.circle(img, (center_x, center_y), 85, (60, 60, 60), 2)
    elif face_type == 3:  # Square face
        pts = np.array([[center_x - 70, center_y - 80], [center_x + 70, center_y - 80],
                       [center_x + 70, center_y + 70], [center_x + 50, center_y + 95],
                       [center_x, center_y + 100], [center_x - 50, center_y + 95],
                       [center_x - 70, center_y + 70]], np.int32)
        cv2.polylines(img, [pts], True, (60, 60, 60), 2)
    elif face_type == 4:  # Heart-shaped face
        pts = np.array([[center_x, center_y - 95], [center_x - 75, center_y - 20],
                       [center_x - 60, center_y + 40], [center_x, center_y + 100],
                       [center_x + 60, center_y + 40], [center_x + 75, center_y - 20]], np.int32)
        cv2.polylines(img, [pts], True, (60, 60, 60), 2)
    
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def generate_all_parts():
    """Generate all facial components"""
    output_dir = "../frontend/public/assets/face-parts"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating realistic facial component sketches...")
    
    for i in range(1, 5):
        cv2.imwrite(f"{output_dir}/eye{i}.png", create_realistic_eye(i))
        print(f"✓ Generated eye{i}.png")
    
    for i in range(1, 5):
        cv2.imwrite(f"{output_dir}/nose{i}.png", create_realistic_nose(i))
        print(f"✓ Generated nose{i}.png")
    
    for i in range(1, 5):
        cv2.imwrite(f"{output_dir}/mouth{i}.png", create_realistic_mouth(i))
        print(f"✓ Generated mouth{i}.png")
    
    for i in range(1, 5):
        cv2.imwrite(f"{output_dir}/hair{i}.png", create_realistic_hair(i))
        print(f"✓ Generated hair{i}.png")
    
    for i in range(1, 5):
        cv2.imwrite(f"{output_dir}/face{i}.png", create_realistic_face(i))
        print(f"✓ Generated face{i}.png")
    
    print(f"\n✅ All 20 realistic facial components generated in {output_dir}")

if __name__ == "__main__":
    generate_all_parts()
