#!/usr/bin/env python3
"""
Headless Google Calendar integration for iDotMatrix display
Designed for server environments without browser access
"""

import os
import json
import datetime
from typing import Optional, Dict, Any, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarIntegrationHeadless:
    """Handles Google Calendar API integration for headless server environments"""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """
        Initialize Google Calendar integration
        
        Args:
            credentials_file: Path to Google API credentials file
            token_file: Path to store/load OAuth token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate with Google Calendar API using headless flow"""
        creds = None
        
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Token refresh failed: {e}")
                    print("Please re-authenticate by running the setup script")
                    raise
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Google API credentials file not found: {self.credentials_file}\n"
                        "Please download credentials.json from Google Cloud Console"
                    )
                
                # Use headless flow for server environments
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                
                # For headless environments, use the console flow
                print("Please visit the following URL to authorize the application:")
                print(flow.authorization_url()[0])
                print("\nAfter authorization, you will be redirected to a page that shows 'This site can't be reached'")
                print("Copy the 'code' parameter from the URL and paste it here:")
                
                auth_code = input("Enter the authorization code: ").strip()
                
                try:
                    flow.fetch_token(code=auth_code)
                    creds = flow.credentials
                except Exception as e:
                    print(f"Authentication failed: {e}")
                    raise
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def get_current_meeting(self, calendar_id: str = 'primary') -> Optional[Dict[str, Any]]:
        """
        Get the current meeting happening now
        
        Args:
            calendar_id: Calendar ID to check (default: 'primary')
            
        Returns:
            Dictionary with meeting information or None if no current meeting
        """
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            
            # Get events happening now
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=now,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return None
            
            # Get the first event (current meeting)
            event = events[0]
            
            return {
                'summary': event.get('summary', 'No Title'),
                'start': event.get('start', {}),
                'end': event.get('end', {}),
                'description': event.get('description', ''),
                'location': event.get('location', ''),
                'attendees': event.get('attendees', []),
                'organizer': event.get('organizer', {}),
                'status': event.get('status', ''),
                'htmlLink': event.get('htmlLink', '')
            }
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    def get_next_meeting(self, calendar_id: str = 'primary', max_results: int = 1) -> Optional[Dict[str, Any]]:
        """
        Get the next upcoming meeting
        
        Args:
            calendar_id: Calendar ID to check (default: 'primary')
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with next meeting information or None if no upcoming meetings
        """
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            # Get upcoming events
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return None
            
            event = events[0]
            
            return {
                'summary': event.get('summary', 'No Title'),
                'start': event.get('start', {}),
                'end': event.get('end', {}),
                'description': event.get('description', ''),
                'location': event.get('location', ''),
                'attendees': event.get('attendees', []),
                'organizer': event.get('organizer', {}),
                'status': event.get('status', ''),
                'htmlLink': event.get('htmlLink', '')
            }
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    def get_todays_meetings(self, calendar_id: str = 'primary') -> List[Dict[str, Any]]:
        """
        Get all meetings for today
        
        Args:
            calendar_id: Calendar ID to check (default: 'primary')
            
        Returns:
            List of dictionaries with meeting information
        """
        try:
            # Start of today
            today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_start_utc = today_start.isoformat() + 'Z'
            
            # End of today
            today_end = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            today_end_utc = today_end.isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=today_start_utc,
                timeMax=today_end_utc,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            meetings = []
            for event in events:
                meetings.append({
                    'summary': event.get('summary', 'No Title'),
                    'start': event.get('start', {}),
                    'end': event.get('end', {}),
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'attendees': event.get('attendees', []),
                    'organizer': event.get('organizer', {}),
                    'status': event.get('status', ''),
                    'htmlLink': event.get('htmlLink', '')
                })
            
            return meetings
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def format_meeting_for_display(self, meeting: Dict[str, Any]) -> str:
        """
        Format meeting information for display on iDotMatrix
        
        Args:
            meeting: Meeting dictionary from get_current_meeting or get_next_meeting
            
        Returns:
            Formatted string for display
        """
        if not meeting:
            return "No meeting"
        
        summary = meeting.get('summary', 'No Title')
        start_time = meeting.get('start', {})
        location = meeting.get('location', '')
        
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
    
    def get_meeting_status_text(self, meeting: Dict[str, Any]) -> str:
        """
        Get a short status text for the meeting
        
        Args:
            meeting: Meeting dictionary
            
        Returns:
            Short status text
        """
        if not meeting:
            return "Free"
        
        summary = meeting.get('summary', 'Meeting')
        
        # Truncate if too long
        if len(summary) > 20:
            summary = summary[:17] + "..."
        
        return summary

def main():
    """Test the Google Calendar integration"""
    try:
        calendar = GoogleCalendarIntegrationHeadless()
        
        print("Google Calendar Integration Test")
        print("=" * 40)
        
        # Get current meeting
        current_meeting = calendar.get_current_meeting()
        if current_meeting:
            print("Current Meeting:")
            print(calendar.format_meeting_for_display(current_meeting))
        else:
            print("No current meeting")
        
        print()
        
        # Get next meeting
        next_meeting = calendar.get_next_meeting()
        if next_meeting:
            print("Next Meeting:")
            print(calendar.format_meeting_for_display(next_meeting))
        else:
            print("No upcoming meetings")
        
        print()
        
        # Get today's meetings count
        todays_meetings = calendar.get_todays_meetings()
        print(f"Today's meetings: {len(todays_meetings)}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have credentials.json file in the current directory")

if __name__ == '__main__':
    main()
