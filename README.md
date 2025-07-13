# 🚀 AI-Driven Quant Trading Platform

A professional, end-to-end algorithmic trading system built with Python, Lean, and QuantConnect. This platform enables design, testing, deployment, and management of multiple ML-driven trading strategies with comprehensive risk management and monitoring.

## 🎯 Purpose

This repository contains a complete quant trading infrastructure for:
- **Strategy Development**: ML-driven alpha generation with proper backtesting
- **Risk Management**: Monte Carlo simulations, regime detection, and portfolio optimization
- **Paper Trading**: Safe strategy validation before live deployment
- **Live Trading**: Professional-grade execution with monitoring and alerts
- **Compliance**: Tax optimization and regulatory compliance (NYC, $245K W-2 bracket)

## 📁 Repository Structure

```
live_trading/
├── lean_workspace/         # All QuantConnect Lean projects (Full Independence)
│   ├── FirstMLTest/       # Self-contained ML strategy (working example)
│   ├── TestStrategy/      # Self-contained copy of FirstMLTest
│   ├── lean.json          # Lean configuration
│   └── data/              # QuantConnect data
├── models/                # ML model training and storage
│   ├── bayesian/          # Bayesian/probabilistic models
│   ├── regime/            # Regime switching models
│   └── rl/                # Reinforcement learning models
├── data/                  # Data processing and labeling
│   └── labeler/           # Labeling logic and tools
├── notebooks/             # Research and analysis notebooks
├── dashboards/            # Streamlit monitoring dashboards
├── portfolio/             # Portfolio optimization tools
├── backtests/             # Backtest results and reports
├── risk_reports/          # Monte Carlo and risk analysis
├── monitoring/            # System monitoring and alerts
├── tax/                   # Tax optimization and tracking
├── reports/               # Performance and analysis reports
├── logs/                  # System logs and postmortems
│   └── postmortems/       # Failure analysis documentation
├── quant-trading-env/     # Python virtual environment
├── requirements.txt       # Python dependencies
├── Makefile              # Build and deployment automation
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone repository
git clone <your-repo-url>
cd live_trading

# Create virtual environment with Python 3.11.13
python3.11 -m venv quant-trading-env --upgrade-deps
source quant-trading-env/bin/activate  # On Windows: quant-trading-env\Scripts\activate

# Install TA-Lib (required for technical analysis)
# On macOS:
brew install ta-lib

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import talib; print('TA-Lib installed successfully')"
```

### 2. QuantConnect Setup
```bash
# Initialize Lean workspace (requires paid QuantConnect account)
cd lean_workspace
lean init --organization="Your Organization Name" --language=python

# Note: FirstMLTest already exists as a working example
# If you need to create a new project from scratch:
# lean create-project "MyNewStrategy"
```

### 3. Account Requirements
- **QuantConnect**: Paid account required for API access and cloud backtesting
- **Python**: Version 3.11.13 (3.13+ has compatibility issues with ML libraries)
- **Operating System**: macOS, Linux, or Windows with WSL2
- **Docker**: Only required for local live trading (Intel/AMD64 only)
  - **macOS**: Docker Desktop or colima (lightweight alternative)
  - **ARM Macs (M1/M2/M3)**: Use QuantConnect cloud deployment instead
  - **Cloud deployment**: No Docker required

### 4. Strategy Development Workflow (Full Independence)
```bash
# 1. List available strategies to copy from
make list-strategies
# Shows: FirstMLTest, TestStrategy

# 2. Create new strategy by copying existing one
make copy-strategy FROM=FirstMLTest TO=MyMomentumStrategy

# 3. Edit the new strategy
# Edit lean_workspace/MyMomentumStrategy/main.py to customize

# 4. Push to QuantConnect cloud
make lean-cloud-push PROJECT=MyMomentumStrategy

# 5. Run cloud backtest
make lean-backtest PROJECT=MyMomentumStrategy

# 6. Run parameter optimization (optional)
make lean-optimize PROJECT=MyMomentumStrategy

# 7. Monitor results via QuantConnect web interface
```

### 5. Parameter Optimization
```bash
# Optimize strategy parameters to find best combinations
make lean-optimize PROJECT=MyMomentumStrategy

# Or use QuantConnect web interface "Optimize Project" button
# - Define parameters in config.json or strategy code
# - QuantConnect tests multiple parameter combinations
# - Results show optimal settings for maximum performance
```

### 6. Live Trading Deployment Options

#### Cloud Deployment (Recommended for ARM Macs)
```bash
# Push strategy to QuantConnect cloud
make lean-cloud-push PROJECT=MyMomentumStrategy

# Deploy via QuantConnect web interface:
# 1. Go to your project in QuantConnect
# 2. Click "Deploy Live" tab
# 3. Configure brokerage settings (IBKR, etc.)
# 4. Click "Deploy" button
# 5. Monitor via QuantConnect dashboard
```

#### Local Deployment (Intel/AMD64 only)
```bash
# Install Docker (if not already installed)
# macOS: brew install colima docker  # Lightweight alternative
# or: brew install --cask docker     # Docker Desktop

# Start Docker service
colima start  # For colima users
# or start Docker Desktop

# Deploy locally
cd lean_workspace
lean live "MyStrategy" --environment "live-interactive"

# Note: ARM Macs (M1/M2/M3) not supported for IBKR local deployment
```

## 🔧 Makefile Commands

### 7. Core Commands
| Command | Description |
|---------|-------------|
| `make build` | Install dependencies and setup environment |
| `make test` | Run all tests and validations |
| `make clean` | Clean temporary files and logs |

### 8. Strategy Management (Full Independence)
| Command | Description |
|---------|-------------|
| `make list-strategies` | List available strategies to copy from |
| `make copy-strategy FROM=source TO=target` | Create new strategy by copying existing one |
| `make create-first-strategy` | Create your first ML strategy (one-time only) |

### 9. Lean-Specific Commands
| Command | Description |
|---------|-------------|
| `make lean-backtest PROJECT=project_name` | Run cloud backtest for specific project |
| `make lean-optimize PROJECT=project_name` | Run parameter optimization for specific project |
| `make lean-cloud-push PROJECT=project_name` | Push project to QuantConnect cloud |
| `make lean-cloud-pull` | Sync all projects from QuantConnect cloud |
| `make lean-research PROJECT=project_name` | Open Jupyter notebook for research |

### 10. Development Commands
| Command | Description |
|---------|-------------|
| `make lint` | Run code linting and formatting |
| `make format` | Format code with Black and isort |
| `make backup` | Create backup of all important files |

## 🏗️ Full Independence Architecture

### 11. Architecture Overview

This project uses a **Full Independence** approach where:

1. **Each strategy is completely self-contained** - no shared dependencies
2. **No templates or shared utilities** - eliminates complexity and dependencies
3. **Copy from existing strategies** - proven strategies become the foundation for new ones
4. **Independent evolution** - each strategy can be modified without affecting others

### Benefits:
- ✅ **Zero Dependencies**: No strategy depends on shared code
- ✅ **Maximum Safety**: Changes to one strategy cannot break others
- ✅ **Easy Deployment**: Each strategy is a complete, deployable unit
- ✅ **Version Independence**: Each strategy can use different versions of utilities
- ✅ **Bulletproof Backtesting**: Each strategy's backtests are completely isolated
- ✅ **Professional Approach**: How real trading firms structure their strategies

### Philosophy:
- **Code duplication is better than dependencies** for trading systems
- **Successful strategies become templates** for new ones
- **Independence trumps code elegance** when money is on the line
- **Each strategy is a fortress** - completely isolated and protected 