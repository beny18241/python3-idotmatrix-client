#!/usr/bin/env python3
"""
Test script to demonstrate the new emoji GIFs with text overlays
"""

import os
import subprocess
from config import DEVICE_ADDRESS

def test_text_overlay_gifs():
    """Test the new emoji GIFs with text overlays"""
    
    print("🎬 Testing emoji GIFs with text overlays...")
    
    # Check if GIFs exist
    gifs = [
        "images/free_emoji_with_text.gif",
        "images/busy_emoji_with_text.gif", 
        "images/error_emoji_with_text.gif"
    ]
    
    for gif in gifs:
        if os.path.exists(gif):
            print(f"✅ Found: {gif}")
        else:
            print(f"❌ Missing: {gif}")
            return False
    
    print("\n🎯 Testing each GIF on your iDotMatrix device...")
    
    # Test FREE GIF
    print("\n1️⃣ Testing FREE emoji with 'FREE' text...")
    cmd = [
        "./run_in_venv.sh",
        "--address", DEVICE_ADDRESS,
        "--set-gif", "images/free_emoji_with_text.gif"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ FREE emoji with text displayed successfully!")
    else:
        print(f"❌ Error displaying FREE emoji: {result.stderr}")
    
    input("Press Enter to continue to CALL emoji test...")
    
    # Test CALL GIF
    print("\n2️⃣ Testing CALL emoji with 'CALL' text...")
    cmd = [
        "./run_in_venv.sh",
        "--address", DEVICE_ADDRESS,
        "--set-gif", "images/busy_emoji_with_text.gif"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ CALL emoji with text displayed successfully!")
    else:
        print(f"❌ Error displaying CALL emoji: {result.stderr}")
    
    input("Press Enter to continue to ERROR emoji test...")
    
    # Test ERROR GIF
    print("\n3️⃣ Testing ERROR emoji with 'ERROR' text...")
    cmd = [
        "./run_in_venv.sh",
        "--address", DEVICE_ADDRESS,
        "--set-gif", "images/error_emoji_with_text.gif"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ ERROR emoji with text displayed successfully!")
    else:
        print(f"❌ Error displaying ERROR emoji: {result.stderr}")
    
    print("\n🎉 All text overlay GIFs tested!")
    print("\n💡 Your calendar scheduler will now use these enhanced GIFs with text overlays:")
    print("   • FREE status: Green checkmark with 'FREE' text")
    print("   • BUSY status: Red X with 'CALL' text") 
    print("   • ERROR status: Orange warning with 'ERROR' text")

if __name__ == "__main__":
    test_text_overlay_gifs()
