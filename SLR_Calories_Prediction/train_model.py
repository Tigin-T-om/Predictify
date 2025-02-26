import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Load Dataset
dataset = pd.read_csv('D:\projects\SLR\SLR_Calories_Prediction\steps_calories.csv')
X = dataset.iloc[:, 0:1].values
y = dataset.iloc[:, 1:2].values

# Handle missing values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
X = imputer.fit_transform(X)
y = imputer.fit_transform(y)

# Split dataset into training (70%) and testing (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Train Linear Regression Model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Save the trained model
joblib.dump(regressor, "slr_model.pkl")
print("Model trained and saved as slr_model.pkl")

# Predict Test Data
y_pred = regressor.predict(X_test)

r2_score = regressor.score(X_test, y_test)
print(f"Model Accuracy (R² Score): {r2_score:.4f}")

# Plot Training Set
plt.scatter(X_train, y_train, color="red")
plt.plot(X_train, regressor.predict(X_train), color="blue")
plt.title("Steps vs Calories Burned (Training Set)")
plt.xlabel("Steps")
plt.ylabel("Calories Burned")
plt.show()

# Plot Test Set
plt.scatter(X_test, y_test, color="red")
plt.plot(X_train, regressor.predict(X_train), color="blue")
plt.title("Steps vs Calories Burned (Test Set)")
plt.xlabel("Steps")
plt.ylabel("Calories Burned")
plt.show()
