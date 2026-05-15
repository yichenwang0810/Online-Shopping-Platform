# app/services/coupon_service.py
from sqlalchemy.orm import Session
from app.models import Coupon
from app.schemas import CouponCreate
from fastapi import HTTPException

class CouponService:
    def __init__(self, db: Session):
        self.db = db

    def validate_coupon(self, code: str) -> float:
        """
        Validates a coupon code and returns the discount percentage.
        Raises HTTPException if invalid.
        """
        coupon = self.db.query(Coupon).filter(
            Coupon.code == code,
            Coupon.is_active == True
        ).first()

        if not coupon:
            raise HTTPException(status_code=404, detail="Invalid or inactive coupon code")
        
        # Check usage limit
        if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
            raise HTTPException(status_code=400, detail="Coupon usage limit exceeded")
        
        return coupon.discount_percent

    def create_coupon(self, coupon_data: CouponCreate) -> Coupon:
        db_coupon = Coupon(**coupon_data.dict())
        self.db.add(db_coupon)
        self.db.commit()
        self.db.refresh(db_coupon)
        return db_coupon

    def apply_coupon(self, code: str):
        coupon = self.db.query(Coupon).filter(
            Coupon.code == code,
            Coupon.is_active == True
        ).first()
        
        if coupon:
            coupon.used_count += 1
            self.db.commit()
            self.db.refresh(coupon)
        
        return coupon