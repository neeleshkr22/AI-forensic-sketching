from opencv_sketch_generator import generate_realistic_face_sketch
import os

os.makedirs('uploads', exist_ok=True)

# Change this prompt to control the generated face
prompt = 'Female, 20s, long hair, realistic portrait'

img = generate_realistic_face_sketch(prompt)
output_path = os.path.join('uploads', 'generated_by_model.png')
img.save(output_path)
print('SAVED:', output_path)
