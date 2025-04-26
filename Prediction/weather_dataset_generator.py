import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Function to generate realistic weather data
def generate_weather_dataset(num_records=500):
    # Start date
    start_date = datetime(2022, 1, 1)
    
    # Create empty dataframe
    data = []
    
    # Generate data for each day
    for i in range(num_records):
        current_date = start_date + timedelta(hours=i)
        
        # Base temperature with seasonal pattern
        season_factor = np.sin(2 * np.pi * (current_date.timetuple().tm_yday / 365))
        base_temp = 15 + 10 * season_factor
        
        # Daily variation (cooler at night, warmer during day)
        hour_factor = np.sin(2 * np.pi * (current_date.hour / 24) - np.pi/2)
        hour_variation = 5 * hour_factor
        
        # Random variation
        random_variation = np.random.normal(0, 2)
        
        # Calculate actual temperature
        temperature = base_temp + hour_variation + random_variation
        
        # Generate other features with realistic correlations
        humidity = max(min(0.7 - 0.3 * hour_factor + 0.2 * season_factor + np.random.normal(0, 0.1), 1.0), 0.3)
        wind_speed = max(5 + 3 * np.random.normal(0, 1) + 2 * abs(season_factor), 0)
        wind_bearing = random.randint(0, 359)
        visibility = max(min(15 - 5 * humidity + np.random.normal(0, 2), 20), 0.5)
        cloud_cover = max(min(humidity * 0.8 + np.random.normal(0, 0.1), 1.0), 0.0)
        pressure = 1013 + 5 * season_factor + np.random.normal(0, 2)
        
        # Apparent temperature (feels like)
        wind_chill = 0
        if temperature < 10 and wind_speed > 4.8:
            wind_chill = 13.12 + 0.6215 * temperature - 11.37 * (wind_speed ** 0.16) + 0.3965 * temperature * (wind_speed ** 0.16)
            wind_chill = temperature - (temperature - wind_chill)
        
        heat_index = 0
        if temperature > 20 and humidity > 0.4:
            heat_index = temperature + 0.5 * (humidity * 10)
        
        apparent_temp = temperature
        if wind_chill != 0:
            apparent_temp = wind_chill
        elif heat_index != 0:
            apparent_temp = heat_index
        
        # Precipitation type (0: none, 1: rain, 2: snow)
        precip_prob = min(max(humidity - 0.4 + 0.1 * np.random.normal(0, 1), 0), 1)
        if precip_prob > 0.7:
            if temperature < 2:  # Snow
                precip_type = 2
            else:  # Rain
                precip_type = 1
        else:  # None
            precip_type = 0
        
        # Add to dataset
        data.append({
            'temperature_c': round(temperature, 2),
            'apparent_temperature_c': round(apparent_temp, 2),
            'humidity': round(humidity, 2),
            'wind_speed_km/h': round(wind_speed, 2),
            'wind_bearing_degrees': wind_bearing,
            'visibility_km': round(visibility, 2),
            'cloud_cover': round(cloud_cover, 2),
            'pressure_millibars': round(pressure, 2),
            'year': current_date.year,
            'month': current_date.month,
            'day': current_date.day,
            'hour': current_date.hour,
            'precip_type_encoded': precip_type
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

# Generate the dataset
weather_df = generate_weather_dataset(500)

# Save to CSV
weather_df.to_csv("weather_data_500.csv", index=False)
print(f"Generated weather dataset with {len(weather_df)} records.")
print(f"Sample data:")
print(weather_df.head())