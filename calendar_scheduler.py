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
    """Get current calendar status"""
    
    try:
        from config import DEVICE_ADDRESS
        from ics_calendar_simple import get_ics_events_for_current_simple
        from config import ICS_CALENDAR_URL
        
        # Get current events from ICS calendar
        current_events = get_ics_events_for_current_simple(ICS_CALENDAR_URL)
        
        if current_events and current_events != "Free":
            return "busy", current_events
        else:
            return "free", "Free"
            
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return "error", "Error"

def display_status_on_device(status, events):
    """Display status on iDotMatrix device with improved formatting"""
    
    try:
        from config import DEVICE_ADDRESS
        
        if status == "free":
            # Green text for free - compact format
            display_text = "🟢 FREE"
            text_size = 12
            text_color = "0-255-0"  # Bright Green
        elif status == "busy":
            # Red text for busy - show meeting details in compact format
            # Clean up the events text
            clean_events = events.replace("ICS:", "").replace("Google:", "").replace("Service:", "").strip()
            if "No events found" in clean_events:
                display_text = "🔴 BUSY"
            else:
                # More aggressive truncation but keep key info
                if len(clean_events) > 25:
                    # Try to keep the most important part (meeting name)
                    meeting_parts = clean_events.split(' @ ')
                    if len(meeting_parts) > 0:
                        meeting_name = meeting_parts[0][:20]  # First 20 chars of meeting name
                        display_text = f"🔴 {meeting_name}"
                    else:
                        display_text = f"🔴 {clean_events[:25]}"
                else:
                    display_text = f"🔴 {clean_events}"
            text_size = 10
            text_color = "255-0-0"  # Bright Red
        else:
            # Error status - compact
            display_text = "⚠️ ERROR"
            text_size = 12
            text_color = "255-165-0"  # Orange
        
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
