#!/bin/bash
# Force install Google Calendar dependencies

set -e

echo "🔧 Force installing Google Calendar dependencies..."

# Check if virtual environment exists
if [ -f "venv/bin/activate" ]; then
    echo "🐍 Virtual environment found - activating..."
    source venv/bin/activate
    PYTHON_CMD="python"
    echo "✅ Using virtual environment Python: $(which python)"
else
    echo "🐍 No virtual environment - using system Python"
    PYTHON_CMD="python3"
    echo "✅ Using system Python: $(which python3)"
fi

# Force upgrade pip
echo "📦 Force upgrading pip..."
$PYTHON_CMD -m pip install --upgrade --force-reinstall pip

# Uninstall and reinstall Google packages
echo "🗑️ Removing existing Google packages..."
$PYTHON_CMD -m pip uninstall -y google-api-python-client google-auth-httplib2 google-auth-oauthlib google-auth google-auth-oauthlib || true

# Install Google packages with force
echo "📦 Installing Google Calendar API dependencies..."
$PYTHON_CMD -m pip install --force-reinstall --no-cache-dir google-api-python-client
$PYTHON_CMD -m pip install --force-reinstall --no-cache-dir google-auth-httplib2
$PYTHON_CMD -m pip install --force-reinstall --no-cache-dir google-auth-oauthlib

# Also install base google-auth
$PYTHON_CMD -m pip install --force-reinstall --no-cache-dir google-auth

# Verify installation
echo "🔍 Verifying installation..."
$PYTHON_CMD -c "
import sys
print('Python path:', sys.path)
print()

try:
    import google.auth.transport.requests
    print('✅ google.auth.transport.requests')
except ImportError as e:
    print('❌ google.auth.transport.requests:', e)

try:
    import google.oauth2.credentials
    print('✅ google.oauth2.credentials')
except ImportError as e:
    print('❌ google.oauth2.credentials:', e)

try:
    import google_auth_oauthlib.flow
    print('✅ google_auth_oauthlib.flow')
except ImportError as e:
    print('❌ google_auth_oauthlib.flow:', e)

try:
    import googleapiclient.discovery
    print('✅ googleapiclient.discovery')
except ImportError as e:
    print('❌ googleapiclient.discovery:', e)
"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Now try:"
echo "  python3 calendar_auth_simple.py"
