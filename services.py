# services.py (Updated)
from sqlalchemy.orm import Session
import models, schemas
from repositories import ProductRepository, OrderRepository
from fastapi import HTTPException

class OrderService:
    @staticmethod
    def create_order(db: Session, user_id: int, items: list):
        product_repo = ProductRepository(db)
        order_repo = OrderRepository(db)
        
        total_price = 0
        
        # Validation Phase
        for item in items:
            product = product_repo.get_by_id(item['product_id'])
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item['product_id']} not found")
            if product.stock_quantity < item['quantity']:
                raise HTTPException(status_code=400, detail=f"Out of stock: {product.name}")
            total_price += product.price * item['quantity']

        # Save Phase
        order_data = {"user_id": user_id, "total_price": total_price}
        return order_repo.create(order_data)