# Calendar Scheduler Setup

## 🕐 **Automatic Calendar Updates Every 30 Minutes**

### **Features:**
- ✅ **🟢 FREE** - Green icon when available
- ✅ **🔴 BUSY** - Red icon with meeting title when occupied
- ✅ **⚠️ ERROR** - Yellow warning for connection issues
- ✅ **Smart Text Sizing** - Smaller text for meetings, larger for status
- ✅ **Auto-refresh** - Updates every 30 minutes

## 🚀 **Quick Setup**

### **1. Install Dependencies**
```bash
# Install schedule library
pip install schedule

# Or run the setup script
./setup_scheduler.sh
```

### **2. Test the Scheduler**
```bash
# Test once
python3 calendar_scheduler.py test

# Test status display
python3 calendar_status_display.py status
python3 calendar_status_display.py display
```

### **3. Run Scheduler**
```bash
# Run continuously (every 30 minutes)
python3 calendar_scheduler.py
```

## 🔧 **Advanced Setup (Server)**

### **Systemd Service (Recommended)**
```bash
# Copy service file
sudo cp calendar-scheduler.service /etc/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable calendar-scheduler
sudo systemctl start calendar-scheduler

# Check status
sudo systemctl status calendar-scheduler

# View logs
sudo journalctl -u calendar-scheduler -f
```

### **Cron Alternative**
```bash
# Edit crontab
crontab -e

# Add this line (every 30 minutes)
*/30 * * * * cd /opt/idotmatrix && python3 calendar_scheduler.py test
```

## 📊 **Status Display Options**

### **Manual Status Check**
```bash
# Show current status
python3 calendar_status_display.py status

# Display on device
python3 calendar_status_display.py display

# Update and display
python3 calendar_status_display.py update
```

### **Status Indicators**
- **🟢 FREE** - Available for meetings (Green, size 8)
- **🔴 MEETING** - In a meeting (Red, size 6, shows meeting title)
- **⚠️ ERROR** - Connection issue (Yellow, size 8)

## 🎯 **Display Features**

### **When FREE:**
- 🟢 Green circle icon
- "FREE" text
- Larger text (size 8)
- Green color
- Slower animation

### **When BUSY:**
- 🔴 Red circle icon
- Meeting title (truncated if long)
- Smaller text (size 6)
- Red color
- Faster animation

### **When ERROR:**
- ⚠️ Warning icon
- "ERROR" text
- Medium text (size 8)
- Yellow color

## 🔧 **Configuration**

### **Update Frequency**
Edit `calendar_scheduler.py` line 95:
```python
# Change from 30 minutes to any interval
schedule.every(15).minutes.do(update_calendar_status)  # Every 15 minutes
schedule.every(1).hour.do(update_calendar_status)      # Every hour
```

### **Text Sizing**
Edit `calendar_status_display.py`:
```python
# Free status
text_size = 8  # Larger for status

# Busy status  
text_size = 6  # Smaller for meeting titles
```

## 📋 **Usage Examples**

### **Development (Local)**
```bash
# Test once
python3 calendar_scheduler.py test

# Run for testing
python3 calendar_scheduler.py
```

### **Production (Server)**
```bash
# Setup systemd service
sudo systemctl enable calendar-scheduler
sudo systemctl start calendar-scheduler

# Monitor
sudo systemctl status calendar-scheduler
```

## 🆘 **Troubleshooting**

### **Device Not Found**
```bash
# Check device address
./run_in_venv.sh --scan

# Update config.py with correct address
```

### **Calendar Not Updating**
```bash
# Test calendar access
python3 test_ics_simple.py

# Check OAuth token
source venv/bin/activate && python3 check_token_status.py
```

### **Service Not Starting**
```bash
# Check service status
sudo systemctl status calendar-scheduler

# View logs
sudo journalctl -u calendar-scheduler -f

# Restart service
sudo systemctl restart calendar-scheduler
```

## 📝 **Notes**

- **Scheduler runs every 30 minutes** by default
- **Status updates automatically** based on calendar events
- **Icons and colors** indicate availability at a glance
- **Meeting titles** are truncated to fit display
- **Error handling** for connection issues
- **Systemd service** for reliable server operation

## 🎉 **Benefits**

- ✅ **Always up-to-date** calendar status
- ✅ **Visual indicators** for quick status check
- ✅ **Automatic updates** without manual intervention
- ✅ **Meeting awareness** with title display
- ✅ **Error handling** for robust operation
