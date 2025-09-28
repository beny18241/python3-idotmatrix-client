#!/usr/bin/env python3
"""
Setup script for dual calendar integration (ICS + Google Calendar)
"""

import os
import json

def setup_dual_calendar():
    """Setup both ICS and Google Calendar integration"""
    
    print("🔧 Setting up dual calendar integration...")
    print("=" * 60)
    
    # Check current config
    print("📋 Current configuration:")
    
    # Check ICS Calendar URL
    try:
        from config import ICS_CALENDAR_URL
        if ICS_CALENDAR_URL == "provide your ICS calendar URL here":
            print("❌ ICS Calendar URL: Not configured")
            ics_configured = False
        else:
            print(f"✅ ICS Calendar URL: {ICS_CALENDAR_URL}")
            ics_configured = True
    except:
        print("❌ ICS Calendar URL: Not configured")
        ics_configured = False
    
    # Check Google Calendar OAuth
    oauth_configured = False
    if os.path.exists('credentials.json') and os.path.exists('token.json'):
        print("✅ Google Calendar OAuth: Configured")
        oauth_configured = True
    else:
        print("❌ Google Calendar OAuth: Not configured")
    
    print("\n🎯 Calendar Integration Status:")
    if ics_configured and oauth_configured:
        print("✅ Both ICS and Google Calendar are configured!")
        print("💡 Your system will check both calendars and show BUSY if either has a meeting")
    elif ics_configured:
        print("✅ ICS Calendar configured")
        print("⚠️  Google Calendar OAuth not configured")
        print("💡 Only ICS calendar will be checked")
    elif oauth_configured:
        print("✅ Google Calendar OAuth configured")
        print("⚠️  ICS Calendar not configured")
        print("💡 Only Google Calendar will be checked")
    else:
        print("❌ No calendars configured!")
        print("💡 You need to configure at least one calendar source")
    
    print("\n🔧 Configuration Options:")
    print("1. Configure ICS Calendar URL")
    print("2. Configure Google Calendar OAuth")
    print("3. Test current configuration")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        setup_ics_calendar()
    elif choice == "2":
        setup_google_oauth()
    elif choice == "3":
        test_calendar_integration()
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

def setup_ics_calendar():
    """Setup ICS calendar URL"""
    
    print("\n📅 Setting up ICS Calendar...")
    print("=" * 40)
    
    print("ICS Calendar URLs are typically:")
    print("• Outlook/Exchange: https://outlook.office365.com/owa/calendar/...")
    print("• Google Calendar: https://calendar.google.com/calendar/ical/...")
    print("• Apple Calendar: https://p123-caldav.icloud.com/...")
    print("• Other: Check your calendar provider's documentation")
    
    ics_url = input("\nEnter your ICS calendar URL: ").strip()
    
    if not ics_url:
        print("❌ No URL provided")
        return
    
    # Update config.py
    try:
        # Read current config
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Replace the placeholder
        new_content = content.replace(
            'ICS_CALENDAR_URL = "provide your ICS calendar URL here"',
            f'ICS_CALENDAR_URL = "{ics_url}"'
        )
        
        # Write back
        with open('config.py', 'w') as f:
            f.write(new_content)
        
        print(f"✅ ICS Calendar URL updated: {ics_url}")
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")

def setup_google_oauth():
    """Setup Google Calendar OAuth"""
    
    print("\n📅 Setting up Google Calendar OAuth...")
    print("=" * 40)
    
    if os.path.exists('credentials.json') and os.path.exists('token.json'):
        print("✅ Google Calendar OAuth is already configured!")
        return
    
    print("To set up Google Calendar OAuth:")
    print("1. Go to Google Cloud Console")
    print("2. Create a new project or select existing")
    print("3. Enable Google Calendar API")
    print("4. Create OAuth 2.0 credentials")
    print("5. Download credentials.json")
    print("6. Run: python oauth_calendar_final.py")
    
    print("\nOr run the automated setup:")
    setup_choice = input("Run automated Google OAuth setup? (y/n): ").strip().lower()
    
    if setup_choice == 'y':
        try:
            import subprocess
            result = subprocess.run(['python', 'oauth_calendar_final.py'], 
                                  capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
        except Exception as e:
            print(f"❌ Error running OAuth setup: {e}")

def test_calendar_integration():
    """Test the calendar integration"""
    
    print("\n🧪 Testing calendar integration...")
    print("=" * 40)
    
    try:
        from calendar_scheduler import get_current_status
        
        print("🔍 Checking calendar status...")
        status, events = get_current_status()
        
        print(f"\n📊 Results:")
        print(f"Status: {status}")
        print(f"Events: {events}")
        
        if status == "busy":
            print("✅ Calendar integration working - you have a meeting!")
        elif status == "free":
            print("✅ Calendar integration working - you're free!")
        elif status == "error":
            print("❌ Calendar integration has errors")
            print("💡 Check your calendar configuration")
        
    except Exception as e:
        print(f"❌ Error testing calendar: {e}")

if __name__ == "__main__":
    setup_dual_calendar()
