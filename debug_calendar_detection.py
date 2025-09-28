#!/usr/bin/env python3
"""
Debug script to test calendar meeting detection
"""

import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_calendar_detection():
    """Test if meetings are being detected correctly"""
    
    print("🔍 Testing calendar meeting detection...")
    
    # Check for service account file
    service_account_file = 'service-account.json'
    if not os.path.exists(service_account_file):
        print("❌ Service account file not found!")
        print("Please run: python calendar_service_account.py")
        return
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Get current time
        now = datetime.datetime.utcnow()
        now_iso = now.isoformat() + 'Z'
        
        print(f"🕐 Current time (UTC): {now_iso}")
        print(f"🕐 Current time (local): {datetime.datetime.now()}")
        
        # Check a wider time range to catch ongoing events
        time_range_start = (now - datetime.timedelta(hours=2)).isoformat() + 'Z'
        time_range_end = (now + datetime.timedelta(hours=2)).isoformat() + 'Z'
        
        print(f"📅 Checking events from: {time_range_start}")
        print(f"📅 Checking events until: {time_range_end}")
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_range_start,
            timeMax=time_range_end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        print(f"\n📋 Found {len(events)} events in time range:")
        
        if not events:
            print("❌ No events found - this is why it shows FREE")
            return
        
        # Check each event
        for i, event in enumerate(events):
            summary = event.get('summary', 'No Title')
            start_time = event.get('start', {})
            end_time = event.get('end', {})
            location = event.get('location', '')
            
            print(f"\n📝 Event {i+1}: {summary}")
            
            # Check if event is happening now
            is_current = False
            if 'dateTime' in start_time and 'dateTime' in end_time:
                try:
                    start_dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                    end_dt = datetime.datetime.fromisoformat(end_time['dateTime'].replace('Z', '+00:00'))
                    now_utc = datetime.datetime.now(datetime.timezone.utc)
                    
                    print(f"   ⏰ Start: {start_dt}")
                    print(f"   ⏰ End: {end_dt}")
                    print(f"   ⏰ Now: {now_utc}")
                    
                    # Check if current time is between start and end
                    if start_dt <= now_utc <= end_dt:
                        is_current = True
                        print(f"   ✅ CURRENT MEETING DETECTED!")
                        print(f"   📍 Location: {location}")
                        return f"{summary}"
                    else:
                        print(f"   ❌ Not current (time mismatch)")
                except Exception as e:
                    print(f"   ❌ Error parsing times: {e}")
            else:
                print(f"   ❌ No dateTime in start/end")
        
        print(f"\n❌ No current meeting found - this is why it shows FREE")
        print(f"💡 Make sure your meeting is:")
        print(f"   - Scheduled for the current time")
        print(f"   - Not an all-day event")
        print(f"   - In your primary calendar")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_calendar_detection()
