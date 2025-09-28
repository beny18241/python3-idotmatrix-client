#!/usr/bin/env python3
"""
Google Calendar authentication with current URL
Uses the current URL from the robust script
"""

import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def current_auth():
    """Authentication with current URL"""
    
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    
    print("🔐 Google Calendar authentication with current URL...")
    print("=" * 60)
    
    # Current URL from the robust script
    current_url = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=251184335563-8ip390ojqtn91gi99tnafp4bn29c8k3o.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fcallback&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly&state=YRytmxqRQQU0als3sMwWC68o8jnJ4G&access_type=offline&include_granted_scopes=true&prompt=consent"
    
    print("📱 Please visit this URL in your browser:")
    print("=" * 60)
    print(current_url)
    print("=" * 60)
    print()
    print("📋 Instructions:")
    print("1. Copy the URL above and open it in your browser")
    print("2. Sign in to your Google account")
    print("3. Grant permission to access your calendar")
    print("4. You'll be redirected to http://localhost:8080/callback")
    print("5. The page will show 'This site can't be reached' - this is normal!")
    print("6. Look at the URL in your browser's address bar")
    print("7. Copy the 'code' parameter from the URL")
    print("8. Paste the code below")
    print()
    print("🔧 What to look for in the URL:")
    print("   http://localhost:8080/callback?code=4/0AVGzR1NEW_CODE_HERE&state=...")
    print("   Copy this part: 4/0AVGzR1NEW_CODE_HERE")
    print()
    
    # Get the authorization code from user
    auth_code = input("🔑 Enter the authorization code: ").strip()
    
    if not auth_code:
        print("❌ No authorization code provided")
        return None
    
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
        
        try:
            # Try with the requested scopes first
            flow.fetch_token(code=auth_code)
            creds = flow.credentials
            print("✅ Authentication successful with requested scopes!")
            
        except Exception as e:
            if "Scope has changed" in str(e):
                print("⚠️  Scope mismatch detected - using granted scopes...")
                
                # Extract the granted scopes from the error message
                error_msg = str(e)
                if "to \"" in error_msg:
                    granted_scopes_str = error_msg.split("to \"")[1].split("\"")[0]
                    granted_scopes = granted_scopes_str.split()
                    
                    print(f"🔧 Using granted scopes: {len(granted_scopes)} scopes")
                    
                    # Create new flow with granted scopes
                    flow2 = Flow.from_client_config(
                        client_config,
                        scopes=granted_scopes
                    )
                    flow2.redirect_uri = 'http://localhost:8080/callback'
                    
                    # Try again with the granted scopes
                    flow2.fetch_token(code=auth_code)
                    creds = flow2.credentials
                    print("✅ Authentication successful with granted scopes!")
                    
                else:
                    raise e
            else:
                raise e
        
        # Save credentials
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        
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
    print("🔧 Google Calendar Authentication (Current URL)")
    print("=" * 60)
    
    # Authenticate
    creds = current_auth()
    
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
