"""
Model Training Script with MLflow Integration
Trains a Logistic Regression model and logs to MLflow
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import mlflow
import mlflow.sklearn
from pathlib import Path
import yaml
import sys
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))
from config import Config


def load_processed_data(config: Config) -> tuple:
    """
    Load processed training data.
    
    Parameters:
    -----------
    config : Config
        Configuration object
    
    Returns:
    --------
    tuple
        (X_train, y_train)
    """
    print("Loading processed training data...")
    train_df = pd.read_csv(config.PROCESSED_DATA_PATH / "train.csv")
    
    X_train = train_df[config.FEATURE_COLUMNS].values
    y_train = train_df[config.TARGET_COLUMN].values
    
    print(f"Training data shape: {X_train.shape}")
    return X_train, y_train


def train_model(X_train: np.ndarray, y_train: np.ndarray, params: dict) -> LogisticRegression:
    """
    Train Logistic Regression model.
    
    Parameters:
    -----------
    X_train : np.ndarray
        Training features
    y_train : np.ndarray
        Training target
    params : dict
        Model hyperparameters
    
    Returns:
    --------
    LogisticRegression
        Trained model
    """
    print("Training Logistic Regression model...")
    
    model = LogisticRegression(
        random_state=params['model']['random_state'],
        max_iter=params['model']['max_iter']
    )
    
    model.fit(X_train, y_train)
    print("Model training completed!")
    
    return model


def evaluate_model(model: LogisticRegression, X_train: np.ndarray, y_train: np.ndarray) -> dict:
    """
    Evaluate model on training data.
    
    Parameters:
    -----------
    model : LogisticRegression
        Trained model
    X_train : np.ndarray
        Training features
    y_train : np.ndarray
        Training target
    
    Returns:
    --------
    dict
        Dictionary of metrics
    """
    print("Evaluating model on training data...")
    
    # Make predictions
    y_pred = model.predict(X_train)
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_train, y_pred),
        'precision': precision_score(y_train, y_pred),
        'recall': recall_score(y_train, y_pred),
        'f1_score': f1_score(y_train, y_pred)
    }
    
    print(f"Training Accuracy: {metrics['accuracy']:.4f}")
    print(f"Training Precision: {metrics['precision']:.4f}")
    print(f"Training Recall: {metrics['recall']:.4f}")
    print(f"Training F1 Score: {metrics['f1_score']:.4f}")
    
    return metrics


def setup_mlflow(config: Config, params: dict):
    """
    Setup MLflow tracking.
    
    Parameters:
    -----------
    config : Config
        Configuration object
    params : dict
        Project parameters
    """
    # Set tracking URI (local or Dagshub)
    tracking_uri = params['mlflow']['tracking_uri']
    
    if tracking_uri == "mlruns":
        # Local tracking
        mlflow.set_tracking_uri("file:./mlruns")
    else:
        # Dagshub or remote
        mlflow.set_tracking_uri(tracking_uri)
    
    # Set experiment
    experiment_name = params['mlflow']['experiment_name']
    mlflow.set_experiment(experiment_name)
    
    print(f"MLflow tracking URI: {mlflow.get_tracking_uri()}")
    print(f"Experiment: {experiment_name}")


def log_to_mlflow(model: LogisticRegression, metrics: dict, params: dict, config: Config):
    """
    Log model and metrics to MLflow.
    
    Parameters:
    -----------
    model : LogisticRegression
        Trained model
    metrics : dict
        Evaluation metrics
    params : dict
        Hyperparameters
    config : Config
        Configuration object
    """
    print("Logging to MLflow...")
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("model_type", params['model']['type'])
        mlflow.log_param("random_state", params['model']['random_state'])
        mlflow.log_param("max_iter", params['model']['max_iter'])
        mlflow.log_param("test_size", params['data']['test_size'])
        
        # Log metrics
        mlflow.log_metric("accuracy", metrics['accuracy'])
        mlflow.log_metric("precision", metrics['precision'])
        mlflow.log_metric("recall", metrics['recall'])
        mlflow.log_metric("f1_score", metrics['f1_score'])
        
        # Log model
        model_name = params['mlflow']['model_name']
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=model_name
        )
        
        run_id = mlflow.active_run().info.run_id
        print(f"MLflow Run ID: {run_id}")
        print(f"Model logged successfully!")
        
        # Save metrics to JSON for DVC
        metrics_output = {
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'f1_score': metrics['f1_score'],
            'run_id': run_id
        }
        
        with open('mlflow_metrics.json', 'w') as f:
            json.dump(metrics_output, f, indent=2)
    
    return run_id


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    # Initialize config
    config = Config()
    config.create_directories()
    
    # Load parameters
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    
    # Setup MLflow
    setup_mlflow(config, params)
    
    # Load data
    X_train, y_train = load_processed_data(config)
    
    # Train model
    model = train_model(X_train, y_train, params)
    
    # Evaluate model
    metrics = evaluate_model(model, X_train, y_train)
    
    # Log to MLflow
    run_id = log_to_mlflow(model, metrics, params, config)
    
    # Save model locally (for DVC)
    model_path = config.MODELS_DIR / "placement_model.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    print("=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    return model, metrics


if __name__ == "__main__":
    model, metrics = main()
