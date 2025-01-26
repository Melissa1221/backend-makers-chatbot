"""Product models."""
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    """Base product model."""
    name: str
    price: float = Field(..., ge=0)
    description: Optional[str] = None
    stock: int = Field(default=0, ge=0)
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    """Product creation model."""
    specs: Dict[str, str] = Field(default_factory=dict)
    labels: List[str] = Field(default_factory=list)

class ProductUpdate(ProductBase):
    """Product update model."""
    name: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    specs: Optional[Dict[str, str]] = None
    labels: Optional[List[str]] = None

class Product(ProductBase):
    """Complete product model."""
    id: int
    specs: Dict[str, str]
    labels: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True 