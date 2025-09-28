#!/usr/bin/env python3
"""
Regenerate OAuth Token
Create a fresh OAuth token for the remote server
"""

import os
import json
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def check_credentials():
    """Check if credentials.json exists"""
    
    print("1️⃣ Checking OAuth credentials...")
    
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("📋 Please download OAuth credentials from Google Cloud Console:")
        print()
        print("🔧 Steps to get credentials.json:")
        print("1. Go to: https://console.cloud.google.com/apis/credentials")
        print("2. Click 'Create Credentials' > 'OAuth client ID'")
        print("3. Choose 'Desktop application'")
        print("4. Name it 'iDotMatrix Calendar'")
        print("5. Download the JSON file as 'credentials.json'")
        print("6. Upload it to the server")
        print()
        return False
    
    print("✅ credentials.json found")
    return True

def create_oauth_token_manual():
    """Create OAuth token manually"""
    
    print("\n2️⃣ Creating OAuth Token Manually")
    print("=" * 40)
    
    print("📋 Since we can't use browser on remote server, here's how to create OAuth token:")
    print()
    print("🔧 Method 1: Use SSH Tunnel (Recommended)")
    print("1. On your LOCAL machine, run:")
    print("   ssh -L 8081:localhost:8081 your_username@your_server_ip")
    print()
    print("2. On the SERVER (with tunnel running), run:")
    print("   python3 oauth_ssh_tunnel_alt.py")
    print()
    print("3. This will open browser on your LOCAL machine")
    print("4. Authenticate with Google")
    print("5. Token will be saved on the server")
    print()
    
    print("🔧 Method 2: Create on Local Machine")
    print("1. On your LOCAL machine:")
    print("   • Download credentials.json from Google Cloud Console")
    print("   • Run: python3 oauth_ssh_tunnel_alt.py")
    print("   • This creates token.json on your local machine")
    print()
    print("2. Copy token.json to server:")
    print("   scp token.json user@server:/opt/idotmatrix/")
    print()
    
    print("🔧 Method 3: Use ICS Calendar Only (Already Working!)")
    print("Since your ICS calendar is working perfectly:")
    print("   python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")
    print()

def create_oauth_token_automated():
    """Create OAuth token with automated flow"""
    
    print("\n3️⃣ Automated OAuth Token Creation")
    print("=" * 40)
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    try:
        print("🔐 Starting OAuth authentication...")
        print("📋 This will try to open a browser (may not work on remote server)")
        
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        # Try different ports
        ports = [8081, 8082, 8083, 8084, 8085]
        
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
    
    print("\n4️⃣ Testing OAuth Token")
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
    
    print("🔧 Regenerate OAuth Token")
    print("=" * 30)
    
    # Check credentials
    if not check_credentials():
        return
    
    # Show manual methods
    create_oauth_token_manual()
    
    # Try automated creation
    print("🔄 Trying automated OAuth creation...")
    if create_oauth_token_automated():
        print("✅ OAuth token created successfully!")
        
        # Test the token
        if test_oauth_token():
            print("✅ OAuth token is working!")
            print("🚀 You can now use:")
            print("   ./run_oauth_calendar.sh DD:4F:93:46:DF:1A tomorrow")
        else:
            print("❌ OAuth token test failed")
    else:
        print("❌ Automated OAuth creation failed")
        print("💡 Use one of the manual methods above")

if __name__ == '__main__':
    main()
