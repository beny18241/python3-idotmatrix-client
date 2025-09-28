#!/usr/bin/env python3
"""
ICS Calendar Solution
Solution for accessing ICS calendars that can't be shared with service account
"""

import os
import sys
import json
import datetime
import requests
from icalendar import Calendar
from google.oauth2 import service_account
from googleapiclient.discovery import build

def fetch_ics_calendar(ics_url):
    """Fetch ICS calendar directly from URL"""
    
    print(f"🔍 Fetching ICS calendar from: {ics_url}")
    
    try:
        # Fetch the ICS calendar
        response = requests.get(ics_url)
        response.raise_for_status()
        
        # Parse the ICS calendar
        calendar = Calendar.from_ical(response.text)
        
        events = []
        for component in calendar.walk():
            if component.name == "VEVENT":
                event = {
                    'summary': str(component.get('summary', 'No Title')),
                    'start': component.get('dtstart'),
                    'end': component.get('dtend'),
                    'location': str(component.get('location', '')),
                    'description': str(component.get('description', ''))
                }
                events.append(event)
        
        print(f"✅ Found {len(events)} events in ICS calendar")
        return events
        
    except Exception as e:
        print(f"❌ Error fetching ICS calendar: {e}")
        return []

def get_ics_events_for_tomorrow(ics_url):
    """Get tomorrow's events from ICS calendar"""
    
    events = fetch_ics_calendar(ics_url)
    
    if not events:
        return "No events found in ICS calendar"
    
    # Get tomorrow's date
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow_date = tomorrow.date()
    
    tomorrow_events = []
    for event in events:
        start_time = event['start']
        if start_time:
            # Handle different date formats
            if hasattr(start_time, 'dt'):
                event_date = start_time.dt.date()
            else:
                event_date = start_time.date()
            
            if event_date == tomorrow_date:
                tomorrow_events.append(event)
    
    if not tomorrow_events:
        return "No events tomorrow in ICS calendar"
    
    # Format events for display
    event_list = []
    for event in tomorrow_events:
        summary = event['summary']
        start_time = event['start']
        location = event['location']
        
        # Format time
        time_str = ""
        if start_time:
            if hasattr(start_time, 'dt'):
                dt = start_time.dt
                if hasattr(dt, 'time'):
                    time_str = dt.time().strftime('%H:%M')
                else:
                    time_str = "All day"
            else:
                time_str = "All day"
        
        # Create display text
        display_text = f"{summary}"
        if time_str:
            display_text += f" @ {time_str}"
        if location:
            display_text += f" ({location})"
        
        event_list.append(display_text)
    
    if len(event_list) == 1:
        return f"Tomorrow: {event_list[0]}"
    elif len(event_list) <= 3:
        return f"Tomorrow: {' | '.join(event_list)}"
    else:
        return f"Tomorrow: {len(event_list)} events"

def get_ics_events_for_today(ics_url):
    """Get today's events from ICS calendar"""
    
    events = fetch_ics_calendar(ics_url)
    
    if not events:
        return "No events found in ICS calendar"
    
    # Get today's date
    today = datetime.datetime.now().date()
    
    today_events = []
    for event in events:
        start_time = event['start']
        if start_time:
            # Handle different date formats
            if hasattr(start_time, 'dt'):
                event_date = start_time.dt.date()
            else:
                event_date = start_time.date()
            
            if event_date == today:
                today_events.append(event)
    
    return f"Today: {len(today_events)} events in ICS calendar"

def get_ics_events_for_current(ics_url):
    """Get current events from ICS calendar"""
    
    events = fetch_ics_calendar(ics_url)
    
    if not events:
        return "No events found in ICS calendar"
    
    # Get current time
    now = datetime.datetime.now()
    current_time = now.time()
    current_date = now.date()
    
    current_events = []
    for event in events:
        start_time = event['start']
        end_time = event['end']
        
        if start_time and end_time:
            # Handle different date formats
            if hasattr(start_time, 'dt'):
                start_dt = start_time.dt
                end_dt = end_time.dt
            else:
                start_dt = start_time
                end_dt = end_time
            
            # Check if event is happening now
            if hasattr(start_dt, 'date') and hasattr(end_dt, 'date'):
                if start_dt.date() <= current_date <= end_dt.date():
                    current_events.append(event)
    
    if not current_events:
        return "Free"
    
    # Format current event
    event = current_events[0]
    summary = event['summary']
    start_time = event['start']
    location = event['location']
    
    # Format time
    time_str = ""
    if start_time:
        if hasattr(start_time, 'dt'):
            dt = start_time.dt
            if hasattr(dt, 'time'):
                time_str = dt.time().strftime('%H:%M')
            else:
                time_str = "Now"
        else:
            time_str = "Now"
    
    # Create display text
    display_text = f"{summary}"
    if time_str:
        display_text += f" @ {time_str}"
    if location:
        display_text += f" ({location})"
    
    return display_text

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python ics_calendar_solution.py <meeting_type>")
        print("  meeting_type: current, today, tomorrow")
        print()
        print("Examples:")
        print("  python ics_calendar_solution.py tomorrow")
        print("  python ics_calendar_solution.py current")
        print("  python ics_calendar_solution.py today")
        return
    
    meeting_type = sys.argv[1]
    
    # ICS calendar URL
    ics_url = "https://outlook.office365.com/owa/calendar/144d73fdf2654fb3b92983ee16e9d0b3@genpt.com/e829a99fc26b4c66a482420d04ea689513863417029725141930/calendar.ics"
    
    print(f"🔧 Getting {meeting_type} events from ICS calendar")
    print("=" * 60)
    
    if meeting_type == "tomorrow":
        events = get_ics_events_for_tomorrow(ics_url)
    elif meeting_type == "today":
        events = get_ics_events_for_today(ics_url)
    elif meeting_type == "current":
        events = get_ics_events_for_current(ics_url)
    else:
        print("❌ Invalid meeting type. Use: current, today, tomorrow")
        return
    
    print(f"📅 {events}")

if __name__ == '__main__':
    main()
