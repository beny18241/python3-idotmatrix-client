#!/usr/bin/env python3
"""
Use Personal Configuration

This script copies your personal configuration to config.py
so you can use your real settings while keeping them private.
"""

import shutil
import os

def use_personal_config():
    """Copy personal config to main config"""
    
    print("🔧 Using Personal Configuration")
    print("=" * 40)
    
    # Check if personal config exists
    if not os.path.exists("config_personal.py"):
        print("❌ config_personal.py not found!")
        print("   Please create config_personal.py with your settings")
        return False
    
    # Backup current config if it exists
    if os.path.exists("config.py"):
        print("📁 Backing up current config.py to config_backup.py")
        shutil.copy2("config.py", "config_backup.py")
    
    # Copy personal config to main config
    try:
        shutil.copy2("config_personal.py", "config.py")
        print("✅ Personal configuration copied to config.py")
        print("🚀 You can now use:")
        print("   python3 ics_only_solution.py tomorrow")
        print("   python3 ics_only_solution.py current")
        print("   python3 ics_only_solution.py today")
        return True
        
    except Exception as e:
        print(f"❌ Error copying config: {e}")
        return False

def restore_default_config():
    """Restore default configuration"""
    
    print("🔧 Restoring Default Configuration")
    print("=" * 40)
    
    if os.path.exists("config_backup.py"):
        try:
            shutil.copy2("config_backup.py", "config.py")
            print("✅ Default configuration restored")
            return True
        except Exception as e:
            print(f"❌ Error restoring config: {e}")
            return False
    else:
        print("❌ No backup configuration found")
        return False

def main():
    """Main function"""
    
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "restore":
        restore_default_config()
    else:
        use_personal_config()

if __name__ == "__main__":
    main()
