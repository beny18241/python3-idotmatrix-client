#!/usr/bin/env python3
"""
SSH Tunnel Guide
Step-by-step guide for SSH tunneling OAuth authentication
"""

def print_ssh_tunnel_guide():
    """Print SSH tunnel guide"""
    
    print("🔧 SSH Tunnel Guide for OAuth Authentication")
    print("=" * 60)
    
    print("📋 Problem: Remote server has no browser for OAuth authentication")
    print("💡 Solution: SSH tunneling to use your local browser")
    print()
    
    print("1️⃣ On your LOCAL machine, run this command:")
    print("   ssh -L 8080:localhost:8080 your_username@your_server_ip")
    print()
    print("   Example:")
    print("   ssh -L 8080:localhost:8080 user@192.168.1.100")
    print("   ssh -L 8080:localhost:8080 user@your-server.com")
    print()
    
    print("2️⃣ This creates a tunnel:")
    print("   • Local port 8080 → Server port 8080")
    print("   • OAuth uses localhost:8080 on server")
    print("   • Browser opens on your LOCAL machine")
    print()
    
    print("3️⃣ On the SERVER, run OAuth setup:")
    print("   python oauth_ssh_tunnel.py")
    print()
    
    print("4️⃣ What happens:")
    print("   • OAuth opens browser on your LOCAL machine")
    print("   • You authenticate with Google")
    print("   • Token is saved on the SERVER")
    print("   • You can now use OAuth calendar access")
    print()
    
    print("5️⃣ Test the setup:")
    print("   python oauth_calendar_final.py DD:4F:93:46:DF:1A tomorrow")
    print()
    
    print("💡 Tips:")
    print("   • Keep the SSH tunnel running during OAuth")
    print("   • You can close the tunnel after OAuth is complete")
    print("   • The OAuth token is saved on the server")
    print("   • You only need to do this once")
    print()
    
    print("🔧 Alternative: Manual OAuth")
    print("   If SSH tunneling doesn't work, you can:")
    print("   1. Run OAuth on your local machine")
    print("   2. Copy the token.json file to the server")
    print("   3. Use the token on the server")

def main():
    """Main function"""
    
    print_ssh_tunnel_guide()

if __name__ == '__main__':
    main()
