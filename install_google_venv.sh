#!/bin/bash
# Install Google packages in virtual environment

set -e

echo "🔧 Installing Google Calendar packages in virtual environment..."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Check Python version in venv
echo "🐍 Python version in venv:"
python --version

# Check pip version in venv
echo "📦 Pip version in venv:"
python -m pip --version

# Upgrade pip in venv
echo "📦 Upgrading pip in virtual environment..."
python -m pip install --upgrade pip

# Install Google packages in venv
echo "📦 Installing Google packages in virtual environment..."

echo "📦 Installing google-api-python-client..."
python -m pip install google-api-python-client

echo "📦 Installing google-auth..."
python -m pip install google-auth

echo "📦 Installing google-auth-httplib2..."
python -m pip install google-auth-httplib2

echo "📦 Installing google-auth-oauthlib..."
python -m pip install google-auth-oauthlib

# Verify installation
echo "🔍 Verifying installation in virtual environment..."
python test_google_imports.py

echo ""
echo "✅ Installation complete in virtual environment!"
echo ""
echo "Now you can run:"
echo "  source venv/bin/activate"
echo "  python calendar_auth_simple.py"
echo ""
echo "Or use the run script:"
echo "  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-current"
