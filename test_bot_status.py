#!/usr/bin/env python3
"""
Test bot functionality and status
"""

import asyncio
import time
from telegram.ext import Application
from config import Config

async def test_bot_connection():
    """Test basic bot connection and info"""
    config = Config()
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    try:
        # Get bot info
        bot_info = await application.bot.get_me()
        print(f"✅ Bot connected: @{bot_info.username} ({bot_info.first_name})")
        
        # Check webhook status
        webhook_info = await application.bot.get_webhook_info()
        print(f"📡 Webhook URL: {webhook_info.url or 'None (polling mode)'}")
        print(f"📊 Pending updates: {webhook_info.pending_update_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Bot connection failed: {e}")
        return False

async def test_assistant_connection():
    """Test OpenAI Assistant connection"""
    try:
        from openai_service import OpenAIService
        config = Config()
        openai_service = OpenAIService(config)
        
        # Test a simple query
        response = await openai_service.get_assistant_response("Test connection", None)
        print(f"✅ Assistant connected: {len(response)} chars response")
        return True
        
    except Exception as e:
        print(f"❌ Assistant connection failed: {e}")
        return False

async def main():
    """Run all status tests"""
    print("=== Bot Status Check ===\n")
    
    bot_ok = await test_bot_connection()
    assistant_ok = await test_assistant_connection()
    
    print(f"\n=== Summary ===")
    print(f"Bot API: {'✅ Working' if bot_ok else '❌ Failed'}")
    print(f"Assistant: {'✅ Working' if assistant_ok else '❌ Failed'}")
    
    if bot_ok and assistant_ok:
        print("\n🎉 All systems operational!")
        print("Bot should be ready to receive messages.")
    else:
        print("\n⚠️ Some systems need attention.")

if __name__ == "__main__":
    asyncio.run(main())