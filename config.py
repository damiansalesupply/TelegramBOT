"""
Configuration management for the Telegram bot
Handles environment variables and validation
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for managing environment variables"""
    
    def __init__(self):
        self.TELEGRAM_TOKEN: Optional[str] = os.getenv("TELEGRAM_TOKEN")
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.ASSISTANT_ID: Optional[str] = os.getenv("ASSISTANT_ID")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
        self.TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "60"))
        
        # New features configuration
        self.SHEET_NAME: str = os.getenv("SHEET_NAME", "SupportLogs")
        self.ALLOWED_USERS: list = self._parse_allowed_users(os.getenv("ALLOWED_USERS", ""))
        self.ENABLE_CSV_LOGGING: bool = os.getenv("ENABLE_CSV_LOGGING", "true").lower() == "true"
        self.ENABLE_SHEETS_LOGGING: bool = os.getenv("ENABLE_SHEETS_LOGGING", "true").lower() == "true"
        self.CREDENTIALS_FILE: str = os.getenv("CREDENTIALS_FILE", "credentials.json")
    
    def _parse_allowed_users(self, users_str: str) -> list:
        """Parse comma-separated user IDs from environment variable"""
        if not users_str.strip():
            return []
        try:
            return [int(user_id.strip()) for user_id in users_str.split(",") if user_id.strip()]
        except ValueError:
            return []
    
    def validate(self) -> None:
        """Validate that all required environment variables are set"""
        required_vars = {
            "TELEGRAM_TOKEN": self.TELEGRAM_TOKEN,
            "OPENAI_API_KEY": self.OPENAI_API_KEY,
            "ASSISTANT_ID": self.ASSISTANT_ID
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please check your .env file or environment configuration."
            )
    
    def __repr__(self) -> str:
        return (
            f"Config(TELEGRAM_TOKEN={'*' * 10 if self.TELEGRAM_TOKEN else 'None'}, "
            f"OPENAI_API_KEY={'*' * 10 if self.OPENAI_API_KEY else 'None'}, "
            f"ASSISTANT_ID={self.ASSISTANT_ID}, "
            f"LOG_LEVEL={self.LOG_LEVEL}, "
            f"ALLOWED_USERS={len(self.ALLOWED_USERS)} users, "
            f"CSV_LOGGING={self.ENABLE_CSV_LOGGING}, "
            f"SHEETS_LOGGING={self.ENABLE_SHEETS_LOGGING})"
        )
