#!/usr/bin/env python3
"""
Automated calendar display for iDotMatrix
Continuously shows current meeting status on the display
"""

import time
import subprocess
import sys
from calendar_integration import GoogleCalendarIntegration

def display_calendar_info(device_address, calendar):
    """Display current calendar information on iDotMatrix"""
    
    # Get current meeting
    current_meeting = calendar.get_current_meeting()
    
    if current_meeting:
        # Show current meeting
        display_text = calendar.format_meeting_for_display(current_meeting)
        print(f"Current meeting: {display_text}")
        
        # Display on iDotMatrix
        cmd = [
            "python", "app.py", 
            "--address", device_address,
            "--set-text", display_text
        ]
        subprocess.run(cmd)
        
    else:
        # No current meeting - show next meeting or "Free"
        next_meeting = calendar.get_next_meeting()
        
        if next_meeting:
            display_text = f"Next: {calendar.get_meeting_status_text(next_meeting)}"
        else:
            display_text = "Free"
            
        print(f"Status: {display_text}")
        
        # Display on iDotMatrix
        cmd = [
            "python", "app.py",
            "--address", device_address, 
            "--set-text", display_text
        ]
        subprocess.run(cmd)

def main():
    """Main calendar display loop"""
    
    if len(sys.argv) != 2:
        print("Usage: python calendar_display.py <device_address>")
        print("Example: python calendar_display.py 00:11:22:33:44:ff")
        sys.exit(1)
    
    device_address = sys.argv[1]
    
    try:
        # Initialize calendar integration
        calendar = GoogleCalendarIntegration()
        print(f"Calendar integration initialized. Displaying on device: {device_address}")
        
        # Continuous loop
        while True:
            try:
                display_calendar_info(device_address, calendar)
                time.sleep(30)  # Update every 30 seconds
                
            except KeyboardInterrupt:
                print("\nStopping calendar display...")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)  # Wait before retrying
                
    except Exception as e:
        print(f"Failed to initialize calendar: {e}")
        print("Make sure you have credentials.json and have run the setup")

if __name__ == "__main__":
    main()
