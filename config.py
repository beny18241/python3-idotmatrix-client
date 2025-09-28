#!/usr/bin/env python3
"""
iDotMatrix Calendar Configuration - Personal Settings

This file contains your personal configuration settings.
This file is NOT committed to git for security.
"""

# =============================================================================
# CALENDAR CONFIGURATION
# =============================================================================

# Your ICS calendar URL (Outlook/Exchange calendar)
ICS_CALENDAR_URL = "provide your ICS calendar URL here"

# Your iDotMatrix device Bluetooth address
# Find this by running: ./run_in_venv.sh --scan
DEVICE_ADDRESS = "DD:4F:93:46:DF:1A"

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

# =============================================================================
# EMOJI GIF TEXT OVERLAY SETTINGS
# =============================================================================

# Enable text overlays on emoji GIFs
ENABLE_TEXT_OVERLAYS = True

# Text overlay settings for different statuses
FREE_TEXT = "FREE"          # Text for free status
BUSY_TEXT = "CALL"         # Text for busy status  
ERROR_TEXT = "ERROR"        # Text for error status

# Text overlay font size (6-12 recommended for 32x32 GIFs)
TEXT_OVERLAY_FONT_SIZE = 6

# Text overlay colors (RGB format: R-G-B)
FREE_TEXT_COLOR = "0-255-0"    # Green
BUSY_TEXT_COLOR = "255-0-0"    # Red
ERROR_TEXT_COLOR = "255-165-0" # Orange
