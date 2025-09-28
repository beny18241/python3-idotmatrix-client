# Fix OAuth "n8n's request is invalid" Error

The "n8n's request is invalid" error indicates there's a fundamental issue with your OAuth client configuration. Here are the solutions:

## 🔧 **Solution 1: Create New OAuth Credentials**

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Select your project (or create a new one)

### Step 2: Create New OAuth Client
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Name it "iDotMatrix Calendar" (not n8n)
5. Click "Create"
6. Download the JSON file and save as `credentials.json`

### Step 3: Configure OAuth Consent Screen
1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External"
3. Fill in required fields:
   - App name: "iDotMatrix Calendar"
   - User support email: your email
   - Developer contact: your email
4. Add your email to test users
5. Save and continue

## 🔧 **Solution 2: Use Different Google Account**

### Step 1: Create New Google Account
1. Create a new Google account
2. Use this account for the OAuth flow
3. This bypasses any existing OAuth issues

### Step 2: Update Credentials
1. Use the new account to create OAuth credentials
2. Download new `credentials.json`
3. Try authentication again

## 🔧 **Solution 3: Create New Google Cloud Project**

### Step 1: Create New Project
1. Go to Google Cloud Console
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth credentials
5. Download `credentials.json`

### Step 2: Use New Project
1. Use the new project's credentials
2. This completely bypasses the n8n OAuth issues

## 🔧 **Solution 4: Manual Authentication**

### Step 1: Use Existing Token
If you have a working `token.json` file from before:
1. Copy it to your server
2. Test if it still works
3. If expired, try refreshing it

### Step 2: Alternative Authentication
1. Use a different authentication method
2. Consider using service account credentials
3. Or use a different OAuth flow

## 🔧 **Quick Fix Commands**

```bash
# Try the simple API approach
python calendar_auth_simple_api.py

# Check your current credentials
python check_credentials.py

# Try creating new credentials
# (Follow the steps above)
```

## 🔧 **Expected Results**

After fixing the OAuth client:
- No more "n8n's request is invalid" errors
- Successful authentication
- Calendar access working
- iDotMatrix display showing calendar info

The key is to create OAuth credentials specifically for iDotMatrix, not reuse the n8n OAuth client.
