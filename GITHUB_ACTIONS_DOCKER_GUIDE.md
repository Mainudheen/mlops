# ☁️ GitHub Actions Docker + Railway Deployment Guide
## Complete Setup for Low-Storage Environments

**Build Docker images in the cloud without installing Docker locally, then deploy to Railway with automatic CI/CD.**

---

## 🎯 What This Solves

**Problem:** You want to use Docker and deploy your MLOps project, but you have limited disk space and can't install Docker Desktop (requires 5GB+).

**Solution:** Use GitHub Actions to build Docker images in the cloud, then deploy to Railway directly from GitHub.

---

## ✅ What's Been Created

### Files Added to Your Project:

1. **`Dockerfile`** - Multi-stage optimized Docker configuration
2. **`requirements.txt`** - Essential Python dependencies
3. **`.github/workflows/docker-build.yml`** - GitHub Actions workflow
4. **`railway.json`** - Railway deployment configuration
5. **`GITHUB_ACTIONS_DOCKER_GUIDE.md`** - This comprehensive guide
6. **`RAILWAY_DEPLOYMENT_GUIDE.md`** - Detailed Railway instructions

---

## 🚀 Quick Start (Choose Your Path)

### Path A: I Want to Learn Everything
Read these guides in order:
1. [`GITHUB_ACTIONS_DOCKER_GUIDE.md`](./GITHUB_ACTIONS_DOCKER_GUIDE.md) - How cloud Docker builds work
2. [`RAILWAY_DEPLOYMENT_GUIDE.md`](./RAILWAY_DEPLOYMENT_GUIDE.md) - Step-by-step deployment

### Path B: Just Show Me The Commands
```powershell
# 1. Initialize Git
cd D:\Mlops-final
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/student-placement-mlops.git
git branch -M main
git push -u origin main

# 3. Watch GitHub Actions build Docker image
# Go to: https://github.com/YOUR_USERNAME/student-placement-mlops/actions

# 4. Deploy to Railway
# Go to: https://railway.app/new
# Select your GitHub repository
```

### Path C: I Need Docker Locally Anyway
Use local deployment instead:
```powershell
# Run without Docker
.\start-local.bat

# Or install Docker later and run:
.\start-docker.bat
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ YOUR WORKFLOW (No Docker Installed!)                    │
└─────────────────────────────────────────────────────────┘

Step 1: Write Code
  ↓
  Local Machine (D:\Mlops-final)
  - Edit Python files
  - Test locally
  - Commit to Git
  ↓
  
Step 2: git push
  ↓
  GitHub Repository
  - Code stored safely
  - Triggers GitHub Actions
  ↓
  
Step 3: GitHub Actions (Cloud Build)
  ↓
  Ubuntu VM with Docker pre-installed
  - Builds Docker image
  - Runs tests
  - Creates production artifact
  ↓
  
Step 4: Railway Deployment
  ↓
  Railway Cloud Platform
  - Pulls Docker image from GitHub
  - Runs container
  - Provides public URL
  ↓
  
Step 5: Live API
  ↓
  https://your-project.up.railway.app
  - Accessible worldwide
  - HTTPS enabled
  - Auto-deploys on updates
```

---

## 🎓 Understanding the Components

### 1. GitHub Actions (Cloud Docker Builder)

**What it is:** GitHub's CI/CD platform that runs automated workflows.

**How we use it:**
- GitHub provides Ubuntu virtual machines
- Docker is pre-installed on these VMs
- Your Dockerfile runs on their infrastructure
- Result: Built Docker image without using your resources

**Cost:** Free for public repositories, generous free tier for private repos.

**Your Workflow File:** `.github/workflows/docker-build.yml`

```yaml
name: Docker Build CI

on: [push]  # Triggers when you push code

jobs:
  docker-build:
    runs-on: ubuntu-latest  # GitHub gives you an Ubuntu machine
    
    steps:
    - uses: actions/checkout@v3  # Gets your code
    - uses: docker/setup-buildx-action@v2  # Sets up Docker
    - uses: docker/build-push-action@v4  # Builds image
      with:
        push: false  # Just build, don't upload yet
```

### 2. Railway (Cloud Hosting Platform)

**What it is:** Platform-as-a-Service (PaaS) that runs your applications.

**How we use it:**
- Connects to your GitHub repository
- Automatically pulls latest code
- Builds and deploys your Docker container
- Provides public HTTPS URL

**Cost:** $5/month credit (enough for hobby projects).

**Configuration File:** `railway.json`

```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app.fastapi_app:app --host 0.0.0.0 --port $PORT"
  }
}
```

### 3. Dockerfile (Container Blueprint)

**What it is:** Instructions for building your Docker image.

**Our Multi-Stage Design:**

