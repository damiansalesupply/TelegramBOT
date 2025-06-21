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
        
        # Get webhook URL with auto-generation
        webhook_url = config.WEBHOOK_URL
        
        # Auto-generate from Replit if not set
        if not webhook_url:
            replit_url = os.environ.get("REPLIT_WEB_HOSTNAME")
            if replit_url:
                webhook_url = f"https://{replit_url}/webhook"
                logger.info(f"Auto-generated webhook URL: {webhook_url}")
            else:
                logger.error("WEBHOOK_URL not set and REPLIT_WEB_HOSTNAME not available")
                sys.exit(1)
            
        logger.info(f"Starting webhook server on port {config.PORT}")
        logger.info(f"Webhook URL: {webhook_url}")
        
        logger.info("✅ All init done. Running application.run_webhook...")
        
        # Start webhook mode
        try:
            application.run_webhook(
                listen="0.0.0.0",
                port=config.PORT,
                webhook_url=webhook_url,
                webhook_path="/",
                drop_pending_updates=True
            )
        except Exception as e:
            logger.exception(f"❌ run_webhook crashed with error: {e}")
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"Failed to start webhook bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if os.getenv("PORT"):
        start_bot_with_webhook()
    else:
        print("Error: This script is intended for production (PORT must be set)")
        sys.exit(1)