#!/usr/bin/env python3
"""
Fix OAuth Token
Fix OAuth token format for remote server
"""

import os
import json
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def fix_oauth_token():
    """Fix OAuth token for remote server"""
    
    print("🔧 Fixing OAuth Token for Remote Server")
    print("=" * 50)
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("Please download OAuth credentials from Google Cloud Console:")
        print("1. Go to: https://console.cloud.google.com/apis/credentials")
        print("2. Click 'Create Credentials' > 'OAuth client ID'")
        print("3. Choose 'Desktop application'")
        print("4. Download the JSON file as 'credentials.json'")
        return False
    
    print("✅ credentials.json found")
    
    # Check existing token
    if os.path.exists('token.json'):
        print("📋 Found existing token.json")
        try:
            with open('token.json', 'r') as f:
                token_data = json.load(f)
            
            print("📋 Current token structure:")
            for key in token_data.keys():
                print(f"   {key}: {'✅' if token_data[key] else '❌'}")
            
            # Check if it's a service account token (wrong type)
            if 'client_email' in token_data:
                print("❌ This appears to be a service account token, not OAuth token")
                print("💡 We need to create a proper OAuth token")
                os.remove('token.json')
                print("🗑️ Removed incorrect token.json")
            
        except Exception as e:
            print(f"❌ Error reading token.json: {e}")
            os.remove('token.json')
            print("🗑️ Removed corrupted token.json")
    
    # Create new OAuth token
    print("\n🔐 Creating new OAuth token...")
    print("📋 This will require browser authentication")
    print("💡 Make sure you have SSH tunnel running if on remote server")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        # Use port 8081 (alternative port)
        creds = flow.run_local_server(port=8081)
        print("✅ OAuth authentication successful")
        
        # Save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("✅ OAuth token saved")
        
        # Verify token structure
        print("\n📋 New token structure:")
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        
        for key in token_data.keys():
            print(f"   {key}: {'✅' if token_data[key] else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ OAuth authentication failed: {e}")
        print("💡 Make sure SSH tunnel is running:")
        print("   ssh -L 8081:localhost:8081 your_username@your_server_ip")
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

def main():
    """Main function"""
    
    print("🔧 OAuth Token Fix for Remote Server")
    print("=" * 40)
    
    # Fix OAuth token
    if not fix_oauth_token():
        print("❌ OAuth token fix failed")
        return
    
    # Test OAuth token
    if not test_oauth_token():
        print("❌ OAuth token test failed")
        return
    
    print("\n✅ OAuth token fix complete!")
    print("🚀 You can now use:")
    print("   ./run_oauth_calendar.sh DD:4F:93:46:DF:1A tomorrow")

if __name__ == '__main__':
    main()