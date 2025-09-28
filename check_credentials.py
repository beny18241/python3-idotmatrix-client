#!/usr/bin/env python3
"""
Check and diagnose Google OAuth credentials
"""

import json
import os

def check_credentials():
    """Check the structure of credentials.json"""
    
    credentials_file = 'credentials.json'
    
    if not os.path.exists(credentials_file):
        print("❌ credentials.json not found!")
        return
    
    print("🔍 Analyzing credentials.json...")
    print("=" * 40)
    
    try:
        with open(credentials_file, 'r') as f:
            client_config = json.load(f)
        
        print("📋 Credentials structure:")
        for key in client_config.keys():
            print(f"  ✅ {key}")
        
        print("\n🔍 Detailed analysis:")
        
        # Check for installed app
        if 'installed' in client_config:
            print("✅ Found 'installed' section (Desktop application)")
            installed = client_config['installed']
            print(f"  Client ID: {installed.get('client_id', 'Not found')}")
            print(f"  Redirect URIs: {installed.get('redirect_uris', 'Not found')}")
            
        # Check for web app
        if 'web' in client_config:
            print("✅ Found 'web' section (Web application)")
            web = client_config['web']
            print(f"  Client ID: {web.get('client_id', 'Not found')}")
            print(f"  Redirect URIs: {web.get('redirect_uris', 'Not found')}")
        
        # Check for other sections
        other_sections = [key for key in client_config.keys() if key not in ['installed', 'web']]
        if other_sections:
            print(f"⚠️  Other sections found: {other_sections}")
        
        print("\n🔧 Recommendations:")
        
        if 'installed' in client_config:
            print("  ✅ Use: python calendar_auth_fixed.py")
        elif 'web' in client_config:
            print("  ✅ Use: python calendar_auth_web.py")
        else:
            print("  ❌ Unknown credentials format")
            print("  🔧 Create new OAuth credentials in Google Cloud Console")
            print("  🔧 Choose 'Desktop application' for easier setup")
        
    except Exception as e:
        print(f"❌ Error reading credentials: {e}")

if __name__ == '__main__':
    check_credentials()
