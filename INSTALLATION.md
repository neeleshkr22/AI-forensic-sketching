# AI Criminal Sketch Matching System - Installation Guide

## Prerequisites

Before installation, ensure you have the following installed:

### Required Software
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **MongoDB 6+** - [Download](https://www.mongodb.com/try/download/community)
- **Git** - [Download](https://git-scm.com/downloads)

### Optional (for GPU acceleration)
- **CUDA Toolkit** - [Download](https://developer.nvidia.com/cuda-downloads)
- **NVIDIA GPU with CUDA support**

## Installation Steps

### Method 1: Automated Setup (Windows)

1. **Run Setup Script**
   ```batch
   setup.bat
   ```

   This will:
   - Create Python virtual environment
   - Install all Python dependencies
   - Install Node.js dependencies
   - Create necessary directories
   - Copy environment configuration files

2. **Configure Environment**
   
   Edit `backend\.env`:
   ```env
   MONGODB_URI=mongodb://localhost:27017/sketch_db
   HUGGINGFACE_API_KEY=your_api_key_here
   ```

   Get your Hugging Face API key from: https://huggingface.co/settings/tokens

3. **Start Application**
   ```batch
   start.bat
   ```

   Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

### Method 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create directories**
   ```bash
   mkdir uploads uploads\sketches uploads\records uploads\temp uploads\enhanced
   mkdir models\saved
   mkdir logs
   ```

6. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your settings
   ```

7. **Start backend server**
   ```bash
   python app.py
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   echo VITE_API_URL=http://localhost:5000 > .env
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

#### Database Setup

1. **Start MongoDB**
   ```bash
   mongod --dbpath ./data/db
   ```

2. **Seed sample data (optional)**
   ```bash
   cd backend
   python database/seed.py
   ```

## Configuration

### Backend Configuration (backend/.env)

```env
# Server
FLASK_ENV=development
PORT=5000
HOST=0.0.0.0

# Database
MONGODB_URI=mongodb://localhost:27017/sketch_db
DB_NAME=sketch_db

# Hugging Face API
HUGGINGFACE_API_KEY=your_key_here
HUGGINGFACE_MODEL=stabilityai/stable-diffusion-2-1

# File Upload
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=16777216

# Model Configuration
MODEL_PATH=./models/saved
FEATURE_VECTOR_SIZE=2048
SVM_KERNEL=rbf
SVM_C=1.0
CONFIDENCE_THRESHOLD=0.6

# Image Processing
IMAGE_SIZE=256
SKETCH_SIZE=512
```

### Frontend Configuration (frontend/.env)

```env
VITE_API_URL=http://localhost:5000
```

## First Time Setup

After installation, follow these steps:

1. **Verify Backend**
   - Open http://localhost:5000 in browser
   - Should see: `{"status": "running", "message": "AI Criminal Sketch Matching System API"}`

2. **Verify Frontend**
   - Open http://localhost:5173 in browser
   - Should see the application homepage

3. **Add Test Records**
   - Go to "Records" page
   - Click "Add Record"
   - Fill in details and upload a photo
   - Photos will be automatically processed for feature extraction

4. **Create Test Sketch**
   - Go to "Create Sketch" page
   - Try AI generation with a prompt like: "Male, 30s, short hair, brown eyes"
   - Or upload an existing sketch
   - Click "Search Database" to test matching

## Troubleshooting

### Common Issues

**MongoDB Connection Error**
```
Solution: Ensure MongoDB is running
mongod --dbpath ./data/db
```

**Python Package Errors**
```
Solution: Upgrade pip and reinstall
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Port Already in Use**
```
Solution: Change port in backend/.env
PORT=5001
```

**CORS Errors**
```
Solution: Check CORS_ORIGINS in backend/.env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Hugging Face API Errors**
```
Solution: 
1. Verify API key in backend/.env
2. Check API rate limits
3. Use local model as fallback (set USE_LOCAL_MODEL=true)
```

## Production Deployment

### Backend

1. **Install production server**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Frontend

1. **Build for production**
   ```bash
   npm run build
   ```

2. **Serve build files**
   ```bash
   npm run preview
   # Or use a static file server
   ```

### Database

1. **Use MongoDB Atlas** (cloud) or configure local MongoDB for production
2. **Enable authentication**
3. **Set up regular backups**

## Additional Resources

- **Documentation**: See README.md
- **API Docs**: http://localhost:5000/api-docs (if enabled)
- **Issues**: Report on GitHub repository
- **Support**: Contact development team

## Security Notes

⚠️ **Important for Production**:

1. Change `SECRET_KEY` in backend/.env
2. Use environment-specific `.env` files
3. Enable HTTPS
4. Implement authentication/authorization
5. Regular security audits
6. Keep dependencies updated
7. Use MongoDB authentication
8. Implement rate limiting
9. Sanitize user inputs
10. Regular backups

## Performance Optimization

For better performance:

1. **Use GPU acceleration** (CUDA)
2. **Enable model caching**
3. **Use CDN for static files**
4. **Implement Redis for caching**
5. **Optimize database indexes**
6. **Use production build for frontend**
7. **Enable compression**
8. **Load balance backend servers**

## Next Steps

1. Explore the application features
2. Add your own criminal records
3. Test sketch creation and matching
4. Customize facial components (in assets/)
5. Train custom models on your data
6. Configure deployment settings
7. Set up monitoring and logging

For questions or support, refer to the main README.md or contact the development team.
