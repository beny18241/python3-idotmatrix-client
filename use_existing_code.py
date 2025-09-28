#!/usr/bin/env python3
"""
Use the existing authorization code to complete authentication
"""

import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def use_existing_code():
    """Use the existing authorization code"""
    
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    
    # The authorization code from your URL
    auth_code = "4/0AVGzR1AVtoANT9oG-cOvB5BTf9loiNshFH9SIyFrr4_4_XcwImE7xiQ1CqBqfX_dDM-HRQ"
    
    print("🔐 Using existing authorization code...")
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
        print()
        print("🔧 The authorization code may have expired or been used already.")
        print("   Let's try with a fresh code from the current URL.")
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
    print("🔧 Google Calendar Authentication (Use Existing Code)")
    print("=" * 60)
    
    # Authenticate
    creds = use_existing_code()
    
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
        print()
        print("🔧 Let's try with a fresh code from the current URL:")
        print("1. Copy the current URL from the robust script")
        print("2. Open it in your browser")
        print("3. Get a fresh authorization code")
        print("4. Run this script again with the new code")

if __name__ == '__main__':
    main()
