import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
import joblib

# Load Cleaned Dataset
dataset = pd.read_csv("weather_data.csv")  # Make sure this file has your cleaned fields

# ✅ Select Features and Target
# Example: Predicting actual temperature using all other features
X = dataset.drop(columns=["temperature_c"]).values
y = dataset[["temperature_c"]].values

# ✅ Handle Missing Values (just in case)
imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
X = imputer.fit_transform(X)
y = imputer.fit_transform(y)

# ✅ Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ✅ Polynomial Feature Expansion
degree = 3  # You can increase/decrease for more complex models
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(X_scaled)

# ✅ Split the Dataset
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# ✅ Train the Model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# ✅ Save Model & Transformers
joblib.dump(regressor, "temperature_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(poly, "poly_transform.pkl")
print("✅ Model and transformers saved successfully.")

# ✅ Predict and Evaluate
y_pred = regressor.predict(X_test)
r2_score = regressor.score(X_test, y_test)
print(f"📈 Model Accuracy (R² Score): {r2_score:.4f}")

# ✅ Visualization
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color="skyblue", edgecolor='k', label="Predicted vs Actual")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label="Ideal Fit")
plt.xlabel("Actual Temperature (°C)")
plt.ylabel("Predicted Temperature (°C)")
plt.title("Actual vs Predicted Temperature")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
