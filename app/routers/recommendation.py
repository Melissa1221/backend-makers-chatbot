"""Recommendation router."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.recommendation import (
    RecommendationType,
    ProductRecommendation,
    UserRecommendations
)
from app.services.recommendation_service import RecommendationService
from app.services.ai_recommendation_service import AIRecommendationService

router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["recommendations"]
)

async def get_recommendation_service() -> RecommendationService:
    """Dependency injection for RecommendationService."""
    return RecommendationService()

async def get_ai_recommendation_service() -> AIRecommendationService:
    """Dependency injection for AIRecommendationService."""
    return AIRecommendationService()

@router.post("/generate/{user_id}")
async def generate_recommendations(
    user_id: int,
    service: AIRecommendationService = Depends(get_ai_recommendation_service)
) -> dict:
    """Generate AI-powered recommendations for a user."""
    await service.generate_recommendations(user_id)
    return {"message": "Recommendations generated successfully"}

@router.post("/track/view/{user_id}/{product_id}")
async def track_product_view(
    user_id: int,
    product_id: int,
    service: AIRecommendationService = Depends(get_ai_recommendation_service)
) -> dict:
    """Track when a user views a product."""
    result = service.supabase.table('user_views').upsert(
        {
            'user_id': user_id,
            'product_id': product_id,
            'viewed_at': 'now()',
            'view_count': 1
        },
        on_conflict='(user_id,product_id)',
        update_columns=['viewed_at', 'view_count']
    ).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to track product view")
    
    return {"message": "Product view tracked successfully"}

@router.post("/track/purchase/{user_id}/{product_id}")
async def track_product_purchase(
    user_id: int,
    product_id: int,
    service: AIRecommendationService = Depends(get_ai_recommendation_service)
) -> dict:
    """Track when a user purchases a product."""
    result = service.supabase.table('user_purchases').insert(
        {
            'user_id': user_id,
            'product_id': product_id
        }
    ).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to track product purchase")
    
    return {"message": "Product purchase tracked successfully"}

@router.get("/user/{user_id}", response_model=UserRecommendations)
async def get_user_recommendations(
    user_id: int,
    service: RecommendationService = Depends(get_recommendation_service)
) -> UserRecommendations:
    """Get personalized recommendations for a user."""
    return await service.get_user_recommendations(user_id)

@router.get("/product/{product_id}", response_model=ProductRecommendation)
async def get_product_recommendation(
    product_id: int,
    service: RecommendationService = Depends(get_recommendation_service)
) -> ProductRecommendation:
    """Get recommendation for a specific product."""
    recommendation = await service.get_product_recommendation(product_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation

@router.get("/type/{recommendation_type}", response_model=List[ProductRecommendation])
async def get_recommendations_by_type(
    recommendation_type: RecommendationType,
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[ProductRecommendation]:
    """Get all products with a specific recommendation type."""
    return await service.get_recommendations_by_type(recommendation_type)

@router.put("/product/{product_id}", response_model=ProductRecommendation)
async def update_product_recommendation(
    product_id: int,
    recommendation_type: RecommendationType,
    score: float,
    service: RecommendationService = Depends(get_recommendation_service)
) -> ProductRecommendation:
    """Update recommendation for a product."""
    recommendation = await service.update_product_recommendation(
        product_id=product_id,
        recommendation_type=recommendation_type,
        score=score
    )
    if not recommendation:
        raise HTTPException(status_code=404, detail="Failed to update recommendation")
    return recommendation 