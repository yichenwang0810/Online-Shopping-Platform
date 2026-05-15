from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_admin_user
from app.services import CouponService
from app.schemas import CouponCreate, CouponApply, CouponResponse

router = APIRouter(prefix="/coupons", tags=["coupons"])

@router.post("/apply")
def apply_coupon(coupon_data: CouponApply, db: Session = Depends(get_db)):
    service = CouponService(db)
    discount = service.validate_coupon(coupon_data.code)
    return {"message": "Coupon valid", "discount_percent": discount}

@router.post("/", response_model=CouponResponse)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db), current_user = Depends(get_current_admin_user)):
    service = CouponService(db)
    return service.create_coupon(coupon)