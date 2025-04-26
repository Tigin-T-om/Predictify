
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the dataset
print("Loading dataset...")
dataset = pd.read_csv("weather_data_500.csv")

# Display basic information
print(f"Dataset shape: {dataset.shape}")
print("\nFeature statistics:")
print(dataset.describe().round(2))

# Check for missing values
missing_values = dataset.isnull().sum()
print("\nMissing values per column:")
print(missing_values)

# Select Features and Target
X = dataset.drop(columns=["temperature_c"]).values
y = dataset[["temperature_c"]].values

# Handle Missing Values
imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
X = imputer.fit_transform(X)
y = imputer.fit_transform(y)

# Split the dataset first (to avoid data leakage)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with scaling, polynomial features, and regularized regression
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('poly', PolynomialFeatures(include_bias=False)),
    ('regressor', Ridge())
])

# Parameter grid for GridSearchCV
param_grid = {
    'poly__degree': [1, 2, 3],
    'regressor__alpha': [0.1, 1.0, 10.0, 100.0]
}

# Grid search with cross-validation
print("\nPerforming grid search to find optimal parameters...")
grid_search = GridSearchCV(
    pipeline, param_grid, cv=5, 
    scoring='neg_mean_squared_error',
    verbose=1
)

grid_search.fit(X_train, y_train)

# Best parameters and model
print(f"\nBest parameters: {grid_search.best_params_}")
best_model = grid_search.best_estimator_

# Evaluate on test set
y_pred = best_model.predict(X_test)
test_mse = mean_squared_error(y_test, y_pred)
test_r2 = r2_score(y_test, y_pred)

print(f"\nTest Results:")
print(f"Mean Squared Error: {test_mse:.4f}")
print(f"R² Score: {test_r2:.4f}")
print(f"Root Mean Squared Error: {np.sqrt(test_mse):.4f}")

# Extract the pipeline components
best_degree = grid_search.best_params_['poly__degree']
best_alpha = grid_search.best_params_['regressor__alpha']

print(f"\nOptimal polynomial degree: {best_degree}")
print(f"Optimal regularization strength (alpha): {best_alpha}")

# Save the model and processors
joblib.dump(best_model, "weather_temp_model.pkl")
print("\nModel saved successfully.")

# Create a more detailed visualization
plt.figure(figsize=(12, 8))

# Prediction vs Actual plot
plt.subplot(2, 2, 1)
plt.scatter(y_test, y_pred, color="skyblue", edgecolor='k', alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("Actual Temperature (°C)")
plt.ylabel("Predicted Temperature (°C)")
plt.title("Actual vs Predicted Temperature")
plt.grid(True)

# Residual plot
plt.subplot(2, 2, 2)
residuals = y_test.ravel() - y_pred.ravel()
plt.scatter(y_test.ravel(), residuals, color="skyblue", edgecolor='k', alpha=0.6)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel("Predicted Temperature (°C)")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.grid(True)

# Residual distribution
plt.subplot(2, 2, 3)
plt.hist(residuals, bins=20, color="lightgreen", edgecolor='k')
plt.xlabel("Residual Value")
plt.ylabel("Frequency")
plt.title("Residual Distribution")
plt.grid(True)

# Feature Importance (for the top features)
if hasattr(best_model.named_steps['regressor'], 'coef_'):
    # Get feature names after polynomial transformation
    poly = best_model.named_steps['poly']
    feature_names = dataset.drop(columns=["temperature_c"]).columns
    poly_features = poly.get_feature_names_out(feature_names)
    
    # Flatten coefficients safely
    coeffs = best_model.named_steps['regressor'].coef_.ravel()
    
    # Sort by absolute magnitude
    indices = np.argsort(np.abs(coeffs))[-10:]  # Top 10 features
    plt.subplot(2, 2, 4)
    plt.barh(range(len(indices)), coeffs[indices], color="lightblue", edgecolor='k')
    plt.yticks(range(len(indices)), [poly_features[i] for i in indices])
    plt.xlabel("Coefficient Magnitude")
    plt.title("Top 10 Feature Coefficients")
    plt.grid(True)

plt.tight_layout()
plt.savefig("model_analysis.png", dpi=300)
plt.show()

# Calculate feature importances
print("\nFeature Importances:")
if hasattr(best_model.named_steps['regressor'], 'coef_'):
    poly = best_model.named_steps['poly']
    feature_names = dataset.drop(columns=["temperature_c"]).columns
    poly_features = poly.get_feature_names_out(feature_names)
    
    # Get coefficients
    coeffs = best_model.named_steps['regressor'].coef_.ravel()
    
    # Create DataFrame for better visualization
    importance_df = pd.DataFrame({
        'Feature': poly_features,
        'Coefficient': coeffs,
        'Abs_Coefficient': np.abs(coeffs)
    })
    
    # Sort by absolute value
    importance_df = importance_df.sort_values('Abs_Coefficient', ascending=False)
    
    # Print top 15 features
    print(importance_df.head(15))
