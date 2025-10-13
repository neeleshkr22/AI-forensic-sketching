# 🚀 Quick Start - Updated with Environment Variables

## Step 1: Setup Backend Environment

```powershell
cd backend

# Create virtual environment (if not exists)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies (includes python-dotenv)
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Copy environment template
Copy-Item .env.example .env

# Edit .env and add your Hugging Face token
# HF_API_TOKEN=your_token_here
```

## Step 2: Get Hugging Face API Token

1. Go to: https://huggingface.co/join
2. Create free account
3. Go to: https://huggingface.co/settings/tokens
4. Click "New token" → Select "Read" access
5. Copy token (starts with `hf_...`)
6. Add to `backend/.env` file

## Step 3: Start MongoDB

Ensure MongoDB is running on `mongodb://localhost:27017/`

## Step 4: Seed Database (First Time Only)

```powershell
cd backend
.\venv\Scripts\python.exe database/seed.py
```

## Step 5: Start Backend

```powershell
cd backend
.\venv\Scripts\python.exe test_app.py
```

You should see:
```
[INFO] AI Model Status: ENABLED (Hugging Face) ✅
```

## Step 6: Start Frontend

Open NEW terminal:
```powershell
cd frontend
npm install
npm run dev
```

## Step 7: Open Application

Frontend: http://localhost:5173
Backend: http://localhost:5000

## 🔐 IMPORTANT: Before GitHub Push

✅ Your `.env` file is protected by `.gitignore`  
✅ Token will NOT be uploaded to GitHub  
✅ Safe to push your code  

See: `SECURITY_SETUP.md` for details

## ✅ Verify Everything Works

Test sketch generation:
```powershell
cd backend
.\venv\Scripts\python.exe test_ai_generation.py
```

Should generate: `uploads/ai_generated_realistic.png`

## 🎨 Generate Your First Sketch

1. Open: http://localhost:5173
2. Navigate to "Create Sketch"
3. Enter: `"Female, 25, long hair, soft features"`
4. Click "Generate Sketch"
5. Wait 20 seconds
6. Enjoy realistic pencil sketch! ✨
