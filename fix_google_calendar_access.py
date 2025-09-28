#!/usr/bin/env python3
"""
Fix Google Calendar Access
Comprehensive solution to fix Google Calendar service account access
"""

import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def check_service_account_file():
    """Check if service account file exists and is valid"""
    
    print("1️⃣ Checking service account file...")
    
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found!")
        print("Please download the service account JSON file from Google Cloud Console")
        return False
    
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in service_account_data]
        
        if missing_fields:
            print(f"❌ Missing fields in service-account.json: {missing_fields}")
            return False
        
        print(f"✅ service-account.json found and valid")
        print(f"   📧 Service account email: {service_account_data.get('client_email', 'Unknown')}")
        print(f"   🏢 Project ID: {service_account_data.get('project_id', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Error reading service-account.json: {e}")
        return False

def test_google_calendar_api():
    """Test Google Calendar API access"""
    
    print("\n2️⃣ Testing Google Calendar API access...")
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Test API access
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        print(f"✅ Google Calendar API access successful")
        print(f"📅 Found {len(calendars)} accessible calendars")
        
        if calendars:
            print("\n📋 Accessible Calendars:")
            for i, calendar in enumerate(calendars):
                calendar_id = calendar.get('id', 'Unknown')
                summary = calendar.get('summary', 'No Title')
                access_role = calendar.get('accessRole', 'Unknown')
                primary = calendar.get('primary', False)
                
                print(f"   {i+1}. {summary}")
                print(f"      ID: {calendar_id}")
                print(f"      Role: {access_role}")
                print(f"      Primary: {primary}")
                print()
        
        return True, calendars
        
    except Exception as e:
        print(f"❌ Google Calendar API error: {e}")
        return False, []

def test_calendar_events(calendars):
    """Test if we can fetch events from calendars"""
    
    print("\n3️⃣ Testing calendar events access...")
    
    if not calendars:
        print("❌ No calendars to test")
        return False
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Test events in each calendar
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing calendar events: {e}")
        return False

def provide_fix_instructions():
    """Provide instructions to fix Google Calendar access"""
    
    print("\n🔧 Google Calendar Access Fix Instructions")
    print("=" * 50)
    
    print("📋 If you're getting 0 calendars, try these steps:")
    print()
    
    print("1️⃣ Check Service Account Roles:")
    print("   • Go to: https://console.cloud.google.com/iam-admin/iam")
    print("   • Find your service account")
    print("   • Add these roles:")
    print("     - Basic > Viewer")
    print("     - Service Account > Service Account User")
    print("     - Project > Editor (if available)")
    print()
    
    print("2️⃣ Enable Google Calendar API:")
    print("   • Go to: https://console.cloud.google.com/apis/library")
    print("   • Search for 'Google Calendar API'")
    print("   • Click 'Enable'")
    print()
    
    print("3️⃣ Share Calendars with Service Account:")
    print("   • Go to: https://calendar.google.com")
    print("   • Click on your calendar settings")
    print("   • Click 'Share with specific people'")
    print("   • Add your service account email")
    print("   • Give 'See all event details' permission")
    print()
    
    print("4️⃣ Check Service Account Email:")
    print("   • Your service account email should be:")
    print("     idotmatrix-service-account@n8nwork-450415.iam.gserviceaccount.com")
    print("   • Make sure this email is shared with your calendars")
    print()
    
    print("5️⃣ Test Again:")
    print("   • Run: python fix_google_calendar_access.py")
    print("   • Or run: python test_calendar_events.py")

def main():
    """Main function"""
    
    print("🔧 Google Calendar Access Diagnostic")
    print("=" * 50)
    
    # Check service account file
    if not check_service_account_file():
        print("\n❌ Service account file issue - please fix first")
        return
    
    # Test Google Calendar API
    api_success, calendars = test_google_calendar_api()
    
    if not api_success:
        print("\n❌ Google Calendar API access failed")
        provide_fix_instructions()
        return
    
    if not calendars:
        print("\n❌ No calendars accessible")
        provide_fix_instructions()
        return
    
    # Test calendar events
    events_success = test_calendar_events(calendars)
    
    if events_success:
        print("\n✅ Google Calendar access is working!")
        print("🚀 You can now use both Google Calendar and ICS calendar")
        print("   python combined_calendar_simple.py DD:4F:93:46:DF:1A tomorrow")
    else:
        print("\n❌ Calendar events access failed")
        provide_fix_instructions()

if __name__ == '__main__':
    main()
