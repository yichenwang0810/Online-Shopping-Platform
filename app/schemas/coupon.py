from pydantic import BaseModel, Field
from typing import Optional

class CouponCreate(BaseModel):
    code: str
    discount_percent: float = Field(..., gt=0, le=100)
    usage_limit: Optional[int] = None

class CouponUpdate(BaseModel):
    code: Optional[str] = None
    discount_percent: Optional[float] = Field(None, gt=0, le=100)
    is_active: Optional[bool] = None
    usage_limit: Optional[int] = None

class CouponResponse(CouponCreate):
    id: int
    is_active: bool
    used_count: int
    
    class Config:
        from_attributes = True

class CouponApply(BaseModel):
    code: str