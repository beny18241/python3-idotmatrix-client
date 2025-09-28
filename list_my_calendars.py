#!/usr/bin/env python3
"""
List My Calendars

This script shows all calendars you have access to.
"""

import os
import sys

def list_google_calendars():
    """List Google Calendar access"""
    
    print("🔍 Google Calendar Access")
    print("=" * 50)
    
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        # Load OAuth token
        creds = Credentials.from_authorized_user_file('token.json')
        
        # Create service
        service = build('calendar', 'v3', credentials=creds)
        
        # Get calendar list
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        print(f"📅 Found {len(calendars)} accessible calendars:")
        print()
        
        for i, calendar in enumerate(calendars, 1):
            calendar_id = calendar['id']
            summary = calendar.get('summary', 'No name')
            access_role = calendar.get('accessRole', 'unknown')
            primary = calendar.get('primary', False)
            
            print(f"{i:2d}. {summary}")
            print(f"    📧 ID: {calendar_id}")
            print(f"    🔑 Role: {access_role}")
            if primary:
                print(f"    ⭐ Primary calendar")
            print()
        
        return calendars
        
    except Exception as e:
        print(f"❌ Google Calendar error: {e}")
        return []

def list_ics_calendar():
    """List ICS calendar access"""
    
    print("🔍 ICS Calendar Access")
    print("=" * 50)
    
    try:
        from config import ICS_CALENDAR_URL
        from ics_calendar_simple import get_ics_events_for_tomorrow_simple, get_ics_events_for_current_simple, get_ics_events_for_today_simple
        
        print(f"📅 ICS Calendar URL:")
        print(f"    {ICS_CALENDAR_URL}")
        print()
        
        # Test access
        print("🧪 Testing ICS calendar access...")
        
        # Test tomorrow
        tomorrow_events = get_ics_events_for_tomorrow_simple(ICS_CALENDAR_URL)
        print(f"📅 Tomorrow: {tomorrow_events}")
        
        # Test current
        current_events = get_ics_events_for_current_simple(ICS_CALENDAR_URL)
        print(f"📅 Current: {current_events}")
        
        # Test today
        today_events = get_ics_events_for_today_simple(ICS_CALENDAR_URL)
        print(f"📅 Today: {today_events}")
        
        print()
        print("✅ ICS Calendar is accessible!")
        
    except Exception as e:
        print(f"❌ ICS Calendar error: {e}")

def main():
    """Main function"""
    
    print("📋 Your Calendar Access Summary")
    print("=" * 60)
    print()
    
    # Check Google Calendar
    google_calendars = list_google_calendars()
    
    print()
    
    # Check ICS Calendar
    list_ics_calendar()
    
    print()
    print("🚀 Usage Commands:")
    print("=" * 30)
    print("📅 ICS Calendar only:")
    print("   python3 ics_only_solution.py tomorrow")
    print("   python3 ics_only_solution.py current")
    print()
    print("📅 Combined (Google + ICS):")
    print("   ./run_oauth_calendar_venv.sh DD:4F:93:46:DF:1A tomorrow")
    print("   ./run_oauth_calendar_venv.sh DD:4F:93:46:DF:1A current")
    print()
    print("📅 Google Calendar only:")
    print("   source venv/bin/activate && python3 oauth_calendar_final.py tomorrow")

if __name__ == "__main__":
    main()
