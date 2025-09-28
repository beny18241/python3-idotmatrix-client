#!/usr/bin/env python3
"""
Fix Server OAuth Token
Fix OAuth token format on remote server
"""

import os
import json
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def check_token_format():
    """Check the current token format"""
    
    print("🔧 Checking OAuth Token Format on Server")
    print("=" * 50)
    
    if not os.path.exists('token.json'):
        print("❌ token.json not found on server")
        return False
    
    try:
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        
        print("📋 Current token structure:")
        for key in token_data.keys():
            print(f"   {key}: {'✅' if token_data[key] else '❌'}")
        
        # Check for required OAuth fields
        required_fields = ['token', 'refresh_token', 'client_id', 'client_secret']
        missing_fields = [field for field in required_fields if field not in token_data]
        
        if missing_fields:
            print(f"❌ Missing required OAuth fields: {missing_fields}")
            return False
        
        print("✅ Token has all required OAuth fields")
        return True
        
    except Exception as e:
        print(f"❌ Error reading token.json: {e}")
        return False

def fix_token_format():
    """Fix the OAuth token format"""
    
    print("\n🔧 Fixing OAuth Token Format")
    print("=" * 40)
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    try:
        # Load existing token
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        
        # Check if it's a service account token
        if 'client_email' in token_data:
            print("❌ This is a service account token, not OAuth token")
            print("💡 We need to create a proper OAuth token")
            return False
        
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
        print(f"❌ Error: {e}")
        return False

def create_proper_oauth_token():
    """Create proper OAuth token on server"""
    
    print("\n🔧 Creating Proper OAuth Token on Server")
    print("=" * 50)
    
    print("📋 The server has an incomplete OAuth token")
    print("💡 We need to create a proper OAuth token")
    print()
    print("🔧 Solutions:")
    print()
    print("1️⃣ Copy OAuth token from your LOCAL machine:")
    print("   • Find token.json on your local machine")
    print("   • Copy it to the server: scp token.json user@server:/opt/idotmatrix/")
    print()
    print("2️⃣ Create new OAuth token with SSH tunnel:")
    print("   • On LOCAL machine: ssh -L 8081:localhost:8081 user@server")
    print("   • On SERVER: python3 oauth_ssh_tunnel_alt.py")
    print()
    print("3️⃣ Use ICS calendar only (already working!):")
    print("   • python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")
    print()
    print("💡 Recommendation: Use ICS calendar since it's working perfectly!")

def main():
    """Main function"""
    
    print("🔧 Fix Server OAuth Token")
    print("=" * 30)
    
    # Check token format
    if not check_token_format():
        print("❌ Token format check failed")
        create_proper_oauth_token()
        return
    
    # Try to fix token format
    if fix_token_format():
        print("✅ OAuth token format fixed!")
        print("🚀 You can now use:")
        print("   ./run_oauth_with_venv.sh DD:4F:93:46:DF:1A tomorrow")
    else:
        print("❌ OAuth token format fix failed")
        create_proper_oauth_token()

if __name__ == '__main__':
    main()
