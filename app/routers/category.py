"""Category router."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

async def get_category_service() -> CategoryService:
    """Dependency injection for CategoryService."""
    return CategoryService()

@router.get("", response_model=List[Category])
@router.get("/", response_model=List[Category])
async def list_categories(
    service: CategoryService = Depends(get_category_service)
) -> List[Category]:
    """Get all categories."""
    return await service.list_categories()

@router.post("", response_model=Category)
@router.post("/", response_model=Category)
async def create_category(
    category: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
) -> Category:
    """Create a new category."""
    return await service.create_category(category)

@router.get("/{category_id}", response_model=Category)
async def get_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service)
) -> Category:
    """Get a category by ID."""
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: UUID,
    category: CategoryUpdate,
    service: CategoryService = Depends(get_category_service)
) -> Category:
    """Update a category."""
    updated_category = await service.update_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service)
) -> dict:
    """Delete a category."""
    if await service.delete_category(category_id):
        return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=404, detail="Category not found") 