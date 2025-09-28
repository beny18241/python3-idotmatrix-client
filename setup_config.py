#!/usr/bin/env python3
"""
Setup Configuration for iDotMatrix Calendar Integration

This script helps you create a config.py file with your settings.
"""

import os

def create_config():
    """Create config.py file with user input"""
    
    print("🔧 iDotMatrix Calendar Configuration Setup")
    print("=" * 50)
    
    # Check if config.py already exists
    if os.path.exists("config.py"):
        overwrite = input("📁 config.py already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("❌ Setup cancelled.")
            return
    
    print("\n📋 Please provide the following information:")
    print()
    
    # Get ICS calendar URL
    print("1️⃣ ICS Calendar URL")
    print("   This is your Outlook/Exchange calendar export URL")
    print("   Example: https://outlook.office365.com/owa/calendar/.../calendar.ics")
    ics_url = input("   ICS URL: ").strip()
    
    if not ics_url:
        print("❌ ICS URL is required!")
        return
    
    # Get device address
    print("\n2️⃣ iDotMatrix Device Address")
    print("   Find this by running: ./run_in_venv.sh --scan")
    device_address = input("   Device Address (e.g., DD:4F:93:46:DF:1A): ").strip()
    
    if not device_address:
        print("❌ Device address is required!")
        return
    
    # Get timezone
    print("\n3️⃣ Timezone")
    print("   Your timezone for calendar parsing")
    timezone = input("   Timezone (default: Europe/Warsaw): ").strip()
    if not timezone:
        timezone = "Europe/Warsaw"
    
    # Create config.py content
    config_content = f'''#!/usr/bin/env python3
"""
iDotMatrix Calendar Configuration

Edit this file to configure your calendar integration settings.
"""

# =============================================================================
# CALENDAR CONFIGURATION
# =============================================================================

# Your ICS calendar URL (Outlook/Exchange calendar)
ICS_CALENDAR_URL = "{ics_url}"

# Your iDotMatrix device Bluetooth address
# Find this by running: ./run_in_venv.sh --scan
DEVICE_ADDRESS = "{device_address}"

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
TIMEZONE = "{timezone}"

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
'''
    
    # Write config.py
    try:
        with open("config.py", "w") as f:
            f.write(config_content)
        
        print("\n✅ Configuration created successfully!")
        print("📁 File: config.py")
        print()
        print("🚀 You can now use:")
        print("   python3 ics_only_solution.py tomorrow")
        print("   python3 ics_only_solution.py current")
        print("   python3 ics_only_solution.py today")
        print()
        print("🔧 Or with device address:")
        print(f"   python3 ics_only_solution.py {device_address} tomorrow")
        
    except Exception as e:
        print(f"❌ Error creating config.py: {e}")

def main():
    """Main function"""
    create_config()

if __name__ == "__main__":
    main()
