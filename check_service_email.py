#!/usr/bin/env python3
"""
Check Service Account Email
Quick check to get the service account email for sharing
"""

import os
import json

def main():
    """Main function"""
    
    print("🔧 Service Account Email Check")
    print("=" * 40)
    
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found!")
        print("Please make sure the service account file is in the current directory")
        return
    
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        email = service_account_data.get('client_email', '')
        project_id = service_account_data.get('project_id', '')
        
        if email:
            print(f"✅ Service account email: {email}")
            print(f"🏢 Project ID: {project_id}")
            print()
            print("📋 Copy this email to share your calendars:")
            print(f"   {email}")
            print()
            print("🔧 Next steps:")
            print("1. Go to: https://calendar.google.com")
            print("2. Click on your calendar settings")
            print("3. Click 'Share with specific people'")
            print(f"4. Add this email: {email}")
            print("5. Set permission to 'See all event details'")
            print("6. Click 'Send'")
            print()
            print("7. Test with: python test_calendar_events.py")
        else:
            print("❌ No client_email found in service-account.json")
            print("Please check your service account file")
            
    except Exception as e:
        print(f"❌ Error reading service-account.json: {e}")

if __name__ == '__main__':
    main()
