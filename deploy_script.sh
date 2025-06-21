#!/bin/bash

# Production deployment script with conflict prevention
echo "🚀 Starting deployment process..."

# Step 1: Kill any existing bot instances
echo "🔄 Stopping existing bot instances..."
pkill -f "python.*bot" || echo "No existing instances found"
pkill -f "python.*simple_bot" || echo "No simple_bot instances found"

# Wait for processes to terminate
sleep 2

# Step 2: Clear webhook to prevent conflicts
echo "🧹 Clearing webhook configuration..."
python -c "
import asyncio
from telegram.ext import Application
from config import Config

async def clear_webhook():
    config = Config()
    app = Application.builder().token(config.TELEGRAM_TOKEN).build()
    result = await app.bot.delete_webhook(drop_pending_updates=True)
    print(f'Webhook cleared: {result}')

asyncio.run(clear_webhook())
" || echo "Warning: Could not clear webhook"

# Step 3: Start the bot
echo "🤖 Starting bot in production mode..."
if [ "$PORT" ] || [ "$GOOGLE_CLOUD_PROJECT" ] || [ "$K_SERVICE" ]; then
    echo "Production environment detected - using webhook mode"
    ALLOWED_USERS=7668792787 python start.py
else
    echo "Development environment - using polling mode"
    ALLOWED_USERS=7668792787 python simple_bot.py
fi