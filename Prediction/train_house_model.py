import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib

# Load the dataset
dataset = pd.read_csv("house_prediction_slr.csv")  # <- Updated filename

# Select relevant columns (updated column names)
data = dataset[['SquareFootage', 'Price']].copy()

# Clean 'SquareFootage' (not needed here, but keeping it for safety)
def convert_sqft(x):
    try:
        return float(x)
    except:
        if '-' in str(x):
            parts = x.split('-')
            return (float(parts[0]) + float(parts[1])) / 2
        return np.nan

data['SquareFootage'] = data['SquareFootage'].apply(convert_sqft)
data.dropna(inplace=True)

# Features and target
X = data[['SquareFootage']].values
y = data[['Price']].values

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)
y = imputer.fit_transform(y)

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Train the model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Evaluate the model
r2_score = regressor.score(X_test, y_test)
print(f"Model Accuracy (R² Score): {r2_score:.4f}")

# Save the model and scaler
joblib.dump(regressor, "house_price_model.pkl")
joblib.dump(scaler, "house_price_scaler.pkl")
print("Model and scaler saved successfully.")

# Plotting - Training Set
plt.figure(figsize=(10, 6))
plt.scatter(X_train, y_train, color="red", label="Training Data")
plt.plot(X_train, regressor.predict(X_train), color="blue", label="Regression Line")
plt.title("Square Footage vs House Price (Training Set)")
plt.xlabel("Square Footage (scaled)")
plt.ylabel("House Price")
plt.legend()
plt.grid(True)
plt.show()

# Plotting - Test Set
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color="green", label="Test Data")
plt.plot(X_train, regressor.predict(X_train), color="blue", label="Regression Line")
plt.title("Square Footage vs House Price (Test Set)")
plt.xlabel("Square Footage (scaled)")
plt.ylabel("House Price")
plt.legend()
plt.grid(True)
plt.show()

# Sample Prediction
min_sqft = 100
min_sqft_scaled = scaler.transform([[min_sqft]])
min_pred = regressor.predict(min_sqft_scaled)[0][0]
print(f"Prediction for 100 sqft: ₹{min_pred:,.2f} lakhs")
