#!/bin/bash
# Complete deployment script for iDotMatrix on remote server

set -e

# Configuration
APP_NAME="idotmatrix"
APP_DIR="/opt/$APP_NAME"
SERVICE_USER="idotmatrix"
SERVICE_FILE="/etc/systemd/system/$APP_NAME.service"

echo "🚀 Starting complete deployment of iDotMatrix..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Please do not run this script as root. It will use sudo when needed."
   exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    bluetooth \
    bluez \
    libbluetooth-dev \
    git \
    curl \
    wget

# Create application user
echo "👤 Creating application user..."
sudo useradd -r -s /bin/false -d $APP_DIR $SERVICE_USER || echo "User $SERVICE_USER already exists"

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
echo "📋 Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
chmod +x run_in_venv.sh create_venv.sh

# Set proper ownership
sudo chown -R $SERVICE_USER:$SERVICE_USER $APP_DIR

# Install systemd service
echo "⚙️ Installing systemd service..."
sudo cp idotmatrix.service $SERVICE_FILE
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME

# Configure Bluetooth permissions
echo "📡 Configuring Bluetooth permissions..."
sudo usermod -a -G bluetooth $SERVICE_USER

# Create data and logs directories
sudo mkdir -p $APP_DIR/data $APP_DIR/logs
sudo chown -R $SERVICE_USER:$SERVICE_USER $APP_DIR/data $APP_DIR/logs

echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Start the service: sudo systemctl start $APP_NAME"
echo "2. Check status: sudo systemctl status $APP_NAME"
echo "3. View logs: sudo journalctl -u $APP_NAME -f"
echo "4. Scan for devices: sudo -u $SERVICE_USER $APP_DIR/venv/bin/python $APP_DIR/app.py --scan"
echo ""
echo "🔧 Service management commands:"
echo "  Start:   sudo systemctl start $APP_NAME"
echo "  Stop:    sudo systemctl stop $APP_NAME"
echo "  Restart: sudo systemctl restart $APP_NAME"
echo "  Status:  sudo systemctl status $APP_NAME"
