#!/usr/bin/env python3
"""
Calendar Status Display

Enhanced display with icons and status indicators for iDotMatrix.
"""

import sys
import subprocess
from datetime import datetime

def get_meeting_status():
    """Get current meeting status with enhanced formatting"""
    
    try:
        from config import ICS_CALENDAR_URL, DEVICE_ADDRESS
        from ics_calendar_simple import get_ics_events_for_current_simple
        
        # Get current events
        current_events = get_ics_events_for_current_simple(ICS_CALENDAR_URL)
        
        if current_events and current_events != "Free":
            return "busy", current_events
        else:
            return "free", "Free"
            
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return "error", "Error"

def format_meeting_text(events, max_length=25):
    """Format meeting text for display"""
    
    if len(events) > max_length:
        # Truncate and add ellipsis
        return events[:max_length-3] + "..."
    return events

def display_status_with_icons(status, events):
    """Display status with appropriate icons and formatting"""
    
    try:
        from config import DEVICE_ADDRESS
        
        if status == "free":
            # Green circle for free
            display_text = "🟢 FREE"
            text_size = 8
            text_color = "0-255-0"  # Green
            text_speed = 30  # Slower for free status
            
        elif status == "busy":
            # Red circle with meeting title
            meeting_title = format_meeting_text(events)
            display_text = f"🔴 {meeting_title}"
            text_size = 6  # Smaller for meeting titles
            text_color = "255-0-0"  # Red
            text_speed = 20  # Faster for meeting info
            
        else:
            # Yellow warning for error
            display_text = "⚠️ ERROR"
            text_size = 8
            text_color = "255-255-0"  # Yellow
            text_speed = 30
        
        # Build command
        cmd = [
            "./run_in_venv.sh",
            "--address", DEVICE_ADDRESS,
            "--set-text", display_text,
            "--text-size", str(text_size),
            "--text-color", text_color,
            "--text-speed", str(text_speed)
        ]
        
        print(f"🚀 Displaying: {display_text}")
        print(f"📏 Size: {text_size}, Color: {text_color}, Speed: {text_speed}")
        
        # Execute command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Status displayed successfully")
            return True
        else:
            print(f"❌ Failed to display: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error displaying status: {e}")
        return False

def show_status_summary():
    """Show current status summary"""
    
    print("📊 Calendar Status Summary")
    print("=" * 40)
    
    status, events = get_meeting_status()
    
    print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📅 Status: {status.upper()}")
    print(f"📋 Events: {events}")
    
    if status == "free":
        print("🟢 You are FREE - Available for meetings")
    elif status == "busy":
        print("🔴 You are BUSY - In a meeting")
        print(f"📝 Meeting: {events}")
    else:
        print("⚠️ ERROR - Cannot determine status")
    
    return status, events

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python3 calendar_status_display.py <command>")
        print("  Commands:")
        print("    status    - Show current status")
        print("    display   - Display status on device")
        print("    update    - Show status and display on device")
        return
    
    command = sys.argv[1]
    
    if command == "status":
        show_status_summary()
        
    elif command == "display":
        status, events = get_meeting_status()
        display_status_with_icons(status, events)
        
    elif command == "update":
        print("🔄 Updating calendar status...")
        status, events = show_status_summary()
        print()
        display_status_with_icons(status, events)
        
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
