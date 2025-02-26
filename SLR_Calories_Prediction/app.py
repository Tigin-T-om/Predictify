from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load trained model
regressor = joblib.load("slr_model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    steps_input = np.array([[data['steps']]])
    prediction = regressor.predict(steps_input)
    return jsonify({'calories_burned': prediction[0][0]})

if __name__ == '__main__':
    app.run(debug=True)
