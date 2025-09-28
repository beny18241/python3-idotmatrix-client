#!/usr/bin/env python3
"""
Google Calendar authentication using Service Account
Bypasses OAuth issues completely
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def service_account_auth():
    """Authentication using service account"""
    
    print("🔐 Google Calendar authentication (Service Account)...")
    print("=" * 60)
    print("ℹ️  This bypasses OAuth completely using service account")
    print("ℹ️  Much more reliable for server environments")
    print()
    
    # Check if service account file exists
    service_account_file = 'service-account.json'
    
    if not os.path.exists(service_account_file):
        print("❌ Service account file not found!")
        print()
        print("📋 To create a service account:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("2. Go to 'APIs & Services' > 'Credentials'")
        print("3. Click 'Create Credentials' > 'Service account'")
        print("4. Name it 'iDotMatrix Service Account'")
        print("5. Click 'Create and Continue'")
        print("6. Skip roles for now, click 'Continue'")
        print("7. Click 'Done'")
        print("8. Click on the created service account")
        print("9. Go to 'Keys' tab")
        print("10. Click 'Add Key' > 'Create new key'")
        print("11. Choose 'JSON' and download")
        print("12. Save as 'service-account.json' in your project")
        print()
        print("📋 Then share your calendar with the service account:")
        print("1. Open Google Calendar")
        print("2. Go to calendar settings")
        print("3. Share with the service account email")
        print("4. Give 'Make changes to events' permission")
        print()
        return None
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        print("✅ Service account credentials loaded")
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Test access
        calendar_list = service.calendarList().list().execute()
        print(f"✅ Successfully connected to Google Calendar")
        print(f"📅 Found {len(calendar_list.get('items', []))} calendars")
        
        # Save credentials for later use
        token_file = 'token.json'
        with open(token_file, 'w') as token:
            token.write(json.dumps({
                'type': 'service_account',
                'file': service_account_file
            }))
        
        print(f"💾 Service account info saved to {token_file}")
        
        return service
        
    except Exception as e:
        print(f"❌ Service account authentication failed: {e}")
        print()
        print("🔧 Troubleshooting tips:")
        print("1. Make sure the service account file is correct")
        print("2. Check that the service account has calendar access")
        print("3. Verify the calendar is shared with the service account")
        print("4. Try creating a new service account")
        return None

def get_current_meeting(service):
    """Get current meeting using service account"""
    try:
        from datetime import datetime
        
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Get events happening now
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=now,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return None
        
        event = events[0]
        return {
            'summary': event.get('summary', 'No Title'),
            'start': event.get('start', {}),
            'end': event.get('end', {}),
            'description': event.get('description', ''),
            'location': event.get('location', '')
        }
        
    except Exception as e:
        print(f"❌ Failed to get current meeting: {e}")
        return None

def test_calendar_access(service):
    """Test if we can access the calendar"""
    if not service:
        print("❌ No service available")
        return False
    
    try:
        # Try to get calendar list
        calendar_list = service.calendarList().list().execute()
        print(f"✅ Successfully connected to Google Calendar")
        print(f"📅 Found {len(calendar_list.get('items', []))} calendars")
        
        # Test getting current meeting
        current_meeting = get_current_meeting(service)
        if current_meeting:
            print(f"📅 Current meeting: {current_meeting['summary']}")
        else:
            print("📅 No current meeting")
        
        return True
        
    except Exception as e:
        print(f"❌ Calendar access test failed: {e}")
        return False

def main():
    """Main authentication function"""
    print("🔧 Google Calendar Authentication (Service Account)")
    print("=" * 60)
    
    # Authenticate
    service = service_account_auth()
    
    if service:
        # Test access
        if test_calendar_access(service):
            print()
            print("🎉 Setup complete! You can now use calendar commands:")
            print("  source venv/bin/activate")
            print("  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-current")
        else:
            print("❌ Calendar access test failed")
    else:
        print("❌ Authentication failed")

if __name__ == '__main__':
    main()
