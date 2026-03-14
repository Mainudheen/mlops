"""
Streamlit UI for Student Placement Prediction
Production-grade interface with responsive design and intuitive UX
"""

import streamlit as st
import requests
import os
from pathlib import Path


# Page Configuration
st.set_page_config(
    page_title="Student Placement Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for production-grade styling
def load_css():
    """Load custom CSS for enhanced UI."""
    st.markdown("""
        <style>
        /* Main Container */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            min-height: 100vh;
        }
        
        /* Card Styling */
        .css-1r6slb0 {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* Header */
        .header {
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            margin-bottom: 0.5rem;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        /* Input Section */
        .input-section {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        /* Prediction Result */
        .result-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .prediction-placed {
            color: #059669;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 1rem 0;
        }
        
        .prediction-not-placed {
            color: #dc2626;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 1rem 0;
        }
        
        .probability-bar {
            background: #e5e7eb;
            border-radius: 10px;
            height: 20px;
            margin: 1rem 0;
            overflow: hidden;
        }
        
        .probability-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
            border-radius: 10px;
        }
        
        .confidence-badge {
            display: inline-block;
            padding: 0.5rem 1.5rem;
            border-radius: 20px;
            font-weight: 600;
            margin-top: 1rem;
        }
        
        .confidence-high {
            background: #d1fae5;
            color: #065f46;
        }
        
        .confidence-medium {
            background: #fef3c7;
            color: #92400e;
        }
        
        .confidence-low {
            background: #fee2e2;
            color: #991b1b;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Sidebar */
        .sidebar-content {
            background: rgba(255, 255, 255, 0.95);
            padding: 1.5rem;
            border-radius: 10px;
        }
        
        /* Info Boxes */
        .info-box {
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Logout Button */
        .logout-button {
            background: #dc2626 !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1.5rem !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            font-weight: 600 !important;
            margin-top: 2rem !important;
            width: 100% !important;
        }
        
        .logout-button:hover {
            background: #b91c1c !important;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .input-section {
                padding: 1rem;
            }
        }
        
        /* Metric Cards */
        .metric-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }
        
        .metric-label {
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)


def get_api_base_url():
    """Get FastAPI backend URL from environment or default."""
    return os.getenv("FASTAPI_URL", "http://localhost:8000")


def predict_placement(features):
    """
    Send prediction request to FastAPI backend.
    
    Parameters:
    -----------
    features : dict
        Dictionary of input features
    
    Returns:
    --------
    dict or None
        Prediction response or None if error
    """
    api_url = get_api_base_url()
    
    try:
        response = requests.post(
            f"{api_url}/predict",
            json=features,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def main():
    """Main Streamlit application."""
    # Load custom CSS
    load_css()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = True
    
    # Check if logged in
    if not st.session_state.logged_in:
        show_login()
        return
    
    # Main app
    show_main_app()


def show_login():
    """Show login screen (placeholder)."""
    st.markdown("""
        <div class="header">
            <h1>🔐 Login Required</h1>
            <p>Please log in to access the prediction system</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()


def logout():
    """Handle logout."""
    st.session_state.logged_in = False
    st.rerun()


def show_main_app():
    """Show main application."""
    # Header
    st.markdown("""
        <div class="header">
            <h1>🎓 Student Placement Prediction System</h1>
            <p>Predict placement outcomes using ML-powered insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("📋 Menu")
        
        # Navigation
        page = st.radio(
            "Navigate to:",
            ["Prediction", "About", "Model Info"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Information
        st.subheader("ℹ️ Information")
        st.markdown("""
        This system uses machine learning to predict 
        student placements based on:
        - Academic performance
        - Practical experience
        - Technical skills
        - Soft skills
        """)
        
        st.divider()
        
        # Logout button (REQUIRED per user preference)
        st.markdown("""
            <style>
            .stButton > button {
                width: 100%;
                background-color: #dc2626;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
            }
            .stButton > button:hover {
                background-color: #b91c1c;
            }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout"):
            logout()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content based on selection
    if page == "Prediction":
        show_prediction_page()
    elif page == "About":
        show_about_page()
    elif page == "Model Info":
        show_model_info_page()


def show_prediction_page():
    """Show prediction input form."""
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Academic Profile")
        cgpa = st.slider(
            "CGPA (0-10)",
            min_value=0.0,
            max_value=10.0,
            value=7.5,
            step=0.1,
            help="Cumulative Grade Point Average"
        )
        
        internships = st.slider(
            "Number of Internships",
            min_value=0,
            max_value=5,
            value=2,
            step=1,
            help="Completed internship programs"
        )
        
        projects = st.slider(
            "Number of Projects",
            min_value=0,
            max_value=10,
            value=3,
            step=1,
            help="Academic/Personal projects completed"
        )
    
    with col2:
        st.subheader("💼 Skills Assessment")
        coding_skills = st.slider(
            "Coding Skills Score",
            min_value=0,
            max_value=100,
            value=65,
            step=1,
            help="Technical coding ability (0-100)"
        )
        
        communication_skills = st.slider(
            "Communication Skills Score",
            min_value=0,
            max_value=100,
            value=68,
            step=1,
            help="Communication and soft skills (0-100)"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_btn = st.button("🔮 Predict Placement", use_container_width=True)
    
    if predict_btn:
        # Prepare features
        features = {
            "cgpa": cgpa,
            "internships": internships,
            "projects": projects,
            "coding_skills_score": coding_skills,
            "communication_skills_score": communication_skills
        }
        
        # Show loading spinner
        with st.spinner("Analyzing profile..."):
            result = predict_placement(features)
        
        if result:
            display_prediction(result)


def display_prediction(result):
    """Display prediction results with visualizations."""
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    st.subheader("📈 Prediction Results")
    
    # Prediction status
    prediction = result.get('prediction', 'Unknown')
    probability = result.get('probability', 0)
    confidence = result.get('confidence', 'Unknown')
    message = result.get('message', '')
    
    # Display prediction with appropriate styling
    if prediction == "Placed":
        st.markdown(f'<div class="prediction-placed">✅ {prediction}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="prediction-not-placed">❌ {prediction}</div>', unsafe_allow_html=True)
    
    # Probability bar
    st.markdown("### Confidence Level")
    st.markdown(f"""
        <div class="probability-bar">
            <div class="probability-fill" style="width: {probability * 100}%"></div>
        </div>
        <p style="text-align: center; font-weight: 600;">{probability * 100:.1f}% Probability</p>
    """, unsafe_allow_html=True)
    
    # Confidence badge
    confidence_class = f"confidence-{confidence.lower()}"
    st.markdown(f"""
        <div style="text-align: center;">
            <span class="confidence-badge {confidence_class}">
                {confidence} Confidence
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    # Message
    st.info(message)
    
    # Feature importance (static for demo)
    st.divider()
    st.subheader("🎯 Key Success Factors")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CGPA Weight", "35%", delta="High Impact")
    with col2:
        st.metric("Internships", "20%", delta="Medium Impact")
    with col3:
        st.metric("Projects", "15%", delta="Medium Impact")
    with col4:
        st.metric("Skills", "30%", delta="Combined")
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_about_page():
    """Show about information."""
    st.markdown("""
        <div class="input-section">
            <h2>📚 About This System</h2>
            <p>This Student Placement Prediction System is a comprehensive MLOps solution that leverages machine learning to predict student placement outcomes.</p>
            
            <h3>🛠️ Technologies Used</h3>
            <ul>
                <li><strong>Machine Learning:</strong> Scikit-learn (Logistic Regression)</li>
                <li><strong>Experiment Tracking:</strong> MLflow</li>
                <li><strong>Data Versioning:</strong> DVC</li>
                <li><strong>Backend API:</strong> FastAPI</li>
                <li><strong>Frontend UI:</strong> Streamlit</li>
                <li><strong>Orchestration:</strong> Apache Airflow</li>
                <li><strong>Containerization:</strong> Docker</li>
                <li><strong>CI/CD:</strong> GitHub Actions</li>
                <li><strong>Deployment:</strong> Railway</li>
            </ul>
            
            <h3>📊 Model Features</h3>
            <div class="metric-container">
                <div class="metric-card">
                    <div class="metric-value">5</div>
                    <div class="metric-label">Input Features</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">80%</div>
                    <div class="metric-label">Train Split</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">20%</div>
                    <div class="metric-label">Test Split</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">LR</div>
                    <div class="metric-label">Model Type</div>
                </div>
            </div>
            
            <h3>🎯 How It Works</h3>
            <ol>
                <li><strong>Data Collection:</strong> Historical student data with placement outcomes</li>
                <li><strong>Feature Engineering:</strong> CGPA, internships, projects, and skills scores</li>
                <li><strong>Model Training:</strong> Logistic Regression with MLflow tracking</li>
                <li><strong>Evaluation:</strong> Comprehensive metrics including accuracy, precision, recall</li>
                <li><strong>Deployment:</strong> REST API via FastAPI with Streamlit UI</li>
            </ol>
            
            <div class="info-box">
                <strong>💡 Note:</strong> This is a demonstration project showcasing MLOps best practices. 
                Real-world deployment would require additional considerations for data privacy, model monitoring, and continuous improvement.
            </div>
        </div>
    """, unsafe_allow_html=True)


def show_model_info_page():
    """Show model information from FastAPI."""
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    api_url = get_api_base_url()
    
    try:
        response = requests.get(f"{api_url}/model-info", timeout=5)
        if response.status_code == 200:
            model_info = response.json()
            
            st.subheader("🤖 Model Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Model Name", model_info.get('model_name', 'N/A'))
                st.metric("Version", model_info.get('version', 'N/A'))
            
            with col2:
                st.metric("MLflow Run ID", model_info.get('mlflow_run_id', 'Not Available')[:8] + "..." if model_info.get('mlflow_run_id') else 'N/A')
            
            st.divider()
            
            st.write("**Input Features:**")
            features = model_info.get('features', [])
            for i, feature in enumerate(features, 1):
                st.write(f"{i}. {feature}")
        else:
            st.warning("Could not retrieve model information. Is the FastAPI server running?")
    except Exception as e:
        st.error(f"Error fetching model info: {str(e)}")
        st.info("Make sure the FastAPI server is running at http://localhost:8000")
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
