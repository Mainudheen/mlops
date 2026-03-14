@echo off
echo ========================================
echo Starting MLOps System with Docker
echo ========================================
echo.

echo [1/4] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running!
    echo.
    echo Please install Docker Desktop from:
    echo https://desktop.docker.com/win/main/amd64/Docker%%20Desktop%%20Installer.exe
    echo.
    pause
    exit /b 1
)
echo Docker is ready!
echo.

echo [2/4] Building Docker images...
docker compose build

if %errorlevel% neq 0 (
    echo ERROR: Failed to build Docker images
    pause
    exit /b 1
)

echo.
echo [3/4] Starting services...
docker compose up -d

if %errorlevel% neq 0 (
    echo ERROR: Failed to start services
    pause
    exit /b 1
)

echo.
echo [4/4] Waiting for services to be ready...
timeout /t 15 /nobreak

echo.
echo ========================================
echo Services Started Successfully!
echo ========================================
echo.
echo FastAPI API: http://localhost:8000
echo Streamlit UI: http://localhost:8501
echo MLflow UI: http://localhost:5000 (run separately)
echo.
echo API Health: http://localhost:8000/health
echo API Docs: http://localhost:8000/docs
echo.
echo To view logs: docker compose logs -f
echo To stop: docker compose down
echo ========================================
echo.
echo Opening services in browser...
timeout /t 3 /nobreak
start http://localhost:8000/health
timeout /t 2 /nobreak
start http://localhost:8501

pause
