#!/usr/bin/env python3
"""
Final Google Calendar authentication using out-of-band flow
This should work reliably for server environments
"""

import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def final_auth():
    """Final authentication using out-of-band flow"""
    
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    
    print("🔐 Final Google Calendar authentication (Out-of-Band)...")
    print("=" * 60)
    
    try:
        # Load credentials
        with open(credentials_file, 'r') as f:
            client_config = json.load(f)
        
        print("✅ Using Desktop application credentials")
        
        # Create flow for desktop application with out-of-band redirect
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES
        )
        
        # Use out-of-band redirect (more reliable for servers)
        flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        
        # Get authorization URL
        auth_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        print("📱 Please visit this URL in your browser:")
        print("=" * 60)
        print(auth_url)
        print("=" * 60)
        print()
        print("📋 Instructions:")
        print("1. Copy the URL above and open it in your browser")
        print("2. Sign in to your Google account")
        print("3. Grant permission to access your calendar")
        print("4. You'll see a page with an authorization code")
        print("5. Copy the code and paste it below")
        print()
        print("⚠️  Important:")
        print("   - This uses out-of-band flow (no localhost redirect)")
        print("   - You'll see a success page with the code")
        print("   - Copy the code immediately - it expires quickly")
        print()
        
        # Get the authorization code from user
        auth_code = input("🔑 Enter the authorization code: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return None
        
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
        print("🔧 Troubleshooting tips:")
        print("1. Make sure you're using a fresh authorization code")
        print("2. Check that the code doesn't have extra spaces or characters")
        print("3. Try the authentication process again")
        print("4. If issues persist, try creating new OAuth credentials")
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
    print("🔧 Google Calendar Authentication (Final - Out-of-Band)")
    print("=" * 60)
    
    # Authenticate
    creds = final_auth()
    
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
