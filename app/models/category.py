"""Category models."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class CategoryBase(BaseModel):
    """Base category model."""
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Category creation model."""
    pass

class CategoryUpdate(CategoryBase):
    """Category update model."""
    name: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    """Complete category model."""
    id: UUID
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True 