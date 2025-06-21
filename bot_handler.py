"""
Telegram bot message handler
Manages incoming messages and coordinates with OpenAI service
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from openai_service import OpenAIService
from logging_service import LoggingService
from thread_manager import ThreadManager
from config import Config

class BotHandler:
    """Handles Telegram bot messages and interactions"""
    
    def __init__(self, config: Config):
        self.config = config
        self.openai_service = OpenAIService(config)
        self.logging_service = LoggingService(config)
        self.thread_manager = ThreadManager(config)
        self.logger = logging.getLogger(__name__)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle incoming text messages from users
        
        Args:
            update: Telegram update object containing message data
            context: Telegram bot context
        """
        if not update.message or not update.message.text:
            return
        
        chat_id = update.message.chat_id
        user_message = update.message.text
        user_id = update.message.from_user.id if update.message.from_user else 0
        user_name = update.message.from_user.full_name if update.message.from_user else "Unknown"
        
        self.logger.info(f"Received message from user {user_id} ({user_name}) in chat {chat_id}: {user_message[:100]}...")
        
        # Check whitelist authorization
        if self.config.ALLOWED_USERS and user_id not in self.config.ALLOWED_USERS:
            await context.bot.send_message(
                chat_id=chat_id, 
                text="❌ You don't have access to this bot."
            )
            self.logger.warning(f"Unauthorized access attempt from user {user_id} ({user_name})")
            return
        
        try:
            # Send typing indicator to show bot is processing
            await context.bot.send_chat_action(chat_id=chat_id, action="typing")
            
            # Get or create thread for this user to maintain context
            thread_id = self.thread_manager.get_or_create_thread(user_id)
            
            # Get response from OpenAI Assistant with persistent context
            response = await self.openai_service.get_assistant_response(user_message, thread_id)
            
            # Send response back to user
            await context.bot.send_message(chat_id=chat_id, text=response)
            
            # Log the conversation
            self.logging_service.log_conversation(user_id, user_name, user_message, response)
            
            self.logger.info(f"Successfully sent response to user {user_id} in chat {chat_id}")
            
        except Exception as e:
            error_message = f"❌ Błąd: {str(e)}"
            try:
                await context.bot.send_message(chat_id=chat_id, text=error_message)
            except Exception as send_error:
                self.logger.error(f"Failed to send error message: {send_error}")
            
            self.logger.error(f"Error handling message from user {user_id}: {str(e)}", exc_info=True)
    
    async def handle_error(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle errors in the bot
        
        Args:
            update: The update that caused the error
            context: Telegram bot context
        """
        self.logger.error(f"Update {update} caused error: {context.error}")
        
        # If we have a chat_id, send error message to user
        if update and hasattr(update, 'message') and hasattr(update, 'message') and update.message:
            chat_id = update.message.chat_id
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="❌ An unexpected error occurred. Please try again later."
                )
            except Exception as send_error:
                self.logger.error(f"Failed to send error message: {send_error}")
