#!/usr/bin/env python3
"""
Telegram Bot with OpenAI Assistant API Integration
Main entry point with mode selection
"""

import os

def main():
    """Main function to select deployment mode"""
    
    # Detect environment
    IS_AUTOSCALE = os.getenv("PORT") is not None
    
    if IS_AUTOSCALE:
        print("🔗 Production mode detected: starting webhook")
        from start import start_bot_with_webhook
        start_bot_with_webhook()
    else:
        print("🔄 Development mode detected: starting polling")
        from simple_bot import start_bot_with_polling
        start_bot_with_polling()

if __name__ == '__main__':
    main()

# Global application instance for graceful shutdown
app_instance = None

async def health_check(request):
    """Health check endpoint for Cloud Run"""
    return web.Response(text="OK", status=200)

async def webhook_handler(request):
    """Handle webhook updates from Telegram"""
    try:
        if not app_instance:
            return web.Response(status=500, text="Bot not initialized")
            
        update_data = await request.json()
        update = Update.de_json(update_data, app_instance.bot)
        
        # Process the update through the application
        await app_instance.process_update(update)
        return web.Response(status=200)
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return web.Response(status=500)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger = logging.getLogger(__name__)
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    if app_instance:
        asyncio.create_task(app_instance.stop())
    sys.exit(0)

async def setup_webhook(config, application):
    """Setup webhook for production deployment"""
    logger = logging.getLogger(__name__)
    
    if not config.WEBHOOK_URL:
        logger.warning("WEBHOOK_URL not set, skipping webhook setup for now")
        logger.info("Webhook will be configured once deployment URL is available")
        return
    
    try:
        # Set webhook
        await application.bot.set_webhook(url=config.WEBHOOK_URL)
        logger.info(f"Webhook set to: {config.WEBHOOK_URL}")
    except Exception as e:
        logger.warning(f"Failed to set webhook: {e}")
        logger.info("Webhook can be configured manually after deployment")

async def run_webhook_server(config, application):
    """Run webhook server for production"""
    logger = logging.getLogger(__name__)
    
    # Create web application
    web_app = web.Application()
    web_app.router.add_post("/webhook", webhook_handler)
    web_app.router.add_get("/health", health_check)
    web_app.router.add_get("/", health_check)
    
    # Start webhook server
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", config.PORT)
    await site.start()
    
    logger.info(f"Webhook server started on port {config.PORT}")
    logger.info("Bot is ready to receive webhook updates")
    
    # Keep the server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down webhook server...")
        await runner.cleanup()

def main():
    """Main function to start the Telegram bot"""
    global app_instance
    
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Load configuration
        config = Config()
        config.validate()
        
        logger.info("Starting Telegram bot...")
        logger.info(f"Environment: {config.ENVIRONMENT}")
        logger.info(f"Bot will use Assistant ID: {config.ASSISTANT_ID}")
        
        # Initialize components
        bot_handler = BotHandler(config)
        thread_manager = ThreadManager(config)
        command_handler = BotCommandHandler(config, thread_manager)
        
        # Create application with proper token validation
        if not config.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN is required")
            
        application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        app_instance = application
        
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
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Choose deployment mode based on environment
        if config.USE_WEBHOOKS:
            logger.info("Starting bot in production mode with webhooks...")
            logger.info(f"Server will bind to port {config.PORT}")
            
            # Run webhook mode asynchronously
            async def run_production():
                await setup_webhook(config, application)
                await run_webhook_server(config, application)
            
            asyncio.run(run_production())
        else:
            logger.error("Polling mode not supported in production - use webhook mode")
            logger.error("This should only run in development with simple_bot.py")
            sys.exit(1)
        
    except Exception as e:
        logging.error(f"Failed to start bot: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
