#!/usr/bin/env python3
"""
Force exclusive bot access by terminating other instances
"""

import asyncio
import time
from telegram.ext import Application
from config import Config

async def force_exclusive_access():
    """Aggressively claim exclusive bot access"""
    config = Config()
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    print("🔄 Forcing exclusive bot access...")
    
    for attempt in range(10):
        try:
            print(f"Attempt {attempt + 1}/10...")
            
            # Clear webhook completely
            await application.bot.delete_webhook(drop_pending_updates=True)
            print("  ✓ Webhook cleared")
            
            # Wait for other instances to timeout
            await asyncio.sleep(2)
            
            # Rapidly consume updates to force other instances to disconnect
            for i in range(5):
                updates = await application.bot.get_updates(limit=100, timeout=1)
                if updates:
                    print(f"  ✓ Consumed {len(updates)} updates")
                await asyncio.sleep(0.5)
            
            # Test exclusive access
            test_updates = await application.bot.get_updates(limit=1, timeout=2)
            print(f"  ✓ Exclusive access confirmed!")
            return True
            
        except Exception as e:
            if "terminated by other getUpdates request" in str(e):
                print(f"  ⚠️ Still conflicted (attempt {attempt + 1})")
                await asyncio.sleep(3)
            else:
                print(f"  ❌ Error: {e}")
                await asyncio.sleep(1)
    
    print("❌ Could not establish exclusive access after 10 attempts")
    return False

async def main():
    """Main function"""
    print("=== Bot Conflict Resolution ===\n")
    
    success = await force_exclusive_access()
    
    if success:
        print("\n🎉 SUCCESS: Bot has exclusive access!")
        print("You can now restart your bot workflow.")
    else:
        print("\n❌ FAILED: Could not resolve conflict")
        print("Other bot instance is persistent - check:")
        print("1. Other Replit deployments")
        print("2. Local development environments") 
        print("3. Cloud deployments")

if __name__ == "__main__":
    asyncio.run(main())