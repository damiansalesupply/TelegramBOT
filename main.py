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