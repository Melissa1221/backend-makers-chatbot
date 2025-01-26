"""Pydantic schemas for data validation."""

from pydantic import BaseModel, EmailStr
from typing import Optional, List

class ProductBase(BaseModel):
    """Base product schema."""
    name: str
    description: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass

class Product(ProductBase):
    """Schema for product response."""
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str

class User(UserBase):
    """Schema for user response."""
    id: int
    is_admin: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for JWT token."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for token data."""
    username: Optional[str] = None

class ChatMessage(BaseModel):
    """Schema for chat messages."""
    message: str

class ChatResponse(BaseModel):
    """Schema for chat responses."""
    response: str

class ChatHistoryEntry(BaseModel):
    """Schema for chat history entries."""
    message: str
    response: str
    timestamp: str

    class Config:
        from_attributes = True

class ChatHistoryResponse(BaseModel):
    """Schema for chat history response."""
    history: List[ChatHistoryEntry] 