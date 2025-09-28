# iDotMatrix Calendar Scheduler - Remote Deployment Guide

This guide shows how to deploy the calendar scheduler as a system service on remote servers.

## 🚀 Quick Deployment

### 1. **Clone Repository on Remote Server**
```bash
git clone https://github.com/beny18241/python3-idotmatrix-client.git
cd python3-idotmatrix-client
```

### 2. **Install Dependencies**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install schedule
```

### 3. **Configure Calendar Sources**
```bash
# Edit config.py with your settings
nano config.py

# Set your ICS calendar URL
ICS_CALENDAR_URL = "https://your-outlook-calendar-url.ics"

# Set your iDotMatrix device address
DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"
```

### 4. **Setup Google Calendar (Optional)**
```bash
# For Google Calendar OAuth
python3 oauth_calendar_final.py

# For Google Calendar Service Account
python3 calendar_service_account.py
```

### 5. **Install as System Service**
```bash
# Make scripts executable
chmod +x setup_calendar_service.sh
chmod +x manage_calendar_service.sh

# Install service
./setup_calendar_service.sh
```

## 🛠️ Service Management

### **Basic Commands**
```bash
# Check service status
./manage_calendar_service.sh status

# View logs
./manage_calendar_service.sh logs

# Test calendar detection
./manage_calendar_service.sh test

# Restart service
./manage_calendar_service.sh restart

# Stop service
./manage_calendar_service.sh stop

# Start service
./manage_calendar_service.sh start
```

### **Advanced Commands**
```bash
# View recent logs (last 50 lines)
./manage_calendar_service.sh logs-tail

# Uninstall service
./manage_calendar_service.sh uninstall
```

## 📊 Monitoring

### **Log Files**
- **Main logs**: `logs/calendar_scheduler.log` - All calendar activities
- **Service logs**: `logs/service.log` - Service startup/shutdown
- **Error logs**: `logs/service.error.log` - Service errors

### **System Logs**
```bash
# Linux (systemd)
sudo journalctl -u idotmatrix-calendar-scheduler -f

# macOS (launchd)
tail -f logs/service.log
```

## 🔧 Configuration

### **Calendar Sources**
The scheduler supports multiple calendar sources:

1. **ICS Calendar** (Outlook/Exchange)
   - Set `ICS_CALENDAR_URL` in `config.py`
   - Most reliable source

2. **Google Calendar OAuth**
   - Personal Google account
   - Requires `credentials.json` and `token.json`

3. **Google Calendar Service Account**
   - Service account authentication
   - Requires `service-account.json`

### **Priority Logic**
- If **any** calendar shows "busy" → displays "BUSY"
- Only shows "FREE" if **all** calendars show free
- Priority: ICS → Google OAuth → Google Service Account

## 🚨 Troubleshooting

### **Service Not Starting**
```bash
# Check service status
./manage_calendar_service.sh status

# View error logs
tail -f logs/service.error.log

# Test manually
python3 calendar_scheduler_all.py test
```

### **Calendar Not Detected**
```bash
# Test each calendar source
python3 ics_calendar_simple.py current
python3 oauth_calendar_final.py
python3 calendar_integration_service.py
```

### **Device Connection Issues**
```bash
# Test device connection
./run_in_venv.sh --scan

# Update device address in config.py
nano config.py
```

## 📈 Performance

### **Resource Usage**
- **CPU**: Minimal (checks every 30 minutes)
- **Memory**: ~50MB
- **Network**: Light (calendar API calls)
- **Disk**: Log files (~1MB/day)

### **Scaling**
- Single instance per iDotMatrix device
- Can run multiple instances for multiple devices
- Each instance needs separate config.py

## 🔒 Security

### **File Permissions**
```bash
# Secure configuration files
chmod 600 config.py
chmod 600 credentials.json
chmod 600 token.json
chmod 600 service-account.json
```

### **Service Security**
- Runs as regular user (not root)
- Limited file system access
- No network ports opened

## 📋 Maintenance

### **Regular Tasks**
```bash
# Check service health (weekly)
./manage_calendar_service.sh status

# Review logs (weekly)
tail -n 100 logs/calendar_scheduler.log

# Update dependencies (monthly)
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### **Log Rotation**
```bash
# Install logrotate (Linux)
sudo apt-get install logrotate

# Create logrotate config
sudo nano /etc/logrotate.d/idotmatrix-calendar
```

## 🎯 Production Deployment

### **Recommended Setup**
1. **Dedicated server** with stable internet
2. **UPS backup** for power outages
3. **Monitoring** with alerts for service failures
4. **Backup** of configuration files

### **Monitoring Script**
```bash
#!/bin/bash
# health_check.sh
if ! ./manage_calendar_service.sh status | grep -q "running"; then
    echo "Service down - restarting"
    ./manage_calendar_service.sh restart
fi
```

## 📞 Support

- **GitHub Issues**: https://github.com/beny18241/python3-idotmatrix-client/issues
- **Documentation**: See README.md
- **Logs**: Check `logs/calendar_scheduler.log` for detailed information
