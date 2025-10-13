# 🔐 Environment Setup Guide

## ⚠️ IMPORTANT: Before Pushing to GitHub

Your Hugging Face API token is now stored in `.env` file which is **automatically ignored by Git**. This means your token is safe and won't be uploaded to GitHub.

## 📁 Files Created for Security

1. **`.env`** - Contains your actual API token (NEVER commit this!)
2. **`.env.example`** - Template file (safe to commit)
3. **`.gitignore`** - Protects `.env` from being committed

## 🔑 Setting Up Your Environment

### For First Time Setup (You):

Your `.env` file is already configured with your token:
```bash
HF_API_TOKEN=hf_your_token_here
```

### For Other Developers (Team Members):

1. Copy the example file:
   ```powershell
   cd backend
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add their own Hugging Face token:
   ```bash
   HF_API_TOKEN=their_token_here
   ```

3. Get token from: https://huggingface.co/settings/tokens

## 📝 What's in .env File

```properties
# Hugging Face API Token (Required for AI sketch generation)
HF_API_TOKEN=your_token_here

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/sketch_db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## ✅ Verify Setup

Check if backend is loading the token correctly:

```powershell
cd backend
.\venv\Scripts\python.exe test_app.py
```

You should see:
```
[INFO] AI Model Status: ENABLED (Hugging Face) ✅
[INFO] HF_API_TOKEN: hf_xxxxx...
```

## 🚫 What NOT to Do

❌ **NEVER** commit `.env` file to GitHub  
❌ **NEVER** hardcode API tokens in Python files  
❌ **NEVER** share your `.env` file publicly  

## ✅ What's Safe to Commit

✅ `.env.example` - Template without real tokens  
✅ `.gitignore` - Protects sensitive files  
✅ All Python code files  
✅ README and documentation  

## 🔄 How It Works Now

### Before (Unsafe):
```python
# Token hardcoded in file - BAD!
os.environ['HF_API_TOKEN'] = 'hf_actual_token'
```

### After (Safe):
```python
# Token loaded from .env file - GOOD!
from dotenv import load_dotenv
load_dotenv()
HF_API_TOKEN = os.environ.get('HF_API_TOKEN')
```

## 📤 Ready to Push to GitHub

Your repository is now safe to push:

```powershell
# Check what will be committed (should NOT see .env)
git status

# The .gitignore protects these files:
# - backend/.env (your token)
# - backend/venv/ (Python virtual environment)
# - backend/uploads/*.png (generated images)
# - node_modules/ (frontend dependencies)

# Add files
git add .

# Commit
git commit -m "Add AI sketch generator with environment security"

# Push
git push origin main
```

## 🔍 Double Check Before Pushing

Run this command to verify .env is ignored:
```powershell
git status --ignored
```

You should see `.env` listed under "Ignored files".

## 👥 For Team Members Cloning Your Repo

1. Clone the repository
2. Copy `.env.example` to `.env`
3. Get their own HF token from: https://huggingface.co/settings/tokens
4. Add token to their `.env` file
5. Install dependencies and run!

## 🆘 If Token Was Already Committed

If you accidentally committed your token before:

1. **Immediately revoke** the token at: https://huggingface.co/settings/tokens
2. Generate a new token
3. Update your `.env` file with new token
4. Follow GitHub's guide to remove sensitive data from history

## ✅ Summary

- ✅ Token stored in `.env` (protected by .gitignore)
- ✅ Template in `.env.example` (safe to share)
- ✅ Code loads from environment variables
- ✅ Safe to push to GitHub
- ✅ Team members can add their own tokens

Your code is now secure and ready for GitHub! 🎉
