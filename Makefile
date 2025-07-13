# AI-Driven Quant Trading Platform Makefile
# Usage: make [target]

.PHONY: help build test train backtest deploy report monitor clean new-strategy

# Default target
help:
	@echo "🚀 AI-Driven Quant Trading Platform"
	@echo "Available targets:"
	@echo "  build         - Install dependencies and setup environment"
	@echo "  setup-creds   - Setup credentials safely using templates"
	@echo "  test          - Run all tests and validations"
	@echo "  train         - Train all models with current data"
	@echo "  backtest      - Run backtests for all strategies"
	@echo "  deploy        - Deploy strategies to paper trading"
	@echo "  report        - Generate performance reports"
	@echo "  monitor       - Launch monitoring dashboard"
	@echo "  clean         - Clean temporary files and logs"
	@echo "  copy-strategy - Create new strategy from existing one (FROM=source TO=target)"
	@echo "  list-strategies - List available strategies to copy from"
	@echo "  lean-optimize - Run parameter optimization (PROJECT=project_name)"
	@echo ""
	@echo "📋 First time? See FIRST_TIME_SETUP.md for complete setup guide"
	@echo ""
	@echo "Example: make copy-strategy FROM=FirstMLTest TO=MyMomentumStrategy"
	@echo "Example: make lean-optimize PROJECT=FirstMLTest"

# Environment setup
build:
	@echo "🔧 Setting up environment..."
	python3.11 -m venv quant-trading-env --upgrade-deps
	@echo "📦 Installing dependencies..."
	quant-trading-env/bin/pip install -r requirements.txt
	@echo "✅ Environment setup complete!"

# Credential setup
setup-creds:
	@echo "🔐 Setting up credentials safely..."
	python setup_credentials.py
	@echo "⚠️  Remember to edit .env file with your actual credentials!"

# Testing
test:
	@echo "🧪 Running tests..."
	quant-trading-env/bin/python -m pytest tests/ -v
	@echo "🔍 Running code quality checks..."
	quant-trading-env/bin/flake8 strategies/ models/ portfolio/ --max-line-length=88
	quant-trading-env/bin/black --check strategies/ models/ portfolio/
	quant-trading-env/bin/mypy strategies/ models/ portfolio/
	@echo "✅ All tests passed!"

# Model training
train:
	@echo "🤖 Training models..."
	quant-trading-env/bin/python models/train_all.py
	@echo "📊 Generating model reports..."
	quant-trading-env/bin/python models/evaluate_all.py
	@echo "✅ Model training complete!"

# Backtesting (Updated for Lean structure)
backtest:
	@echo "📈 Running backtests..."
	@cd lean_workspace && find . -name "*.py" -path "./*/main.py" | while read project; do \
		project_name=$$(dirname "$$project" | sed 's|./||'); \
		echo "Testing $$project_name"; \
		../quant-trading-env/bin/lean backtest "$$project_name"; \
	done
	@echo "📊 Generating backtest reports..."
	quant-trading-env/bin/python backtests/generate_reports.py
	@echo "✅ Backtesting complete!"

# Deployment (Updated for Lean structure)
deploy:
	@echo "🚀 Deploying to paper trading..."
	@cd lean_workspace && find . -name "*.py" -path "./*/main.py" | while read project; do \
		project_name=$$(dirname "$$project" | sed 's|./||'); \
		echo "Deploying $$project_name"; \
		../quant-trading-env/bin/lean cloud live start --project="$$project_name" --brokerage="Paper Trading"; \
	done
	@echo "✅ Deployment complete!"

# Reporting
report:
	@echo "📊 Generating performance reports..."
	quant-trading-env/bin/python reports/generate_daily_report.py
	quant-trading-env/bin/python reports/generate_monthly_report.py
	quant-trading-env/bin/python reports/generate_risk_report.py
	@echo "📧 Sending report notifications..."
	quant-trading-env/bin/python monitoring/send_notifications.py
	@echo "✅ Reports generated!"

# Monitoring
monitor:
	@echo "🔍 Launching monitoring dashboard..."
	quant-trading-env/bin/streamlit run dashboards/monitor.py --server.port 8501

# Cleanup
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.log" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	@echo "✅ Cleanup complete!"