```dockerfile
# Stage 1: Builder (heavy lifting)
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2: Production (lightweight final image)
FROM python:3.10-slim as production
WORKDIR /app
COPY --from=builder /wheels /wheels  # Reuse wheels from Stage 1
RUN pip install --no-cache-dir /wheels/*
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why Multi-Stage?**
- Stage 1 installs build tools and dependencies
- Stage 2 only includes what's needed to run
- Result: ~400MB instead of ~1.2GB!

---

## 📋 Detailed Step-by-Step Guide

### Phase 1: Prepare Your Code

#### Step 1: Verify All Files Exist

```powershell
# Check file structure
tree /F

# Should see:
# ├─ Dockerfile
# ├─ requirements.txt
# ├─ railway.json
# └─ .github/workflows/docker-build.yml
```

#### Step 2: Test Locally First

```powershell
# Make sure your app works locally
python src\generate_data.py
python src\data_preprocessing.py
python src\train.py

# Test FastAPI
uvicorn app.fastapi_app:app --reload
# Visit: http://localhost:8000/health
```

---

### Phase 2: Set Up GitHub Repository

#### Step 3: Create GitHub Account

If you don't have one:
1. Go to https://github.com/signup
2. Sign up (free)
3. Verify email

#### Step 4: Create New Repository

1. Click "+" → "New repository"
2. Name: `student-placement-mlops`
3. Description: "MLOps system with GitHub Actions Docker builds"
4. Visibility: **Public** (for unlimited free Actions)
5. **Don't** initialize with README (you already have code)
6. Click "Create repository"

#### Step 5: Initialize Git Locally

```powershell
cd D:\Mlops-final

# Initialize Git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: MLOps with cloud Docker builds"

# Link to GitHub
git remote add origin https://github.com/YOUR_USERNAME/student-placement-mlops.git

# Rename branch
git branch -M main

# Push to GitHub
git push -u origin main
```

**Enter GitHub credentials** when prompted.

#### Step 6: Verify Push Success

Visit: https://github.com/YOUR_USERNAME/student-placement-mlops

You should see all your files!

---

### Phase 3: GitHub Actions Cloud Build

#### Step 7: Watch the Magic Happen

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. You'll see: "Docker Build CI workflow running"

**What's happening:**
```
🔄 Docker Build CI #1 is running...

✅ Set up Docker Buildx (2 seconds)
✅ Checkout code (1 second)
⏳ Build Docker image (3-5 minutes)
⏸️ Verify Docker build
```

#### Step 8: Inspect Build Logs

Click on the running workflow → Click on "Build Docker image" step

You'll see real-time output:
```
#1 [internal] load build definition from Dockerfile
#1 DONE 0.1s

#2 [internal] load .dockerignore
#2 DONE 0.0s

#3 [builder 1/6] FROM python:3.10-slim
#3 DONE 2.5s

#4 [builder 2/6] WORKDIR /app
#4 DONE 0.1s

...

#15 exporting to image
#15 DONE 0.5s
```

#### Step 9: Success! ✅

When complete, you'll see:
```
✅ Docker Build CI #1
All jobs succeeded
```

**Congratulations!** Your Docker image was built in the cloud without Docker on your machine! 🎉

---

### Phase 4: Deploy to Railway

#### Step 10: Create Railway Account

1. Go to https://railway.app/
2. Click **"Login"**
3. **"Sign in with GitHub"** (easiest)
4. Authorize Railway
5. Complete profile

#### Step 11: Deploy Your Project

**Method A: One-Click Deploy**

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `student-placement-mlops`
4. Railway auto-detects Dockerfile
5. Click **"Deploy Now"**

**Method B: Manual Setup**

1. **"New Project"** → **"Empty Project"**
2. Name: "Student Placement API"
3. **"+"** → **"GitHub Repo"**
4. Select repository
5. Under **"Settings"**:
   - Start Command: `uvicorn app.fastapi_app:app --host 0.0.0.0 --port $PORT`
   - DockerfilePath: `./Dockerfile`

#### Step 12: Configure Environment Variables

In Railway dashboard:

1. Click your project
2. **"Variables"** tab
3. Add:

| Variable | Value |
|----------|-------|
| `FASTAPI_ENV` | `production` |
| `MLFLOW_TRACKING_URI` | `file:/app/mlruns` |
| `PORT` | `8000` |

4. Click **"Add"** for each

#### Step 13: Deploy!

1. Go to **"Deployments"** tab
2. Railway starts building automatically
3. Wait 2-3 minutes
4. Status changes to **"Deployed"** ✅

#### Step 14: Get Your Public URL

1. **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**
4. Copy URL: `https://student-placement-api-production.up.railway.app`

**Test it:**
```powershell
curl https://your-project.up.railway.app/health
```

**Open in browser:**
```
https://your-project.up.railway.app/docs
```

---

## 🔄 Automatic Updates (CI/CD)

Now every time you push to GitHub:

```powershell
# Make changes
git add .
git commit -m "Improved model accuracy"
git push origin main
```

