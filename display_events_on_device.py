#!/usr/bin/env python3
"""
Display events on iDotMatrix device
Simple script to display calendar events on the iDotMatrix device
"""

import os
import sys
import subprocess
from calendar_display_all_calendars import get_events_from_all_calendars

def display_events_on_device(device_address, meeting_type="tomorrow"):
    """Display events on iDotMatrix device"""
    
    print(f"🔧 Displaying {meeting_type} events on device {device_address}")
    print("=" * 60)
    
    # Get events from all calendars
    events = get_events_from_all_calendars(meeting_type)
    
    if not events:
        print("❌ No events found!")
        return False
    
    print(f"📅 Events: {events}")
    
    # Display on device
    try:
        # Use the run script to display text
        cmd = [
            "./run_in_venv.sh",
            "--address", device_address,
            "--set-text", events
        ]
        
        print(f"🚀 Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Events displayed successfully on iDotMatrix device!")
            print(f"📱 Displayed: {events}")
            return True
        else:
            print(f"❌ Failed to display on device: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error displaying on device: {e}")
        return False

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python display_events_on_device.py <device_address> [meeting_type]")
        print("  device_address: Bluetooth address of iDotMatrix device")
        print("  meeting_type: current, next, today, tomorrow (default: tomorrow)")
        print()
        print("Examples:")
        print("  python display_events_on_device.py DD:4F:93:46:DF:1A tomorrow")
        print("  python display_events_on_device.py DD:4F:93:46:DF:1A current")
        print("  python display_events_on_device.py DD:4F:93:46:DF:1A next")
        return
    
    device_address = sys.argv[1]
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "tomorrow"
    
    # Display events on device
    success = display_events_on_device(device_address, meeting_type)
    
    if success:
        print("\n🎉 Success! Events are now displayed on your iDotMatrix device!")
    else:
        print("\n❌ Failed to display events on device")
        print("Please check:")
        print("1. Device address is correct")
        print("2. iDotMatrix device is connected")
        print("3. Service account has access to calendars")

if __name__ == '__main__':
    main()
