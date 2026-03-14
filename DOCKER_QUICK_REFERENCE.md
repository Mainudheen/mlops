# 🐳 Docker Quick Reference - MLOps System

Essential Docker commands for managing your Student Placement Prediction MLOps System.

---

## 🚀 Quick Start

### Install Docker (If Not Installed)
```powershell
# Download and install Docker Desktop
# https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
```

### Start All Services
```powershell
# Method 1: Use batch file (recommended)
.\start-docker.bat

# Method 2: Manual command
docker compose up --build -d

# Method 3: With MLflow included
docker compose --profile full up -d
```

---

## 📊 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| FastAPI | http://localhost:8000 | REST API backend |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/health | Service status |
| Streamlit | http://localhost:8501 | User interface |
| MLflow | http://localhost:5000 | Experiment tracking |

---

## 🔧 Essential Commands

### Build & Start
```powershell
# Build images
docker compose build

# Start services
docker compose up -d

# Build and start
docker compose up --build -d

# Start with MLflow
docker compose --profile full up -d
```

### Stop & Clean
```powershell
# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Stop, remove volumes, and remove images
docker compose down -v --rmi all
```

### Status & Logs
```powershell
# List containers
docker compose ps

# View logs
docker compose logs -f

# View specific service logs
docker compose logs fastapi
docker compose logs streamlit
docker compose logs mlflow
```

---

## 🛠️ Management Commands

### Restart Services
```powershell
# Restart all
docker compose restart

# Restart specific service
docker compose restart fastapi
```

### Rebuild & Update
```powershell
# Rebuild without cache
docker compose build --no-cache

# Pull latest images
docker compose pull

# Recreate containers
docker compose up -d --force-recreate
```

### Execute Inside Container
```powershell
# Open shell in FastAPI container
docker compose exec fastapi bash

# Run Python command
docker compose exec fastapi python --version

# List files
docker compose exec fastapi ls -la
```

---

## 📈 Monitoring Commands

### Resource Usage
```powershell
# View CPU/memory usage
docker stats

# View disk usage
docker system df

# View detailed info
docker system df -v
```

### Container Info
```powershell
# Show running processes
docker top placement-api

# Inspect container
docker inspect placement-api
```

---

## 🧹 Cleanup Commands

### Remove Unused Data
```powershell
# Remove dangling images
docker image prune

# Remove all unused data
docker system prune -a

# Remove stopped containers
docker container prune
```

### Reset Everything
```powershell
# Complete reset
docker compose down -v
docker system prune -a --volumes
```

---

## 🔍 Troubleshooting Commands

### Check Docker Status
```powershell
# Docker version
docker --version

# Compose version
docker compose version

# Docker info
docker info

# Test Docker
docker run hello-world
```

### Debug Issues
```powershell
# Check if services are running
docker compose ps

# View error logs
docker compose logs --tail=100

# Check network
docker network inspect mlops-network

# Check volume mounts
docker volume ls
```

### Force Refresh
```powershell
# Remove everything and rebuild
docker compose down -v
docker system prune -f
docker compose up --build -d
```

---

## 📦 Image Management

### List Images
```powershell
# List all images
docker images

# List project images
docker images | Select-String "placement"
```

### Tag & Push (for deployment)
```powershell
# Tag image
docker tag placement-api:latest your-username/placement-api:latest

# Push to registry
docker push your-username/placement-api:latest
```

### Save & Load
```powershell
# Save image to file
docker save -o placement-api.tar placement-api:latest

# Load from file
docker load -i placement-api.tar
```

---

## 🎯 Common Workflows

### Daily Development
```powershell
# Morning: Start services
docker compose up -d

# Work on code, then rebuild
docker compose build
docker compose up -d --force-recreate

# Evening: Stop services
docker compose down
```

### Deploy Update
```powershell
# Pull latest code
git pull

# Rebuild images
docker compose build --no-cache

# Deploy new containers
docker compose up -d --force-recreate

# Verify
docker compose ps
docker compose logs -f
```

### Complete Reset
```powershell
# Remove everything
docker compose down -v
docker system prune -a -f

# Clean project
Remove-Item -Recurse -Force .\mlruns\*
Remove-Item -Recurse -Force .\models\*

# Rebuild from scratch
docker compose up --build -d
```

---

## 🔐 Security Best Practices

### Don't Commit
- Never commit `.env` files with secrets
- Don't hardcode credentials in Dockerfile
- Use Docker secrets for sensitive data

### Scan Images
```powershell
# Scan for vulnerabilities (requires Docker Scout)
docker scout cve placement-api:latest
```

### Update Regularly
```powershell
# Update base images
docker pull python:3.10-slim
docker compose build --no-cache
```

---

## 📋 Health Checks

### Manual Health Check
```powershell
# FastAPI health
curl http://localhost:8000/health

# Streamlit (browser)
Start-Process "http://localhost:8501"

# MLflow (browser)
Start-Process "http://localhost:5000"
```

### Automated Monitoring
```powershell
# Continuous monitoring
while ($true) {
    docker compose ps
    Start-Sleep -Seconds 10
}
```

---

## 🆘 Emergency Commands

### Container Won't Start
```powershell
# Check logs
docker compose logs fastapi

# Inspect config
docker compose config

# Try interactive mode
docker compose up fastapi
```

### Port Conflicts
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Out of Disk Space
```powershell
# Clean Docker
docker system prune -a -f

# Remove old images
docker image prune -a -f

# Check size
docker system df
```

---

## 🎓 Learning Resources

- **Official Docs:** https://docs.docker.com/
- **Compose Reference:** https://docs.docker.com/compose/
- **Best Practices:** https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- **Troubleshooting:** https://docs.docker.com/desktop/troubleshoot/

---

**Quick Start Command:**
```powershell
.\start-docker.bat
```

This single command will check Docker, build images, start services, and open browsers! 🚀
