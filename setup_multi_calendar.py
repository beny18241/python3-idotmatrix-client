#!/usr/bin/env python3
"""
Setup script for multi-calendar integration
Helps configure multiple Google Calendars
"""

import os
import json
from calendar_integration_multi import get_all_calendars

def setup_multi_calendar():
    """Setup multi-calendar configuration"""
    
    print("🔧 Multi-Calendar Setup for iDotMatrix")
    print("=" * 50)
    
    # Check if service account exists
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        print("Please run: python calendar_service_account.py")
        return False
    
    # Get all accessible calendars
    print("📅 Discovering accessible calendars...")
    calendars = get_all_calendars()
    
    if not calendars:
        print("❌ No calendars accessible!")
        return False
    
    print(f"✅ Found {len(calendars)} accessible calendars:")
    print()
    
    # Create configuration
    config = {
        "calendars": {},
        "default_calendar": "primary",
        "timezone": "Europe/Warsaw"
    }
    
    # Add each calendar to configuration
    for i, calendar in enumerate(calendars):
        calendar_id = calendar.get('id', f'calendar_{i}')
        summary = calendar.get('summary', f'Calendar {i+1}')
        description = calendar.get('description', '')
        
        print(f"{i+1}. {summary}")
        print(f"   ID: {calendar_id}")
        if description:
            print(f"   Description: {description}")
        print()
        
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
        
        print("✅ Configuration saved to calendar_config.json")
        print()
        print("📋 Configuration summary:")
        print(f"  Default calendar: {config['default_calendar']}")
        print(f"  Total calendars: {len(config['calendars'])}")
        print(f"  Timezone: {config['timezone']}")
        print()
        
        # Test the configuration
        print("🧪 Testing configuration...")
        from calendar_display_multi import get_calendar_info_from_config
        
        # Test current meeting
        current_meeting = get_calendar_info_from_config("current")
        if current_meeting:
            print(f"📅 Current meeting: {current_meeting}")
        else:
            print("📅 No current meeting")
        
        # Test next meeting
        next_meeting = get_calendar_info_from_config("next")
        if next_meeting:
            print(f"📅 Next meeting: {next_meeting}")
        else:
            print("📅 No next meeting")
        
        print()
        print("✅ Multi-calendar setup complete!")
        print()
        print("🚀 Usage:")
        print("  python calendar_display_multi.py DD:4F:93:46:DF:1A current")
        print("  python calendar_display_multi.py DD:4F:93:46:DF:1A next")
        print("  python calendar_display_multi.py DD:4F:93:46:DF:1A today")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False

def main():
    """Main function"""
    setup_multi_calendar()

if __name__ == '__main__':
    main()
