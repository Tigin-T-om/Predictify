from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Load trained model
regressor = joblib.load("slr_model.pkl")

# Load dataset for accuracy calculation
dataset = pd.read_csv('D:/projects/SLR/SLR_Calories_Prediction/steps_calories.csv')
X = dataset.iloc[:, 0:1].values
y = dataset.iloc[:, 1:2].values

# Split dataset (same as training)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Compute R² Score (Accuracy) based on test set
r2_score = regressor.score(X_test, y_test)
formatted_accuracy = f"{r2_score:.4f}"  # Convert to string

@app.route('/')
def home():
    print(f"Sending Accuracy to Frontend: {formatted_accuracy}")  # Debugging
    return render_template('index.html', accuracy=formatted_accuracy)  # Ensure accuracy is passed

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    steps_input = np.array([[data['steps']]])
    prediction = regressor.predict(steps_input)

    print(f"Sending Prediction: {prediction[0][0]}, Accuracy: {formatted_accuracy}")  # Debugging

    return jsonify({
        'calories_burned': prediction[0][0],
        'accuracy': formatted_accuracy  # Ensure accuracy is sent
    })

if __name__ == '__main__':
    app.run(debug=True)
