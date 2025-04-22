import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib

# Load Dataset
dataset = pd.read_csv("diabetes_prediction_dataset.csv")

# Check column names for reference (optional)
# print(dataset.columns)

# Separate features and target
X = dataset[['gender', 'age', 'hypertension', 'heart_disease',
             'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']]
y = dataset['diabetes']

# Define preprocessing for categorical columns
categorical_features = ['gender', 'smoking_history']
numeric_features = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']

# Create column transformer
preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(drop='first'), categorical_features),
    ('num', StandardScaler(), numeric_features)
])

# Create pipeline with preprocessor and logistic regression model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the pipeline
pipeline.fit(X_train, y_train)

# Save model
joblib.dump(pipeline, "diabetes_model_pipeline.pkl")
print("Model pipeline saved as diabetes_model_pipeline.pkl")

# Evaluate model
accuracy = pipeline.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

# Predict on test set
y_pred = pipeline.predict(X_test)

# Visualization
plt.figure(figsize=(8, 6))
plt.scatter(range(len(y_test)), y_test, color="red", label="Actual")
plt.scatter(range(len(y_pred)), y_pred, color="blue", marker="x", label="Predicted")
plt.xlabel("Samples")
plt.ylabel("Diabetes (0 = No, 1 = Yes)")
plt.title("Actual vs Predicted Diabetes Cases")
plt.legend()
plt.grid(True)
plt.show()
