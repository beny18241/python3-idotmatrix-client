#!/usr/bin/env python3
"""
Setup script for own calendars only
Works with calendars you own and can share with service account
"""

import os
import json
from calendar_integration_multi import get_all_calendars

def setup_own_calendars():
    """Setup own calendars configuration"""
    
    print("🔧 Own Calendars Setup for iDotMatrix")
    print("=" * 50)
    
    # Check if service account exists
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        print("Please run: python calendar_service_account.py")
        return False
    
    # Get all accessible calendars
    print("📅 Discovering your own calendars...")
    calendars = get_all_calendars()
    
    if not calendars:
        print("❌ No calendars accessible!")
        print("Please share your calendars with the service account first.")
        return False
    
    print(f"✅ Found {len(calendars)} accessible calendars:")
    print()
    
    # Filter to own calendars only
    own_calendars = []
    for calendar in calendars:
        calendar_id = calendar.get('id', '')
        summary = calendar.get('summary', 'No Title')
        access_role = calendar.get('accessRole', '')
        
        if access_role in ['owner', 'writer']:
            own_calendars.append(calendar)
            print(f"✅ Own calendar: {summary} ({access_role})")
        else:
            print(f"❌ Cannot access: {summary} ({access_role})")
    
    if not own_calendars:
        print("❌ No own calendars found!")
        print("You need to share your calendars with the service account.")
        return False
    
    print()
    print(f"📅 Using {len(own_calendars)} own calendars:")
    
    # Create configuration
    config = {
        "calendars": {},
        "default_calendar": "primary",
        "timezone": "Europe/Warsaw"
    }
    
    # Add each own calendar to configuration
    for calendar in own_calendars:
        calendar_id = calendar.get('id', '')
        summary = calendar.get('summary', 'No Title')
        
        print(f"  - {summary}")
        
        # Add to configuration
        config["calendars"][calendar_id] = {
            "id": calendar_id,
            "name": summary,
            "enabled": True
        }
    
    # Set default calendar
    if "primary" in config["calendars"]:
        config["default_calendar"] = "primary"
    else:
        # Use first calendar as default
        first_calendar_id = list(config["calendars"].keys())[0]
        config["default_calendar"] = first_calendar_id
    
    # Save configuration
    try:
        with open('calendar_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print()
        print("✅ Configuration saved to calendar_config.json")
        print()
        print("📋 Configuration summary:")
        print(f"  Default calendar: {config['default_calendar']}")
        print(f"  Own calendars: {len(config['calendars'])}")
        print(f"  Timezone: {config['timezone']}")
        print()
        
        # Test the configuration
        print("🧪 Testing configuration...")
        from calendar_display_own_only import get_calendar_info_own_only
        
        # Test current meeting
        current_meeting = get_calendar_info_own_only("current")
        if current_meeting:
            print(f"📅 Current meeting: {current_meeting}")
        else:
            print("📅 No current meeting")
        
        # Test next meeting
        next_meeting = get_calendar_info_own_only("next")
        if next_meeting:
            print(f"📅 Next meeting: {next_meeting}")
        else:
            print("📅 No next meeting")
        
        print()
        print("✅ Own calendars setup complete!")
        print()
        print("🚀 Usage:")
        print("  python calendar_display_own_only.py DD:4F:93:46:DF:1A current")
        print("  python calendar_display_own_only.py DD:4F:93:46:DF:1A next")
        print("  python calendar_display_own_only.py DD:4F:93:46:DF:1A today")
        print()
        print("📝 Note: This only works with calendars you own and can share")
        print("   Imported calendars from others cannot be accessed")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False

def main():
    """Main function"""
    setup_own_calendars()

if __name__ == '__main__':
    main()
