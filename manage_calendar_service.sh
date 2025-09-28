#!/bin/bash
"""
Manage iDotMatrix Calendar Scheduler Service
Provides easy commands to start, stop, restart, and check status
"""

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Service configuration
SERVICE_NAME="idotmatrix-calendar-scheduler"
PLIST_NAME="com.idotmatrix.calendar"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect operating system
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    echo -e "${RED}❌ Unsupported operating system: $OSTYPE${NC}"
    exit 1
fi

# Function to show usage
show_usage() {
    echo -e "${BLUE}🔧 iDotMatrix Calendar Service Manager${NC}"
    echo "=================================="
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start     - Start the calendar service"
    echo "  stop      - Stop the calendar service"
    echo "  restart   - Restart the calendar service"
    echo "  status    - Check service status"
    echo "  logs      - Show service logs (follow mode)"
    echo "  logs-tail - Show last 50 log lines"
    echo "  test      - Test calendar status (one-time)"
    echo "  uninstall - Remove the service"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 status"
    echo "  $0 logs"
    echo "  $0 test"
}

# Function to start service
start_service() {
    echo -e "${BLUE}▶️  Starting iDotMatrix Calendar Service...${NC}"
    
    if [[ "$OS" == "macos" ]]; then
        launchctl start "$PLIST_NAME"
        echo -e "${GREEN}✅ Service started${NC}"
    elif [[ "$OS" == "linux" ]]; then
        sudo systemctl start "$SERVICE_NAME"
        echo -e "${GREEN}✅ Service started${NC}"
    fi
}

# Function to stop service
stop_service() {
    echo -e "${BLUE}⏹️  Stopping iDotMatrix Calendar Service...${NC}"
    
    if [[ "$OS" == "macos" ]]; then
        launchctl stop "$PLIST_NAME"
        echo -e "${GREEN}✅ Service stopped${NC}"
    elif [[ "$OS" == "linux" ]]; then
        sudo systemctl stop "$SERVICE_NAME"
        echo -e "${GREEN}✅ Service stopped${NC}"
    fi
}

# Function to restart service
restart_service() {
    echo -e "${BLUE}🔄 Restarting iDotMatrix Calendar Service...${NC}"
    stop_service
    sleep 2
    start_service
}

# Function to check status
check_status() {
    echo -e "${BLUE}📊 Checking service status...${NC}"
    
    if [[ "$OS" == "macos" ]]; then
        if launchctl list | grep -q "$PLIST_NAME"; then
            echo -e "${GREEN}✅ Service is running${NC}"
            launchctl list | grep "$PLIST_NAME"
        else
            echo -e "${RED}❌ Service is not running${NC}"
        fi
    elif [[ "$OS" == "linux" ]]; then
        sudo systemctl status "$SERVICE_NAME" --no-pager
    fi
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}📝 Showing service logs (press Ctrl+C to exit)...${NC}"
    
    if [[ "$OS" == "macos" ]]; then
        if [[ -f "$SCRIPT_DIR/logs/service.log" ]]; then
            tail -f "$SCRIPT_DIR/logs/service.log"
        else
            echo -e "${YELLOW}⚠️  Service log file not found: $SCRIPT_DIR/logs/service.log${NC}"
        fi
    elif [[ "$OS" == "linux" ]]; then
        sudo journalctl -u "$SERVICE_NAME" -f
    fi
}

# Function to show recent logs
show_logs_tail() {
    echo -e "${BLUE}📝 Showing last 50 log lines...${NC}"
    
    if [[ "$OS" == "macos" ]]; then
        if [[ -f "$SCRIPT_DIR/logs/service.log" ]]; then
            tail -n 50 "$SCRIPT_DIR/logs/service.log"
        else
            echo -e "${YELLOW}⚠️  Service log file not found: $SCRIPT_DIR/logs/service.log${NC}"
        fi
    elif [[ "$OS" == "linux" ]]; then
        sudo journalctl -u "$SERVICE_NAME" -n 50 --no-pager
    fi
}

# Function to test calendar
test_calendar() {
    echo -e "${BLUE}🧪 Testing calendar status...${NC}"
    cd "$SCRIPT_DIR"
    source venv/bin/activate
    python3 calendar_scheduler_all.py test
}

# Function to uninstall service
uninstall_service() {
    echo -e "${YELLOW}⚠️  This will remove the iDotMatrix Calendar Service${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}🗑️  Uninstalling service...${NC}"
        
        if [[ "$OS" == "macos" ]]; then
            PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
            launchctl unload "$PLIST_PATH" 2>/dev/null || true
            rm -f "$PLIST_PATH"
            echo -e "${GREEN}✅ Service uninstalled${NC}"
        elif [[ "$OS" == "linux" ]]; then
            sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
            sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
            sudo rm -f "/etc/systemd/system/$SERVICE_NAME.service"
            sudo systemctl daemon-reload
            echo -e "${GREEN}✅ Service uninstalled${NC}"
        fi
    else
        echo -e "${BLUE}ℹ️  Uninstall cancelled${NC}"
    fi
}

# Main script logic
case "${1:-help}" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
        ;;
    logs-tail)
        show_logs_tail
        ;;
    test)
        test_calendar
        ;;
    uninstall)
        uninstall_service
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        show_usage
        exit 1
        ;;
esac
