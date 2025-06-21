"""
OpenAI Assistant API service
Handles communication with OpenAI Assistant API for intelligent responses
"""

import logging
import asyncio
from typing import Optional
from openai import OpenAI
from config import Config

class OpenAIService:
    """Service for interacting with OpenAI Assistant API"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.logger = logging.getLogger(__name__)
    
    async def get_assistant_response(self, user_message: str) -> str:
        """
        Get response from OpenAI Assistant
        
        Args:
            user_message: The user's message to process
            
        Returns:
            Assistant's response as a string
            
        Raises:
            Exception: If the API call fails or times out
        """
        try:
            self.logger.debug(f"Creating thread for message: {user_message[:50]}...")
            
            # Create a new thread for this conversation
            thread = self.client.beta.threads.create()
            self.logger.debug(f"Created thread: {thread.id}")
            
            # Add the user's message to the thread
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_message
            )
            
            # Create and start a run with the assistant
            run = self.client.beta.threads.runs.create(
                assistant_id=self.config.ASSISTANT_ID,
                thread_id=thread.id
            )
            
            self.logger.debug(f"Started run: {run.id}")
            
            # Wait for the run to complete with timeout
            response_text = await self._wait_for_completion(thread.id, run.id)
            
            self.logger.info("Successfully got response from OpenAI Assistant")
            return response_text
            
        except Exception as e:
            self.logger.error(f"Error getting assistant response: {str(e)}")
            raise Exception("Failed to get response from AI assistant. Please try again.")
    
    async def _wait_for_completion(self, thread_id: str, run_id: str) -> str:
        """
        Wait for the assistant run to complete and return the response
        
        Args:
            thread_id: The thread ID
            run_id: The run ID
            
        Returns:
            The assistant's response text
            
        Raises:
            Exception: If the run fails, is cancelled, or times out
        """
        start_time = asyncio.get_event_loop().time()
        retry_count = 0
        
        while retry_count < self.config.MAX_RETRIES:
            try:
                # Check if we've exceeded the timeout
                elapsed_time = asyncio.get_event_loop().time() - start_time
                if elapsed_time > self.config.TIMEOUT_SECONDS:
                    raise Exception(f"Assistant response timed out after {self.config.TIMEOUT_SECONDS} seconds")
                
                # Check the run status
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, 
                    run_id=run_id
                )
                
                self.logger.debug(f"Run status: {run_status.status}")
                
                if run_status.status == "completed":
                    # Get the assistant's response
                    messages = self.client.beta.threads.messages.list(thread_id=thread_id)
                    
                    if not messages.data:
                        raise Exception("No response received from assistant")
                    
                    # Get the latest assistant message
                    for message in messages.data:
                        if message.role == "assistant":
                            if message.content and len(message.content) > 0:
                                content = message.content[0]
                                if hasattr(content, 'text') and hasattr(content.text, 'value'):
                                    return content.text.value
                    
                    raise Exception("No valid response content found")
                
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    error_msg = f"Assistant run {run_status.status}"
                    if hasattr(run_status, 'last_error') and run_status.last_error:
                        error_msg += f": {run_status.last_error}"
                    raise Exception(error_msg)
                
                elif run_status.status in ["queued", "in_progress", "cancelling"]:
                    # Still processing, wait a bit
                    await asyncio.sleep(1)
                    continue
                
                else:
                    # Unknown status, wait and retry
                    self.logger.warning(f"Unknown run status: {run_status.status}")
                    await asyncio.sleep(1)
                    continue
                    
            except Exception as e:
                retry_count += 1
                if retry_count >= self.config.MAX_RETRIES:
                    raise e
                
                self.logger.warning(f"Retry {retry_count}/{self.config.MAX_RETRIES} after error: {str(e)}")
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
        
        raise Exception(f"Failed to get assistant response after {self.config.MAX_RETRIES} retries")
