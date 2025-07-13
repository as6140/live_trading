# 🚀 First-Time Setup Guide

Complete setup guide for the QuantConnect + IBKR live trading system from scratch.

## Prerequisites

- **Python 3.11+** installed
- **Git** installed
- **Text editor** (VS Code, nano, vim, etc.)

## Step 1: Account Setup

### A. Interactive Brokers Account
1. **Create Account**: Go to [InteractiveBrokers.com](https://www.interactivebrokers.com)
2. **Apply for Account**: Choose "Individual" account type
3. **Fund Account**: Minimum $10,000 for live trading (or just enable paper trading)
4. **Enable Paper Trading**:
   - Log into [Client Portal](https://gdcdyn.interactivebrokers.com)
   - Account Settings → Trading Permissions → Paper Trading Account
   - **Write down your paper account number** (format: DUM123456)

### B. QuantConnect Account  
1. **Sign Up**: Go to [QuantConnect.com](https://www.quantconnect.com)
2. **Verify Email**: Check your inbox and verify account
3. **Get API Access**: Account → My Account → API tab
4. **Choose Plan**: 
   - Free tier: Good for learning and basic strategies
   - Paid tier: More computational resources and data

## Step 2: Environment Setup

### A. Clone Repository
```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd live_trading

# Verify structure
ls -la
```

### B. Python Environment
```bash
# Create isolated Python environment
python3.11 -m venv quant-trading-env --upgrade-deps

# Activate environment
source quant-trading-env/bin/activate  # macOS/Linux
# OR
quant-trading-env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install QuantConnect CLI
pip install lean
```

## Step 3: Credential Configuration

### A. Run Setup Script
```bash
# This copies credential templates and sets up structure
python setup_credentials.py
```

### B. Configure Your Credentials
```bash
# Edit the .env file with your actual details
nano .env  # or use your preferred editor
```

**Fill in your .env file:**
```bash
# Your IBKR Paper Trading Details
IBKR_ACCOUNT=DUM123456           # Your paper account number from Step 1A
IBKR_USERNAME=your_ib_username   # Your IBKR login username  
IBKR_PASSWORD=your_ib_password   # Your IBKR login password

# QuantConnect API (optional - can login via CLI instead)
# QC_USER_ID=your_user_id
# QC_API_TOKEN=your_api_token
```

### C. Apply Credentials
```bash
# Run setup again to apply your credentials to lean.json
python setup_credentials.py

# Verify credentials were applied
grep "ib-account" lean_workspace/lean.json
# Should show your account number, not ${IBKR_ACCOUNT}
```

## Step 4: QuantConnect Integration

### A. Login to QuantConnect
```bash
# Connect your local environment to QuantConnect
lean login
# Enter your QuantConnect email and password when prompted
```

### B. Test Connection
```bash
# List your QuantConnect projects (should see FirstMLTest)
lean cloud status

# Test data download (optional)
lean data download --dataset "US Equity Security Master"
```

## Step 5: Deploy First Strategy

### A. Push to Cloud
```bash
# Upload FirstMLTest strategy to QuantConnect cloud
lean cloud push --project "FirstMLTest"
```

### B. Deploy Live Trading
1. **Go to QuantConnect Dashboard**: https://www.quantconnect.com
2. **Find FirstMLTest Project**: Click on it
3. **Click "Deploy Live"**
4. **Configure Deployment**:
   - **Brokerage**: Select "Interactive Brokers"
   - **Account**: Enter your paper account number
   - **Username**: Your IBKR username
   - **Password**: Your IBKR password
   - **Environment**: Paper Trading
5. **Click "Deploy"**

## Step 6: Verify Everything Works

### A. Check QuantConnect Dashboard
- Strategy should show "Live" status
- Monitor for any error messages
- Check logs for successful IBKR connection

### B. Check IBKR Account
- Log into [IBKR Client Portal](https://gdcdyn.interactivebrokers.com)
- Switch to Paper Trading view
- Verify strategy positions appear

### C. Local Testing (Optional)
```bash
# Test local deployment (Intel Macs/Linux only)
lean live "FirstMLTest" --environment "live-interactive"
# ARM Macs: Use cloud deployment instead
```

## Troubleshooting

### Common Issues

**"Docker not found" Error**:
- For cloud deployment: Not needed, ignore this
- For local deployment: Install Docker or use colima alternative

**"ARM architecture not supported"**:
- Use cloud deployment instead of local
- This is expected on M1/M2/M3 Macs for IBKR

**Authentication Errors**:
- Double-check your .env file credentials
- Verify IBKR paper trading is enabled
- Try re-running `python setup_credentials.py`

**QuantConnect Login Issues**:
- Verify email/password at quantconnect.com
- Check internet connection
- Try `lean logout` then `lean login` again

### Getting Help

1. **Check Logs**: Look in `logs/` directory for detailed error messages
2. **QuantConnect Community**: [https://www.quantconnect.com/forum](https://www.quantconnect.com/forum)
3. **IBKR Support**: For account/permission issues
4. **GitHub Issues**: For repository-specific problems

## Next Steps

Once everything is working:

1. **Monitor Performance**: Check QuantConnect dashboard daily
2. **Explore Strategies**: Look at other algorithms in lean_workspace/
3. **Learn QuantConnect**: Work through their tutorials
4. **Develop New Strategies**: See `system_prompt_checklist.md` for development workflow

## Security Reminders

- ✅ `.env` file is gitignored (safe)
- ✅ `lean.json` uses environment variables (safe)
- ✅ Only templates are committed to Git
- ⚠️ Never commit actual credentials to version control
- 🔒 Use paper trading until you're confident in your strategies 