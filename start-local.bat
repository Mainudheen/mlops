@echo off
echo ========================================
echo Starting MLOps System (Local Mode)
echo ========================================
echo.

echo [1/4] Running ML Pipeline...
python src\generate_data.py
python src\data_preprocessing.py
python src\train.py
python src\evaluate.py

echo.
echo ========================================
echo Pipeline Complete!
echo ========================================
echo.
echo Now open 3 terminal windows:
echo.
echo Terminal 1 - FastAPI:
echo   uvicorn app.fastapi_app:app --reload --host 0.0.0.0 --port 8000
echo.
echo Terminal 2 - Streamlit:
echo   streamlit run app\streamlit_app.py
echo.
echo Terminal 3 - MLflow:
echo   mlflow ui --port 5000 --host 0.0.0.0
echo.
echo ========================================
echo Services:
echo   FastAPI: http://localhost:8000
echo   Streamlit: http://localhost:8501
echo   MLflow: http://localhost:5000
echo ========================================
echo.
pause
