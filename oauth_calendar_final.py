#!/usr/bin/env python3
"""
OAuth Calendar Final Solution
Complete OAuth solution that bypasses service account limitations
"""

import os
import sys
import json
import datetime
import subprocess
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

def get_ics_calendar_events(meeting_type="tomorrow"):
    """Get events from ICS calendar"""
    
    try:
        print("2️⃣ Checking ICS Calendar...")
        # Load configuration
        try:
            from config import ICS_CALENDAR_URL
            ics_url = ICS_CALENDAR_URL
        except ImportError:
            print("❌ Configuration file not found!")
            print("   Please create config.py with your ICS_CALENDAR_URL")
            return "Configuration error"
        
        # Import here to avoid errors if not available
        from ics_calendar_simple import get_ics_events_for_tomorrow_simple, get_ics_events_for_current_simple, get_ics_events_for_today_simple
        
        if meeting_type == "tomorrow":
            ics_events = get_ics_events_for_tomorrow_simple(ics_url)
        elif meeting_type == "current":
            ics_events = get_ics_events_for_current_simple(ics_url)
        elif meeting_type == "today":
            ics_events = get_ics_events_for_today_simple(ics_url)
        else:
            ics_events = "Invalid meeting type"
        
        if ics_events and ics_events != "No events found":
            print(f"✅ ICS Calendar: {ics_events}")
            return ics_events
        else:
            print("❌ No events in ICS Calendar")
            return None
            
    except Exception as e:
        print(f"❌ ICS Calendar error: {e}")
        return None

def combine_events(google_events, ics_events):
    """Combine events from both sources"""
    
    print("3️⃣ Combining events from all sources...")
    
    events_list = []
    
    if google_events and google_events != "No events found" and google_events != "OAuth authentication failed":
        # Extract Google Calendar events
        if "Tomorrow:" in google_events:
            google_text = google_events.replace("Tomorrow:", "").strip()
            events_list.append(f"Google: {google_text}")
        else:
            events_list.append(f"Google: {google_events}")
    
    if ics_events and ics_events != "No events found":
        # Extract ICS Calendar events
        if "Tomorrow:" in ics_events:
            ics_text = ics_events.replace("Tomorrow:", "").strip()
            events_list.append(f"ICS: {ics_text}")
        else:
            events_list.append(f"ICS: {ics_events}")
    
    if not events_list:
        return "No events found"
    
    # Combine events
    if len(events_list) == 1:
        return events_list[0]
    else:
        return " | ".join(events_list)

def get_combined_events_final(meeting_type="tomorrow"):
    """Get events from both Google Calendar and ICS calendar"""
    
    print(f"🔧 Getting {meeting_type} events from all sources")
    print("=" * 60)
    
    # Get Google Calendar events (OAuth)
    print("1️⃣ Checking Google Calendar (OAuth)...")
    google_events = get_oauth_calendar_events(meeting_type)
    
    # Get ICS Calendar events
    ics_events = get_ics_calendar_events(meeting_type)
    
    # Combine events
    combined_events = combine_events(google_events, ics_events)
    
    print(f"📅 Combined events: {combined_events}")
    return combined_events

def display_combined_events_on_device_final(device_address, meeting_type="tomorrow"):
    """Display combined events on iDotMatrix device"""
    
    print(f"🔧 Displaying {meeting_type} events on device {device_address}")
    print("=" * 60)
    
    # Get events from all sources
    events = get_combined_events_final(meeting_type)
    
    if not events or events == "No events found":
        print("❌ No events found!")
        return False
    
    print(f"📅 Events: {events}")
    
    # Display on device
    try:
        # Use the run script to display text
        cmd = [
            "./run_in_venv.sh",
            "--address", device_address,
            "--set-text", events
        ]
        
        print(f"🚀 Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Events displayed successfully on iDotMatrix device!")
            print(f"📱 Displayed: {events}")
            return True
        else:
            print(f"❌ Failed to display on device: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error displaying on device: {e}")
        return False

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python oauth_calendar_final.py <device_address> [meeting_type]")
        print("  device_address: Bluetooth address of iDotMatrix device")
        print("  meeting_type: current, today, tomorrow (default: tomorrow)")
        print()
        print("Examples:")
        print("  python oauth_calendar_final.py DD:4F:93:46:DF:1A tomorrow")
        print("  python oauth_calendar_final.py DD:4F:93:46:DF:1A current")
        print("  python oauth_calendar_final.py DD:4F:93:46:DF:1A today")
        print()
        print("🔧 This solution combines:")
        print("   • Google Calendar (via OAuth)")
        print("   • ICS Calendar (direct access)")
        return
    
    device_address = sys.argv[1]
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "tomorrow"
    
    # Display combined events on device
    success = display_combined_events_on_device_final(device_address, meeting_type)
    
    if success:
        print("\n🎉 Success! Events are now displayed on your iDotMatrix device!")
        print("📋 This solution combines:")
        print("   • Google Calendar (via OAuth)")
        print("   • ICS Calendar (direct access)")
    else:
        print("\n❌ Failed to display events on device")
        print("Please check:")
        print("1. Device address is correct")
        print("2. iDotMatrix device is connected")
        print("3. Internet connection is working")
        print("4. OAuth credentials are properly configured")

if __name__ == '__main__':
    main()
