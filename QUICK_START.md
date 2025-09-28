# iDotMatrix Calendar Integration - Quick Start

## 🚀 New Users - Start Here!

### 1. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Find Your Device
```bash
./run_in_venv.sh --scan
# Note down your device address (e.g., DD:4F:93:46:DF:1A)
```

### 3. Choose Your Calendar Setup

#### Option A: ICS Calendar Only (Easiest)
1. Edit `ics_calendar_simple.py` - replace `YOUR_CALENDAR_ID` with your ICS URL
2. Test: `python3 test_ics_simple.py`
3. Use: `python3 ics_only_solution.py YOUR_DEVICE_ADDRESS tomorrow`

#### Option B: Google Calendar + ICS (Full Features)
1. Create OAuth credentials in [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Download `credentials.json` to project folder
3. Setup SSH tunnel: `ssh -L 8080:localhost:8080 user@server`
4. Authenticate: `source venv/bin/activate && python3 oauth_ssh_tunnel_alt.py`
5. Edit `ics_calendar_simple.py` for your ICS URL (optional)
6. Use: `./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS tomorrow`

## 📋 Quick Commands

### Display Calendar Events
```bash
# Tomorrow's events (combined)
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS tomorrow

# Current events
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS current

# Today's events
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS today

# ICS only (no Google auth needed)
python3 ics_only_solution.py YOUR_DEVICE_ADDRESS tomorrow
```

### Check Status
```bash
# Check OAuth token
source venv/bin/activate && python3 check_token_status.py

# Test ICS calendar
python3 test_ics_simple.py
```

### Basic Device Commands
```bash
# Set text
./run_in_venv.sh --address YOUR_DEVICE_ADDRESS --set-text "Hello World"

# Show clock
./run_in_venv.sh --address YOUR_DEVICE_ADDRESS --clock 0

# Set image
./run_in_venv.sh --address YOUR_DEVICE_ADDRESS --image true --set-image ./images/demo_32.png
```

## 🔧 Configuration

Copy `calendar_config_template.py` and customize:
- Device address
- ICS calendar URL
- Timezone
- Display preferences

## 🆘 Troubleshooting

### Can't Connect to Device
```bash
# Scan for devices
./run_in_venv.sh --scan

# Make sure device is on and in pairing mode
# Check Bluetooth is enabled
```

### OAuth Issues
```bash
# Check token status
source venv/bin/activate && python3 check_token_status.py

# Fix token
source venv/bin/activate && python3 fix_server_oauth.py

# Regenerate token
source venv/bin/activate && python3 fix_oauth_now.py
```

### ICS Calendar Issues
```bash
# Test ICS access
python3 test_ics_simple.py

# Edit ics_calendar_simple.py to fix URL
```

## 📝 Notes

- **OAuth Token**: Auto-refreshes for 6+ months
- **ICS Calendar**: No authentication needed
- **Combined Solution**: Best of both worlds
- **Remote Server**: Works with SSH tunneling

## 📖 Full Documentation

See `README.md` for complete documentation and advanced features.
