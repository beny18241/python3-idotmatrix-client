#!/usr/bin/env python3
"""
Fix OAuth NOW
Actually fix the OAuth token issue properly
"""

import os
import json
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def delete_broken_token():
    """Delete the broken OAuth token"""
    
    print("🔧 Deleting Broken OAuth Token")
    print("=" * 40)
    
    if os.path.exists('token.json'):
        os.remove('token.json')
        print("✅ Deleted broken token.json")
    else:
        print("❌ No token.json found")

def create_fresh_oauth_token():
    """Create a fresh OAuth token"""
    
    print("\n🔧 Creating Fresh OAuth Token")
    print("=" * 40)
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("📋 Please download OAuth credentials from Google Cloud Console:")
        print("1. Go to: https://console.cloud.google.com/apis/credentials")
        print("2. Click 'Create Credentials' > 'OAuth client ID'")
        print("3. Choose 'Desktop application'")
        print("4. Name it 'iDotMatrix Calendar'")
        print("5. Download the JSON file as 'credentials.json'")
        print("6. Upload it to the server")
        return False
    
    print("✅ credentials.json found")
    
    # Create new OAuth token
    print("🔐 Creating new OAuth token...")
    print("📋 This will require browser authentication")
    print("💡 Make sure you have SSH tunnel running if on remote server")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        # Try different ports
        ports = [8080, 8081, 8082, 8083, 8084, 8085]
        
        for port in ports:
            try:
                print(f"🔄 Trying port {port}...")
                creds = flow.run_local_server(port=port)
                print(f"✅ OAuth authentication successful on port {port}")
                
                # Save credentials
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                print("✅ OAuth token saved")
                
                return True
                
            except Exception as e:
                print(f"❌ Port {port} failed: {e}")
                continue
        
        print("❌ All ports failed")
        return False
        
    except Exception as e:
        print(f"❌ OAuth authentication failed: {e}")
        return False

def test_oauth_token():
    """Test the OAuth token"""
    
    print("\n🔧 Testing OAuth Token")
    print("=" * 30)
    
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Load credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
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
        print(f"❌ Error testing OAuth token: {e}")
        return False

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
    
    print("🔧 Fix OAuth NOW - Complete Solution")
    print("=" * 50)
    
    # Delete broken token
    delete_broken_token()
    
    # Create fresh OAuth token
    if not create_fresh_oauth_token():
        print("❌ OAuth token creation failed")
        print("💡 Use ICS calendar only (already working!):")
        print("   python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")
        return
    
    # Test OAuth token
    if not test_oauth_token():
        print("❌ OAuth token test failed")
        return
    
    # Test OAuth calendar
    success, calendars = test_oauth_calendar()
    
    if success:
        print("✅ OAuth Calendar access working!")
        print("🚀 You can now use:")
        print("   ./run_oauth_calendar_venv.sh DD:4F:93:46:DF:1A tomorrow")
    else:
        print("❌ OAuth Calendar test failed")
        print("💡 Use ICS calendar only (already working!):")
        print("   python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")

if __name__ == '__main__':
    main()
