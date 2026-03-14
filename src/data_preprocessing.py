"""
Data Preprocessing Module
Handles data loading, cleaning, and train-test splitting
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import yaml
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))
from config import Config


def load_data(data_path: Path) -> pd.DataFrame:
    """
    Load dataset from CSV file.
    
    Parameters:
    -----------
    data_path : Path
        Path to the raw data file
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataset
    """
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape}")
    return df


def preprocess_data(df: pd.DataFrame, config: Config) -> tuple:
    """
    Preprocess the data: handle missing values, scale features, split data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw dataset
    config : Config
        Configuration object
    
    Returns:
    --------
    tuple
        (X_train, X_test, y_train, y_test, scaler)
    """
    print("Preprocessing data...")
    
    # Separate features and target
    X = df[config.FEATURE_COLUMNS].copy()
    y = df[config.TARGET_COLUMN].copy()
    
    # Handle missing values (if any)
    if X.isnull().sum().sum() > 0:
        print("Handling missing values...")
        X = X.fillna(X.median(numeric_only=True))
    
    # Scale features
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    print(f"Splitting data (test_size={config.TEST_SIZE})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=y  # Maintain class distribution
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test, scaler


def save_processed_data(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: pd.Series,
    y_test: pd.Series,
    scaler: StandardScaler,
    output_dir: Path
):
    """
    Save processed data and scaler.
    
    Parameters:
    -----------
    X_train, X_test : np.ndarray
        Scaled feature arrays
    y_train, y_test : pd.Series
        Target arrays
    scaler : StandardScaler
        Fitted scaler
    output_dir : Path
        Output directory
    """
    print(f"Saving processed data to {output_dir}...")
    
    # Create DataFrames
    train_df = pd.DataFrame(X_train, columns=Config.FEATURE_COLUMNS)
    train_df[Config.TARGET_COLUMN] = y_train.values
    
    test_df = pd.DataFrame(X_test, columns=Config.FEATURE_COLUMNS)
    test_df[Config.TARGET_COLUMN] = y_test.values
    
    # Save datasets
    train_df.to_csv(output_dir / "train.csv", index=False)
    test_df.to_csv(output_dir / "test.csv", index=False)
    
    # Save scaler
    joblib.dump(scaler, output_dir / "scaler.pkl")
    
    print("Processed data saved successfully!")


def main():
    """Main preprocessing pipeline."""
    print("=" * 60)
    print("DATA PREPROCESSING PIPELINE")
    print("=" * 60)
    
    # Initialize config
    config = Config()
    config.create_directories()
    
    # Load parameters
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    
    # Update config with parameters if needed
    config.TEST_SIZE = params['data']['test_size']
    config.RANDOM_STATE = params['data']['random_state']
    
    # Load data
    df = load_data(config.RAW_DATA_PATH)
    
    # Check for required columns
    required_columns = config.FEATURE_COLUMNS + [config.TARGET_COLUMN]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Preprocess data
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df, config)
    
    # Save processed data
    save_processed_data(
        X_train, X_test, y_train, y_test, scaler,
        config.PROCESSED_DATA_PATH
    )
    
    print("=" * 60)
    print("PREPROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
