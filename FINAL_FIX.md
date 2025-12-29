# 🎯 Final Fix: Build Timeout

## The Real Problem
Your build is **timing out** because it's trying to install:
- PyTorch (~2GB)
- CUDA libraries (~3GB) 
- All dependencies (~8.7GB total)
- **Takes 10+ minutes → TIMEOUT** ❌

## ✅ The Solution: Use API-Based Embeddings

**Don't install local models!** Use Gemini API for embeddings instead.

### Step 1: Updated requirements.txt
I've removed `sentence-transformers` from requirements.txt. This removes:
- ❌ PyTorch (2GB)
- ❌ CUDA libraries (3GB)
- ❌ Build timeout issues

### Step 2: Set Environment Variable
In Railway **Variables** tab, set:
```bash
EMBEDDING_PROVIDER=gemini
```

This uses Gemini API for embeddings (free tier available) instead of downloading heavy local models.

### Step 3: Commit and Push
```bash
git add requirements.txt
git commit -m "Remove sentence-transformers to fix build timeout - use Gemini API instead"
git push origin main
```

---

## 📋 Complete Railway Variables

After the build succeeds, add ALL these variables:

```bash
# LLM
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSyBBR6iROyACZh8kqyyNAE5l41hm5-0zHXo

# Embeddings (API-based - no local models!)
EMBEDDING_PROVIDER=gemini
EMBEDDING_MODEL=models/embedding-001

# Storage
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data

# Backend
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

---

## ⚡ Why This Works

**Before:**
- sentence-transformers → PyTorch → CUDA → 8.7GB → **TIMEOUT** ❌

**After:**
- Gemini API embeddings → No local models → ~500MB → **SUCCESS** ✅

---

## 🚀 Expected Results

- **Build time**: 2-5 minutes (instead of timing out)
- **Image size**: ~500MB-1GB (instead of 8.7GB)
- **All features work**: Gemini API handles embeddings
- **Free tier friendly**: No heavy downloads

---

## ✅ Next Steps

1. **Commit the updated requirements.txt**
2. **Push to GitHub**
3. **Railway will rebuild** (should succeed now!)
4. **Add variables** (especially `EMBEDDING_PROVIDER=gemini`)
5. **Done!** 🎉

---

**This should fix it!** The build will be much faster without PyTorch/CUDA. 🚀


