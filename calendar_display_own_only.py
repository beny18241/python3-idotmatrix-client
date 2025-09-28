#!/usr/bin/env python3
"""
Calendar display for iDotMatrix using only your own calendars
Works with calendars you own and can share with service account
"""

import os
import sys
import json
import subprocess
from calendar_integration_multi import get_calendar_info_multi, get_all_calendars

def get_own_calendars():
    """Get only calendars that you own (can share with service account)"""
    
    calendars = get_all_calendars()
    own_calendars = []
    
    for calendar in calendars:
        calendar_id = calendar.get('id', '')
        summary = calendar.get('summary', 'No Title')
        access_role = calendar.get('accessRole', '')
        
        # Only include calendars you own or have write access to
        if access_role in ['owner', 'writer']:
            own_calendars.append(calendar)
            print(f"✅ Own calendar: {summary} ({access_role})")
        else:
            print(f"❌ Cannot access: {summary} ({access_role})")
    
    return own_calendars

def get_calendar_info_own_only(meeting_type="current"):
    """Get calendar information from your own calendars only"""
    
    own_calendars = get_own_calendars()
    
    if not own_calendars:
        print("❌ No own calendars accessible!")
        return None
    
    # Try each own calendar
    for calendar in own_calendars:
        calendar_id = calendar.get('id', '')
        summary = calendar.get('summary', 'Unknown')
        
        print(f"🔍 Checking calendar: {summary}")
        
        result = get_calendar_info_multi(calendar_id, meeting_type)
        if result and result != "Free" and result != "No meetings":
            print(f"✅ Found meeting in {summary}: {result}")
            return result
        else:
            print(f"📅 No meetings in {summary}")
    
    # If no meetings found in any calendar, return default
    if own_calendars:
        primary_calendar = own_calendars[0]
        calendar_id = primary_calendar.get('id', '')
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
    """Main function for own calendars display"""
    
    if len(sys.argv) < 2:
        print("Usage: python calendar_display_own_only.py <device_address> [meeting_type]")
        print("  device_address: Bluetooth address of iDotMatrix device")
        print("  meeting_type: current, next, today (default: current)")
        return
    
    device_address = sys.argv[1]
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "current"
    
    print(f"🔧 Displaying {meeting_type} meeting from your own calendars on device {device_address}")
    print("=" * 70)
    
    # Get calendar information from your own calendars
    calendar_info = get_calendar_info_own_only(meeting_type)
    
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
