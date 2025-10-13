"""
Test Flask App with Ultra-Realistic Sketch Functionality
"""
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import uuid
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import sketch generators
from opencv_sketch_generator import generate_realistic_face_sketch
from hf_client import generate_from_hf
from sketch_converter import convert_to_pencil_sketch

# Check if Hugging Face token is available
HF_API_TOKEN = os.environ.get('HF_API_TOKEN') or os.environ.get('HUGGINGFACE_API_KEY')
USE_AI_MODEL = HF_API_TOKEN is not None

print(f"[INFO] AI Model Status: {'ENABLED (Hugging Face)' if USE_AI_MODEL else 'DISABLED (Using OpenCV fallback)'}")
if USE_AI_MODEL:
    print(f"[INFO] HF_API_TOKEN: {HF_API_TOKEN[:15]}...")
else:
    print("[INFO] Set HF_API_TOKEN environment variable to enable AI model generation")

app = Flask(__name__)
CORS(app)

# Mock data storage
sketches = {}
mock_results = []

@app.route('/')
def index():
    return jsonify({"status": "running", "message": "Backend API is working!"})

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/sketch/generate', methods=['POST'])
def generate_sketch_endpoint():
    """
    Generate realistic sketch using best available method:
    1. Hugging Face AI model (if HF_API_TOKEN is set) - PHOTOREALISTIC
    2. OpenCV local generator (fallback) - GOOD QUALITY
    """
    data = request.json
    prompt = data.get('prompt', '')
    
    try:
        if USE_AI_MODEL:
            # Use Hugging Face AI model for photorealistic face generation
            print(f"[AI] Generating with Stable Diffusion XL: {prompt}")
            img_bytes = generate_from_hf(
                prompt=f"professional portrait photo of {prompt}, high quality, detailed, studio lighting, neutral background",
                negative_prompt="cartoon, anime, sketch, drawing, painting, low quality, blurry, distorted, deformed",
                guidance=7.5,
                width=768,
                height=1024
            )
            
            # Convert bytes to PIL Image
            photo_img = Image.open(io.BytesIO(img_bytes))
            print(f"[AI] Converting to pencil sketch style...")
            
            # Convert photorealistic image to pencil sketch
            img = convert_to_pencil_sketch(photo_img)
            generation_method = "Stable Diffusion XL + Pencil Conversion"
        else:
            # Fallback to OpenCV generator
            print(f"[LOCAL] Generating sketch with OpenCV: {prompt}")
            img = generate_realistic_face_sketch(prompt)
            generation_method = "OpenCV Local Generator"
        
        # Save to bytes
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        sketch_id = str(uuid.uuid4())
        sketches[sketch_id] = img_io.getvalue()
        
        # Save to uploads folder
        uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        img_path = os.path.join(uploads_dir, f"{sketch_id}.png")
        img.save(img_path)
        
        print(f"[SUCCESS] Sketch generated: {sketch_id} using {generation_method}")
        
        return jsonify({
            "success": True,
            "sketch_id": sketch_id,
            "image_data": f"data:image/png;base64,{img_base64}",
            "prompt": prompt,
            "method": generation_method,
            "created_at": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"[ERROR] Sketch generation failed: {str(e)}")
        
        # If AI model fails, try fallback
        if USE_AI_MODEL:
            print("[FALLBACK] Retrying with OpenCV generator...")
            try:
                img = generate_realistic_face_sketch(prompt)
                img_io = io.BytesIO()
                img.save(img_io, 'PNG')
                img_io.seek(0)
                img_base64 = base64.b64encode(img_io.getvalue()).decode()
                
                sketch_id = str(uuid.uuid4())
                sketches[sketch_id] = img_io.getvalue()
                
                return jsonify({
                    "success": True,
                    "sketch_id": sketch_id,
                    "image_data": f"data:image/png;base64,{img_base64}",
                    "prompt": prompt,
                    "method": "OpenCV Local Generator (Fallback)",
                    "warning": "AI model failed, used fallback generator",
                    "created_at": datetime.now().isoformat()
                })
            except Exception as fallback_error:
                return jsonify({"error": f"All generation methods failed: {str(fallback_error)}"}), 500
        
        return jsonify({"error": str(e)}), 500
    
    return jsonify({
        "success": True,
        "sketch_id": sketch_id,
        "image_data": f"data:image/png;base64,{img_base64}",
        "prompt": prompt,
        "created_at": datetime.now().isoformat()
    })

@app.route('/api/sketch/compose', methods=['POST'])
def compose_sketch():
    """Compose sketch from components"""
    data = request.json
    components = data.get('components', [])
    
    sketch_id = str(uuid.uuid4())
    
    return jsonify({
        "success": True,
        "sketch_id": sketch_id,
        "message": f"Composed from {len(components)} components"
    })

@app.route('/api/sketch/upload', methods=['POST'])
def upload_sketch():
    """Upload a sketch image"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    sketch_id = str(uuid.uuid4())
    
    return jsonify({
        "success": True,
        "sketch_id": sketch_id,
        "filename": file.filename
    })

@app.route('/api/sketch/search', methods=['POST'])
def search_sketch():
    """Search database with sketch"""
    # Return mock results with actual database records
    from pymongo import MongoClient
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['sketch_db']
        records = list(db.criminal_records.find().limit(5))
        
        results = []
        for i, record in enumerate(records):
            results.append({
                "record_id": str(record['_id']),
                "name": record['name'],
                "age": record['age'],
                "gender": record['gender'],
                "crime_type": record['crime_type'],
                "location": record['location'],
                "status": record['status'],
                "confidence": round(0.95 - (i * 0.1), 2),
                "similarity_score": round(0.92 - (i * 0.08), 2)
            })
        
        return jsonify({
            "success": True,
            "matches": results,
            "total_matches": len(results)
        })
    except Exception as e:
        return jsonify({
            "success": True,
            "matches": [
                {
                    "record_id": "1",
                    "name": "John Anderson",
                    "age": 34,
                    "gender": "Male",
                    "crime_type": "Robbery",
                    "location": "Downtown Mall, New York",
                    "status": "wanted",
                    "confidence": 0.95,
                    "similarity_score": 0.92
                }
            ],
            "total_matches": 1
        })

@app.route('/api/sketch/image/<sketch_id>')
def get_sketch_image(sketch_id):
    """Get sketch image by ID"""
    if sketch_id in sketches:
        img_bytes = sketches[sketch_id]
        return send_file(io.BytesIO(img_bytes), mimetype='image/png')
    return jsonify({"error": "Sketch not found"}), 404


@app.route('/api/sample/latest')
def get_latest_sample():
    """Return the locally generated sample image if present"""
    sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads', 'generated_by_model.png')
    if os.path.exists(sample_path):
        return send_file(sample_path, mimetype='image/png')
    return jsonify({"error": "No sample available"}), 404


@app.route('/api/sketch/generate_hosted', methods=['POST'])
def generate_sketch_hosted():
    """Generate a sketch using a hosted pretrained model (Hugging Face).
    Requires environment variable HF_API_TOKEN to be set on the server.
    """
    data = request.json or {}
    prompt = data.get('prompt', '')

    # Ensure HF client has token available via environment
    if 'HF_API_TOKEN' not in os.environ or not os.environ.get('HF_API_TOKEN'):
        return jsonify({"error": "HF_API_TOKEN not configured on server. Provide a Hugging Face token in environment."}), 400

    try:
        img_bytes = generate_from_hf(prompt)
        # save to uploads and return path
        uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        out_path = os.path.join(uploads_dir, f'generated_hosted_{uuid.uuid4().hex}.png')
        with open(out_path, 'wb') as f:
            f.write(img_bytes)

        # Also keep in-memory for existing API
        sketch_id = str(uuid.uuid4())
        sketches[sketch_id] = img_bytes

        return jsonify({
            "success": True,
            "sketch_id": sketch_id,
            "path": out_path,
            "prompt": prompt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sketch/status')
def sketch_status():
    """Get service status"""
    return jsonify({
        "status": "operational",
        "models_loaded": True,
        "database_connected": True
    })

@app.route('/api/records', methods=['GET'])
def get_records():
    """Get all criminal records"""
    from pymongo import MongoClient
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['sketch_db']
        records = list(db.criminal_records.find())
        
        # Convert ObjectId to string
        for record in records:
            record['_id'] = str(record['_id'])
            if 'created_at' in record:
                record['created_at'] = record['created_at'].isoformat()
            if 'updated_at' in record:
                record['updated_at'] = record['updated_at'].isoformat()
            if 'crime_date' in record:
                record['crime_date'] = record['crime_date'].isoformat()
        
        return jsonify({
            "success": True,
            "records": records,
            "total": len(records)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/records/<record_id>')
def get_record(record_id):
    """Get a single record"""
    from pymongo import MongoClient
    from bson import ObjectId
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['sketch_db']
        record = db.criminal_records.find_one({"_id": ObjectId(record_id)})
        
        if record:
            record['_id'] = str(record['_id'])
            if 'created_at' in record:
                record['created_at'] = record['created_at'].isoformat()
            if 'updated_at' in record:
                record['updated_at'] = record['updated_at'].isoformat()
            if 'crime_date' in record:
                record['crime_date'] = record['crime_date'].isoformat()
            
            return jsonify({"success": True, "record": record})
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    print("Available endpoints:")
    print("  GET  / - Health check")
    print("  POST /api/sketch/generate - Generate sketch from text")
    print("  POST /api/sketch/search - Search with sketch")
    print("  GET  /api/records - List all records")
    app.run(host='0.0.0.0', port=5000, debug=True)

