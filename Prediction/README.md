# Machine Learning Prediction Web Application

A Flask web application that provides multiple machine learning prediction models:
1. House Price Prediction (Simple Linear Regression)
2. Employee Salary Prediction (Multiple Linear Regression)
3. Diabetes Risk Prediction (Logistic Regression)
4. Fruit Classification (K-Nearest Neighbors)

## Project Structure
```
Prediction/
├─ static/
│  ├─ fruit_plot.png
│  ├─ script.js
│  └─ style.css
├─ templates/
│  └─ index.html
├─ app.py
├─ diabetes_model.pkl
├─ diabetes_prediction.csv
├─ diabetes_scaler.pkl
├─ employee_salaries.csv
├─ fruit_classification.csv
├─ fruit_model.pkl
├─ fruit_scaler.pkl
├─ house_prices.csv
├─ README.md
├─ requirements.txt
├─ salary_model.pkl
├─ salary_scaler.pkl
├─ slr_model.pkl
├─ train_diabetes_model.py
├─ train_fruit_model.py
├─ train_mlr_model.py
└─ train_model.py
```

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the models:
```bash
python train_model.py  # House Price Model
python train_mlr_model.py  # Salary Model
python train_diabetes_model.py  # Diabetes Model
python train_fruit_model.py  # Fruit Classification Model
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and go to `http://localhost:5000`

## Models

### House Price Prediction
- Input: Square footage
- Output: Predicted house price
- Model: Simple Linear Regression

### Employee Salary Prediction
- Inputs: Years of experience, Test score
- Output: Predicted salary
- Model: Multiple Linear Regression

### Diabetes Risk Prediction
- Inputs: BMI, Blood Pressure, Glucose Level
- Output: Risk prediction (High/Low) with probability
- Model: Logistic Regression

### Fruit Classification
- Inputs: Weight (grams), Color Intensity (0-100)
- Output: Predicted fruit type with probability distribution
- Model: K-Nearest Neighbors
- Classes: Apple, Banana, Orange, Pear

## Features
- Modern, responsive UI with Bootstrap
- Real-time predictions using AJAX
- Interactive visualizations
- Model accuracy display
- Input validation
- Error handling
- Color-coded results
- Probability distributions for classifications 