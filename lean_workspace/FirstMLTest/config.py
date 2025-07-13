"""
Strategy Configuration Template
==============================

This file contains all configurable parameters for the strategy template.
Customize these values for your specific strategy implementation.
"""

from datetime import datetime
from typing import List, Dict, Any

# ==================== BASIC STRATEGY SETTINGS ====================

# Strategy identification
STRATEGY_NAME = "TemplateStrategy"
STRATEGY_VERSION = "1.0.0"
STRATEGY_DESCRIPTION = "Template strategy for ML-driven trading"

# Backtest settings
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2023, 12, 31)
INITIAL_CASH = 100000

# ==================== TRADING PARAMETERS ====================

# Symbols to trade
SYMBOLS = [
    "SPY",   # S&P 500 ETF
    "QQQ",   # Nasdaq 100 ETF
    "IWM",   # Russell 2000 ETF
    "EFA",   # Developed Markets ETF
    "EEM",   # Emerging Markets ETF
]

# Rebalancing settings
REBALANCE_FREQUENCY = 5  # Days between rebalances
REBALANCE_HOUR = 10     # Hour of day to rebalance (market time)
REBALANCE_MINUTE = 0    # Minute of hour to rebalance

# Position sizing
MAX_POSITION_SIZE = 0.10        # Maximum 10% per position
MAX_TOTAL_ALLOCATION = 0.80     # Maximum 80% total invested
MIN_TRADE_SIZE = 0.01           # Minimum 1% position change to trade

# ==================== RISK MANAGEMENT ====================

# Drawdown protection
MAX_DRAWDOWN_THRESHOLD = 0.15   # 15% max drawdown before protection
DRAWDOWN_REDUCTION_FACTOR = 0.5 # Reduce positions by 50% during drawdown
DRAWDOWN_RECOVERY_THRESHOLD = 0.075  # 7.5% recovery before resuming

# Volatility management
HIGH_VOLATILITY_THRESHOLD = 0.02    # 2% daily volatility threshold
VOLATILITY_ADJUSTMENT_FACTOR = 0.5  # Reduce positions by 50% in high vol

# Risk-free rate for calculations
RISK_FREE_RATE = 0.02  # 2% annual risk-free rate

# ==================== MODEL SETTINGS ====================

# Model file path (relative to strategy directory)
MODEL_PATH = "model.pkl"

# Supported model types
SUPPORTED_MODEL_TYPES = [
    'sklearn',      # Scikit-learn models
    'xgboost',      # XGBoost models
    'lightgbm',     # LightGBM models
    'tensorflow',   # TensorFlow/Keras models
    'pytorch',      # PyTorch models
    'custom'        # Custom pickle models
]

# Feature columns (must match model training)
FEATURE_COLUMNS = [
    'returns_1d',      # 1-day return
    'returns_5d',      # 5-day return
    'returns_20d',     # 20-day return
    'rsi',             # RSI indicator (0-1)
    'bb_position',     # Bollinger Band position (0-1)
    'macd_signal',     # MACD signal (-1/+1)
    'volume_ratio',    # Volume vs average
    'volatility',      # Price volatility
    'momentum',        # Price momentum
    'trend_strength',  # Trend strength (ADX)
]

# Feature engineering settings
FEATURE_CLIPPING = {
    'returns_1d': (-0.2, 0.2),
    'returns_5d': (-0.5, 0.5),
    'returns_20d': (-1.0, 1.0),
    'volume_ratio': (0.1, 10.0),
    'volatility': (0.0, 0.1),
    'momentum': (-0.5, 0.5)
}

# Prediction settings
PREDICTION_THRESHOLD = 0.1      # Minimum prediction confidence
USE_PREDICTION_PROBABILITIES = True  # Use probabilities if available
PREDICTION_SMOOTHING = 0.1      # Exponential smoothing factor
CONFIDENCE_SCALING = True       # Scale predictions by confidence
FALLBACK_ON_MODEL_FAILURE = True  # Use fallback predictor if model fails

# ==================== TECHNICAL INDICATORS ====================

