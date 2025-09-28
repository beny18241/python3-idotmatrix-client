#!/bin/bash

echo "🔧 Setting up ICS Calendar Monitor for iDotMatrix"
echo "=================================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root: sudo $0"
    exit 1
fi

# Copy service file
echo "📋 Installing systemd service..."
cp ics-calendar-monitor.service /etc/systemd/system/

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable service
echo "✅ Enabling ICS calendar monitor..."
systemctl enable ics-calendar-monitor.service

# Start service
echo "🚀 Starting ICS calendar monitor..."
systemctl start ics-calendar-monitor.service

# Check status
echo "📊 Service status:"
systemctl status ics-calendar-monitor.service --no-pager

echo ""
echo "🎉 ICS Calendar Monitor setup complete!"
echo ""
echo "📋 Commands:"
echo "  sudo systemctl status ics-calendar-monitor    # Check status"
echo "  sudo systemctl stop ics-calendar-monitor      # Stop service"
echo "  sudo systemctl start ics-calendar-monitor     # Start service"
echo "  sudo systemctl restart ics-calendar-monitor   # Restart service"
echo "  sudo journalctl -u ics-calendar-monitor -f    # View logs"
echo ""
echo "🔄 The service will:"
echo "  • Refresh ICS calendar every 30 minutes"
echo "  • Display tomorrow's events on iDotMatrix device"
echo "  • Automatically restart if it fails"
echo "  • Start automatically on boot"
