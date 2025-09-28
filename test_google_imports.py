#!/usr/bin/env python3
"""
Test Google Calendar imports
"""

print("🔍 Testing Google Calendar imports...")

try:
    import google.auth.transport.requests
    print("✅ google.auth.transport.requests")
except ImportError as e:
    print("❌ google.auth.transport.requests:", e)

try:
    import google.oauth2.credentials
    print("✅ google.oauth2.credentials")
except ImportError as e:
    print("❌ google.oauth2.credentials:", e)

try:
    import google_auth_oauthlib.flow
    print("✅ google_auth_oauthlib.flow")
except ImportError as e:
    print("❌ google_auth_oauthlib.flow:", e)

try:
    import googleapiclient.discovery
    print("✅ googleapiclient.discovery")
except ImportError as e:
    print("❌ googleapiclient.discovery:", e)

print("\n🔍 Python path:")
import sys
for path in sys.path:
    print(f"  {path}")

print("\n🔍 Installed packages:")
import pkg_resources
installed_packages = [d.project_name for d in pkg_resources.working_set]
google_packages = [pkg for pkg in installed_packages if 'google' in pkg.lower()]
for pkg in google_packages:
    print(f"  {pkg}")
