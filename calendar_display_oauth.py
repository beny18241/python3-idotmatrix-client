#!/usr/bin/env python3
"""
Calendar display using OAuth authentication (token.json)
Works with your existing OAuth setup
"""

import os
import sys
import json
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_calendar_info_oauth(meeting_type="current"):
    """Get calendar information using OAuth authentication"""
    
    token_file = 'token.json'
    
    if not os.path.exists(token_file):
        print("❌ Token file not found!")
        print("Please run: python calendar_service_account.py")
        return None
    
    try:
        # Load OAuth credentials
        credentials = Credentials.from_authorized_user_file(token_file)
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        if meeting_type == "current":
            # Get current meeting - check for ongoing events
            now = datetime.datetime.utcnow()
            now_iso = now.isoformat() + 'Z'
            
            # Check a smaller time range to catch ongoing events
            time_range_start = (now - datetime.timedelta(minutes=30)).isoformat() + 'Z'
            time_range_end = (now + datetime.timedelta(minutes=30)).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=time_range_start,
                timeMax=time_range_end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return "Free"
            
            # Check each event to see if it's happening now
            for event in events:
                summary = event.get('summary', 'No Title')
                start_time = event.get('start', {})
                end_time = event.get('end', {})
                location = event.get('location', '')
                
                # Check if event is happening now
                if 'dateTime' in start_time and 'dateTime' in end_time:
                    try:
                        start_dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                        end_dt = datetime.datetime.fromisoformat(end_time['dateTime'].replace('Z', '+00:00'))
                        now_utc = datetime.datetime.now(datetime.timezone.utc)
                        
                        # Check if current time is between start and end
                        if start_dt <= now_utc <= end_dt:
                            # Create display text for current event
                            time_str = start_dt.strftime('%H:%M')
                            display_text = f"{summary}"
                            if time_str:
                                display_text += f" @ {time_str}"
                            if location:
                                display_text += f" ({location})"
                            
                            return display_text
                    except:
                        pass
            
            # If no current event found, return Free
            return "Free"
            
        elif meeting_type == "next":
            # Get next meeting
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=1,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return "No meetings"
            
            event = events[0]
            summary = event.get('summary', 'No Title')
            start_time = event.get('start', {})
            location = event.get('location', '')
            
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
            
            return display_text
            
        elif meeting_type == "today":
            # Get today's meetings count
            today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_start_utc = today_start.isoformat() + 'Z'
            
            today_end = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            today_end_utc = today_end.isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=today_start_utc,
                timeMax=today_end_utc,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return f"Today: {len(events)} meetings"
        
        elif meeting_type == "tomorrow":
            # Get tomorrow's events
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow_start_utc = tomorrow_start.isoformat() + 'Z'
            
            tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
            tomorrow_end_utc = tomorrow_end.isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=tomorrow_start_utc,
                timeMax=tomorrow_end_utc,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return "No events tomorrow"
            
            # Format tomorrow's events
            event_list = []
            for event in events:
                summary = event.get('summary', 'No Title')
                start_time = event.get('start', {})
                location = event.get('location', '')
                
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
                
                event_list.append(display_text)
            
            if len(event_list) == 1:
                return f"Tomorrow: {event_list[0]}"
            elif len(event_list) <= 3:
                return f"Tomorrow: {' | '.join(event_list)}"
            else:
                return f"Tomorrow: {len(event_list)} events"
        
        else:
            return "Invalid meeting type"
        
    except Exception as e:
        print(f"❌ Failed to get calendar info: {e}")
        return None

def main():
    """Main function for OAuth calendar display"""
    
    if len(sys.argv) < 2:
        print("Usage: python calendar_display_oauth.py <meeting_type>")
        print("  meeting_type: current, next, today, tomorrow")
        return
    
    meeting_type = sys.argv[1]
    
    # Get calendar information
    calendar_info = get_calendar_info_oauth(meeting_type)
    
    if calendar_info:
        print(calendar_info)
    else:
        print("❌ Failed to get calendar information")

if __name__ == '__main__':
    main()
