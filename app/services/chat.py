"""Chat service integrating with LangChain chatbot."""

from typing import Dict, Any
from langchain_core.messages import HumanMessage
from ecommerce_chatbot.chatbot import create_chatbot
from .store import store

class ChatService:
    """Service for handling chat interactions."""
    
    def __init__(self):
        """Initialize chat service."""
        self._chatbot = create_chatbot()
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    def _get_or_create_session(self, username: str) -> Dict[str, Any]:
        """Get or create a chat session for a user."""
        if username not in self._sessions:
            self._sessions[username] = {
                "config": {"configurable": {"thread_id": f"user_{username}"}},
                "conversation_history": []
            }
        return self._sessions[username]
    
    async def send_message(
        self,
        user: dict,
        message: str
    ) -> str:
        """Send a message to the chatbot and store the interaction."""
        # Get or create user session
        session = self._get_or_create_session(user["username"])
        
        # Create message and add to history
        user_message = HumanMessage(content=message)
        session["conversation_history"].append(user_message)
        
        # Get chatbot response
        response_content = ""
        async for chunk, _ in self._chatbot.astream(
            {"messages": session["conversation_history"]},
            session["config"],
            stream_mode="messages"
        ):
            if hasattr(chunk, 'content'):
                response_content += chunk.content
        
        # Store chat history
        store.add_chat_message(user["username"], message, response_content)
        
        return response_content
    
    def get_chat_history(self, user: dict) -> list[dict]:
        """Get chat history for a user."""
        return store.get_chat_history(user["username"])

# Create a singleton instance
chat_service = ChatService() 