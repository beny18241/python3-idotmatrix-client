#!/usr/bin/env python3
"""
Simple check for service account status
Diagnoses why service account can't access calendars
"""

import os
import json

def check_service_account_status():
    """Check service account status"""
    
    print("🔍 Service Account Status Check")
    print("=" * 40)
    
    # Check if service account file exists
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        print("🔧 SOLUTION: Run 'python calendar_service_account.py'")
        return False
    
    print("✅ Service account file exists")
    
    # Check service account email
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        client_email = service_account_data.get('client_email', '')
        if client_email:
            print(f"📧 Service account email: {client_email}")
        else:
            print("❌ No client_email found in service account file")
            return False
            
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")
        return False
    
    print()
    print("🔧 NEXT STEPS:")
    print("=" * 20)
    print("1. Go to Google Calendar: https://calendar.google.com")
    print("2. Click the gear icon (Settings) in the top right")
    print("3. Click 'Settings' from the dropdown")
    print("4. In the left sidebar, click 'Settings for my calendars'")
    print("5. Click on your main calendar name")
    print("6. Click 'Share with specific people'")
    print("7. Click 'Add people'")
    print(f"8. Add this email: {client_email}")
    print("9. Set permission to 'See all event details'")
    print("10. Click 'Send'")
    print()
    print("⏳ After sharing, wait 2-3 minutes, then run:")
    print("   python diagnose_calendar.py")
    print()
    print("🎯 QUICK LINKS:")
    print("• Google Calendar: https://calendar.google.com")
    print("• Calendar Settings: https://calendar.google.com/calendar/r/settings")
    
    return True

def main():
    """Main function"""
    check_service_account_status()

if __name__ == '__main__':
    main()