# Create new strategy by copying existing one (Full Independence)
copy-strategy:
	@if [ -z "$(FROM)" ] || [ -z "$(TO)" ]; then \
		echo "❌ Error: Please specify FROM and TO strategy names"; \
		echo "Usage: make copy-strategy FROM=FirstMLTest TO=MyNewStrategy"; \
		echo ""; \
		echo "Available strategies to copy from:"; \
		@cd lean_workspace && find . -maxdepth 1 -type d -name "*" ! -name "." ! -name "data" | sed 's|./||' | sort; \
		exit 1; \
	fi
	@if [ ! -d "lean_workspace/$(FROM)" ]; then \
		echo "❌ Error: Source strategy '$(FROM)' not found"; \
		exit 1; \
	fi
	@if [ -d "lean_workspace/$(TO)" ]; then \
		echo "❌ Error: Target strategy '$(TO)' already exists"; \
		exit 1; \
	fi
	@echo "📝 Creating new strategy '$(TO)' based on '$(FROM)'..."
	@cp -r lean_workspace/$(FROM) lean_workspace/$(TO)
	@echo "✅ Strategy '$(TO)' created successfully!"
	@echo "📂 Location: lean_workspace/$(TO)/"
	@echo "📝 Next steps:"
	@echo "   1. Edit lean_workspace/$(TO)/main.py to customize your strategy"
	@echo "   2. Update any model paths or configurations"
	@echo "   3. Test with: make lean-backtest PROJECT=$(TO)"

# List available strategies to copy from
list-strategies:
	@echo "📋 Available strategies in lean_workspace/:"
	@cd lean_workspace && find . -maxdepth 1 -type d -name "*" ! -name "." ! -name "data" | sed 's|./||' | sort

# Development helpers
lint:
	@echo "🔍 Running linter..."
	quant-trading-env/bin/black strategies/ models/ portfolio/ lean_workspace/
	quant-trading-env/bin/flake8 strategies/ models/ portfolio/ lean_workspace/ --max-line-length=88

format:
	@echo "🎨 Formatting code..."
	quant-trading-env/bin/black strategies/ models/ portfolio/ lean_workspace/
	quant-trading-env/bin/isort strategies/ models/ portfolio/ lean_workspace/

# Data management
update-data:
	@echo "📥 Updating market data..."
	quant-trading-env/bin/python data/update_data.py
	@echo "✅ Data update complete!"

# Model management
retrain-models:
	@echo "🔄 Retraining all models..."
	quant-trading-env/bin/python models/retrain_all.py
	@echo "✅ Model retraining complete!"

# Risk management
risk-check:
	@echo "⚠️ Running risk checks..."
	quant-trading-env/bin/python risk_reports/run_risk_checks.py
	@echo "✅ Risk checks complete!"

# Backup
backup:
	@echo "💾 Creating backup..."
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	tar -czf "backup_$$timestamp.tar.gz" \
		strategies/ models/ data/ backtests/ reports/ lean_workspace/ \
		--exclude="*.pyc" --exclude="__pycache__" --exclude="*.log"
	@echo "✅ Backup created!"

# Install development dependencies
dev-install:
	@echo "🛠️ Installing development dependencies..."
	quant-trading-env/bin/pip install pytest black flake8 mypy isort pre-commit
	quant-trading-env/bin/pre-commit install
	@echo "✅ Development environment ready!"

# Lean-specific commands
lean-backtest:
	@if [ -z "$(PROJECT)" ]; then \
		echo "❌ Error: Please specify project name with PROJECT=project_name"; \
		exit 1; \
	fi
	@echo "📈 Running Lean backtest for $(PROJECT)..."
	@cd lean_workspace && ../quant-trading-env/bin/lean cloud backtest "$(PROJECT)"

lean-optimize:
	@if [ -z "$(PROJECT)" ]; then \
		echo "❌ Error: Please specify project name with PROJECT=project_name"; \
		exit 1; \
	fi
	@echo "⚙️ Running parameter optimization for $(PROJECT)..."
	@cd lean_workspace && ../quant-trading-env/bin/lean cloud optimize "$(PROJECT)"

lean-research:
	@if [ -z "$(PROJECT)" ]; then \
		echo "❌ Error: Please specify project name with PROJECT=project_name"; \
		exit 1; \
	fi
	@echo "🔬 Opening research notebook for $(PROJECT)..."
	@cd lean_workspace/$(PROJECT) && ../../quant-trading-env/bin/jupyter notebook research.ipynb

lean-cloud-pull:
	@echo "☁️ Syncing projects from QuantConnect cloud..."
	@cd lean_workspace && ../quant-trading-env/bin/lean cloud pull

lean-cloud-push:
	@if [ -z "$(PROJECT)" ]; then \
		echo "❌ Error: Please specify project name with PROJECT=project_name"; \
		exit 1; \
	fi
	@echo "☁️ Pushing $(PROJECT) to QuantConnect cloud..."
	@cd lean_workspace && ../quant-trading-env/bin/lean cloud push --project "$(PROJECT)" 