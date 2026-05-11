# repositories.py
from sqlalchemy.orm import Session
import models, schemas

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Product).offset(skip).limit(limit).all()

    def get_by_id(self, product_id: int):
        return self.db.query(models.Product).filter(models.Product.id == product_id).first()

    def create(self, product: schemas.ProductCreate):
        db_product = models.Product(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_data: dict):
        db_order = models.Order(**order_data)
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order