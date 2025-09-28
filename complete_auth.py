#!/usr/bin/env python3
"""
Complete Google Calendar authentication with the provided code
"""

import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def complete_authentication():
    """Complete authentication with the provided code"""
    
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    
    # The authorization code from your URL
    auth_code = "4/0AVGzR1DF1LOny83GMEaFi5RAlsNlC0n5B24TAsLVvvNEHg3KjqhUJkxDzc0ZGGjpWOFnLQ"
    
    print("🔐 Completing Google Calendar authentication...")
    print("=" * 50)
    
    try:
        # Load credentials
        with open(credentials_file, 'r') as f:
            client_config = json.load(f)
        
        print("✅ Using Desktop application credentials")
        
        # Create flow for desktop application
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES
        )
        
        # Use localhost redirect
        flow.redirect_uri = 'http://localhost:8080/callback'
        
        print("🔄 Exchanging authorization code for tokens...")
        
        # Exchange code for tokens
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        # Save credentials
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        
        print("✅ Authentication successful!")
        print(f"💾 Credentials saved to {token_file}")
        
        return creds
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return None

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
    print("🔧 Google Calendar Authentication (Complete)")
    print("=" * 50)
    
    # Authenticate
    creds = complete_authentication()
    
    if creds:
        # Test access
        if test_calendar_access(creds):
            print()
            print("🎉 Setup complete! You can now use calendar commands:")
            print("  source venv/bin/activate")
            print("  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-current")
        else:
            print("❌ Calendar access test failed")
    else:
        print("❌ Authentication failed")

if __name__ == '__main__':
    main()
