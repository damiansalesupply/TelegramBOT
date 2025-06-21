"""
Thread management service for maintaining conversation context per user
Handles persistent thread storage and retrieval
"""

import logging
import json
import os
from typing import Dict, Optional
from openai import OpenAI
from config import Config
from database_service import DatabaseService


class ThreadManager:
    """Manages conversation threads for each user to maintain context"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.logger = logging.getLogger(__name__)
        
        # Initialize database service with fallback to file storage
        try:
            self.db_service = DatabaseService()
            self.logger.info("ThreadManager using database backend")
        except Exception as e:
            self.logger.warning(f"Database not available, using file backend: {e}")
            self.db_service = None
            self.threads_file = "user_threads.json"
            self._user_threads: Dict[int, str] = {}
            self._load_threads()
    
    def _load_threads(self) -> None:
        """Load existing threads from file"""
        try:
            if os.path.exists(self.threads_file):
                with open(self.threads_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert string keys back to int
                    self._user_threads = {int(k): v for k, v in data.items()}
                self.logger.info(f"Loaded {len(self._user_threads)} existing threads")
            else:
                self.logger.info("No existing threads file found, starting fresh")
        except Exception as e:
            self.logger.error(f"Failed to load threads: {str(e)}")
            self._user_threads = {}
    
    def _save_threads(self) -> None:
        """Save threads to file"""
        try:
            # Convert int keys to string for JSON serialization
            data = {str(k): v for k, v in self._user_threads.items()}
            with open(self.threads_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.logger.debug("Saved threads to file")
        except Exception as e:
            self.logger.error(f"Failed to save threads: {str(e)}")
    
    def get_or_create_thread(self, user_id: int) -> str:
        """
        Get existing thread for user or create a new one
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Thread ID for the user
        """
        if user_id in self._user_threads:
            thread_id = self._user_threads[user_id]
            self.logger.debug(f"Using existing thread {thread_id} for user {user_id}")
            return thread_id
        
        try:
            # Create new thread
            thread = self.client.beta.threads.create()
            thread_id = thread.id
            
            # Store and save
            self._user_threads[user_id] = thread_id
            self._save_threads()
            
            self.logger.info(f"Created new thread {thread_id} for user {user_id}")
            return thread_id
            
        except Exception as e:
            self.logger.error(f"Failed to create thread for user {user_id}: {str(e)}")
            raise Exception("Failed to create conversation thread")
    
    def clear_user_thread(self, user_id: int) -> bool:
        """
        Clear thread for a specific user (for reset functionality)
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if thread was cleared, False if no thread existed
        """
        if user_id in self._user_threads:
            del self._user_threads[user_id]
            self._save_threads()
            self.logger.info(f"Cleared thread for user {user_id}")
            return True
        return False
    
    def get_thread_stats(self) -> Dict[str, int]:
        """Get statistics about managed threads"""
        return {
            "total_threads": len(self._user_threads),
            "active_users": len(self._user_threads)
        }