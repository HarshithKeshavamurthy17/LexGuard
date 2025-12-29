# 🔗 Ollama Base URL Guide for Railway

## ⚠️ Important: Railway Can't Run Ollama Server

Railway is a cloud platform - you **cannot** run an Ollama server on Railway itself. You have 3 options:

---

## Option 1: Use a Public Ollama Server (Recommended if you have one)

If you have Ollama running on:
- Your own server/VPS
- A cloud VM (AWS, DigitalOcean, etc.)
- A service like [Ollama Cloud](https://ollama.com) (if available)

**Set:**
```bash
OLLAMA_BASE_URL=http://your-server-ip:11434
# OR
OLLAMA_BASE_URL=https://your-ollama-domain.com
```

**Example:**
```bash
OLLAMA_BASE_URL=http://123.45.67.89:11434
```

---

## Option 2: Use Gemini for LLM + Sentence-Transformers for Embeddings (Easiest)

Since you don't have a public Ollama server, use this setup:

**Railway Variables:**
```bash
# LLM - Use Gemini (has free tier, but watch quotas)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here

# Embeddings - Use sentence-transformers (local, FREE, NO QUOTAS!)
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Other required vars
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

**This way:**
- ✅ Embeddings = sentence-transformers (free, no quotas)
- ✅ LLM = Gemini (free tier, but has quotas)
- ✅ No Ollama server needed

---

## Option 3: Set Up Your Own Ollama Server

1. **Get a VPS/Server** (DigitalOcean, AWS EC2, etc.)
2. **Install Ollama:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama serve
   ```
3. **Pull a model:**
   ```bash
   ollama pull llama3.2
   ```
4. **Make it accessible** (configure firewall, reverse proxy, etc.)
5. **Use the public IP/URL in Railway:**
   ```bash
   OLLAMA_BASE_URL=http://your-vps-ip:11434
   ```

---

## 🎯 Recommended Setup for Railway (No Ollama Server)

**Since you don't have Ollama running, use this:**

```bash
# LLM Provider
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSyBBR6iROyACZh8kqyyNAE5l41hm5-0zHXo

# Embeddings (local, free, no quotas!)
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Storage
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data

# Backend
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

**Don't set `OLLAMA_BASE_URL`** - it's not needed if you're using Gemini for LLM.

---

## ✅ Summary

- **If you have Ollama server:** `OLLAMA_BASE_URL=http://your-server:11434`
- **If you DON'T have Ollama server:** Use Gemini for LLM, sentence-transformers for embeddings (don't set `OLLAMA_BASE_URL`)

**For Railway, Option 2 is easiest!** 🚀

