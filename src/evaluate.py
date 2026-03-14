"""
Model Evaluation Script
Evaluates the trained model on test data and generates comprehensive metrics
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
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


def load_test_data(config: Config) -> tuple:
    """
    Load processed test data.
    
    Parameters:
    -----------
    config : Config
        Configuration object
    
    Returns:
    --------
    tuple
        (X_test, y_test)
    """
    print("Loading processed test data...")
    test_df = pd.read_csv(config.PROCESSED_DATA_PATH / "test.csv")
    
    X_test = test_df[config.FEATURE_COLUMNS].values
    y_test = test_df[config.TARGET_COLUMN].values
    
    print(f"Test data shape: {X_test.shape}")
    return X_test, y_test


def load_model(model_path: Path):
    """
    Load trained model.
    
    Parameters:
    -----------
    model_path : Path
        Path to the saved model
    
    Returns:
    --------
    Trained model
    """
    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    return model


def load_model_from_mlflow(model_name: str, tracking_uri: str = "mlruns"):
    """
    Load model from MLflow registry.
    
    Parameters:
    -----------
    model_name : str
        Name of the model in MLflow
    tracking_uri : str
        MLflow tracking URI
    
    Returns:
    --------
    Trained model
    """
    print(f"Loading model '{model_name}' from MLflow...")
    
    if tracking_uri == "mlruns":
        mlflow.set_tracking_uri("file:./mlruns")
    else:
        mlflow.set_tracking_uri(tracking_uri)
    
    model_uri = f"models:/{model_name}/latest"
    model = mlflow.sklearn.load_model(model_uri)
    print("Model loaded from MLflow!")
    
    return model


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    """
    Comprehensive model evaluation.
    
    Parameters:
    -----------
    model : Trained model
        X_test : np.ndarray
            Test features
        y_test : np.ndarray
            Test target
    
    Returns:
    --------
    dict
        Dictionary of all evaluation metrics
    """
    print("Evaluating model on test data...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate basic metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }
    
    # Calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    metrics['confusion_matrix'] = {
        'true_negative': int(cm[0][0]),
        'false_positive': int(cm[0][1]),
        'false_negative': int(cm[1][0]),
        'true_positive': int(cm[1][1])
    }
    
    # Print results
    print("\n" + "=" * 60)
    print("MODEL EVALUATION RESULTS")
    print("=" * 60)
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1_score']:.4f}")
    print(f"ROC-AUC:   {metrics['roc_auc']:.4f}")
    print("\nConfusion Matrix:")
    print(f"  TN: {metrics['confusion_matrix']['true_negative']}  FP: {metrics['confusion_matrix']['false_positive']}")
    print(f"  FN: {metrics['confusion_matrix']['false_negative']}  TP: {metrics['confusion_matrix']['true_positive']}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("=" * 60)
    
    return metrics


def log_evaluation_to_mlflow(metrics: dict, params: dict):
    """
    Log evaluation metrics to MLflow.
    
    Parameters:
    -----------
    metrics : dict
        Evaluation metrics
    params : dict
        Project parameters
    """
    print("Logging evaluation metrics to MLflow...")
    
    experiment_name = params['mlflow']['experiment_name']
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run(nested=True):
        # Log metrics
        mlflow.log_metric("test_accuracy", metrics['accuracy'])
        mlflow.log_metric("test_precision", metrics['precision'])
        mlflow.log_metric("test_recall", metrics['recall'])
        mlflow.log_metric("test_f1_score", metrics['f1_score'])
        mlflow.log_metric("test_roc_auc", metrics['roc_auc'])
        
        # Log confusion matrix as parameters
        mlflow.log_param("test_tn", metrics['confusion_matrix']['true_negative'])
        mlflow.log_param("test_fp", metrics['confusion_matrix']['false_positive'])
        mlflow.log_param("test_fn", metrics['confusion_matrix']['false_negative'])
        mlflow.log_param("test_tp", metrics['confusion_matrix']['true_positive'])
        
        run_id = mlflow.active_run().info.run_id
        print(f"Evaluation logged to MLflow (Run ID: {run_id})")


def save_evaluation_results(metrics: dict, output_path: Path):
    """
    Save evaluation results to JSON file.
    
    Parameters:
    -----------
    metrics : dict
        Evaluation metrics
    output_path : Path
        Output file path
    """
    # Prepare JSON-serializable metrics
    output_metrics = {
        'accuracy': float(metrics['accuracy']),
        'precision': float(metrics['precision']),
        'recall': float(metrics['recall']),
        'f1_score': float(metrics['f1_score']),
        'roc_auc': float(metrics['roc_auc']),
        'confusion_matrix': metrics['confusion_matrix']
    }
    
    with open(output_path, 'w') as f:
        json.dump(output_metrics, f, indent=2)
    
    print(f"Evaluation results saved to {output_path}")


def main():
    """Main evaluation pipeline."""
    print("=" * 60)
    print("MODEL EVALUATION PIPELINE")
    print("=" * 60)
    
    # Initialize config
    config = Config()
    
    # Load parameters
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    
    # Load test data
    X_test, y_test = load_test_data(config)
    
    # Try loading from MLflow first, fallback to local file
    try:
        model = load_model_from_mlflow(
            model_name=params['mlflow']['model_name'],
            tracking_uri=params['mlflow']['tracking_uri']
        )
    except Exception as e:
        print(f"MLflow load failed: {e}")
        print("Falling back to local model...")
        model = load_model(config.MODELS_DIR / "placement_model.pkl")
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    
    # Log to MLflow
    log_evaluation_to_mlflow(metrics, params)
    
    # Save results locally
    save_evaluation_results(metrics, Path('evaluation_results.json'))
    
    print("=" * 60)
    print("EVALUATION COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    return metrics


if __name__ == "__main__":
    metrics = main()
