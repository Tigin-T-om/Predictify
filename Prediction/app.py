from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

app = Flask(__name__)

# Load all models and preprocessors
def load_models():
    models = {
        # Simple Linear Regression
        'house_price': {
            'model': joblib.load('house_price_model.pkl'),
            'scaler': joblib.load('house_price_scaler.pkl')
        },
        # Multiple Linear Regression
        'employee_salary': {
            'model': joblib.load('employee_salary_model.pkl'),
            'preprocessor': joblib.load('salary_preprocessor.pkl'),
            'scaler': joblib.load('salary_scaler.pkl')
        },
        # Polynomial Regression
        'temperature': {
            'model': joblib.load('weather_temp_model.pkl')
        },
        # KNN
        'fruit': {
            'model': joblib.load('fruit_knn_model.pkl'),
            'scaler': joblib.load('fruit_scaler.pkl'),
            'encoder': joblib.load('fruit_label_encoder.pkl')
        },
        # Logistic Regression
        'diabetes': {
            'pipeline': joblib.load('diabetes_model_pipeline.pkl')
        }
    }
    return models

models = load_models()

@app.route('/')
def home():
    return render_template('index.html')

# Simple Linear Regression
@app.route('/predict_house_price', methods=['POST'])
def predict_house_price():
    try:
        # Get square footage from form
        square_footage = float(request.form['square_footage'])
        
        # Prepare input
        X = np.array([[square_footage]])
        X_scaled = models['house_price']['scaler'].transform(X)
        
        # Predict
        prediction = models['house_price']['model'].predict(X_scaled)[0][0]
        
        return jsonify({
            'success': True,
            'prediction': f"₹{prediction:,.2f}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Multiple Linear Regression
@app.route('/predict_salary', methods=['POST'])
def predict_salary():
    try:
        # Get features
        age = float(request.form['age'])
        gender = request.form['gender']
        education = request.form['education_level']
        job_title = request.form['job_title']
        experience = float(request.form['experience'])
        
        # Create input DataFrame
        input_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            'Education Level': [education],
            'Job Title': [job_title],
            'Years of Experience': [experience]
        })
        
        # Process features
        X_processed = models['employee_salary']['preprocessor'].transform(input_data)
        
        # Predict
        prediction_scaled = models['employee_salary']['model'].predict(X_processed)
        prediction = models['employee_salary']['scaler'].inverse_transform(prediction_scaled)[0][0]
        
        return jsonify({
            'success': True,
            'prediction': f"₹{prediction:,.2f}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Polynomial Regression
@app.route('/predict_temperature', methods=['POST'])
def predict_temperature():
    try:
        # Get weather features
        apparent_temp = float(request.form['apparent_temperature'])
        humidity = float(request.form['humidity'])
        wind_speed = float(request.form['wind_speed'])
        wind_bearing = float(request.form['wind_bearing'])
        visibility = float(request.form['visibility'])
        cloud_cover = float(request.form['cloud_cover'])
        pressure = float(request.form['pressure'])
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        hour = int(request.form['hour'])
        precip_type = int(request.form['precip_type'])
        
        # Create input array
        features = np.array([[
            apparent_temp, humidity, wind_speed, wind_bearing, 
            visibility, cloud_cover, pressure, year, month, 
            day, hour, precip_type
        ]])
        
        # Predict using pipeline
        prediction = models['temperature']['model'].predict(features)[0][0]
        
        return jsonify({
            'success': True,
            'prediction': f"{prediction:.2f}°C"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# KNN Classifier
@app.route('/predict_fruit', methods=['POST'])
def predict_fruit():
    try:
        # Get features
        mass = float(request.form['mass'])
        width = float(request.form['width'])
        height = float(request.form['height'])
        color_score = float(request.form['color_score'])
        
        # Create input array
        features = np.array([[mass, width, height, color_score]])
        
        # Scale features
        features_scaled = models['fruit']['scaler'].transform(features)
        
        # Predict
        prediction_code = models['fruit']['model'].predict(features_scaled)[0]
        prediction = models['fruit']['encoder'].inverse_transform([prediction_code])[0]
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Logistic Regression
@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    try:
        # Get features
        gender = request.form['gender']
        age = float(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        smoking_history = request.form['smoking_history']
        bmi = float(request.form['bmi'])
        hba1c = float(request.form['hba1c'])
        glucose = float(request.form['glucose'])
        
        # Create input DataFrame
        input_data = pd.DataFrame({
            'gender': [gender],
            'age': [age],
            'hypertension': [hypertension],
            'heart_disease': [heart_disease],
            'smoking_history': [smoking_history],
            'bmi': [bmi],
            'HbA1c_level': [hba1c],
            'blood_glucose_level': [glucose]
        })
        
        # Predict using pipeline
        prediction = models['diabetes']['pipeline'].predict(input_data)[0]
        probability = models['diabetes']['pipeline'].predict_proba(input_data)[0][1] * 100
        
        result = "Positive (Diabetic)" if prediction == 1 else "Negative (Non-diabetic)"
        
        return jsonify({
            'success': True,
            'prediction': result,
            'probability': f"{probability:.2f}%"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/get_model_info', methods=['GET'])
def get_model_info():
    return jsonify({
        'models': [
            {
                'id': 'house_price',
                'name': 'House Price Prediction',
                'type': 'Simple Linear Regression',
                'features': ['Square Footage']
            },
            {
                'id': 'employee_salary',
                'name': 'Employee Salary Prediction',
                'type': 'Multiple Linear Regression',
                'features': ['Age', 'Gender', 'Education Level', 'Job Title', 'Experience']
            },
            {
                'id': 'temperature',
                'name': 'Temperature Prediction',
                'type': 'Polynomial Regression',
                'features': ['Apparent Temperature', 'Humidity', 'Wind Speed', 'Wind Bearing', 
                             'Visibility', 'Cloud Cover', 'Pressure', 'Year', 'Month', 'Day', 
                             'Hour', 'Precipitation Type']
            },
            {
                'id': 'fruit',
                'name': 'Fruit Classification',
                'type': 'K-Nearest Neighbors',
                'features': ['Mass', 'Width', 'Height', 'Color Score']
            },
            {
                'id': 'diabetes',
                'name': 'Diabetes Prediction',
                'type': 'Logistic Regression',
                'features': ['Gender', 'Age', 'Hypertension', 'Heart Disease', 
                             'Smoking History', 'BMI', 'HbA1c Level', 'Glucose Level']
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)