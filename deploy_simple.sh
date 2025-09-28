#!/bin/bash
# Simple deployment script for iDotMatrix on remote server

set -e

echo "🚀 Deploying iDotMatrix to remote server..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip if not present
echo "🐍 Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install system dependencies for Bluetooth
echo "📡 Installing Bluetooth dependencies..."
sudo apt install -y bluetooth bluez libbluetooth-dev

# Create application directory
APP_DIR="/opt/idotmatrix"
echo "📁 Creating application directory at $APP_DIR..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
echo "📋 Copying application files..."
cp -r . $APP_DIR/

# Create virtual environment
echo "🔧 Setting up virtual environment..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
chmod +x run_in_venv.sh
chmod +x create_venv.sh

echo "✅ Deployment complete!"
echo ""
echo "To run the application:"
echo "  cd $APP_DIR"
echo "  ./run_in_venv.sh --scan"
echo ""
echo "For GUI:"
echo "  cd $APP_DIR"
echo "  source venv/bin/activate"
echo "  python gui.py"
