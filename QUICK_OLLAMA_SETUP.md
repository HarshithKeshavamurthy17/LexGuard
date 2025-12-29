# ⚡ Quick Ollama Setup for Railway

## 🎯 Goal
Run Ollama on a **free cloud VM** and connect Railway to it.

---

## 🚀 Fastest Option: Oracle Cloud (FREE Forever)

### Step 1: Get Free VM (2 minutes)
1. Go to: **https://www.oracle.com/cloud/free/**
2. Sign up (needs credit card, but **won't charge** for free tier)
3. Create VM:
   - **Shape**: `VM.Standard.A1.Flex` (ARM, 4 CPU, 24GB RAM - **FREE!**)
   - **OS**: Ubuntu 22.04
   - **SSH Key**: Generate and download

### Step 2: Install Ollama (2 minutes)
```bash
# SSH into your VM
ssh ubuntu@YOUR_VM_IP

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in background
nohup ollama serve > ollama.log 2>&1 &

# Pull a model
ollama pull llama3.2
```

### Step 3: Open Port (1 minute)
1. Oracle Cloud Console → **Networking** → **Virtual Cloud Networks**
2. Click your VCN → **Security Lists** → **Default Security List**
3. **Add Ingress Rule:**
   - Source: `0.0.0.0/0`
   - Port: `11434`
   - Protocol: `TCP`

### Step 4: Set Railway Variables (1 minute)
In Railway → **Variables** tab, add:

```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://YOUR_VM_PUBLIC_IP:11434

EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=all-MiniLM-L6-v2

CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

**Replace `YOUR_VM_PUBLIC_IP` with your actual VM IP!**

---

## ✅ Done!

Your Railway app will now:
- ✅ Use **Ollama** for LLM (free, no quotas)
- ✅ Use **sentence-transformers** for embeddings (free, no quotas)
- ✅ **No Gemini needed!**

---

## 🔧 Keep Ollama Running

To keep Ollama running after you disconnect:

```bash
# Install screen
sudo apt install screen

# Start Ollama in screen
screen -S ollama
ollama serve
# Press Ctrl+A, then D to detach

# To reconnect later:
screen -r ollama
```

**Or use systemd** (better for production - see `OLLAMA_RAILWAY_SETUP.md`)

---

## 🆘 Troubleshooting

**Can't connect to Ollama?**
- Check firewall: Port 11434 must be open
- Check Ollama is running: `ps aux | grep ollama`
- Test from Railway: `curl http://YOUR_VM_IP:11434/api/tags`

**Ollama stops when I disconnect?**
- Use `screen` or `tmux` (see above)
- Or set up systemd service (see full guide)

---

**Total time: ~5 minutes. Free forever!** 🎉

