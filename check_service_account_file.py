#!/usr/bin/env python3
"""
Check service account file
Simple check to see if service-account.json exists and is valid
"""

import os
import json

def check_service_account_file():
    """Check service account file"""
    
    print("🔍 Service Account File Check")
    print("=" * 40)
    
    # Check if file exists
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found!")
        print("Please create the service account file first")
        return False
    
    print("✅ service-account.json exists")
    
    # Check file contents
    try:
        with open('service-account.json', 'r') as f:
            data = json.load(f)
        
        print("✅ File is valid JSON")
        
        # Check required fields
        required_fields = ['client_email', 'private_key', 'project_id']
        missing_fields = []
        
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields: {', '.join(missing_fields)}")
            return False
        
        print("✅ All required fields present")
        
        # Show key information
        client_email = data.get('client_email', '')
        project_id = data.get('project_id', '')
        
        print(f"\n📧 Service Account Email: {client_email}")
        print(f"🏗️  Project ID: {project_id}")
        
        print("\n🔧 NEXT STEPS:")
        print("-" * 20)
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
        print("⏳ Wait 5-10 minutes for permissions to propagate")
        print("Then run: python diagnose_calendar.py")
        
        return True
        
    except json.JSONDecodeError:
        print("❌ File is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def main():
    """Main function"""
    check_service_account_file()

if __name__ == '__main__':
    main()
