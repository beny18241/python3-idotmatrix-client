#!/usr/bin/env python3
"""
Check Token Status
Check OAuth token status and configuration
"""

import os
import json
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def check_token_file():
    """Check token.json file"""
    
    print("🔧 Checking Token File")
    print("=" * 30)
    
    if not os.path.exists('token.json'):
        print("❌ token.json not found!")
        return False
    
    try:
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        
        print("✅ token.json found")
        print("📋 Token structure:")
        for key in token_data.keys():
            print(f"   {key}: {'✅' if token_data[key] else '❌'}")
        
        # Check expiration
        if 'expiry' in token_data:
            expiry = datetime.datetime.fromisoformat(token_data['expiry'].replace('Z', '+00:00'))
            now = datetime.datetime.now(datetime.timezone.utc)
            
            if expiry > now:
                time_left = expiry - now
                print(f"⏰ Token expires in: {time_left}")
                print(f"📅 Expires at: {expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            else:
                print("❌ Token has expired!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading token.json: {e}")
        return False

def check_token_validity():
    """Check if token is valid and can be refreshed"""
    
    print("\n🔧 Checking Token Validity")
    print("=" * 30)
    
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Load credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Check if token is valid
        if creds.valid:
            print("✅ OAuth token is valid")
            return True
        elif creds.expired and creds.refresh_token:
            print("🔄 Token expired but refresh token available")
            print("🔄 Attempting to refresh...")
            
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully")
                
                # Save refreshed token
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                print("✅ Refreshed token saved")
                return True
                
            except Exception as e:
                print(f"❌ Token refresh failed: {e}")
                return False
        else:
            print("❌ OAuth token is invalid")
            return False
            
    except Exception as e:
        print(f"❌ Error checking token validity: {e}")
        return False

def check_calendar_access():
    """Check if token can access Google Calendar"""
    
    print("\n🔧 Checking Calendar Access")
    print("=" * 30)
    
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Load credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Create service
        from googleapiclient.discovery import build
        service = build('calendar', 'v3', credentials=creds)
        
        # Get calendar list
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        print(f"✅ Calendar access working")
        print(f"📅 Found {len(calendars)} accessible calendars")
        
        return True
        
    except Exception as e:
        print(f"❌ Calendar access failed: {e}")
        return False

def main():
    """Main function"""
    
    print("🔧 OAuth Token Status Check")
    print("=" * 40)
    
    # Check token file
    if not check_token_file():
        return
    
    # Check token validity
    if not check_token_validity():
        print("\n❌ Token is not valid")
        print("💡 You may need to copy a fresh token from your local machine")
        return
    
    # Check calendar access
    if not check_calendar_access():
        print("\n❌ Calendar access failed")
        print("💡 Check your Google Calendar API settings")
        return
    
    print("\n✅ OAuth token is working perfectly!")
    print("🚀 You can use:")
    print("   ./run_oauth_calendar_venv.sh DD:4F:93:46:DF:1A tomorrow")

if __name__ == '__main__':
    main()
