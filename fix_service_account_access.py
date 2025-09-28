#!/usr/bin/env python3
"""
Fix service account access to calendars
Step-by-step guide to share calendars with service account
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
    """Main function to fix service account access"""
    
    print("🔧 Fix Service Account Calendar Access")
    print("=" * 50)
    
    # Get service account email
    service_account_email = get_service_account_email()
    if not service_account_email:
        return
    
    print()
    print("📋 STEP-BY-STEP SOLUTION:")
    print("=" * 30)
    print()
    print("🔍 The issue: Service account can't access your calendars")
    print("💡 The solution: Share your calendars with the service account")
    print()
    print("📝 STEP 1: Share Your Primary Calendar")
    print("-" * 40)
    print("1. Go to Google Calendar: https://calendar.google.com")
    print("2. Click the gear icon (Settings) in the top right")
    print("3. Click 'Settings' from the dropdown")
    print("4. In the left sidebar, click 'Settings for my calendars'")
    print("5. Click on your main calendar name")
    print("6. Click 'Share with specific people'")
    print("7. Click 'Add people'")
    print(f"8. Add this email: {service_account_email}")
    print("9. Set permission to 'See all event details'")
    print("10. Click 'Send'")
    print()
    print("📝 STEP 2: Share Your Imported Calendar")
    print("-" * 40)
    print("1. In Google Calendar, find your imported calendar in the left sidebar")
    print("2. Click the three dots next to the calendar name")
    print("3. Click 'Settings and sharing'")
    print("4. Click 'Share with specific people'")
    print("5. Click 'Add people'")
    print(f"6. Add this email: {service_account_email}")
    print("7. Set permission to 'See all event details'")
    print("8. Click 'Send'")
    print()
    print("📝 STEP 3: Test Access")
    print("-" * 40)
    print("After sharing both calendars:")
    print("1. Wait 2-3 minutes for permissions to propagate")
    print("2. Run: python diagnose_calendar.py")
    print("3. You should see: 'Found X accessible calendars'")
    print("4. Then run: python calendar_display_all_calendars.py tomorrow")
    print()
    print("🎯 QUICK LINKS:")
    print("-" * 20)
    print("• Google Calendar: https://calendar.google.com")
    print("• Calendar Settings: https://calendar.google.com/calendar/r/settings")
    print()
    print("⚠️  IMPORTANT NOTES:")
    print("-" * 20)
    print("• You need to share EACH calendar individually")
    print("• The service account is like a separate Google account")
    print("• It needs explicit permission to access your calendars")
    print("• This is different from your personal Google account access")
    print()
    print("✅ After completing these steps, your service account will have")
    print("   access to both your primary calendar and imported calendar!")

if __name__ == '__main__':
    main()
