# 🔧 Fix Calendar Access for Service Account

The service account needs permission to access your calendars. Follow these steps:

## Step 1: Get Service Account Email

First, you need to run the service account setup to get the service account email:

```bash
# Run the service account setup
python calendar_service_account.py
```

This will create a `service-account.json` file with the service account email.

## Step 2: Share Calendars with Service Account

Once you have the service account email, you need to share your calendars with it:

### For Your Primary Calendar:
1. Go to [Google Calendar](https://calendar.google.com)
2. Click the gear icon (Settings) in the top right
3. Click 'Settings' from the dropdown
4. In the left sidebar, click 'Settings for my calendars'
5. Click on your calendar name
6. Click 'Share with specific people'
7. Click 'Add people'
8. Add the service account email (from step 1)
9. Set permission to 'See all event details'
10. Click 'Send'

### For Your Imported Calendar:
1. Go to [Google Calendar](https://calendar.google.com)
2. Find your imported calendar in the left sidebar
3. Click the three dots next to the calendar name
4. Click 'Settings and sharing'
5. Click 'Share with specific people'
6. Click 'Add people'
7. Add the service account email
8. Set permission to 'See all event details'
9. Click 'Send'

## Step 3: Test Access

After sharing the calendars, test the access:

```bash
# Test multi-calendar setup
python setup_multi_calendar.py
```

## Step 4: Display on iDotMatrix

Once access is working, display calendar info:

```bash
# Display current meeting from any calendar
python calendar_display_multi.py DD:4F:93:46:DF:1A current
```

## Troubleshooting

### If you get "No calendars accessible":
- Make sure you've shared the calendars with the service account
- Wait a few minutes for permissions to propagate
- Check that the service account email is correct

### If you get "Service account file not found":
- Run `python calendar_service_account.py` first
- Make sure `service-account.json` exists

### If you get "ModuleNotFoundError":
- Make sure you're in the virtual environment
- Run `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)

## Quick Links

- [Google Calendar](https://calendar.google.com)
- [Calendar Settings](https://calendar.google.com/calendar/r/settings)
- [Google Cloud Console](https://console.cloud.google.com)
