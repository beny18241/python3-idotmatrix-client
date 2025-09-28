#!/usr/bin/env python3
"""
Copy OAuth from Local
Copy OAuth token from local machine to remote server
"""

import os
import json
import sys

def print_copy_instructions():
    """Print instructions for copying OAuth token from local machine"""
    
    print("🔧 Copy OAuth Token from Local Machine to Remote Server")
    print("=" * 60)
    
    print("📋 Since OAuth worked locally but not on remote server:")
    print()
    print("🔧 STEP 1: On your LOCAL machine")
    print("1. Find the token.json file (created when OAuth worked locally)")
    print("2. Copy it to the remote server")
    print()
    print("🔧 STEP 2: Copy methods")
    print("Method A - SCP:")
    print("   scp token.json user@server:/opt/idotmatrix/")
    print()
    print("Method B - Manual copy:")
    print("1. Open token.json on your local machine")
    print("2. Copy the contents")
    print("3. Create token.json on server with same contents")
    print()
    print("🔧 STEP 3: Test on server")
    print("   source venv/bin/activate && python3 oauth_calendar_final.py tomorrow")
    print()
    print("💡 Alternative: Use ICS calendar only (already working!)")
    print("   python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")

def check_local_token():
    """Check if local token exists"""
    
    print("\n🔧 Checking for Local OAuth Token")
    print("=" * 40)
    
    if os.path.exists('token.json'):
        print("✅ token.json found on server")
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
                print("💡 You need to copy the token from your local machine")
                return False
            
            print("✅ Token has all required OAuth fields")
            return True
            
        except Exception as e:
            print(f"❌ Error reading token.json: {e}")
            return False
    else:
        print("❌ No token.json found on server")
        print("💡 You need to copy the token from your local machine")
        return False

def test_oauth_token():
    """Test the OAuth token"""
    
    print("\n🔧 Testing OAuth Token")
    print("=" * 30)
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        
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
    
    print("🔧 Copy OAuth Token from Local Machine")
    print("=" * 50)
    
    # Check if local token exists
    if not check_local_token():
        print_copy_instructions()
        return
    
    # Test OAuth token
    if not test_oauth_token():
        print("❌ OAuth token test failed")
        print_copy_instructions()
        return
    
    print("✅ OAuth token is working!")
    print("🚀 You can now use:")
    print("   ./run_oauth_calendar_venv.sh DD:4F:93:46:DF:1A tomorrow")

if __name__ == '__main__':
    main()
