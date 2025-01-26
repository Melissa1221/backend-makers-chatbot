"""Recommendation models."""
from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class RecommendationType(str, Enum):
    """Types of recommendations."""
    HIGHLY_RECOMMENDED = "highly_recommended"
    RECOMMENDED = "recommended"
    NOT_RECOMMENDED = "not_recommended"

class ProductRecommendation(BaseModel):
    """Product recommendation model."""
    product_id: int
    recommendation_type: RecommendationType
    score: float = Field(..., ge=0.0, le=1.0)
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True

class ProductRecommendationResponse(BaseModel):
    product_id: int
    product_name: str
    recommendation_type: str
    score: float
    updated_at: datetime

class RecommendationListResponse(BaseModel):
    recommendations: List[ProductRecommendationResponse]

class UserRecommendations(BaseModel):
    """User recommendations response model."""
    highly_recommended: List[int] = Field(default_factory=list)
    recommended: List[int] = Field(default_factory=list)
    not_recommended: List[int] = Field(default_factory=list)
    updated_at: Optional[datetime] = None