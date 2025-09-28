#!/usr/bin/env python3
"""
Simple Calendar Status Display

Uses simple text patterns instead of emoji for better iDotMatrix compatibility.
"""

import sys
import subprocess
from datetime import datetime

def get_meeting_status():
    """Get current meeting status"""
    
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

def format_simple_display(status, events):
    """Format display text for iDotMatrix"""
    
    if status == "free":
        return "FREE", 8, "0-255-0"  # Green text, larger size
        
    elif status == "busy":
        # Truncate meeting title
        meeting_title = events[:20] if len(events) > 20 else events
        return f"BUSY: {meeting_title}", 6, "255-0-0"  # Red text, smaller size
        
    else:
        return "ERROR", 8, "255-255-0"  # Yellow text

def display_simple_status():
    """Display simple status on iDotMatrix"""
    
    try:
        from config import DEVICE_ADDRESS
        
        # Get status
        status, events = get_meeting_status()
        
        # Format display
        display_text, text_size, text_color = format_simple_display(status, events)
        
        print(f"📊 Status: {status}")
        print(f"📝 Display: {display_text}")
        print(f"📏 Size: {text_size}, Color: {text_color}")
        
        # Build command
        cmd = [
            "./run_in_venv.sh",
            "--address", DEVICE_ADDRESS,
            "--set-text", display_text,
            "--text-size", str(text_size),
            "--text-color", text_color
        ]
        
        print(f"🚀 Command: {' '.join(cmd)}")
        
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

def show_status_info():
    """Show status information"""
    
    print("📊 Simple Calendar Status")
    print("=" * 40)
    
    status, events = get_meeting_status()
    
    print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📅 Status: {status.upper()}")
    print(f"📋 Events: {events}")
    
    if status == "free":
        print("🟢 You are FREE - Available for meetings")
        print("📝 Display: FREE (Green text)")
    elif status == "busy":
        print("🔴 You are BUSY - In a meeting")
        print(f"📝 Meeting: {events}")
        print("📝 Display: BUSY: [meeting title] (Red text)")
    else:
        print("⚠️ ERROR - Cannot determine status")
        print("📝 Display: ERROR (Yellow text)")
    
    return status, events

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python3 calendar_status_simple.py <command>")
        print("  Commands:")
        print("    status    - Show current status")
        print("    display   - Display status on device")
        print("    update    - Show status and display on device")
        return
    
    command = sys.argv[1]
    
    if command == "status":
        show_status_info()
        
    elif command == "display":
        display_simple_status()
        
    elif command == "update":
        print("🔄 Updating calendar status...")
        status, events = show_status_info()
        print()
        display_simple_status()
        
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
