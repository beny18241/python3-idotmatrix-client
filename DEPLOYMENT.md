# iDotMatrix Remote Server Deployment Guide

This guide provides multiple deployment options for installing iDotMatrix on a remote server.

## Prerequisites

- Ubuntu/Debian server (or similar Linux distribution)
- SSH access to the server
- Bluetooth hardware (if using physical devices)
- Python 3.7+ (for non-Docker deployments)

## Deployment Options

### Option 1: Simple Python Installation (Quick Setup)

**Best for:** Development, testing, or simple setups

```bash
# Upload your project to the server
scp -r . user@your-server:/tmp/idotmatrix

# SSH into your server
ssh user@your-server

# Run the simple deployment script
cd /tmp/idotmatrix
chmod +x deploy_simple.sh
./deploy_simple.sh
```

**Usage:**
```bash
cd /opt/idotmatrix
./run_in_venv.sh --scan
```

### Option 2: Docker Deployment (Recommended for Production)

**Best for:** Production environments, easy management, isolation

```bash
# Upload your project to the server
scp -r . user@your-server:/tmp/idotmatrix

# SSH into your server
ssh user@your-server

# Run the Docker deployment script
cd /tmp/idotmatrix
chmod +x deploy_docker.sh
./deploy_docker.sh
```

**Usage:**
```bash
# View logs
docker-compose logs -f

# Scan for devices
docker-compose exec idotmatrix python app.py --scan

# Stop services
docker-compose down
```

### Option 3: Complete Systemd Service (Production Service)

**Best for:** Production servers, automatic startup, service management

```bash
# Upload your project to the server
scp -r . user@your-server:/tmp/idotmatrix

# SSH into your server
ssh user@your-server

# Run the complete deployment script
cd /tmp/idotmatrix
chmod +x deploy_complete.sh
./deploy_complete.sh
```

**Service Management:**
```bash
# Start the service
sudo systemctl start idotmatrix

# Check status
sudo systemctl status idotmatrix

# View logs
sudo journalctl -u idotmatrix -f

# Stop the service
sudo systemctl stop idotmatrix
```

## Manual Installation Steps

If you prefer to install manually:

### 1. System Dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv bluetooth bluez libbluetooth-dev
```

### 2. Application Setup
```bash
# Create directory
sudo mkdir -p /opt/idotmatrix
sudo chown $USER:$USER /opt/idotmatrix

# Copy files
cp -r . /opt/idotmatrix/
cd /opt/idotmatrix

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Create Systemd Service (Optional)
```bash
# Copy service file
sudo cp idotmatrix.service /etc/systemd/system/

# Create service user
sudo useradd -r -s /bin/false -d /opt/idotmatrix idotmatrix
sudo chown -R idotmatrix:idotmatrix /opt/idotmatrix

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable idotmatrix
sudo systemctl start idotmatrix
```

## Bluetooth Configuration

### For Physical Bluetooth Devices

1. **Enable Bluetooth:**
```bash
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
```

2. **Configure permissions:**
```bash
sudo usermod -a -G bluetooth $USER
# or for service user:
sudo usermod -a -G bluetooth idotmatrix
```

3. **Test Bluetooth:**
```bash
# Scan for devices
bluetoothctl scan on
```

### For Docker with Bluetooth

Docker containers need special configuration for Bluetooth access:

```bash
# Run with privileged mode and host networking
docker run --privileged --network=host -it idotmatrix python app.py --scan
```

## Usage Examples

### Command Line Interface

```bash
# Scan for devices
python app.py --scan

# Connect to specific device
python app.py --address 00:11:22:33:44:ff --screen on

# Set text
python app.py --address 00:11:22:33:44:ff --set-text "Hello World"

# Display image
python app.py --address 00:11:22:33:44:ff --image true --set-image ./images/demo_32.png
```

### GUI Interface

```bash
# Run GUI (requires display)
python gui.py
```

## Troubleshooting

### Common Issues

1. **Bluetooth Permission Denied:**
```bash
sudo usermod -a -G bluetooth $USER
# Log out and back in
```

2. **Device Not Found:**
```bash
# Check Bluetooth is running
sudo systemctl status bluetooth

# Reset Bluetooth
sudo systemctl restart bluetooth
```

3. **Python Dependencies:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

4. **Docker Bluetooth Issues:**
```bash
# Run with proper permissions
docker run --privileged --network=host --cap-add=NET_ADMIN idotmatrix
```

### Logs and Debugging

**Systemd Service Logs:**
```bash
sudo journalctl -u idotmatrix -f
```

**Docker Logs:**
```bash
docker-compose logs -f idotmatrix
```

**Manual Debug:**
```bash
# Run with verbose logging
python app.py --scan --verbose
```

## Security Considerations

1. **Service User:** The systemd service runs as a non-root user (`idotmatrix`)
2. **Bluetooth Permissions:** Only necessary users are added to the bluetooth group
3. **Docker Isolation:** Docker containers provide process isolation
4. **Network Security:** Consider firewall rules if exposing web interfaces

## Performance Optimization

1. **Resource Limits:** Set appropriate CPU/memory limits for Docker containers
2. **Log Rotation:** Configure log rotation to prevent disk space issues
3. **Monitoring:** Set up monitoring for service health and resource usage

## Backup and Recovery

1. **Configuration Backup:**
```bash
# Backup configuration
tar -czf idotmatrix-backup.tar.gz /opt/idotmatrix/data /opt/idotmatrix/logs
```

2. **Service Recovery:**
```bash
# Restore and restart
sudo systemctl restart idotmatrix
```

## Support

For issues specific to deployment:
- Check the main project README.md
- Review system logs: `sudo journalctl -u idotmatrix`
- Test Bluetooth connectivity: `bluetoothctl scan on`
- Verify Python dependencies: `pip list`
