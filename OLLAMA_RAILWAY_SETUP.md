# 🚀 Ollama Setup for Railway (Free Tier)

## The Problem
Railway can't run Ollama server directly. You need Ollama running somewhere else that Railway can access.

## ✅ Solution: Free Cloud Ollama Server

You have **3 free options** to run Ollama:

---

## Option 1: Oracle Cloud Free Tier (Recommended - Easiest)

**Oracle Cloud offers a free tier with 2 VMs!**

### Steps:

1. **Sign up for Oracle Cloud Free Tier:**
   - Go to: https://www.oracle.com/cloud/free/
   - Create account (requires credit card, but won't charge for free tier)

2. **Create a VM:**
   - Go to Compute → Instances
   - Create instance:
     - **Shape**: VM.Standard.A1.Flex (ARM, 4 OCPU, 24GB RAM - FREE!)
     - **OS**: Ubuntu 22.04
     - **SSH Key**: Generate and download

3. **Install Ollama on the VM:**
   ```bash
   # SSH into your VM
   ssh ubuntu@your-vm-ip
   
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Start Ollama (runs on port 11434)
   ollama serve
   
   # In another terminal, pull a model
   ollama pull llama3.2
   ```

4. **Make it accessible:**
   - In Oracle Cloud, go to: Networking → Virtual Cloud Networks
   - Edit Security List → Ingress Rules
   - Add rule: Source 0.0.0.0/0, Port 11434, Protocol TCP

5. **Get your public IP:**
   - In Compute → Instances, find your VM's public IP

6. **Set Railway variables:**
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

---

## Option 2: Google Cloud Free Tier

**Google Cloud offers $300 free credits for 90 days**

1. **Sign up:** https://cloud.google.com/free
2. **Create VM:**
   - Compute Engine → VM Instance
   - Machine type: e2-micro (free tier eligible)
   - OS: Ubuntu 22.04
3. **Install Ollama** (same as Option 1)
4. **Open firewall port 11434**
5. **Use the public IP in Railway**

---

## Option 3: Run Ollama in Railway (Advanced)

**This is tricky but possible with Docker:**

1. **Create a separate Railway service for Ollama**
2. **Use a Dockerfile that runs Ollama**
3. **Get the internal Railway URL**

But this is complex. **Option 1 (Oracle Cloud) is much easier!**

---

## 🎯 Quick Start: Oracle Cloud (5 minutes)

1. **Sign up:** https://www.oracle.com/cloud/free/
2. **Create VM** (ARM shape, Ubuntu 22.04)
3. **SSH and run:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama serve &
   ollama pull llama3.2
   ```
4. **Open port 11434** in firewall
5. **Copy public IP** → Use in Railway: `OLLAMA_BASE_URL=http://YOUR_IP:11434`

---

## ⚠️ Important Notes

- **Keep Ollama running:** Use `screen` or `tmux` to keep it running:
  ```bash
  screen -S ollama
  ollama serve
  # Press Ctrl+A then D to detach
  ```

- **Or use systemd service** (better for production):
  ```bash
  # Create service file
  sudo nano /etc/systemd/system/ollama.service
  ```
  ```ini
  [Unit]
  Description=Ollama Service
  After=network.target

  [Service]
  ExecStart=/usr/local/bin/ollama serve
  User=ubuntu
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
  ```bash
  sudo systemctl enable ollama
  sudo systemctl start ollama
  ```

---

## ✅ Final Railway Variables

Once you have Ollama running on a VM:

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

**That's it! Your app will use Ollama (free, no quotas) for LLM and sentence-transformers for embeddings!** 🎉

