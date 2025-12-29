# 🔧 Fix: Langchain Import Error on Railway

## The Problem
```
ModuleNotFoundError: No module named 'langchain_google_genai'
```

**Why this happens:**
- The code was importing `GoogleGenerativeAIEmbeddings` from `langchain_google_genai`
- This package is not in `requirements.txt` (we removed langchain dependencies)
- We're using Gemini API directly, not through langchain

## ✅ The Fix

I've replaced the langchain-based embeddings with **direct Gemini API calls**:

1. ✅ **Removed langchain import** from `lexguard/llm/gemini_client.py`
2. ✅ **Created `GeminiEmbeddings` class** that uses `google-generativeai` directly
3. ✅ **Made langchain import lazy** in `lexguard/llm/base.py` (for sentence-transformers fallback)

**Before:**
```python
# ❌ Requires langchain_google_genai package
from langchain_google_genai import GoogleGenerativeAIEmbeddings
```

**After:**
```python
# ✅ Uses google-generativeai directly (already installed)
import google.generativeai as genai

class GeminiEmbeddings:
    def embed_query(self, text: str) -> List[float]:
        # Direct API call
        result = genai.embed_content(model=self.model, content=text)
        return result.embedding
```

---

## 🚀 Next Steps

1. **Commit the fix:**
   ```bash
   git add lexguard/llm/gemini_client.py lexguard/llm/base.py
   git commit -m "Fix langchain import error - use direct Gemini API for embeddings"
   git push origin main
   ```

2. **Railway will auto-redeploy**

3. **Document upload should work now!**

---

## ✅ What This Fixes

- ✅ No more `ModuleNotFoundError: No module named 'langchain_google_genai'`
- ✅ Embeddings work using direct Gemini API
- ✅ No langchain dependencies needed
- ✅ Document upload and analysis should work

---

**Commit and push - document upload should work now!** 🎉

