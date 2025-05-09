import pickle
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

def load_model(model_path):
    """
    Load the trained model and feature names from pickle file
    """
    try:
        # Check if the file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        print(f"Loading model from: {model_path}")
        
        with open(model_path, 'rb') as file:
            model_data = pickle.load(file)
        
        # Print what we got from pickle for debugging
        print(f"Type of loaded object: {type(model_data)}")
        
        # Handle different possible pickle structures
        if isinstance(model_data, dict):
            print(f"Keys in model_data: {list(model_data.keys())}")
            
            # Try to get model and feature_names from the dictionary
            model = model_data.get('model')
            feature_names = model_data.get('feature_names')
            
            # If model not found in expected key, check alternatives
            if model is None:
                # Maybe the model is the entire object
                if 'model' not in model_data and hasattr(model_data, 'predict'):
                    print("Using the entire pickle object as the model")
                    model = model_data
                    # Try to get feature names from model attributes
                    if hasattr(model, 'feature_names_in_'):
                        feature_names = model.feature_names_in_.tolist()
                    else:
                        # You may need to provide feature names manually
                        raise ValueError("Feature names not found in model")
        else:
            # Maybe the pickle is just the model without a dictionary wrapper
            print("Pickle is not a dictionary. Checking if it's a model directly...")
            if hasattr(model_data, 'predict'):
                print("Using the entire pickle object as the model")
                model = model_data
                # Try to get feature names from model attributes
                if hasattr(model, 'feature_names_in_'):
                    feature_names = model.feature_names_in_.tolist()
                else:
                    # You may need to provide feature names manually
                    raise ValueError("Feature names not found in model")
            else:
                raise ValueError("Unable to find a valid model in the pickle file")
        
        # Final check
        if model is None:
            raise ValueError("Model not found in pickle file")
        if feature_names is None or not feature_names:
            raise ValueError("Feature names not found in model data")
            
        print(f"Model loaded successfully. Type: {type(model)}")
        print(f"Feature names: {feature_names[:5]}... (total: {len(feature_names)})")
        
        return model, feature_names
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Print the full traceback
        raise Exception(f"Failed to load model: {str(e)}")

def preprocess_input(data, feature_names):
    """
    Preprocess user input to match the format expected by the model
    """
    # Check if feature_names is None or empty
    if feature_names is None or len(feature_names) == 0:
        raise ValueError("Feature names cannot be None or empty")
        
    # Create a DataFrame with the expected feature names
    input_dict = {feature: [0] for feature in feature_names}
    input_df = pd.DataFrame(input_dict)
    
    # Handle numeric features
    numeric_features = {
        'age': float,
        'avg_glucose_level': float,
        'bmi': float
    }
    
    for feature, dtype in numeric_features.items():
        if feature in data and feature in feature_names:
            try:
                input_df.loc[0, feature] = dtype(data[feature])
            except (ValueError, TypeError):
                # Handle conversion errors
                print(f"Warning: Could not convert {feature} value to {dtype}")
    
    # Handle categorical features with one-hot encoding
    categorical_mappings = {
        'gender': ['gender_Female', 'gender_Male', 'gender_Other'],
        'hypertension': ['hypertension_0', 'hypertension_1'],
        'heart_disease': ['heart_disease_0', 'heart_disease_1'],
        'ever_married': ['ever_married_No', 'ever_married_Yes'],
        'work_type': ['work_type_Govt_job', 'work_type_Never_worked', 'work_type_Private', 
                     'work_type_Self-employed', 'work_type_children'],
        'Residence_type': ['Residence_type_Rural', 'Residence_type_Urban'],
        'smoking_status': ['smoking_status_Unknown', 'smoking_status_formerly_smoked', 
                          'smoking_status_never_smoked', 'smoking_status_smokes']
    }
    
    for feature, encoded_features in categorical_mappings.items():
        if feature in data and data[feature] is not None:
            value = data[feature]
            for encoded_feature in encoded_features:
                if encoded_feature == f"{feature}_{value}" and encoded_feature in feature_names:
                    input_df.loc[0, encoded_feature] = 1
    
    # Ensure we're only using columns that exist in feature_names
    valid_columns = [col for col in input_df.columns if col in feature_names]
    input_df = input_df[valid_columns]
    
    # If some feature_names are still missing, add them
    missing_columns = [col for col in feature_names if col not in input_df.columns]
    for col in missing_columns:
        input_df[col] = 0
    
    # Reorder columns to match the model's expectations
    input_df = input_df[feature_names]
    
    return input_df

