#!/usr/bin/env python3
"""
Startup script for Telegram bot with proper environment handling
Ensures single instance and proper port configuration for deployment
"""

import os
import sys
import psutil
import logging
from pathlib import Path

def kill_existing_instances():
    """Kill any existing bot instances to prevent conflicts"""
    current_pid = os.getpid()
    killed_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
                
            cmdline = proc.info['cmdline'] or []
            cmdline_str = ' '.join(cmdline)
            
            # Check if this is another bot instance
            if ('python' in cmdline_str and 
                ('main.py' in cmdline_str or 'start.py' in cmdline_str) and
                'telegram' in cmdline_str.lower()):
                
                logging.info(f"Killing existing bot instance: PID {proc.info['pid']}")
                proc.terminate()
                killed_processes.append(proc.info['pid'])
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return killed_processes

def setup_environment():
    """Setup environment variables for deployment"""
    # Set default environment if not specified
    if not os.getenv('ENVIRONMENT'):
        # Detect if running in Cloud Run or similar production environment
        if os.getenv('K_SERVICE') or os.getenv('GOOGLE_CLOUD_PROJECT'):
            os.environ['ENVIRONMENT'] = 'production'
        elif os.getenv('REPLIT_DB_URL'):
            # Running in Replit environment - use development mode for now
            os.environ['ENVIRONMENT'] = 'development'
        else:
            os.environ['ENVIRONMENT'] = 'development'
    
    # Set webhook URL for production
    if os.getenv('ENVIRONMENT') == 'production':
        if not os.getenv('WEBHOOK_URL'):
            if os.getenv('K_SERVICE'):
                # Auto-generate webhook URL for Cloud Run
                service_url = f"https://{os.getenv('K_SERVICE')}-{os.getenv('GOOGLE_CLOUD_PROJECT')}.a.run.app"
                os.environ['WEBHOOK_URL'] = f"{service_url}/webhook"
            # Note: Replit webhook URL should be set manually when deploying
            # Automatic webhook URL generation removed to prevent conflicts
    
    # Ensure PORT is set
    if not os.getenv('PORT'):
        os.environ['PORT'] = '8080' if os.getenv('ENVIRONMENT') == 'production' else '5000'
    
    logging.info(f"Environment: {os.getenv('ENVIRONMENT')}")
    logging.info(f"Port: {os.getenv('PORT')}")
    if os.getenv('WEBHOOK_URL'):
        logging.info(f"Webhook URL: {os.getenv('WEBHOOK_URL')}")

def main():
    """Main startup function"""
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting bot with deployment fixes...")
    
    # Kill existing instances to prevent conflicts
    killed = kill_existing_instances()
    if killed:
        logger.info(f"Stopped {len(killed)} existing bot instances")
    
    # Setup environment
    setup_environment()
    
    # Import and run the main bot
    try:
        from main import main as bot_main
        bot_main()
    except ImportError as e:
        logger.error(f"Failed to import main bot module: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Bot startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()