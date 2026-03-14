# 🐳 Docker Setup Guide for MLOps System

Complete guide to configure and run your Student Placement Prediction MLOps System with Docker.

---

## 📋 Prerequisites

- Windows 10/11 (64-bit)
- 4GB RAM minimum (8GB recommended)
- 5GB free disk space
- Administrator access for installation
- Virtualization enabled in BIOS

---

## 🚀 Step 1: Install Docker Desktop

### Download Options

**Option A: Direct Download (Fastest)**
```
https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
```

**Option B: Official Website**
1. Visit: https://www.docker.com/products/docker-desktop/
2. Click "Download for Windows"
3. Run the downloaded installer

### Installation Process

1. **Run Installer**
   - Double-click `Docker Desktop Installer.exe`
   - Click "Yes" to allow changes

2. **Choose Configuration**
   - ✅ Select "Use WSL 2 instead of Hyper-V" (recommended)
   - Choose installation path (default: `C:\Program Files\Docker`)
   - Click "OK"

3. **Wait for Installation**
   - Downloads necessary components (~500MB)
   - Installs Docker Desktop
   - Installs WSL 2 kernel if needed
   - Time: 5-15 minutes depending on internet

4. **Complete Installation**
   - Click "Close and Restart" when prompted
   - System will restart automatically

5. **Launch Docker Desktop**
   - After restart, Docker Desktop launches automatically
   - Wait for whale icon in system tray to stop spinning 🐳
   - Status should show: "Docker Desktop is running"

---

## ✅ Step 2: Verify Docker Installation

Open PowerShell and run:

```powershell
# Check Docker version
docker --version

# Expected output: Docker version 24.x.x

# Check Docker Compose version
docker compose version

# Expected output: Docker Compose version v2.x.x

# Check Docker daemon is running
docker info

# Expected: Client and Server information displayed

# Test Docker with hello-world
docker run hello-world

# Expected: "Hello from Docker!" message
```

If all commands work, Docker is successfully installed! ✅

---

## 🔧 Step 3: Configure Docker for MLOps Project

Your project already has all Docker configuration files ready:

### Configuration Files Overview

1. **Dockerfile** - Builds FastAPI container
2. **Dockerfile.streamlit** - Builds Streamlit container
3. **docker-compose.yml** - Orchestrates all services
4. **.dockerignore** - Excludes unnecessary files

### What's Configured

✅ **Multi-stage build** for optimized image size  
✅ **Health checks** for service monitoring  
✅ **Volume mounting** for data persistence  
✅ **Network isolation** for security  
✅ **Environment variables** for configuration  
✅ **Port mapping** for service access  

---

## 🎯 Step 4: Start All Services with Docker

### Option A: Using Batch File (Easiest)

```powershell
# Navigate to project directory
cd D:\Mlops-final

# Run the startup script
.\start-docker.bat
```

### Option B: Manual Commands

```powershell
# Navigate to project
cd D:\Mlops-final

# Build all containers
docker compose build

# Start all services
docker compose up -d

# Or start with MLflow included
docker compose --profile full up -d
```

### Option C: One-Line Command

```powershell
docker compose up --build -d
```

---

## 📊 Step 5: Verify Services Are Running

### Check Container Status

```powershell
# List all running containers
docker compose ps

# Expected output:
# NAME              STATUS    PORTS
# placement-api     Up        0.0.0.0:8000->8000/tcp
# placement-ui      Up        0.0.0.0:8501->8501/tcp
```

### View Service Logs

```powershell
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs fastapi
docker compose logs streamlit
docker compose logs mlflow
```

### Test Each Service

**1. FastAPI Backend**
```powershell
# Health check
curl http://localhost:8000/health

# Expected: {"status":"healthy","model_loaded":true,"version":"1.0.0"}

# API Documentation
Start-Process "http://localhost:8000/docs"
```

**2. Streamlit UI**
```powershell
# Open in browser
Start-Process "http://localhost:8501"
```

**3. MLflow Tracking**
```powershell
# Open in browser (with profile)
Start-Process "http://localhost:5000"
```

---

## 🔍 Step 6: Access Your Services

Once running, access your services at:

| Service | URL | Purpose |
|---------|-----|---------|
| **FastAPI** | http://localhost:8000 | REST API backend |
| **FastAPI Docs** | http://localhost:8000/docs | Interactive API docs |
| **FastAPI Health** | http://localhost:8000/health | Health check endpoint |
| **Streamlit** | http://localhost:8501 | User interface |
| **MLflow** | http://localhost:5000 | Experiment tracking |

---

## 🛠️ Step 7: Common Docker Commands

### Managing Containers

```powershell
# Start services
docker compose up -d

# Stop services
docker compose down

# Restart services
docker compose restart

# View running containers
docker compose ps

# View logs
docker compose logs -f

# Rebuild containers
docker compose build

# Force rebuild without cache
docker compose build --no-cache
```

### Cleaning Up

```powershell
# Stop and remove all containers
docker compose down -v

# Remove dangling images
docker image prune -a

# Remove all stopped containers
docker container prune
```

### Inside Containers

```powershell
# Execute command inside container
docker compose exec fastapi bash

# View container environment
docker compose exec fastapi env

# Check disk usage inside container
docker compose exec fastapi df -h
```

---

## 📦 Docker Architecture

