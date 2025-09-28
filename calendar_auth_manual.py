#!/usr/bin/env python3
"""
Manual Google Calendar authentication for server environments
Uses a simpler approach that works better with headless servers
"""

import os
import json
import urllib.parse
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def manual_oauth_flow():
    """Manual OAuth flow that works better for headless servers"""
    
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    
    # Check if credentials file exists
    if not os.path.exists(credentials_file):
        print(f"❌ {credentials_file} not found!")
        print("Please download credentials.json from Google Cloud Console")
        return None
    
    # Check if token already exists
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            if creds and creds.valid:
                print("✅ Valid token found, no need to re-authenticate")
                return creds
            elif creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✅ Token refreshed successfully")
                    # Save refreshed token
                    with open(token_file, 'w') as token:
                        token.write(creds.to_json())
                    return creds
                except Exception as e:
                    print(f"❌ Token refresh failed: {e}")
                    print("Will need to re-authenticate")
        except Exception as e:
            print(f"❌ Error loading token: {e}")
    
    print("🔐 Starting manual Google Calendar authentication...")
    print("=" * 50)
    
    try:
        # Load credentials
        with open(credentials_file, 'r') as f:
            client_config = json.load(f)
        
        # Create flow with minimal configuration
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'
        )
        
        # Get authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        print("📱 Please visit this URL in your browser:")
        print("=" * 50)
        print(auth_url)
        print("=" * 50)
        print()
        print("📋 Instructions:")
        print("1. Copy the URL above and open it in your browser")
        print("2. Sign in to your Google account")
        print("3. Grant permission to access your calendar")
        print("4. You'll see a page with an authorization code")
        print("5. Copy the code and paste it below")
        print()
        
        # Get authorization code from user
        auth_code = input("🔑 Enter the authorization code: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return None
        
        # Exchange code for tokens
        print("🔄 Exchanging code for tokens...")
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
    print("🔧 Google Calendar Authentication Setup")
    print("=" * 40)
    
    # Authenticate
    creds = manual_oauth_flow()
    
    if creds:
        # Test access
        if test_calendar_access(creds):
            print()
            print("🎉 Setup complete! You can now use calendar commands:")
            print("  source venv/bin/activate")
            print("  python calendar_auth_simple.py")
            print("  ./run_in_venv.sh --address DD:4F:93:46:DF:1A --calendar-current")
        else:
            print("❌ Calendar access test failed")
    else:
        print("❌ Authentication failed")

if __name__ == '__main__':
    main()
