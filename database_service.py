"""
Database service for the Telegram bot
Handles all database operations including conversation logging and thread management
"""

import logging
from datetime import datetime
from typing import Optional, List, Dict
from models import DatabaseManager, User, ConversationLog, UserThread

class DatabaseService:
    """Service for handling all database operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.db_manager = DatabaseManager()
            self.logger.info("Database connection established")
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise
    
    def create_or_update_user(self, telegram_id: int, username: str = None, 
                             first_name: str = None, last_name: str = None) -> None:
        """Create or update user in database"""
        session = self.db_manager.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            
            if user:
                # Update existing user
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.last_seen = datetime.utcnow()
            else:
                # Create new user
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_authorized=True
                )
                session.add(user)
            
            session.commit()
            self.logger.debug(f"User {telegram_id} created/updated in database")
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create/update user {telegram_id}: {e}")
        finally:
            self.db_manager.close_session(session)
    
    def log_conversation(self, user_id: int, user_name: str, question: str, 
                        answer: str, thread_id: str = None, response_time: int = None) -> None:
        """Log conversation to database"""
        session = self.db_manager.get_session()
        try:
            conversation = ConversationLog(
                user_id=user_id,
                user_name=user_name,
                question=question,
                answer=answer,
                thread_id=thread_id,
                response_time=response_time
            )
            session.add(conversation)
            session.commit()
            self.logger.debug(f"Conversation logged for user {user_id}")
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to log conversation for user {user_id}: {e}")
        finally:
            self.db_manager.close_session(session)
    
    def get_user_thread(self, user_id: int) -> Optional[str]:
        """Get thread ID for user"""
        session = self.db_manager.get_session()
        try:
            user_thread = session.query(UserThread).filter(UserThread.user_id == user_id).first()
            return user_thread.thread_id if user_thread else None
            
        except Exception as e:
            self.logger.error(f"Failed to get thread for user {user_id}: {e}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def create_user_thread(self, user_id: int, thread_id: str) -> None:
        """Create or update user thread"""
        session = self.db_manager.get_session()
        try:
            user_thread = session.query(UserThread).filter(UserThread.user_id == user_id).first()
            
            if user_thread:
                # Update existing thread
                user_thread.thread_id = thread_id
                user_thread.updated_at = datetime.utcnow()
            else:
                # Create new thread
                user_thread = UserThread(
                    user_id=user_id,
                    thread_id=thread_id
                )
                session.add(user_thread)
            
            session.commit()
            self.logger.debug(f"Thread {thread_id} created/updated for user {user_id}")
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create/update thread for user {user_id}: {e}")
        finally:
            self.db_manager.close_session(session)
    
    def clear_user_thread(self, user_id: int) -> bool:
        """Clear thread for user"""
        session = self.db_manager.get_session()
        try:
            user_thread = session.query(UserThread).filter(UserThread.user_id == user_id).first()
            
            if user_thread:
                session.delete(user_thread)
                session.commit()
                self.logger.debug(f"Thread cleared for user {user_id}")
                return True
            else:
                return False
                
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to clear thread for user {user_id}: {e}")
            return False
        finally:
            self.db_manager.close_session(session)
    
    def get_conversation_stats(self) -> Dict[str, int]:
        """Get conversation statistics"""
        session = self.db_manager.get_session()
        try:
            total_conversations = session.query(ConversationLog).count()
            total_users = session.query(User).count()
            active_threads = session.query(UserThread).count()
            
            return {
                'total_conversations': total_conversations,
                'total_users': total_users,
                'active_threads': active_threads
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get conversation stats: {e}")
            return {'total_conversations': 0, 'total_users': 0, 'active_threads': 0}
        finally:
            self.db_manager.close_session(session)
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations"""
        session = self.db_manager.get_session()
        try:
            conversations = session.query(ConversationLog)\
                .order_by(ConversationLog.timestamp.desc())\
                .limit(limit)\
                .all()
            
            return [
                {
                    'user_id': conv.user_id,
                    'user_name': conv.user_name,
                    'question': conv.question[:100] + '...' if len(conv.question) > 100 else conv.question,
                    'timestamp': conv.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'thread_id': conv.thread_id
                }
                for conv in conversations
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to get recent conversations: {e}")
            return []
        finally:
            self.db_manager.close_session(session)