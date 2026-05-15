from pydantic import BaseModel
from datetime import datetime

class InventoryLogResponse(BaseModel):
    id: int
    product_id: int
    change_amount: int
    reason: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class InventoryUpdate(BaseModel):
    product_id: int
    change_amount: int
    reason: str