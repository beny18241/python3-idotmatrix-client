#!/bin/bash
# Fix Remote Service Issues
# This script helps fix common service issues on remote servers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Fixing Remote Service Issues${NC}"
echo "=================================="

# Get current user and paths
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)
VENV_PATH="$CURRENT_DIR/venv/bin/python"
SCRIPT_PATH="$CURRENT_DIR/calendar_scheduler_all.py"

echo -e "${BLUE}📊 Current Configuration:${NC}"
echo "  User: $CURRENT_USER"
echo "  Directory: $CURRENT_DIR"
echo "  Python: $VENV_PATH"
echo "  Script: $SCRIPT_PATH"
echo ""

# Check if files exist
if [[ ! -f "$VENV_PATH" ]]; then
    echo -e "${RED}❌ Virtual environment not found: $VENV_PATH${NC}"
    echo -e "${YELLOW}💡 Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt${NC}"
    exit 1
fi

if [[ ! -f "$SCRIPT_PATH" ]]; then
    echo -e "${RED}❌ Scheduler script not found: $SCRIPT_PATH${NC}"
    exit 1
fi

# Stop existing service
echo -e "${BLUE}⏹️  Stopping existing service...${NC}"
sudo systemctl stop idotmatrix-calendar-scheduler 2>/dev/null || true

# Create new service file with correct paths
echo -e "${BLUE}📝 Creating new service file...${NC}"
cat > /tmp/idotmatrix-calendar-scheduler.service << EOF
[Unit]
Description=iDotMatrix Calendar Scheduler
Documentation=https://github.com/beny18241/python3-idotmatrix-client
After=network.target
Wants=network.target

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$VENV_PATH $SCRIPT_PATH
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=idotmatrix-calendar

# Environment variables
Environment=PATH=$CURRENT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=$CURRENT_DIR

# Security settings (relaxed for compatibility)
NoNewPrivileges=false
PrivateTmp=false
ProtectSystem=false
ProtectHome=false

[Install]
WantedBy=multi-user.target
EOF

# Install new service file
echo -e "${BLUE}📋 Installing service file...${NC}"
sudo mv /tmp/idotmatrix-calendar-scheduler.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/idotmatrix-calendar-scheduler.service

# Reload systemd
echo -e "${BLUE}🔄 Reloading systemd...${NC}"
sudo systemctl daemon-reload

# Enable service
echo -e "${BLUE}🔧 Enabling service...${NC}"
sudo systemctl enable idotmatrix-calendar-scheduler

# Test the script first
echo -e "${BLUE}🧪 Testing scheduler script...${NC}"
if $VENV_PATH $SCRIPT_PATH test; then
    echo -e "${GREEN}✅ Script test passed${NC}"
else
    echo -e "${YELLOW}⚠️  Script test had issues, but continuing...${NC}"
fi

# Start service
echo -e "${BLUE}▶️  Starting service...${NC}"
sudo systemctl start idotmatrix-calendar-scheduler

# Wait a moment and check status
sleep 3
echo -e "${BLUE}📊 Checking service status...${NC}"
sudo systemctl status idotmatrix-calendar-scheduler --no-pager

echo ""
echo -e "${GREEN}🎉 Service fix completed!${NC}"
echo -e "${BLUE}📋 Management commands:${NC}"
echo "  Status:  sudo systemctl status idotmatrix-calendar-scheduler"
echo "  Logs:    sudo journalctl -u idotmatrix-calendar-scheduler -f"
echo "  Restart: sudo systemctl restart idotmatrix-calendar-scheduler"
echo "  Stop:    sudo systemctl stop idotmatrix-calendar-scheduler"
echo "  Start:   sudo systemctl start idotmatrix-calendar-scheduler"
