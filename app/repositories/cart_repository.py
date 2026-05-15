from sqlalchemy.orm import Session
from app.models import CartItem
from app.schemas import CartItemCreate, CartItemUpdate

class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_cart(self, user_id: int):
        return self.db.query(CartItem).filter(CartItem.user_id == user_id).all()

    def get_cart_item(self, user_id: int, product_id: int):
        return self.db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        ).first()

    def add_item(self, user_id: int, item: CartItemCreate):
        # Check if item already exists
        existing_item = self.get_cart_item(user_id, item.product_id)
        if existing_item:
            existing_item.quantity += item.quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item
        else:
            db_item = CartItem(
                user_id=user_id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            return db_item

    def update_item(self, user_id: int, product_id: int, item_update: CartItemUpdate):
        db_item = self.get_cart_item(user_id, product_id)
        if db_item:
            update_data = item_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_item, field, value)
            self.db.commit()
            self.db.refresh(db_item)
        return db_item

    def remove_item(self, user_id: int, product_id: int):
        db_item = self.get_cart_item(user_id, product_id)
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
        return db_item

    def clear_cart(self, user_id: int):
        self.db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        self.db.commit()