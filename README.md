# Stroke Prediction Web Application
A comprehensive web application for stroke prediction using a machine learning model built with PyCaret, integrated with Flask, and featuring an interactive dashboard built with Streamlit.
Features

Interactive Prediction Form: Input patient information to get stroke risk prediction
Informative Chatbot: Provides information about strokes, risk factors, and prevention
Analytics Dashboard: Visualizes stroke data analysis with Streamlit
Responsive Design: Clean UI using Bootstrap framework

Project Structure
stroke-prediction-app/
├── app.py                    # Main Flask application
├── final.py                  # stroke prediction using PyCaret
├── model.py                  # Model loading and prediction logic
├── chatbot.py                # Chatbot functionality
├── streamlit_dashboard.py    # Streamlit dashboard
├── best_lr.pkl               # Pre-trained model (not included in repo)
├── requirements.txt          # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   └── js/
│       └── script.js         # JavaScript for UI interactions
└── templates/
    ├── base.html             # Base template with common elements
    └── index.html            # Main application page
Installation

Clone this repository:

bashgit clone https://github.com/yourusername/stroke-prediction-app.git
cd stroke-prediction-app

Create and activate a virtual environment:

bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bashpip install -r requirements.txt

Place your trained model file best_lr.pkl in the project root directory.

Usage

Run the Flask application:

bashpython app.py
The application will be available at http://localhost:8000

Run the Streamlit dashboard separately:

bashstreamlit run streamlit_dashboard.py
The dashboard will be available at http://localhost:8501
Dependencies

Python 3.11+
Flask
Waitress
Streamlit
PyCaret
Pandas
NumPy
Scikit-learn
Bootstrap (included via CDN)

Model Information
The stroke prediction model was trained using PyCaret with Logistic Regression. The model file model_stroke.pkl contains the trained model and preprocessing pipeline.
