"""
Configuration file for the MLOps project
Centralizes all paths and settings
"""

from pathlib import Path


class Config:
    """Configuration class with project settings."""
    
    # Project root directory
    PROJECT_ROOT = Path(__file__).parent.parent
    
    # Data paths
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_PATH = DATA_DIR / "raw" / "placement_data.csv"
    PROCESSED_DATA_PATH = DATA_DIR / "processed"
    
    # Model paths
    MODELS_DIR = PROJECT_ROOT / "models"
    
    # MLflow settings
    MLFLOW_EXPERIMENT_NAME = "student_placement_prediction"
    MLFLOW_MODEL_NAME = "placement_classifier"
    MLFLOW_TRACKING_URI = "mlruns"
    
    # Data processing settings
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    # Feature columns
    FEATURE_COLUMNS = [
        'CGPA',
        'Internships',
        'Projects',
        'Coding_Skills_Score',
        'Communication_Skills_Score'
    ]
    
    TARGET_COLUMN = 'Placement_Status'
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
        cls.MODELS_DIR.mkdir(parents=True, exist_ok=True)
