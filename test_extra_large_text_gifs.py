#!/usr/bin/env python3
"""
Test script to demonstrate the new emoji GIFs with EXTRA LARGE text overlays
"""

import os
import subprocess
from config import DEVICE_ADDRESS

def test_extra_large_text_overlay_gifs():
    """Test the new emoji GIFs with extra large, very visible text overlays"""
    
    print("🎬 Testing emoji GIFs with EXTRA LARGE text overlays...")
    print("=" * 60)
    
    # Check if GIFs exist
    gifs = [
        "images/free_emoji_with_large_text.gif",
        "images/busy_emoji_with_large_text.gif", 
        "images/error_emoji_with_large_text.gif"
    ]
    
    for gif in gifs:
        if os.path.exists(gif):
            print(f"✅ Found: {gif}")
        else:
            print(f"❌ Missing: {gif}")
            return False
    
    print("\n🎯 Testing each GIF with EXTRA LARGE text on your iDotMatrix device...")
    print("💡 The text should now be MUCH larger and more visible!")
    
    # Test FREE GIF
    print("\n1️⃣ Testing FREE emoji with extra large 'FREE' text...")
    cmd = [
        "./run_in_venv.sh",
        "--address", DEVICE_ADDRESS,
        "--set-gif", "images/free_emoji_with_large_text.gif"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ FREE emoji with extra large text displayed successfully!")
    else:
        print(f"❌ Error displaying FREE emoji: {result.stderr}")
    
    input("Press Enter to continue to CALL emoji test...")
    
    # Test CALL GIF
    print("\n2️⃣ Testing CALL emoji with extra large 'CALL' text...")
    cmd = [
        "./run_in_venv.sh",
        "--address", DEVICE_ADDRESS,
        "--set-gif", "images/busy_emoji_with_large_text.gif"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ CALL emoji with extra large text displayed successfully!")
    else:
        print(f"❌ Error displaying CALL emoji: {result.stderr}")
    
    input("Press Enter to continue to ERROR emoji test...")
    
    # Test ERROR GIF
    print("\n3️⃣ Testing ERROR emoji with extra large 'ERROR' text...")
    cmd = [
        "./run_in_venv.sh",
        "--address", DEVICE_ADDRESS,
        "--set-gif", "images/error_emoji_with_large_text.gif"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ ERROR emoji with extra large text displayed successfully!")
    else:
        print(f"❌ Error displaying ERROR emoji: {result.stderr}")
    
    print("\n🎉 All extra large text overlay GIFs tested!")
    print("\n💡 Your calendar scheduler will now use these enhanced GIFs with EXTRA LARGE text:")
    print("   • FREE status: Green checkmark with extra large 'FREE' text")
    print("   • BUSY status: Red X with extra large 'CALL' text") 
    print("   • ERROR status: Orange warning with extra large 'ERROR' text")
    print("\n🔍 The text should now be MUCH more visible on your iDotMatrix display!")
    print("📏 Each letter is now drawn as 3x3 pixel blocks for maximum visibility!")

if __name__ == "__main__":
    test_extra_large_text_overlay_gifs()
