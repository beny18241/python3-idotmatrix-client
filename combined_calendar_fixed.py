#!/usr/bin/env python3
"""
Combined Calendar Solution (Fixed)
Combines Google Calendar service account with ICS calendar access
Handles both calendars working together
"""

import os
import sys
import subprocess
import json
import datetime
from ics_calendar_simple import get_ics_events_for_tomorrow_simple, get_ics_events_for_current_simple, get_ics_events_for_today_simple

def get_google_calendar_events(meeting_type="tomorrow"):
    """Get events from Google Calendar using service account"""
    
    try:
        # Import here to avoid errors if Google libraries not available
        from calendar_display_all_calendars import get_events_from_all_calendars
        
        print("1️⃣ Checking Google Calendar...")
        google_events = get_events_from_all_calendars(meeting_type)
        
        if google_events and google_events != "No events found":
            print(f"✅ Google Calendar: {google_events}")
            return google_events
        else:
            print("❌ No events in Google Calendar")
            return None
            
    except Exception as e:
        print(f"❌ Google Calendar error: {e}")
        return None

def get_ics_calendar_events(meeting_type="tomorrow"):
    """Get events from ICS calendar"""
    
    try:
        print("2️⃣ Checking ICS Calendar...")
        ics_url = "https://outlook.office365.com/owa/calendar/144d73fdf2654fb3b92983ee16e9d0b3@genpt.com/e829a99fc26b4c66a482420d04ea689513863417029725141930/calendar.ics"
        
        if meeting_type == "tomorrow":
            ics_events = get_ics_events_for_tomorrow_simple(ics_url)
        elif meeting_type == "current":
            ics_events = get_ics_events_for_current_simple(ics_url)
        elif meeting_type == "today":
            ics_events = get_ics_events_for_today_simple(ics_url)
        else:
            ics_events = "Invalid meeting type"
        
        if ics_events and ics_events != "No events found":
            print(f"✅ ICS Calendar: {ics_events}")
            return ics_events
        else:
            print("❌ No events in ICS Calendar")
            return None
            
    except Exception as e:
        print(f"❌ ICS Calendar error: {e}")
        return None

def combine_events(google_events, ics_events):
    """Combine events from both sources"""
    
    print("3️⃣ Combining events from all sources...")
    
    events_list = []
    
    if google_events and google_events != "No events found":
        # Extract Google Calendar events
        if "Tomorrow:" in google_events:
            google_text = google_events.replace("Tomorrow:", "").strip()
            events_list.append(f"Google: {google_text}")
        else:
            events_list.append(f"Google: {google_events}")
    
    if ics_events and ics_events != "No events found":
        # Extract ICS Calendar events
        if "Tomorrow:" in ics_events:
            ics_text = ics_events.replace("Tomorrow:", "").strip()
            events_list.append(f"ICS: {ics_text}")
        else:
            events_list.append(f"ICS: {ics_events}")
    
    if not events_list:
        return "No events found"
    
    # Combine events
    if len(events_list) == 1:
        return events_list[0]
    else:
        return " | ".join(events_list)

def get_combined_events_fixed(meeting_type="tomorrow"):
    """Get events from both Google Calendar and ICS calendar"""
    
    print(f"🔧 Getting {meeting_type} events from all sources")
    print("=" * 60)
    
    # Get Google Calendar events
    google_events = get_google_calendar_events(meeting_type)
    
    # Get ICS Calendar events
    ics_events = get_ics_calendar_events(meeting_type)
    
    # Combine events
    combined_events = combine_events(google_events, ics_events)
    
    print(f"📅 Combined events: {combined_events}")
    return combined_events

def display_combined_events_on_device_fixed(device_address, meeting_type="tomorrow"):
    """Display combined events on iDotMatrix device"""
    
    print(f"🔧 Displaying {meeting_type} events on device {device_address}")
    print("=" * 60)
    
    # Get events from all sources
    events = get_combined_events_fixed(meeting_type)
    
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
        print("Usage: python combined_calendar_fixed.py <device_address> [meeting_type]")
        print("  device_address: Bluetooth address of iDotMatrix device")
        print("  meeting_type: current, today, tomorrow (default: tomorrow)")
        print()
        print("Examples:")
        print("  python combined_calendar_fixed.py DD:4F:93:46:DF:1A tomorrow")
        print("  python combined_calendar_fixed.py DD:4F:93:46:DF:1A current")
        print("  python combined_calendar_fixed.py DD:4F:93:46:DF:1A today")
        print()
        print("🔧 This solution combines:")
        print("   • Google Calendar (via service account)")
        print("   • ICS Calendar (direct access)")
        return
    
    device_address = sys.argv[1]
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "tomorrow"
    
    # Display combined events on device
    success = display_combined_events_on_device_fixed(device_address, meeting_type)
    
    if success:
        print("\n🎉 Success! Events are now displayed on your iDotMatrix device!")
        print("📋 This solution combines:")
        print("   • Google Calendar (via service account)")
        print("   • ICS Calendar (direct access)")
    else:
        print("\n❌ Failed to display events on device")
        print("Please check:")
        print("1. Device address is correct")
        print("2. iDotMatrix device is connected")
        print("3. Internet connection is working")
        print("4. Google Calendar service account is properly configured")

if __name__ == '__main__':
    main()
