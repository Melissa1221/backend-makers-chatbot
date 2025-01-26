"""Chat router for handling chat interactions."""

from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from ..services.auth import get_current_active_user
from ..services.chat import chat_service
from app.models.chat import ChatMessage, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

class ChatMessage(BaseModel):
    """Chat message schema."""
    message: str

class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str

class ChatHistoryEntry(BaseModel):
    """Chat history entry schema."""
    message: str
    response: str
    timestamp: str

class ChatHistoryResponse(BaseModel):
    """Chat history response schema."""
    history: List[ChatHistoryEntry]

async def get_chat_service() -> ChatService:
    """Dependency injection for ChatService."""
    return ChatService()

@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    """Send a message to the chatbot."""
    response = await service.get_chat_response(message.message)
    return ChatResponse(response=response)

@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    current_user: dict = Depends(get_current_active_user),
):
    """Get chat history for the current user."""
    history = chat_service.get_chat_history(current_user)
    return ChatHistoryResponse(history=history)

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    try:
        while True:
            # Receive message
            message = await websocket.receive_text()
            
            # Get chat service
            service = ChatService()
            
            # Process message and get response
            response = await service.get_chat_response(message)
            
            # Send response back
            await websocket.send_text(response)
            
    except WebSocketDisconnect:
        # Handle disconnect
        pass 