#!/usr/bin/env python3
"""
Get service account email for calendar sharing
Shows the email address you need to share your calendar with
"""

import os
import json

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
    """Main function"""
    
    print("🔧 Get Service Account Email for Calendar Sharing")
    print("=" * 60)
    
    # Get service account email
    service_account_email = get_service_account_email()
    if not service_account_email:
        return
    
    print()
    print("📋 NOW SHARE YOUR CALENDAR WITH THE SERVICE ACCOUNT:")
    print("=" * 60)
    print()
    print("🔧 STEP 1: Go to Google Calendar")
    print("1. Open: https://calendar.google.com")
    print("2. Click the gear icon (Settings) in the top right")
    print("3. Click 'Settings' from the dropdown")
    print()
    print("🔧 STEP 2: Share Your Main Calendar")
    print("1. In the left sidebar, click 'Settings for my calendars'")
    print("2. Click on your main calendar name")
    print("3. Click 'Share with specific people'")
    print("4. Click 'Add people'")
    print(f"5. Add this email: {service_account_email}")
    print("6. Set permission to 'See all event details'")
    print("7. Click 'Send'")
    print()
    print("🔧 STEP 3: Test Access")
    print("1. Wait 2-3 minutes for permissions to propagate")
    print("2. Run: python diagnose_calendar.py")
    print("3. You should see: 'Found X accessible calendars'")
    print("4. Then run: python calendar_display_all_calendars.py tomorrow")
    print()
    print("🎯 QUICK LINKS:")
    print("• Google Calendar: https://calendar.google.com")
    print("• Calendar Settings: https://calendar.google.com/calendar/r/settings")
    print()
    print("⚠️  IMPORTANT:")
    print("• The service account is like a separate Google account")
    print("• It needs explicit permission to access your calendars")
    print("• You need to share your calendar with the service account email")
    print()
    print("✅ After sharing:")
    print("   - Service account will access your calendar")
    print("   - Tomorrow's events will be found")
    print("   - iDotMatrix will display events")

if __name__ == '__main__':
    main()
