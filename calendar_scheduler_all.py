#!/usr/bin/env python3
"""
All Calendars Scheduler
Combines ICS and Google Calendar sources with fallback logic
Runs every 30 minutes and displays status on iDotMatrix device
"""

import time
import schedule
import subprocess
import sys
import os
import logging
from datetime import datetime

# Configure logging
def setup_logging():
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/calendar_scheduler.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()

def get_all_calendar_status():
    """Get current status from all available calendar sources"""
    
    logger.info("🔍 Checking all calendar sources...")
    print("🔍 Checking all calendar sources...")
    
    # Try ICS Calendar first (most reliable)
    ics_status = None
    ics_events = None
    try:
        from config import ICS_CALENDAR_URL
        from ics_calendar_simple import get_ics_events_for_current_simple
        
        logger.info("📅 Checking ICS Calendar...")
        print("📅 Checking ICS Calendar...")
        current_events = get_ics_events_for_current_simple(ICS_CALENDAR_URL)
        
        if current_events and current_events != "Free":
            ics_status = "busy"
            ics_events = current_events
            logger.info(f"ICS Calendar: BUSY - {current_events}")
        else:
            ics_status = "free"
            ics_events = "Free"
            logger.info("ICS Calendar: FREE")
            
        print(f"✅ ICS Calendar: {ics_status}")
        
    except Exception as e:
        logger.error(f"ICS Calendar error: {e}")
        print(f"❌ ICS Calendar error: {e}")
        ics_status = "error"
        ics_events = "ICS Error"
    
    # Try Google Calendar OAuth
    google_status = None
    google_events = None
    try:
        from oauth_calendar_final import get_oauth_calendar_events
        
        logger.info("📅 Checking Google Calendar (OAuth)...")
        print("📅 Checking Google Calendar (OAuth)...")
        current_events = get_oauth_calendar_events("current")
        
        if current_events and current_events != "Free" and current_events != "OAuth authentication failed":
            google_status = "busy"
            google_events = current_events
            logger.info(f"Google OAuth: BUSY - {current_events}")
        else:
            google_status = "free"
            google_events = "Free"
            logger.info("Google OAuth: FREE")
            
        print(f"✅ Google OAuth: {google_status}")
        
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        print(f"❌ Google OAuth error: {e}")
        google_status = "error"
        google_events = "Google OAuth Error"
    
    # Try Google Calendar Service Account
    service_status = None
    service_events = None
    try:
        from calendar_integration_service import get_current_meeting_service
        
        logger.info("📅 Checking Google Calendar (Service Account)...")
        print("📅 Checking Google Calendar (Service Account)...")
        current_meeting = get_current_meeting_service()
        
        if current_meeting:
            service_status = "busy"
            service_events = current_meeting
            logger.info(f"Google Service: BUSY - {current_meeting}")
        else:
            service_status = "free"
            service_events = "Free"
            logger.info("Google Service: FREE")
            
        print(f"✅ Google Service: {service_status}")
        
    except Exception as e:
        logger.error(f"Google Service Account error: {e}")
        print(f"❌ Google Service Account error: {e}")
        service_status = "error"
        service_events = "Google Service Error"
    
    # Determine final status with priority logic
    logger.info("📊 Status Summary:")
    print("\n📊 Status Summary:")
    print(f"   ICS Calendar: {ics_status} - {ics_events}")
    print(f"   Google OAuth: {google_status} - {google_events}")
    print(f"   Google Service: {service_status} - {service_events}")
    
    logger.info(f"ICS Calendar: {ics_status} - {ics_events}")
    logger.info(f"Google OAuth: {google_status} - {google_events}")
    logger.info(f"Google Service: {service_status} - {service_events}")
    
    # Priority: If any calendar shows busy, use that
    if ics_status == "busy":
        final_status = "busy"
        final_events = f"ICS: {ics_events}"
        logger.info(f"Final Status: {final_status} - {final_events}")
        return final_status, final_events
    elif google_status == "busy":
        final_status = "busy"
        final_events = f"Google: {google_events}"
        logger.info(f"Final Status: {final_status} - {final_events}")
        return final_status, final_events
    elif service_status == "busy":
        final_status = "busy"
        final_events = f"Service: {service_events}"
        logger.info(f"Final Status: {final_status} - {final_events}")
        return final_status, final_events
    
    # If all show free, return free
    if ics_status == "free" and google_status == "free" and service_status == "free":
        final_status = "free"
        final_events = "Free"
        logger.info(f"Final Status: {final_status} - {final_events}")
        return final_status, final_events
    
    # If there are errors but no busy status, return free with warning
    error_count = sum(1 for status in [ics_status, google_status, service_status] if status == "error")
    if error_count > 0:
        final_status = "free"
        final_events = f"Free (some sources unavailable)"
        logger.warning(f"Final Status: {final_status} - {final_events} (errors in {error_count} sources)")
        return final_status, final_events
    
    final_status = "free"
    final_events = "Free"
    logger.info(f"Final Status: {final_status} - {final_events}")
    return final_status, final_events

