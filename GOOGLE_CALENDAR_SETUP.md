# Google Calendar Integration Setup

This guide will help you set up Google Calendar integration for the iDotMatrix display.

## Prerequisites

1. A Google account
2. Google Cloud Console access
3. Python environment with the required dependencies

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click on it and press "Enable"

## Step 2: Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields (App name, User support email, Developer contact)
   - Add your email to test users
4. For Application type, choose "Desktop application"
5. Give it a name (e.g., "iDotMatrix Calendar Integration")
6. Click "Create"
7. Download the JSON file and rename it to `credentials.json`
8. Place `credentials.json` in your iDotMatrix project directory

## Step 3: Install Dependencies

The required dependencies are already added to `pyproject.toml`. Install them with:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Or if using the virtual environment:

```bash
./create_venv.sh
```

## Step 4: First Run Authentication

When you first run a calendar command, the application will:

1. Open a web browser
2. Ask you to sign in to your Google account
3. Request permission to access your calendar
4. Save the authentication token to `token.json`

## Usage Examples

### Display Current Meeting
```bash
./run_in_venv.sh --address auto --calendar-current
```

### Display Next Meeting
```bash
./run_in_venv.sh --address auto --calendar-next
```

### Display Today's Meeting Count
```bash
./run_in_venv.sh --address auto --calendar-today
```

### Custom Credentials/Token Files
```bash
./run_in_venv.sh --address auto --calendar-current --calendar-credentials /path/to/credentials.json --calendar-token /path/to/token.json
```

## Features

- **Current Meeting**: Shows the meeting happening right now
- **Next Meeting**: Shows the next upcoming meeting
- **Today's Count**: Shows how many meetings you have today
- **Auto-refresh**: Token automatically refreshes when needed
- **Error Handling**: Graceful fallbacks when no meetings are found

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded the credentials file from Google Cloud Console
- Rename it to `credentials.json` and place it in the project directory

### "Permission denied"
- Make sure you granted calendar access during the OAuth flow
- Check that the Google Calendar API is enabled in your project

### "No current meeting found"
- This is normal when you don't have a meeting scheduled right now
- The display will show "Free" instead

### Token expires
- The application will automatically refresh tokens
- If issues persist, delete `token.json` and re-authenticate

## Security Notes

- Keep your `credentials.json` file secure and don't commit it to version control
- The `token.json` file contains your access token and should also be kept private
- Both files are already added to `.gitignore`

## API Limits

Google Calendar API has generous limits for personal use:
- 1,000,000 queries per day
- 100 queries per 100 seconds per user

This should be more than sufficient for typical usage.
