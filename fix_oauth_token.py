#!/usr/bin/env python3
"""
Fix OAuth token format
Adds missing fields to token.json for proper OAuth authentication
"""

import os
import json

def fix_oauth_token():
    """Fix OAuth token format"""
    
    print("🔧 Fixing OAuth Token Format")
    print("=" * 40)
    
    # Check if token.json exists
    if not os.path.exists('token.json'):
        print("❌ Token file not found!")
        print("Please run: python calendar_service_account.py")
        return False
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ Credentials file not found!")
        print("Please make sure credentials.json exists")
        return False
    
    try:
        # Load token.json
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        
        # Load credentials.json
        with open('credentials.json', 'r') as f:
            credentials_data = json.load(f)
        
        print("✅ Found token.json and credentials.json")
        
        # Extract client_id and client_secret from credentials
        if 'installed' in credentials_data:
            client_id = credentials_data['installed']['client_id']
            client_secret = credentials_data['installed']['client_secret']
        elif 'web' in credentials_data:
            client_id = credentials_data['web']['client_id']
            client_secret = credentials_data['web']['client_secret']
        else:
            print("❌ Could not find client_id and client_secret in credentials.json")
            return False
        
        print(f"📧 Client ID: {client_id}")
        print(f"🔑 Client Secret: {client_secret[:10]}...")
        
        # Add missing fields to token.json
        token_data['client_id'] = client_id
        token_data['client_secret'] = client_secret
        
        # Save fixed token.json
        with open('token.json', 'w') as f:
            json.dump(token_data, f, indent=2)
        
        print("✅ Fixed token.json with missing fields")
        print()
        print("🧪 Testing OAuth authentication...")
        
        # Test the fixed token
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            credentials = Credentials.from_authorized_user_file('token.json')
            service = build('calendar', 'v3', credentials=credentials)
            
            # Test calendar access
            calendar_list = service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            print(f"✅ OAuth authentication working!")
            print(f"📅 Found {len(calendars)} accessible calendars")
            
            if calendars:
                print("📋 Accessible calendars:")
                for calendar in calendars:
                    summary = calendar.get('summary', 'No Title')
                    access_role = calendar.get('accessRole', '')
                    print(f"  - {summary} ({access_role})")
            
            return True
            
        except Exception as e:
            print(f"❌ OAuth authentication failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error fixing OAuth token: {e}")
        return False

def main():
    """Main function"""
    if fix_oauth_token():
        print()
        print("🎉 OAuth token fixed!")
        print("Now you can use:")
        print("  python calendar_display_oauth.py tomorrow")
    else:
        print()
        print("❌ Failed to fix OAuth token")
        print("Please check your credentials.json file")

if __name__ == '__main__':
    main()
