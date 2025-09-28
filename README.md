# iDotMatrix Calendar Integration

Complete calendar integration solution for iDotMatrix devices with Google Calendar and ICS calendar support.

## 🚀 New Calendar Features

- **Google Calendar Integration**: OAuth-based access to multiple Google calendars
- **ICS Calendar Support**: Direct access to Outlook/Exchange ICS calendars  
- **Combined Solution**: Display events from both Google Calendar and ICS calendars
- **Auto-Refresh**: OAuth tokens automatically refresh for 6+ months
- **Remote Server Support**: Works on headless servers with SSH tunneling
- **Multiple Calendar Sources**: Access personal, work, family, and imported calendars
- **Tomorrow Events**: Display tomorrow's meetings and events

## 🔄 OAuth Token Management (NEW)

### Token Lifecycle
- **Access Token**: Expires every 1 hour (auto-refreshes automatically)
- **Refresh Token**: Expires every 6 months (auto-refreshes automatically)
- **Maintenance**: Only need to copy token again in 6 months

### Check Token Status
```bash
source venv/bin/activate && python3 check_token_status.py
```

### Copy Token from Local Machine (NEW)
```bash
# On your LOCAL machine - copy token to server:
scp token.json user@server:/opt/idotmatrix/

# On the SERVER - verify copied token:
source venv/bin/activate && python3 copy_oauth_from_local.py
```

## 🚀 Quick Start - Calendar Features

### Combined Calendar Solution (Recommended)
```bash
# Display tomorrow's events from both Google Calendar and ICS
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS tomorrow

# Display current events
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS current

# Display today's events
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS today
```

### ICS Calendar Only (No Authentication Required)
```bash
# Works without Google authentication
# Using config.py (recommended)
python3 ics_only_solution.py tomorrow
python3 ics_only_solution.py current
python3 ics_only_solution.py today

# Or specify device manually
python3 ics_only_solution.py YOUR_DEVICE_ADDRESS tomorrow
python3 ics_only_solution.py YOUR_DEVICE_ADDRESS current
python3 ics_only_solution.py YOUR_DEVICE_ADDRESS today
```

### Google Calendar Only
```bash
# Display events from Google Calendar only
source venv/bin/activate && python3 oauth_calendar_final.py tomorrow
```

## 🔐 Calendar Setup

### 1. Google Calendar OAuth Setup
```bash
# Step 1: Create OAuth credentials in Google Cloud Console
# Step 2: Download credentials.json to your project

# Step 3: Setup SSH tunnel from your LOCAL machine:
ssh -L 8080:localhost:8080 user@server

# Step 4: On the SERVER (with tunnel running):
source venv/bin/activate && python3 oauth_ssh_tunnel_alt.py
```

### 2. ICS Calendar Setup (Optional)

#### Quick Setup
```bash
# Run the configuration setup
python3 setup_config.py
```

#### Manual Configuration
Edit `config.py` to set your settings:
```python
# Your ICS calendar URL
ICS_CALENDAR_URL = "https://outlook.office365.com/owa/calendar/.../calendar.ics"

# Your device address
DEVICE_ADDRESS = "DD:4F:93:46:DF:1A"

# Your timezone
TIMEZONE = "Europe/Warsaw"
```

## 🔧 Calendar Troubleshooting

### Check Token Status
```bash
source venv/bin/activate && python3 check_token_status.py
```

### Fix OAuth Issues
```bash
source venv/bin/activate && python3 fix_server_oauth.py
```

### Test ICS Calendar
```bash
python3 test_ics_simple.py
```

### Regenerate OAuth Token (if needed)
```bash
source venv/bin/activate && python3 fix_oauth_now.py
```

## 📁 Calendar Integration Files

### Main Calendar Scripts
- `oauth_calendar_final.py` - OAuth calendar solution
- `ics_only_solution.py` - ICS calendar solution  
- `run_oauth_calendar_venv.sh` - OAuth calendar wrapper
- `ics_calendar_simple.py` - ICS calendar parser

### Token Management
- `check_token_status.py` - Token status checker
- `copy_oauth_from_local.py` - Token copy utility
- `fix_server_oauth.py` - Fix OAuth token format
- `fix_oauth_now.py` - Regenerate OAuth token

### Testing Tools
- `test_ics_simple.py` - ICS calendar tester
- `oauth_ssh_tunnel_alt.py` - SSH tunnel for OAuth

---

# Original iDotMatrix Documentation

> [!NOTE]  
> Due to a long-term health condition (post-COVID since almost three years), I am unable to continue developing this project. Although many amazing contributors have helped over the years, I am unsure when I will be able to resume work. This is my most popular project (over 300 stars!), and I hope others will continue to improve the client and library for various use cases, such as Home Assistant integration. Thank you for your understanding and support.

<br/>
<p align="center">
  <a href="https://github.com/derkalle4/python3-idotmatrix-client">
    <img src="images/logo.png" alt="Logo" width="250" height="250">
  </a>

  <h3 align="center">Pixel Display Client</h3>

  <p align="center">
    control all your 16x16 or 32x32 pixel displays
    <br/>
    <br/>
    <a href="https://github.com/derkalle4/python3-idotmatrix-client"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/derkalle4/python3-idotmatrix-client/issues">Report Bug</a>
    .
    <a href="https://github.com/derkalle4/python3-idotmatrix-client/issues">Request Feature</a>
  </p>
</p>

