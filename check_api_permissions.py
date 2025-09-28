#!/usr/bin/env python3
"""
Check API permissions and service account setup
Simple check for common service account issues
"""

import os
import json

def check_api_permissions():
    """Check API permissions and service account setup"""
    
    print("🔍 API Permissions Check")
    print("=" * 40)
    
    # Check if service account file exists
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found!")
        return False
    
    print("✅ service-account.json exists")
    
    # Load service account data
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        client_email = service_account_data.get('client_email', '')
        project_id = service_account_data.get('project_id', '')
        
        print(f"📧 Service Account Email: {client_email}")
        print(f"🏗️  Project ID: {project_id}")
        
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")
        return False
    
    print("\n🔧 COMMON ISSUES AND SOLUTIONS:")
    print("=" * 40)
    print()
    print("❌ ISSUE 1: Google Calendar API not enabled")
    print("✅ SOLUTION:")
    print("1. Go to: https://console.cloud.google.com")
    print("2. Select your project:", project_id)
    print("3. Go to 'APIs & Services' > 'Library'")
    print("4. Search for 'Google Calendar API'")
    print("5. Click on 'Google Calendar API'")
    print("6. Click 'Enable'")
    print()
    print("❌ ISSUE 2: Service account has no roles")
    print("✅ SOLUTION:")
    print("1. Go to: https://console.cloud.google.com")
    print("2. Go to 'IAM & Admin' > 'IAM'")
    print("3. Find your service account:", client_email)
    print("4. Click the pencil icon to edit")
    print("5. Add role: 'Calendar API User'")
    print("6. Click 'Save'")
    print()
    print("❌ ISSUE 3: Calendar not properly shared")
    print("✅ SOLUTION:")
    print("1. Go to: https://calendar.google.com")
    print("2. Click gear icon > Settings")
    print("3. Go to 'Settings for my calendars'")
    print("4. Click on your calendar name")
    print("5. Click 'Share with specific people'")
    print("6. Remove the service account if it exists")
    print("7. Add it back:", client_email)
    print("8. Set permission to 'See all event details'")
    print("9. Click 'Send'")
    print()
    print("❌ ISSUE 4: Service account key is invalid")
    print("✅ SOLUTION:")
    print("1. Go to: https://console.cloud.google.com")
    print("2. Go to 'IAM & Admin' > 'Service Accounts'")
    print("3. Find your service account")
    print("4. Go to 'Keys' tab")
    print("5. Delete the old key")
    print("6. Create a new key (JSON)")
    print("7. Download and replace service-account.json")
    print()
    print("⏳ IMPORTANT: Wait 10-15 minutes after making changes")
    print("Then test with: python diagnose_calendar.py")
    print()
    print("🎯 QUICK LINKS:")
    print("-" * 20)
    print("• Google Cloud Console: https://console.cloud.google.com")
    print("• APIs & Services: https://console.cloud.google.com/apis/library")
    print("• IAM & Admin: https://console.cloud.google.com/iam-admin/iam")
    print("• Google Calendar: https://calendar.google.com")
    print()
    print("📧 Service Account Email to Check:")
    print(f"   {client_email}")

def main():
    """Main function"""
    check_api_permissions()

if __name__ == '__main__':
    main()
