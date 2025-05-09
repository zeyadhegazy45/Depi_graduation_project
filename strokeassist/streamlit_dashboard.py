import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.metrics import confusion_matrix, roc_curve, auc
import os

# Set page configuration
st.set_page_config(
    page_title="Stroke Prediction Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the model (for feature importance)
@st.cache_resource
def load_model():
    try:
        with open('stroke_model.pkl', 'rb') as file:
            model_data = pickle.load(file)
        return model_data['model'], model_data['feature_names']
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None, None

# Load stroke dataset
@st.cache_data
def load_data():
    # Try to load the dataset from common paths
    potential_paths = [
        'D:\\healthcare-dataset-stroke-data.csv'
    ]
    
    for path in potential_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    
    # If no dataset is found, create a mock dataset for demonstration
    st.warning("No actual stroke dataset found. Using synthetic data for demonstration.")
    
    # Create synthetic data based on stroke dataset schema
    np.random.seed(42)
    n_samples = 500
    
    data = {
        'id': range(1, n_samples + 1),
        'gender': np.random.choice(['Male', 'Female', 'Other'], n_samples, p=[0.48, 0.51, 0.01]),
        'age': np.clip(np.random.normal(45, 20, n_samples), 0, 100),
        'hypertension': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'heart_disease': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'ever_married': np.random.choice(['Yes', 'No'], n_samples),
        'work_type': np.random.choice(['Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'], n_samples),
        'Residence_type': np.random.choice(['Urban', 'Rural'], n_samples),
        'avg_glucose_level': np.clip(np.random.normal(106, 45, n_samples), 50, 300),
        'bmi': np.clip(np.random.normal(28, 7, n_samples), 10, 60),
        'smoking_status': np.random.choice(['never_smoked', 'formerly_smoked', 'smokes', 'Unknown'], n_samples),
    }
    
    # Adding stroke with correlation to risk factors
    stroke_prob = 0.05 + 0.1 * (data['age'] > 60).astype(int) + \
                  0.1 * data['hypertension'] + \
                  0.1 * data['heart_disease'] + \
                  0.05 * (data['avg_glucose_level'] > 200).astype(int)
    stroke_prob = np.clip(stroke_prob, 0, 0.9)
    data['stroke'] = np.random.binomial(1, stroke_prob)
    
    return pd.DataFrame(data)

# Main function
def main():
    model, feature_names = load_model()
    df = load_data()
    
    # Sidebar
    st.sidebar.title("Stroke Dashboard Navigation")
    page = st.sidebar.radio(
        "Select a page",
        ["Overview", "Demographics Analysis", "Risk Factors", "Model Insights"]
    )
    
    # Overview page
    if page == "Overview":
        st.title("Stroke Dataset Overview 🧠")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dataset Summary")
            st.write(f"Total Records: {len(df)}")
            st.write(f"Stroke Cases: {df['stroke'].sum()} ({df['stroke'].mean()*100:.2f}%)")
            st.write(f"Non-Stroke Cases: {len(df) - df['stroke'].sum()} ({(1-df['stroke'].mean())*100:.2f}%)")
            
            st.subheader("Dataset Preview")
            st.dataframe(df.head())
            
        with col2:
            st.subheader("Stroke Distribution")
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(df['stroke'].value_counts(), 
                   labels=['No Stroke', 'Stroke'], 
                   autopct='%1.1f%%',
                   colors=['#4CAF50', '#F44336'],
                   explode=[0, 0.1])
            ax.set_title('Stroke Distribution')
            st.pyplot(fig)
        
        st.subheader("Dataset Statistics")
        
        # Calculate statistics for numerical columns
        numeric_cols = ['age', 'avg_glucose_level', 'bmi']
        st.write(df[numeric_cols].describe())
    
    # Demographics Analysis page
    elif page == "Demographics Analysis":
        st.title("Demographics Analysis 👥")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stroke by Gender")
            gender_stroke = df.groupby('gender')['stroke'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='gender', y='stroke', data=gender_stroke, ax=ax)
            ax.set_title('Stroke Incidence by Gender')
            ax.set_ylabel('Stroke Incidence Rate')
            st.pyplot(fig)
            
            st.subheader("Stroke by Work Type")
            work_stroke = df.groupby('work_type')['stroke'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='work_type', y='stroke', data=work_stroke, ax=ax)
            ax.set_title('Stroke Incidence by Work Type')
            ax.set_ylabel('Stroke Incidence Rate')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            st.subheader("Stroke by Age Groups")
            # Create age groups
            df['age_group'] = pd.cut(df['age'], bins=[0, 20, 40, 60, 80, 100], labels=['0-20', '21-40', '41-60', '61-80', '81-100'])
            age_stroke = df.groupby('age_group')['stroke'].mean().reset_index()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='age_group', y='stroke', data=age_stroke, ax=ax)
            ax.set_title('Stroke Incidence by Age Group')
            ax.set_ylabel('Stroke Incidence Rate')
            st.pyplot(fig)
            
            st.subheader("Stroke by Residence Type")
            residence_stroke = df.groupby('Residence_type')['stroke'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='Residence_type', y='stroke', data=residence_stroke, ax=ax)
            ax.set_title('Stroke Incidence by Residence Type')
            ax.set_ylabel('Stroke Incidence Rate')
            st.pyplot(fig)
    
    # Risk Factors page
    elif page == "Risk Factors":
        st.title("Stroke Risk Factors Analysis 🔍")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stroke by Hypertension")
            hypertension_stroke = df.groupby('hypertension')['stroke'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='hypertension', y='stroke', data=hypertension_stroke, ax=ax)
            ax.set_title('Stroke Incidence by Hypertension')
            ax.set_ylabel('Stroke Incidence Rate')
            ax.set_xticks([0, 1])
            ax.set_xticklabels(['No Hypertension', 'Hypertension'])
            st.pyplot(fig)
            
            st.subheader("Average Glucose Level vs Stroke")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='stroke', y='avg_glucose_level', data=df, ax=ax)
            ax.set_title('Average Glucose Level by Stroke Status')
            ax.set_xticklabels(['No Stroke', 'Stroke'])
            st.pyplot(fig)
        
        with col2:
            st.subheader("Stroke by Heart Disease")
            heart_stroke = df.groupby('heart_disease')['stroke'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='heart_disease', y='stroke', data=heart_stroke, ax=ax)
            ax.set_title('Stroke Incidence by Heart Disease')
            ax.set_ylabel('Stroke Incidence Rate')
            ax.set_xticks([0, 1])
            ax.set_xticklabels(['No Heart Disease', 'Heart Disease'])
            st.pyplot(fig)
            
            st.subheader("BMI vs Stroke")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='stroke', y='bmi', data=df, ax=ax)
            ax.set_title('BMI by Stroke Status')
            ax.set_xticklabels(['No Stroke', 'Stroke'])
            st.pyplot(fig)
        
        st.subheader("Smoking Status and Stroke")
        smoking_stroke = df.groupby('smoking_status')['stroke'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='smoking_status', y='stroke', data=smoking_stroke, ax=ax)
        ax.set_title('Stroke Incidence by Smoking Status')
        ax.set_ylabel('Stroke Incidence Rate')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    # Model Insights page
    elif page == "Model Insights":
        st.title("Model Insights and Feature Importance 📊")
        
        if model is not None:
            # Display feature importance
            st.subheader("Feature Importance")
            
            if hasattr(model, 'coef_'):
                coef = model.coef_[0]
                importance = pd.DataFrame({
                    'Feature': feature_names,
                    'Importance': np.abs(coef)
                }).sort_values('Importance', ascending=False)
                
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.barplot(x='Importance', y='Feature', data=importance.head(15), ax=ax)
                ax.set_title('Top 15 Feature Importance (Absolute Value)')
                st.pyplot(fig)
                
                # Show positive and negative influences
                st.subheader("Feature Influence Direction")
                influence = pd.DataFrame({
                    'Feature': feature_names,
                    'Coefficient': coef
                }).sort_values('Coefficient', ascending=False)
                
                fig, ax = plt.subplots(figsize=(12, 8))
                bars = sns.barplot(x='Coefficient', y='Feature', data=influence.head(15), ax=ax)
                
                # Color bars based on positive or negative influence
                for i, bar in enumerate(bars.patches):
                    if bar.get_width() < 0:
                        bar.set_color('#F44336')  # Red for negative
                    else:
                        bar.set_color('#4CAF50')  # Green for positive
                
                ax.set_title('Top 15 Features by Coefficient Value')
                ax.axvline(x=0, color='black', linestyle='-', alpha=0.7)
                st.pyplot(fig)
            else:
                st.write("Feature importance visualization not available for this model type.")
        else:
            st.error("Model could not be loaded for analysis.")
        
        # Risk prediction chart
        st.subheader("Stroke Risk by Age and Hypertension")
        
        # Create a risk visualization
        age_range = np.linspace(20, 80, 100)
        risk_no_hypertension = []
        risk_with_hypertension = []
        
        for age in age_range:
            # This is a simplified risk calculation for visualization
            risk_no = 0.01 + age * 0.001
            risk_with = 0.01 + age * 0.001 + 0.1
            
            risk_no_hypertension.append(min(risk_no, 1.0))
            risk_with_hypertension.append(min(risk_with, 1.0))
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(age_range, risk_no_hypertension, label='No Hypertension', color='#4CAF50')
        ax.plot(age_range, risk_with_hypertension, label='With Hypertension', color='#F44336')
        ax.set_xlabel('Age')
        ax.set_ylabel('Stroke Risk Probability')
        ax.set_title('Estimated Stroke Risk by Age and Hypertension')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        st.subheader("Interactive Risk Assessment")
        st.write("This is a simplified risk visualization based on age and key risk factors.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Age", 20, 100, 50)
            hypertension = st.checkbox("Hypertension")
            heart_disease = st.checkbox("Heart Disease")
        
        with col2:
            glucose = st.slider("Average Glucose Level", 50, 300, 100)
            smoking = st.selectbox("Smoking Status", ["Never Smoked", "Formerly Smoked", "Currently Smoking"])
        
        # Calculate simplified risk score (this is for visualization only)
        risk_score = 0.01 + (age * 0.005) + (hypertension * 0.15) + (heart_disease * 0.15)
        risk_score += (glucose > 140) * 0.05
        risk_score += (smoking == "Currently Smoking") * 0.1 + (smoking == "Formerly Smoked") * 0.05
        risk_score = min(risk_score, 0.95)  # Cap at 95%
        
        # Display risk gauge
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(['Risk'], [risk_score], color='red' if risk_score > 0.5 else 'orange' if risk_score > 0.2 else 'green')
            ax.barh(['Risk'], [1], color='lightgray', alpha=0.3)
            ax.set_xlim(0, 1)
            ax.set_xticks([0, 0.2, 0.5, 0.8, 1])
            ax.set_xticklabels(['0%', '20%', '50%', '80%', '100%'])
            ax.set_title(f'Estimated Stroke Risk: {risk_score:.1%}')
            st.pyplot(fig)
            
            if risk_score < 0.2:
                st.success("Your estimated risk is relatively low based on the factors provided.")
            elif risk_score < 0.5:
                st.warning("Your estimated risk is moderate. Consider discussing with a healthcare provider.")
            else:
                st.error("Your estimated risk is high. Please consult with a healthcare provider.")
            
            st.info("Note: This is a simplified visualization and not a medical assessment. Always consult with healthcare professionals for proper medical advice.")

# Run the app
if __name__ == '__main__':
    main()