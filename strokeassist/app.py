from flask import Flask, render_template, request, jsonify
import os
import json
from model import load_model, predict_stroke_risk
from chatbot import get_chatbot_response

app = Flask(__name__)

# Load the model at startup
try:
    model, feature_names = load_model('stroke_model.pkl')
    print("Model and features loaded successfully")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model, feature_names = None, None

@app.route('/')
def home():
    """Render the homepage with the prediction form"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request and return result"""
    try:
        # Get form data
        data = request.form.to_dict()
        
        # Make prediction
        prediction, probability, feature_importance = predict_stroke_risk(
            model, 
            feature_names,
            data
        )
        
        # Format result for display
        result = {
            'prediction': 'High Risk' if prediction == 1 else 'Low Risk',
            'probability': f"{probability:.2%}",
            'feature_importance': feature_importance
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """Handle chatbot message and return response"""
    try:
        message = request.json.get('message', '')
        response = get_chatbot_response(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/dashboard')
def dashboard():
    """Provide information about how to access the Streamlit dashboard"""
    return render_template('dashboard_info.html')

if __name__ == '__main__':
    try:
        print("Starting the application...")
        # For development
        # app.run(debug=True)

        # For production
        from waitress import serve
        port = int(os.environ.get('PORT', 8080))
        print(f"Starting server on port {port}")
        serve(app, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Error starting the server: {str(e)}")


