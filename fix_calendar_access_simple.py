#!/usr/bin/env python3
"""
Simple script to fix calendar access for service account
No external dependencies required
"""

import os
import json

def get_service_account_email():
    """Get the service account email from the JSON file"""
    
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        print("Please run: python calendar_service_account.py")
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
    print("   Then run: python setup_multi_calendar.py")
    print()
    print("🎯 Quick Links:")
    print("   - Google Calendar: https://calendar.google.com")
    print("   - Calendar Settings: https://calendar.google.com/calendar/r/settings")
    print()

if __name__ == '__main__':
    main()
