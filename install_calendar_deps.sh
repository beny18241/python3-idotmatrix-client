#!/bin/bash
# Comprehensive Google Calendar dependencies installation

set -e

echo "🔧 Installing Google Calendar dependencies..."

# Check if we're in a virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
    PYTHON_CMD="python"
    echo "✅ Using virtual environment Python"
else
    echo "🐍 Using system Python..."
    PYTHON_CMD="python3"
    echo "✅ Using system Python"
fi

# Check Python version
echo "🐍 Python version:"
$PYTHON_CMD --version

# Upgrade pip first
echo "📦 Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip

# Install Google API dependencies
echo "📦 Installing Google Calendar API dependencies..."
$PYTHON_CMD -m pip install google-api-python-client
$PYTHON_CMD -m pip install google-auth-httplib2
$PYTHON_CMD -m pip install google-auth-oauthlib

# Verify installation
echo "🔍 Verifying installation..."
$PYTHON_CMD -c "import google.auth.transport.requests; print('✅ google.auth.transport.requests')"
$PYTHON_CMD -c "import google.oauth2.credentials; print('✅ google.oauth2.credentials')"
$PYTHON_CMD -c "import google_auth_oauthlib.flow; print('✅ google_auth_oauthlib.flow')"
$PYTHON_CMD -c "import googleapiclient.discovery; print('✅ googleapiclient.discovery')"

echo ""
echo "✅ All Google Calendar dependencies installed successfully!"
echo ""
echo "Now you can run:"
echo "  python3 calendar_auth_simple.py"
