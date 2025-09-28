#!/usr/bin/env python3
"""
Fix Calendar Sharing
Step-by-step solution to share calendars with service account
"""

import os
import json

def get_service_account_email():
    """Get service account email from JSON file"""
    
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found!")
        return None
    
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        email = service_account_data.get('client_email', '')
        print(f"✅ Service account email: {email}")
        return email
        
    except Exception as e:
        print(f"❌ Error reading service-account.json: {e}")
        return None

def provide_sharing_instructions(service_account_email):
    """Provide step-by-step instructions to share calendars"""
    
    print("\n🔧 Calendar Sharing Fix Instructions")
    print("=" * 50)
    
    print("📋 The issue is that your calendars need to be shared with the service account.")
    print("Even though the service account has proper roles, it can't see calendars")
    print("unless they are explicitly shared with it.")
    print()
    
    print("1️⃣ Share Your Primary Calendar:")
    print("   • Go to: https://calendar.google.com")
    print("   • Click on your main calendar (usually your name)")
    print("   • Click the three dots (⋮) next to your calendar name")
    print("   • Click 'Settings and sharing'")
    print("   • Scroll down to 'Share with specific people'")
    print("   • Click 'Add people'")
    print(f"   • Add this email: {service_account_email}")
    print("   • Set permission to 'See all event details'")
    print("   • Click 'Send'")
    print()
    
    print("2️⃣ Share Any Other Calendars:")
    print("   • Repeat the same process for any other calendars you want to access")
    print("   • This includes imported calendars, shared calendars, etc.")
    print()
    
    print("3️⃣ Check Calendar Sharing Status:")
    print("   • Go to: https://calendar.google.com")
    print("   • Click on each calendar")
    print("   • Look for the service account email in the sharing list")
    print("   • Make sure it has 'See all event details' permission")
    print()
    
    print("4️⃣ Test After Sharing:")
    print("   • Run: python test_calendar_events.py")
    print("   • You should now see your calendars!")
    print()
    
    print("💡 Important Notes:")
    print("   • The service account needs to be added to EACH calendar individually")
    print("   • Just having the right IAM roles is not enough")
    print("   • Each calendar must be shared with the service account email")
    print("   • This is a Google Calendar limitation, not a service account issue")

def check_api_enablement():
    """Check if Google Calendar API is enabled"""
    
    print("\n🔧 Google Calendar API Check")
    print("=" * 30)
    
    print("📋 Make sure Google Calendar API is enabled:")
    print("   • Go to: https://console.cloud.google.com/apis/library")
    print("   • Search for 'Google Calendar API'")
    print("   • Make sure it shows 'Enabled'")
    print("   • If not enabled, click 'Enable'")
    print()
    
    print("📋 Alternative API check:")
    print("   • Go to: https://console.cloud.google.com/apis/dashboard")
    print("   • Look for 'Google Calendar API' in the list")
    print("   • Make sure it's enabled")

def main():
    """Main function"""
    
    print("🔧 Calendar Sharing Diagnostic")
    print("=" * 40)
    
    # Get service account email
    service_account_email = get_service_account_email()
    
    if not service_account_email:
        print("❌ Cannot get service account email")
        return
    
    # Check API enablement
    check_api_enablement()
    
    # Provide sharing instructions
    provide_sharing_instructions(service_account_email)
    
    print("\n🎯 Next Steps:")
    print("1. Share your calendars with the service account email")
    print("2. Run: python test_calendar_events.py")
    print("3. If it works, run: python combined_calendar_fixed.py DD:4F:93:46:DF:1A tomorrow")

if __name__ == '__main__':
    main()
