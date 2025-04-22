from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, accuracy_score
import joblib
from house_price_predictor import HousePricePredictor

app = Flask(__name__)

# Load available models and scalers
try:
    house_model = joblib.load('house_price_model.pkl')
    house_scaler = joblib.load('house_price_scaler.pkl')
    salary_model = joblib.load('employee_salary_model.pkl')
    salary_preprocessor = joblib.load('salary_preprocessor.pkl')
    salary_scaler = joblib.load('salary_scaler.pkl')
    diabetes_model = joblib.load('diabetes_model_pipeline.pkl')
    fruit_model = joblib.load('fruit_knn_model.pkl')
    fruit_scaler = joblib.load('fruit_scaler.pkl')
    fruit_label_encoder = joblib.load('fruit_label_encoder.pkl')
    temp_model = joblib.load('temperature_model.pkl')
    temp_scaler = joblib.load('scaler.pkl')
    temp_poly = joblib.load('poly_transform.pkl')
except FileNotFoundError as e:
    print(f"Error loading model files: {str(e)}")
    print("Please ensure all model files are present in the Prediction directory")
    exit(1)

# Calculate accuracies for available models
try:
    # House Price Model Accuracy
    house_data = pd.read_csv('house_prediction_slr.csv')
    house_data = house_data.dropna()  # Remove any rows with NaN values
    X_house = house_data[['SquareFootage']].values
    y_house = house_data[['Price']].values
    X_house_scaled = house_scaler.transform(X_house)
    house_accuracy = r2_score(y_house, house_model.predict(X_house_scaled))

    # Salary Model Accuracy
    salary_data = pd.read_csv('Salary Data.csv')
    salary_data = salary_data.dropna()  # Remove any rows with NaN values
    X_salary = salary_data.drop(columns=['Salary'])
    y_salary = salary_data['Salary'].values.reshape(-1, 1)
    X_salary_processed = salary_preprocessor.transform(X_salary)
    y_salary_scaled = salary_scaler.transform(y_salary)
    salary_accuracy = r2_score(y_salary_scaled, salary_model.predict(X_salary_processed))

    # Diabetes Model Accuracy
    diabetes_data = pd.read_csv('diabetes_prediction_dataset.csv')
    diabetes_data = diabetes_data.dropna()  # Remove any rows with NaN values
    X_diabetes = diabetes_data[['gender', 'age', 'hypertension', 'heart_disease',
                               'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']]
    y_diabetes = diabetes_data['diabetes']
    diabetes_accuracy = diabetes_model.score(X_diabetes, y_diabetes)

    # Fruit Model Accuracy
    fruit_data = pd.read_csv('fruit_data.csv')
    fruit_data = fruit_data.dropna()  # Remove any rows with NaN values
    X_fruit = fruit_data[['mass', 'width', 'height', 'color_score']]
    y_fruit = fruit_data['fruit_name']
    X_fruit_scaled = fruit_scaler.transform(X_fruit)
    y_fruit_encoded = fruit_label_encoder.transform(y_fruit)
    fruit_accuracy = accuracy_score(y_fruit_encoded, fruit_model.predict(X_fruit_scaled))

    # Temperature Model Accuracy
    temp_data = pd.read_csv('weather_data.csv')
    temp_data = temp_data.dropna()  # Remove any rows with NaN values
    X_temp = temp_data.drop(columns=['temperature_c']).values
    y_temp = temp_data[['temperature_c']].values
    X_temp_scaled = temp_scaler.transform(X_temp)
    X_temp_poly = temp_poly.transform(X_temp_scaled)
    temp_accuracy = r2_score(y_temp, temp_model.predict(X_temp_poly))

except FileNotFoundError as e:
    print(f"Error loading dataset files: {str(e)}")
    print("Please ensure all dataset files are present in the Prediction directory")
    exit(1)
except Exception as e:
    print(f"Error calculating model accuracies: {str(e)}")
    # Set default accuracies if calculation fails
    house_accuracy = 0.0
    salary_accuracy = 0.0
    diabetes_accuracy = 0.0
    fruit_accuracy = 0.0
    temp_accuracy = 0.0

# Initialize the house price predictor
house_predictor = HousePricePredictor()

