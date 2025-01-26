"""Chat models."""
from pydantic import BaseModel

class ChatMessage(BaseModel):
    """Chat message schema."""
    message: str

class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str 