#!/usr/bin/env python3
"""
Debug service account access
Detailed diagnosis of service account calendar access issues
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def debug_service_account():
    """Debug service account access"""
    
    print("🔍 Service Account Debug Tool")
    print("=" * 50)
    
    # Check if service account file exists
    if not os.path.exists('service-account.json'):
        print("❌ Service account file not found!")
        print("Please create service-account.json first")
        return False
    
    print("✅ Service account file exists")
    
    # Load and analyze service account file
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        print("\n📋 Service Account Details:")
        print("-" * 30)
        
        client_email = service_account_data.get('client_email', 'Not found')
        project_id = service_account_data.get('project_id', 'Not found')
        private_key_id = service_account_data.get('private_key_id', 'Not found')
        
        print(f"📧 Client Email: {client_email}")
        print(f"🏗️  Project ID: {project_id}")
        print(f"🔑 Private Key ID: {private_key_id}")
        
        if not client_email or client_email == 'Not found':
            print("❌ Invalid service account file - missing client_email")
            return False
        
        print("\n🔧 Testing Service Account Authentication:")
        print("-" * 40)
        
        try:
            # Load service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                'service-account.json',
                scopes=['https://www.googleapis.com/auth/calendar.readonly']
            )
            print("✅ Service account credentials loaded")
            
            # Create service
            service = build('calendar', 'v3', credentials=credentials)
            print("✅ Google Calendar API service created")
            
            # Test calendar list access
            print("\n📅 Testing Calendar Access:")
            print("-" * 30)
            
            try:
                calendar_list = service.calendarList().list().execute()
                calendars = calendar_list.get('items', [])
                
                print(f"✅ Calendar API call successful")
                print(f"📊 Found {len(calendars)} calendars")
                
                if calendars:
                    print("\n📋 Accessible Calendars:")
                    for i, calendar in enumerate(calendars):
                        calendar_id = calendar.get('id', 'Unknown')
                        summary = calendar.get('summary', 'No Title')
                        access_role = calendar.get('accessRole', 'Unknown')
                        primary = calendar.get('primary', False)
                        
                        print(f"  {i+1}. {summary}")
                        print(f"     ID: {calendar_id}")
                        print(f"     Role: {access_role}")
                        print(f"     Primary: {primary}")
                        print()
                else:
                    print("❌ No calendars found - this is the problem!")
                    print("\n🔧 TROUBLESHOOTING:")
                    print("-" * 20)
                    print("1. Check if the service account email is correct:")
                    print(f"   {client_email}")
                    print("2. Go to Google Calendar and verify:")
                    print("   - Calendar is shared with this email")
                    print("   - Permission is set to 'See all event details'")
                    print("   - The sharing was successful")
                    print("3. Try sharing the calendar again:")
                    print("   - Go to calendar settings")
                    print("   - Remove the service account")
                    print("   - Add it back with 'See all event details'")
                    print("4. Wait 5-10 minutes for permissions to propagate")
                
            except Exception as e:
                print(f"❌ Calendar API call failed: {e}")
                print("\n🔧 TROUBLESHOOTING:")
                print("-" * 20)
                print("1. Check if Google Calendar API is enabled:")
                print("   - Go to Google Cloud Console")
                print("   - APIs & Services > Library")
                print("   - Search for 'Google Calendar API'")
                print("   - Make sure it's enabled")
                print("2. Check service account permissions:")
                print("   - Go to IAM & Admin > Service Accounts")
                print("   - Find your service account")
                print("   - Check if it has any roles assigned")
                
        except Exception as e:
            print(f"❌ Service account authentication failed: {e}")
            print("\n🔧 TROUBLESHOOTING:")
            print("-" * 20)
            print("1. Check if service-account.json is valid")
            print("2. Verify the JSON file is not corrupted")
            print("3. Try creating a new service account key")
            
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")
        return False
    
    print("\n🎯 NEXT STEPS:")
    print("-" * 20)
    print("1. If no calendars found:")
    print("   - Share your calendar with the service account email")
    print("   - Set permission to 'See all event details'")
    print("   - Wait 5-10 minutes for permissions to propagate")
    print("2. If API errors:")
    print("   - Enable Google Calendar API in Google Cloud Console")
    print("   - Check service account permissions")
    print("3. Test again:")
    print("   - Run: python diagnose_calendar.py")
    print("   - Should show: 'Found X accessible calendars'")
    
    return True

def main():
    """Main function"""
    debug_service_account()

if __name__ == '__main__':
    main()
