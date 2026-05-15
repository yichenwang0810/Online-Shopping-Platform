from pydantic import BaseModel
from .product import ProductResponse

class WishlistItemCreate(BaseModel):
    product_id: int

class WishlistItemResponse(BaseModel):
    id: int
    product: ProductResponse
    
    class Config:
        from_attributes = True