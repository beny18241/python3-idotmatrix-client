#!/usr/bin/env python3
"""
Test script for tomorrow's events
Quick test of tomorrow functionality
"""

from calendar_display_service import get_calendar_info

def main():
    """Test tomorrow's events"""
    print("🔧 Testing Tomorrow's Events")
    print("=" * 40)
    
    # Test tomorrow's events
    tomorrow_events = get_calendar_info("tomorrow")
    
    if tomorrow_events:
        print(f"📅 Tomorrow's events: {tomorrow_events}")
    else:
        print("📅 No events tomorrow")
    
    print()
    print("✅ Tomorrow's events test complete!")

if __name__ == '__main__':
    main()
