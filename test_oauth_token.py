#!/usr/bin/env python3
"""
Test OAuth token format
Verifies that the OAuth token has all required fields
"""

import os
import json

def test_oauth_token():
    """Test OAuth token format"""
    
    print("🔧 Testing OAuth Token Format")
    print("=" * 40)
    
    # Check if token.json exists
    if not os.path.exists('token.json'):
        print("❌ Token file not found!")
        return False
    
    try:
        # Load token.json
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        
        print("✅ Token file loaded")
        
        # Check required fields
        required_fields = ['token', 'refresh_token', 'client_id', 'client_secret', 'token_uri']
        missing_fields = []
        
        for field in required_fields:
            if field not in token_data:
                missing_fields.append(field)
            else:
                print(f"✅ {field}: {str(token_data[field])[:20]}...")
        
        if missing_fields:
            print(f"❌ Missing fields: {', '.join(missing_fields)}")
            return False
        else:
            print("✅ All required fields present")
            return True
        
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

def main():
    """Main function"""
    if test_oauth_token():
        print()
        print("🎉 OAuth token is properly formatted!")
        print("Now you can use on your server:")
        print("  python calendar_display_oauth.py tomorrow")
    else:
        print()
        print("❌ OAuth token is missing required fields")
        print("Please run: python fix_oauth_token.py")

if __name__ == '__main__':
    main()
