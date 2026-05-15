from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import ProductRepository, OrderRepository
from app.schemas import OrderCreate

class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.order_repo = OrderRepository(db)

    def create_order(self, user_id: int, order: OrderCreate):
        total_price = 0
        order_items = []
        
        # Validation Phase
        for item in order.items:
            product = self.product_repo.get_by_id(item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Out of stock: {product.name}")
            
            item_total = product.price * item.quantity
            total_price += item_total
            
            order_items.append({
                'product_id': item.product_id,
                'quantity': item.quantity,
                'price': product.price
            })
        
        # Create order
        db_order = self.order_repo.create(user_id, order)
        
        # Add order items
        self.order_repo.add_order_items(db_order.id, order_items)
        
        # Update total price
        self.order_repo.update_total_price(db_order.id, total_price)
        
        # Update stock quantities
        for item in order_items:
            product = self.product_repo.get_by_id(item['product_id'])
            product.stock_quantity -= item['quantity']
            # TODO: Add inventory log
        
        self.db.commit()
        return self.order_repo.get_by_id(db_order.id)