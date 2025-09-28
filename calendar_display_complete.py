#!/usr/bin/env python3
"""
Complete calendar display for iDotMatrix using service account
Displays calendar information on the iDotMatrix device
"""

import os
import sys
import subprocess
import time
from calendar_display_service import get_calendar_info

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
    """Main function for calendar display"""
    
    if len(sys.argv) < 2:
        print("Usage: python calendar_display_complete.py <device_address> [meeting_type]")
        print("  device_address: Bluetooth address of iDotMatrix device")
        print("  meeting_type: current, next, today (default: current)")
        return
    
    device_address = sys.argv[1]
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "current"
    
    print(f"🔧 Displaying {meeting_type} meeting on device {device_address}")
    print("=" * 60)
    
    # Get calendar information
    calendar_info = get_calendar_info(meeting_type)
    
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