**Automatic sequence:**
1. ✅ GitHub detects push
2. ✅ GitHub Actions builds new Docker image
3. ✅ Railway detects new image
4. ✅ Railway redeploys automatically
5. ✅ Your updates go live in 3-5 minutes!

**No manual deployment needed!**

---

## 💰 Cost Breakdown

### GitHub Actions (Cloud Docker)

**Free Tier:**
- Public repos: Unlimited free minutes
- Private repos: 2,000 minutes/month
- More than enough for this project!

**Your Usage:**
- Each build: ~5 minutes
- Daily builds: 150 minutes/month
- Well within free limits! ✅

### Railway (Hosting)

**Free Trial:**
- $5 credit/month
- No credit card initially required

**Typical Usage:**
- Small API: ~$2-3/month
- Leaves credits for other projects

**Total Monthly Cost:** $0-5 (mostly free!)

---

## 🆘 Troubleshooting

### Problem: "Docker build failed"

**Check logs in GitHub Actions:**
```
# Look for error messages like:
ERROR: failed to solve: failed to compute cache key
```

**Common causes:**
- Missing `requirements.txt`
- Syntax error in Dockerfile
- File paths incorrect

**Solution:**
1. Click failed workflow in Actions tab
2. Read error message carefully
3. Fix the issue locally
4. Commit and push again
5. GitHub Actions will retry automatically

### Problem: "Railway deployment failed"

**Check Railway logs:**
1. Click your project
2. "Deployments" tab
3. Click failed deployment
4. View logs

**Common issues:**
- Wrong start command
- Missing environment variables
- Port mismatch

**Solution:**
- Verify `railway.json` has correct start command
- Add all required environment variables
- Ensure PORT=8000

### Problem: "Can't access deployed API"

**Check:**
1. Is deployment status "Deployed"?
2. Are you using HTTPS (not HTTP)?
3. Did you generate the domain in Settings?

**Debug:**
```powershell
# Health check
curl https://your-project.up.railway.app/health

# If fails, check Railway logs for errors
```

---

## ✅ Verification Checklist

After completing setup:

### GitHub Actions
- [ ] Repository created on GitHub
- [ ] Code pushed successfully
- [ ] Actions tab shows green checkmark
- [ ] Docker build completed
- [ ] Can view build logs

### Railway Deployment
- [ ] Railway account created
- [ ] Project connected to GitHub
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Public URL generated
- [ ] Health endpoint responds
- [ ] API docs accessible

### Overall
- [ ] Can access API via public URL
- [ ] Predictions work remotely
- [ ] Automatic redeployment on push
- [ ] No Docker installed locally ✅

---

## 🎓 What You've Learned

By setting up this way, you now understand:

1. ✅ **GitHub Actions** - Cloud-based CI/CD automation
2. ✅ **Docker in Cloud** - Build without local installation
3. ✅ **Railway** - Modern PaaS for deployment
4. ✅ **Automatic Deployments** - GitOps workflow
5. ✅ **Cost Optimization** - Free tier usage
6. ✅ **Production Deployment** - Real-world practices

---

## 📚 Additional Resources

### Official Documentation
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Railway Documentation](https://docs.railway.app/)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

### Tutorials
- [GitHub Actions for Beginners](https://github.com/sdras/awesome-actions)
- [Railway Quickstart](https://docs.railway.app/quickstart/)
- [Deploy FastAPI to Railway](https://www.railway.app/templates/fastapi)

### Community Support
- [GitHub Community](https://github.community/)
- [Railway Discord](https://discord.gg/railway)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/github-actions)

---

## 🎉 Success Summary

You now have:

✅ **Cloud Docker Builds** - No local installation needed  
✅ **Automatic CI/CD** - Push to deploy workflow  
✅ **Live API** - Accessible worldwide  
✅ **Production Infrastructure** - Professional setup  
✅ **Cost Effective** - Mostly free  
✅ **Scalable** - Easy to upgrade  

**Total Disk Space Used:** <100MB (vs 5GB+ for Docker Desktop)  
**Setup Time:** ~15 minutes  
**Monthly Cost:** $0-5  

---

## 🚀 Next Steps

1. **Share your API** with friends/colleagues
2. **Integrate** with frontend applications
3. **Monitor** usage and performance
4. **Iterate** on your ML model
5. **Learn more** about cloud deployment patterns

**Your journey to cloud-native MLOps starts here!** 🌟

---

**Questions?** Check the detailed guides:
- [`GITHUB_ACTIONS_DOCKER_GUIDE.md`](./GITHUB_ACTIONS_DOCKER_GUIDE.md)
- [`RAILWAY_DEPLOYMENT_GUIDE.md`](./RAILWAY_DEPLOYMENT_GUIDE.md)

**Created:** March 14, 2026  
**Difficulty:** Beginner-Friendly ⭐⭐⭐⭐⭐  
**Prerequisites:** Basic Git knowledge
