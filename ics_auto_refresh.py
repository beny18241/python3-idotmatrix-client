#!/usr/bin/env python3
"""
ICS Calendar Auto-Refresh
Automatically refreshes ICS calendar and displays events on iDotMatrix device
"""

import os
import sys
import time
import json
import datetime
import subprocess
from ics_calendar_simple import get_ics_events_for_tomorrow_simple, get_ics_events_for_current_simple, get_ics_events_for_today_simple

def get_ics_events_with_cache(meeting_type="tomorrow", cache_duration_minutes=30):
    """Get ICS events with caching to avoid too frequent requests"""
    
    cache_file = f"ics_cache_{meeting_type}.json"
    ics_url = "https://outlook.office365.com/owa/calendar/144d73fdf2654fb3b92983ee16e9d0b3@genpt.com/e829a99fc26b4c66a482420d04ea689513863417029725141930/calendar.ics"
    
    # Check if cache exists and is fresh
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is still fresh
            cache_time = datetime.datetime.fromisoformat(cache_data['timestamp'])
            now = datetime.datetime.now()
            
            if (now - cache_time).total_seconds() < cache_duration_minutes * 60:
                print(f"📋 Using cached {meeting_type} events (refreshed {cache_duration_minutes}min ago)")
                return cache_data['events']
        except:
            pass
    
    # Fetch fresh data
    print(f"🔄 Fetching fresh {meeting_type} events from ICS calendar...")
    
    try:
        if meeting_type == "tomorrow":
            events = get_ics_events_for_tomorrow_simple(ics_url)
        elif meeting_type == "current":
            events = get_ics_events_for_current_simple(ics_url)
        elif meeting_type == "today":
            events = get_ics_events_for_today_simple(ics_url)
        else:
            events = "Invalid meeting type"
        
        # Cache the result
        cache_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'events': events
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)
        
        print(f"✅ Fresh {meeting_type} events cached")
        return events
        
    except Exception as e:
        print(f"❌ Error fetching {meeting_type} events: {e}")
        return "Error fetching events"

def display_events_on_device(device_address, events):
    """Display events on iDotMatrix device"""
    
    if not events or events == "No events found" or events == "Error fetching events":
        print("❌ No events to display!")
        return False
    
    try:
        # Use the run script to display text
        cmd = [
            "./run_in_venv.sh",
            "--address", device_address,
            "--set-text", events
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Events displayed on device: {events}")
            return True
        else:
            print(f"❌ Failed to display on device: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error displaying on device: {e}")
        return False

def auto_refresh_ics_calendar(device_address, meeting_type="tomorrow", refresh_interval_minutes=30):
    """Automatically refresh ICS calendar and display events"""
    
    print(f"🔄 Auto-refreshing ICS calendar every {refresh_interval_minutes} minutes")
    print(f"📱 Displaying {meeting_type} events on device {device_address}")
    print("=" * 60)
    
    while True:
        try:
            print(f"\n🕐 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking for events...")
            
            # Get events with caching
            events = get_ics_events_with_cache(meeting_type, refresh_interval_minutes)
            
            # Display on device
            success = display_events_on_device(device_address, events)
            
            if success:
                print(f"✅ {meeting_type.title()} events displayed successfully!")
            else:
                print(f"❌ Failed to display {meeting_type} events")
            
            # Wait for next refresh
            print(f"⏰ Waiting {refresh_interval_minutes} minutes until next refresh...")
            time.sleep(refresh_interval_minutes * 60)
            
        except KeyboardInterrupt:
            print("\n🛑 Auto-refresh stopped by user")
            break
        except Exception as e:
            print(f"❌ Error in auto-refresh: {e}")
            print("⏰ Waiting 5 minutes before retry...")
            time.sleep(5 * 60)

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python ics_auto_refresh.py <device_address> [meeting_type] [refresh_interval_minutes]")
        print("  device_address: Bluetooth address of iDotMatrix device")
        print("  meeting_type: current, today, tomorrow (default: tomorrow)")
        print("  refresh_interval_minutes: How often to refresh (default: 30)")
        print()
        print("Examples:")
        print("  python ics_auto_refresh.py DD:4F:93:46:DF:1A tomorrow 30")
        print("  python ics_auto_refresh.py DD:4F:93:46:DF:1A current 15")
        print("  python ics_auto_refresh.py DD:4F:93:46:DF:1A today 60")
        print()
        print("Press Ctrl+C to stop auto-refresh")
        return
    
    device_address = sys.argv[1]
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "tomorrow"
    refresh_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    # Start auto-refresh
    auto_refresh_ics_calendar(device_address, meeting_type, refresh_interval)

if __name__ == '__main__':
    main()
