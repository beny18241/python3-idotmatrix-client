#!/usr/bin/env python3
"""
Monitor ICS Calendar Update Frequency
Monitors how often the ICS calendar source updates
"""

import os
import sys
import time
import json
import datetime
import hashlib
import requests

def get_ics_calendar_hash(ics_url):
    """Get hash of ICS calendar content to detect changes"""
    
    try:
        response = requests.get(ics_url)
        response.raise_for_status()
        
        # Create hash of the content
        content_hash = hashlib.md5(response.text.encode()).hexdigest()
        return content_hash, response.text
        
    except Exception as e:
        print(f"❌ Error fetching ICS calendar: {e}")
        return None, None

def monitor_ics_updates(ics_url, monitor_duration_minutes=60):
    """Monitor ICS calendar for updates"""
    
    print(f"🔍 Monitoring ICS calendar updates for {monitor_duration_minutes} minutes")
    print(f"📅 ICS URL: {ics_url}")
    print("=" * 60)
    
    # Get initial hash
    print("1️⃣ Getting initial calendar state...")
    initial_hash, initial_content = get_ics_calendar_hash(ics_url)
    
    if not initial_hash:
        print("❌ Failed to get initial calendar state")
        return
    
    print(f"✅ Initial calendar hash: {initial_hash[:16]}...")
    
    # Count events in initial content
    event_count = initial_content.count('BEGIN:VEVENT')
    print(f"📊 Initial event count: {event_count}")
    
    # Monitor for changes
    print(f"\n2️⃣ Monitoring for changes every 5 minutes...")
    print("Press Ctrl+C to stop monitoring")
    print("-" * 60)
    
    start_time = datetime.datetime.now()
    update_count = 0
    last_update_time = None
    
    try:
        while True:
            time.sleep(5 * 60)  # Check every 5 minutes
            
            current_hash, current_content = get_ics_calendar_hash(ics_url)
            
            if not current_hash:
                print(f"❌ {datetime.datetime.now().strftime('%H:%M:%S')} - Failed to fetch calendar")
                continue
            
            if current_hash != initial_hash:
                update_count += 1
                last_update_time = datetime.datetime.now()
                
                # Count events in updated content
                new_event_count = current_content.count('BEGIN:VEVENT')
                event_change = new_event_count - event_count
                
                print(f"🔄 {last_update_time.strftime('%H:%M:%S')} - Calendar updated!")
                print(f"   📊 Events: {event_count} → {new_event_count} ({event_change:+d})")
                print(f"   🔑 Hash: {current_hash[:16]}...")
                print(f"   📈 Total updates: {update_count}")
                print("-" * 60)
                
                # Update for next comparison
                initial_hash = current_hash
                event_count = new_event_count
            else:
                elapsed = datetime.datetime.now() - start_time
                print(f"⏰ {datetime.datetime.now().strftime('%H:%M:%S')} - No changes (monitoring for {elapsed})")
            
            # Check if monitoring duration reached
            elapsed = datetime.datetime.now() - start_time
            if elapsed.total_seconds() >= monitor_duration_minutes * 60:
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    
    # Summary
    print(f"\n📊 Monitoring Summary:")
    print(f"   ⏱️  Duration: {monitor_duration_minutes} minutes")
    print(f"   🔄 Updates detected: {update_count}")
    print(f"   📅 Last update: {last_update_time.strftime('%H:%M:%S') if last_update_time else 'None'}")
    
    if update_count > 0:
        avg_interval = (monitor_duration_minutes * 60) / update_count
        print(f"   ⏰ Average update interval: {avg_interval:.1f} minutes")
        
        if avg_interval < 10:
            print("   🚀 High frequency updates (real-time to 10 minutes)")
        elif avg_interval < 30:
            print("   ⚡ Medium frequency updates (10-30 minutes)")
        else:
            print("   🐌 Low frequency updates (30+ minutes)")
    else:
        print("   📝 No updates detected during monitoring period")
        print("   💡 This could mean:")
        print("      • Calendar is very stable")
        print("      • Updates happen less frequently")
        print("      • Calendar source has low activity")

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python monitor_ics_updates.py [monitor_duration_minutes]")
        print("  monitor_duration_minutes: How long to monitor (default: 60)")
        print()
        print("Examples:")
        print("  python monitor_ics_updates.py 60    # Monitor for 1 hour")
        print("  python monitor_ics_updates.py 120   # Monitor for 2 hours")
        print("  python monitor_ics_updates.py 30    # Monitor for 30 minutes")
        return
    
    monitor_duration = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    
    # ICS calendar URL
    ics_url = "https://outlook.office365.com/owa/calendar/144d73fdf2654fb3b92983ee16e9d0b3@genpt.com/e829a99fc26b4c66a482420d04ea689513863417029725141930/calendar.ics"
    
    # Start monitoring
    monitor_ics_updates(ics_url, monitor_duration)

if __name__ == '__main__':
    main()
