#!/usr/bin/env python3
"""
Step-by-step guide to create new OAuth credentials
"""

def create_new_oauth_guide():
    """Guide for creating new OAuth credentials"""
    
    print("🔧 Step-by-Step OAuth Credentials Creation")
    print("=" * 50)
    print()
    print("The issue is that your OAuth client is configured for 'n8n'")
    print("but we need it for 'iDotMatrix'. Here's how to fix it:")
    print()
    
    print("📋 Step 1: Go to Google Cloud Console")
    print("   URL: https://console.cloud.google.com/")
    print("   - Sign in with your Google account")
    print("   - Select your project (or create a new one)")
    print()
    
    print("📋 Step 2: Create New OAuth Client")
    print("   1. Go to 'APIs & Services' > 'Credentials'")
    print("   2. Click 'Create Credentials' > 'OAuth client ID'")
    print("   3. Choose 'Desktop application'")
    print("   4. Name it 'iDotMatrix Calendar' (NOT n8n)")
    print("   5. Click 'Create'")
    print("   6. Download the JSON file")
    print("   7. Save it as 'credentials.json' in your project")
    print()
    
    print("📋 Step 3: Configure OAuth Consent Screen")
    print("   1. Go to 'APIs & Services' > 'OAuth consent screen'")
    print("   2. Choose 'External'")
    print("   3. Fill in required fields:")
    print("      - App name: 'iDotMatrix Calendar'")
    print("      - User support email: your email")
    print("      - Developer contact: your email")
    print("   4. Add your email to test users")
    print("   5. Save and continue")
    print()
    
    print("📋 Step 4: Enable Google Calendar API")
    print("   1. Go to 'APIs & Services' > 'Library'")
    print("   2. Search for 'Google Calendar API'")
    print("   3. Click on it and press 'Enable'")
    print()
    
    print("📋 Step 5: Test the New Credentials")
    print("   After creating new credentials:")
    print("   1. Replace your current 'credentials.json' with the new one")
    print("   2. Run: python calendar_auth_final.py")
    print("   3. The authentication should work without 'n8n' errors")
    print()
    
    print("🔧 Alternative: Create New Google Cloud Project")
    print("   If the above doesn't work:")
    print("   1. Create a completely new Google Cloud project")
    print("   2. Enable Google Calendar API")
    print("   3. Create OAuth credentials")
    print("   4. Use the new project's credentials")
    print()
    
    print("✅ Expected Results:")
    print("   - No more 'n8n's request is invalid' errors")
    print("   - Successful authentication")
    print("   - Calendar access working")
    print("   - iDotMatrix display showing calendar info")
    print()
    
    print("🚀 Ready to create new OAuth credentials?")
    print("   Follow the steps above, then run:")
    print("   python calendar_auth_final.py")

def main():
    """Main function"""
    create_new_oauth_guide()

if __name__ == '__main__':
    main()
