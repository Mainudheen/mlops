"""
FastAPI Application for Student Placement Prediction
Provides REST API endpoints for model inference
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import mlflow
import mlflow.sklearn
from pathlib import Path
import yaml
from typing import Optional
import os

# Initialize FastAPI app
app = FastAPI(
    title="Student Placement Prediction API",
    description="Predict student placement based on skills and qualifications",
    version="1.0.0"
)


# Request/Response Models
class PredictionRequest(BaseModel):
    """Input features for prediction."""
    cgpa: float = Field(..., description="CGPA (0-10)", example=8.5)
    internships: int = Field(..., description="Number of internships (0-5)", example=3)
    projects: int = Field(..., description="Number of projects (0-10)", example=5)
    coding_skills_score: float = Field(..., description="Coding skills score (0-100)", example=75.0)
    communication_skills_score: float = Field(..., description="Communication skills score (0-100)", example=80.0)


class PredictionResponse(BaseModel):
    """Prediction output."""
    prediction: str
    probability: float
    confidence: str
    message: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    version: str


class ModelInfoResponse(BaseModel):
    """Model information response."""
    model_name: str
    version: str
    features: list
    mlflow_run_id: Optional[str] = None


# Global variables
model = None
scaler = None
config = None
params = None


def load_config():
    """Load configuration and parameters."""
    global config, params
    
    if params is None:
        with open('params.yaml', 'r') as f:
            params = yaml.safe_load(f)
    
    if config is None:
        from src.config import Config
        config = Config()


def load_model_from_mlflow():
    """Load model from MLflow registry."""
    global model, scaler
    
    load_config()
    
    try:
        # Set MLflow tracking URI
        tracking_uri = params['mlflow']['tracking_uri']
        if tracking_uri == "mlruns":
            mlflow.set_tracking_uri("file:./mlruns")
        else:
            mlflow.set_tracking_uri(tracking_uri)
        
        # Load model from registry
        model_name = params['mlflow']['model_name']
        model_uri = f"models:/{model_name}/latest"
        model = mlflow.sklearn.load_model(model_uri)
        
        # Try to load scaler
        scaler_path = config.PROCESSED_DATA_PATH / "scaler.pkl"
        if scaler_path.exists():
            scaler = joblib.load(scaler_path)
        
        print("Model loaded from MLflow successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading model from MLflow: {e}")
        return False


def load_model_local():
    """Load model from local file."""
    global model, scaler
    
    load_config()
    
    try:
        # Load model
        model_path = config.MODELS_DIR / "placement_model.pkl"
        model = joblib.load(model_path)
        
        # Load scaler
        scaler_path = config.PROCESSED_DATA_PATH / "scaler.pkl"
        if scaler_path.exists():
            scaler = joblib.load(scaler_path)
        
        print("Model loaded locally successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading local model: {e}")
        return False


def initialize_model():
    """Initialize model (try MLflow first, then local)."""
    global model
    
    if model is not None:
        return True
    
    # Try MLflow first
    if load_model_from_mlflow():
        return True
    
    # Fallback to local
    if load_model_local():
        return True
    
    return False


@app.on_event("startup")
async def startup_event():
    """Initialize model on startup."""
    print("Starting up FastAPI application...")
    initialize_model()
    print("Startup complete!")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns the current status of the API and model.
    """
    model_loaded = model is not None
    
    return HealthResponse(
        status="healthy",
        model_loaded=model_loaded,
        version="1.0.0"
    )


@app.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    """
    Get model information.
    Returns details about the loaded model.
    """
    load_config()
    
    run_id = None
    try:
        if params['mlflow']['tracking_uri'] == "mlruns":
            mlflow.set_tracking_uri("file:./mlruns")
        else:
            mlflow.set_tracking_uri(params['mlflow']['tracking_uri'])
        
        # Get latest run
        experiment = mlflow.get_experiment_by_name(params['mlflow']['experiment_name'])
        if experiment:
            runs = mlflow.search_runs(
                experiment_ids=[experiment.experiment_id],
                order_by=["start_time DESC"],
                max_results=1
            )
            if len(runs) > 0:
                run_id = runs.iloc[0]['run_id']
    except Exception as e:
        print(f"Error getting MLflow run info: {e}")
    
    return ModelInfoResponse(
        model_name=params['mlflow']['model_name'],
        version="1.0.0",
        features=config.FEATURE_COLUMNS,
        mlflow_run_id=run_id
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_placement(request: PredictionRequest):
    """
    Predict student placement.
    
    Takes student features and returns placement prediction with probability.
    """
    global model, scaler
    
    try:
        # Check if model is loaded
        if model is None:
            initialize_model()
            
            if model is None:
                raise HTTPException(
                    status_code=503,
                    detail="Model not loaded. Please check server logs."
                )
        
        # Prepare input features
        import numpy as np
        
        features = np.array([[
            request.cgpa,
            request.internships,
            request.projects,
            request.coding_skills_score,
            request.communication_skills_score
        ]])
        
        # Scale features if scaler is available
        if scaler is not None:
            features_scaled = scaler.transform(features)
        else:
            features_scaled = features
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        # Determine confidence level
        probability = float(prediction_proba[1] if prediction == 1 else prediction_proba[0])
        
        if probability >= 0.8:
            confidence = "High"
        elif probability >= 0.6:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        # Create response message
        placement_status = "Placed" if prediction == 1 else "Not Placed"
        message = f"Based on the provided features, the student is predicted to be {placement_status.lower()}."
        
        return PredictionResponse(
            prediction=placement_status,
            probability=round(probability, 4),
            confidence=confidence,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during prediction: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Student Placement Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "model_info": "/model-info",
            "predict": "/predict (POST)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
