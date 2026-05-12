# app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.dependencies import get_db
from app.services.coupon_service import CouponService
from app.repositories.product_repo import ProductRepository

router = APIRouter()

# --- Existing Product Routes ---
@router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.get_all()

# --- Wishlist Routes ---
@router.get("/wishlist/{user_id}", response_model=List[schemas.WishlistItemResponse])
def get_wishlist(user_id: int, db: Session = Depends(get_db)):
    items = db.query(models.WishlistItem).filter(models.WishlistItem.user_id == user_id).all()
    # Enrich data with product details
    return [
        schemas.WishlistItemResponse(
            id=item.id, 
            product_id=item.product_id, 
            product_name=item.product.name, 
            product_price=item.product.price
        ) 
        for item in items
    ]

@router.post("/wishlist", response_model=schemas.WishlistItemResponse)
def add_to_wishlist(item: schemas.WishlistItemCreate, user_id: int, db: Session = Depends(get_db)):
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db_item = models.WishlistItem(user_id=user_id, product_id=item.product_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return schemas.WishlistItemResponse(
        id=db_item.id, 
        product_id=db_item.product_id, 
        product_name=product.name, 
        product_price=product.price
    )

# --- Coupon Routes ---
@router.post("/coupons/apply")
def apply_coupon(coupon_data: schemas.CouponApply, db: Session = Depends(get_db)):
    service = CouponService(db)
    discount = service.validate_coupon(coupon_data.code)
    return {"message": "Coupon valid", "discount_percent": discount}

@router.post("/coupons", response_model=schemas.CouponCreate)
def create_coupon(coupon: schemas.CouponCreate, db: Session = Depends(get_db)):
    service = CouponService(db)
    return service.create_coupon(coupon)

# --- Inventory History Route ---
@router.get("/inventory/logs/{product_id}", response_model=List[schemas.InventoryLogResponse])
def get_inventory_logs(product_id: int, db: Session = Depends(get_db)):
    logs = db.query(models.InventoryLog).filter(models.InventoryLog.product_id == product_id).all()
    return logs