# 🚀 Railway Deployment Guide
## Deploy Your MLOps Docker App from GitHub (No Docker Locally!)

Complete beginner-friendly guide to deploy your FastAPI ML app to Railway using GitHub Actions.

---

## 📋 Prerequisites

- ✅ GitHub account (free)
- ✅ Railway account (free tier available)
- ✅ Code pushed to GitHub repository
- ✅ No Docker installation needed!

---

## 🎯 Quick Start (5 Minutes)

### Step 1: Push Your Code to GitHub

```powershell
# Navigate to project
cd D:\Mlops-final

# Initialize Git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Railway deployment"

# Push to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/student-placement-mlops.git
git branch -M main
git push -u origin main
```

**Verify on GitHub:**
1. Go to https://github.com/YOUR_USERNAME/student-placement-mlops
2. Confirm all files are visible
3. Check Actions tab shows successful Docker build ✅

---

### Step 2: Create Railway Account

1. **Visit Railway**: https://railway.app/
2. **Click "Login"** → "Sign in with GitHub"
3. **Authorize Railway** to access your GitHub repositories
4. **Complete signup** (no credit card needed initially)

**Free Tier Includes:**
- $5 credit/month (~500 hours of usage)
- Enough for testing and small projects
- Automatic deployments included

---

### Step 3: Deploy from GitHub

#### Option A: One-Click Deploy (Easiest)

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select `student-placement-mlops`
4. Railway auto-detects the Dockerfile
5. Click **"Deploy Now"**

#### Option B: Manual Setup

If auto-detect fails:

1. Click **"New Project"** → **"Empty Project"**
2. Name it: "Student Placement API"
3. Click **"Add"** → **"GitHub Repo"**
4. Select your repository
5. Under **"Settings"**:
   - **Root Directory**: `/` (leave as default)
   - **Start Command**: `uvicorn app.fastapi_app:app --host 0.0.0.0 --port $PORT`
   - **DockerfilePath**: `./Dockerfile`

---

### Step 4: Configure Environment Variables

In Railway dashboard:

1. Click on your project
2. Go to **"Variables"** tab
3. Add these variables:

```
FASTAPI_ENV=production
MLFLOW_TRACKING_URI=file:/app/mlruns
PORT=8000
PYTHON_VERSION=3.10
```

**How to add:**
- Click "Variables" button
- Click "+ Variable"
- Enter KEY and VALUE
- Click "Add"

---

### Step 5: Deploy!

1. Go back to **"Deployment"** tab
2. Railway will automatically start building
3. Watch the logs in real-time
4. Wait for status: **"Deployed"** ✅

**Build Process:**
```
📦 Building...
  ├─ Pulling Python 3.10 image
  ├─ Installing dependencies
  ├─ Copying your code
  └─ Starting server
✅ Deployed!
```

---

### Step 6: Get Your Public URL

Once deployed:

1. Click **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"**
4. Copy your URL (looks like):
   ```
   https://your-project-name.up.railway.app
   ```

**Your API is now live!** 🎉

Access at:
- API Health: `https://your-project-name.up.railway.app/health`
- API Docs: `https://your-project-name.up.railway.app/docs`

---

## 🔧 Testing Your Deployment

### Test Health Endpoint

```powershell
# Replace with your actual Railway URL
curl https://your-project-name.up.railway.app/health

# Expected response:
{"status":"healthy","model_loaded":true,"version":"1.0.0"}
```

### Test Prediction Endpoint

```powershell
curl -X POST "https://your-project-name.up.railway.app/predict" `
  -H "Content-Type: application/json" `
  -d '{
    "cgpa": 8.5,
    "internships": 3,
    "projects": 5,
    "coding_skills_score": 75,
    "communication_skills_score": 80
  }'
```

### Open in Browser

Simply visit:
```
https://your-project-name.up.railway.app/docs
```

You'll see interactive Swagger UI documentation!

---

## 🔄 Automatic Updates

Railway automatically redeploys when you push to GitHub!

```powershell
# Make changes to your code
git add .
git commit -m "Improved prediction accuracy"
git push origin main
```

**What happens:**
1. GitHub Actions builds new Docker image
2. Railway detects the change
3. Automatically redeploys (takes ~2 minutes)
4. Your updates go live!

No manual intervention needed! ✨

---

## 📊 Monitoring Your Deployment

### View Logs in Railway

1. Go to Railway dashboard
2. Click your project
3. Click **"Deployments"** tab
4. Click latest deployment
5. View real-time logs

### Check Resource Usage

1. Click **"Metrics"** tab
2. See CPU, Memory, Network usage
3. Monitor for any issues

### Set Up Alerts (Optional)

Railway Pro accounts can set up alerts for:
- High CPU usage
- Memory limits
- Failed deployments

---

## 🆘 Troubleshooting

### Issue 1: Build Fails

**Check logs in Railway:**
```
❌ Build failed
Error: Cannot find module 'app.fastapi_app'
```

**Solution:**
- Verify file structure: `app/fastapi_app.py` exists
- Check import paths in your code
- Ensure `requirements.txt` has all dependencies

