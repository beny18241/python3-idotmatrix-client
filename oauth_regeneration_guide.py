#!/usr/bin/env python3
"""
OAuth Regeneration Guide
Step-by-step guide for regenerating OAuth token
"""

def print_regeneration_guide():
    """Print OAuth regeneration guide"""
    
    print("🔧 OAuth Token Regeneration Guide")
    print("=" * 50)
    
    print("📋 Since you can't find any existing tokens, let's create a fresh one:")
    print()
    
    print("🔧 STEP 1: Get OAuth Credentials")
    print("1. Go to: https://console.cloud.google.com/apis/credentials")
    print("2. Click 'Create Credentials' > 'OAuth client ID'")
    print("3. Choose 'Desktop application'")
    print("4. Name it 'iDotMatrix Calendar'")
    print("5. Download the JSON file as 'credentials.json'")
    print("6. Upload it to the server")
    print()
    
    print("🔧 STEP 2: Create OAuth Token")
    print("Method A - SSH Tunnel (Recommended):")
    print("1. On your LOCAL machine:")
    print("   ssh -L 8081:localhost:8081 your_username@your_server_ip")
    print()
    print("2. On the SERVER (with tunnel running):")
    print("   python3 oauth_ssh_tunnel_alt.py")
    print()
    print("3. Browser will open on your LOCAL machine")
    print("4. Authenticate with Google")
    print("5. Token will be saved on the server")
    print()
    
    print("Method B - Create on Local Machine:")
    print("1. On your LOCAL machine:")
    print("   • Download credentials.json")
    print("   • Run: python3 oauth_ssh_tunnel_alt.py")
    print("   • This creates token.json")
    print()
    print("2. Copy token.json to server:")
    print("   scp token.json user@server:/opt/idotmatrix/")
    print()
    
    print("🔧 STEP 3: Test OAuth Token")
    print("python3 fix_token_format.py")
    print()
    
    print("🔧 STEP 4: Use OAuth Calendar")
    print("./run_oauth_calendar.sh DD:4F:93:46:DF:1A tomorrow")
    print()
    
    print("💡 Alternative: Use ICS Calendar Only (Already Working!)")
    print("Since your ICS calendar is working perfectly:")
    print("   python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")
    print()
    
    print("🎯 Quick Commands:")
    print("   python3 regenerate_oauth_token.py")
    print("   python3 oauth_ssh_tunnel_alt.py")
    print("   python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")

def main():
    """Main function"""
    
    print_regeneration_guide()

if __name__ == '__main__':
    main()
