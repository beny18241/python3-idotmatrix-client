#!/usr/bin/env python3
"""
OAuth Calendar Solution
Alternative solution using OAuth instead of service account
"""

import os
import sys
import json
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_oauth_credentials():
    """Get OAuth credentials"""
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    creds = None
    
    # Check if token.json exists
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            print("✅ OAuth token found")
        except Exception as e:
            print(f"❌ Error loading OAuth token: {e}")
            creds = None
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("✅ OAuth token refreshed")
            except Exception as e:
                print(f"❌ Error refreshing OAuth token: {e}")
                creds = None
        
        if not creds:
            if not os.path.exists('credentials.json'):
                print("❌ credentials.json not found!")
                print("Please download OAuth credentials from Google Cloud Console")
                return None
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                print("✅ OAuth authentication successful")
            except Exception as e:
                print(f"❌ OAuth authentication failed: {e}")
                return None
        
        # Save credentials for next run
        try:
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            print("✅ OAuth token saved")
        except Exception as e:
            print(f"❌ Error saving OAuth token: {e}")
    
    return creds

def get_oauth_calendar_events(meeting_type="tomorrow"):
    """Get events from Google Calendar using OAuth"""
    
    print(f"🔧 Getting {meeting_type} events from Google Calendar (OAuth)")
    print("=" * 60)
    
    try:
        # Get OAuth credentials
        creds = get_oauth_credentials()
        if not creds:
            return "OAuth authentication failed"
        
        # Create service
        service = build('calendar', 'v3', credentials=creds)
        print("✅ Google Calendar API service created")
        
        # Get calendar list
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        print(f"📅 Found {len(calendars)} accessible calendars")
        
        if not calendars:
            return "No calendars accessible"
        
        # Get events based on meeting type
        if meeting_type == "tomorrow":
            # Get tomorrow's events
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow_start_utc = tomorrow_start.isoformat() + 'Z'
            tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
            tomorrow_end_utc = tomorrow_end.isoformat() + 'Z'
            
            all_events = []
            for calendar in calendars:
                calendar_id = calendar.get('id', '')
                summary = calendar.get('summary', 'Unknown')
                
                try:
                    events_result = service.events().list(
                        calendarId=calendar_id,
                        timeMin=tomorrow_start_utc,
                        timeMax=tomorrow_end_utc,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()
                    
                    events = events_result.get('items', [])
                    if events:
                        for event in events:
                            event_summary = event.get('summary', 'No Title')
                            start_time = event.get('start', {})
                            
                            time_str = ""
                            if 'dateTime' in start_time:
                                try:
                                    dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                                    time_str = dt.strftime('%H:%M')
                                except:
                                    time_str = "All day"
                            elif 'date' in start_time:
                                time_str = "All day"
                            
                            all_events.append(f"{event_summary} @ {time_str}")
                
                except Exception as e:
                    print(f"❌ Error accessing calendar {summary}: {e}")
            
            if all_events:
                if len(all_events) == 1:
                    return f"Tomorrow: {all_events[0]}"
                elif len(all_events) <= 3:
                    return f"Tomorrow: {' | '.join(all_events)}"
                else:
                    return f"Tomorrow: {len(all_events)} events"
            else:
                return "No events tomorrow"
        
        elif meeting_type == "current":
            # Get current events
            now = datetime.datetime.now()
            now_utc = now.isoformat() + 'Z'
            
            for calendar in calendars:
                calendar_id = calendar.get('id', '')
                
                try:
                    events_result = service.events().list(
                        calendarId=calendar_id,
                        timeMin=now_utc,
                        maxResults=1,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()
                    
                    events = events_result.get('items', [])
                    if events:
                        event = events[0]
                        event_summary = event.get('summary', 'No Title')
                        start_time = event.get('start', {})
                        
                        time_str = ""
                        if 'dateTime' in start_time:
                            try:
                                dt = datetime.datetime.fromisoformat(start_time['dateTime'].replace('Z', '+00:00'))
                                time_str = dt.strftime('%H:%M')
                            except:
                                time_str = "Now"
                        elif 'date' in start_time:
                            time_str = "Now"
                        
                        return f"{event_summary} @ {time_str}"
                
                except Exception as e:
                    print(f"❌ Error accessing calendar: {e}")
            
            return "Free"
        
        else:
            return "Invalid meeting type"
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Error: {e}"

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python oauth_calendar_solution.py <meeting_type>")
        print("  meeting_type: current, today, tomorrow")
        print()
        print("Examples:")
        print("  python oauth_calendar_solution.py tomorrow")
        print("  python oauth_calendar_solution.py current")
        print("  python oauth_calendar_solution.py today")
        return
    
    meeting_type = sys.argv[1]
    
    # Get events using OAuth
    events = get_oauth_calendar_events(meeting_type)
    
    print(f"📅 {events}")

if __name__ == '__main__':
    main()
