#!/usr/bin/env python3
"""
Google Calendar authentication with scope handling
Handles cases where Google requests additional scopes
"""

import os
import json
import urllib.parse
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def scope_fix_oauth_flow():
    """OAuth flow that handles scope mismatches"""
    
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    
    # Check if credentials file exists
    if not os.path.exists(credentials_file):
        print(f"❌ {credentials_file} not found!")
        print("Please download credentials.json from Google Cloud Console")
        return None
    
    # Check if token already exists and is valid
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
    
    print("🔐 Starting Google Calendar authentication (Scope Fix)...")
    print("=" * 60)
    
    try:
        # Load credentials
        with open(credentials_file, 'r') as f:
            client_config = json.load(f)
        
        print("✅ Using Desktop application with scope handling")
        
        # Create flow for desktop application
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES
        )
        
        # Use localhost redirect
        flow.redirect_uri = 'http://localhost:8080/callback'
        
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
        print("4. You'll be redirected to http://localhost:8080/callback")
        print("5. The page will show 'This site can't be reached' - this is normal!")
        print("6. Look at the URL in your browser's address bar")
        print("7. Copy the 'code' parameter from the URL")
        print("8. Paste the code below")
        print()
        print("⚠️  Note: Google may request additional permissions beyond calendar access.")
        print("   This is normal - just grant all permissions to proceed.")
        print()
        
        # Get authorization code from user
        auth_code = input("🔑 Enter the authorization code: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return None
        
        # Exchange code for tokens
        print("🔄 Exchanging code for tokens...")
        
        try:
            flow.fetch_token(code=auth_code)
            creds = flow.credentials
        except Exception as e:
            if "Scope has changed" in str(e):
                print("⚠️  Scope mismatch detected - trying alternative approach...")
                
                # Try with the actual granted scopes
                granted_scopes = str(e).split('"')[1] if '"' in str(e) else None
                if granted_scopes:
                    print(f"🔧 Using granted scopes: {granted_scopes[:100]}...")
                    
                    # Create new flow with granted scopes
                    granted_scopes_list = granted_scopes.split()
                    flow2 = Flow.from_client_config(
                        client_config,
                        scopes=granted_scopes_list
                    )
                    flow2.redirect_uri = 'http://localhost:8080/callback'
                    
                    # Try again with the granted scopes
                    flow2.fetch_token(code=auth_code)
                    creds = flow2.credentials
                else:
                    raise e
            else:
                raise e
        
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
        print("1. Make sure you're using the correct authorization code")
        print("2. Check that the code doesn't have extra spaces or characters")
        print("3. The localhost redirect is normal - just copy the code from the URL")
        print("4. Try the authentication process again")
        print("5. If scope issues persist, try creating new OAuth credentials")
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
    print("🔧 Google Calendar Authentication (Scope Fix)")
    print("=" * 60)
    
    # Authenticate
    creds = scope_fix_oauth_flow()
    
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
