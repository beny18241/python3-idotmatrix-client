#!/usr/bin/env python3
"""
Fix calendar access for service account
Ensures service account can access all your calendars
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def check_service_account_access():
    """Check what calendars the service account can access"""
    
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        print("Please run: python calendar_service_account.py")
        return False
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Try to get calendar list
        print("🔍 Checking service account access...")
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        if calendars:
            print(f"✅ Service account can access {len(calendars)} calendars:")
            for calendar in calendars:
                calendar_id = calendar.get('id', 'Unknown')
                summary = calendar.get('summary', 'No Title')
                access_role = calendar.get('accessRole', 'Unknown')
                print(f"  - {summary} ({access_role})")
                print(f"    ID: {calendar_id}")
            return True
        else:
            print("❌ Service account cannot access any calendars")
            return False
            
    except Exception as e:
        print(f"❌ Error checking service account access: {e}")
        return False

def get_service_account_email():
    """Get the service account email from the JSON file"""
    
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        return None
    
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        client_email = service_account_data.get('client_email', '')
        if client_email:
            print(f"📧 Service account email: {client_email}")
            return client_email
        else:
            print("❌ Could not find client_email in service account file")
            return None
            
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")
        return None

def main():
    """Main function to fix calendar access"""
    
    print("🔧 Fixing Calendar Access for Service Account")
    print("=" * 50)
    
    # Get service account email
    service_account_email = get_service_account_email()
    if not service_account_email:
        return
    
    print()
    print("📋 To fix calendar access, you need to:")
    print("=" * 50)
    print()
    print("1. Go to Google Calendar (https://calendar.google.com)")
    print("2. Click on the gear icon (Settings) in the top right")
    print("3. Click 'Settings' from the dropdown")
    print("4. In the left sidebar, click 'Settings for my calendars'")
    print("5. Click on your calendar name")
    print("6. Click 'Share with specific people'")
    print("7. Click 'Add people'")
    print(f"8. Add this email: {service_account_email}")
    print("9. Set permission to 'See all event details'")
    print("10. Click 'Send'")
    print()
    print("🔄 Repeat steps 5-10 for each calendar you want to access")
    print()
    print("📅 For your imported calendar:")
    print("   - Go to the imported calendar settings")
    print("   - Share it with the service account email")
    print("   - Set permission to 'See all event details'")
    print()
    print("⏳ After sharing, wait a few minutes for permissions to propagate")
    print("   Then run this script again to test access")
    print()
    
    # Check current access
    print("🔍 Current access status:")
    if check_service_account_access():
        print("✅ Service account has calendar access!")
    else:
        print("❌ Service account needs calendar access")
        print("   Follow the steps above to share your calendars")

if __name__ == '__main__':
    main()
