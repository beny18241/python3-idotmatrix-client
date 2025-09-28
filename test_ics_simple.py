#!/usr/bin/env python3
"""
Test ICS Calendar Access (Simple)
Simple test to verify ICS calendar can be accessed without additional dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ics_calendar_simple import get_ics_events_for_tomorrow_simple, get_ics_events_for_current_simple, get_ics_events_for_today_simple

def test_ics_calendar_simple():
    """Test ICS calendar access"""
    
    print("🔧 Testing ICS Calendar Access (Simple)")
    print("=" * 50)
    
    # ICS calendar URL
    ics_url = "https://outlook.office365.com/owa/calendar/144d73fdf2654fb3b92983ee16e9d0b3@genpt.com/e829a99fc26b4c66a482420d04ea689513863417029725141930/calendar.ics"
    
    # Test tomorrow's events
    print("1️⃣ Testing tomorrow's events...")
    tomorrow_events = get_ics_events_for_tomorrow_simple(ics_url)
    print(f"📅 Tomorrow: {tomorrow_events}")
    print()
    
    # Test today's events
    print("2️⃣ Testing today's events...")
    today_events = get_ics_events_for_today_simple(ics_url)
    print(f"📅 Today: {today_events}")
    print()
    
    # Test current events
    print("3️⃣ Testing current events...")
    current_events = get_ics_events_for_current_simple(ics_url)
    print(f"📅 Current: {current_events}")
    print()
    
    print("✅ ICS Calendar test complete!")
    print("🚀 Next step: Test combined solution")
    print("   python combined_calendar_simple.py DD:4F:93:46:DF:1A tomorrow")

if __name__ == '__main__':
    test_ics_calendar_simple()
