#!/bin/bash
# Quick fix for Google Calendar dependencies on server

set -e

echo "🔧 Fixing Google Calendar dependencies..."

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

echo "✅ Dependencies installed!"
echo ""
echo "Now run the setup again:"
echo "  ./setup_calendar_server.sh"
