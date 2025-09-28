#!/bin/bash
# Debug Python environment and dependencies

echo "🔍 Debugging Python environment..."

# Check current directory
echo "📁 Current directory: $(pwd)"

# Check if virtual environment exists
if [ -f "venv/bin/activate" ]; then
    echo "✅ Virtual environment found"
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
    PYTHON_CMD="python"
    echo "✅ Using virtual environment Python: $(which python)"
else
    echo "❌ No virtual environment found"
    PYTHON_CMD="python3"
    echo "✅ Using system Python: $(which python3)"
fi

# Check Python version and path
echo "🐍 Python version:"
$PYTHON_CMD --version
echo "🐍 Python path: $(which $PYTHON_CMD)"

# Check pip version and path
echo "📦 Pip version:"
$PYTHON_CMD -m pip --version
echo "📦 Pip path: $($PYTHON_CMD -m pip show pip | grep Location || echo 'Not found')"

# Check if packages are installed
echo "🔍 Checking installed packages..."
$PYTHON_CMD -m pip list | grep -E "(google|oauth)" || echo "No Google packages found"

# Try to import packages
echo "🔍 Testing imports..."
$PYTHON_CMD -c "
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
echo "🔧 If packages are missing, run:"
echo "  $PYTHON_CMD -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
