#!/usr/bin/env python3
"""
Quick ICS Calendar Test
Quick test to check ICS calendar update frequency
"""

import requests
import hashlib
import datetime

def quick_ics_test():
    """Quick test of ICS calendar update frequency"""
    
    print("🔍 Quick ICS Calendar Update Test")
    print("=" * 40)
    
    ics_url = "https://outlook.office365.com/owa/calendar/144d73fdf2654fb3b92983ee16e9d0b3@genpt.com/e829a99fc26b4c66a482420d04ea689513863417029725141930/calendar.ics"
    
    try:
        # Get initial state
        print("1️⃣ Getting initial calendar state...")
        response1 = requests.get(ics_url)
        response1.raise_for_status()
        
        hash1 = hashlib.md5(response1.text.encode()).hexdigest()
        event_count1 = response1.text.count('BEGIN:VEVENT')
        
        print(f"✅ Initial state: {event_count1} events, hash: {hash1[:16]}...")
        
        # Wait 5 minutes
        print("\n2️⃣ Waiting 5 minutes to check for updates...")
        print("   (This will help determine update frequency)")
        
        import time
        time.sleep(5 * 60)  # Wait 5 minutes
        
        # Get updated state
        print("3️⃣ Checking for updates...")
        response2 = requests.get(ics_url)
        response2.raise_for_status()
        
        hash2 = hashlib.md5(response2.text.encode()).hexdigest()
        event_count2 = response2.text.count('BEGIN:VEVENT')
        
        print(f"✅ Updated state: {event_count2} events, hash: {hash2[:16]}...")
        
        # Compare
        if hash1 == hash2:
            print("📝 No changes detected in 5 minutes")
            print("💡 This suggests:")
            print("   • Calendar updates less frequently than 5 minutes")
            print("   • Or no events were added/changed during this time")
            print("   • Calendar source is stable")
        else:
            print("🔄 Changes detected in 5 minutes!")
            print(f"   📊 Events: {event_count1} → {event_count2} ({event_count2 - event_count1:+d})")
            print("💡 This suggests:")
            print("   • Calendar updates frequently (every 5 minutes or less)")
            print("   • Real-time or near real-time updates")
            print("   • High activity calendar source")
        
        print(f"\n📋 Summary:")
        print(f"   ⏰ Test duration: 5 minutes")
        print(f"   🔄 Changes detected: {'Yes' if hash1 != hash2 else 'No'}")
        print(f"   📅 Event count: {event_count1} → {event_count2}")
        
        if hash1 != hash2:
            print(f"   🚀 Update frequency: High (every 5 minutes or less)")
            print(f"   💡 Recommended refresh: Every 5-10 minutes")
        else:
            print(f"   🐌 Update frequency: Low (5+ minutes)")
            print(f"   💡 Recommended refresh: Every 15-30 minutes")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    quick_ics_test()
