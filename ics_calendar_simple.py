#!/usr/bin/env python3
"""
Simple ICS Calendar Solution
Works without additional dependencies - uses basic Python libraries only
"""

import os
import sys
import json
import datetime
import requests
import re

def fetch_ics_calendar_simple(ics_url):
    """Fetch ICS calendar using basic Python libraries"""
    
    print(f"🔍 Fetching ICS calendar from: {ics_url}")
    
    try:
        # Fetch the ICS calendar
        response = requests.get(ics_url)
        response.raise_for_status()
        
        # Parse the ICS calendar manually
        ics_content = response.text
        
        # Find all VEVENT blocks
        events = []
        event_blocks = re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', ics_content, re.DOTALL)
        
        for event_block in event_blocks:
            event = {}
            
            # Extract summary
            summary_match = re.search(r'SUMMARY:(.*?)(?:\r?\n|$)', event_block)
            if summary_match:
                event['summary'] = summary_match.group(1).strip()
            else:
                event['summary'] = 'No Title'
            
            # Extract start time
            start_match = re.search(r'DTSTART(?:;.*?)?:(.*?)(?:\r?\n|$)', event_block)
            if start_match:
                event['start'] = start_match.group(1).strip()
            else:
                event['start'] = None
            
            # Extract end time
            end_match = re.search(r'DTEND(?:;.*?)?:(.*?)(?:\r?\n|$)', event_block)
            if end_match:
                event['end'] = end_match.group(1).strip()
            else:
                event['end'] = None
            
            # Extract location
            location_match = re.search(r'LOCATION:(.*?)(?:\r?\n|$)', event_block)
            if location_match:
                event['location'] = location_match.group(1).strip()
            else:
                event['location'] = ''
            
            # Extract description
            desc_match = re.search(r'DESCRIPTION:(.*?)(?:\r?\n|$)', event_block)
            if desc_match:
                event['description'] = desc_match.group(1).strip()
            else:
                event['description'] = ''
            
            events.append(event)
        
        print(f"✅ Found {len(events)} events in ICS calendar")
        return events
        
    except Exception as e:
        print(f"❌ Error fetching ICS calendar: {e}")
        return []

def parse_ics_datetime(dt_str):
    """Parse ICS datetime string"""
    if not dt_str:
        return None
    
    try:
        # Handle different ICS datetime formats
        if 'T' in dt_str:
            # Full datetime format: 20241201T143000Z
            if dt_str.endswith('Z'):
                # UTC time
                dt_str = dt_str[:-1] + '+00:00'
            return datetime.datetime.fromisoformat(dt_str)
        else:
            # Date only format: 20241201
            return datetime.datetime.strptime(dt_str, '%Y%m%d')
    except:
        return None

def get_ics_events_for_tomorrow_simple(ics_url):
    """Get tomorrow's events from ICS calendar"""
    
    events = fetch_ics_calendar_simple(ics_url)
    
    if not events:
        return "No events found in ICS calendar"
    
    # Get tomorrow's date
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow_date = tomorrow.date()
    
    tomorrow_events = []
    for event in events:
        start_time = event['start']
        if start_time:
            event_dt = parse_ics_datetime(start_time)
            if event_dt and event_dt.date() == tomorrow_date:
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
            event_dt = parse_ics_datetime(start_time)
            if event_dt and hasattr(event_dt, 'time'):
                time_str = event_dt.time().strftime('%H:%M')
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

def get_ics_events_for_today_simple(ics_url):
    """Get today's events from ICS calendar"""
    
    events = fetch_ics_calendar_simple(ics_url)
    
    if not events:
        return "No events found in ICS calendar"
    
    # Get today's date
    today = datetime.datetime.now().date()
    
    today_events = []
    for event in events:
        start_time = event['start']
        if start_time:
            event_dt = parse_ics_datetime(start_time)
            if event_dt and event_dt.date() == today:
                today_events.append(event)
    
    return f"Today: {len(today_events)} events in ICS calendar"

def get_ics_events_for_current_simple(ics_url):
    """Get current events from ICS calendar"""
    
    events = fetch_ics_calendar_simple(ics_url)
    
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
            start_dt = parse_ics_datetime(start_time)
            end_dt = parse_ics_datetime(end_time)
            
            # Check if event is happening now
            if start_dt and end_dt:
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
        event_dt = parse_ics_datetime(start_time)
        if event_dt and hasattr(event_dt, 'time'):
            time_str = event_dt.time().strftime('%H:%M')
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
        print("Usage: python ics_calendar_simple.py <meeting_type>")
        print("  meeting_type: current, today, tomorrow")
        print()
        print("Examples:")
        print("  python ics_calendar_simple.py tomorrow")
        print("  python ics_calendar_simple.py current")
        print("  python ics_calendar_simple.py today")
        return
    
    meeting_type = sys.argv[1]
    
    # ICS calendar URL
    ics_url = "https://outlook.office365.com/owa/calendar/144d73fdf2654fb3b92983ee16e9d0b3@genpt.com/e829a99fc26b4c66a482420d04ea689513863417029725141930/calendar.ics"
    
    print(f"🔧 Getting {meeting_type} events from ICS calendar")
    print("=" * 60)
    
    if meeting_type == "tomorrow":
        events = get_ics_events_for_tomorrow_simple(ics_url)
    elif meeting_type == "today":
        events = get_ics_events_for_today_simple(ics_url)
    elif meeting_type == "current":
        events = get_ics_events_for_current_simple(ics_url)
    else:
        print("❌ Invalid meeting type. Use: current, today, tomorrow")
        return
    
    print(f"📅 {events}")

if __name__ == '__main__':
    main()
