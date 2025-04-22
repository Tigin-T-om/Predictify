import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import joblib

class HousePricePredictor:
    def __init__(self, model_path='house_model.pkl'):
        self.min_sqft = 900
        self.max_sqft = 5000
        self.min_price = 10  # Minimum realistic price in lakhs
        self.max_price = 500  # Maximum realistic price in lakhs
        
        # Load the trained model
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Model file {model_path} not found")
            
        # Create preprocessing pipeline
        self.pipeline = Pipeline([
            ('log_transform', FunctionTransformer(np.log1p)),
            ('model', self.model)
        ])
        
    def validate_input(self, sqft):
        """Validate input square footage"""
        if not isinstance(sqft, (int, float)):
            raise ValueError("Square footage must be a number")
            
        if sqft < self.min_sqft:
            raise ValueError(f"Square footage must be at least {self.min_sqft} sqft")
            
        if sqft > self.max_sqft:
            raise ValueError(f"Square footage must be at most {self.max_sqft} sqft")
            
        return float(sqft)
        
    def predict(self, sqft):
        """Make a prediction with input validation and transformation"""
        try:
            # Validate input
            sqft = self.validate_input(sqft)
            
            # Transform and predict
            prediction = self.pipeline.predict([[sqft]])[0]
            
            # Apply domain knowledge constraints
            prediction = max(self.min_price, min(self.max_price, prediction))
            
            # Check if prediction was capped
            warning = None
            if prediction in [self.min_price, self.max_price]:
                warning = "Prediction capped to realistic range"
                
            return {
                'prediction': prediction,
                'warning': warning,
                'input_validated': True
            }
            
        except ValueError as e:
            return {
                'error': str(e),
                'input_validated': False
            }
        except Exception as e:
            return {
                'error': f"Prediction failed: {str(e)}",
                'input_validated': False
            } 