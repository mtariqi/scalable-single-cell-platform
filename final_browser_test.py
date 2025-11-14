# Create a final browser test script
import requests
import webbrowser
import time
import sys
import subprocess

print("🎯 FINAL BROWSER ACCESS TEST")
print("===========================")

# Test the server
urls = ["http://localhost:8501", "http://127.0.0.1:8501"]

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ {url} - Server responding (HTTP {response.status_code})")
        
        # Check if it's Streamlit
        if 'streamlit' in response.text.lower():
            print("   ↳ Streamlit application detected")
        
    except Exception as e:
        print(f"❌ {url} - Connection failed: {e}")
        sys.exit(1)

print("\n🚀 ATTEMPTING TO OPEN IN BROWSER...")

# Try multiple browsers
browsers = [
    ['firefox'],
    ['google-chrome', '--incognito'],
    ['chromium-browser', '--incognito']
]

browser_opened = False
for browser in browsers:
    browser_name = browser[0]
    try:
        print(f"   Trying {browser_name}...")
        cmd = browser + ['http://localhost:8501']
        subprocess.Popen(cmd)
        browser_opened = True
        time.sleep(2)
        break
    except Exception as e:
        print(f"   {browser_name} failed: {e}")

# Fallback to webbrowser module
if not browser_opened:
    print("   Trying default browser...")
    webbrowser.open('http://localhost:8501')

print("\n📋 MANUAL ACCESS INSTRUCTIONS:")
print("1. OPEN FIREFOX BROWSER (most reliable)")
print("2. Go to: http://localhost:8501")
print("3. Wait 20-30 seconds for Streamlit to fully load")
print("4. If blank page, check browser console (F12) for errors")
print("\n⚡ QUICK FIXES:")
print("   - Use Firefox instead of Chrome")
print("   - Use incognito/private mode")
print("   - Try http://127.0.0.1:8501")
print("   - Wait patiently - first load can take 30+ seconds")

print("\n🎉 PLATFORM STATUS: RUNNING AND ACCESSIBLE")

