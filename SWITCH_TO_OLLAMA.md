# 🔄 Switch to Ollama (Free, No Quotas)

## ✅ Changes Made

1. **Default LLM Provider**: Changed from `gemini` to `ollama`
2. **Default Embedding Provider**: Set to `sentence-transformers` (local, free)
3. **Added Ollama Embedding Support**: Can use Ollama server for embeddings if available
4. **Fallback Logic**: Falls back to sentence-transformers if Ollama server not available

## 🚀 For Railway Deployment

Since Railway can't run Ollama server, the app will use:
- **LLM**: Ollama (but you need to set `OLLAMA_BASE_URL` to a public Ollama instance OR use sentence-transformers for embeddings only)
- **Embeddings**: sentence-transformers (local, free, no quotas)

**Actually, for Railway, you should:**
- Use `sentence-transformers` for embeddings (already default)
- For LLM, you can either:
  1. Set up a public Ollama instance and point `OLLAMA_BASE_URL` to it
  2. Or switch back to Gemini for LLM (but use sentence-transformers for embeddings)

## 📋 Railway Environment Variables

```bash
# LLM - Use Ollama (or set to gemini if no Ollama server)
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434  # Or your public Ollama URL

# Embeddings - Use sentence-transformers (local, free)
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Other required vars
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

## ⚠️ Important Note

**For Railway (no Ollama server):**
- The app defaults to `sentence-transformers` for embeddings (works!)
- For LLM, if you don't have a public Ollama instance, you can:
  - Keep `LLM_PROVIDER=ollama` and it will try to connect (will fail gracefully)
  - OR set `LLM_PROVIDER=gemini` for LLM but keep `EMBEDDING_PROVIDER=sentence-transformers`

**The key fix:** Embeddings now use `sentence-transformers` (local, free, no quotas) instead of Gemini API!

---

## 🎯 What This Fixes

- ✅ No more Gemini API quota errors for embeddings
- ✅ Uses local sentence-transformers (free, no limits)
- ✅ Ollama support for LLM (if server available)
- ✅ Graceful fallbacks if Ollama not available

**Commit and push - embeddings will work without quotas!** 🎉

