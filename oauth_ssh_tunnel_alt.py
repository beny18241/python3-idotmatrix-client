#!/usr/bin/env python3
"""
OAuth SSH Tunnel Alternative
OAuth authentication with SSH tunneling using alternative port
"""

import os
import sys
import json
import webbrowser
import subprocess
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def find_available_port():
    """Find an available port for OAuth"""
    
    import socket
    
    # Try ports 8080-8090
    for port in range(8080, 8090):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', port))
            sock.close()
            return port
        except OSError:
            continue
    
    return None

def setup_ssh_tunnel_alt():
    """Setup SSH tunnel for OAuth authentication with alternative port"""
    
    print("🔧 SSH Tunnel OAuth Setup (Alternative Port)")
    print("=" * 60)
    
    # Find available port
    port = find_available_port()
    
    if not port:
        print("❌ No available ports found (8080-8090)")
        print("💡 Try killing processes using these ports")
        return None
    
    print(f"✅ Found available port: {port}")
    print()
    print("📋 To use OAuth on remote server, you need SSH tunneling:")
    print()
    print("1️⃣ From your LOCAL machine, run this command:")
    print(f"   ssh -L {port}:localhost:{port} your_username@your_server_ip")
    print()
    print("2️⃣ This creates a tunnel from your local port {port} to server port {port}")
    print("3️⃣ OAuth will use localhost:{port} on the server")
    print("4️⃣ Your browser will open on your LOCAL machine")
    print()
    print("💡 Example:")
    print(f"   ssh -L {port}:localhost:{port} user@192.168.1.100")
    print(f"   ssh -L {port}:localhost:{port} user@your-server.com")
    print()
    
    return port

def oauth_authentication_with_tunnel_alt(port):
    """OAuth authentication with SSH tunnel using alternative port"""
    
    print(f"\n🔐 Starting OAuth Authentication with SSH Tunnel (Port {port})")
    print("=" * 70)
    
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
    
    # Check if token.json exists and is valid
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            if creds.valid:
                print("✅ OAuth token is already valid")
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
        except Exception as e:
            print(f"❌ Error with existing OAuth token: {e}")
    
    # Get new OAuth credentials
    print("🔐 Starting OAuth authentication...")
    print("📋 This will open a browser on your LOCAL machine")
    print("📋 Make sure you have SSH tunnel running!")
    print()
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        # Use the available port for OAuth callback
        creds = flow.run_local_server(port=port)
        print("✅ OAuth authentication successful")
        
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("✅ OAuth token saved")
        
        return True
        
    except Exception as e:
        print(f"❌ OAuth authentication failed: {e}")
        print(f"💡 Make sure SSH tunnel is running:")
        print(f"   ssh -L {port}:localhost:{port} your_username@your_server_ip")
        return False

def test_oauth_calendar_with_tunnel_alt():
    """Test OAuth calendar access with tunnel"""
    
    print("\n🔧 Testing OAuth Calendar Access")
    print("=" * 50)
    
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Load credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Create service
        service = build('calendar', 'v3', credentials=creds)
        print("✅ Google Calendar API service created")
        
        # Get calendar list
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        print(f"📅 Found {len(calendars)} accessible calendars")
        
        if calendars:
            print("\n📋 Accessible Calendars:")
            for i, calendar in enumerate(calendars):
                calendar_id = calendar.get('id', 'Unknown')
                summary = calendar.get('summary', 'No Title')
                access_role = calendar.get('accessRole', 'Unknown')
                primary = calendar.get('primary', False)
                
                print(f"   {i+1}. {summary}")
                print(f"      ID: {calendar_id}")
                print(f"      Role: {access_role}")
                print(f"      Primary: {primary}")
                print()
        
        return True, calendars
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, []

def main():
    """Main function"""
    
    print("🔧 OAuth SSH Tunnel Setup (Alternative Port)")
    print("=" * 50)
    
    # Setup SSH tunnel with alternative port
    port = setup_ssh_tunnel_alt()
    
    if not port:
        print("❌ SSH tunnel setup failed")
        return
    
    # OAuth authentication
    if not oauth_authentication_with_tunnel_alt(port):
        print("❌ OAuth authentication failed")
        return
    
    # Test OAuth
    success, calendars = test_oauth_calendar_with_tunnel_alt()
    
    if success:
        print("✅ OAuth Calendar setup complete!")
        print("🚀 You can now use:")
        print("   ./run_oauth_calendar.sh DD:4F:93:46:DF:1A tomorrow")
    else:
        print("❌ OAuth Calendar test failed")
        print("Please check your OAuth credentials")

if __name__ == '__main__':
    main()
