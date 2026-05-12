# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Wishlist Schemas ---
class WishlistItemCreate(BaseModel):
    product_id: int

class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    
    class Config:
        from_attributes = True

# --- Coupon Schemas ---
class CouponCreate(BaseModel):
    code: str
    discount_percent: float

class CouponApply(BaseModel):
    code: str

# --- Inventory Schema ---
class InventoryLogResponse(BaseModel):
    id: int
    product_id: int
    change_amount: int
    reason: str
    timestamp: datetime
    
    class Config:
        from_attributes = True