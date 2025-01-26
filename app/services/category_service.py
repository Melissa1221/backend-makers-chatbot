"""Category service with Supabase integration."""
from typing import List, Optional
from app.db.supabase import get_supabase
from app.models.category import CategoryCreate, CategoryUpdate, Category

class CategoryService:
    """Category service with Supabase integration."""

    def __init__(self):
        """Initialize service with Supabase client."""
        self.supabase = get_supabase()

    async def create_category(self, category: CategoryCreate) -> Category:
        """Create a new category."""
        result = self.supabase.table('categories').insert({
            'name': category.name,
            'description': category.description
        }).execute()
        
        return Category(**result.data[0])

    async def get_category(self, category_id: int) -> Optional[Category]:
        """Get a category by ID."""
        result = self.supabase.table('categories').select('*').eq('id', category_id).execute()
        if not result.data:
            return None
        return Category(**result.data[0])

    async def list_categories(self) -> List[Category]:
        """Get all categories."""
        result = self.supabase.table('categories').select('*').execute()
        return [Category(**data) for data in result.data]

    async def update_category(self, category_id: int, category: CategoryUpdate) -> Optional[Category]:
        """Update a category."""
        update_data = category.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_category(category_id)

        result = self.supabase.table('categories').update(
            update_data
        ).eq('id', category_id).execute()
        
        if not result.data:
            return None
        return Category(**result.data[0])

    async def delete_category(self, category_id: int) -> bool:
        """Delete a category."""
        result = self.supabase.table('categories').delete().eq('id', category_id).execute()
        return bool(result.data) 