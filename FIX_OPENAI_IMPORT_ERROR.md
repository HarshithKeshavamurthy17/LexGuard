# 🔧 Fix: OpenAI Import Error on Railway

## The Problem
```
ModuleNotFoundError: No module named 'openai'
```

**Why this happens:**
- The code was importing `OpenAIClient` at module level
- This caused `openai` to be imported even when using Gemini
- `openai` package is not in `requirements.txt` (we're using Gemini)

## ✅ The Fix

I've made the imports **lazy** (only load when needed):

1. ✅ **`lexguard/llm/__init__.py`**: Only imports the client that's actually being used
2. ✅ **`lexguard/llm/openai_client.py`**: Handles missing `openai` package gracefully

**Before:**
```python
# ❌ Always imports, even if not used
from lexguard.llm.openai_client import OpenAIClient
```

**After:**
```python
# ✅ Only imports when provider is "openai"
if provider == "openai":
    from lexguard.llm.openai_client import OpenAIClient
    return OpenAIClient()
```

---

## 🚀 Next Steps

1. **Commit the fix:**
   ```bash
   git add lexguard/llm/__init__.py lexguard/llm/openai_client.py
   git commit -m "Fix OpenAI import error - make imports lazy"
   git push origin main
   ```

2. **Railway will auto-redeploy**

3. **The backend should start successfully now!**

---

## ✅ What This Fixes

- ✅ No more `ModuleNotFoundError: No module named 'openai'`
- ✅ Backend starts successfully with Gemini provider
- ✅ Only loads the LLM client that's actually configured
- ✅ Clear error if someone tries to use OpenAI without installing it

---

**Commit and push - the backend should start now!** 🎉