def predict_stroke_risk(model, feature_names, data):
    """
    Make stroke risk prediction based on user input
    """
    # Check for None values
    if model is None:
        raise ValueError("Model cannot be None")
    if feature_names is None:
        raise ValueError("Feature names cannot be None")
    if data is None:
        raise ValueError("Input data cannot be None")
    
    # Preprocess the input data
    input_data = preprocess_input(data, feature_names)
    
    # Make prediction
    try:
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]  # Probability of positive class
        prediction = 1 if probability >= 0.7 else 0
    except Exception as e:
        raise Exception(f"Error during prediction: {str(e)}")
    
    # Get feature importance
    # For logistic regression, we can use coefficients as importance
    top_features = {}
    if hasattr(model, 'coef_'):
        try:
            importance = model.coef_[0]
            # Check if importance array matches feature_names length
            if len(importance) != len(feature_names):
                print(f"Warning: Importance array length ({len(importance)}) doesn't match feature names length ({len(feature_names)})")
                return prediction, probability, {}
                
            feature_importance = dict(zip(feature_names, importance))
            
            # Sort by absolute value of importance
            feature_importance = {k: v for k, v in sorted(
                feature_importance.items(), 
                key=lambda item: abs(item[1]), 
                reverse=True
            )}
            
            # Take only top 5 features with non-zero importance
            count = 0
            for feature, importance in feature_importance.items():
                if abs(importance) > 0:
                    # Clean up feature name for display
                    display_name = feature.split('_')[0] if '_' in feature else feature
                    top_features[display_name] = importance
                    count += 1
                    if count >= 5:
                        break
        except Exception as e:
            print(f"Warning: Error calculating feature importance: {str(e)}")
    
    return prediction, probability, top_features

# Example usage with hardcoded feature names as fallback
def example():
    try:
        # Try to load model
        try:
            model, feature_names = load_model("stroke_model.pkl")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            print("Using fallback approach...")
            
            # If the model loading fails due to feature_names issue, 
            # try direct model loading with hardcoded feature names
            with open("stroke_model.pkl", 'rb') as file:
                model = pickle.load(file)
            
            # Hardcoded feature names - you need to provide these based on your model
            feature_names = [
              'age', 'avg_glucose_level', 'bmi', 
               'hypertension_0', 'heart_disease_0',
            'ever_married_Yes', 'work_type_Private', 
             'Residence_type_Urban',  'smoking_status_never smoked', 'gender_Male'
            ]
        
        # Example input data
        input_data = {
            'age': 65,
            'gender': 'Male',
            'hypertension': '1',
            'heart_disease': '0',
            'ever_married': 'Yes',
            'work_type': 'Private',
            'Residence_type': 'Urban',
            'avg_glucose_level': 200.5,
            'bmi': 28.5,
            'smoking_status': 'formerly_smoked'
        }
        
        # Make prediction
        prediction, probability, top_features = predict_stroke_risk(model, feature_names, input_data)
        
        print(f"Stroke prediction: {prediction}")
        print(f"Probability: {probability:.2f}")
        print("Top features contributing to prediction:")
        for feature, importance in top_features.items():
            print(f"  {feature}: {importance:.4f}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

# If you want to run the example, uncomment the line below
# example()