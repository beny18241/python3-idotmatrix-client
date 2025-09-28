# iDotMatrix Calendar Integration

This guide shows how to set up Google Calendar integration with your iDotMatrix device using service account authentication.

## 🚀 Quick Start

### 1. Set up Service Account Authentication

```bash
# Run the service account setup
python calendar_service_account.py
```

Follow the instructions to:
- Create a service account in Google Cloud Console
- Download the service account JSON file
- Share your calendar with the service account

### 2. Test Calendar Integration

```bash
# Test the service account integration
python calendar_integration_service.py
```

### 3. Display Calendar on iDotMatrix Device

```bash
# Display current meeting
python calendar_display_complete.py DD:4F:93:46:DF:1A current

# Display next meeting
python calendar_display_complete.py DD:4F:93:46:DF:1A next

# Display today's meetings count
python calendar_display_complete.py DD:4F:93:46:DF:1A today
```

## 📁 File Structure

### Working Files (Keep These)
- `calendar_service_account.py` - Service account setup and authentication
- `calendar_integration_service.py` - Service account calendar functions
- `calendar_display_service.py` - Calendar display functions
- `calendar_display_complete.py` - Complete calendar display for iDotMatrix
- `requirements.txt` - Python dependencies
- `DEPLOYMENT.md` - Server deployment guide

### Deployment Files
- `deploy_simple.sh` - Simple Python deployment
- `deploy_docker.sh` - Docker deployment
- `deploy_complete.sh` - Complete systemd service deployment
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose configuration

## 🔧 Usage Examples

### Basic Calendar Display
```bash
# Get current meeting text
python calendar_display_service.py current

# Get next meeting text
python calendar_display_service.py next

# Get today's meetings count
python calendar_display_service.py today
```

### Display on iDotMatrix Device
```bash
# Display current meeting on device
python calendar_display_complete.py DD:4F:93:46:DF:1A current
```

### Continuous Display
```bash
# Update every 30 seconds
while true; do
    python calendar_display_complete.py DD:4F:93:46:DF:1A current
    sleep 30
done
```

## 🛠️ Troubleshooting

### Service Account Issues
- Make sure `service-account.json` exists
- Verify the service account has calendar access
- Check that your calendar is shared with the service account

### Device Connection Issues
- Ensure Bluetooth is enabled
- Check device address is correct
- Try running `./run_in_venv.sh --scan` to find devices

## 📋 Dependencies

- Python 3.7+
- Google API Python Client
- iDotMatrix library
- Bluetooth support

## 🎉 Success!

Once set up, you'll have:
- ✅ Google Calendar integration working
- ✅ iDotMatrix device displaying calendar info
- ✅ No OAuth authentication issues
- ✅ Reliable server deployment
