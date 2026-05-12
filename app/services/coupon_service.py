# app/services/coupon_service.py
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException

class CouponService:
    def __init__(self, db: Session):
        self.db = db

    def validate_coupon(self, code: str) -> float:
        """
        Validates a coupon code and returns the discount percentage.
        Raises HTTPException if invalid.
        """
        coupon = self.db.query(models.Coupon).filter(
            models.Coupon.code == code,
            models.Coupon.is_active == True
        ).first()

        if not coupon:
            raise HTTPException(status_code=404, detail="Invalid or inactive coupon code")
        
        return coupon.discount_percent

    def create_coupon(self, coupon_data: schemas.CouponCreate) -> models.Coupon:
        db_coupon = models.Coupon(**coupon_data.dict())
        self.db.add(db_coupon)
        self.db.commit()
        self.db.refresh(db_coupon)
        return db_coupon