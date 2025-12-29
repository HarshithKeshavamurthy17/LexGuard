# 🐛 Troubleshooting Guide for Railway Deployment

Common issues and solutions when deploying LexGuard to Railway.

---

## 🔴 Build Failures

### Error: `ModuleNotFoundError: No module named 'X'`

**Cause**: Missing dependency in `requirements.txt`

**Solution**:
1. Check which package is missing from the error message
2. Add it to `requirements.txt` with flexible version:
   ```txt
   package-name>=1.0.0
   ```
3. Commit and push:
   ```bash
   git add requirements.txt
   git commit -m "Add missing dependency"
   git push origin main
   ```
4. Railway will auto-redeploy

**Prevention**: Always test locally first:
```bash
pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
```

---

### Error: `ERROR: Could not find a version that satisfies the requirement`

**Cause**: Version conflict or package doesn't exist

**Solution**:
1. Check the package name is correct
2. Use flexible versions (`>=` instead of `==`)
3. Remove version pinning if causing issues:
   ```txt
   # Bad
   pandas==2.1.3
   
   # Good
   pandas>=2.0.0
   ```

---

### Error: Build timeout

**Cause**: Large dependencies (like `sentence-transformers`) taking too long to download

**Solution**:
1. Railway free tier has build time limits
2. Use smaller models:
   ```bash
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```
3. Consider using Railway Pro tier for faster builds

---

## 🟡 Runtime Errors

### Error: `Backend failed to start within the expected time`

**Cause**: FastAPI backend not starting correctly

**Solution**:
1. Check environment variables:
   ```bash
   BACKEND_HOST=127.0.0.1
   BACKEND_PORT=8000
   ```
2. Check Railway logs for backend startup errors
3. Verify port is not already in use
4. Increase timeout in `streamlit_app.py` if needed

---

### Error: `Port already in use` or `Address already in use`

**Cause**: Port conflict or incorrect port configuration

**Solution**:
1. Ensure start command uses `$PORT`:
   ```bash
   streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
   ```
2. Don't hardcode port numbers
3. Railway sets `$PORT` automatically

---

### Error: `ImportError: cannot import name 'X'`

**Cause**: Missing package or version mismatch

**Solution**:
1. Check `requirements.txt` includes the package
2. Verify package version compatibility
3. Check Railway build logs for installation errors
4. Test imports locally:
   ```bash
   python -c "import package_name"
   ```

---

### Error: `FileNotFoundError: /data/chroma` or storage errors

**Cause**: Incorrect storage path for Railway

**Solution**:
1. Use Railway's ephemeral storage:
   ```bash
   CHROMA_DB_PATH=/tmp/data/chroma
   DATA_DIR=/tmp/data
   ```
2. Create directories in code if needed
3. Note: Data is lost on restart (ephemeral storage)

---

## 🟠 LLM/API Errors

### Error: `429 Quota exceeded` (Gemini)

**Cause**: API quota limit reached

**Solution**:
1. Switch to local embeddings:
   ```bash
   EMBEDDING_PROVIDER=sentence-transformers
   ```
2. Check API usage in Google Cloud Console
3. Wait for quota reset or upgrade API plan
4. Use OpenAI as alternative

---

### Error: `401 Unauthorized` or `Invalid API key`

**Cause**: Missing or incorrect API key

**Solution**:
1. Verify API key is set in Railway environment variables
2. Check key has no extra spaces or quotes
3. Regenerate API key if needed
4. Ensure correct variable name:
   - `OPENAI_API_KEY` for OpenAI
   - `GOOGLE_API_KEY` for Gemini

---

### Error: `Model not found` (Gemini)

**Cause**: Incorrect model name format

**Solution**:
1. Use correct format:
   ```bash
   GEMINI_MODEL=models/gemini-1.5-flash-latest
   ```
2. Check available models in Gemini docs
3. Ensure model name starts with `models/`

---

## 🟢 Service Issues

### App is sleeping / takes 30+ seconds to load

**Cause**: Normal behavior for Railway free tier

**Solution**:
1. **This is expected!** Free tier apps sleep after 7 days of inactivity
2. Wait 10-30 seconds for wake-up
3. Add note to README about wake-up time
4. Consider upgrading to Railway Pro for no sleep mode

**Do NOT**:
- ❌ Create keep-alive scripts (violates ToS)
- ❌ Continuously ping the app
- ❌ Use external services to ping app

---

### Error: `502 Bad Gateway` or service unavailable

**Cause**: Service crashed or not responding

**Solution**:
1. Check Railway logs for crash errors
2. Verify start command is correct
3. Check memory usage (free tier has limits)
4. Restart service in Railway dashboard
5. Review recent code changes that might cause crashes

---

### Error: Out of memory

**Cause**: Railway free tier memory limits

**Solution**:
1. Use smaller embedding models
2. Reduce batch sizes in code
3. Optimize memory usage
4. Consider upgrading to Railway Pro
5. Use external services for heavy processing

---

## 🔵 Configuration Issues

### Environment variables not working

**Cause**: Variables not set or incorrect names

**Solution**:
1. Check Railway Variables tab
2. Verify variable names match code (case-sensitive)
3. Restart service after adding variables
4. Check logs for variable access errors
5. Use Railway's variable validation

---

### Wrong Python version

**Cause**: Railway using wrong Python version

**Solution**:
1. Create `runtime.txt` in repo root:
   ```
   python-3.11
   ```
2. Or set in Railway settings if available
3. Redeploy after changing

---

## 🟣 Data Persistence Issues

### Data lost after restart

**Cause**: Railway free tier uses ephemeral storage

**Solution**:
1. **Expected behavior** - data is lost on restart
2. Use `/tmp/data` for temporary storage
3. For production, use:
   - Railway persistent volumes (paid)
   - External storage (S3, etc.)
   - Database (PostgreSQL, etc.)

---

## 📊 Debugging Tips

### View Logs

1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click latest deployment
5. View "Logs" tab

### Test Locally First

Always test changes locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Test with Railway-like environment
export PORT=8501
streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

### Check Environment

Verify environment variables in Railway:
1. Go to "Variables" tab
2. Check all required variables are set
3. Verify values are correct (no typos)

### Common Commands

```bash
# Check if app runs locally
make run

# Test imports
python -c "import streamlit; import fastapi; print('OK')"

# Check requirements
pip check

# Verify file structure
ls -la app/streamlit_app.py
```

---

## 🆘 Still Having Issues?

### Get Help

1. **Check Railway Logs**: Most issues show up in logs
2. **Railway Docs**: [docs.railway.app](https://docs.railway.app)
3. **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
4. **GitHub Issues**: Open an issue with:
   - Error message
   - Railway logs
   - Steps to reproduce
   - Environment details

### Useful Links

- [Railway Documentation](https://docs.railway.app)
- [Streamlit Deployment Guide](https://docs.streamlit.io/deploy)
- [Python Environment Variables](https://docs.python.org/3/library/os.html#os.environ)

---

## ✅ Prevention Checklist

Before deploying, ensure:

- [ ] All dependencies in `requirements.txt`
- [ ] Versions use `>=` not `==`
- [ ] Tested locally with `pip install -r requirements.txt`
- [ ] Environment variables documented
- [ ] Start command uses `$PORT`
- [ ] Storage paths use `/tmp/data`
- [ ] No hardcoded local paths
- [ ] API keys are set in Railway
- [ ] Python version specified

---

**Last Updated**: Check Railway logs first - they usually contain the solution!


