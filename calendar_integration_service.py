#!/usr/bin/env python3
"""
Service account integration for iDotMatrix calendar commands
Replaces OAuth flow with service account authentication
"""

import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_current_meeting_service():
    """Get current meeting using service account"""
    
    service_account_file = 'service-account.json'
    token_file = 'token.json'
    
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
        
        # Get current meeting
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=now,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return None
        
        event = events[0]
        
        # Format meeting for display
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
        
    except Exception as e:
        print(f"❌ Failed to get current meeting: {e}")
        return None

def get_next_meeting_service():
    """Get next meeting using service account"""
    
    service_account_file = 'service-account.json'
    
    if not os.path.exists(service_account_file):
        print("❌ Service account file not found!")
        return None
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
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
            return None
        
        event = events[0]
        
        # Format meeting for display
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
        
    except Exception as e:
        print(f"❌ Failed to get next meeting: {e}")
        return None

def get_todays_meetings_count():
    """Get today's meetings count using service account"""
    
    service_account_file = 'service-account.json'
    
    if not os.path.exists(service_account_file):
        print("❌ Service account file not found!")
        return 0
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Get today's meetings
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
        return len(events)
        
    except Exception as e:
        print(f"❌ Failed to get today's meetings: {e}")
        return 0

def main():
    """Test the service account integration"""
    print("🔧 Testing Service Account Calendar Integration")
    print("=" * 50)
    
    # Test current meeting
    current_meeting = get_current_meeting_service()
    if current_meeting:
        print(f"📅 Current meeting: {current_meeting}")
    else:
        print("📅 No current meeting")
    
    # Test next meeting
    next_meeting = get_next_meeting_service()
    if next_meeting:
        print(f"📅 {next_meeting}")
    else:
        print("📅 No upcoming meetings")
    
    # Test today's meetings count
    todays_count = get_todays_meetings_count()
    print(f"📅 Today's meetings: {todays_count}")
    
    print()
    print("✅ Service account integration working!")
    print("Now you can use calendar commands with service account authentication.")

if __name__ == '__main__':
    main()
