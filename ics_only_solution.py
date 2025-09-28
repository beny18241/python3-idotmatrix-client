#!/usr/bin/env python3
"""
ICS Only Solution
Simple solution using only ICS calendar (which is working perfectly)
"""

import os
import sys
import subprocess
from ics_calendar_simple import get_ics_events_for_tomorrow_simple, get_ics_events_for_current_simple, get_ics_events_for_today_simple

def get_ics_events_only(meeting_type="tomorrow"):
    """Get events from ICS calendar only"""
    
    print(f"🔧 Getting {meeting_type} events from ICS calendar")
    print("=" * 60)
    
    try:
        # Load configuration
        from config import ICS_CALENDAR_URL, DEVICE_ADDRESS
        ics_url = ICS_CALENDAR_URL
        
        if meeting_type == "tomorrow":
            events = get_ics_events_for_tomorrow_simple(ics_url)
        elif meeting_type == "current":
            events = get_ics_events_for_current_simple(ics_url)
        elif meeting_type == "today":
            events = get_ics_events_for_today_simple(ics_url)
        else:
            events = "Invalid meeting type"
        
        if events and events != "No events found":
            print(f"✅ ICS Calendar: {events}")
            return events
        else:
            print("❌ No events in ICS Calendar")
            return "No events found"
            
    except Exception as e:
        print(f"❌ ICS Calendar error: {e}")
        return "Error fetching events"

def display_ics_events_on_device(device_address, meeting_type="tomorrow"):
    """Display ICS events on iDotMatrix device"""
    
    print(f"🔧 Displaying {meeting_type} events on device {device_address}")
    print("=" * 60)
    
    # Get events from ICS calendar
    events = get_ics_events_only(meeting_type)
    
    if not events or events == "No events found":
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
        print("Usage: python3 ics_only_solution.py [device_address] [meeting_type]")
        print("  device_address: Bluetooth address of iDotMatrix device (optional if in config.py)")
        print("  meeting_type: current, today, tomorrow (default: tomorrow)")
        print()
        print("Examples:")
        print("  python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")
        print("  python3 ics_only_solution.py tomorrow  # Uses device from config.py")
        print("  python3 ics_only_solution.py current  # Uses device from config.py")
        print()
        print("🔧 This solution uses:")
        print("   • ICS Calendar (direct access) - Working perfectly!")
        print("   • Configuration from config.py")
        return
    
    # Parse arguments
    if len(sys.argv) == 2:
        # Only meeting type provided, use device from config
        try:
            from config import DEVICE_ADDRESS
            device_address = DEVICE_ADDRESS
            meeting_type = sys.argv[1]
        except ImportError:
            print("❌ Configuration file not found!")
            print("   Please create config.py with your DEVICE_ADDRESS")
            print("   Or use: python ics_only_solution.py <device_address> <meeting_type>")
            return
    else:
        # Both device and meeting type provided
        device_address = sys.argv[1]
        meeting_type = sys.argv[2]
    
    # Display ICS events on device
    success = display_ics_events_on_device(device_address, meeting_type)
    
    if success:
        print("\n🎉 Success! Events are now displayed on your iDotMatrix device!")
        print("📋 This solution uses:")
        print("   • ICS Calendar (direct access) - Working perfectly!")
    else:
        print("\n❌ Failed to display events on device")
        print("Please check:")
        print("1. Device address is correct")
        print("2. iDotMatrix device is connected")
        print("3. Internet connection is working")

if __name__ == '__main__':
    main()
