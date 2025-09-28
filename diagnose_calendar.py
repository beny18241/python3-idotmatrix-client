#!/usr/bin/env python3
"""
Diagnostic script to check calendar access and events
Shows what calendars are accessible and what events are found
"""

import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def diagnose_calendar_access():
    """Diagnose calendar access and events"""
    
    print("🔍 Calendar Diagnostic Tool")
    print("=" * 50)
    
    # Check if service account exists
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        print("Please run: python calendar_service_account.py")
        return False
    
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
        print("3️⃣ Getting all accessible calendars...")
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        print(f"✅ Found {len(calendars)} accessible calendars")
        
        if not calendars:
            print("❌ No calendars accessible!")
            print("Please share your calendars with the service account")
            return False
        
        print()
        print("4️⃣ Calendar Analysis:")
        print("=" * 30)
        
        accessible_calendars = []
        
        for i, calendar in enumerate(calendars):
            calendar_id = calendar.get('id', '')
            summary = calendar.get('summary', 'No Title')
            access_role = calendar.get('accessRole', '')
            primary = calendar.get('primary', False)
            
            print(f"📅 Calendar {i+1}: {summary}")
            print(f"   ID: {calendar_id}")
            print(f"   Access Role: {access_role}")
            print(f"   Primary: {primary}")
            
            if access_role in ['owner', 'writer', 'reader']:
                accessible_calendars.append(calendar)
                print("   ✅ ACCESSIBLE")
            else:
                print("   ❌ NOT ACCESSIBLE")
            
            print()
        
        print("5️⃣ Checking Events in Each Calendar:")
        print("=" * 40)
        
        # Check today's events
        today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_start_utc = today_start.isoformat() + 'Z'
        today_end = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        today_end_utc = today_end.isoformat() + 'Z'
        
        # Check tomorrow's events
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start_utc = tomorrow_start.isoformat() + 'Z'
        tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
        tomorrow_end_utc = tomorrow_end.isoformat() + 'Z'
        
        for calendar in accessible_calendars:
            calendar_id = calendar.get('id', '')
            summary = calendar.get('summary', 'Unknown')
            
            print(f"🔍 Checking calendar: {summary}")
            
            try:
                # Check today's events
                today_events = service.events().list(
                    calendarId=calendar_id,
                    timeMin=today_start_utc,
                    timeMax=today_end_utc,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                
                today_count = len(today_events.get('items', []))
                print(f"   📅 Today's events: {today_count}")
                
                # Check tomorrow's events
                tomorrow_events = service.events().list(
                    calendarId=calendar_id,
                    timeMin=tomorrow_start_utc,
                    timeMax=tomorrow_end_utc,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                
                tomorrow_count = len(tomorrow_events.get('items', []))
                print(f"   📅 Tomorrow's events: {tomorrow_count}")
                
                # Show tomorrow's events if any
                if tomorrow_count > 0:
                    print(f"   📋 Tomorrow's events in {summary}:")
                    for event in tomorrow_events.get('items', []):
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
                
            except Exception as e:
                print(f"   ❌ Error accessing calendar: {e}")
            
            print()
        
        print("6️⃣ Summary:")
        print("=" * 20)
        print(f"📊 Total accessible calendars: {len(accessible_calendars)}")
        print("🔧 The script should check ALL accessible calendars, not just primary")
        print("💡 If you see events in other calendars, the script needs to be updated")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during diagnosis: {e}")
        return False

def main():
    """Main function"""
    diagnose_calendar_access()

if __name__ == '__main__':
    main()