@app.route('/')
def home():
    return render_template('index.html',
                         house_accuracy="{:.4f}".format(house_accuracy),
                         salary_accuracy="{:.4f}".format(salary_accuracy),
                         diabetes_accuracy="{:.4f}".format(diabetes_accuracy),
                         fruit_accuracy="{:.4f}".format(fruit_accuracy),
                         temp_accuracy="{:.4f}".format(temp_accuracy))

@app.route('/predict_house', methods=['POST'])
def predict_house():
    try:
        data = request.get_json()
        sqft = data.get('sqft')
        
        if sqft is None:
            return jsonify({'error': 'Square footage is required'}), 400
            
        # Get prediction from the predictor
        result = house_predictor.predict(sqft)
        
        if not result['input_validated']:
            return jsonify({'error': result['error']}), 400
            
        # Return prediction with warning if any
        response = {
            'prediction': result['prediction'],
            'accuracy': house_accuracy
        }
        
        if result['warning']:
            response['warning'] = result['warning']
            
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_salary', methods=['POST'])
def predict_salary():
    try:
        data = request.get_json()
        age = float(data['age'])
        years_experience = float(data['years_experience'])
        gender = data['gender']
        education_level = data['education_level']
        job_title = data['job_title']
        
        # Create input DataFrame
        input_data = pd.DataFrame({
            'Age': [age],
            'Years of Experience': [years_experience],
            'Gender': [gender],
            'Education Level': [education_level],
            'Job Title': [job_title]
        })
        
        # Preprocess input
        X_processed = salary_preprocessor.transform(input_data)
        
        # Make prediction
        prediction_scaled = salary_model.predict(X_processed)[0]
        prediction = salary_scaler.inverse_transform([[prediction_scaled]])[0][0]
        
        return jsonify({
            'prediction': float(prediction),
            'accuracy': float(salary_accuracy)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    try:
        data = request.get_json()
        gender = data['gender']
        age = float(data['age'])
        hypertension = int(data['hypertension'])
        heart_disease = int(data['heart_disease'])
        smoking_history = data['smoking_history']
        bmi = float(data['bmi'])
        hba1c_level = float(data['hba1c_level'])
        blood_glucose_level = float(data['blood_glucose_level'])
        
        # Create input DataFrame
        input_data = pd.DataFrame({
            'gender': [gender],
            'age': [age],
            'hypertension': [hypertension],
            'heart_disease': [heart_disease],
            'smoking_history': [smoking_history],
            'bmi': [bmi],
            'HbA1c_level': [hba1c_level],
            'blood_glucose_level': [blood_glucose_level]
        })
        
        # Make prediction
        prediction = diabetes_model.predict(input_data)[0]
        probability = diabetes_model.predict_proba(input_data)[0][1] * 100
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability),
            'accuracy': float(diabetes_accuracy)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_fruit', methods=['POST'])
def predict_fruit():
    try:
        data = request.get_json()
        mass = float(data['mass'])
        width = float(data['width'])
        height = float(data['height'])
        color_score = float(data['color_score'])
        
        # Input validation
        if mass <= 0 or width <= 0 or height <= 0:
            return jsonify({'error': 'Mass, width, and height must be positive'}), 400
        if color_score < 0 or color_score > 1:
            return jsonify({'error': 'Color score must be between 0 and 1'}), 400
            
        # Scale inputs
        X = [[mass, width, height, color_score]]
        X_scaled = fruit_scaler.transform(X)
        
        # Get prediction probabilities
        probabilities = fruit_model.predict_proba(X_scaled)[0]
        prediction_idx = np.argmax(probabilities)
        predicted_fruit = fruit_label_encoder.inverse_transform([prediction_idx])[0]
        
        return jsonify({
            'prediction': predicted_fruit,
            'confidence': float(probabilities[prediction_idx] * 100),
            'accuracy': float(fruit_accuracy)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_temperature', methods=['POST'])
def predict_temperature():
    try:
        data = request.get_json()
        # Get all features except temperature_c
        input_data = {k: float(v) for k, v in data.items() if k != 'temperature_c'}
        
        # Create input array
        X = np.array([list(input_data.values())])
        
        # Scale and transform
        X_scaled = temp_scaler.transform(X)
        X_poly = temp_poly.transform(X_scaled)
        
        # Make prediction
        prediction = temp_model.predict(X_poly)[0][0]
        
        return jsonify({
            'prediction': float(prediction),
            'accuracy': float(temp_accuracy)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
