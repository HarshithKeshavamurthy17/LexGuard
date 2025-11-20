# 🦙 Ollama Setup Guide for LexGuard

LexGuard now uses **Ollama** - a free, local AI that runs on your computer. No API keys, no payments, 100% private!

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Ollama

**macOS:**
```bash
brew install ollama
```

Or download from: https://ollama.ai/download

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download installer from: https://ollama.ai/download

---

### Step 2: Start Ollama

```bash
ollama serve
```

Keep this terminal window open! (Or it runs in the background on macOS/Linux)

---

### Step 3: Download a Model

Open a **new terminal** and run:

```bash
ollama pull llama3.2
```

This downloads the Llama 3.2 model (~2GB). Takes 2-5 minutes depending on your internet.

**Alternative models:**
- `ollama pull phi3` - Smaller, faster (1.5GB)
- `ollama pull mistral` - Good balance (4GB)
- `ollama pull llama3.2:1b` - Smallest version (1GB)

---

### Step 4: Test It Works

```bash
ollama run llama3.2 "Hello, how are you?"
```

You should see a response! If you do, you're ready to go! ✅

---

## 🎯 Run LexGuard with Ollama

Now that Ollama is set up:

```bash
cd /Users/anithalakshmipathy/Documents/legal-helper
make run
```

That's it! LexGuard will automatically use Ollama.

---

## 🔧 Configuration

Your `.env` file is already configured for Ollama:

```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

**To change the model**, edit `.env`:
```bash
OLLAMA_MODEL=phi3  # or mistral, or any other model
```

Then restart LexGuard.

---

## 🆚 Ollama vs OpenAI

| Feature | Ollama (Free) | OpenAI (Paid) |
|---------|---------------|---------------|
| Cost | 100% Free | ~$0.01-0.05 per contract |
| Privacy | Runs locally | Data sent to OpenAI |
| Speed | Depends on your hardware | Very fast |
| Quality | Good (90% of OpenAI) | Excellent |
| Setup | 5 minutes | Instant (need API key) |

**Recommendation:** Start with Ollama. Upgrade to OpenAI later if you need higher quality.

---

## 💡 Recommended Models

### For Best Speed (Recommended for most users)
```bash
ollama pull llama3.2:1b  # Fastest, still good quality
```

### For Best Quality
```bash
ollama pull llama3.2  # Default, great balance
```

### For Lowest Memory Usage
```bash
ollama pull phi3  # Only 1.5GB, works on older computers
```

---

## 🛠️ Troubleshooting

### "Connection refused" error

**Problem:** Ollama isn't running

**Solution:**
```bash
# Start Ollama
ollama serve

# Keep this terminal open and run LexGuard in another terminal
```

---

### Model not found

**Problem:** You haven't downloaded the model

**Solution:**
```bash
ollama pull llama3.2
```

---

### Slow responses

**Problem:** Model is too large for your hardware

**Solution:** Use a smaller model:
```bash
ollama pull llama3.2:1b
```

Then update `.env`:
```bash
OLLAMA_MODEL=llama3.2:1b
```

---

### Out of memory

**Problem:** Not enough RAM

**Solutions:**
1. Use smallest model: `ollama pull phi3`
2. Close other applications
3. Or switch to OpenAI (cloud-based, no local memory needed)

---

## 🎮 Using Ollama

Once Ollama is running, LexGuard will automatically:
- ✅ Use it for contract summaries
- ✅ Use it for chat responses
- ✅ Use it for risk explanations
- ✅ Still use local embeddings (no internet needed!)

Everything runs on your computer. No data leaves your machine!

---

## 🔄 Switching Back to OpenAI

If you want to use OpenAI later:

1. Get an OpenAI API key
2. Edit `.env`:
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_key_here
   ```
3. Restart LexGuard

---

## 📊 Performance Expectations

**With Ollama on a typical laptop:**
- Contract analysis: 30-60 seconds
- Chat response: 5-15 seconds
- Summary generation: 20-40 seconds

**With OpenAI API:**
- Contract analysis: 10-30 seconds
- Chat response: 2-5 seconds
- Summary generation: 5-15 seconds

Both work great! Ollama just takes a bit longer.

---

## ✅ Verify Everything Works

Quick test:

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Test model
ollama run llama3.2 "Explain what a contract is in one sentence"

# Terminal 3: Run LexGuard
cd /Users/anithalakshmipathy/Documents/legal-helper
make run
```

If all three work, you're golden! 🎉

---

## 🆘 Need Help?

1. Check Ollama is running: `ollama list`
2. Check model is downloaded: `ollama list` (should show llama3.2)
3. Test Ollama directly: `ollama run llama3.2 "test"`
4. Check LexGuard logs for errors

---

**Enjoy your free, private, local AI contract analyzer!** 🚀⚖️


