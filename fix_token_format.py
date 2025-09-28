#!/usr/bin/env python3
"""
Fix Token Format
Fix OAuth token format without requiring browser authentication
"""

import os
import json
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def fix_token_format():
    """Fix OAuth token format without browser"""
    
    print("🔧 Fixing OAuth Token Format (No Browser Required)")
    print("=" * 60)
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    # Check if token.json exists
    if not os.path.exists('token.json'):
        print("❌ token.json not found!")
        print("💡 You need to create an OAuth token first")
        return False
    
    print("✅ token.json found")
    
    try:
        # Load existing token
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        
        print("📋 Current token structure:")
        for key in token_data.keys():
            print(f"   {key}: {'✅' if token_data[key] else '❌'}")
        
        # Check if it's a service account token
        if 'client_email' in token_data:
            print("❌ This is a service account token, not OAuth token")
            print("💡 We need to create a proper OAuth token")
            return False
        
        # Check if it's missing required OAuth fields
        required_fields = ['token', 'refresh_token', 'client_id', 'client_secret']
        missing_fields = [field for field in required_fields if field not in token_data]
        
        if missing_fields:
            print(f"❌ Missing required OAuth fields: {missing_fields}")
            print("💡 This token was created incorrectly")
            return False
        
        print("✅ Token has all required OAuth fields")
        
        # Try to load as OAuth credentials
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            print("✅ OAuth token loaded successfully")
            
            # Test if token is valid
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
                return False
                
        except Exception as e:
            print(f"❌ Error loading OAuth token: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error reading token.json: {e}")
        return False

def create_oauth_token_manually():
    """Create OAuth token manually without browser"""
    
    print("\n🔧 Manual OAuth Token Creation")
    print("=" * 40)
    
    print("📋 To create OAuth token manually:")
    print()
    print("1️⃣ On your LOCAL machine:")
    print("   • Download credentials.json from Google Cloud Console")
    print("   • Run: python3 oauth_ssh_tunnel_alt.py")
    print("   • This will create token.json on your local machine")
    print()
    print("2️⃣ Copy token.json to server:")
    print("   • scp token.json user@server:/opt/idotmatrix/")
    print("   • Or copy the contents manually")
    print()
    print("3️⃣ Test on server:")
    print("   • python3 fix_token_format.py")
    print()
    print("💡 Alternative: Use ICS calendar only (already working!)")
    print("   • python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")

def test_oauth_calendar():
    """Test OAuth calendar access"""
    
    print("\n🔧 Testing OAuth Calendar Access")
    print("=" * 40)
    
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Load credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Create service
        from googleapiclient.discovery import build
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
    
    print("🔧 OAuth Token Format Fix (No Browser)")
    print("=" * 50)
    
    # Try to fix existing token
    if fix_token_format():
        print("✅ OAuth token format fixed!")
        
        # Test OAuth calendar
        success, calendars = test_oauth_calendar()
        
        if success:
            print("✅ OAuth Calendar access working!")
            print("🚀 You can now use:")
            print("   ./run_oauth_calendar.sh DD:4F:93:46:DF:1A tomorrow")
        else:
            print("❌ OAuth Calendar test failed")
            create_oauth_token_manually()
    else:
        print("❌ OAuth token format fix failed")
        create_oauth_token_manually()

if __name__ == '__main__':
    main()
