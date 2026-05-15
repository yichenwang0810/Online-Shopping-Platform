from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import CartRepository, ProductRepository
from app.schemas import CartItemCreate, CartItemUpdate

class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)

    def get_cart(self, user_id: int):
        cart_items = self.cart_repo.get_user_cart(user_id)
        total = 0
        for item in cart_items:
            item.subtotal = item.product.price * item.quantity
            total += item.subtotal
        return {"items": cart_items, "total": total}

    def add_to_cart(self, user_id: int, item: CartItemCreate):
        # Check if product exists and has stock
        product = self.product_repo.get_by_id(item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        
        return self.cart_repo.add_item(user_id, item)

    def update_cart_item(self, user_id: int, product_id: int, item_update: CartItemUpdate):
        # Check stock if quantity is being updated
        if item_update.quantity:
            product = self.product_repo.get_by_id(product_id)
            if product.stock_quantity < item_update.quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock")
        
        return self.cart_repo.update_item(user_id, product_id, item_update)

    def remove_from_cart(self, user_id: int, product_id: int):
        return self.cart_repo.remove_item(user_id, product_id)

    def clear_cart(self, user_id: int):
        self.cart_repo.clear_cart(user_id)