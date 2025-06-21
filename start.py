#!/usr/bin/env python3
"""
Production webhook mode for Telegram bot
"""

import os
import logging
import sys
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from config import Config
from bot_handler import BotHandler
from command_handler import CommandHandler as BotCommandHandler
from thread_manager import ThreadManager
from utils import setup_logging

def start_bot_with_webhook():
    """Start bot in webhook mode for production"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = Config()
        config.validate()
        
        logger.info("Starting Telegram bot in webhook mode...")
        logger.info(f"Bot will use Assistant ID: {config.ASSISTANT_ID}")
        
        # Initialize components
        bot_handler = BotHandler(config)
        thread_manager = ThreadManager(config)
        command_handler = BotCommandHandler(config, thread_manager)
        
        # Create application
        if not config.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN is required")
            
        application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("reset", command_handler.handle_reset))
        application.add_handler(CommandHandler("stats", command_handler.handle_stats))
        
        # Add message handler
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
        
        # Set environment variables
        os.environ["ALLOWED_USERS"] = "7668792787"
        
        # Get webhook URL
        webhook_url = config.WEBHOOK_URL
        if not webhook_url:
            logger.error("WEBHOOK_URL not configured for production")
            sys.exit(1)
            
        logger.info(f"Starting webhook server on port {config.PORT}")
        logger.info(f"Webhook URL: {webhook_url}")
        
        # Start webhook mode
        application.run_webhook(
            listen="0.0.0.0",
            port=config.PORT,
            webhook_url=webhook_url,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start webhook bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_bot_with_webhook()