#!/bin/bash

echo "🔧 Running OAuth Calendar Solution"
echo "==================================="

# Activate virtual environment
source venv/bin/activate

# Run OAuth calendar solution
python3 oauth_calendar_final.py "$@"
