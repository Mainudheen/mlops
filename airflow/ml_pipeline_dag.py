"""
Apache Airflow DAG for MLOps Pipeline
Orchestrates data preprocessing, model training, and evaluation
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# Default arguments for the DAG
default_args = {
    'owner': 'mlops_team',
    'depends_on_past': False,
    'email': ['mlops-alerts@example.com'],  # Replace with actual email
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def generate_data():
    """Generate synthetic dataset."""
    from src.generate_data import main as generate_main
    generate_main()


def validate_data():
    """Validate the generated dataset."""
    import pandas as pd
    from src.config import Config
    
    config = Config()
    df = pd.read_csv(config.RAW_DATA_PATH)
    
    # Validate required columns
    required_columns = [
        'CGPA', 'Internships', 'Projects',
        'Coding_Skills_Score', 'Communication_Skills_Score',
        'Placement_Status'
    ]
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Validate data quality
    assert len(df) > 0, "Dataset is empty"
    assert df['CGPA'].between(0, 10).all(), "CGPA out of range"
    assert df['Placement_Status'].isin([0, 1]).all(), "Invalid target values"
    
    print(f"Data validation passed! Shape: {df.shape}")


# Create the DAG
dag = DAG(
    'student_placement_mlops_pipeline',
    default_args=default_args,
    description='End-to-end MLOps pipeline for student placement prediction',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['mlops', 'machine-learning', 'placement-prediction'],
)


# Task 1: Generate Data
generate_data_task = PythonOperator(
    task_id='generate_data',
    python_callable=generate_data,
    dag=dag,
)


# Task 2: Validate Data
validate_data_task = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data,
    dag=dag,
)


# Task 3: Data Preprocessing
preprocess_data_task = BashOperator(
    task_id='preprocess_data',
    bash_command=f'cd {project_root} && python src/data_preprocessing.py',
    dag=dag,
)


# Task 4: Model Training
train_model_task = BashOperator(
    task_id='train_model',
    bash_command=f'cd {project_root} && python src/train.py',
    env={
        'PYTHONPATH': str(project_root),
        'MLFLOW_TRACKING_URI': 'file:./mlruns'
    },
    dag=dag,
)


# Task 5: Model Evaluation
evaluate_model_task = BashOperator(
    task_id='evaluate_model',
    bash_command=f'cd {project_root} && python src/evaluate.py',
    env={
        'PYTHONPATH': str(project_root),
        'MLFLOW_TRACKING_URI': 'file:./mlruns'
    },
    dag=dag,
)


# Task 6: Send Notification (placeholder)
def send_notification(**context):
    """Send notification about pipeline completion."""
    run_id = context['run_id']
    execution_date = context['execution_date']
    
    # Placeholder for actual notification logic
    # Could integrate with Slack, Email, or other notification services
    print(f"Pipeline completed successfully!")
    print(f"Run ID: {run_id}")
    print(f"Execution Date: {execution_date}")
    print("Model has been trained and evaluated. Ready for deployment.")


notify_completion_task = PythonOperator(
    task_id='notify_completion',
    python_callable=send_notification,
    provide_context=True,
    dag=dag,
)


# Define task dependencies
generate_data_task >> validate_data_task >> preprocess_data_task >> train_model_task >> evaluate_model_task >> notify_completion_task


# Documentation
dag.doc_md = """
## Student Placement Prediction MLOps Pipeline

This DAG orchestrates the complete MLOps workflow for the student placement prediction system.

### Tasks:
1. **Generate Data**: Creates synthetic training dataset
2. **Validate Data**: Ensures data quality and schema compliance
3. **Preprocess Data**: Cleans, scales, and splits data
4. **Train Model**: Trains Logistic Regression with MLflow tracking
5. **Evaluate Model**: Evaluates on test set and logs metrics
6. **Notify Completion**: Sends success notification

### Schedule:
Runs daily at 2:00 AM UTC

### Monitoring:
- Check Airflow UI for task status
- Review MLflow for experiment metrics
- Email notifications on failure
"""


if __name__ == "__main__":
    dag.cli()
