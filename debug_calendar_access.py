#!/usr/bin/env python3
"""
Debug script to show how imported calendars are detected
Shows the complete process of calendar discovery
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def debug_calendar_discovery():
    """Debug how the system discovers imported calendars"""
    
    print("🔍 Debug: How Imported Calendars are Detected")
    print("=" * 60)
    
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
        
        # Get calendar list - THIS IS THE KEY STEP
        print("3️⃣ Requesting calendar list from Google...")
        print("   API Call: service.calendarList().list().execute()")
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        print(f"✅ Found {len(calendars)} calendars from Google API")
        
        print()
        print("4️⃣ Analyzing each calendar:")
        print("=" * 40)
        
        own_calendars = []
        imported_calendars = []
        other_calendars = []
        
        for i, calendar in enumerate(calendars):
            calendar_id = calendar.get('id', '')
            summary = calendar.get('summary', 'No Title')
            access_role = calendar.get('accessRole', '')
            description = calendar.get('description', '')
            primary = calendar.get('primary', False)
            
            print(f"📅 Calendar {i+1}: {summary}")
            print(f"   ID: {calendar_id}")
            print(f"   Access Role: {access_role}")
            print(f"   Primary: {primary}")
            if description:
                print(f"   Description: {description}")
            
            # Categorize calendar
            if access_role == 'owner':
                own_calendars.append(calendar)
                print("   ✅ OWN CALENDAR (you own this)")
            elif access_role == 'writer':
                own_calendars.append(calendar)
                print("   ✅ OWN CALENDAR (you can write to this)")
            elif access_role == 'reader':
                imported_calendars.append(calendar)
                print("   📥 IMPORTED CALENDAR (you can only read this)")
            else:
                other_calendars.append(calendar)
                print(f"   ❓ OTHER ({access_role})")
            
            print()
        
        print("5️⃣ Summary:")
        print("=" * 20)
        print(f"📊 Total calendars: {len(calendars)}")
        print(f"✅ Own calendars: {len(own_calendars)}")
        print(f"📥 Imported calendars: {len(imported_calendars)}")
        print(f"❓ Other calendars: {len(other_calendars)}")
        print()
        
        if imported_calendars:
            print("📥 Imported calendars found:")
            for calendar in imported_calendars:
                summary = calendar.get('summary', 'No Title')
                calendar_id = calendar.get('id', '')
                print(f"   - {summary}")
                print(f"     ID: {calendar_id}")
            print()
            print("🎯 These imported calendars can be accessed if:")
            print("   1. The service account has permission to access them")
            print("   2. The calendar owner shared them with the service account")
            print("   3. Your Google account has the right permissions")
        else:
            print("📥 No imported calendars found")
            print("   This means either:")
            print("   - You don't have access to any imported calendars")
            print("   - The imported calendars aren't shared with the service account")
        
        print()
        print("🔧 How the system works:")
        print("   1. Google Calendar API returns ALL calendars you have access to")
        print("   2. The system checks the 'accessRole' field for each calendar")
        print("   3. 'owner'/'writer' = your own calendars")
        print("   4. 'reader' = imported calendars from others")
        print("   5. The system tries to access events from all calendars")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during calendar discovery: {e}")
        print()
        print("🔧 Troubleshooting:")
        print("   1. Make sure service-account.json exists")
        print("   2. Check that the service account has calendar permissions")
        print("   3. Verify that your calendars are shared with the service account")
        return False

def main():
    """Main function"""
    debug_calendar_discovery()

if __name__ == '__main__':
    main()
