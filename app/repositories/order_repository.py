from sqlalchemy.orm import Session
from app.models import Order, OrderItem
from app.schemas import OrderCreate

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: int = None, skip: int = 0, limit: int = 100):
        query = self.db.query(Order)
        if user_id:
            query = query.filter(Order.user_id == user_id)
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()

    def create(self, user_id: int, order: OrderCreate):
        db_order = Order(user_id=user_id, total_price=0.0)
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def add_order_items(self, order_id: int, items: list):
        for item in items:
            db_item = OrderItem(
                order_id=order_id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            )
            self.db.add(db_item)
        self.db.commit()

    def update_total_price(self, order_id: int, total_price: float):
        order = self.get_by_id(order_id)
        if order:
            order.total_price = total_price
            self.db.commit()
            self.db.refresh(order)
        return order