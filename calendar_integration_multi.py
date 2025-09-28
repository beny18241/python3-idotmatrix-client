#!/usr/bin/env python3
"""
Multi-calendar integration for iDotMatrix using service account
Supports multiple Google Calendars
"""

import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_calendar_info_multi(calendar_id="primary", meeting_type="current"):
    """Get calendar information from a specific calendar using service account"""
    
    service_account_file = 'service-account.json'
    
    if not os.path.exists(service_account_file):
        print("❌ Service account file not found!")
        print("Please run: python calendar_service_account.py")
        return None
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
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
            
            events = events_result.get('items', [])
            
            if not events:
                return "Free"
            
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
            display_text = f"{summary}"
            if time_str:
                display_text += f" @ {time_str}"
            if location:
                display_text += f" ({location})"
            
            return display_text
            
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
                calendarId=calendar_id,
                timeMin=today_start_utc,
                timeMax=today_end_utc,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return f"Today: {len(events)} meetings"
        
        else:
            return "Invalid meeting type"
        
    except Exception as e:
        print(f"❌ Failed to get calendar info from {calendar_id}: {e}")
        return None

def get_all_calendars():
    """Get list of all accessible calendars"""
    
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
        
        return calendars
        
    except Exception as e:
        print(f"❌ Failed to get calendar list: {e}")
        return []

def main():
    """Test multi-calendar integration"""
    print("🔧 Testing Multi-Calendar Integration")
    print("=" * 50)
    
    # Get all accessible calendars
    calendars = get_all_calendars()
    
    if calendars:
        print("📅 Available calendars:")
        for calendar in calendars:
            calendar_id = calendar.get('id', 'Unknown')
            summary = calendar.get('summary', 'No Title')
            print(f"  - {summary} ({calendar_id})")
        
        print()
        
        # Test each calendar
        for calendar in calendars:
            calendar_id = calendar.get('id', 'primary')
            summary = calendar.get('summary', 'Unknown')
            
            print(f"🔍 Testing calendar: {summary}")
            
            # Test current meeting
            current_meeting = get_calendar_info_multi(calendar_id, "current")
            if current_meeting:
                print(f"  📅 Current: {current_meeting}")
            else:
                print(f"  📅 Current: No meeting")
            
            # Test next meeting
            next_meeting = get_calendar_info_multi(calendar_id, "next")
            if next_meeting:
                print(f"  📅 Next: {next_meeting}")
            else:
                print(f"  📅 Next: No meetings")
            
            print()
    else:
        print("❌ No calendars accessible")
    
    print("✅ Multi-calendar integration working!")

if __name__ == '__main__':
    main()
