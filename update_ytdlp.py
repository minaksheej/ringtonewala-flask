#!/usr/bin/env python3
"""
Script to update yt-dlp to the latest version
This helps resolve YouTube download issues that occur due to outdated yt-dlp versions
"""

import subprocess
import sys
import os

def update_ytdlp():
    print("🔄 Updating yt-dlp to the latest version...")
    print("This may help resolve YouTube download issues.\n")
    
    try:
        # Update yt-dlp using pip
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"
        ], capture_output=True, text=True, check=True)
        
        print("✅ yt-dlp updated successfully!")
        print("📋 Update output:")
        print(result.stdout)
        
        # Check the new version
        version_result = subprocess.run([
            sys.executable, "-m", "yt_dlp", "--version"
        ], capture_output=True, text=True, check=True)
        
        print(f"📦 Current yt-dlp version: {version_result.stdout.strip()}")
        
    except subprocess.CalledProcessError as e:
        print("❌ Error updating yt-dlp:")
        print(f"Return code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🎵 YouTube to Audio Converter - yt-dlp Updater")
    print("=" * 50)
    
    success = update_ytdlp()
    
    if success:
        print("\n🎉 Update completed! You can now restart your Flask app.")
        print("💡 If you're still having issues, try:")
        print("   1. Wait a few minutes before trying again")
        print("   2. Try with a different YouTube video")
        print("   3. Check if the video is publicly available")
    else:
        print("\n❌ Update failed. You may need to manually update yt-dlp.")
        print("Try running: pip install --upgrade yt-dlp")
