#!/usr/bin/env python3
"""
Troubleshoot service account access
Comprehensive diagnosis of service account calendar access issues
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def troubleshoot_service_account():
    """Troubleshoot service account access"""
    
    print("🔍 Service Account Troubleshooting")
    print("=" * 50)
    
    # Check if service account file exists
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found!")
        return False
    
    print("✅ service-account.json exists")
    
    # Load service account data
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        client_email = service_account_data.get('client_email', '')
        project_id = service_account_data.get('project_id', '')
        
        print(f"📧 Service Account Email: {client_email}")
        print(f"🏗️  Project ID: {project_id}")
        
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")
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
        
        # Test 1: Check if we can make API calls
        print("\n🧪 Test 1: Basic API Access")
        print("-" * 30)
        try:
            # Try to get calendar list
            calendar_list = service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            print(f"✅ API call successful")
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
                
        except Exception as e:
            print(f"❌ API call failed: {e}")
            print("\n🔧 TROUBLESHOOTING STEPS:")
            print("-" * 30)
            print("1. Check if Google Calendar API is enabled:")
            print("   - Go to Google Cloud Console")
            print("   - APIs & Services > Library")
            print("   - Search for 'Google Calendar API'")
            print("   - Make sure it's enabled")
            print()
            print("2. Check service account permissions:")
            print("   - Go to IAM & Admin > Service Accounts")
            print("   - Find your service account")
            print("   - Check if it has any roles assigned")
            print("   - Try adding 'Calendar API User' role")
            print()
            print("3. Check calendar sharing:")
            print("   - Go to Google Calendar")
            print("   - Check if calendar is shared with:")
            print(f"   {client_email}")
            print("   - Permission should be 'See all event details'")
            print()
            print("4. Try creating a new service account key:")
            print("   - Delete the current service-account.json")
            print("   - Create a new key in Google Cloud Console")
            print("   - Download the new JSON file")
            return False
        
        # Test 2: Check specific calendar access
        print("\n🧪 Test 2: Specific Calendar Access")
        print("-" * 30)
        try:
            # Try to access primary calendar
            events_result = service.events().list(
                calendarId='primary',
                timeMin='2024-01-01T00:00:00Z',
                timeMax='2024-12-31T23:59:59Z',
                maxResults=1
            ).execute()
            
            events = events_result.get('items', [])
            print(f"✅ Primary calendar accessible")
            print(f"📅 Found {len(events)} events in primary calendar")
            
        except Exception as e:
            print(f"❌ Primary calendar access failed: {e}")
            print("This suggests the service account doesn't have access to your primary calendar")
        
        # Test 3: Check if we can list all calendars
        print("\n🧪 Test 3: Calendar List Permissions")
        print("-" * 30)
        try:
            # Try to get calendar list with different parameters
            calendar_list = service.calendarList().list(
                minAccessRole='reader'
            ).execute()
            
            calendars = calendar_list.get('items', [])
            print(f"✅ Calendar list with reader access: {len(calendars)} calendars")
            
            if calendars:
                print("📋 Calendars with reader access:")
                for calendar in calendars:
                    summary = calendar.get('summary', 'No Title')
                    access_role = calendar.get('accessRole', 'Unknown')
                    print(f"  - {summary} ({access_role})")
            
        except Exception as e:
            print(f"❌ Calendar list with reader access failed: {e}")
        
        print("\n🎯 SUMMARY:")
        print("-" * 20)
        if calendars:
            print("✅ Service account is working!")
            print("✅ Calendars are accessible!")
            print("✅ The issue might be with the specific calendar sharing")
        else:
            print("❌ Service account cannot access any calendars")
            print("❌ This suggests a fundamental access issue")
            print("\n🔧 NEXT STEPS:")
            print("1. Double-check calendar sharing in Google Calendar")
            print("2. Verify the service account email is correct")
            print("3. Try sharing the calendar again")
            print("4. Wait 10-15 minutes for permissions to propagate")
            print("5. Check if Google Calendar API is enabled")
        
        return True
        
    except Exception as e:
        print(f"❌ Service account authentication failed: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("-" * 20)
        print("1. Check if service-account.json is valid")
        print("2. Verify the JSON file is not corrupted")
        print("3. Try creating a new service account key")
        print("4. Make sure Google Calendar API is enabled")
        return False

def main():
    """Main function"""
    troubleshoot_service_account()

if __name__ == '__main__':
    main()
