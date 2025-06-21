"""
Configuration management for the Telegram bot
Handles environment variables and validation
"""

import os
from typing import Optional

class Config:
    """Configuration class for managing environment variables"""
    
    def __init__(self):
        self.TELEGRAM_TOKEN: Optional[str] = os.getenv("TELEGRAM_TOKEN")
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.ASSISTANT_ID: Optional[str] = os.getenv("ASSISTANT_ID")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
        self.TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "60"))
    
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
            f"LOG_LEVEL={self.LOG_LEVEL})"
        )
