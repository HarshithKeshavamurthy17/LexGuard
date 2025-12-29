# 🚀 Railway Setup - Next Steps

You have your API key! Here's exactly what to do now.

---

## ⚠️ SECURITY FIRST

**Your API key is sensitive!** If you've shared it publicly:
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Delete the old key
3. Create a new one
4. Keep it private!

---

## 📋 Step-by-Step: Add Key to Railway

### Step 1: Go to Railway Dashboard

1. Open [railway.app](https://railway.app)
2. Sign in
3. Select your project (or create one if you haven't)

### Step 2: Find the Variables Tab

**Where is it?** Look for one of these:

**Option A: In the Service Settings**
1. Click on your **service** (the box with your app name)
2. Look at the **top menu bar** - you'll see tabs like:
   - **Deployments** | **Metrics** | **Settings** | **Variables** ← **CLICK THIS!**
3. Click **"Variables"** tab

**Option B: In Project Settings**
1. If you don't see Variables in the service, click the **project name** (top left)
2. Go to **"Settings"** → **"Variables"**

**Option C: Quick Access**
1. Click on your service
2. Look for a button/link that says **"Variables"** or **"Environment Variables"**
3. It's usually in the top navigation or in a sidebar

**Still can't find it?**
- Try clicking **"Settings"** first, then look for **"Variables"** inside
- Or look for **"Environment"** or **"Env"** tab
- Railway UI might vary slightly, but it's always in the service settings area

### Step 3: Add Environment Variables

Click **"New Variable"** and add these one by one:

#### Variable 1: LLM Provider
- **Name**: `LLM_PROVIDER`
- **Value**: `gemini`
- Click **"Add"**

#### Variable 2: Google API Key (YOUR KEY!)
- **Name**: `GOOGLE_API_KEY`
- **Value**: `AIzaSyBBR6iROyACZh8kqyyNAE5l41hm5-0zHXo` *(paste your actual key)*
- Click **"Add"**

#### Variable 3: Embedding Provider
- **Name**: `EMBEDDING_PROVIDER`
- **Value**: `sentence-transformers`
- Click **"Add"**

#### Variable 4: Embedding Model
- **Name**: `EMBEDDING_MODEL`
- **Value**: `sentence-transformers/all-MiniLM-L6-v2`
- Click **"Add"**

#### Variable 5: Chroma DB Path
- **Name**: `CHROMA_DB_PATH`
- **Value**: `/tmp/data/chroma`
- Click **"Add"**

#### Variable 6: Data Directory
- **Name**: `DATA_DIR`
- **Value**: `/tmp/data`
- Click **"Add"**

#### Variable 7: Backend Host
- **Name**: `BACKEND_HOST`
- **Value**: `127.0.0.1`
- Click **"Add"**

#### Variable 8: Backend Port
- **Name**: `BACKEND_PORT`
- **Value**: `8000`
- Click **"Add"**

### Step 4: Verify All Variables

You should see 8 variables in the list:
- ✅ `LLM_PROVIDER` = `gemini`
- ✅ `GOOGLE_API_KEY` = `AIzaSy...` (your key)
- ✅ `EMBEDDING_PROVIDER` = `sentence-transformers`
- ✅ `EMBEDDING_MODEL` = `sentence-transformers/all-MiniLM-L6-v2`
- ✅ `CHROMA_DB_PATH` = `/tmp/data/chroma`
- ✅ `DATA_DIR` = `/tmp/data`
- ✅ `BACKEND_HOST` = `127.0.0.1`
- ✅ `BACKEND_PORT` = `8000`

### Step 5: Redeploy

1. Go to **"Deployments"** tab
2. Click **"Redeploy"** (or Railway will auto-redeploy)
3. Wait for deployment to complete (2-5 minutes)

### Step 6: Test

1. Go to your Railway domain
2. Try uploading a contract
3. Check if analysis works
4. Test the Questions tab

---

## ✅ Quick Copy-Paste Checklist

Add these to Railway Variables:

```bash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSyBBR6iROyACZh8kqyyNAE5l41hm5-0zHXo
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_DB_PATH=/tmp/data/chroma
DATA_DIR=/tmp/data
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

---

## 🎯 What Happens Next?

1. **Railway will redeploy** with your new variables
2. **App will start** with Gemini API access
3. **All features will work**:
   - ✅ Contract upload
   - ✅ AI analysis
   - ✅ Questions/chat
   - ✅ Report generation

---

## 🐛 If Something Goes Wrong

### Check Railway Logs:
1. Go to **"Deployments"** tab
2. Click latest deployment
3. View **"Logs"** tab
4. Look for errors

### Common Issues:
- **"Invalid API key"** → Check key is copied correctly (no spaces)
- **"Quota exceeded"** → You've hit free tier limits (wait or upgrade)
- **"Backend failed"** → Check `BACKEND_PORT` is `8000`

---

## 🔐 Security Reminder

**After adding to Railway:**
- ✅ Key is stored securely in Railway
- ✅ Never commit keys to GitHub
- ✅ Don't share keys publicly
- ✅ Consider rotating keys periodically

---

## ✨ You're Done!

Once variables are added and app redeploys, your LexGuard app will be fully functional with Gemini AI! 🎉

