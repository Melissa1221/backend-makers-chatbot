"""Product router."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.product import Product, ProductCreate, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

async def get_product_service() -> ProductService:
    """Dependency injection for ProductService."""
    return ProductService()

@router.get("", response_model=List[Product])
@router.get("/", response_model=List[Product])
async def list_products(
    service: ProductService = Depends(get_product_service)
) -> List[Product]:
    """Get all products."""
    return await service.list_products()

@router.post("", response_model=Product)
@router.post("/", response_model=Product)
async def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
) -> Product:
    """Create a new product."""
    return await service.create_product(product)

@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
) -> Product:
    """Get a product by ID."""
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service)
) -> Product:
    """Update a product."""
    updated_product = await service.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
) -> dict:
    """Delete a product."""
    if await service.delete_product(product_id):
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/category/{category_id}", response_model=List[Product])
async def list_products_by_category(
    category_id: int,
    service: ProductService = Depends(get_product_service)
) -> List[Product]:
    """Get all products in a specific category."""
    return await service.get_products_by_category(category_id)

@router.get("/label/{label_name}", response_model=List[Product])
async def list_products_by_label(
    label_name: str,
    service: ProductService = Depends(get_product_service)
) -> List[Product]:
    """Get all products with a specific label."""
    return await service.get_products_by_label(label_name) 
