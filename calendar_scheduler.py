#!/usr/bin/env python3
"""
Calendar Scheduler

This script runs calendar updates every 30 minutes and displays status on iDotMatrix.
"""

import time
import schedule
import subprocess
import sys
import os
from datetime import datetime

def get_current_status():
    """Get current calendar status from both ICS and Google Calendar"""
    
    print("🔍 Checking all calendar sources...")
    
    # Try ICS Calendar first
    ics_status = None
    ics_events = None
    try:
        from config import ICS_CALENDAR_URL
        from ics_calendar_simple import get_ics_events_for_current_simple
        
        print("📅 Checking ICS Calendar...")
        current_events = get_ics_events_for_current_simple(ICS_CALENDAR_URL)
        
        if current_events and current_events != "Free":
            ics_status = "busy"
            ics_events = current_events
            print(f"✅ ICS Calendar: BUSY - {current_events}")
        else:
            ics_status = "free"
            ics_events = "Free"
            print("✅ ICS Calendar: FREE")
            
    except Exception as e:
        print(f"❌ ICS Calendar error: {e}")
        ics_status = "error"
        ics_events = "ICS Error"
    
    # Try Google Calendar OAuth
    google_status = None
    google_events = None
    try:
        from calendar_display_oauth import get_calendar_info_oauth
        
        print("📅 Checking Google Calendar OAuth...")
        current_events = get_calendar_info_oauth("current")
        
        if current_events and current_events != "Free":
            google_status = "busy"
            google_events = current_events
            print(f"✅ Google Calendar: BUSY - {current_events}")
        else:
            google_status = "free"
            google_events = "Free"
            print("✅ Google Calendar: FREE")
            
    except Exception as e:
        print(f"❌ Google Calendar OAuth error: {e}")
        google_status = "error"
        google_events = "Google OAuth Error"
    
    # Combine results - if any calendar shows busy, we're busy
    if ics_status == "busy" or google_status == "busy":
        # Prefer the one that's not an error
        if ics_status == "busy":
            return "busy", f"ICS: {ics_events}"
        elif google_status == "busy":
            return "busy", f"Google: {google_events}"
    
    # Check for errors
    if ics_status == "error" and google_status == "error":
        return "error", "Both calendars failed"
    elif ics_status == "error":
        return "error", f"ICS failed, Google: {google_events}"
    elif google_status == "error":
        return "error", f"Google failed, ICS: {ics_events}"
    
    # Both show free
    return "free", "Free"

def display_status_on_device(status, events):
    """Display status on iDotMatrix device with animated emoji GIFs"""
    
    try:
        from config import DEVICE_ADDRESS
        
        # Check if emoji GIFs with meeting titles exist, create them if not
        if not os.path.exists("images/free_emoji_with_meeting_title.gif"):
            print("Creating emoji GIFs with meeting titles...")
            import create_emoji_gifs_with_meeting_titles
            create_emoji_gifs_with_meeting_titles.main()
        
        if status == "free":
            # Animated green checkmark with large "FREE" text for free
            gif_path = "images/free_emoji_with_meeting_title.gif"
            print(f"Displaying FREE animation with meeting title: {gif_path}")
            
            # Use the run script to display animated GIF
            cmd = [
                "./run_in_venv.sh",
                "--address", DEVICE_ADDRESS,
                "--set-gif", gif_path
            ]
            
        elif status == "busy":
            # Animated red X with large "CALL" text for busy
            gif_path = "images/busy_emoji_with_meeting_title.gif"
            print(f"Displaying CALL animation with meeting title: {gif_path}")
            
            # Use the run script to display animated GIF
            cmd = [
                "./run_in_venv.sh",
                "--address", DEVICE_ADDRESS,
                "--set-gif", gif_path
            ]
            
        else:
            # Animated orange warning with large "ERROR" text for error
            gif_path = "images/error_emoji_with_meeting_title.gif"
            print(f"Displaying ERROR animation with meeting title: {gif_path}")
            
            # Use the run script to display animated GIF
            cmd = [
                "./run_in_venv.sh",
                "--address", DEVICE_ADDRESS,
                "--set-gif", gif_path
            ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Status displayed with animated emoji")
            return True
        else:
            print(f"❌ Failed to display: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error displaying on device: {e}")
        return False

def update_calendar_status():
    """Update calendar status on device"""
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n🕐 [{timestamp}] Updating calendar status...")
    
    # Get current status
    status, events = get_current_status()
    
    print(f"📊 Status: {status}")
    print(f"📅 Events: {events}")
    
    # Display on device
    success = display_status_on_device(status, events)
    
    if success:
        print(f"✅ Calendar status updated successfully")
    else:
        print(f"❌ Failed to update calendar status")
    
    return success

def run_scheduler():
    """Run the calendar scheduler"""
    
    print("🕐 Calendar Scheduler Started")
    print("=" * 50)
    print("📅 Updates every 30 minutes")
    print("🟢 FREE = Available")
    print("🔴 BUSY = In meeting")
    print("⚠️ ERROR = Connection issue")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Schedule updates every 30 minutes
    schedule.every(30).minutes.do(update_calendar_status)
    
    # Run initial update
    update_calendar_status()
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
        sys.exit(0)

def main():
    """Main function"""
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("🧪 Testing calendar status update...")
        update_calendar_status()
    else:
        run_scheduler()

if __name__ == "__main__":
    main()
