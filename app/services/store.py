"""In-memory data store for the application."""

from typing import Dict, List
from datetime import datetime

class DataStore:
    """Simple in-memory data store."""
    
    def __init__(self):
        """Initialize empty data store."""
        self.users: Dict[str, dict] = {}  # username -> user data
        self.chat_history: Dict[str, List[dict]] = {}  # username -> list of messages
        
    def add_user(self, username: str, email: str, hashed_password: str) -> dict:
        """Add a new user."""
        if username in self.users:
            return None
        user = {
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
            "id": len(self.users) + 1
        }
        self.users[username] = user
        self.chat_history[username] = []
        return user
    
    def get_user(self, username: str) -> dict:
        """Get user by username."""
        return self.users.get(username)
    
    def add_chat_message(self, username: str, message: str, response: str):
        """Add a chat message to history."""
        if username not in self.chat_history:
            self.chat_history[username] = []
        
        self.chat_history[username].append({
            "message": message,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_chat_history(self, username: str) -> List[dict]:
        """Get chat history for a user."""
        return self.chat_history.get(username, [])

# Create singleton instance
store = DataStore() 