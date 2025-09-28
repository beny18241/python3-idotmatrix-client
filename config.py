#!/usr/bin/env python3
"""
iDotMatrix Calendar Configuration

Edit this file to configure your calendar integration settings.
"""

# =============================================================================
# CALENDAR CONFIGURATION
# =============================================================================

# Your ICS calendar URL (Outlook/Exchange calendar)
ICS_CALENDAR_URL = "https://outlook.office365.com/owa/calendar/144d73fdf2654fb3b92983ee16e9d0b3@genpt.com/e829a99fc26b4c66a482420d04ea689513863417029725141930/calendar.ics"

# Your iDotMatrix device Bluetooth address
# Find this by running: ./run_in_venv.sh --scan
DEVICE_ADDRESS = "DD:4F:93:46:DF:1A"  # Replace with your device address

# =============================================================================
# DISPLAY SETTINGS
# =============================================================================

# Default calendar view when no argument is provided
DEFAULT_CALENDAR_VIEW = "current"  # Options: "current", "next", "today", "tomorrow"

# Text display settings
TEXT_SIZE = 10
TEXT_COLOR = "255-255-255"  # RGB format: R-G-B
TEXT_SPEED = 50

# =============================================================================
# TIMEZONE SETTINGS
# =============================================================================

# Your timezone for ICS calendar parsing
TIMEZONE = "Europe/Warsaw"

# =============================================================================
# OAuth SETTINGS (Optional - for Google Calendar integration)
# =============================================================================

# OAuth credentials file (download from Google Cloud Console)
OAUTH_CREDENTIALS_FILE = "credentials.json"

# OAuth token file (auto-generated after authentication)
OAUTH_TOKEN_FILE = "token.json"

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================

# ICS refresh interval in seconds (how often to check for updates)
ICS_REFRESH_INTERVAL = 300  # 5 minutes

# Maximum number of events to display
MAX_EVENTS_DISPLAY = 3

# Event text length limit
MAX_TEXT_LENGTH = 200
