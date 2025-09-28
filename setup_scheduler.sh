#!/bin/bash

echo "🕐 Setting up Calendar Scheduler"
echo "================================"

# Install schedule library
echo "📦 Installing schedule library..."
source venv/bin/activate
pip install schedule

# Make scheduler executable
chmod +x calendar_scheduler.py

# Test the scheduler
echo "🧪 Testing scheduler..."
python3 calendar_scheduler.py test

echo ""
echo "✅ Scheduler setup complete!"
echo ""
echo "🚀 Usage:"
echo "   python3 calendar_scheduler.py        # Run scheduler"
echo "   python3 calendar_scheduler.py test   # Test once"
echo ""
echo "🔧 For systemd service (on server):"
echo "   sudo cp calendar-scheduler.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable calendar-scheduler"
echo "   sudo systemctl start calendar-scheduler"
echo "   sudo systemctl status calendar-scheduler"
