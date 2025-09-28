#!/usr/bin/env python3
"""
Quick Commands Reference
Correct Python commands for the project
"""

def print_quick_commands():
    """Print quick commands reference"""
    
    print("🔧 Quick Commands Reference")
    print("=" * 40)
    
    print("📋 Use 'python3' instead of 'python' on this server")
    print()
    
    print("🔧 SSH Tunnel Setup:")
    print("1. On your LOCAL machine:")
    print("   ssh -L 8080:localhost:8080 your_username@your_server_ip")
    print()
    print("2. On the SERVER (with tunnel running):")
    print("   python3 oauth_ssh_tunnel.py")
    print()
    
    print("🔧 Test OAuth Calendar:")
    print("   python3 oauth_calendar_final.py DD:4F:93:46:DF:1A tomorrow")
    print("   python3 oauth_calendar_final.py DD:4F:93:46:DF:1A current")
    print("   python3 oauth_calendar_final.py DD:4F:93:46:DF:1A today")
    print()
    
    print("🔧 Test ICS Calendar:")
    print("   python3 test_ics_simple.py")
    print("   python3 combined_calendar_simple.py DD:4F:93:46:DF:1A tomorrow")
    print()
    
    print("🔧 Debug Commands:")
    print("   python3 debug_calendar_access.py")
    print("   python3 check_service_email.py")
    print("   python3 fix_calendar_sharing.py")
    print()
    
    print("💡 Remember:")
    print("   • Use 'python3' not 'python'")
    print("   • Keep SSH tunnel running during OAuth")
    print("   • OAuth token is saved on server")
    print("   • You only need to do OAuth once")

def main():
    """Main function"""
    
    print_quick_commands()

if __name__ == '__main__':
    main()
