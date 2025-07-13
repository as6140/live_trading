"""
Model Loading Utilities for Lean Strategies
===========================================

This module provides utilities for loading and validating ML models
in Lean strategies with proper error handling and logging.

Supports multiple ML frameworks:
- Scikit-learn models
- XGBoost models  
- LightGBM models
- TensorFlow/Keras models
- PyTorch models
- Custom pickle models
"""

import os
import pickle
import numpy as np
import pandas as pd
from typing import Any, List, Optional, Dict, Union
from datetime import datetime
import logging
import warnings

# Optional imports for different ML frameworks
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False

try:
    import tensorflow as tf
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False
    tf = None

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None

try:
    import sklearn
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress common warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)


class ModelLoader:
    """
    Enhanced model loader that supports multiple ML frameworks with better error handling.
    
    Supports:
    - XGBoost
    - LightGBM  
    - TensorFlow/Keras
    - PyTorch
    - Scikit-learn
    - Custom pickle models
    """
    
    def __init__(self, model_path: str, feature_columns: List[str]):
        """
        Initialize the ModelLoader.
        
        Args:
            model_path: Path to the trained model file
            feature_columns: List of feature column names
        """
        self.model_path = model_path
        self.feature_columns = feature_columns
        self.model = None
        self.model_type = None
        self.feature_importance = None
        self.model_metadata = {}
        
        # Performance tracking
        self.prediction_count = 0
        self.error_count = 0
        self.last_prediction_time = None
        
        # Load the model on initialization
        success, message = self.load_model()
        if not success:
            logger.error(f"Failed to load model: {message}")
            raise Exception(f"Model loading failed: {message}")
    
    def load_model(self):
        """
        Load the ML model from the specified path.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Check if file exists
            if not os.path.exists(self.model_path):
                return False, f"Model file not found: {self.model_path}"
            
            # Load the model
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            # Handle different model formats
            if isinstance(model_data, dict):
                # Model with metadata
                self.model = model_data.get('model')
                self.model_metadata = model_data.get('metadata', {})
                self.feature_importance = model_data.get('feature_importance')
            else:
                # Direct model object
                self.model = model_data
            
            # Validate model
            validation_success, validation_message = self._validate_model()
            if not validation_success:
                return False, validation_message
            
            # Determine model type
            self._determine_model_type()
            
            logger.info(f"Successfully loaded {self.model_type} model from {self.model_path}")
            return True, f"Model loaded successfully: {self.model_type}"
            
        except Exception as e:
            error_msg = f"Error loading model: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _validate_model(self):
        """
        Validate the loaded model.
        
        Returns:
            Tuple of (success, message)
        """
        if self.model is None:
            return False, "Model is None after loading"
        
        # Check if model has predict method
        if not self._has_predict_method():
            return False, "Model does not have a predict method"
        
        # Test prediction with dummy data
        try:
            dummy_features = np.random.random((1, len(self.feature_columns)))
            _ = self._safe_predict(dummy_features)
            return True, "Model validation successful"
        except Exception as e:
            return False, f"Model validation failed: {str(e)}"
    
    def _determine_model_type(self):
        """Determine the type of loaded model."""
        model_class = self.model.__class__.__name__
        module_name = self.model.__class__.__module__
        
        if 'xgboost' in module_name:
            self.model_type = 'XGBoost'
        elif 'lightgbm' in module_name:
            self.model_type = 'LightGBM'
        elif 'tensorflow' in module_name or 'keras' in module_name:
            self.model_type = 'TensorFlow'
        elif 'torch' in module_name:
            self.model_type = 'PyTorch'
        elif 'sklearn' in module_name:
            self.model_type = 'Scikit-learn'
        else:
            self.model_type = f'Custom ({model_class})'
    
    def _has_predict_method(self) -> bool:
        """Check if model has predict method."""
        return hasattr(self.model, 'predict') and callable(getattr(self.model, 'predict'))
    
    def _safe_predict(self, features: np.ndarray) -> Optional[Union[float, np.ndarray]]:
        """
        Safely make predictions with error handling.
        
        Args:
            features: Input features for prediction
            
        Returns:
            Prediction result or None if failed
        """
        try:
            # Handle different model types
            if self.model_type == 'TensorFlow':
                # TensorFlow/Keras models
                prediction = self.model.predict(features, verbose=0)
                return prediction.flatten() if len(prediction.shape) > 1 else prediction
            elif self.model_type == 'PyTorch':
                # PyTorch models
                import torch
                with torch.no_grad():
                    tensor_features = torch.FloatTensor(features)
                    prediction = self.model(tensor_features)
                    return prediction.numpy()
            else:
                # Standard sklearn-compatible models
                return self.model.predict(features)
                
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return None
    
    def predict(self, features: np.ndarray) -> Optional[float]:
        """
        Make a prediction using the loaded model.
        
        Args:
            features: Input features as numpy array
            
        Returns:
            Prediction value or None if failed
        """
        try:
            # Validate input
            if features is None or len(features) == 0:
                logger.warning("Empty features provided for prediction")
                return None
            
            # Ensure features are 2D
            if features.ndim == 1:
                features = features.reshape(1, -1)
            
            # Check feature count
            if features.shape[1] != len(self.feature_columns):
                logger.error(f"Feature count mismatch: expected {len(self.feature_columns)}, got {features.shape[1]}")
                return None
            
            # Handle NaN values
            if np.any(np.isnan(features)):
                logger.warning("NaN values detected in features, replacing with 0")
                features = np.nan_to_num(features)
            
            # Make prediction
            prediction = self._safe_predict(features)
            
            if prediction is None:
                self.error_count += 1
                return None
            
            # Handle different prediction formats
            if isinstance(prediction, np.ndarray):
                result = float(prediction[0]) if len(prediction) > 0 else 0.0
            else:
                result = float(prediction)
            
            # Update tracking
            self.prediction_count += 1
            self.last_prediction_time = datetime.now()
            
            # Clamp extreme values for safety
            if abs(result) > 1e6:
                logger.warning(f"Extreme prediction value detected: {result}, clamping to [-1e6, 1e6]")
                result = np.clip(result, -1e6, 1e6)
            
            return result
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            self.error_count += 1
            return None
    
    def predict_proba(self, features: np.ndarray) -> Optional[np.ndarray]:
        """
        Get prediction probabilities (for classification models).
        
        Args:
            features: Input features as numpy array
            
        Returns:
            Prediction probabilities or None if failed
        """
        try:
            if not hasattr(self.model, 'predict_proba'):
                logger.warning("Model does not support predict_proba")
                return None
            
            # Ensure features are 2D
            if features.ndim == 1:
                features = features.reshape(1, -1)
            
            # Handle NaN values
            if np.any(np.isnan(features)):
                features = np.nan_to_num(features)
            
            probabilities = self.model.predict_proba(features)
            return probabilities
            
        except Exception as e:
            logger.error(f"Probability prediction failed: {str(e)}")
            return None
    
    def get_feature_importance(self) -> Optional[Dict[str, float]]:
        """
        Get feature importance if available.
        
        Returns:
            Dictionary of feature importance or None
        """
        try:
            # Return cached importance if available
            if self.feature_importance is not None:
                return self.feature_importance
            
            # Try to get from model
            importance = None
            if hasattr(self.model, 'feature_importances_'):
                importance = self.model.feature_importances_
            elif hasattr(self.model, 'feature_importance'):
                importance = self.model.feature_importance()
            elif hasattr(self.model, 'coef_'):
                importance = np.abs(self.model.coef_).flatten()
            
            if importance is not None and len(importance) == len(self.feature_columns):
                self.feature_importance = dict(zip(self.feature_columns, importance))
                return self.feature_importance
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get feature importance: {str(e)}")
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information and statistics.
        
        Returns:
            Dictionary containing model information
        """
        info = {
            'model_type': self.model_type,
            'model_path': self.model_path,
            'feature_count': len(self.feature_columns),
            'prediction_count': self.prediction_count,
            'error_count': self.error_count,
            'error_rate': self.error_count / max(self.prediction_count, 1),
            'last_prediction_time': self.last_prediction_time,
            'has_feature_importance': self.get_feature_importance() is not None,
            'metadata': self.model_metadata
        }
        
        return info
    
    def reload_model(self):
        """
        Reload the model from disk.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Reset state
            self.model = None
            self.model_type = None
            self.feature_importance = None
            self.model_metadata = {}
            
            # Reload
            return self.load_model()
            
        except Exception as e:
            error_msg = f"Failed to reload model: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def save_model_with_metadata(self, model: Any, metadata: Dict[str, Any], 
                                output_path: str) -> bool:
        """
        Save model with metadata.
        
        Args:
            model: The model to save
            metadata: Metadata dictionary
            output_path: Path to save the model
            
        Returns:
            True if successful, False otherwise
        """
        try:
            model_data = {
                'model': model,
                'metadata': metadata,
                'feature_columns': self.feature_columns,
                'save_time': datetime.now().isoformat()
            }
            
            # Add feature importance if available
            if hasattr(model, 'feature_importances_'):
                model_data['feature_importance'] = dict(zip(
                    self.feature_columns, 
                    model.feature_importances_
                ))
            
            with open(output_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Model saved successfully to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save model: {str(e)}")
            return False


class FallbackPredictor:
    """
    Fallback predictor that provides simple predictions when main model fails.
    """
    
    def __init__(self, feature_columns: List[str]):
        """Initialize with feature columns."""
        self.feature_columns = feature_columns
        self.call_count = 0
    
    def predict(self, features: np.ndarray) -> float:
        """
        Provide a simple fallback prediction.
        
        For trading, we'll return a neutral signal (0.0) as fallback.
        This represents "no position" or "hold" recommendation.
        
        Args:
            features: Input features (unused in fallback)
            
        Returns:
            Neutral prediction (0.0)
        """
        self.call_count += 1
        
        # Log occasional warnings about fallback usage
        if self.call_count % 100 == 1:
            logger.warning(f"Using fallback predictor (call #{self.call_count})")
        
        # Return neutral signal
        return 0.0
    
    def get_info(self) -> Dict[str, Any]:
        """Get fallback predictor information."""
        return {
            'type': 'FallbackPredictor',
            'call_count': self.call_count,
            'feature_columns': self.feature_columns
        }


def create_model_loader(model_path: str, feature_columns: List[str]) -> ModelLoader:
    """
    Factory function to create a ModelLoader instance.
    
    Args:
        model_path: Path to the model file
        feature_columns: List of feature column names
        
    Returns:
        ModelLoader instance
    """
    return ModelLoader(model_path, feature_columns) 