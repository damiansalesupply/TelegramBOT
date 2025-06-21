#!/usr/bin/env python3
"""
Simplified Telegram bot without webhook conflicts
Pure polling mode implementation
"""

import logging
import sys
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from config import Config
from bot_handler import BotHandler
from command_handler import CommandHandler as BotCommandHandler
from thread_manager import ThreadManager
from utils import setup_logging

def main():
    """Main function to start the Telegram bot in pure polling mode"""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Load configuration
        config = Config()
        config.validate()
        
        logger.info("Starting Telegram bot...")
        logger.info(f"Bot will use Assistant ID: {config.ASSISTANT_ID}")
        
        # Initialize components
        bot_handler = BotHandler(config)
        thread_manager = ThreadManager(config)
        command_handler = BotCommandHandler(config, thread_manager)
        
        # Create application
        application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("reset", command_handler.handle_reset))
        application.add_handler(CommandHandler("stats", command_handler.handle_stats))
        
        # Add message handler for text messages (excluding commands)
        message_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            bot_handler.handle_message
        )
        application.add_handler(message_handler)
        
        # Add error handler
        application.add_error_handler(bot_handler.handle_error)
        
        # Log configuration
        logger.info(f"Configuration: {config}")
        if config.ALLOWED_USERS:
            logger.info(f"Whitelist enabled with {len(config.ALLOWED_USERS)} authorized users")
        else:
            logger.info("Whitelist disabled - all users allowed")
        
        logger.info("Starting bot in polling mode...")
        logger.info("Bot started successfully. Listening for messages...")
        
        # Run the bot with simple polling - will clear webhooks automatically
        application.run_polling(
            allowed_updates=["message"],
            drop_pending_updates=True
        )
        
    except Exception as e:
        logging.error(f"Failed to start bot: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()