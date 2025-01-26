from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import List

class RecommendationType(str, Enum):
    HIGHLY_RECOMMENDED = "Highly Recommended"
    RECOMMENDED = "Recommended"
    NOT_RECOMMENDED = "Not Recommended"

class ProductRecommendation(BaseModel):
    product_id: int
    recommendation_type: RecommendationType
    score: float
    updated_at: datetime

class ProductRecommendationResponse(BaseModel):
    product_id: int
    product_name: str
    recommendation_type: str
    score: float
    updated_at: datetime

class RecommendationListResponse(BaseModel):
    recommendations: List[ProductRecommendationResponse]