"""
Command handler for bot administrative commands
Handles special commands like /reset, /stats, etc.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from thread_manager import ThreadManager
from config import Config


class CommandHandler:
    """Handles bot administrative commands"""
    
    def __init__(self, config: Config, thread_manager: ThreadManager):
        self.config = config
        self.thread_manager = thread_manager
        self.logger = logging.getLogger(__name__)
    
    async def handle_reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Reset conversation context for the user"""
        if not update.message:
            return
            
        user_id = update.message.from_user.id if update.message.from_user else 0
        chat_id = update.message.chat_id
        
        # Check authorization
        if self.config.ALLOWED_USERS and user_id not in self.config.ALLOWED_USERS:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ You don't have access to this bot."
            )
            return
        
        # Clear user's thread
        cleared = self.thread_manager.clear_user_thread(user_id)
        
        if cleared:
            await context.bot.send_message(
                chat_id=chat_id,
                text="✅ Conversation context has been reset. Starting fresh!"
            )
            self.logger.info(f"Reset conversation context for user {user_id}")
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="ℹ️ No conversation context to reset."
            )
    
    async def handle_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show bot statistics (admin only)"""
        if not update.message:
            return
            
        user_id = update.message.from_user.id if update.message.from_user else 0
        chat_id = update.message.chat_id
        
        # Check authorization
        if self.config.ALLOWED_USERS and user_id not in self.config.ALLOWED_USERS:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ You don't have access to this bot."
            )
            return
        
        # Get thread statistics
        stats = self.thread_manager.get_thread_stats()
        
        stats_message = (
            f"📊 Bot Statistics:\n"
            f"• Active conversations: {stats['active_users']}\n"
            f"• Total threads: {stats['total_threads']}\n"
            f"• CSV logging: {'✅' if self.config.ENABLE_CSV_LOGGING else '❌'}\n"
            f"• Sheets logging: {'✅' if self.config.ENABLE_SHEETS_LOGGING else '❌'}\n"
            f"• Whitelist: {'✅' if self.config.ALLOWED_USERS else '❌ (All users allowed)'}"
        )
        
        await context.bot.send_message(chat_id=chat_id, text=stats_message)
        self.logger.info(f"Showed stats to user {user_id}")