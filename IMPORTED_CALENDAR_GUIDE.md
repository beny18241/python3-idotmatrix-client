# 📥 Working with Imported Calendars

This guide explains how to access events from imported calendars (calendars from other people) with your iDotMatrix device.

## 🔍 Understanding Imported Calendars

### What are Imported Calendars?
- Calendars shared by other people/organizations
- You have "reader" access (can see events, can't modify)
- Examples: Team calendars, company calendars, shared family calendars

### Why They're Tricky
- You can't share them with the service account (you don't own them)
- The service account needs explicit permission to access them
- Only the calendar owner can share them with the service account

## 🚀 Solutions for Imported Calendars

### Option 1: Ask Calendar Owner to Share
**Best solution if possible:**

1. Contact the person who owns the imported calendar
2. Ask them to share it with your service account email
3. They need to:
   - Go to their Google Calendar settings
   - Share the calendar with your service account email
   - Set permission to "See all event details"

### Option 2: Use Your Own Calendar Access
**Works if you have the events in your own calendar:**

1. Subscribe to the imported calendar in your Google Calendar
2. The events will appear in your own calendar
3. Share your own calendar with the service account
4. The service account can then see the events

### Option 3: Manual Event Copying
**If you can't get service account access:**

1. Manually copy important events to your own calendar
2. Use your own calendar with the service account
3. This gives you control over which events to display

## 🔧 Technical Setup

### Step 1: Setup All Accessible Calendars
```bash
# Setup with all calendars you have access to
python setup_all_calendars.py
```

### Step 2: Test Access
```bash
# Test if you can access imported calendars
python calendar_display_imported.py DD:4F:93:46:DF:1A current
```

### Step 3: Display Events
```bash
# Display current meeting from any accessible calendar
python calendar_display_imported.py DD:4F:93:46:DF:1A current

# Display next meeting from any accessible calendar
python calendar_display_imported.py DD:4F:93:46:DF:1A next
```

## 🎯 Expected Results

### If Imported Calendar is Accessible:
```
✅ Accessible calendar: Team Calendar (reader)
📅 Current meeting: Team Meeting @ 14:30
```

### If Imported Calendar is Not Accessible:
```
❌ Cannot access: Team Calendar (reader)
📅 No meetings found
```

## 🛠️ Troubleshooting

### "No calendars accessible"
- Make sure you've shared your own calendars with the service account
- Check that the service account email is correct
- Wait a few minutes for permissions to propagate

### "Cannot access imported calendar"
- The imported calendar owner needs to share it with your service account
- You can't share someone else's calendar yourself
- Consider copying important events to your own calendar

### "Service account file not found"
- Run `python calendar_service_account.py` first
- Make sure `service-account.json` exists

## 📋 Quick Links

- [Google Calendar](https://calendar.google.com)
- [Calendar Settings](https://calendar.google.com/calendar/r/settings)
- [Google Cloud Console](https://console.cloud.google.com)

## 🎉 Success!

Once set up, you'll have:
- ✅ Access to your own calendars
- ✅ Access to imported calendars (if shared with service account)
- ✅ iDotMatrix device displaying events from all sources
- ✅ Smart fallback between multiple calendars
