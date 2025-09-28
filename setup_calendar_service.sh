#!/bin/bash
# Setup iDotMatrix Calendar Scheduler as a System Service
# Supports both systemd (Linux) and launchd (macOS)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="idotmatrix-calendar-scheduler"
PLIST_NAME="com.idotmatrix.calendar"

echo -e "${BLUE}🔧 Setting up iDotMatrix Calendar Scheduler as a System Service${NC}"
echo "=================================================================="

# Detect operating system
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo -e "${GREEN}✅ Detected macOS - Using launchd${NC}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo -e "${GREEN}✅ Detected Linux - Using systemd${NC}"
else
    echo -e "${RED}❌ Unsupported operating system: $OSTYPE${NC}"
    exit 1
fi

# Check if running as root (not recommended for user services)
if [[ $EUID -eq 0 ]]; then
    echo -e "${YELLOW}⚠️  Warning: Running as root. Consider running as regular user.${NC}"
fi

# Create logs directory
echo -e "${BLUE}📁 Creating logs directory...${NC}"
mkdir -p "$SCRIPT_DIR/logs"
chmod 755 "$SCRIPT_DIR/logs"

# Make sure the scheduler script is executable
chmod +x "$SCRIPT_DIR/calendar_scheduler_all.py"

if [[ "$OS" == "macos" ]]; then
    echo -e "${BLUE}🍎 Setting up macOS launchd service...${NC}"
    
    # Copy plist to LaunchAgents directory
    PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
    echo -e "${BLUE}📋 Installing service plist to: $PLIST_PATH${NC}"
    
    # Create LaunchAgents directory if it doesn't exist
    mkdir -p "$HOME/Library/LaunchAgents"
    
    # Copy and update the plist with current user
    sed "s|maciejpindela|$USER|g" "$SCRIPT_DIR/$PLIST_NAME.plist" > "$PLIST_PATH"
    
    # Set proper permissions
    chmod 644 "$PLIST_PATH"
    
    # Load the service
    echo -e "${BLUE}🚀 Loading service...${NC}"
    launchctl load "$PLIST_PATH"
    
    # Start the service
    echo -e "${BLUE}▶️  Starting service...${NC}"
    launchctl start "$PLIST_NAME"
    
    echo -e "${GREEN}✅ macOS service installed and started!${NC}"
    echo -e "${BLUE}📋 Service management commands:${NC}"
    echo "  Start:   launchctl start $PLIST_NAME"
    echo "  Stop:    launchctl stop $PLIST_NAME"
    echo "  Restart: launchctl stop $PLIST_NAME && launchctl start $PLIST_NAME"
    echo "  Status:  launchctl list | grep $PLIST_NAME"
    echo "  Logs:    tail -f $SCRIPT_DIR/logs/service.log"
    echo "  Uninstall: launchctl unload $PLIST_PATH && rm $PLIST_PATH"
    
elif [[ "$OS" == "linux" ]]; then
    echo -e "${BLUE}🐧 Setting up Linux systemd service...${NC}"
    
    # Copy service file to systemd directory
    SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME.service"
    echo -e "${BLUE}📋 Installing service file to: $SERVICE_PATH${NC}"
    
    # Update the service file with current user
    sed "s|maciejpindela|$USER|g" "$SCRIPT_DIR/$SERVICE_NAME.service" > "/tmp/$SERVICE_NAME.service"
    
    # Move to systemd directory (requires sudo)
    echo -e "${YELLOW}🔐 This requires sudo privileges...${NC}"
    sudo mv "/tmp/$SERVICE_NAME.service" "$SERVICE_PATH"
    sudo chmod 644 "$SERVICE_PATH"
    
    # Reload systemd
    echo -e "${BLUE}🔄 Reloading systemd...${NC}"
    sudo systemctl daemon-reload
    
    # Enable the service
    echo -e "${BLUE}🔧 Enabling service...${NC}"
    sudo systemctl enable "$SERVICE_NAME"
    
    # Start the service
    echo -e "${BLUE}▶️  Starting service...${NC}"
    sudo systemctl start "$SERVICE_NAME"
    
    echo -e "${GREEN}✅ Linux service installed and started!${NC}"
    echo -e "${BLUE}📋 Service management commands:${NC}"
    echo "  Start:   sudo systemctl start $SERVICE_NAME"
    echo "  Stop:    sudo systemctl stop $SERVICE_NAME"
    echo "  Restart: sudo systemctl restart $SERVICE_NAME"
    echo "  Status:  sudo systemctl status $SERVICE_NAME"
    echo "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
    echo "  Uninstall: sudo systemctl stop $SERVICE_NAME && sudo systemctl disable $SERVICE_NAME && sudo rm $SERVICE_PATH"
fi

echo ""
echo -e "${GREEN}🎉 iDotMatrix Calendar Scheduler is now running as a system service!${NC}"
echo -e "${BLUE}📊 The scheduler will:${NC}"
echo "  • Check all calendars every 30 minutes"
echo "  • Update your iDotMatrix device automatically"
echo "  • Log all activities to logs/calendar_scheduler.log"
echo "  • Restart automatically if it crashes"
echo "  • Start automatically on system boot"
echo ""
echo -e "${YELLOW}💡 To test the service, run:${NC}"
echo "  python3 calendar_scheduler_all.py test"
echo ""
echo -e "${BLUE}📝 Log files:${NC}"
echo "  • Main logs: logs/calendar_scheduler.log"
if [[ "$OS" == "macos" ]]; then
    echo "  • Service logs: logs/service.log"
    echo "  • Service errors: logs/service.error.log"
fi
