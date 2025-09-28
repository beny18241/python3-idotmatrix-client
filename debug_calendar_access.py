#!/usr/bin/env python3
"""
Debug Calendar Access
Comprehensive diagnostic to identify calendar access issues
"""

import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def debug_service_account():
    """Debug service account configuration"""
    
    print("1️⃣ Service Account Configuration")
    print("=" * 40)
    
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found!")
        return False
    
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        print("✅ service-account.json found")
        print(f"   📧 Email: {service_account_data.get('client_email', 'Unknown')}")
        print(f"   🏢 Project: {service_account_data.get('project_id', 'Unknown')}")
        print(f"   🔑 Type: {service_account_data.get('type', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading service-account.json: {e}")
        return False

def debug_api_access():
    """Debug Google Calendar API access"""
    
    print("\n2️⃣ Google Calendar API Access")
    print("=" * 40)
    
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
        
        # Test API access with a simple call
        try:
            # Try to get calendar list
            calendar_list = service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            print(f"✅ API access successful")
            print(f"📅 Found {len(calendars)} calendars")
            
            if calendars:
                print("\n📋 Calendar Details:")
                for i, calendar in enumerate(calendars):
                    calendar_id = calendar.get('id', 'Unknown')
                    summary = calendar.get('summary', 'No Title')
                    access_role = calendar.get('accessRole', 'Unknown')
                    primary = calendar.get('primary', False)
                    
                    print(f"   {i+1}. {summary}")
                    print(f"      ID: {calendar_id}")
                    print(f"      Role: {access_role}")
                    print(f"      Primary: {primary}")
                    print()
            
            return True, calendars
            
        except HttpError as e:
            print(f"❌ HTTP Error: {e}")
            print(f"   Status: {e.resp.status}")
            print(f"   Reason: {e.resp.reason}")
            
            if e.resp.status == 403:
                print("   💡 This suggests permission issues")
            elif e.resp.status == 404:
                print("   💡 This suggests API not enabled")
            elif e.resp.status == 401:
                print("   💡 This suggests authentication issues")
            
            return False, []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, []

def debug_calendar_sharing():
    """Debug calendar sharing issues"""
    
    print("\n3️⃣ Calendar Sharing Debug")
    print("=" * 40)
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Try to get primary calendar
        try:
            primary_calendar = service.calendars().get(calendarId='primary').execute()
            print("✅ Primary calendar accessible")
            print(f"   📅 Summary: {primary_calendar.get('summary', 'Unknown')}")
            print(f"   🆔 ID: {primary_calendar.get('id', 'Unknown')}")
            print(f"   📧 Owner: {primary_calendar.get('summary', 'Unknown')}")
            
        except HttpError as e:
            print(f"❌ Primary calendar not accessible: {e}")
            if e.resp.status == 403:
                print("   💡 Primary calendar not shared with service account")
            elif e.resp.status == 404:
                print("   💡 Primary calendar not found")
        
        # Try to get calendar list
        try:
            calendar_list = service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            if calendars:
                print(f"✅ Found {len(calendars)} accessible calendars")
                
                # Check each calendar's access
                for calendar in calendars:
                    calendar_id = calendar.get('id', '')
                    summary = calendar.get('summary', 'Unknown')
                    access_role = calendar.get('accessRole', 'Unknown')
                    
                    print(f"   📅 {summary}")
                    print(f"      Role: {access_role}")
                    
                    # Try to get events from this calendar
                    try:
                        events_result = service.events().list(
                            calendarId=calendar_id,
                            timeMin=datetime.datetime.now().isoformat() + 'Z',
                            maxResults=1
                        ).execute()
                        
                        events = events_result.get('items', [])
                        print(f"      Events accessible: {len(events)}")
                        
                    except HttpError as e:
                        print(f"      ❌ Events not accessible: {e}")
                        
            else:
                print("❌ No calendars accessible")
                print("💡 This suggests:")
                print("   • Calendars not shared with service account")
                print("   • Service account doesn't have calendar access")
                print("   • API permissions issue")
                
        except HttpError as e:
            print(f"❌ Calendar list not accessible: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def provide_solutions():
    """Provide solutions based on diagnostic results"""
    
    print("\n4️⃣ Solutions")
    print("=" * 40)
    
    print("🔧 If you're still getting 0 calendars, try these solutions:")
    print()
    
    print("1️⃣ Double-check Calendar Sharing:")
    print("   • Go to: https://calendar.google.com")
    print("   • Click on your calendar")
    print("   • Click 'Settings and sharing'")
    print("   • Make sure the service account email is listed")
    print("   • Make sure it has 'See all event details' permission")
    print()
    
    print("2️⃣ Try Different Sharing Method:")
    print("   • Instead of 'Share with specific people'")
    print("   • Try 'Make available to public' temporarily")
    print("   • Set to 'See all event details'")
    print("   • Test if this works")
    print("   • If it works, the issue is with specific sharing")
    print()
    
    print("3️⃣ Check Service Account Domain:")
    print("   • Make sure you're using the correct Google account")
    print("   • The service account should be in the same domain")
    print("   • Or the calendar should be explicitly shared")
    print()
    
    print("4️⃣ Try Alternative Approach:")
    print("   • Use OAuth instead of service account")
    print("   • Run: python calendar_auth_final.py")
    print("   • This bypasses service account issues")
    print()
    
    print("5️⃣ Check API Enablement:")
    print("   • Go to: https://console.cloud.google.com/apis/library")
    print("   • Search for 'Google Calendar API'")
    print("   • Make sure it's enabled")
    print("   • Try disabling and re-enabling it")

def main():
    """Main function"""
    
    print("🔧 Calendar Access Debug")
    print("=" * 50)
    
    # Debug service account
    if not debug_service_account():
        return
    
    # Debug API access
    api_success, calendars = debug_api_access()
    
    if not api_success:
        print("\n❌ API access failed - check API enablement")
        provide_solutions()
        return
    
    # Debug calendar sharing
    debug_calendar_sharing()
    
    # Provide solutions
    provide_solutions()

if __name__ == '__main__':
    main()