#!/bin/bash
# Setup Google Calendar integration for headless server

set -e

echo "🔧 Setting up Google Calendar integration for server..."

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo "❌ credentials.json not found!"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create a project and enable Google Calendar API"
    echo "3. Create OAuth credentials (Desktop application)"
    echo "4. Download the JSON file and save as 'credentials.json'"
    echo "5. Upload credentials.json to your server"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✅ Found credentials.json"

# Check if we're in a virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
    PYTHON_CMD="python"
else
    echo "🐍 Using system Python..."
    PYTHON_CMD="python3"
fi

# Install Google API dependencies
echo "📦 Installing Google Calendar API dependencies..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Test the headless authentication
echo "🔐 Testing Google Calendar authentication..."
echo "This will open a URL for you to authorize the application."
echo ""

$PYTHON_CMD calendar_integration_headless.py

echo ""
echo "✅ Calendar setup complete!"
echo ""
echo "Now you can use calendar commands:"
echo "  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-current"
echo "  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-next"
echo "  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-today"
