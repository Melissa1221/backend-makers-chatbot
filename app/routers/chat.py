"""Chat router for handling chat interactions."""

from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from ..services.auth import get_current_active_user
from ..services.chat import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])

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

@router.post("/send", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    current_user: dict = Depends(get_current_active_user),
):
    """Send a message to the chatbot."""
    response = await chat_service.send_message(current_user, message.message)
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
            
            # Get user (in a real app, you'd validate the client_id)
            user = {"username": client_id, "id": 0}  # Simplified for demo
            
            # Process message and get response
            response = await chat_service.send_message(user, message)
            
            # Send response back
            await websocket.send_text(response)
            
    except WebSocketDisconnect:
        # Handle disconnect
        pass 