from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user
from app.models import WishlistItem
from app.schemas import WishlistItemCreate, WishlistItemResponse

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.get("/", response_model=List[WishlistItemResponse])
def get_wishlist(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    items = db.query(WishlistItem).filter(WishlistItem.user_id == current_user.id).all()
    # Enrich data with product details
    return [
        WishlistItemResponse(
            id=item.id, 
            product_id=item.product_id, 
            product_name=item.product.name, 
            product_price=item.product.price
        ) for item in items
    ]

@router.post("/", response_model=WishlistItemResponse)
def add_to_wishlist(item: WishlistItemCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Check if product exists
    from app.models import Product
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if already in wishlist
    existing = db.query(WishlistItem).filter(
        WishlistItem.user_id == current_user.id,
        WishlistItem.product_id == item.product_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")
        
    db_item = WishlistItem(user_id=current_user.id, product_id=item.product_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return WishlistItemResponse(
        id=db_item.id, 
        product_id=db_item.product_id, 
        product_name=product.name, 
        product_price=product.price
    )

@router.delete("/{product_id}")
def remove_from_wishlist(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    item = db.query(WishlistItem).filter(
        WishlistItem.user_id == current_user.id,
        WishlistItem.product_id == product_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in wishlist")
    
    db.delete(item)
    db.commit()
    return {"message": "Item removed from wishlist"}