#!/usr/bin/env python3
"""
Setup script for all accessible calendars
Tries to work with both own calendars and imported calendars
"""

import os
import json
from calendar_integration_multi import get_all_calendars

def setup_all_calendars():
    """Setup all accessible calendars configuration"""
    
    print("🔧 All Accessible Calendars Setup for iDotMatrix")
    print("=" * 50)
    
    # Check if service account exists
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        print("Please run: python calendar_service_account.py")
        return False
    
    # Get all accessible calendars
    print("📅 Discovering all accessible calendars...")
    calendars = get_all_calendars()
    
    if not calendars:
        print("❌ No calendars accessible!")
        print("Please share your calendars with the service account first.")
        return False
    
    print(f"✅ Found {len(calendars)} accessible calendars:")
    print()
    
    # Categorize calendars
    own_calendars = []
    imported_calendars = []
    
    for calendar in calendars:
        calendar_id = calendar.get('id', '')
        summary = calendar.get('summary', 'No Title')
        access_role = calendar.get('accessRole', '')
        
        if access_role in ['owner', 'writer']:
            own_calendars.append(calendar)
            print(f"✅ Own calendar: {summary} ({access_role})")
        elif access_role == 'reader':
            imported_calendars.append(calendar)
            print(f"📥 Imported calendar: {summary} ({access_role})")
        else:
            print(f"❌ Cannot access: {summary} ({access_role})")
    
    print()
    print(f"📊 Calendar summary:")
    print(f"  Own calendars: {len(own_calendars)}")
    print(f"  Imported calendars: {len(imported_calendars)}")
    print(f"  Total accessible: {len(own_calendars) + len(imported_calendars)}")
    print()
    
    if not own_calendars and not imported_calendars:
        print("❌ No accessible calendars found!")
        return False
    
    # Create configuration
    config = {
        "calendars": {},
        "default_calendar": "primary",
        "timezone": "Europe/Warsaw"
    }
    
    # Add each accessible calendar to configuration
    for calendar in own_calendars + imported_calendars:
        calendar_id = calendar.get('id', '')
        summary = calendar.get('summary', 'No Title')
        access_role = calendar.get('accessRole', '')
        
        print(f"  - {summary} ({access_role})")
        
        # Add to configuration
        config["calendars"][calendar_id] = {
            "id": calendar_id,
            "name": summary,
            "enabled": True,
            "access_role": access_role
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
        print(f"  Total calendars: {len(config['calendars'])}")
        print(f"  Timezone: {config['timezone']}")
        print()
        
        # Test the configuration
        print("🧪 Testing configuration...")
        from calendar_display_imported import get_calendar_info_all_access
        
        # Test current meeting
        current_meeting = get_calendar_info_all_access("current")
        if current_meeting:
            print(f"📅 Current meeting: {current_meeting}")
        else:
            print("📅 No current meeting")
        
        # Test next meeting
        next_meeting = get_calendar_info_all_access("next")
        if next_meeting:
            print(f"📅 Next meeting: {next_meeting}")
        else:
            print("📅 No next meeting")
        
        print()
        print("✅ All calendars setup complete!")
        print()
        print("🚀 Usage:")
        print("  python calendar_display_imported.py DD:4F:93:46:DF:1A current")
        print("  python calendar_display_imported.py DD:4F:93:46:DF:1A next")
        print("  python calendar_display_imported.py DD:4F:93:46:DF:1A today")
        print()
        print("📝 Note: This works with all calendars you have access to")
        print("   Including imported calendars from other people")
        print("   The service account needs to be shared with your calendars")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False

def main():
    """Main function"""
    setup_all_calendars()

if __name__ == '__main__':
    main()
