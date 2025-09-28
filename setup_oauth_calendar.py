#!/usr/bin/env python3
"""
Setup OAuth Calendar Access
Simple setup for OAuth-based calendar access
"""

import os
import sys
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def setup_oauth_calendar():
    """Setup OAuth calendar access"""
    
    print("🔧 Setting up OAuth Calendar Access")
    print("=" * 50)
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("Please download OAuth credentials from Google Cloud Console:")
        print("1. Go to: https://console.cloud.google.com/apis/credentials")
        print("2. Click 'Create Credentials' > 'OAuth client ID'")
        print("3. Choose 'Desktop application'")
        print("4. Download the JSON file as 'credentials.json'")
        return False
    
    print("✅ credentials.json found")
    
    # Check if token.json exists
    if os.path.exists('token.json'):
        print("✅ OAuth token found")
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            if creds.valid:
                print("✅ OAuth token is valid")
                return True
            elif creds.expired and creds.refresh_token:
                print("🔄 Refreshing OAuth token...")
                creds.refresh(Request())
                print("✅ OAuth token refreshed")
                
                # Save refreshed token
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                print("✅ OAuth token saved")
                return True
            else:
                print("❌ OAuth token is invalid")
        except Exception as e:
            print(f"❌ Error with OAuth token: {e}")
    
    # Get new OAuth credentials
    print("🔐 Starting OAuth authentication...")
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        print("✅ OAuth authentication successful")
        
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("✅ OAuth token saved")
        
        return True
        
    except Exception as e:
        print(f"❌ OAuth authentication failed: {e}")
        return False

def test_oauth_calendar():
    """Test OAuth calendar access"""
    
    print("\n🔧 Testing OAuth Calendar Access")
    print("=" * 50)
    
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Load credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Create service
        service = build('calendar', 'v3', credentials=creds)
        print("✅ Google Calendar API service created")
        
        # Get calendar list
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        print(f"📅 Found {len(calendars)} accessible calendars")
        
        if calendars:
            print("\n📋 Accessible Calendars:")
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
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, []

def main():
    """Main function"""
    
    print("🔧 OAuth Calendar Setup")
    print("=" * 30)
    
    # Setup OAuth
    if not setup_oauth_calendar():
        print("❌ OAuth setup failed")
        return
    
    # Test OAuth
    success, calendars = test_oauth_calendar()
    
    if success:
        print("✅ OAuth Calendar setup complete!")
        print("🚀 You can now use:")
        print("   python oauth_calendar_final.py DD:4F:93:46:DF:1A tomorrow")
    else:
        print("❌ OAuth Calendar test failed")
        print("Please check your OAuth credentials")

if __name__ == '__main__':
    main()
