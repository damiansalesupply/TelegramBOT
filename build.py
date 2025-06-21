#!/usr/bin/env python3
"""
Build script for Replit deployment with environment detection
"""

import os
import sys
import subprocess
import asyncio
from telegram.ext import Application

def clear_webhook():
    """Clear webhook configuration"""
    try:
        token = os.getenv("TELEGRAM_TOKEN")
        if not token:
            print("Warning: TELEGRAM_TOKEN not found")
            return
            
        import requests
        url = f"https://api.telegram.org/bot{token}/deleteWebhook"
        response = requests.post(url, data={"drop_pending_updates": True})
        if response.status_code == 200:
            print("Webhook cleared successfully")
        else:
            print(f"Warning: Could not clear webhook: {response.text}")
    except Exception as e:
        print(f"Warning: Could not clear webhook: {e}")

def main():
    """Main build function"""
    print("🚀 Starting deployment process...")
    
    # Step 1: Kill existing processes
    print("🔄 Stopping existing bot instances...")
    try:
        subprocess.run(["pkill", "-f", "python.*bot"], check=False)
        subprocess.run(["pkill", "-f", "python.*simple_bot"], check=False)
    except:
        pass
    
    # Step 2: Clear webhook
    print("🧹 Clearing webhook configuration...")
    clear_webhook()
    
    # Step 3: Set environment and start bot
    os.environ["ALLOWED_USERS"] = "7668792787"
    
    print("🤖 Starting bot...")
    if not os.getenv("PORT"):
        print("Dev mode detected: using polling")
        subprocess.run([sys.executable, "simple_bot.py"])
    else:
        print("Prod mode detected: using webhook")
        subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    main()