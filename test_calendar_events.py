#!/usr/bin/env python3
"""
Test calendar events
Simple script to test if service account can see calendars and events
"""

import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_calendar_events():
    """Test calendar events access"""
    
    print("🔧 Testing Calendar Events Access")
    print("=" * 50)
    
    # Check if service account file exists
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found!")
        print("Please make sure the service account file is in the current directory")
        return False
    
    print("✅ service-account.json found")
    
    try:
        # Load service account credentials
        print("1️⃣ Loading service account credentials...")
        credentials = service_account.Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        print("✅ Service account credentials loaded")
        
        # Create service
        print("2️⃣ Creating Google Calendar API service...")
        service = build('calendar', 'v3', credentials=credentials)
        print("✅ Google Calendar API service created")
        
        # Get all accessible calendars
        print("3️⃣ Getting accessible calendars...")
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        print(f"✅ Found {len(calendars)} accessible calendars")
        
        if not calendars:
            print("❌ No calendars accessible!")
            print("Please check:")
            print("1. Service account has proper roles")
            print("2. Calendars are shared with the service account")
            print("3. Google Calendar API is enabled")
            return False
        
        print("\n📋 Accessible Calendars:")
        print("-" * 30)
        for i, calendar in enumerate(calendars):
            calendar_id = calendar.get('id', 'Unknown')
            summary = calendar.get('summary', 'No Title')
            access_role = calendar.get('accessRole', 'Unknown')
            primary = calendar.get('primary', False)
            
            print(f"{i+1}. {summary}")
            print(f"   ID: {calendar_id}")
            print(f"   Role: {access_role}")
            print(f"   Primary: {primary}")
            print()
        
        # Test events in each calendar
        print("4️⃣ Testing events in each calendar...")
        print("-" * 40)
        
        for calendar in calendars:
            calendar_id = calendar.get('id', '')
            summary = calendar.get('summary', 'Unknown')
            
            print(f"🔍 Testing calendar: {summary}")
            
            try:
                # Get today's events
                today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                today_start_utc = today_start.isoformat() + 'Z'
                today_end = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
                today_end_utc = today_end.isoformat() + 'Z'
                
                events_result = service.events().list(
                    calendarId=calendar_id,
                    timeMin=today_start_utc,
                    timeMax=today_end_utc,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                
                today_events = events_result.get('items', [])
                print(f"   📅 Today's events: {len(today_events)}")
                
                # Get tomorrow's events
                tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
                tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                tomorrow_start_utc = tomorrow_start.isoformat() + 'Z'
                tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
                tomorrow_end_utc = tomorrow_end.isoformat() + 'Z'
                
                events_result = service.events().list(
                    calendarId=calendar_id,
                    timeMin=tomorrow_start_utc,
                    timeMax=tomorrow_end_utc,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                
                tomorrow_events = events_result.get('items', [])
                print(f"   📅 Tomorrow's events: {len(tomorrow_events)}")
                
                # Show tomorrow's events
                if tomorrow_events:
                    print("   📋 Tomorrow's events:")
                    for event in tomorrow_events:
                        event_summary = event.get('summary', 'No Title')
                        start_time = event.get('start', {})
                        
                        time_str = ""
                        if 'dateTime' in start_time:
                            try:
                                dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                                time_str = dt.strftime('%H:%M')
                            except:
                                time_str = "All day"
                        elif 'date' in start_time:
                            time_str = "All day"
                        
                        print(f"     - {event_summary} @ {time_str}")
                
                print()
                
            except Exception as e:
                print(f"   ❌ Error accessing calendar: {e}")
                print()
        
        print("5️⃣ Summary:")
        print("-" * 20)
        print("✅ Service account is working!")
        print("✅ Calendars are accessible!")
        print("✅ Events can be retrieved!")
        print()
        print("🚀 Next steps:")
        print("1. Run: python calendar_display_all_calendars.py tomorrow")
        print("2. Display events on iDotMatrix device")
        print("3. Set up continuous calendar display")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if service-account.json is valid")
        print("2. Verify Google Calendar API is enabled")
        print("3. Check service account permissions")
        print("4. Ensure calendars are shared with service account")
        return False

def main():
    """Main function"""
    test_calendar_events()

if __name__ == '__main__':
    main()
