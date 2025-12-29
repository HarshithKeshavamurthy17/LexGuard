# ✅ Railway Deployment Checklist

Use this checklist to ensure a successful deployment of LexGuard to Railway.

---

## 📋 Pre-Deployment

### Code Preparation
- [ ] All code is committed to GitHub
- [ ] `requirements.txt` is updated with all dependencies
- [ ] `requirements.txt` uses flexible versions (`>=` not `==`)
- [ ] Main app file is `app/streamlit_app.py`
- [ ] No hardcoded paths or local-only configurations
- [ ] Environment variables are used for all secrets

### Dependencies Check
- [ ] `streamlit` is in requirements.txt
- [ ] `fastapi` and `uvicorn` are in requirements.txt
- [ ] `pandas` and `numpy` are in requirements.txt (if used)
- [ ] `sentence-transformers` is in requirements.txt
- [ ] `chromadb` is in requirements.txt
- [ ] `plotly` is in requirements.txt
- [ ] `httpx` is in requirements.txt
- [ ] All other dependencies from `pyproject.toml` are in `requirements.txt`

### File Verification
- [ ] `app/streamlit_app.py` exists and is the main entry point
- [ ] `backend/main.py` exists
- [ ] `lexguard/` package structure is intact
- [ ] No local data files committed (use `.gitignore`)

---

## 🚂 Railway Setup

### Account & Project
- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] New project created in Railway
- [ ] Service created from GitHub repo

### Configuration
- [ ] Start command set: `streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- [ ] Python version set (3.11 recommended)
- [ ] Build command configured (if needed)

### Environment Variables
- [ ] `LLM_PROVIDER` set (gemini/openai/ollama)
- [ ] `EMBEDDING_PROVIDER` set (sentence-transformers recommended)
- [ ] API keys set (if using OpenAI/Gemini):
  - [ ] `OPENAI_API_KEY` (if using OpenAI)
  - [ ] `GOOGLE_API_KEY` (if using Gemini)
- [ ] Storage paths set:
  - [ ] `CHROMA_DB_PATH=/tmp/data/chroma`
  - [ ] `DATA_DIR=/tmp/data`
- [ ] Backend config set:
  - [ ] `BACKEND_HOST=127.0.0.1`
  - [ ] `BACKEND_PORT=8000`

---

## 🚀 Deployment

### Build Process
- [ ] Build starts automatically or manually triggered
- [ ] Build completes without errors
- [ ] All dependencies install successfully
- [ ] No import errors in build logs

### Service Startup
- [ ] Service starts successfully
- [ ] No port binding errors
- [ ] Backend starts correctly
- [ ] Streamlit app loads

### Domain Setup
- [ ] Domain generated in Railway
- [ ] Domain URL copied and saved
- [ ] Domain is accessible

---

## ✅ Post-Deployment Testing

### Basic Functionality
- [ ] App homepage loads
- [ ] No error messages on initial load
- [ ] Sidebar displays correctly
- [ ] File uploader is visible

### Core Features
- [ ] Can upload a PDF contract
- [ ] Contract analysis completes
- [ ] Dashboard tab shows data
- [ ] Clauses tab displays clauses
- [ ] Questions tab works
- [ ] Report generation works

### API Functionality
- [ ] Backend health check works
- [ ] Upload endpoint responds
- [ ] Chat endpoint works (if using LLM)
- [ ] Report download works

### Error Handling
- [ ] Invalid file upload shows error
- [ ] Missing API keys show appropriate message
- [ ] Network errors handled gracefully

---

## 🔍 Verification

### Logs Check
- [ ] No critical errors in Railway logs
- [ ] Backend startup logs visible
- [ ] Streamlit startup logs visible
- [ ] No repeated error messages

### Performance
- [ ] App loads within 30 seconds (after wake-up)
- [ ] Contract analysis completes in reasonable time
- [ ] No memory errors
- [ ] No timeout errors

### User Experience
- [ ] UI is responsive
- [ ] All buttons work
- [ ] Navigation between tabs works
- [ ] Data displays correctly

---

## 📝 Documentation

### README Update
- [ ] README.md updated with Railway deployment info
- [ ] Live demo URL added (or placeholder)
- [ ] Free tier notes added
- [ ] Wake-up time mentioned (10-30 seconds)

### Deployment Guide
- [ ] `RAILWAY_DEPLOYMENT.md` created
- [ ] Step-by-step instructions included
- [ ] Troubleshooting section added
- [ ] Environment variables documented

---

## 🎯 Final Steps

### Sharing
- [ ] Railway URL shared with team/users
- [ ] README updated with live URL
- [ ] Documentation updated

### Monitoring
- [ ] Railway dashboard bookmarked
- [ ] Logs accessible
- [ ] Metrics visible

### Maintenance
- [ ] Auto-deploy enabled (default)
- [ ] Environment variables documented
- [ ] Backup plan for data (if needed)

---

## 🐛 If Issues Occur

### Build Failures
1. Check `requirements.txt` for missing packages
2. Verify Python version compatibility
3. Review build logs for specific errors
4. Test locally with `pip install -r requirements.txt`

### Runtime Errors
1. Check Railway logs for error messages
2. Verify environment variables are set
3. Test backend startup locally
4. Check port configuration

### Service Crashes
1. Review Railway logs
2. Check memory usage
3. Verify start command is correct
4. Test with minimal configuration

---

## ✨ Success Criteria

- ✅ App is accessible via Railway URL
- ✅ All core features work
- ✅ No critical errors in logs
- ✅ Documentation is updated
- ✅ Team can access and use the app

---

**Deployment Date**: _______________

**Deployed By**: _______________

**Railway URL**: _______________

**Status**: ⬜ Pending | ⬜ In Progress | ⬜ Complete | ⬜ Failed

**Notes**:
_________________________________________________
_________________________________________________
_________________________________________________


