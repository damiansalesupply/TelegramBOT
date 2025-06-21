"""
Logging service for conversation tracking
Handles CSV and Google Sheets logging functionality
"""

import csv
import logging
import os
from datetime import datetime
from typing import Optional, Any
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import Config


class LoggingService:
    """Service for logging conversations to CSV and Google Sheets"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._worksheet = None
        self._sheets_initialized = False
        
        # Initialize CSV file with headers if it doesn't exist
        if self.config.ENABLE_CSV_LOGGING:
            self._initialize_csv()
    
    def _initialize_csv(self) -> None:
        """Initialize CSV file with headers if it doesn't exist"""
        csv_file = "conversation_log.csv"
        if not os.path.exists(csv_file):
            try:
                with open(csv_file, mode="w", encoding="utf-8", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Timestamp", "User ID", "User Name", "Question", "Answer"])
                self.logger.info("Created CSV log file with headers")
            except Exception as e:
                self.logger.error(f"Failed to create CSV file: {str(e)}")
    
    def _get_worksheet(self) -> Optional[Any]:
        """Get Google Sheets worksheet connection"""
        if not self.config.ENABLE_SHEETS_LOGGING:
            return None
            
        if self._worksheet is not None:
            return self._worksheet
            
        if not self._sheets_initialized:
            try:
                # Check if credentials file exists
                if not os.path.exists(self.config.CREDENTIALS_FILE):
                    self.logger.warning(f"Google Sheets credentials file not found: {self.config.CREDENTIALS_FILE}")
                    self._sheets_initialized = True
                    return None
                
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    self.config.CREDENTIALS_FILE, scope  # type: ignore
                )
                client = gspread.authorize(creds)  # type: ignore
                sheet = client.open(self.config.SHEET_NAME).sheet1
                self._worksheet = sheet
                self.logger.info(f"Connected to Google Sheets: {self.config.SHEET_NAME}")
                
            except Exception as e:
                self.logger.error(f"Failed to connect to Google Sheets: {str(e)}")
                self._worksheet = None
            
            self._sheets_initialized = True
        
        return self._worksheet
    
    def log_conversation(self, user_id: int, user_name: str, question: str, answer: str) -> None:
        """
        Log conversation to both CSV and Google Sheets
        
        Args:
            user_id: Telegram user ID
            user_name: User's full name
            question: User's question
            answer: Bot's response
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log to CSV
        if self.config.ENABLE_CSV_LOGGING:
            self._log_to_csv(timestamp, user_id, user_name, question, answer)
        
        # Log to Google Sheets
        if self.config.ENABLE_SHEETS_LOGGING:
            self._log_to_sheets(timestamp, user_id, user_name, question, answer)
    
    def _log_to_csv(self, timestamp: str, user_id: int, user_name: str, question: str, answer: str) -> None:
        """Log conversation to CSV file"""
        try:
            with open("conversation_log.csv", mode="a", encoding="utf-8", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, user_id, user_name, question, answer])
            self.logger.debug(f"Logged conversation to CSV for user {user_id}")
        except Exception as e:
            self.logger.error(f"Failed to log to CSV: {str(e)}")
    
    def _log_to_sheets(self, timestamp: str, user_id: int, user_name: str, question: str, answer: str) -> None:
        """Log conversation to Google Sheets"""
        try:
            worksheet = self._get_worksheet()
            if worksheet is None:
                return
            
            row = [timestamp, str(user_id), user_name, question, answer]
            worksheet.append_row(row)
            self.logger.debug(f"Logged conversation to Google Sheets for user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to log to Google Sheets: {str(e)}")