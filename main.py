#!/usr/bin/env python3
"""
Telegram Bot with OpenAI Assistant API Integration
Main entry point for the application
"""

import logging
import sys
from telegram.ext import Application, MessageHandler, filters
from config import Config
from bot_handler import BotHandler
from utils import setup_logging

def main():
    """Main function to start the Telegram bot"""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Load configuration
        config = Config()
        config.validate()
        
        logger.info("Starting Telegram bot...")
        logger.info(f"Bot will use Assistant ID: {config.ASSISTANT_ID}")
        
        # Initialize bot handler
        bot_handler = BotHandler(config)
        
        # Create application
        application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        
        # Add message handler for text messages (excluding commands)
        message_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            bot_handler.handle_message
        )
        application.add_handler(message_handler)
        
        # Add error handler
        application.add_error_handler(bot_handler.handle_error)
        
        logger.info("Bot started successfully. Listening for messages...")
        
        # Run the bot
        application.run_polling(
            allowed_updates=["message"],
            drop_pending_updates=True
        )
        
    except Exception as e:
        logging.error(f"Failed to start bot: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