# Indicator parameters
INDICATORS = {
    'sma_short': 20,     # Short-term SMA period
    'sma_long': 50,      # Long-term SMA period
    'rsi_period': 14,    # RSI period
    'bb_period': 20,     # Bollinger Bands period
    'bb_std': 2,         # Bollinger Bands standard deviations
    'macd_fast': 12,     # MACD fast period
    'macd_slow': 26,     # MACD slow period
    'macd_signal': 9,    # MACD signal period
    'atr_period': 14,    # ATR period
    'stoch_period': 14,  # Stochastic period
    'momentum_period': 10,  # Momentum period
    'roc_period': 10,    # Rate of change period
    'adx_period': 14,    # ADX period
}

# ==================== FEATURE ENGINEERING ====================

# Data history requirements
LOOKBACK_PERIOD = 100       # Days of price history to keep
MIN_HISTORY_REQUIRED = 20   # Minimum days before generating features

# Feature normalization
NORMALIZE_FEATURES = True
FEATURE_SCALING_METHOD = 'standard'  # 'standard', 'minmax', 'robust'

# Volume calculations
VOLUME_LOOKBACK = 10  # Days for volume average calculation

# ==================== LOGGING & MONITORING ====================

# Logging settings
LOG_LEVEL = "INFO"  # "DEBUG", "INFO", "WARNING", "ERROR"
LOG_PREDICTIONS = True
LOG_TRADES = True
LOG_RISK_METRICS = True

# Performance tracking
TRACK_FEATURE_IMPORTANCE = True
TRACK_PREDICTION_ACCURACY = True
CALCULATE_ATTRIBUTION = True

# ==================== MARKET REGIMES ====================

# Trend detection
TREND_LOOKBACK = 50      # Days for trend calculation
TREND_THRESHOLD = 0.02   # 2% threshold for trend detection

# Volatility regimes
VOLATILITY_LOOKBACK = 20  # Days for volatility calculation
LOW_VOL_THRESHOLD = 0.01  # 1% daily vol = low volatility
HIGH_VOL_THRESHOLD = 0.03 # 3% daily vol = high volatility

# ==================== PORTFOLIO OPTIMIZATION ====================

# Optimization settings (if using portfolio optimizer)
OPTIMIZATION_FREQUENCY = 20  # Days between portfolio optimization
OPTIMIZATION_LOOKBACK = 252  # Days of data for optimization
OPTIMIZATION_METHOD = 'sharpe'  # 'sharpe', 'min_vol', 'max_return'

# Correlation management
MAX_CORRELATION = 0.8    # Maximum correlation between positions
CORRELATION_LOOKBACK = 60  # Days for correlation calculation

# ==================== TRANSACTION COSTS ====================

# Trading costs (adjust based on broker)
COMMISSION_PER_TRADE = 0.0    # Commission per trade
SPREAD_COST = 0.0005          # Bid-ask spread cost (0.05%)
MARKET_IMPACT = 0.0010        # Market impact cost (0.10%)

# ==================== SAFETY & VALIDATION ====================

# Model validation
VALIDATE_MODEL_ON_LOAD = True
REQUIRE_MODEL_METADATA = False
FALLBACK_TO_SIMPLE_STRATEGY = True

# Data validation
VALIDATE_FEATURES = True
CHECK_DATA_QUALITY = True
HANDLE_MISSING_DATA = True

# Emergency controls
ENABLE_KILL_SWITCH = True
MAX_DAILY_LOSS = 0.05        # 5% max daily loss
MAX_MONTHLY_LOSS = 0.15      # 15% max monthly loss

# ==================== ADVANCED SETTINGS ====================

# Machine learning
USE_ENSEMBLE_PREDICTION = False  # Average multiple models
ENSEMBLE_WEIGHTS = [1.0]        # Weights for ensemble models
RETRAIN_FREQUENCY = 30          # Days between model retraining

# Model validation and robustness
CROSS_VALIDATION_FOLDS = 5      # K-fold CV for model validation
USE_PURGED_CV = True            # Use purged cross-validation for time series
VALIDATION_WINDOW = 252         # Days for rolling validation

# Bayesian optimization for hyperparameters
USE_BAYESIAN_OPTIMIZATION = False  # Use Optuna for hyperparameter tuning
OPTIMIZATION_TRIALS = 100       # Number of optimization trials
OPTIMIZATION_TIMEOUT = 3600     # Timeout in seconds

