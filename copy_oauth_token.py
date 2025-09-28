#!/usr/bin/env python3
"""
Copy OAuth Token
Guide for copying OAuth token from local machine to server
"""

def print_copy_guide():
    """Print guide for copying OAuth token"""
    
    print("🔧 Copy OAuth Token from Local Machine")
    print("=" * 50)
    
    print("📋 Since OAuth was working with tunnel before, copy the token:")
    print()
    print("1️⃣ On your LOCAL machine:")
    print("   • Go to the directory where you ran OAuth")
    print("   • Find the token.json file")
    print("   • Copy it to the server")
    print()
    print("2️⃣ Copy methods:")
    print("   Method 1 - SCP:")
    print("   scp token.json user@server:/opt/idotmatrix/")
    print()
    print("   Method 2 - Manual copy:")
    print("   • Open token.json on local machine")
    print("   • Copy the contents")
    print("   • Create token.json on server with same contents")
    print()
    print("3️⃣ Test on server:")
    print("   python3 fix_token_format.py")
    print()
    print("💡 Alternative: Use ICS calendar only (already working!)")
    print("   python3 ics_only_solution.py DD:4F:93:46:DF:1A tomorrow")

def main():
    """Main function"""
    
    print_copy_guide()

if __name__ == '__main__':
    main()
