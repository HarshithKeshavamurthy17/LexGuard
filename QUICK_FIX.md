# ⚡ Quick Fix - Do This Now

## The Problem
- Image size: 8.7 GB (too big!)
- Railway limit: 4.0 GB
- **Result**: Build failed ❌

## The Solution (3 Steps)

### Step 1: Commit the Fix Files
I've created these files for you:
- ✅ `.dockerignore` - Excludes large files
- ✅ `.railwayignore` - Excludes large files from Railway
- ✅ `runtime.txt` - Sets Python version

**Run this:**
```bash
git add .dockerignore .railwayignore runtime.txt
git commit -m "Fix Railway image size issue"
git push origin main
```

### Step 2: Wait for Railway to Redeploy
- Railway will auto-detect the push
- It will rebuild (should be ~1-2 GB now, not 8.7 GB)
- Check the "Deployments" tab
- Should see "SUCCESS" ✅

### Step 3: Add Variables (After Build Succeeds)
1. Click **"Variables"** tab (top menu - you can see it!)
2. Add these 8 variables:

```
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSyBBR6iROyACZh8kqyyNAE5l41hm5-0zHXo
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

## That's It! 🎉

After Step 1, Railway will rebuild automatically. Once it succeeds, add the variables and you're done!