# Model explainability
CALCULATE_SHAP_VALUES = False   # Calculate SHAP feature importance
TRACK_FEATURE_DRIFT = True      # Monitor feature distribution drift
FEATURE_IMPORTANCE_THRESHOLD = 0.01  # Minimum importance to consider

# Regime switching
USE_REGIME_DETECTION = False    # Enable regime-based model switching
REGIME_MODELS = {}              # Different models for different regimes
REGIME_DETECTION_METHOD = 'hmm'  # 'hmm', 'volatility', 'returns'

# Reinforcement learning
USE_RL_POSITION_SIZING = False  # Use RL for position sizing
RL_MODEL_PATH = "rl_model.pkl"  # Path to RL model
RL_ENVIRONMENT = 'gym'          # 'gym', 'custom'
RL_ALGORITHM = 'ppo'            # 'ppo', 'dqn', 'a2c'

# Probabilistic modeling
USE_BAYESIAN_MODELS = False     # Use PyMC for Bayesian modeling
MCMC_SAMPLES = 1000            # Number of MCMC samples
UNCERTAINTY_ESTIMATION = True   # Estimate prediction uncertainty

# ==================== NOTIFICATION SETTINGS ====================

# Alerts
SEND_TRADE_ALERTS = True
SEND_RISK_ALERTS = True
SEND_PERFORMANCE_ALERTS = True

# Notification channels
SLACK_WEBHOOK = None    # Slack webhook URL
EMAIL_ALERTS = None     # Email address for alerts
DISCORD_WEBHOOK = None  # Discord webhook URL

# ==================== DEVELOPMENT & TESTING ====================

# Development mode
DEBUG_MODE = False
PAPER_TRADING = True
SIMULATE_LATENCY = False

# Testing
ENABLE_BACKTESTING = True
SAVE_BACKTEST_DATA = True
GENERATE_REPORTS = True

# ==================== HELPER FUNCTIONS ====================

def get_symbol_config(symbol: str) -> Dict[str, Any]:
    """Get symbol-specific configuration if needed."""
    symbol_configs = {
        'SPY': {'max_position': 0.20, 'rebalance_threshold': 0.02},
        'QQQ': {'max_position': 0.15, 'rebalance_threshold': 0.02},
        'IWM': {'max_position': 0.10, 'rebalance_threshold': 0.03},
        'EFA': {'max_position': 0.10, 'rebalance_threshold': 0.03},
        'EEM': {'max_position': 0.08, 'rebalance_threshold': 0.03},
    }
    return symbol_configs.get(symbol, {
        'max_position': MAX_POSITION_SIZE,
        'rebalance_threshold': MIN_TRADE_SIZE
    })

def get_risk_config() -> Dict[str, Any]:
    """Get risk management configuration."""
    return {
        'max_drawdown': MAX_DRAWDOWN_THRESHOLD,
        'max_position_size': MAX_POSITION_SIZE,
        'max_total_allocation': MAX_TOTAL_ALLOCATION,
        'volatility_threshold': HIGH_VOLATILITY_THRESHOLD,
        'risk_free_rate': RISK_FREE_RATE,
    }

def get_model_config() -> Dict[str, Any]:
    """Get model configuration."""
    return {
        'model_path': MODEL_PATH,
        'feature_columns': FEATURE_COLUMNS,
        'prediction_threshold': PREDICTION_THRESHOLD,
        'use_probabilities': USE_PREDICTION_PROBABILITIES,
        'validate_on_load': VALIDATE_MODEL_ON_LOAD,
    }

def validate_config() -> bool:
    """Validate configuration settings."""
    # Check that position sizes don't exceed limits
    if MAX_POSITION_SIZE > 1.0:
        raise ValueError("MAX_POSITION_SIZE cannot exceed 1.0")
    
    if MAX_TOTAL_ALLOCATION > 1.0:
        raise ValueError("MAX_TOTAL_ALLOCATION cannot exceed 1.0")
    
    # Check that we have symbols defined
    if not SYMBOLS:
        raise ValueError("SYMBOLS list cannot be empty")
    
    # Check that feature columns are defined
    if not FEATURE_COLUMNS:
        raise ValueError("FEATURE_COLUMNS list cannot be empty")
    
    # Check date consistency
    if START_DATE >= END_DATE:
        raise ValueError("START_DATE must be before END_DATE")
    
    return True

# Validate configuration on import
validate_config() 