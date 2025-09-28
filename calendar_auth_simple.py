#!/usr/bin/env python3
"""
Simple Google Calendar authentication for server environments
Uses the out-of-band (OOB) flow which is more reliable for headless servers
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    """Simple authentication for Google Calendar"""
    
    creds = None
    token_file = 'token.json'
    credentials_file = 'credentials.json'
    
    # Check if token already exists
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully")
            except Exception as e:
                print(f"❌ Token refresh failed: {e}")
                print("Please re-authenticate")
                creds = None
        
        if not creds:
            if not os.path.exists(credentials_file):
                print(f"❌ {credentials_file} not found!")
                print("Please download credentials.json from Google Cloud Console")
                return None
            
            print("🔐 Starting Google Calendar authentication...")
            print("=" * 50)
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                
                # Use out-of-band flow for headless environments
                auth_url, _ = flow.authorization_url(
                    access_type='offline',
                    include_granted_scopes='true',
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
                )
                
                print("📱 Please visit this URL in your browser:")
                print("=" * 50)
                print(auth_url)
                print("=" * 50)
                print()
                print("📋 After visiting the URL:")
                print("1. Sign in to your Google account")
                print("2. Grant permission to access your calendar")
                print("3. You'll see a page with an authorization code")
                print("4. Copy the code and paste it below")
                print()
                
                auth_code = input("🔑 Enter the authorization code: ").strip()
                
                if not auth_code:
                    print("❌ No authorization code provided")
                    return None
                
                # Exchange the code for tokens
                flow.fetch_token(code=auth_code)
                creds = flow.credentials
                
                print("✅ Authentication successful!")
                
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                return None
        
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        print(f"💾 Credentials saved to {token_file}")
    
    return creds

def test_calendar_access(creds):
    """Test if we can access the calendar"""
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
    print("🔧 Google Calendar Authentication Setup")
    print("=" * 40)
    
    # Authenticate
    creds = authenticate_google_calendar()
    
    if creds:
        # Test access
        if test_calendar_access(creds):
            print()
            print("🎉 Setup complete! You can now use calendar commands:")
            print("  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-current")
            print("  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-next")
            print("  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-today")
        else:
            print("❌ Calendar access test failed")
    else:
        print("❌ Authentication failed")

if __name__ == '__main__':
    main()
