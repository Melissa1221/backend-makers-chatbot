"""AI-powered recommendation service."""
from datetime import datetime
from typing import List, Dict, Optional
import numpy as np
from app.db.supabase import get_supabase
from app.models.recommendation import RecommendationType
from app.services.product_service import ProductService
from app.services.recommendation_service import RecommendationService

class AIRecommendationService:
    """AI-powered recommendation service."""

    def __init__(self):
        """Initialize service with dependencies."""
        self.supabase = get_supabase()
        self.product_service = ProductService()
        self.recommendation_service = RecommendationService()

    async def _calculate_content_score(self, user_preferences: Dict, product_data: Dict) -> float:
        """Calculate content-based similarity score."""
        score = 0.0
        
        # Category matching
        if user_preferences.get('preferred_categories'):
            if product_data['category_id'] in user_preferences['preferred_categories']:
                score += 0.3

        # Label matching
        if user_preferences.get('preferred_labels'):
            matching_labels = set(product_data['labels']).intersection(
                set(user_preferences['preferred_labels'])
            )
            score += len(matching_labels) * 0.2

        # Price range matching
        if user_preferences.get('price_range'):
            min_price, max_price = user_preferences['price_range']
            if min_price <= product_data['price'] <= max_price:
                score += 0.2

        # Specs matching
        if user_preferences.get('preferred_specs'):
            for spec_key, spec_value in user_preferences['preferred_specs'].items():
                if product_data['specs'].get(spec_key) == spec_value:
                    score += 0.1

        return min(score, 1.0)

    async def _get_user_preferences(self, user_id: int) -> Dict:
        """Get user preferences from interaction history."""
        # Get user's purchase history
        purchase_history = self.supabase.table('user_purchases')\
            .select('product_id')\
            .eq('user_id', user_id)\
            .execute()

        # Get user's viewed products
        viewed_products = self.supabase.table('user_views')\
            .select('product_id')\
            .eq('user_id', user_id)\
            .execute()

        # Get details of interacted products
        interacted_products = []
        for product_id in [p['product_id'] for p in purchase_history.data + viewed_products.data]:
            product = await self.product_service.get_product(product_id)
            if product:
                interacted_products.append(product)

        if not interacted_products:
            return {}

        # Extract preferences
        preferences = {
            'preferred_categories': [],
            'preferred_labels': [],
            'price_range': (0, 0),
            'preferred_specs': {}
        }

        # Analyze product interactions to build preferences
        prices = []
        category_counts = {}
        label_counts = {}
        spec_counts = {}

        for product in interacted_products:
            # Track categories
            if product.category_id:
                category_counts[product.category_id] = category_counts.get(product.category_id, 0) + 1

            # Track labels
            for label in product.labels:
                label_counts[label] = label_counts.get(label, 0) + 1

            # Track prices
            prices.append(product.price)

            # Track specs
            for key, value in product.specs.items():
                if key not in spec_counts:
                    spec_counts[key] = {}
                spec_counts[key][value] = spec_counts[key].get(value, 0) + 1

        # Set preferred categories (top 2)
        preferences['preferred_categories'] = sorted(
            category_counts.keys(),
            key=lambda x: category_counts[x],
            reverse=True
        )[:2]

        # Set preferred labels (top 3)
        preferences['preferred_labels'] = sorted(
            label_counts.keys(),
            key=lambda x: label_counts[x],
            reverse=True
        )[:3]

        # Set price range
        if prices:
            avg_price = np.mean(prices)
            std_price = np.std(prices) if len(prices) > 1 else avg_price * 0.2
            preferences['price_range'] = (
                max(0, avg_price - std_price),
                avg_price + std_price
            )

        # Set preferred specs (most common value for each key)
        for spec_key, value_counts in spec_counts.items():
            most_common = max(value_counts.items(), key=lambda x: x[1])[0]
            preferences['preferred_specs'][spec_key] = most_common

        return preferences

    async def generate_recommendations(self, user_id: int) -> None:
        """Generate AI-powered recommendations for a user."""
        # Get user preferences
        user_preferences = await self._get_user_preferences(user_id)

        # Get all products
        products = await self.product_service.list_products()

        # Calculate scores for each product
        for product in products:
            product_data = {
                'id': product.id,
                'category_id': product.category_id,
                'labels': product.labels,
                'price': product.price,
                'specs': product.specs or {}
            }

            # Calculate content-based score
            score = await self._calculate_content_score(user_preferences, product_data)

            # Determine recommendation type based on score
            if score >= 0.7:
                rec_type = RecommendationType.HIGHLY_RECOMMENDED
            elif score >= 0.4:
                rec_type = RecommendationType.RECOMMENDED
            else:
                rec_type = RecommendationType.NOT_RECOMMENDED

            # Update recommendation in database
            await self.recommendation_service.update_product_recommendation(
                product_id=product.id,
                recommendation_type=rec_type,
                score=score
            ) 