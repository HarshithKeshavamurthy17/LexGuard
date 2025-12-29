# 🚂 Railway Deployment Guide for LexGuard

Complete step-by-step guide to deploy LexGuard Contract AI to Railway.app.

---

## 📋 Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Railway Account** - Sign up at [railway.app](https://railway.app) (free tier available)
3. **API Keys** (optional) - For LLM providers:
   - OpenAI API key (if using OpenAI)
   - Google Gemini API key (if using Gemini)
   - Or use Ollama (local, requires setup)

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Ensure your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Sign in with your **GitHub account** (recommended for easy repo access)

### Step 3: Create a New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `legal-helper` repository
4. Railway will automatically detect it's a Python project

### Step 4: Configure the Service

Railway will create a service automatically. Now configure it:

#### 4.1 Set the Start Command

1. Go to your service settings
2. Click on **"Settings"** tab
3. Scroll to **"Start Command"**
4. Enter:
   ```bash
   streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
   ```

#### 4.2 Set Python Version (Optional but Recommended)

1. In the same **"Settings"** tab
2. Find **"Build Command"** (or create `runtime.txt`)
3. Create a file `runtime.txt` in your repo root with:
   ```
   python-3.11
   ```
   Or set it in Railway settings if available.

### Step 5: Configure Environment Variables

1. Go to your service **"Variables"** tab
2. Add the following environment variables:

#### 🔑 Get Your API Key First!

**You need a Google Gemini API key** (it's free!):
- Go to: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Sign in with Google account
- Click **"Create API Key"**
- Copy the key (starts with `AIza...`)

📖 **Full guide**: See [API_KEYS_SETUP.md](./API_KEYS_SETUP.md) for detailed instructions

#### Required Variables:

```bash
# LLM Provider (choose one: "ollama", "openai", or "gemini")
LLM_PROVIDER=gemini

# Embedding Provider (recommended: "sentence-transformers" for free tier)
EMBEDDING_PROVIDER=sentence-transformers

# If using OpenAI:
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# If using Gemini (REPLACE with your actual key from Google AI Studio!):
GOOGLE_API_KEY=AIzaSyC...paste_your_actual_key_here...
GEMINI_MODEL=models/gemini-1.5-flash-latest

# If using Ollama (requires Ollama service):
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://ollama:11434

# Storage paths (Railway provides ephemeral storage)
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data

# Backend configuration (for internal FastAPI)
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

#### Recommended for Free Tier:

```bash
# Use local embeddings to avoid API costs (no API key needed!)
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Use Gemini for LLM (free tier available - GET KEY FROM GOOGLE AI STUDIO!)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSyC...your_actual_key_from_google_ai_studio...
```

### Step 6: Deploy

1. Railway will automatically deploy when you push to GitHub
2. Or click **"Deploy"** button manually
3. Watch the build logs in the **"Deployments"** tab
4. Wait for deployment to complete (usually 2-5 minutes)

### Step 7: Generate a Domain

1. Go to **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"**
4. Railway will create a domain like: `lexguard-production.up.railway.app`
5. Copy this URL - your app is now live!

---

## 🔧 Configuration Details

### Port Configuration

Railway automatically sets the `$PORT` environment variable. The start command uses this:
- `--server.port $PORT` - Uses Railway's assigned port
- `--server.address 0.0.0.0` - Allows external connections

### Data Persistence

⚠️ **Important**: Railway's free tier uses **ephemeral storage**. Data is lost when the service restarts.

- Use `/tmp/data` for temporary storage (recommended for free tier)
- For production, consider Railway's persistent volumes (paid feature)
- Or use external storage (S3, etc.)

### Backend Startup

The Streamlit app automatically starts the FastAPI backend internally. No separate service needed.

---

## ✅ Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Can upload a PDF contract
- [ ] Analysis completes successfully
- [ ] Questions tab works
- [ ] Report generation works
- [ ] No errors in Railway logs

---

## 🐛 Troubleshooting

### Build Fails

**Error**: `ModuleNotFoundError` or missing package

**Solution**:
1. Check `requirements.txt` includes all dependencies
2. Ensure versions use `>=` not `==` (flexible versions)
3. Check Railway build logs for specific missing package

### App Crashes on Startup

**Error**: Port binding issues or import errors

**Solution**:
1. Verify start command: `streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
2. Check environment variables are set correctly
3. Review Railway logs in "Deployments" tab

### "Backend failed to start" Error

**Solution**:
1. Check `BACKEND_PORT` is set to `8000`
2. Verify `BACKEND_HOST` is `127.0.0.1`
3. Check Railway logs for backend startup errors

### Embedding Model Download Fails

**Error**: `sentence-transformers` model download timeout

**Solution**:
1. Increase build timeout in Railway settings (if available)
2. Or use a smaller model: `EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2`
3. Pre-download model in Dockerfile (advanced)

### Out of Memory Errors

**Error**: Service runs out of memory

**Solution**:
1. Railway free tier has limited RAM
2. Use smaller embedding models
3. Consider upgrading to paid tier for more resources

---

## 📊 Monitoring

### View Logs

1. Go to your service in Railway dashboard
2. Click **"Deployments"** tab
3. Click on latest deployment
4. View **"Logs"** tab for real-time logs

### Check Service Health

1. Visit your Railway domain
2. If app is sleeping, wait 10-30 seconds for wake-up
3. Check Railway metrics in dashboard

---

## 🔄 Updating Your App

Railway auto-deploys on every GitHub push:

1. Make changes to your code
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. Railway automatically detects the push and redeploys
4. Monitor deployment in Railway dashboard

---

## 💰 Free Tier Limitations

Railway's free tier includes:
- **$5 monthly credit** (usually enough for small apps)
- **Sleeps after 7 days** of inactivity
- **10-30 second wake-up time** (normal behavior)
- **Ephemeral storage** (data lost on restart)

### Acceptable Behavior:
- ✅ App sleeping after inactivity
- ✅ 10-30 second wake-up time
- ✅ Occasional restarts

### Not Allowed:
- ❌ Aggressive keep-alive scripts (violates ToS)
- ❌ Continuous polling to prevent sleep

---

## 🎯 Production Recommendations

For production use, consider:

1. **Upgrade to Railway Pro** ($20/month):
   - No sleep mode
   - Persistent storage
   - More resources

2. **Use External Storage**:
   - AWS S3 for contract storage
   - PostgreSQL for metadata
   - Redis for caching

3. **Add Monitoring**:
   - Railway's built-in metrics
   - External monitoring (Sentry, etc.)

4. **Set Up CI/CD**:
   - GitHub Actions for testing
   - Railway auto-deploy on merge

---

## 📞 Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **Project Issues**: Open an issue on GitHub

---

## ✨ Success!

Your LexGuard app should now be live at: `https://[your-project].up.railway.app`

Share the URL and start analyzing contracts! 🎉

