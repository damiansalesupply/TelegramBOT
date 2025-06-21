#!/usr/bin/env python3
"""
Simple deployment script with conflict prevention
"""

import asyncio
import subprocess
import sys
import os
from telegram.ext import Application
from config import Config

async def stop_existing_instances():
    """Stop any existing bot instances"""
    print("Stopping existing bot instances...")
    try:
        subprocess.run(["pkill", "-f", "python.*bot"], check=False)
        subprocess.run(["pkill", "-f", "python.*simple_bot"], check=False)
        await asyncio.sleep(2)
        print("Existing instances stopped")
    except Exception as e:
        print(f"Warning: Could not stop instances: {e}")

async def clear_webhook():
    """Clear webhook configuration"""
    print("Clearing webhook configuration...")
    try:
        config = Config()
        app = Application.builder().token(config.TELEGRAM_TOKEN).build()
        result = await app.bot.delete_webhook(drop_pending_updates=True)
        print(f"Webhook cleared: {result}")
    except Exception as e:
        print(f"Warning: Could not clear webhook: {e}")

def start_bot():
    """Start the bot based on environment"""
    print("Starting bot...")
    
    # Set environment variables
    os.environ["ALLOWED_USERS"] = "7668792787"
    
    # Check if we're in production (Cloud Run)
    if os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("K_SERVICE"):
        print("Production environment detected - using webhook mode")
        subprocess.run([sys.executable, "start.py"])
    else:
        print("Development environment - using polling mode")
        subprocess.run([sys.executable, "simple_bot.py"])

async def main():
    """Main deployment function"""
    print("🚀 Starting deployment with conflict prevention...")
    
    await stop_existing_instances()
    await clear_webhook()
    start_bot()

if __name__ == "__main__":
    asyncio.run(main())