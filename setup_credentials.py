#!/usr/bin/env python3
"""
Credential Setup Script for QuantConnect Live Trading

This script helps set up your credentials safely:
1. Copies lean.json.example to lean.json
2. Replaces environment variable placeholders with actual values
3. Creates .env file from .env.example if it doesn't exist

Usage:
    python setup_credentials.py
"""

import json
import os
import shutil
from pathlib import Path

def setup_credentials():
    """Set up credentials for QuantConnect trading."""
    
    # Paths
    lean_example = Path("lean_workspace/lean.json.example")
    lean_config = Path("lean_workspace/lean.json")
    env_example = Path("credentials.template")
    env_file = Path(".env")
    
    print("🔐 QuantConnect Credential Setup")
    print("=" * 40)
    
    # Step 1: Copy lean.json.example to lean.json
    if not lean_config.exists():
        print(f"📋 Copying {lean_example} to {lean_config}")
        shutil.copy2(lean_example, lean_config)
    else:
        print(f"✅ {lean_config} already exists")
    
    # Step 2: Copy .env.example to .env if it doesn't exist
    if not env_file.exists() and env_example.exists():
        print(f"📋 Copying {env_example} to {env_file}")
        shutil.copy2(env_example, env_file)
        print("⚠️  Please edit .env file with your actual credentials")
    else:
        print(f"✅ {env_file} already exists or no template available")
    
    # Step 3: Load environment variables and update lean.json
    if env_file.exists():
        print("🔄 Loading environment variables from .env")
        
        # Load .env file
        env_vars = {}
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        
        # Read lean.json
        with open(lean_config, 'r') as f:
            config = json.load(f)
        
        # Replace placeholders
        replacements = {
            "${IBKR_ACCOUNT}": env_vars.get('IBKR_ACCOUNT', ''),
            "${IBKR_USERNAME}": env_vars.get('IBKR_USERNAME', ''),
            "${IBKR_PASSWORD}": env_vars.get('IBKR_PASSWORD', ''),
        }
        
        # Update config
        for old, new in replacements.items():
            if new:  # Only replace if we have a value
                config_str = json.dumps(config)
                config_str = config_str.replace(old, new)
                config = json.loads(config_str)
        
        # Write updated config
        with open(lean_config, 'w') as f:
            json.dump(config, f, indent=4)
        
        print("✅ Updated lean.json with environment variables")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your actual credentials")
    print("2. Run: python setup_credentials.py (to apply the changes)")
    print("3. Test with: lean live \"FirstMLTest\" --environment \"live-interactive\"")
    
    print("\n⚠️  Security reminder:")
    print("- .env file is gitignored (safe)")
    print("- lean.json is gitignored (safe)")
    print("- Only lean.json.example and credentials.template are committed")

if __name__ == "__main__":
    setup_credentials() 