#!/usr/bin/env python3
"""
Fix webhook conflicts permanently
"""

import asyncio
import logging
from telegram.ext import Application
from config import Config

async def clear_webhook_permanently():
    """Clear webhook and prevent auto-setting"""
    config = Config()
    
    # Create application
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    try:
        # Delete webhook
        await application.bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook deleted successfully")
        
        # Get webhook info to confirm
        webhook_info = await application.bot.get_webhook_info()
        print(f"Webhook URL: '{webhook_info.url}'")
        print(f"Pending updates: {webhook_info.pending_update_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(clear_webhook_permanently())