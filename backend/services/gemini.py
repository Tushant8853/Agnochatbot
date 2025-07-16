import google.generativeai as genai
from typing import List, Dict, Any, Optional
from config import settings
from utils.logger import logger

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)

class GeminiService:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            self.model = None
        self.chat = None
    
    def start_chat(self, context: str = "") -> None:
        """Start a new chat session with optional context."""
        if context:
            self.chat = self.model.start_chat(history=[
                {"role": "user", "parts": [f"Context: {context}"]},
                {"role": "model", "parts": ["I understand the context and will use it to provide relevant responses."]}
            ])
        else:
            self.chat = self.model.start_chat()
    
    async def generate_response(
        self, 
        message: str, 
        context: str = "", 
        memory_context: str = ""
    ) -> str:
        """Generate a response using Gemini with context and memory."""
        try:
            print("Message ::::::",message)
            # Prepare the full context
            full_context = ""
            if context:
                full_context += f"System Context: {context}\n\n"
            if memory_context:
                full_context += f"Memory Context: {memory_context}\n\n"
            
            if full_context:
                # Start a new chat with context
                self.start_chat(full_context)
                if self.chat:
                    response = self.chat.send_message(message)
                else:
                    return "I apologize, but I'm experiencing technical difficulties. Please try again."
            else:
                # Use existing chat or start new one
                if not self.chat:
                    self.start_chat()
                if self.chat:
                    response = self.chat.send_message(message)
                else:
                    return "I apologize, but I'm experiencing technical difficulties. Please try again."
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."
    
    async def generate_response_without_chat(
        self, 
        message: str, 
        context: str = ""
    ) -> str:
        """Generate a response without maintaining chat history."""
        try:
            prompt = message
            if context:
                prompt = f"Context: {context}\n\nUser: {message}"
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."

# Global instance
gemini_service = GeminiService() 