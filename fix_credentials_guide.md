# Fix Google Calendar OAuth "Invalid Request" Error

The "invalid request" error usually means there's an issue with your OAuth client configuration. Here's how to fix it:

## 🔧 **Step 1: Check Your Credentials**

Your `credentials.json` file should look like this for a Desktop application:

```json
{
  "installed": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your-client-secret",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
  }
}
```

## 🔧 **Step 2: Create New Credentials (Recommended)**

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Select your project** (or create a new one)
3. **Enable Google Calendar API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"
4. **Create OAuth credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop application"
   - Give it a name like "iDotMatrix Calendar"
   - Click "Create"
5. **Download the JSON file** and save as `credentials.json`

## 🔧 **Step 3: Configure OAuth Consent Screen**

1. **Go to "APIs & Services" > "OAuth consent screen"**
2. **Choose "External"** (unless you have a Google Workspace)
3. **Fill in required fields**:
   - App name: "iDotMatrix Calendar"
   - User support email: your email
   - Developer contact: your email
4. **Add your email to test users**
5. **Save and continue**

## 🔧 **Step 4: Test the Fixed Authentication**

```bash
# Use the fixed authentication script
python calendar_auth_fixed.py
```

## 🔧 **Common Issues and Solutions**

### Issue: "n8n's request is invalid"
- **Cause**: Wrong OAuth client type or configuration
- **Solution**: Create new Desktop application credentials

### Issue: "Access blocked"
- **Cause**: OAuth consent screen not configured
- **Solution**: Configure OAuth consent screen and add test users

### Issue: "Invalid redirect URI"
- **Cause**: Wrong redirect URI in credentials
- **Solution**: Use Desktop application credentials (not Web application)

### Issue: "This app isn't verified"
- **Cause**: App is in testing mode
- **Solution**: Add your email as a test user in OAuth consent screen

## 🔧 **Quick Fix Commands**

```bash
# 1. Check your current credentials
cat credentials.json | grep -E "(installed|web)"

# 2. If it shows "web" instead of "installed", create new credentials

# 3. Use the fixed authentication
python calendar_auth_fixed.py
```

## 🔧 **Expected Success Flow**

1. **Visit the URL** - Should work without "invalid request" errors
2. **Sign in** - Use your Google account
3. **Grant permission** - Allow calendar access
4. **Get authorization code** - Copy from the success page
5. **Paste the code** - Into your terminal
6. **Test access** - Verify calendar connection works

The fixed authentication script includes better error handling and troubleshooting tips!