### Services Running

```
┌─────────────────────────────────────┐
│     Docker Network (mlops-network)  │
│                                     │
│  ┌──────────────┐  ┌──────────────┐│
│  │  FastAPI     │  │  Streamlit   ││
│  │  Container   │  │  Container   ││
│  │  Port: 8000  │  │  Port: 8501  ││
│  └──────┬───────┘  └──────┬───────┘│
│         │                 │         │
│         └────────┬────────┘         │
│                  │                  │
│         ┌────────▼────────┐         │
│         │  Shared Volumes │         │
│         │  - mlruns/      │         │
│         │  - models/      │         │
│         │  - data/        │         │
│         └─────────────────┘         │
└─────────────────────────────────────┘
```

### Volume Mapping

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./mlruns` | `/app/mlruns` | MLflow tracking data |
| `./models` | `/app/models` | Trained models |
| `./data` | `/app/data` | Dataset storage |

---

## ⚙️ Configuration Options

### Environment Variables

Set in `docker-compose.yml`:

```yaml
environment:
  - FASTAPI_ENV=production      # Production mode
  - MLFLOW_TRACKING_URI=file:/app/mlruns  # MLflow location
  - FASTAPI_URL=http://fastapi:8000       # API URL for Streamlit
```

### Resource Limits (Optional)

Add to `docker-compose.yml` to limit resource usage:

```yaml
services:
  fastapi:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

---

## 🆘 Troubleshooting

### Issue 1: Docker Won't Start

**Solution:**
```powershell
# Check WSL status
wsl --list --verbose

# Update WSL
wsl --update

# Restart Docker Desktop
# Stop Docker Desktop from system tray
# Start Docker Desktop again
```

### Issue 2: Port Already in Use

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Issue 3: Containers Keep Restarting

**Check logs:**
```powershell
docker compose logs fastapi
```

**Common fixes:**
```powershell
# Rebuild without cache
docker compose build --no-cache

# Remove volumes and restart
docker compose down -v
docker compose up -d
```

### Issue 4: Can't Access Services

**Check firewall:**
```powershell
# Allow Docker through Windows Firewall
# Windows Security → Firewall → Allow an app → Docker Desktop
```

**Check network:**
```powershell
# Verify containers are on same network
docker network inspect mlops-network
```

---

## 🎯 Best Practices

### 1. Regular Cleanup

```powershell
# Weekly cleanup
docker compose down -v
docker system prune -a
```

### 2. Backup Data

```powershell
# Backup MLflow data
docker run --rm -v ${PWD}/mlruns:/backup alpine tar czf backup.tar.gz /app/mlruns
```

### 3. Update Images

```powershell
# Pull latest base images
docker compose pull

# Rebuild containers
docker compose up -d --build
```

### 4. Monitor Resources

```powershell
# View resource usage
docker stats

# Check disk usage
docker system df
```

---

## 📈 Performance Optimization

### Reduce Image Size

Your Dockerfile already uses multi-stage build which reduces size by ~60%.

### Speed Up Builds

```powershell
# Use build cache
docker compose build --parallel

# Or use buildx for faster builds
docker buildx build --platform linux/amd64 -t placement-api .
```

### Optimize Volumes

Use named volumes for better performance:

```yaml
volumes:
  mlruns_data:
  models_data:
  data_raw:
```

---

## 🚀 Next Steps After Docker Setup

### 1. Run the ML Pipeline

```powershell
# Execute pipeline inside container
docker compose exec fastapi python src/generate_data.py
docker compose exec fastapi python src/data_preprocessing.py
docker compose exec fastapi python src/train.py
docker compose exec fastapi python src/evaluate.py
```

### 2. Access MLflow UI

```powershell
# Start MLflow service
docker compose --profile full up -d

# Access at http://localhost:5000
```

### 3. Deploy to Production

```powershell
# Build production images
docker compose -f docker-compose.prod.yml build

# Deploy
docker compose -f docker-compose.prod.yml up -d
```

---

## ✅ Verification Checklist

After Docker setup, verify:

- [ ] Docker Desktop is running (whale icon stationary)
- [ ] `docker --version` works
- [ ] `docker compose version` works
- [ ] `docker run hello-world` succeeds
- [ ] `docker compose up -d` starts all services
- [ ] `docker compose ps` shows running containers
- [ ] http://localhost:8000/health responds
- [ ] http://localhost:8501 loads Streamlit UI
- [ ] http://localhost:5000 loads MLflow UI (with profile)
- [ ] Logs accessible via `docker compose logs`
- [ ] Volumes persist data correctly

---

## 📞 Support Resources

- **Docker Docs:** https://docs.docker.com/
- **Docker Desktop:** https://docs.docker.com/desktop/
- **Compose Reference:** https://docs.docker.com/compose/
- **Project Issues:** Create GitHub issue

---

## 🎉 Success!

Once Docker is configured and services are running, you have:

✅ **Production-ready containerized deployment**  
✅ **Isolated, reproducible environment**  
✅ **Easy scaling and updates**  
✅ **Professional MLOps infrastructure**  
✅ **All services running in harmony**  

**Your complete MLOps stack is now containerized!** 🐳🚀

---

**Last Updated:** March 14, 2026  
**Docker Version:** 24.x+  
**Compose Version:** v2.x+
