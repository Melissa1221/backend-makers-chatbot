from fastapi import APIRouter, Depends
from typing import List
from app.services.recommendation import RecommendationService
from app.models.recommendation import ProductRecommendationResponse, RecommendationListResponse

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/", response_model=RecommendationListResponse)
async def get_recommendations():
    service = RecommendationService()
    recommendations = service.get_recommendations()
    return RecommendationListResponse(recommendations=recommendations)

@router.get("/by-type/{recommendation_type}", response_model=RecommendationListResponse)
async def get_recommendations_by_type(recommendation_type: str):
    service = RecommendationService()
    recommendations = service.get_recommendations_by_type(recommendation_type)
    return RecommendationListResponse(recommendations=recommendations)