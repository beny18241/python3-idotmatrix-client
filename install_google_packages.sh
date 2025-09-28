#!/bin/bash
# Install Google packages for server environment

set -e

echo "🔧 Installing Google Calendar packages for server..."

# Check Python version
echo "🐍 Python version:"
python3 --version

# Check pip version
echo "📦 Pip version:"
python3 -m pip --version

# Upgrade pip first
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install Google packages one by one
echo "📦 Installing google-api-python-client..."
python3 -m pip install google-api-python-client

echo "📦 Installing google-auth..."
python3 -m pip install google-auth

echo "📦 Installing google-auth-httplib2..."
python3 -m pip install google-auth-httplib2

echo "📦 Installing google-auth-oauthlib..."
python3 -m pip install google-auth-oauthlib

# Verify installation
echo "🔍 Verifying installation..."
python3 test_google_imports.py

echo ""
echo "✅ Installation complete!"
echo ""
echo "Now you can run:"
echo "  python3 calendar_auth_simple.py"
