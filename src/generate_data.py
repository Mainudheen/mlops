"""
Data Generation Script for Student Placement Prediction
Generates synthetic dataset with realistic distributions
"""

import pandas as pd
import numpy as np
from pathlib import Path


def generate_placement_data(n_samples=1000, random_state=42):
    """
    Generate synthetic student placement dataset.
    
    Parameters:
    -----------
    n_samples : int
        Number of samples to generate
    random_state : int
        Random seed for reproducibility
    
    Returns:
    --------
    pd.DataFrame
        Generated dataset
    """
    np.random.seed(random_state)
    
    # Generate features with realistic distributions
    cgpa = np.clip(np.random.normal(7.5, 1.2, n_samples), 0, 10)
    internships = np.random.poisson(2, n_samples)
    internships = np.clip(internships, 0, 5)
    
    projects = np.random.poisson(3, n_samples)
    projects = np.clip(projects, 0, 10)
    
    coding_skills = np.clip(np.random.normal(65, 18, n_samples), 0, 100)
    communication_skills = np.clip(np.random.normal(68, 15, n_samples), 0, 100)
    
    # Create target variable based on weighted formula
    # Higher CGPA, more internships, more projects, better skills increase placement probability
    placement_score = (
        0.35 * (cgpa / 10) +
        0.20 * (internships / 5) +
        0.15 * (projects / 10) +
        0.15 * (coding_skills / 100) +
        0.15 * (communication_skills / 100)
    )
    
    # Add some randomness to make it more realistic
    noise = np.random.normal(0, 0.1, n_samples)
    placement_score = placement_score + noise
    
    # Threshold for placement (adjustable)
    threshold = 0.55
    placement_status = (placement_score > threshold).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'CGPA': np.round(cgpa, 2),
        'Internships': internships,
        'Projects': projects,
        'Coding_Skills_Score': np.round(coding_skills, 1),
        'Communication_Skills_Score': np.round(communication_skills, 1),
        'Placement_Status': placement_status
    })
    
    # Replace any remaining NaN values
    df = df.fillna(df.median(numeric_only=True))
    
    return df


def main():
    """Main function to generate and save dataset."""
    print("Generating synthetic placement dataset...")
    
    # Generate dataset
    df = generate_placement_data(n_samples=1000, random_state=42)
    
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Save dataset
    output_path = data_dir / "placement_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Dataset saved to {output_path}")
    print(f"\nDataset Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"Features: {df.columns.tolist()}")
    print(f"\nPlacement Distribution:")
    print(df['Placement_Status'].value_counts())
    print(f"\nFeature Statistics:")
    print(df.describe())
    
    return df


if __name__ == "__main__":
    main()
