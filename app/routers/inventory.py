from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_admin_user
from app.models import InventoryLog
from app.schemas import InventoryLogResponse

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/logs/{product_id}", response_model=List[InventoryLogResponse])
def get_inventory_logs(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin_user)):
    logs = db.query(InventoryLog).filter(InventoryLog.product_id == product_id).all()
    return logs