#!/bin/bash
# Deployment script for Telegram bot with proper environment setup

set -e

echo "Starting bot deployment..."

# Install dependencies
echo "Installing dependencies..."
uv add python-telegram-bot aiohttp psutil

# Set environment for production deployment
export ENVIRONMENT=production
export PORT=${PORT:-8080}

# Auto-detect Cloud Run environment and set webhook URL
if [ -n "$K_SERVICE" ] && [ -n "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "Detected Cloud Run environment"
    export WEBHOOK_URL="https://${K_SERVICE}-${GOOGLE_CLOUD_PROJECT}.a.run.app/webhook"
    echo "Webhook URL set to: $WEBHOOK_URL"
fi

# Kill any existing bot instances
echo "Checking for existing bot instances..."
pkill -f "python.*main.py" || true
pkill -f "python.*start.py" || true

# Start the bot
echo "Starting bot..."
python start.py