"""
Unit Tests for MLOps Pipeline
Tests data preprocessing, model training, and API endpoints
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.generate_data import generate_placement_data
from src.data_preprocessing import load_data, preprocess_data
from sklearn.linear_model import LogisticRegression


class TestConfig:
    """Test configuration module."""
    
    def test_config_initialization(self):
        """Test config object creation."""
        config = Config()
        assert config is not None
        assert hasattr(config, 'FEATURE_COLUMNS')
        assert hasattr(config, 'TARGET_COLUMN')
    
    def test_feature_columns(self):
        """Test feature columns are defined correctly."""
        config = Config()
        expected_features = [
            'CGPA',
            'Internships',
            'Projects',
            'Coding_Skills_Score',
            'Communication_Skills_Score'
        ]
        assert config.FEATURE_COLUMNS == expected_features
    
    def test_target_column(self):
        """Test target column is defined correctly."""
        config = Config()
        assert config.TARGET_COLUMN == 'Placement_Status'


class TestDataGeneration:
    """Test data generation module."""
    
    def test_generate_data_shape(self):
        """Test generated data has correct shape."""
        df = generate_placement_data(n_samples=100, random_state=42)
        assert df.shape[0] == 100
        assert df.shape[1] == 6  # 5 features + 1 target
    
    def test_generate_data_columns(self):
        """Test generated data has correct columns."""
        df = generate_placement_data(n_samples=100, random_state=42)
        expected_columns = [
            'CGPA', 'Internships', 'Projects',
            'Coding_Skills_Score', 'Communication_Skills_Score',
            'Placement_Status'
        ]
        assert list(df.columns) == expected_columns
    
    def test_cgpa_range(self):
        """Test CGPA is within valid range."""
        df = generate_placement_data(n_samples=1000, random_state=42)
        assert df['CGPA'].min() >= 0
        assert df['CGPA'].max() <= 10
    
    def test_internships_range(self):
        """Test internships count is within valid range."""
        df = generate_placement_data(n_samples=1000, random_state=42)
        assert df['Internships'].min() >= 0
        assert df['Internships'].max() <= 5
    
    def test_projects_range(self):
        """Test projects count is within valid range."""
        df = generate_placement_data(n_samples=1000, random_state=42)
        assert df['Projects'].min() >= 0
        assert df['Projects'].max() <= 10
    
    def test_skills_score_range(self):
        """Test skill scores are within valid range."""
        df = generate_placement_data(n_samples=1000, random_state=42)
        assert df['Coding_Skills_Score'].min() >= 0
        assert df['Coding_Skills_Score'].max() <= 100
        assert df['Communication_Skills_Score'].min() >= 0
        assert df['Communication_Skills_Score'].max() <= 100
    
    def test_placement_status_values(self):
        """Test placement status has binary values."""
        df = generate_placement_data(n_samples=1000, random_state=42)
        assert set(df['Placement_Status'].unique()).issubset({0, 1})
    
    def test_reproducibility(self):
        """Test data generation is reproducible."""
        df1 = generate_placement_data(n_samples=100, random_state=42)
        df2 = generate_placement_data(n_samples=100, random_state=42)
        pd.testing.assert_frame_equal(df1, df2)


class TestDataPreprocessing:
    """Test data preprocessing module."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return generate_placement_data(n_samples=100, random_state=42)
    
    def test_preprocess_data_output_length(self, sample_data):
        """Test preprocessed data splits correctly."""
        config = Config()
        X_train, X_test, y_train, y_test, scaler = preprocess_data(sample_data, config)
        
        total_samples = len(X_train) + len(X_test)
        assert total_samples == len(sample_data)
    
    def test_train_test_split_ratio(self, sample_data):
        """Test train-test split ratio."""
        config = Config()
        X_train, X_test, y_train, y_test, scaler = preprocess_data(sample_data, config)
        
        train_ratio = len(X_train) / len(sample_data)
        assert abs(train_ratio - 0.8) < 0.05  # Allow small variance
    
    def test_scaler_fitted(self, sample_data):
        """Test scaler is properly fitted."""
        config = Config()
        X_train, X_test, y_train, y_test, scaler = preprocess_data(sample_data, config)
        
        assert hasattr(scaler, 'mean_')
        assert hasattr(scaler, 'scale_')
    
    def test_scaled_features_range(self, sample_data):
        """Test scaled features have reasonable range."""
        config = Config()
        X_train, X_test, y_train, y_test, scaler = preprocess_data(sample_data, config)
        
        # Scaled data should have mean close to 0 and std close to 1
        assert abs(X_train.mean()) < 1.0
        assert abs(X_train.std() - 1.0) < 0.5


class TestModelTraining:
    """Test model training functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        df = generate_placement_data(n_samples=200, random_state=42)
        config = Config()
        X_train, X_test, y_train, y_test, scaler = preprocess_data(df, config)
        return X_train, y_train
    
    def test_model_training(self, sample_data):
        """Test model can be trained."""
        X_train, y_train = sample_data
        
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
        
        assert hasattr(model, 'coef_')
        assert model.coef_.shape == (1, 5)  # 5 features
    
    def test_model_prediction(self, sample_data):
        """Test model can make predictions."""
        X_train, y_train = sample_data
        
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_train[:10])
        assert len(predictions) == 10
        assert all(p in [0, 1] for p in predictions)
    
    def test_model_probability(self, sample_data):
        """Test model can predict probabilities."""
        X_train, y_train = sample_data
        
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
        
        probas = model.predict_proba(X_train[:10])
        assert probas.shape == (10, 2)
        assert np.allclose(probas.sum(axis=1), 1.0)


class TestIntegration:
    """Integration tests for the full pipeline."""
    
    def test_end_to_end_pipeline(self):
        """Test complete pipeline from data generation to prediction."""
        # Generate data
        df = generate_placement_data(n_samples=200, random_state=42)
        
        # Preprocess
        config = Config()
        X_train, X_test, y_train, y_test, scaler = preprocess_data(df, config)
        
        # Train
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
        
        # Predict
        predictions = model.predict(X_test)
        
        # Validate
        assert len(predictions) == len(X_test)
        assert all(p in [0, 1] for p in predictions)
        
        # Calculate accuracy
        accuracy = (predictions == y_test).mean()
        assert accuracy > 0.5  # Better than random


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
