#!/usr/bin/env python3
"""
Debug Google Calendar OAuth integration
"""

import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def debug_google_calendar():
    """Debug Google Calendar OAuth integration"""
    
    print("🔍 Debugging Google Calendar OAuth integration...")
    
    # Check for OAuth files
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    
    if not os.path.exists(credentials_file):
        print("❌ credentials.json not found!")
        return
    
    if not os.path.exists(token_file):
        print("❌ token.json not found!")
        return
    
    print("✅ OAuth files found")
    
    try:
        # Load credentials
        creds = Credentials.from_authorized_user_file(token_file)
        
        # Create service
        service = build('calendar', 'v3', credentials=creds)
        
        # Get current time
        now = datetime.datetime.utcnow()
        now_iso = now.isoformat() + 'Z'
        
        print(f"🕐 Current time (UTC): {now_iso}")
        print(f"🕐 Current time (local): {datetime.datetime.now()}")
        
        # Check a wider time range
        time_range_start = (now - datetime.timedelta(hours=2)).isoformat() + 'Z'
        time_range_end = (now + datetime.timedelta(hours=2)).isoformat() + 'Z'
        
        print(f"📅 Checking events from: {time_range_start}")
        print(f"📅 Checking events until: {time_range_end}")
        
        # Get events
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
            print("💡 Make sure your meeting is:")
            print("   - In your primary calendar (beny18241@gmail.com)")
            print("   - Scheduled for the current time")
            print("   - Not an all-day event")
            return
        
        # Check each event
        for i, event in enumerate(events):
            summary = event.get('summary', 'No Title')
            start_time = event.get('start', {})
            end_time = event.get('end', {})
            location = event.get('location', '')
            
            print(f"\n📝 Event {i+1}: {summary}")
            print(f"   📅 Start: {start_time}")
            print(f"   📅 End: {end_time}")
            print(f"   📍 Location: {location}")
            
            # Check if event is happening now
            is_current = False
            if 'dateTime' in start_time and 'dateTime' in end_time:
                try:
                    start_dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                    end_dt = datetime.datetime.fromisoformat(end_time['dateTime'].replace('Z', '+00:00'))
                    now_utc = datetime.datetime.now(datetime.timezone.utc)
                    
                    print(f"   ⏰ Start (UTC): {start_dt}")
                    print(f"   ⏰ End (UTC): {end_dt}")
                    print(f"   ⏰ Now (UTC): {now_utc}")
                    
                    # Check if current time is between start and end
                    if start_dt <= now_utc <= end_dt:
                        is_current = True
                        print(f"   ✅ CURRENT MEETING DETECTED!")
                        return f"{summary}"
                    else:
                        print(f"   ❌ Not current (time mismatch)")
                        if start_dt > now_utc:
                            print(f"   ⏰ Meeting starts in: {start_dt - now_utc}")
                        else:
                            print(f"   ⏰ Meeting ended: {now_utc - end_dt}")
                except Exception as e:
                    print(f"   ❌ Error parsing times: {e}")
            else:
                print(f"   ❌ No dateTime in start/end (might be all-day event)")
        
        print(f"\n❌ No current meeting found - this is why it shows FREE")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_google_calendar()