![Downloads](https://img.shields.io/github/downloads/derkalle4/python3-idotmatrix-client/total) ![Contributors](https://img.shields.io/github/contributors/derkalle4/python3-idotmatrix-client?color=dark-green) ![Forks](https://img.shields.io/github/forks/derkalle4/python3-idotmatrix-client?style=social) ![Stargazers](https://img.shields.io/github/stars/derkalle4/python3-idotmatrix-client?style=social) ![Issues](https://img.shields.io/github/issues/derkalle4/python3-idotmatrix-client) ![License](https://img.shields.io/github/license/derkalle4/python3-idotmatrix-client) 

## Table Of Contents

* [Calendar Integration (NEW)](#calendar-integration-new)
* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [GUI](#gui)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

## About The Project

This repository aims to reverse engineer the [iDotMatrix](https://play.google.com/store/apps/details?id=com.tech.idotmatrix&pli=1) Android App for pixel screen displays like [this one on Aliexpress](https://de.aliexpress.com/item/1005006105517779.html). The goal is to be able to control multiple pixel screen displays via a GUI, an Rest API and the command line.

**NEW**: Calendar integration allows you to display your Google Calendar and ICS calendar events directly on your iDotMatrix device!

## Built With

* [Python 3](https://www.python.org/downloads/)
* [iDotMatrix Library](https://github.com/derkalle4/python3-idotmatrix-library)
* [Google Calendar API](https://developers.google.com/calendar) (NEW)
* [OAuth 2.0](https://oauth.net/2/) (NEW)
* [argparse](https://docs.python.org/3/library/argparse.html)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [bleak](https://github.com/hbldh/bleak)
* [pillow](https://python-pillow.org)

## Getting Started

### Prerequisites

* Latest version of Python (Python3)
* iDotMatrix device
* Google Cloud Console account (for calendar integration)

### Installation

#### For Linux or MSYS2/Git Bash

1. Clone the repo
```sh
git clone https://github.com/beny18241/python3-idotmatrix-client.git
```

2. `cd` to it
```sh
cd python3-idotmatrix-client
```

3. Create virtual environment and install all dependencies
```sh
./create_venv.sh
```

4. Install calendar dependencies (NEW)
```sh
source venv/bin/activate
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Usage

### Calendar Integration (NEW)

#### Calendar Commands

```bash
# Display calendar events with your device address
# Replace YOUR_DEVICE_ADDRESS with your actual device address

# Tomorrow's events (combined Google + ICS)
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS tomorrow

# Current events
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS current

# Today's events
./run_oauth_calendar_venv.sh YOUR_DEVICE_ADDRESS today

# ICS calendar only (no authentication)
python3 ics_only_solution.py YOUR_DEVICE_ADDRESS tomorrow
```

### Original Device Commands

If you used the ./create_venv.sh you should use this command to run the app:

```sh
./run_in_venv.sh <YOUR_COMMAND_LINE_ARGUMENTS>
```

#### command line arguments

##### --address (required for all commands except "scan")

Specifies the address of the pixel display device. Use "auto" to use the first available device (automatically looking for IDM-* devices in range).

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff
```

##### --calendar-current (NEW)

Display current meeting from Google Calendar.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --calendar-current
```

##### --calendar-next (NEW)

Display next meeting from Google Calendar.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --calendar-next
```

##### --calendar-today (NEW)

Display today's meetings from Google Calendar.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --calendar-today
```

##### --calendar-tomorrow (NEW)

Display tomorrow's meetings from Google Calendar.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --calendar-tomorrow
```

##### --scan

Scans all bluetooth devices in range for iDotMatrix devices.

```sh
./run_in_venv.sh --scan
```

##### --set-text

Sets a given text to the display.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --set-text "Hello World"
```

##### --clock

Sets the mode of the clock (0-7).

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --clock 0
```

##### --image

Display an image on the device.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --image true --set-image ./images/demo_32.png
```

## GUI

You can run the GUI uncompiled with python, or you can build an executable with PyInstaller.

### Run via Python
* Open terminal at `/python3-idotmatrix-client`
* Run `pip install pyqt5`
* Run `py gui.py`

## Troubleshooting

### Calendar Issues (NEW)

#### Check OAuth Token Status
```bash
source venv/bin/activate && python3 check_token_status.py
```

#### OAuth Token Issues
```bash
# Fix OAuth token format
source venv/bin/activate && python3 fix_server_oauth.py

# Regenerate OAuth token
source venv/bin/activate && python3 fix_oauth_now.py
```

#### ICS Calendar Issues
```bash
# Test ICS calendar access
python3 test_ics_simple.py
```

### Device Issues

#### Can't find device ID 

Try:
- Check that bluetooth is on
- Place the iDotMatrix display nearby
- Unplug and replug the iDotMatrix display
- Restart your PC

#### Can't upload gifs/images

Try:
- Sending the "reset" command (`--reset`)
- Use `--process-image` so the program tries to scale your images correctly
- Pre-scale your image to 32x32 or 16x16 pixels using an image editor

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GNU GENERAL PUBLIC License. See [LICENSE](https://github.com/derkalle4/python3-idotmatrix-client/blob/main/LICENSE) for more information.

## Authors

* [Kalle Minkner](https://github.com/derkalle4) - *Project Founder*
* [Jon-Mailes Graeffe](https://github.com/jmgraeffe) - *Co-Founder*
* [Calendar Integration Contributors](https://github.com/beny18241) - *Calendar Features*