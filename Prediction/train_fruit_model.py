import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the dataset
df = pd.read_csv("fruit_data.csv")  # replace with your actual file path

# Features and label
X = df[['mass', 'width', 'height', 'color_score']]
y = df['fruit_name']  # or use 'fruit_label' if preferred

# Encode the fruit names to numbers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Save label classes for future reference
fruit_classes = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
print("Fruit classes:", fruit_classes)

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

# Train KNN model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Predictions
y_pred = knn.predict(X_test)

# Evaluation
print("Accuracy Score:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save model and scaler
joblib.dump(knn, "fruit_knn_model.pkl")
joblib.dump(scaler, "fruit_scaler.pkl")
joblib.dump(label_encoder, "fruit_label_encoder.pkl")

print("Model, scaler, and label encoder saved successfully.")