def display_status_on_device(status, events):
    """Display status on iDotMatrix device with animated emoji GIFs"""
    
    try:
        from config import DEVICE_ADDRESS
        
        # Check if required GIFs exist
        if not os.path.exists("images/free_emoji.gif"):
            logger.warning("Free emoji GIF not found: images/free_emoji.gif")
        if not os.path.exists("images/busy_emoji.gif"):
            logger.warning("Busy emoji GIF not found: images/busy_emoji.gif")
        if not os.path.exists("images/error_emoji.gif"):
            logger.warning("Error emoji GIF not found: images/error_emoji.gif")
        
        if status == "free":
            # Free emoji for free status
            gif_path = "images/free_emoji.gif"
            logger.info(f"Displaying FREE animation: {gif_path}")
            
            # Use the run script to display animated GIF
            cmd = [
                "./run_in_venv.sh",
                "--address", DEVICE_ADDRESS,
                "--set-gif", gif_path
            ]
            
        elif status == "busy":
            # Busy emoji for busy status
            gif_path = "images/busy_emoji.gif"
            logger.info(f"Displaying BUSY animation: {gif_path}")
            
            # Use the run script to display animated GIF
            cmd = [
                "./run_in_venv.sh",
                "--address", DEVICE_ADDRESS,
                "--set-gif", gif_path
            ]
            
        else:
            # Error emoji for error status
            gif_path = "images/error_emoji.gif"
            logger.info(f"Displaying ERROR animation: {gif_path}")
            
            # Use the run script to display animated GIF
            cmd = [
                "./run_in_venv.sh",
                "--address", DEVICE_ADDRESS,
                "--set-gif", gif_path
            ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        print(f"🚀 Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Status displayed successfully with animation")
            print(f"✅ Status displayed with animated emoji")
            return True
        else:
            logger.error(f"Failed to display on device: {result.stderr}")
            print(f"❌ Failed to display: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Error displaying on device: {e}")
        print(f"❌ Error displaying on device: {e}")
        return False

def update_calendar_status():
    """Update calendar status on device using all sources"""
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    logger.info(f"🕐 [{timestamp}] Updating calendar status from all sources...")
    print(f"\n🕐 [{timestamp}] Updating calendar status from all sources...")
    
    # Get status from all calendars
    status, events = get_all_calendar_status()
    
    logger.info(f"📊 Final Status: {status}")
    logger.info(f"📅 Final Events: {events}")
    print(f"📊 Final Status: {status}")
    print(f"📅 Final Events: {events}")
    
    # Display on device
    success = display_status_on_device(status, events)
    
    if success:
        logger.info("✅ Calendar status updated successfully")
        print(f"✅ Calendar status updated successfully")
    else:
        logger.error("❌ Failed to update calendar status")
        print(f"❌ Failed to update calendar status")
    
    return success

def run_scheduler():
    """Run the all calendars scheduler"""
    
    logger.info("🕐 All Calendars Scheduler Started")
    print("🕐 All Calendars Scheduler Started")
    print("=" * 50)
    print("📅 Updates every 30 minutes")
    print("🔍 Sources: ICS + Google OAuth + Google Service Account")
    print("🟢 FREE = Available")
    print("🔴 BUSY = In meeting")
    print("⚠️ ERROR = Connection issue")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Schedule updates every 30 minutes
    schedule.every(30).minutes.do(update_calendar_status)
    logger.info("Scheduled updates every 30 minutes")
    
    # Run initial update
    logger.info("Running initial calendar status update")
    update_calendar_status()
    
    # Keep running
    try:
        logger.info("Scheduler running - checking every minute")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user")
        print("\n🛑 Scheduler stopped by user")
        sys.exit(0)

def main():
    """Main function"""
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        logger.info("🧪 Testing all calendars status update...")
        print("🧪 Testing all calendars status update...")
        update_calendar_status()
    else:
        run_scheduler()

if __name__ == "__main__":
    main()