### Issue 2: Container Crashes on Startup

**Common causes:**
- Port mismatch
- Missing environment variables
- Model file not found

**Debug steps:**
1. Check Railway logs for error messages
2. Verify PORT variable is set to 8000
3. Ensure model is trained and saved before deployment

### Issue 3: 502 Bad Gateway

**Cause:** Application didn't start properly

**Solutions:**
```yaml
# In railway.json, ensure correct start command:
{
  "deploy": {
    "startCommand": "uvicorn app.fastapi_app:app --host 0.0.0.0 --port $PORT"
  }
}
```

### Issue 4: Slow Cold Starts

Railway spins down inactive projects. First request after inactivity takes ~30 seconds.

**Solutions:**
- Use Railway's "Always On" feature (Pro)
- Send periodic health checks
- Upgrade to paid plan for always-on

---

## 💰 Cost Estimation

### Free Tier ($5 credit/month)

**Example usage:**
- 500 hours/month = ~$2-3
- Leaves $2-7 for other projects
- Sufficient for development/testing

### Paid Plans

If you exceed free tier:
- Hobby: $5/month for 1000 hours
- Pro: $20/month for unlimited hours
- Pay-as-you-go also available

**Tip:** Delete projects when not in use to save credits!

---

## 🔐 Security Best Practices

### 1. Never Commit Secrets

```powershell
# ❌ Don't do this:
echo "API_KEY=secret123" >> .env
git add .env
git commit -m "Add secrets"  # BAD!

# ✅ Do this instead:
# Add secrets in Railway dashboard under Variables
```

### 2. Use GitHub Secrets for CI/CD

For sensitive values needed in GitHub Actions:

1. Go to GitHub repo Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add NAME and VALUE
4. Reference in workflow: `${{ secrets.YOUR_SECRET }}`

### 3. Enable HTTPS Only

Railway provides HTTPS automatically. Always use:
```
https://your-project.up.railway.app
```

Not:
```
http://your-project.up.railway.app  # ❌ Insecure
```

---

## 📈 Scaling Your Deployment

### Vertical Scaling (More Resources)

In Railway dashboard:
1. Settings → Scaling
2. Increase RAM (default: 512MB)
3. Increase CPU (default: 0.25 vCPU)
4. Changes apply immediately

### Horizontal Scaling (Multiple Instances)

Railway supports multiple instances:
1. Click "Scale" button
2. Choose number of replicas
3. Load balancer distributes traffic

### Database Integration

Railway offers managed databases:
1. New → Database
2. Choose PostgreSQL or MySQL
3. Connection string auto-injected as variable
4. Use in your app: `os.getenv("DATABASE_URL")`

---

## 🎯 Complete Workflow Summary

```
┌─────────────────────┐
│ 1. Write Code       │
│    (Local Machine)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 2. git push         │
│    (To GitHub)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 3. GitHub Actions   │
│    Builds Docker    │
│    (Cloud - Free)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 4. Railway Deploys  │
│    Runs Container   │
│    (Cloud - $5/mo)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 5. Live API         │
│    Public URL       │
│    Ready to Use!    │
└─────────────────────┘
```

---

## ✅ Deployment Checklist

Before deploying:

- [ ] All files committed to Git
- [ ] Code pushed to GitHub
- [ ] GitHub Actions build successful (green checkmark)
- [ ] `railway.json` file present
- [ ] `requirements.txt` has all dependencies
- [ ] Model trained and saved in `models/` folder
- [ ] No hardcoded secrets in code

After deploying:

- [ ] Deployment status shows "Deployed"
- [ ] Health endpoint responds: `/health`
- [ ] API docs accessible: `/docs`
- [ ] Prediction endpoint works: `/predict`
- [ ] Logs show no errors
- [ ] HTTPS enabled on domain

---

## 🎓 Learning Resources

- **Railway Docs**: https://docs.railway.app/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Docker Basics**: https://docs.docker.com/get-started/
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

## 🆘 Need Help?

### Railway Support
- Documentation: https://docs.railway.app/
- Discord Community: https://discord.gg/railway
- Twitter: @Railway

### GitHub Actions Help
- Community Forum: https://github.community/
- Stack Overflow: Tag `github-actions`

### This Project
- Check README.md for local setup
- Review DOCKER_QUICK_REFERENCE.md
- Create issue on GitHub repository

---

## 🎉 Success!

If you've followed this guide, you now have:

✅ **Live API** accessible worldwide  
✅ **Automatic deployments** on every git push  
✅ **Zero Docker** installed locally  
✅ **Production-grade** infrastructure  
✅ **Free tier** friendly setup  

**Congratulations on deploying your MLOps system!** 🚀

---

**Your deployment URL:** `https://your-project-name.up.railway.app`

**Next Steps:**
1. Share your API with friends/colleagues
2. Integrate with frontend applications
3. Monitor usage and performance
4. Iterate and improve your ML model!

---

**Last Updated:** March 14, 2026  
**Difficulty:** Beginner-Friendly ⭐⭐⭐⭐⭐
