#!/usr/bin/env python3
"""
iDotMatrix Calendar Configuration Template

This file contains the configuration settings for calendar integration.
Copy this file and modify the values according to your setup.
"""

# =============================================================================
# DEVICE CONFIGURATION
# =============================================================================

# Your iDotMatrix device Bluetooth address
# Find this by running: ./run_in_venv.sh --scan
DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"  # Replace with your device address

# =============================================================================
# ICS CALENDAR CONFIGURATION  
# =============================================================================

# Your ICS calendar URL (Outlook/Exchange calendar)
# Get this from your Outlook calendar settings
ICS_CALENDAR_URL = "https://outlook.office365.com/owa/calendar/YOUR_CALENDAR_ID/calendar.ics"

# ICS refresh interval in seconds (how often to check for updates)
ICS_REFRESH_INTERVAL = 300  # 5 minutes

# =============================================================================
# GOOGLE CALENDAR CONFIGURATION
# =============================================================================

# OAuth credentials file (download from Google Cloud Console)
OAUTH_CREDENTIALS_FILE = "credentials.json"

# OAuth token file (auto-generated after authentication)
OAUTH_TOKEN_FILE = "token.json"

# Service account file (alternative to OAuth)
SERVICE_ACCOUNT_FILE = "service-account.json"

# =============================================================================
# DISPLAY CONFIGURATION
# =============================================================================

# Default calendar view type when no argument is provided
DEFAULT_VIEW = "current"  # Options: "current", "next", "today", "tomorrow"

# Text formatting options
TEXT_SIZE = 10
TEXT_COLOR = "255-255-255"  # RGB format: R-G-B
TEXT_SPEED = 50

# =============================================================================
# TIMEZONE CONFIGURATION
# =============================================================================

# Your timezone (for ICS calendar parsing)
TIMEZONE = "Europe/Warsaw"  # Replace with your timezone

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

"""
After configuring this file, you can use these commands:

1. Combined Calendar (Google + ICS):
   ./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS tomorrow

2. ICS Calendar Only:
   python3 ics_only_solution.py YOUR_DEVICE_ADDRESS tomorrow

3. Check OAuth Token Status:
   source venv/bin/activate && python3 check_token_status.py

4. Test ICS Calendar:
   python3 test_ics_simple.py

5. Basic Device Commands:
   ./run_in_venv.sh --address YOUR_DEVICE_ADDRESS --set-text "Hello World"
   ./run_in_venv.sh --address YOUR_DEVICE_ADDRESS --clock 0
"""

# =============================================================================
# TROUBLESHOOTING
# =============================================================================

"""
Common Issues and Solutions:

1. Device Connection Issues:
   - Make sure device is turned on and in pairing mode
   - Check Bluetooth is enabled on your system
   - Verify device address with: ./run_in_venv.sh --scan

2. OAuth Token Issues:
   - Check token status: python3 check_token_status.py
   - Fix token format: python3 fix_server_oauth.py
   - Regenerate token: python3 fix_oauth_now.py

3. ICS Calendar Issues:
   - Test ICS access: python3 test_ics_simple.py
   - Verify ICS URL is accessible in browser
   - Check timezone configuration

4. Google Calendar Issues:
   - Ensure Google Calendar API is enabled
   - Check OAuth credentials are valid
   - Verify calendar sharing permissions
"""
