from typing import List
import numpy as np
from datetime import datetime
from app.db.supabase import get_supabase_client
from app.models.product import Product
from app.models.recommendation import RecommendationType, ProductRecommendation, ProductRecommendationResponse

class RecommendationService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def get_all_products(self) -> List[Product]:
        response = self.supabase.table('products').select("*").execute()
        products = []
        for item in response.data:
            item['specs'] = item.get('specs', {})
            item['labels'] = item.get('labels', [])
            products.append(Product(**item))
        return products

    def calculate_product_features(self, product: Product) -> np.ndarray:
        features = np.array([
            float(product.price),
            len(product.description),
            product.rating or 0.0,
            product.stock,
            len(product.specs or {}),
            len(product.labels or [])
        ])
        return features

    def classify_recommendation(self, score: float) -> RecommendationType:
        if score >= 150:
            return RecommendationType.HIGHLY_RECOMMENDED
        elif score >= 50:
            return RecommendationType.RECOMMENDED
        else:
            return RecommendationType.NOT_RECOMMENDED

    def update_recommendations(self):
        products = self.get_all_products()
        
        
        recommendations = []
        for product in products:
            features = self.calculate_product_features(product)
            
            
            score = np.mean(features)  
            
            rec_type = self.classify_recommendation(score)
            
            recommendation = ProductRecommendation(
                product_id=product.id,
                recommendation_type=rec_type,
                score=float(score),
                updated_at=datetime.now()
            )
            recommendations.append(recommendation)

        for rec in recommendations:
            self.supabase.table('product_recommendations').upsert({
                'product_id': rec.product_id,
                'recommendation_type': rec.recommendation_type,
                'score': rec.score,
                'updated_at': rec.updated_at.isoformat()
            }).execute()

    def get_recommendations(self) -> List[ProductRecommendationResponse]:
        query = """
        SELECT pr.*, p.name as product_name 
        FROM product_recommendations pr
        JOIN products p ON p.id = pr.product_id
        ORDER BY pr.score DESC
        """
        response = self.supabase.table('product_recommendations').select("*").execute()
        
        recommendations = []
        for rec in response.data:
            product_data = self.supabase.table('products').select("name").eq('id', rec['product_id']).single().execute()
            recommendations.append(
                ProductRecommendationResponse(
                    product_id=rec['product_id'],
                    product_name=product_data.data['name'],
                    recommendation_type=rec['recommendation_type'],
                    score=rec['score'],
                    updated_at=rec['updated_at']
                )
            )
        return recommendations

    def get_recommendations_by_type(self, rec_type: str) -> List[ProductRecommendationResponse]:
        response = self.supabase.table('product_recommendations').select("*").eq('recommendation_type', rec_type).execute()
        
        recommendations = []
        for rec in response.data:
            product_data = self.supabase.table('products').select("name").eq('id', rec['product_id']).single().execute()
            recommendations.append(
                ProductRecommendationResponse(
                    product_id=rec['product_id'],
                    product_name=product_data.data['name'],
                    recommendation_type=rec['recommendation_type'],
                    score=rec['score'],
                    updated_at=rec['updated_at']
                )
            )
        return recommendations