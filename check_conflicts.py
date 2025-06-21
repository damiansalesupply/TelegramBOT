#!/usr/bin/env python3
"""
Check for bot conflicts and force exclusive access
"""

import asyncio
import time
from telegram.ext import Application
from config import Config

async def test_polling_conflict():
    """Test if another instance is using polling"""
    config = Config()
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    print("Testing for polling conflicts...")
    
    try:
        # Try to get updates
        updates = await application.bot.get_updates(limit=1, timeout=1)
        print(f"✅ No conflict detected. Got {len(updates)} updates.")
        return False
        
    except Exception as e:
        if "terminated by other getUpdates request" in str(e):
            print(f"❌ CONFLICT: Another bot instance is polling!")
            print(f"Error: {e}")
            return True
        else:
            print(f"❌ Other error: {e}")
            return False

async def force_exclusive_access():
    """Try to force exclusive access by rapid polling"""
    config = Config()
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    print("Attempting to force exclusive access...")
    
    for attempt in range(5):
        try:
            print(f"Attempt {attempt + 1}/5...")
            
            # Clear any pending updates
            await application.bot.delete_webhook(drop_pending_updates=True)
            await asyncio.sleep(1)
            
            # Try to establish exclusive polling
            updates = await application.bot.get_updates(limit=100, timeout=5)
            print(f"Cleared {len(updates)} pending updates")
            
            # Test if we have exclusive access
            test_updates = await application.bot.get_updates(limit=1, timeout=1)
            print(f"✅ Exclusive access established!")
            return True
            
        except Exception as e:
            if "terminated by other getUpdates request" in str(e):
                print(f"Still conflicted, waiting...")
                await asyncio.sleep(2)
            else:
                print(f"Error: {e}")
                await asyncio.sleep(1)
    
    print("❌ Failed to establish exclusive access")
    return False

async def main():
    """Main conflict detection and resolution"""
    print("=== Bot Conflict Detection ===\n")
    
    # Test for conflicts
    has_conflict = await test_polling_conflict()
    
    if has_conflict:
        print("\nConflict detected! Attempting resolution...")
        success = await force_exclusive_access()
        
        if success:
            print("✅ Conflict resolved! Bot should work now.")
        else:
            print("❌ Could not resolve conflict.")
            print("\nPossible solutions:")
            print("1. Stop any local bot instances on your machine")
            print("2. Check other development environments")
            print("3. Wait for the other instance to timeout")
    else:
        print("✅ No conflicts detected. Bot should work fine.")

if __name__ == "__main__":
    asyncio.run(main())