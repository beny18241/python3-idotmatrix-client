#!/usr/bin/env python3
"""
Unified Calendar Scheduler
Combines all calendar sources: ICS, Google Calendar OAuth, and Google Calendar Service Account
Runs every 30 minutes and displays status on iDotMatrix device
"""

import time
import schedule
import subprocess
import sys
import os
from datetime import datetime

def get_ics_calendar_status():
    """Get current status from ICS calendar"""
    
    try:
        from config import ICS_CALENDAR_URL
        from ics_calendar_simple import get_ics_events_for_current_simple
        
        print("📅 Checking ICS Calendar...")
        current_events = get_ics_events_for_current_simple(ICS_CALENDAR_URL)
        
        if current_events and current_events != "Free":
            return "busy", current_events, "ICS"
        else:
            return "free", "Free", "ICS"
            
    except Exception as e:
        print(f"❌ ICS Calendar error: {e}")
        return "error", "ICS Error", "ICS"

def get_google_oauth_status():
    """Get current status from Google Calendar OAuth"""
    
    try:
        from oauth_calendar_final import get_oauth_calendar_events
        
        print("📅 Checking Google Calendar (OAuth)...")
        current_events = get_oauth_calendar_events("current")
        
        if current_events and current_events != "Free" and current_events != "OAuth authentication failed":
            return "busy", current_events, "Google OAuth"
        else:
            return "free", "Free", "Google OAuth"
            
    except Exception as e:
        print(f"❌ Google OAuth error: {e}")
        return "error", "Google OAuth Error", "Google OAuth"

def get_google_service_status():
    """Get current status from Google Calendar Service Account"""
    
    try:
        from calendar_integration_service import get_current_meeting_service
        
        print("📅 Checking Google Calendar (Service Account)...")
        current_meeting = get_current_meeting_service()
        
        if current_meeting:
            return "busy", current_meeting, "Google Service"
        else:
            return "free", "Free", "Google Service"
            
    except Exception as e:
        print(f"❌ Google Service Account error: {e}")
        return "error", "Google Service Error", "Google Service"

def get_unified_calendar_status():
    """Get current status from all calendar sources"""
    
    print("🔍 Checking all calendar sources...")
    
    # Get status from all sources
    ics_status, ics_events, ics_source = get_ics_calendar_status()
    google_oauth_status, google_oauth_events, google_oauth_source = get_google_oauth_status()
    google_service_status, google_service_events, google_service_source = get_google_service_status()
    
    # Combine results
    all_statuses = [
        (ics_status, ics_events, ics_source),
        (google_oauth_status, google_oauth_events, google_oauth_source),
        (google_service_status, google_service_events, google_service_source)
    ]
    
    # Find any busy status
    busy_sources = []
    for status, events, source in all_statuses:
        if status == "busy":
            busy_sources.append((events, source))
    
    if busy_sources:
        # If any calendar shows busy, display the first one
        events, source = busy_sources[0]
        return "busy", f"{source}: {events}"
    
    # Check for errors
    error_sources = []
    for status, events, source in all_statuses:
        if status == "error":
            error_sources.append(source)
    
    if error_sources:
        return "error", f"Errors in: {', '.join(error_sources)}"
    
    # All sources show free
    return "free", "Free"

def display_status_on_device(status, events):
    """Display status on iDotMatrix device"""
    
    try:
        from config import DEVICE_ADDRESS
        
        if status == "free":
            # Green text for free
            display_text = "FREE"
            text_size = 8
            text_color = "0-255-0"  # Green
        elif status == "busy":
            # Red text for busy
            display_text = f"BUSY: {events[:30]}..." if len(events) > 30 else f"BUSY: {events}"
            text_size = 6
            text_color = "255-0-0"  # Red
        else:
            # Error status
            display_text = "ERROR"
            text_size = 8
            text_color = "255-255-0"  # Yellow
        
        # Use the run script to display text
        cmd = [
            "./run_in_venv.sh",
            "--address", DEVICE_ADDRESS,
            "--set-text", display_text,
            "--text-size", str(text_size),
            "--text-color", text_color
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Status displayed: {display_text}")
            return True
        else:
            print(f"❌ Failed to display: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error displaying on device: {e}")
        return False

def update_calendar_status():
    """Update calendar status on device using all sources"""
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n🕐 [{timestamp}] Updating calendar status from all sources...")
    
    # Get unified status from all calendars
    status, events = get_unified_calendar_status()
    
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
    """Run the unified calendar scheduler"""
    
    print("🕐 Unified Calendar Scheduler Started")
    print("=" * 50)
    print("📅 Updates every 30 minutes (at :00 and :30)")
    print("🔍 Sources: ICS + Google OAuth + Google Service Account")
    print("🟢 FREE = Available")
    print("🔴 BUSY = In meeting")
    print("⚠️ ERROR = Connection issue")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Schedule updates every 30 minutes starting at full hours
    schedule.every().hour.at(":00").do(update_calendar_status)  # Every hour at :00
    schedule.every().hour.at(":30").do(update_calendar_status)  # Every hour at :30
    
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
        print("🧪 Testing unified calendar status update...")
        update_calendar_status()
    else:
        run_scheduler()

if __name__ == "__main__":
    main()
