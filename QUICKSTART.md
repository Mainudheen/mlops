# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Generate Dataset

```bash
python src/generate_data.py
```

Expected output:
```
Generating synthetic placement dataset...
Dataset saved to D:\Mlops-final\data\raw\placement_data.csv

Dataset Statistics:
Total samples: 1000
Features: ['CGPA', 'Internships', 'Projects', 'Coding_Skills_Score', 'Communication_Skills_Score', 'Placement_Status']
```

### Step 3: Preprocess Data

```bash
python src/data_preprocessing.py
```

Expected output:
```
============================================================
DATA PREPROCESSING PIPELINE
============================================================
Loading data from D:\Mlops-final\data\raw\placement_data.csv...
Dataset shape: (1000, 6)
Preprocessing data...
Scaling features...
Splitting data (test_size=0.2)...
Training set size: 800
Test set size: 200
Saving processed data to D:\Mlops-final\data\processed...
Processed data saved successfully!
============================================================
PREPROCESSING COMPLETED SUCCESSFULLY
============================================================
```

### Step 4: Train Model

```bash
python src/train.py
```

Expected output:
```
============================================================
MODEL TRAINING PIPELINE
============================================================
MLflow tracking URI: file:./mlruns
Experiment: student_placement_prediction
Loading processed training data...
Training data shape: (800, 5)
Training Logistic Regression model...
Model training completed!
Evaluating model on training data...
Training Accuracy: 0.XXXX
Training Precision: 0.XXXX
Training Recall: 0.XXXX
Training F1 Score: 0.XXXX
Logging to MLflow...
MLflow Run ID: xxxxxxxxxxxxxxxx
Model logged successfully!
Model saved to D:\Mlops-final\models\placement_model.pkl
============================================================
TRAINING COMPLETED SUCCESSFULLY
============================================================
```

### Step 5: Evaluate Model

```bash
python src/evaluate.py
```

Expected output:
```
============================================================
MODEL EVALUATION PIPELINE
============================================================
Loading processed test data...
Test data shape: (200, 5)
Loading model 'placement_classifier' from MLflow...
Model loaded from MLflow!
Evaluating model on test data...

============================================================
MODEL EVALUATION RESULTS
============================================================
Accuracy:  0.XXXX
Precision: 0.XXXX
Recall:    0.XXXX
F1 Score:  0.XXXX
ROC-AUC:   0.XXXX

Confusion Matrix:
  TN: XX  FP: XX
  FN: XX  TP: XX

Classification Report:
              precision    recall  f1-score   support
           0       0.XX      0.XX      0.XX        XX
           1       0.XX      0.XX      0.XX        XX
    accuracy                           0.XX       200
   macro avg       0.XX      0.XX      0.XX       200
weighted avg       0.XX      0.XX      0.XX       200
============================================================
Evaluation logged to MLflow (Run ID: xxxxxxxxxxxxxxxx)
Evaluation results saved to evaluation_results.json
============================================================
EVALUATION COMPLETED SUCCESSFULLY
============================================================
```

### Step 6: Run FastAPI Server

```bash
uvicorn app.fastapi_app:app --reload
```

Access API at: http://localhost:8000

Test the API:
```bash
curl http://localhost:8000/health
```

### Step 7: Run Streamlit UI

Open a new terminal:

```bash
streamlit run app/streamlit_app.py
```

Access UI at: http://localhost:8501

---

## 🐳 Docker Quick Start

### Build and Run with Docker Compose

```bash
# Build all services
docker-compose up --build

# Or build individually
docker build -t placement-api .
docker build -f Dockerfile.streamlit -t placement-ui .

# Run API only
docker run -p 8000:8000 placement-api
```

---

## ✅ Verify Installation

Run tests:
```bash
pytest tests/ -v
```

All tests should pass!

---

## 🎯 Next Steps

- View MLflow UI: `mlflow ui --port 5000`
- Setup Airflow: Configure and start scheduler
- Deploy to Railway: Follow deployment guide in README
- Customize model parameters in `params.yaml`

---

**Need Help?** Check the full [README.md](README.md) for detailed documentation.
