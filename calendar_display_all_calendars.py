#!/usr/bin/env python3
"""
Calendar display for iDotMatrix checking ALL accessible calendars
Finds events from any calendar you have access to
"""

import os
import sys
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_all_accessible_calendars():
    """Get all calendars you have access to"""
    
    service_account_file = 'service-account.json'
    
    if not os.path.exists(service_account_file):
        print("❌ Service account file not found!")
        return []
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Get calendar list
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        # Filter to accessible calendars
        accessible_calendars = []
        for calendar in calendars:
            access_role = calendar.get('accessRole', '')
            if access_role in ['owner', 'writer', 'reader']:
                accessible_calendars.append(calendar)
        
        return accessible_calendars
        
    except Exception as e:
        print(f"❌ Failed to get calendars: {e}")
        return []

def get_events_from_all_calendars(meeting_type="current"):
    """Get events from all accessible calendars"""
    
    accessible_calendars = get_all_accessible_calendars()
    
    if not accessible_calendars:
        print("❌ No accessible calendars found!")
        return None
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        all_events = []
        
        for calendar in accessible_calendars:
            calendar_id = calendar.get('id', '')
            calendar_name = calendar.get('summary', 'Unknown')
            
            try:
                if meeting_type == "current":
                    # Get current meeting
                    now = datetime.datetime.utcnow().isoformat() + 'Z'
                    
                    events_result = service.events().list(
                        calendarId=calendar_id,
                        timeMin=now,
                        timeMax=now,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()
                    
                elif meeting_type == "next":
                    # Get next meeting
                    now = datetime.datetime.utcnow().isoformat() + 'Z'
                    
                    events_result = service.events().list(
                        calendarId=calendar_id,
                        timeMin=now,
                        maxResults=1,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()
                    
                elif meeting_type == "today":
                    # Get today's meetings
                    today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    today_start_utc = today_start.isoformat() + 'Z'
                    today_end = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
                    today_end_utc = today_end.isoformat() + 'Z'
                    
                    events_result = service.events().list(
                        calendarId=calendar_id,
                        timeMin=today_start_utc,
                        timeMax=today_end_utc,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()
                    
                elif meeting_type == "tomorrow":
                    # Get tomorrow's events
                    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
                    tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                    tomorrow_start_utc = tomorrow_start.isoformat() + 'Z'
                    tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
                    tomorrow_end_utc = tomorrow_end.isoformat() + 'Z'
                    
                    events_result = service.events().list(
                        calendarId=calendar_id,
                        timeMin=tomorrow_start_utc,
                        timeMax=tomorrow_end_utc,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()
                
                else:
                    continue
                
                events = events_result.get('items', [])
                
                # Add calendar name to events
                for event in events:
                    event['calendar_name'] = calendar_name
                    all_events.append(event)
                
            except Exception as e:
                print(f"❌ Error accessing {calendar_name}: {e}")
                continue
        
        # Process events
        if not all_events:
            if meeting_type == "tomorrow":
                return "No events tomorrow"
            elif meeting_type == "today":
                return "No meetings today"
            else:
                return "No meetings found"
        
        # Sort events by start time
        all_events.sort(key=lambda x: x.get('start', {}).get('dateTime', x.get('start', {}).get('date', '')))
        
        if meeting_type == "current":
            # Return first current event
            event = all_events[0]
            summary = event.get('summary', 'No Title')
            start_time = event.get('start', {})
            location = event.get('location', '')
            calendar_name = event.get('calendar_name', '')
            
            # Format time
            time_str = ""
            if 'dateTime' in start_time:
                try:
                    dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                    time_str = dt.strftime('%H:%M')
                except:
                    time_str = "Now"
            elif 'date' in start_time:
                time_str = "All day"
            
            # Create display text
            display_text = f"{summary}"
            if time_str:
                display_text += f" @ {time_str}"
            if location:
                display_text += f" ({location})"
            if calendar_name and calendar_name != 'Primary':
                display_text += f" [{calendar_name}]"
            
            return display_text
            
        elif meeting_type == "next":
            # Return first upcoming event
            event = all_events[0]
            summary = event.get('summary', 'No Title')
            start_time = event.get('start', {})
            location = event.get('location', '')
            calendar_name = event.get('calendar_name', '')
            
            # Format time
            time_str = ""
            if 'dateTime' in start_time:
                try:
                    dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                    time_str = dt.strftime('%H:%M')
                except:
                    time_str = "Now"
            elif 'date' in start_time:
                time_str = "All day"
            
            # Create display text
            display_text = f"Next: {summary}"
            if time_str:
                display_text += f" @ {time_str}"
            if location:
                display_text += f" ({location})"
            if calendar_name and calendar_name != 'Primary':
                display_text += f" [{calendar_name}]"
            
            return display_text
            
        elif meeting_type == "today":
            return f"Today: {len(all_events)} meetings"
            
        elif meeting_type == "tomorrow":
            # Format tomorrow's events
            event_list = []
            for event in all_events:
                summary = event.get('summary', 'No Title')
                start_time = event.get('start', {})
                location = event.get('location', '')
                calendar_name = event.get('calendar_name', '')
                
                # Format time
                time_str = ""
                if 'dateTime' in start_time:
                    try:
                        dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                        time_str = dt.strftime('%H:%M')
                    except:
                        time_str = "All day"
                elif 'date' in start_time:
                    time_str = "All day"
                
                # Create display text
                display_text = f"{summary}"
                if time_str:
                    display_text += f" @ {time_str}"
                if location:
                    display_text += f" ({location})"
                if calendar_name and calendar_name != 'Primary':
                    display_text += f" [{calendar_name}]"
                
                event_list.append(display_text)
            
            if len(event_list) == 1:
                return f"Tomorrow: {event_list[0]}"
            elif len(event_list) <= 3:
                return f"Tomorrow: {' | '.join(event_list)}"
            else:
                return f"Tomorrow: {len(event_list)} events"
        
        return "No events found"
        
    except Exception as e:
        print(f"❌ Failed to get events: {e}")
        return None

def main():
    """Main function for all calendars display"""
    
    if len(sys.argv) < 2:
        print("Usage: python calendar_display_all_calendars.py <meeting_type>")
        print("  meeting_type: current, next, today, tomorrow")
        return
    
    meeting_type = sys.argv[1]
    
    print(f"🔧 Getting {meeting_type} events from ALL calendars...")
    
    # Get events from all calendars
    events = get_events_from_all_calendars(meeting_type)
    
    if events:
        print(events)
    else:
        print("❌ Failed to get events")

if __name__ == '__main__':
    main()
