#!/bin/bash

echo "🔧 Running OAuth SSH Tunnel Setup"
echo "=================================="

# Activate virtual environment
source venv/bin/activate

# Run OAuth SSH tunnel setup
python3 oauth_ssh_tunnel.py
