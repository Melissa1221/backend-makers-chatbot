"""Recommendation service with Supabase integration."""
from datetime import datetime
from typing import Dict, List, Optional
from app.db.supabase import get_supabase
from app.models.recommendation import RecommendationType, ProductRecommendation, UserRecommendations

class RecommendationService:
    """Service for managing product recommendations."""

    def __init__(self):
        """Initialize service with Supabase client."""
        self.supabase = get_supabase()

    async def get_user_recommendations(self, user_id: int) -> UserRecommendations:
        """Get recommendations for a user."""
        # Get all recommendations ordered by score
        result = self.supabase.table('product_recommendations')\
            .select('*')\
            .order('score', desc=True)\
            .execute()

        if not result.data:
            return UserRecommendations(updated_at=datetime.utcnow())

        # Group products by recommendation type
        recommendations = UserRecommendations(
            highly_recommended=[],
            recommended=[],
            not_recommended=[],
            updated_at=datetime.utcnow()
        )

        for item in result.data:
            score = item['score']
            product_id = item['product_id']
            
            # Classify based on score
            if score >= 0.7:
                recommendations.highly_recommended.append(product_id)
            elif score >= 0.4:
                recommendations.recommended.append(product_id)
            else:
                recommendations.not_recommended.append(product_id)

        return recommendations

    async def update_product_recommendation(
        self,
        product_id: int,
        recommendation_type: RecommendationType,
        score: float
    ) -> Optional[ProductRecommendation]:
        """Update or create a product recommendation."""
        data = {
            'product_id': product_id,
            'recommendation_type': recommendation_type,
            'score': score,
            'updated_at': datetime.utcnow().isoformat()
        }

        result = self.supabase.table('product_recommendations')\
            .upsert(data, on_conflict='product_id')\
            .execute()

        if not result.data:
            return None

        return ProductRecommendation(**result.data[0])

    async def get_product_recommendation(
        self,
        product_id: int
    ) -> Optional[ProductRecommendation]:
        """Get recommendation for a specific product."""
        result = self.supabase.table('product_recommendations')\
            .select('*')\
            .eq('product_id', product_id)\
            .execute()

        if not result.data:
            return None

        return ProductRecommendation(**result.data[0])

    async def get_recommendations_by_type(
        self,
        recommendation_type: RecommendationType
    ) -> List[ProductRecommendation]:
        """Get all products with a specific recommendation type."""
        result = self.supabase.table('product_recommendations')\
            .select('*')\
            .eq('recommendation_type', recommendation_type)\
            .order('score', desc=True)\
            .execute()

        return [ProductRecommendation(**item) for item in result.data] 