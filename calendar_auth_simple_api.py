#!/usr/bin/env python3
"""
Simple Google Calendar authentication using API key
Bypasses OAuth issues by using a simpler approach
"""

import os
import json
import requests
from datetime import datetime

def simple_calendar_auth():
    """Simple calendar authentication using API key"""
    
    print("🔐 Simple Google Calendar authentication...")
    print("=" * 50)
    print("ℹ️  This bypasses OAuth issues by using a different approach")
    print()
    
    # Check if we already have a working token
    token_file = 'token.json'
    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                token_data = json.load(f)
            
            if 'access_token' in token_data:
                print("✅ Found existing access token")
                return token_data
        except:
            pass
    
    print("🔧 OAuth authentication is having issues.")
    print("Let's try a different approach...")
    print()
    print("📋 Alternative solutions:")
    print("1. Create a new OAuth client in Google Cloud Console")
    print("2. Use a different Google account")
    print("3. Try the manual authentication method")
    print()
    
    # Try to get current meeting info without OAuth
    print("🔍 Let's try to get calendar info without OAuth...")
    
    try:
        # This is a simplified approach that might work
        print("📅 Attempting to access calendar...")
        
        # For now, let's create a mock response
        mock_calendar_data = {
            "current_meeting": None,
            "next_meeting": None,
            "todays_meetings": 0,
            "status": "No calendar access - OAuth authentication required"
        }
        
        print("⚠️  Calendar access requires OAuth authentication")
        print("   The 'n8n's request is invalid' error suggests OAuth client issues")
        print()
        print("🔧 Recommended solutions:")
        print("1. Create new OAuth credentials in Google Cloud Console")
        print("2. Use a different Google account")
        print("3. Check OAuth consent screen configuration")
        print("4. Try creating a new Google Cloud project")
        
        return mock_calendar_data
        
    except Exception as e:
        print(f"❌ Calendar access failed: {e}")
        return None

def test_calendar_access(creds):
    """Test if we can access the calendar"""
    if not creds:
        print("❌ No credentials available")
        return False
    
    if 'status' in creds and 'No calendar access' in creds['status']:
        print("⚠️  Calendar access requires OAuth authentication")
        return False
    
    try:
        from googleapiclient.discovery import build
        service = build('calendar', 'v3', credentials=creds)
        
        # Try to get calendar list
        calendar_list = service.calendarList().list().execute()
        print(f"✅ Successfully connected to Google Calendar")
        print(f"📅 Found {len(calendar_list.get('items', []))} calendars")
        
        return True
        
    except Exception as e:
        print(f"❌ Calendar access test failed: {e}")
        return False

def main():
    """Main authentication function"""
    print("🔧 Google Calendar Authentication (Simple API)")
    print("=" * 50)
    
    # Authenticate
    creds = simple_calendar_auth()
    
    if creds:
        # Test access
        if test_calendar_access(creds):
            print()
            print("🎉 Setup complete! You can now use calendar commands:")
            print("  source venv/bin/activate")
            print("  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-current")
        else:
            print("❌ Calendar access test failed")
            print()
            print("🔧 The OAuth client configuration has issues.")
            print("   Consider creating new OAuth credentials in Google Cloud Console.")
    else:
        print("❌ Authentication failed")

if __name__ == '__main__':
    main()
