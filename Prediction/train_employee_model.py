import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Load Dataset
dataset = pd.read_csv("Salary Data.csv")

# Drop rows with missing target (Salary)
dataset = dataset.dropna(subset=["Salary"])

# Separate features and target
X = dataset.drop(columns="Salary")
y = dataset["Salary"].values.reshape(-1, 1)

# Identify columns
num_cols = ["Age", "Years of Experience"]
cat_cols = ["Gender", "Education Level", "Job Title"]

# Preprocessing for numerical and categorical data
num_imputer = SimpleImputer(strategy='mean')
cat_imputer_encoder = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# Combine into a column transformer
preprocessor = ColumnTransformer([
    ('num', num_imputer, num_cols),
    ('cat', cat_imputer_encoder, cat_cols)
])

# Scale target
target_scaler = StandardScaler()
y = target_scaler.fit_transform(y)

# Transform the features
X_processed = preprocessor.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.3, random_state=42)

# Train the model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Save model, preprocessor, and scaler
joblib.dump(regressor, "employee_salary_model.pkl")
joblib.dump(preprocessor, "salary_preprocessor.pkl")
joblib.dump(target_scaler, "salary_scaler.pkl")

print("Model, preprocessor, and scaler saved.")

# Predict
y_pred = regressor.predict(X_test)

# Evaluate
r2_score = regressor.score(X_test, y_test)
print(f"Model Accuracy (R² Score): {r2_score:.4f}")

# Plot predictions
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Salary (scaled)')
plt.ylabel('Predicted Salary (scaled)')
plt.title('Actual vs Predicted Salaries')
plt.show()
