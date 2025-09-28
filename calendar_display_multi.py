#!/usr/bin/env python3
"""
Multi-calendar display for iDotMatrix using service account
Supports multiple Google Calendars with configuration
"""

import os
import sys
import json
import subprocess
from calendar_integration_multi import get_calendar_info_multi, get_all_calendars

def load_calendar_config():
    """Load calendar configuration from JSON file"""
    config_file = 'calendar_config.json'
    
    if not os.path.exists(config_file):
        print("❌ Calendar configuration file not found!")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Failed to load calendar config: {e}")
        return None

def get_calendar_info_from_config(meeting_type="current"):
    """Get calendar information using configuration"""
    
    config = load_calendar_config()
    if not config:
        return None
    
    calendars = config.get('calendars', {})
    default_calendar = config.get('default_calendar', 'primary')
    
    # Try default calendar first
    if default_calendar in calendars:
        calendar_config = calendars[default_calendar]
        if calendar_config.get('enabled', True):
            calendar_id = calendar_config.get('id', default_calendar)
            result = get_calendar_info_multi(calendar_id, meeting_type)
            if result and result != "Free" and result != "No meetings":
                return result
    
    # Try other enabled calendars
    for calendar_name, calendar_config in calendars.items():
        if calendar_name == default_calendar:
            continue
        
        if calendar_config.get('enabled', True):
            calendar_id = calendar_config.get('id', calendar_name)
            result = get_calendar_info_multi(calendar_id, meeting_type)
            if result and result != "Free" and result != "No meetings":
                return result
    
    # If no meetings found in any calendar, return default
    if default_calendar in calendars:
        calendar_config = calendars[default_calendar]
        calendar_id = calendar_config.get('id', default_calendar)
        return get_calendar_info_multi(calendar_id, meeting_type)
    
    return "No meetings found"

def display_on_device(device_address, text):
    """Display text on iDotMatrix device"""
    try:
        # Use the run script to display text
        cmd = [
            "./run_in_venv.sh",
            "--address", device_address,
            "--set-text", text
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Displayed on device: {text}")
            return True
        else:
            print(f"❌ Failed to display on device: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error displaying on device: {e}")
        return False

def main():
    """Main function for multi-calendar display"""
    
    if len(sys.argv) < 2:
        print("Usage: python calendar_display_multi.py <device_address> [meeting_type]")
        print("  device_address: Bluetooth address of iDotMatrix device")
        print("  meeting_type: current, next, today (default: current)")
        return
    
    device_address = sys.argv[1]
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "current"
    
    print(f"🔧 Displaying {meeting_type} meeting from multiple calendars on device {device_address}")
    print("=" * 70)
    
    # Get calendar information from configuration
    calendar_info = get_calendar_info_from_config(meeting_type)
    
    if calendar_info:
        print(f"📅 Calendar info: {calendar_info}")
        
        # Display on device
        if display_on_device(device_address, calendar_info):
            print("✅ Calendar information displayed successfully!")
        else:
            print("❌ Failed to display on device")
    else:
        print("❌ Failed to get calendar information")

if __name__ == '__main__':
    main()
