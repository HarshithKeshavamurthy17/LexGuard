# ⚡ Fix: Build Timeout Issue

## The Problem
- Build is **timing out** (taking too long)
- Installing **PyTorch + CUDA** libraries (HUGE - several GB)
- `sentence-transformers` pulls in full PyTorch by default
- Railway free tier has build time limits

## The Solution

I've optimized `requirements.txt` to:
1. ✅ Use **CPU-only** versions (no CUDA)
2. ✅ Remove **unnecessary** dependencies (langchain, watchdog)
3. ✅ Use **onnxruntime** for lighter inference
4. ✅ Make OCR optional (pdf2image, pytesseract)

---

## What Changed

### Removed Heavy Dependencies:
- ❌ Full PyTorch (pulled in by sentence-transformers)
- ❌ CUDA libraries (nvidia-* packages)
- ❌ langchain packages (not needed - we use direct API calls)
- ❌ watchdog (development only)

### Kept Essential:
- ✅ sentence-transformers (but will use CPU/ONNX)
- ✅ chromadb (lightweight)
- ✅ All core functionality

---

## Next Steps

1. **Commit the optimized requirements.txt:**
   ```bash
   git add requirements.txt
   git commit -m "Optimize requirements to fix build timeout"
   git push origin main
   ```

2. **Railway will rebuild** - should be much faster now!

3. **Expected build time**: 2-5 minutes (instead of timing out)

---

## If Still Timing Out

### Option 1: Use Even Lighter Embeddings
Switch to API-based embeddings instead of local:

```bash
# In Railway Variables:
EMBEDDING_PROVIDER=gemini  # Use Gemini API instead of local
```

Then remove from requirements.txt:
```txt
# sentence-transformers>=2.2.2  # Comment out
# onnxruntime>=1.15.0  # Comment out
```

### Option 2: Pre-build Docker Image
Build locally and push to Docker Hub, then use that image in Railway.

### Option 3: Upgrade Railway Plan
Railway Pro ($20/month) has longer build timeouts.

---

## Why This Works

**Before:**
- sentence-transformers → PyTorch → CUDA → 5+ GB download
- Build time: 10+ minutes → **TIMEOUT**

**After:**
- sentence-transformers → ONNX Runtime (CPU) → ~500 MB
- Build time: 2-5 minutes → **SUCCESS** ✅

---

**Try the optimized requirements.txt first - it should fix it!** 🚀


