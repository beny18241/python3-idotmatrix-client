#!/usr/bin/env python3
"""
Calendar display for iDotMatrix including imported calendars
Works with both own calendars and imported calendars you have access to
"""

import os
import sys
import json
import subprocess
from calendar_integration_multi import get_calendar_info_multi, get_all_calendars

def get_all_accessible_calendars():
    """Get all calendars you have access to (own + imported)"""
    
    calendars = get_all_calendars()
    accessible_calendars = []
    
    for calendar in calendars:
        calendar_id = calendar.get('id', '')
        summary = calendar.get('summary', 'No Title')
        access_role = calendar.get('accessRole', '')
        
        # Include all calendars you have access to
        if access_role in ['owner', 'writer', 'reader']:
            accessible_calendars.append(calendar)
            print(f"✅ Accessible calendar: {summary} ({access_role})")
        else:
            print(f"❌ Cannot access: {summary} ({access_role})")
    
    return accessible_calendars

def get_calendar_info_all_access(meeting_type="current"):
    """Get calendar information from all accessible calendars"""
    
    accessible_calendars = get_all_accessible_calendars()
    
    if not accessible_calendars:
        print("❌ No accessible calendars found!")
        return None
    
    # Try each accessible calendar
    for calendar in accessible_calendars:
        calendar_id = calendar.get('id', '')
        summary = calendar.get('summary', 'Unknown')
        access_role = calendar.get('accessRole', '')
        
        print(f"🔍 Checking calendar: {summary} ({access_role})")
        
        try:
            result = get_calendar_info_multi(calendar_id, meeting_type)
            if result and result != "Free" and result != "No meetings":
                print(f"✅ Found meeting in {summary}: {result}")
                return result
            else:
                print(f"📅 No meetings in {summary}")
        except Exception as e:
            print(f"❌ Error accessing {summary}: {e}")
            continue
    
    # If no meetings found in any calendar, return default
    if accessible_calendars:
        primary_calendar = accessible_calendars[0]
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
    """Main function for all accessible calendars display"""
    
    if len(sys.argv) < 2:
        print("Usage: python calendar_display_imported.py <device_address> [meeting_type]")
        print("  device_address: Bluetooth address of iDotMatrix device")
        print("  meeting_type: current, next, today (default: current)")
        return
    
    device_address = sys.argv[1]
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "current"
    
    print(f"🔧 Displaying {meeting_type} meeting from all accessible calendars on device {device_address}")
    print("=" * 70)
    
    # Get calendar information from all accessible calendars
    calendar_info = get_calendar_info_all_access(meeting_type)
    
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
