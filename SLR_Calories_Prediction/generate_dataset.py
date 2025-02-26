import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic dataset
steps = np.random.randint(1000, 20000, 500).astype(float)
calories = steps * 0.05 + np.random.normal(0, 50, 500)  # Adding some noise

# Introduce missing values
steps[np.random.choice(500, 50, replace=False)] = np.nan
calories[np.random.choice(500, 30, replace=False)] = np.nan

# Create DataFrame
dataset = pd.DataFrame({'Steps': steps, 'Calories Burned': calories})

# Save dataset as CSV file
dataset.to_csv('steps_calories.csv', index=False)

print("Dataset generated and saved as steps_calories.csv")
