from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.services import CartService
from app.schemas import CartItemCreate, CartItemUpdate, CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = CartService(db)
    return service.get_cart(current_user.id)

@router.post("/items")
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = CartService(db)
    return service.add_to_cart(current_user.id, item)

@router.put("/items/{product_id}")
def update_cart_item(product_id: int, item_update: CartItemUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = CartService(db)
    return service.update_cart_item(current_user.id, product_id, item_update)

@router.delete("/items/{product_id}")
def remove_from_cart(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = CartService(db)
    return service.remove_from_cart(current_user.id, product_id)

@router.delete("/")
def clear_cart(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = CartService(db)
    service.clear_cart(current_user.id)
    return {"message": "Cart cleared successfully"}