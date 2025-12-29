# 🔑 API Keys Setup Guide

How to get API keys for LexGuard deployment.

---

## 🎯 Quick Answer

You need a **Google Gemini API key** to use the LLM features. Here's how to get it:

---

## 🔵 Google Gemini API Key (Recommended - Free Tier Available)

### Step 1: Get Your API Key

1. **Go to Google AI Studio**
   - Visit: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   - Sign in with your Google account

2. **Create API Key**
   - Click **"Create API Key"**
   - Select or create a Google Cloud project
   - Copy the API key (starts with `AIza...`)

3. **Free Tier Limits**
   - ✅ Free tier available
   - ✅ 15 requests per minute
   - ✅ 1,500 requests per day
   - ✅ Good for testing and small projects

### Step 2: Use in Railway

Set this environment variable in Railway:
```bash
GOOGLE_API_KEY=AIzaSyC...your_actual_key_here...
```

**Important**: Replace `your_key_here` with your actual API key from Google AI Studio!

---

## 🟢 Alternative: OpenAI API Key

If you prefer OpenAI instead of Gemini:

### Step 1: Get OpenAI API Key

1. **Go to OpenAI Platform**
   - Visit: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Sign in or create account

2. **Create API Key**
   - Click **"Create new secret key"**
   - Copy the key (starts with `sk-...`)

3. **Pricing**
   - ⚠️ Pay-as-you-go (not free)
   - 💰 ~$0.15 per 1M tokens (GPT-4o-mini)
   - 💰 More expensive than Gemini free tier

### Step 2: Use in Railway

Set these environment variables:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...your_actual_key_here...
OPENAI_MODEL=gpt-4o-mini
```

---

## 🟡 Alternative: Use Only Local Embeddings (No API Key Needed!)

If you want to avoid API costs entirely, you can use **only local embeddings** (but LLM features won't work):

### Configuration (No API Key Required)

```bash
LLM_PROVIDER=gemini  # Still need this, but won't work without key
EMBEDDING_PROVIDER=sentence-transformers  # ✅ No API key needed!
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Limitation**: 
- ✅ Embeddings work (for search)
- ❌ Chat/LLM features won't work without API key
- ❌ Contract summaries won't work

---

## 📋 Recommended Setup for Free Tier

### Best Option: Gemini (Free Tier)

```bash
# LLM Configuration
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSyC...your_actual_key_here...

# Embeddings (Local - No API Key Needed!)
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Storage
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data

# Backend
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

**Why this setup?**
- ✅ Gemini free tier = $0 cost
- ✅ Local embeddings = $0 cost
- ✅ All features work
- ✅ Perfect for Railway free tier

---

## 🔐 Security Best Practices

### ✅ DO:
- Store API keys in Railway Variables (not in code)
- Use different keys for development/production
- Rotate keys periodically
- Monitor API usage

### ❌ DON'T:
- Commit API keys to GitHub
- Share keys publicly
- Use production keys in development
- Hardcode keys in source code

---

## 🧪 Test Your API Key

### Test Gemini Key:
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_KEY_HERE")
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
response = model.generate_content("Hello!")
print(response.text)
```

### Test OpenAI Key:
```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY_HERE")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

## 📊 Cost Comparison

| Provider | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Gemini** | ✅ Yes (15 req/min) | Pay-as-you-go | Free tier users |
| **OpenAI** | ❌ No | $0.15/1M tokens | Production apps |
| **sentence-transformers** | ✅ Always free | N/A | Local embeddings |

---

## 🆘 Troubleshooting

### Error: "API key not valid"
- Check key is copied correctly (no extra spaces)
- Verify key hasn't expired
- Ensure correct provider is set

### Error: "Quota exceeded"
- You've hit free tier limits
- Wait for quota reset (daily)
- Or upgrade to paid tier

### Error: "Invalid API key format"
- Gemini keys start with `AIza...`
- OpenAI keys start with `sk-...`
- Check you're using the right key type

---

## 📝 Quick Reference

### For Railway Deployment:

**Minimum Required (Gemini + Local Embeddings):**
```bash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSyC...your_key...
EMBEDDING_PROVIDER=sentence-transformers
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

**Where to get keys:**
- Gemini: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- OpenAI: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

**Need help?** Check the [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) guide!


